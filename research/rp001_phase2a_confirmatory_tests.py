"""
RP-001 Phase 2A.4: Confirmatory hypothesis tests H-C1 through H-C5.

Exactly the five pre-registered hypotheses (RP001_CONFIRMATORY_HYPOTHESES.md),
judged per RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md. Statistical methods
(Spearman rank IC, Newey-West t, cross-sectional OLS residualization,
Benjamini-Hochberg FDR alpha=0.10) reused unchanged from the exploratory
phase's validated code (rp001_interaction_incremental.py,
rp001_regime_robustness.py). No new sub-cuts beyond what H-C1-H-C5 specify.
"""
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
PROC_DIR = ROOT / "rp001_data" / "phase2a" / "processed"

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def daily_ic(df, feature, ret_col, min_n=8):
    """Vectorized daily Spearman IC: rank both columns within-date, then a
    closed-form per-date Pearson correlation on the ranks (equivalent to
    Spearman) via groupby.agg sums -- avoids a Python-level per-date loop
    calling scipy.stats.spearmanr, which is the bottleneck at full-universe
    scale (thousands of dates x up to ~2000 stocks/day)."""
    sub = df[["date", feature, ret_col]].dropna()
    if len(sub) == 0:
        return pd.DataFrame(columns=["date", "ic", "n"]).set_index("date")
    g = sub.groupby("date")
    x = g[feature].rank(pct=True)
    y = g[ret_col].rank(pct=True)
    tmp = pd.DataFrame({"date": sub["date"].values, "x": x.values, "y": y.values})
    grp = tmp.groupby("date")
    n = grp["x"].transform("count")
    tmp = tmp[n >= min_n]
    if len(tmp) == 0:
        return pd.DataFrame(columns=["date", "ic", "n"]).set_index("date")
    # closed-form correlation via sums: corr = (n*sxy - sx*sy) / sqrt((n*sxx - sx^2)(n*syy - sy^2))
    sums = tmp.assign(xy=tmp["x"] * tmp["y"], xx=tmp["x"] ** 2, yy=tmp["y"] ** 2).groupby("date").agg(
        n=("x", "count"), sx=("x", "sum"), sy=("y", "sum"), sxy=("xy", "sum"), sxx=("xx", "sum"), syy=("yy", "sum"))
    num = sums["n"] * sums["sxy"] - sums["sx"] * sums["sy"]
    den = np.sqrt((sums["n"] * sums["sxx"] - sums["sx"] ** 2) * (sums["n"] * sums["syy"] - sums["sy"] ** 2))
    ic = (num / den).replace([np.inf, -np.inf], np.nan)
    out = pd.DataFrame({"ic": ic, "n": sums["n"]}).dropna()
    return out.sort_index()


def newey_west_tstat(x, lags=5):
    x = np.asarray(x, dtype=float)
    n = len(x)
    if n < 2:
        return np.nan, np.nan
    mean_x = x.mean()
    resid = x - mean_x
    gamma0 = np.sum(resid ** 2) / n
    v = gamma0
    for lag in range(1, min(lags, n - 1) + 1):
        w = 1 - lag / (lags + 1)
        v += 2 * w * np.sum(resid[lag:] * resid[:-lag]) / n
    se = np.sqrt(v / n) if v > 0 else np.nan
    t = mean_x / se if se and se > 0 else np.nan
    return t, se


def ic_stats(ic_df, label):
    if len(ic_df) == 0:
        return {"label": label, "n": 0, "mean_ic": np.nan, "median_ic": np.nan,
                "t_nw": np.nan, "ci_low": np.nan, "ci_high": np.nan, "raw_p": np.nan}
    ic = ic_df["ic"].values
    n = len(ic)
    mean_ic = ic.mean()
    median_ic = np.median(ic)
    t_nw, se = newey_west_tstat(ic)
    ci_low, ci_high = (mean_ic - 1.96 * se, mean_ic + 1.96 * se) if se and pd.notna(se) else (np.nan, np.nan)
    raw_p = 2 * (1 - stats.norm.cdf(abs(t_nw))) if pd.notna(t_nw) else np.nan
    return {"label": label, "n": int(n), "mean_ic": float(mean_ic), "median_ic": float(median_ic),
            "t_nw": float(t_nw) if pd.notna(t_nw) else None,
            "ci_low": float(ci_low) if pd.notna(ci_low) else None,
            "ci_high": float(ci_high) if pd.notna(ci_high) else None,
            "raw_p": float(raw_p) if pd.notna(raw_p) else None}


