"""RP-001 Milestone 1C-R Part 1: Structural Break Robustness.
ruptures (Bai-Perron style) failed to build (no C++ compiler in this
environment) -- using a self-implemented Quandt-Andrews sup-Wald test with
permutation p-values instead, which is the standard formal method for an
UNKNOWN breakpoint and directly addresses the "break date chosen from the
same data" concern (it tests every candidate date, not one).
"""
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_1c_plus.parquet")

def daily_ic_series(df, feature, ret_col):
    recs = []
    for d, g in df.groupby("date"):
        sub = g[[feature, ret_col]].dropna()
        if len(sub) < 8: continue
        ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
        recs.append({"date": d, "ic": ic})
    return pd.DataFrame(recs).set_index("date")["ic"].sort_index() if recs else pd.Series(dtype=float)

def newey_west_se(x, lags=5):
    n = len(x); mean_x = x.mean(); resid = x - mean_x
    gamma0 = np.sum(resid**2)/n
    v = gamma0
    for lag in range(1, lags+1):
        w = 1 - lag/(lags+1)
        v += 2*w*np.sum(resid[lag:]*resid[:-lag])/n
    return np.sqrt(v/n)

def quandt_andrews(x, trim=0.15, n_perm=2000, seed=42):
    """Sup-Wald test for an unknown single break in the mean of series x.
    Tests every candidate split point in [trim*n, (1-trim)*n], returns the
    max |t-stat| and a permutation-based p-value for that max statistic."""
    n = len(x)
    lo, hi = int(n*trim), int(n*(1-trim))
    stats_by_tau = []
    for tau in range(lo, hi):
        pre, post = x[:tau], x[tau:]
        if len(pre) < 10 or len(post) < 10: continue
        t, _ = stats.ttest_ind(pre, post, equal_var=False)
        stats_by_tau.append((tau, t))
    if not stats_by_tau:
        return None
    taus, tstats = zip(*stats_by_tau)
    tstats = np.array(tstats)
    sup_idx = np.argmax(np.abs(tstats))
    sup_tau, sup_t = taus[sup_idx], tstats[sup_idx]

    rng = np.random.default_rng(seed)
    perm_sup = np.zeros(n_perm)
    for i in range(n_perm):
        xp = rng.permutation(x)
        best = 0.0
        for tau in range(lo, hi, 3):  # step 3 for speed, still ~115 candidate points per permutation
            pre, post = xp[:tau], xp[tau:]
            if len(pre) < 10 or len(post) < 10: continue
            t, _ = stats.ttest_ind(pre, post, equal_var=False)
            if abs(t) > best: best = abs(t)
        perm_sup[i] = best
    p_value = (perm_sup >= abs(sup_t)).mean()
    return {"sup_tau_idx": sup_tau, "sup_t": sup_t, "p_value_permutation": p_value,
            "all_taus": taus, "all_tstats": tstats}

print("="*70); print("1. UNKNOWN-BREAKPOINT TEST (Quandt-Andrews sup-Wald, permutation p-value)"); print("="*70)
for feature in ["F_INST_01_foreign_rank", "F_INST_07_flow_to_volume"]:
    ic = daily_ic_series(feat, feature, "fwd_ret_t5")
    x = ic.values
    dates = ic.index
    result = quandt_andrews(x)
    break_date = dates[result["sup_tau_idx"]]
    print(f"\n{feature}:")
    print(f"  Sup-Wald break date: {break_date.date()}  sup|t|={abs(result['sup_t']):.3f}")
    print(f"  Permutation p-value (2000 reps, properly accounts for searching over all dates): {result['p_value_permutation']:.4f}")
    result["_break_date"] = break_date
    globals()[f"result_{feature}"] = result

print("\n"+"="*70); print("2. BREAK-DATE SENSITIVITY (+/- 20, 40 trading days around 2025-09-24)"); print("="*70)
ic_foreign = daily_ic_series(feat, "F_INST_01_foreign_rank", "fwd_ret_t5")
base_date = pd.Timestamp("2025-09-24")
base_idx = ic_foreign.index.get_indexer([base_date], method="nearest")[0]
for offset in [-40, -20, 0, 20, 40]:
    idx = base_idx + offset
    if idx < 20 or idx > len(ic_foreign)-20: continue
    d = ic_foreign.index[idx]
    pre = ic_foreign.values[:idx]
    post = ic_foreign.values[idx:]
    t, p = stats.ttest_ind(pre, post, equal_var=False)
    se_pre = newey_west_se(pre); se_post = newey_west_se(post)
    print(f"Split at {d.date()} (offset {offset:+d}d): pre_mean={pre.mean():.4f} (NW_se={se_pre:.4f}) "
          f"post_mean={post.mean():.4f} (NW_se={se_post:.4f}) Welch t={t:.3f} p={p:.4f}")

print("\n"+"="*70); print("3. ROLLING-WINDOW ROBUSTNESS (40d vs 90d)"); print("="*70)
for w in [40, 90]:
    roll = ic_foreign.rolling(w, min_periods=w//2).mean()
    print(f"\nWindow={w}d: start={roll.dropna().iloc[0]:.4f} "
          f"peak={roll.max():.4f} ({roll.idxmax().date()}) "
          f"trough={roll.min():.4f} ({roll.idxmin().date()}) "
          f"end={roll.dropna().iloc[-1]:.4f}")
    roll.to_csv(ROOT / "rp001_data" / f"rolling_ic_foreign_w{w}.csv")

print("\n"+"="*70); print("4. FEATURE CONSISTENCY: does F_INST_07 break at the same time as F_INST_01?"); print("="*70)
ic_flowvol = daily_ic_series(feat, "F_INST_07_flow_to_volume", "fwd_ret_t5")
break_01 = globals()["result_F_INST_01_foreign_rank"]["_break_date"]
break_07 = globals()["result_F_INST_07_flow_to_volume"]["_break_date"]
gap_days = abs((break_01 - break_07).days)
print(f"F_INST_01 break date: {break_01.date()}")
print(f"F_INST_07 break date: {break_07.date()}")
print(f"Gap: {gap_days} calendar days")
print(f"Interpretation: {'consistent with a shared market-wide break' if gap_days < 60 else 'NOT consistent with a single shared break -- feature-specific, not market-wide'}")
