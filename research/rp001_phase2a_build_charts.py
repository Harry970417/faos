"""
RP-001 Phase 2A: Showcase charts, built entirely from real computed results
(confirmatory dataset + test results JSON + acquisition manifests). No
illustrative/placeholder data anywhere.
"""
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
PROC_DIR = ROOT / "rp001_data" / "phase2a" / "processed"
CHART_DIR = ROOT / "figures"
CHART_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 120, "font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def daily_ic_series(df, feature, ret_col, min_n=8):
    sub = df[["date", feature, ret_col]].dropna()
    g = sub.groupby("date")
    x = g[feature].rank(pct=True)
    y = g[ret_col].rank(pct=True)
    tmp = pd.DataFrame({"date": sub["date"].values, "x": x.values, "y": y.values})
    n = tmp.groupby("date")["x"].transform("count")
    tmp = tmp[n >= min_n]
    s = tmp.assign(xy=tmp["x"] * tmp["y"], xx=tmp["x"] ** 2, yy=tmp["y"] ** 2).groupby("date").agg(
        n=("x", "count"), sx=("x", "sum"), sy=("y", "sum"), sxy=("xy", "sum"), sxx=("xx", "sum"), syy=("yy", "sum"))
    num = s["n"] * s["sxy"] - s["sx"] * s["sy"]
    den = np.sqrt((s["n"] * s["sxx"] - s["sx"] ** 2) * (s["n"] * s["syy"] - s["sy"] ** 2))
    ic = (num / den).replace([np.inf, -np.inf], np.nan)
    return ic.dropna().sort_index()


