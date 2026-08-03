from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_1c_plus.parquet")

def daily_ic(df, feature, ret_col):
    recs = []
    for d, g in df.groupby("date"):
        sub = g[[feature, ret_col]].dropna()
        if len(sub) < 8: continue
        ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
        recs.append(ic)
    return np.array(recs)

def newey_west_tstat(x, lags=5):
    n = len(x); mean_x = x.mean(); resid = x - mean_x
    gamma0 = np.sum(resid**2)/n
    v = gamma0
    for lag in range(1, lags+1):
        w = 1 - lag/(lags+1)
        v += 2*w*np.sum(resid[lag:]*resid[:-lag])/n
    se = np.sqrt(v/n)
    return mean_x/se if se>0 else np.nan

def neutralize(df, feature, controls):
    out = pd.Series(index=df.index, dtype=float)
    for d, g in df.groupby("date"):
        y = g[feature].values
        X = np.column_stack([np.ones(len(g))] + [g[c].fillna(g[c].median()).values if pd.api.types.is_numeric_dtype(g[c]) else pd.get_dummies(g[c], drop_first=True).values.astype(float) for c in controls])
        valid = ~np.isnan(y)
        if valid.sum() < X.shape[1]+2: continue
        beta,*_ = np.linalg.lstsq(X[valid], y[valid], rcond=None)
        resid = y.copy(); resid[valid] = y[valid] - X[valid]@beta
        out.loc[g.index] = resid
    return out

TESTS = [
    ("F_INT_05_foreign_x_volatility", "_foreign_rank", "_vol_rank", "Foreign x Volatility"),
    ("F_INT_06_foreign_x_size", "_foreign_rank", "_size_rank", "Foreign x Size"),
    ("F_INT_07_foreign_x_momentum", "_foreign_rank", "_mom_rank_real", "Foreign x Momentum"),
]

for feature, c1, c2, label in TESTS:
    print("="*70); print(f"{label} ({feature})"); print("="*70)
    raw_results = {}
    for h in [1, 3, 5]:
        ret_col = f"fwd_ret_t{h}"
        raw = daily_ic(feat, feature, ret_col)
        raw_results[h] = raw
        print(f"  Raw t+{h}: mean_ic={raw.mean():.4f}  t_nw={newey_west_tstat(raw):.3f}  n={len(raw)}")

    feat["_resid_both"] = neutralize(feat, feature, [c1, c2])
    for h in [1, 3, 5]:
        ret_col = f"fwd_ret_t{h}"
        resid_ic = daily_ic(feat, "_resid_both", ret_col)
        t_resid = newey_west_tstat(resid_ic)
        print(f"  Residualized (vs BOTH components) t+{h}: mean_ic={resid_ic.mean():.4f}  t_nw={t_resid:.3f}")

    # break-period stability of the residualized version (t+5)
    feat["_resid_t5"] = feat["_resid_both"]
    pre = feat[feat["date"] < "2025-09-24"]
    post = feat[feat["date"] >= "2025-09-24"]
    ic_pre = daily_ic(pre, "_resid_both", "fwd_ret_t5")
    ic_post = daily_ic(post, "_resid_both", "fwd_ret_t5")
    print(f"  Residualized IC pre-break: mean={ic_pre.mean():.4f} (n={len(ic_pre)})  post-break: mean={ic_post.mean():.4f} (n={len(ic_post)})")

    # sector-neutral on top of the residualized version
    feat["_resid_sector_neutral"] = neutralize(feat, feature, [c1, c2, "sector"])
    ic_sector = daily_ic(feat, "_resid_sector_neutral", "fwd_ret_t5")
    print(f"  Residualized + sector-neutral t+5: mean_ic={ic_sector.mean():.4f}  t_nw={newey_west_tstat(ic_sector):.3f}")

    resid_t5 = daily_ic(feat, "_resid_both", "fwd_ret_t5")
    t_final = newey_west_tstat(resid_t5)
    if abs(t_final) > 2.0 and abs(newey_west_tstat(ic_sector)) > 1.5:
        verdict = "GENUINE INCREMENTAL INTERACTION (survives both residualization and sector-neutrality)"
    elif abs(t_final) < 1.0:
        verdict = "ADDITIVE RECOMBINATION ARTIFACT (residual IC collapses toward zero)"
    else:
        verdict = "INCONCLUSIVE (weak or unstable after controls)"
    print(f"  >>> VERDICT: {verdict}")
    print()