def bh_fdr(pvals, alpha=0.10):
    """Benjamini-Hochberg FDR. Returns q-values aligned to input order."""
    pvals = np.asarray(pvals, dtype=float)
    n = len(pvals)
    valid = ~np.isnan(pvals)
    q = np.full(n, np.nan)
    idx = np.where(valid)[0]
    order = idx[np.argsort(pvals[idx])]
    m = len(order)
    prev_q = 1.0
    ranked_q = np.zeros(m)
    for rank, i in enumerate(order[::-1]):
        r = m - rank
        val = pvals[i] * m / r
        prev_q = min(prev_q, val)
        ranked_q[m - rank - 1] = prev_q
    for pos, i in enumerate(order):
        q[i] = ranked_q[pos]
    return q


def neutralize(df, feature, controls):
    """Cross-sectional OLS residualization, per date, against `controls`."""
    out = pd.Series(index=df.index, dtype=float)
    for d, g in df.groupby("date"):
        y = g[feature].values
        X_cols = [np.ones(len(g))]
        for c in controls:
            X_cols.append(g[c].values)
        X = np.column_stack(X_cols)
        valid = ~np.isnan(y) & ~np.isnan(X).any(axis=1)
        if valid.sum() < X.shape[1] + 2:
            continue
        beta, *_ = np.linalg.lstsq(X[valid], y[valid], rcond=None)
        resid = np.full(len(g), np.nan)
        resid[valid] = y[valid] - X[valid] @ beta
        out.loc[g.index] = resid
    return out


