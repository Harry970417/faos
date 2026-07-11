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
    if not recs:
        return pd.Series(dtype=float)
    return pd.DataFrame(recs).set_index("date")["ic"]

def group_ic(df, feature, ret_col, group_col):
    out = []
    for gv, gdf in df.groupby(group_col, observed=True):
        s = daily_ic_series(gdf, feature, ret_col)
        if len(s) >= 5:
            out.append({group_col: gv, "n_days": len(s), "mean_ic": s.mean(),
                        "icir": s.mean()/s.std() if s.std()>0 else np.nan, "pos_ratio": (s>0).mean()})
    return pd.DataFrame(out)

RET = "fwd_ret_t5"

print("="*70); print("1. STRUCTURAL BREAK: Rolling IC + Break Detection"); print("="*70)
ic_series = daily_ic_series(feat, "F_INST_01_foreign_rank", RET).sort_index()
rolling_ic = ic_series.rolling(60, min_periods=30).mean()
rolling_ic.to_csv(ROOT / "rp001_data" / "rolling_ic_foreign.csv")
print(f"Rolling 60-day IC (F_INST_01_foreign, t+5): range {rolling_ic.min():.4f} to {rolling_ic.max():.4f}")
print(f"Rolling IC at start: {rolling_ic.dropna().iloc[0]:.4f}  at end: {rolling_ic.dropna().iloc[-1]:.4f}")

# Break detection: simple CUSUM-style test on the IC series
x = ic_series.dropna().values
n = len(x)
mean_x = x.mean()
cusum = np.cumsum(x - mean_x)
break_idx = np.argmax(np.abs(cusum))
break_date = ic_series.dropna().index[break_idx]
print(f"\nCUSUM break detection: max |cumulative deviation| at index {break_idx} -> date {break_date.date()}")
pre = x[:break_idx]; post = x[break_idx:]
t_break, p_break = stats.ttest_ind(pre, post, equal_var=False)
print(f"Pre-break mean IC: {pre.mean():.4f} (n={len(pre)})  Post-break mean IC: {post.mean():.4f} (n={len(post)})")
print(f"Welch t-test for break significance: t={t_break:.3f} p={p_break:.4f}")

print("\n"+"="*70); print("2. CROSS-SECTIONAL STABILITY"); print("="*70)
for col, label in [("mcap_tercile","Market Cap"), ("sector","Industry"), ("pbr_tercile","Value/Growth (PBR)"), ("liq_tercile","Liquidity")]:
    print(f"\n-- {label} --")
    g = group_ic(feat, "F_INST_01_foreign_rank", RET, col)
    if col == "sector":
        g = g[g["n_days"] >= 100]  # only well-populated sectors
    print(g.round(4).to_string(index=False))

print("\n"+"="*70); print("3. MARKET REGIME"); print("="*70)
for col, label in [("market_regime","Bull/Bear/Sideways"), ("market_vol_regime","High/Low Volatility")]:
    print(f"\n-- {label} --")
    print(group_ic(feat, "F_INST_01_foreign_rank", RET, col).round(4).to_string(index=False))

print("\n"+"="*70); print("4. INTERACTION ANALYSIS (Foreign x ...)"); print("="*70)
for f, label in [("F_INT_07_foreign_x_momentum","Foreign x Momentum"),
                  ("F_INT_04_foreign_x_liquidity","Foreign x Liquidity"),
                  ("F_INT_05_foreign_x_volatility","Foreign x Volatility"),
                  ("F_INT_06_foreign_x_size","Foreign x Size")]:
    s = daily_ic_series(feat, f, RET)
    t_nw = s.mean() / (s.std()/np.sqrt(len(s)))
    print(f"{label:25s}: mean_ic={s.mean():.4f}  icir={s.mean()/s.std():.4f}  n_days={len(s)}  t_raw={t_nw:.2f}")
    # compare vs plain foreign alone
plain = daily_ic_series(feat, "F_INST_01_foreign_rank", RET)
print(f"{'(plain Foreign, for reference)':25s}: mean_ic={plain.mean():.4f}  icir={plain.mean()/plain.std():.4f}")
