from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_1c_plus.parquet")
price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw_price").glob("price_*.csv"))], ignore_index=True)
price = price.rename(columns={"Trading_Volume":"volume"})
price["date"] = pd.to_datetime(price["date"])
price = price.sort_values(["stock_id","date"])
price["ret1d"] = price.groupby("stock_id")["close"].pct_change()

def daily_ic_series(df, feature, ret_col):
    recs = []
    for d, g in df.groupby("date"):
        sub = g[[feature, ret_col]].dropna()
        if len(sub) < 8: continue
        ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
        recs.append({"date": d, "ic": ic})
    return pd.DataFrame(recs).set_index("date")["ic"].sort_index() if recs else pd.Series(dtype=float)

def newey_west_tstat(x, lags=5):
    n = len(x); mean_x = x.mean(); resid = x - mean_x
    gamma0 = np.sum(resid**2)/n
    v = gamma0
    for lag in range(1, lags+1):
        w = 1 - lag/(lags+1)
        v += 2*w*np.sum(resid[lag:]*resid[:-lag])/n
    se = np.sqrt(v/n)
    return mean_x/se if se>0 else np.nan, se

RET = "fwd_ret_t5"
ic_series = daily_ic_series(feat, "F_INST_01_foreign_rank", RET)

print("="*70); print("PRE-COMMITTED PRIMARY SPEC: market realized vol (20d), MEDIAN split"); print("="*70)
print("(This was the spec already used in Milestone 1C+, stated as primary BEFORE this robustness pass,")
print(" not selected after comparing thresholds -- reported here for traceability.)\n")

# ---- Build multiple volatility definitions ----
mkt_close = price.groupby("date")["close"].mean().sort_index()
mkt_ret = mkt_close.pct_change()

vol_defs = {}
vol_defs["market_rvol_20d"] = mkt_ret.rolling(20, min_periods=10).std() * np.sqrt(252)
vol_defs["market_rvol_40d"] = mkt_ret.rolling(40, min_periods=20).std() * np.sqrt(252)
# cross-sectional return dispersion: daily std of returns ACROSS the 50 stocks
xsec_disp = price.groupby("date")["ret1d"].std()
vol_defs["xsec_dispersion_raw"] = xsec_disp
vol_defs["xsec_dispersion_20d_smooth"] = xsec_disp.rolling(20, min_periods=10).mean()

results = []
for vol_name, vol_series in vol_defs.items():
    for split_type in ["median", "tercile_extremes"]:
        aligned = vol_series.reindex(ic_series.index)
        if split_type == "median":
            thresh = aligned.median()
            low_mask = aligned <= thresh
            high_mask = aligned > thresh
            label = f"{vol_name} (median={thresh:.4f})"
        else:
            q33, q66 = aligned.quantile([0.333, 0.667])
            low_mask = aligned <= q33
            high_mask = aligned > q66
            label = f"{vol_name} (tercile: low<={q33:.4f}, high>{q66:.4f})"

        for regime_name, mask in [("Low", low_mask), ("High", high_mask)]:
            sub = ic_series[mask.fillna(False)]
            if len(sub) < 15: continue
            t_nw, se_nw = newey_west_tstat(sub.values)
            ci_low, ci_high = sub.mean()-1.96*se_nw, sub.mean()+1.96*se_nw
            results.append({"vol_definition": vol_name, "split": split_type, "regime": regime_name,
                            "n_days": len(sub), "mean_ic": sub.mean(), "t_nw": t_nw,
                            "ci95_low": ci_low, "ci95_high": ci_high, "pos_ratio": (sub>0).mean()})

res_df = pd.DataFrame(results)
pd.set_option("display.width", 200)
print(res_df.round(4).to_string(index=False))
res_df.to_csv(ROOT / "rp001_data" / "regime_robustness_full.csv", index=False)

print("\n"+"="*70); print("DOUBLE-SORT: Low-vol effect vs Pre-break-period effect vs 2024-only effect"); print("="*70)
vol20 = vol_defs["market_rvol_20d"].reindex(ic_series.index)
low_vol_mask = vol20 <= vol20.median()
pre_break_mask = pd.Series(ic_series.index < pd.Timestamp("2025-09-24"), index=ic_series.index)
year_2024_mask = pd.Series(ic_series.index.year == 2024, index=ic_series.index)

cells = {
    "Low-vol & Pre-break": low_vol_mask & pre_break_mask,
    "Low-vol & Post-break": low_vol_mask & ~pre_break_mask,
    "High-vol & Pre-break": ~low_vol_mask & pre_break_mask,
    "High-vol & Post-break": ~low_vol_mask & ~pre_break_mask,
}
for name, mask in cells.items():
    sub = ic_series[mask.fillna(False)]
    if len(sub) < 10:
        print(f"{name}: n={len(sub)} (too few for reliable stat)")
        continue
    t_nw, se = newey_west_tstat(sub.values)
    print(f"{name}: n={len(sub)}  mean_ic={sub.mean():.4f}  t_nw={t_nw:.3f}")

print("\n2024-only vs Low-vol-only decomposition:")
only_2024 = ic_series[year_2024_mask.fillna(False)]
only_lowvol_not2024 = ic_series[(low_vol_mask & ~year_2024_mask).fillna(False)]
print(f"2024 (any vol regime): n={len(only_2024)} mean_ic={only_2024.mean():.4f}")
print(f"Low-vol, but NOT 2024 (2025-2026 low-vol days): n={len(only_lowvol_not2024)} mean_ic={only_lowvol_not2024.mean():.4f}")
print("If the second number is still clearly positive, low-vol effect is NOT purely a 2024 artifact.")
print("If it collapses toward zero, the 'low-vol effect' may just be relabeling the 2024 effect.")