def main():
    log("Loading confirmatory dataset...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_dataset_v0.1.parquet")
    log(f"Panel: {len(panel):,} rows")

    sample = panel[panel["in_confirmatory_sample"] == True].copy()
    log(f"Confirmatory sample (coverage-gate-passing stocks): {len(sample):,} rows, "
        f"{sample['stock_id'].nunique()} stocks")

    results = {}
    all_primary_tests = []  # (test_id, stat_dict) for joint BH-FDR
    results_path = PROC_DIR / "rp001_confirmatory_test_results.json"

    def checkpoint():
        with open(results_path, "w", encoding="utf-8") as f:
            json.dump({"generated_utc": pd.Timestamp.now(tz="UTC").isoformat(),
                       "partial": True, "results": results}, f, indent=2, default=str)

    # ================= H-C1: pre-break positive IC =================
    log("H-C1: pre-break positive predictive power...")
    pre = sample[sample["break_period"] == "pre"]
    hc1 = {}
    for h in [1, 3, 5]:
        ic_df = daily_ic(pre, "F_INST_01_foreign_rank", f"fwd_ret_t{h}")
        st = ic_stats(ic_df, f"H-C1 t+{h}")
        hc1[f"t{h}"] = st
        all_primary_tests.append((f"H-C1_t{h}", st))
    results["H-C1"] = hc1
    checkpoint()

    # ================= H-C2: post-break null =================
    log("H-C2: post-break null effect (t+5)...")
    post = sample[sample["break_period"] == "post"]
    ic_df = daily_ic(post, "F_INST_01_foreign_rank", "fwd_ret_t5")
    hc2 = {"t5": ic_stats(ic_df, "H-C2 t+5")}
    all_primary_tests.append(("H-C2_t5", hc2["t5"]))
    results["H-C2"] = hc2
    checkpoint()

    # ================= H-C3: liquidity conditionality =================
    log("H-C3: liquidity conditionality (t+5, full sample)...")
    hc3 = {}
    for tercile in ["Illiquid", "Mid", "Liquid"]:
        sub = sample[sample["liq_tercile"] == tercile]
        ic_df = daily_ic(sub, "F_INST_01_foreign_rank", "fwd_ret_t5")
        st = ic_stats(ic_df, f"H-C3 {tercile}")
        hc3[tercile] = st
        all_primary_tests.append((f"H-C3_{tercile}", st))
    results["H-C3"] = hc3
    checkpoint()

    # ================= H-C4: volatility x break double-sort =================
    log("H-C4: volatility-regime x break-period double-sort (t+5)...")
    hc4 = {}
    for vol in ["LowVol", "HighVol"]:
        for bp in ["pre", "post"]:
            sub = sample[(sample["market_vol_regime"] == vol) & (sample["break_period"] == bp)]
            ic_df = daily_ic(sub, "F_INST_01_foreign_rank", "fwd_ret_t5")
            key = f"{vol}_{bp}"
            st = ic_stats(ic_df, f"H-C4 {key}")
            hc4[key] = st
            all_primary_tests.append((f"H-C4_{key}", st))
    results["H-C4"] = hc4
    checkpoint()

    # ================= H-C5: interaction residualization =================
    log("H-C5: interaction feature residualization (5 constructible + 2 inconclusive)...")
    hc5 = {}
    INT_SPECS = [
        ("F_INT_01_flow_x_momentum", "F_INST_05_aggregate_rank", "_mom20_rank"),
        ("F_INT_03_flow_x_liquidity", "F_INST_05_aggregate_rank", "_adv20_rank"),
        ("F_INT_04_foreign_x_liquidity", "F_INST_01_foreign_rank", "_adv20_rank"),
        ("F_INT_05_foreign_x_volatility", "F_INST_01_foreign_rank", "_rvol20_rank"),
        ("F_INT_07_foreign_x_momentum", "F_INST_01_foreign_rank", "_mom20_rank"),
    ]
    sample = sample.reset_index(drop=True)
    for feat, c1, c2 in INT_SPECS:
        log(f"  residualizing {feat}...")
        raw_ic = {h: ic_stats(daily_ic(sample, feat, f"fwd_ret_t{h}"), f"{feat} raw t+{h}") for h in [1, 3, 5]}
        resid = neutralize(sample, feat, [c1, c2])
        sample["_resid_tmp"] = resid
        resid_ic = {h: ic_stats(daily_ic(sample, "_resid_tmp", f"fwd_ret_t{h}"), f"{feat} resid t+{h}") for h in [1, 3, 5]}
        hc5[feat] = {"raw": raw_ic, "residualized": resid_ic, "constructible": True}
        all_primary_tests.append((f"H-C5_{feat}_resid_t5", resid_ic[5]))
        results["H-C5"] = hc5
        checkpoint()
    for feat in ["F_INT_02_flow_x_size", "F_INT_06_foreign_x_size"]:
        hc5[feat] = {"raw": None, "residualized": None, "constructible": False,
                     "reason": "Deviation D-08: market capitalization data unavailable at full-universe confirmatory scale"}
    results["H-C5"] = hc5

    # ================= Joint Benjamini-Hochberg FDR (alpha=0.10) across all primary tests =================
    log(f"Applying joint BH-FDR (alpha=0.10) across {len(all_primary_tests)} primary tests...")
    pvals = [st["raw_p"] if st and st.get("raw_p") is not None else np.nan for _, st in all_primary_tests]
    qvals = bh_fdr(pvals, alpha=0.10)
    fdr_table = []
    for (test_id, st), q in zip(all_primary_tests, qvals):
        fdr_table.append({"test_id": test_id, "n": st.get("n"), "mean_ic": st.get("mean_ic"),
                           "t_nw": st.get("t_nw"), "raw_p": st.get("raw_p"),
                           "q_bh": float(q) if pd.notna(q) else None,
                           "significant_q10": bool(pd.notna(q) and q < 0.10)})

    out = {
        "generated_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "confirmatory_sample_stocks": int(sample["stock_id"].nunique()),
        "confirmatory_sample_rows": int(len(sample)),
        "results": results,
        "multiple_testing": {"method": "Benjamini-Hochberg", "alpha": 0.10, "n_tests": len(all_primary_tests),
                              "table": fdr_table},
    }
    with open(PROC_DIR / "rp001_confirmatory_test_results.json", "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, default=str)
    log(f"Saved: {PROC_DIR / 'rp001_confirmatory_test_results.json'}")

    # ---- console summary ----
    log("\n" + "=" * 70)
    log("H-C1 (pre-break positive IC):")
    for h in [1, 3, 5]:
        st = hc1[f"t{h}"]
        log(f"  t+{h}: mean_ic={st['mean_ic']:.4f} median_ic={st['median_ic']:.4f} t_nw={st['t_nw']:.3f} n={st['n']}")
    log("H-C2 (post-break null, t+5):")
    st = hc2["t5"]
    log(f"  mean_ic={st['mean_ic']:.4f} t_nw={st['t_nw']:.3f} n={st['n']}")
    log("H-C3 (liquidity conditionality, t+5):")
    for k, st in hc3.items():
        log(f"  {k}: mean_ic={st['mean_ic']:.4f} t_nw={st['t_nw']:.3f} n={st['n']}")
    log("H-C4 (volatility x break double-sort, t+5):")
    for k, st in hc4.items():
        log(f"  {k}: mean_ic={st['mean_ic']:.4f} t_nw={st['t_nw']:.3f} n={st['n']}")
    log("H-C5 (interaction residualization, t+5):")
    for feat, d in hc5.items():
        if d["constructible"]:
            r = d["residualized"][5]
            log(f"  {feat}: residual_mean_ic={r['mean_ic']:.4f} t_nw={r['t_nw']:.3f} n={r['n']}")
        else:
            log(f"  {feat}: NOT CONSTRUCTIBLE ({d['reason']})")
    log("DONE")


if __name__ == "__main__":
    main()