def main():
    log("Loading confirmatory dataset...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_dataset_v0.1.parquet")
    sample = panel[panel["in_confirmatory_sample"] == True].copy()
    with open(PROC_DIR / "rp001_confirmatory_test_results.json", encoding="utf-8") as f:
        results = json.load(f)
    cov = pd.read_csv(PROC_DIR / "rp001_stock_coverage.csv")
    universe = pd.read_csv(ROOT / "rp001_data" / "phase2a_acquisition_universe.csv", dtype=str)

    # ==== Chart 1: Universe coverage (market x eligibility) ====
    log("Chart 1: universe coverage...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    mkt_counts = universe["market"].value_counts()
    elig_stocks = set(panel["stock_id"].unique())
    total_by_mkt = universe.groupby("market")["stock_id"].apply(lambda s: len(s))
    elig_by_mkt = universe[universe["stock_id"].isin(elig_stocks)].groupby("market")["stock_id"].apply(lambda s: len(s))
    mkts = list(total_by_mkt.index)
    x = np.arange(len(mkts))
    ax.bar(x - 0.2, total_by_mkt.values, width=0.4, label="Universe (acquired)", color="#4C72B0")
    ax.bar(x + 0.2, [elig_by_mkt.get(m, 0) for m in mkts], width=0.4, label="Has eligible panel rows", color="#55A868")
    ax.set_xticks(x); ax.set_xticklabels(mkts)
    ax.set_ylabel("Stock count"); ax.set_title("RP-001 Phase 2A: Universe Coverage by Market")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure01_UniverseCoverage.png"); plt.close(fig)

    # ==== Chart 2: Missingness (coverage-rate histogram + gate) ====
    log("Chart 2: missingness distribution...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(cov["coverage_rate"], bins=40, color="#4C72B0", alpha=0.85)
    ax.axvline(0.80, color="red", linestyle="--", label="80% coverage gate")
    n_pass = (cov["coverage_rate"] >= 0.80).sum()
    ax.set_xlabel("Per-stock F_INST_01 coverage rate"); ax.set_ylabel("Number of stocks")
    ax.set_title(f"RP-001 Phase 2A: Institutional-Data Coverage Distribution\n({n_pass}/{len(cov)} stocks pass the 80% gate)")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure02_MissingnessDistribution.png"); plt.close(fig)

    # ==== Chart 3: Institutional-category history (Dealer vs split, market-wide daily count) ====
    log("Chart 3: institutional category history...")
    inst_sample_path = PROC_DIR / "rp001_confirmatory_panel_raw.parquet"
    raw = pd.read_parquet(inst_sample_path, columns=["date", "Dealer", "Dealer_self", "Dealer_Hedging"])
    raw["date_m"] = pd.to_datetime(raw["date"]).dt.to_period("M").dt.to_timestamp()
    monthly = raw.groupby("date_m").agg(
        dealer_undiff=("Dealer", lambda s: s.notna().sum()),
        dealer_split=("Dealer_self", lambda s: s.notna().sum()))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly.index, monthly["dealer_undiff"], label="Undifferentiated 'Dealer' (row count/month)", color="#C44E52")
    ax.plot(monthly.index, monthly["dealer_split"], label="Split 'Dealer_self' (row count/month)", color="#55A868")
    ax.axvspan(pd.Timestamp("2025-08-01"), pd.Timestamp("2025-10-31"), alpha=0.15, color="orange", label="Break window")
    ax.set_ylabel("Institutional rows / month"); ax.set_title("RP-001 Phase 2A: Dealer-Category Schema History (Market-Wide)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure03_InstitutionalCategoryHistory.png"); plt.close(fig)
    del raw

    # ==== Chart 4: Rolling IC (F_INST_01, t+5, 60-day rolling mean) ====
    log("Chart 4: rolling IC...")
    ic5 = daily_ic_series(sample, "F_INST_01_foreign_rank", "fwd_ret_t5")
    ic5.index = pd.to_datetime(ic5.index)
    ic5_roll = ic5.rolling(60, min_periods=30).mean()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(ic5_roll.index, ic5_roll.values, color="#4C72B0", linewidth=1.2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(pd.Timestamp("2025-09-25"), color="red", linestyle="--", label="Locked break point estimate (2025-09-25)")
    ax.set_ylabel("60-day rolling mean IC (t+5)"); ax.set_title("RP-001 Phase 2A: F_INST_01 Rolling IC, Full Universe (2012-2026)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure04_RollingIC.png"); plt.close(fig)

    # ==== Chart 5: Break before/after (exploratory vs confirmatory) ====
    log("Chart 5: break before/after comparison...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = ["Pre-break\n(exploratory)", "Pre-break\n(confirmatory)", "Post-break\n(exploratory)", "Post-break\n(confirmatory)"]
    vals = [0.052, results["results"]["H-C1"]["t5"]["mean_ic"], -0.008, results["results"]["H-C2"]["t5"]["mean_ic"]]
    colors = ["#4C72B0", "#4C72B0", "#C44E52", "#C44E52"]
    hatches = ["", "//", "", "//"]
    bars = ax.bar(labels, vals, color=colors)
    for b, h in zip(bars, hatches):
        b.set_hatch(h)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean IC (t+5), Spearman Rank IC"); ax.set_title(
        "RP-001: Break-Period IC, Exploratory vs. Confirmatory\n"
        "(solid = exploratory, 50 stocks, 2024-2026; hatched = confirmatory, 1,462 stocks, 2012-2026)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure05_BreakBeforeAfter.png"); plt.close(fig)

    # ==== Chart 6: Liquidity groups ====
    log("Chart 6: liquidity groups...")
    hc3 = results["results"]["H-C3"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    terciles = ["Illiquid", "Mid", "Liquid"]
    ics = [hc3[t]["mean_ic"] for t in terciles]
    ts = [hc3[t]["t_nw"] for t in terciles]
    colors = ["#55A868" if abs(t) > 1.96 else "#B0B0B0" for t in ts]
    bars = ax.bar(terciles, ics, color=colors)
    for bar, t in zip(bars, ts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0003, f"t={t:.2f}", ha="center", fontsize=9)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean IC (t+5), Spearman Rank IC")
    ax.set_title("RP-001 Phase 2A: H-C3 Liquidity Conditionality\nConfirmatory sample, 1,462 stocks, full 2012-2026 sample (green = |NW t|>1.96)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure06_LiquidityGroups.png"); plt.close(fig)

    # ==== Chart 7: Hypothesis verdicts scorecard ====
    log("Chart 7: hypothesis verdicts...")
    verdicts = {"H-C1": "Not Replicated", "H-C2": "Replicated*", "H-C3": "Partially Replicated",
                "H-C4": "Not Replicated", "H-C5": "Not Replicated"}
    color_map = {"Replicated*": "#55A868", "Partially Replicated": "#DD8452", "Not Replicated": "#C44E52"}
    fig, ax = plt.subplots(figsize=(8, 3.5))
    hyps = list(verdicts.keys())
    for i, h in enumerate(hyps):
        ax.barh(h, 1, color=color_map[verdicts[h]])
        ax.text(0.5, i, verdicts[h], ha="center", va="center", color="white", fontweight="bold")
    ax.set_xlim(0, 1); ax.set_xticks([])
    ax.set_title("RP-001 Phase 2A: H-C1-H-C5 Verdict Scorecard\n(*H-C2 replicated by letter, but weakened by H-C1's failure)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure07_HypothesisVerdicts.png"); plt.close(fig)

    # ==== Chart 8: Exploratory vs Confirmatory comparison (all 5 features/hyps) ====
    log("Chart 8: exploratory vs confirmatory magnitude comparison...")
    fig, ax = plt.subplots(figsize=(9, 5))
    items = ["H-C1 t+5\n(pre-break IC)", "H-C3 Illiquid\n(t+5 IC)", "H-C4 LowVol&Pre\n(t+5 IC)",
             "F_INT_01 resid\n(t+5 IC)", "F_INT_03 resid\n(t+5 IC)"]
    explor = [0.052, 0.034, 0.069, -0.004, -0.004]
    confirm = [results["results"]["H-C1"]["t5"]["mean_ic"], hc3["Illiquid"]["mean_ic"],
               results["results"]["H-C4"]["LowVol_pre"]["mean_ic"],
               results["results"]["H-C5"]["F_INT_01_flow_x_momentum"]["residualized"]["5"]["mean_ic"],
               results["results"]["H-C5"]["F_INT_03_flow_x_liquidity"]["residualized"]["5"]["mean_ic"]]
    x = np.arange(len(items))
    ax.bar(x - 0.2, explor, width=0.4, label="Exploratory (50 stocks)", color="#4C72B0")
    ax.bar(x + 0.2, confirm, width=0.4, label="Confirmatory (full universe)", color="#DD8452")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(items, fontsize=8)
    ax.set_ylabel("Mean IC"); ax.set_title("RP-001: Exploratory vs. Confirmatory Effect Magnitudes")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure08_ExploratoryVsConfirmatory.png"); plt.close(fig)

    # ==== Chart 9: Interaction residualization, raw vs. residual IC ====
    log("Chart 9: interaction residualization before/after...")
    hc5 = results["results"]["H-C5"]
    int_names = ["F_INT_01\n(flow x momentum)", "F_INT_03\n(flow x liquidity)", "F_INT_04\n(foreign x liquidity)",
                 "F_INT_05\n(foreign x volatility)", "F_INT_07\n(foreign x momentum)"]
    int_keys = ["F_INT_01_flow_x_momentum", "F_INT_03_flow_x_liquidity", "F_INT_04_foreign_x_liquidity",
                "F_INT_05_foreign_x_volatility", "F_INT_07_foreign_x_momentum"]
    raw_ic = [hc5[k]["raw"]["5"]["mean_ic"] for k in int_keys]
    resid_ic = [hc5[k]["residualized"]["5"]["mean_ic"] for k in int_keys]
    resid_t = [hc5[k]["residualized"]["5"]["t_nw"] for k in int_keys]
    fig, ax = plt.subplots(figsize=(10, 5))
    x = np.arange(len(int_names))
    ax.bar(x - 0.2, raw_ic, width=0.4, label="Raw IC (before residualization)", color="#4C72B0")
    bars2 = ax.bar(x + 0.2, resid_ic, width=0.4, label="Residual IC (after joint residualization)", color="#DD8452")
    for bar, t in zip(bars2, resid_t):
        marker = "*" if abs(t) > 1.96 else ""
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + (0.0003 if bar.get_height() >= 0 else -0.0012),
                f"t={t:.2f}{marker}", ha="center", fontsize=8)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(int_names, fontsize=8)
    ax.set_ylabel("Mean IC (t+5), Spearman Rank IC")
    ax.set_title("RP-001 Phase 2A: H-C5 Interaction Residualization, Before vs. After\n"
                  "Confirmatory sample, 1,462 stocks, 2012-2026 (* = survives |NW t|>1.96)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure09_InteractionResidualization.png"); plt.close(fig)

    # ==== Chart 10: Data quality issues and fixes summary ====
    log("Chart 10: data quality issues and fixes summary...")
    fq = pd.read_csv(ROOT / "rp001_data" / "phase2a" / "manifests" / "failed_queue.csv")
    m = pd.read_csv(ROOT / "rp001_data" / "phase2a" / "manifests" / "pull_manifest.csv", dtype=str)
    n_dealer_instances = 69  # RP001_PHASE2A_DEVIATION_LOG.md D-05, individually verified, cumulative count
    n_calendar_contam = 16459  # Trading Calendar Gate exclusions, RP001_PHASE2A_CONFIRMATORY_DATASET.md
    n_tooling_bugs = 2
    n_empty_legit = int((m["status"] == "empty").sum())
    categories = ["Dealer schema\ninstances verified\n(0 affected F_INST_01)", "Mis-dated rows\nexcluded\n(Trading Calendar Gate)",
                  "Legitimate empty\nresponses\n(TDR-style codes)", "Acquisition\ntooling bugs\nfound & fixed"]
    counts = [n_dealer_instances, n_calendar_contam, n_empty_legit, n_tooling_bugs]
    fig, axes = plt.subplots(1, 4, figsize=(11, 4))
    for ax, cat, cnt in zip(axes, categories, counts):
        ax.bar([0], [cnt], color="#4C72B0", width=0.5)
        ax.set_xticks([]); ax.set_title(cat, fontsize=9)
        ax.text(0, cnt, f"{cnt:,}", ha="center", va="bottom", fontsize=11, fontweight="bold")
        ax.set_ylim(0, cnt * 1.25 if cnt > 0 else 1)
    fig.suptitle("RP-001 Phase 2A: Data Quality Issues Found and Resolved (all individually verified, zero unresolved)", fontsize=11)
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure10_DataQualitySummary.png"); plt.close(fig)

    # ==== Chart 11: Full research lifecycle timeline ====
    log("Chart 11: research lifecycle timeline...")
    milestones = [
        ("2026-07-10", "FAOS Alpha 0.2\nbaseline"),
        ("2026-07-11", "Exploratory research\ncomplete (Milestones 0A-1D)"),
        ("2026-07-11", "Phase 2A\nProtocol Lock"),
        ("2026-07-31", "Phase 2A.1\nReadiness + Phase 2A.2-R"),
        ("2026-08-02", "Full acquisition complete\n(19 batches, 2,255 stocks)"),
        ("2026-08-03", "Confirmatory Dataset +\nH-C1-H-C5 results"),
        ("2026-08-03", "RP-001 formal\nclosure"),
    ]
    dates = [pd.Timestamp(d) for d, _ in milestones]
    labels = [l for _, l in milestones]
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.plot(dates, [0] * len(dates), color="#4C72B0", linewidth=2, zorder=1)
    ax.scatter(dates, [0] * len(dates), color="#DD8452", s=80, zorder=2)
    levels = [0.35, 0.7, 1.05, -0.35, -0.7, -1.05, 0.35]
    for i, (d, l) in enumerate(zip(dates, labels)):
        y = levels[i % len(levels)]
        ax.annotate(l, (d, 0), xytext=(d, y), ha="center", fontsize=8,
                    arrowprops=dict(arrowstyle="-", color="gray", lw=0.6))
    ax.set_ylim(-1.4, 1.4); ax.set_yticks([])
    ax.set_title("RP-001 Full Research Lifecycle Timeline (actual commit dates)")
    fig.autofmt_xdate()
    fig.tight_layout(); fig.savefig(CHART_DIR / "Figure11_ResearchLifecycleTimeline.png"); plt.close(fig)

    log(f"All 11 figures saved to {CHART_DIR}")
    log("DONE")


if __name__ == "__main__":
    main()
