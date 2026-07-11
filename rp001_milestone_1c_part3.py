import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_v0.2.parquet")

with open(ROOT / "rp001_data" / "twse_company_info.json", encoding="utf-8") as f:
    company_info = json.load(f)
sector_map = {c.get("公司代號"): c.get("產業別") for c in company_info}
feat["sector"] = feat["stock_id"].map(sector_map)
price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw_price").glob("price_*.csv"))], ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
shares_map = {}
for c in company_info:
    try: shares_map[c.get("公司代號")] = float(c.get("已發行普通股數或TDR原股發行股數","0"))
    except (ValueError,TypeError): pass
price["mcap"] = price["stock_id"].map(shares_map) * price["close"]
feat = pd.merge(feat, price[["stock_id","date","mcap"]], on=["stock_id","date"], how="left")
feat["log_mcap"] = np.log(feat["mcap"])

def daily_ic(df, feature, ret_col):
    recs = []
    for d, g in df.groupby("date"):
        sub = g[[feature, ret_col]].dropna()
        if len(sub) < 10: continue
        ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
        recs.append(ic)
    return np.array(recs)

def neutralize(df, feature, group_cols):
    """Cross-sectional residual of `feature` after regressing out group_cols
    (categorical -> dummies, numeric -> as-is) within each date."""
    out = pd.Series(index=df.index, dtype=float)
    for d, g in df.groupby("date"):
        y = g[feature].values
        X_parts = [np.ones(len(g))]
        for col in group_cols:
            if pd.api.types.is_numeric_dtype(g[col]):
                X_parts.append(g[col].fillna(g[col].median()).values)
            else:
                dummies = pd.get_dummies(g[col], drop_first=True).values.astype(float)
                if dummies.shape[1] > 0:
                    X_parts.append(dummies)
        X = np.column_stack(X_parts) if len(X_parts) > 1 else X_parts[0].reshape(-1,1)
        valid = ~np.isnan(y)
        if valid.sum() < X.shape[1] + 2:
            continue
        beta, *_ = np.linalg.lstsq(X[valid], y[valid], rcond=None)
        resid = y.copy()
        resid[valid] = y[valid] - X[valid] @ beta
        out.loc[g.index] = resid
    return out

print("="*70)
print("NEUTRALIZATION (t+5 horizon)")
print("="*70)
ret_col = "fwd_ret_t5"
for feature in ["F_INST_01_foreign_rank", "F_INT_02_flow_x_size", "F_INT_03_flow_x_liquidity"]:
    raw_ic = daily_ic(feat, feature, ret_col)
    feat["_mcap_neutral"] = neutralize(feat, feature, ["log_mcap"])
    mcap_ic = daily_ic(feat, "_mcap_neutral", ret_col)
    feat["_sector_neutral"] = neutralize(feat, feature, ["sector"])
    sector_ic = daily_ic(feat, "_sector_neutral", ret_col)
    print(f"\n{feature}:")
    print(f"  Raw:            mean_ic={raw_ic.mean():.4f}  icir={raw_ic.mean()/raw_ic.std():.4f}")
    print(f"  Mcap-neutral:   mean_ic={mcap_ic.mean():.4f}  icir={mcap_ic.mean()/mcap_ic.std():.4f}  (retention: {mcap_ic.mean()/raw_ic.mean()*100:.0f}% of raw IC)")
    print(f"  Sector-neutral: mean_ic={sector_ic.mean():.4f}  icir={sector_ic.mean()/sector_ic.std():.4f}  (retention: {sector_ic.mean()/raw_ic.mean()*100:.0f}% of raw IC)")

print("\n"+"="*70)
print("REDUNDANCY DIAGNOSTICS: F_INST_05 vs 06 vs 07 incremental info")
print("="*70)
for feature in ["F_INST_05_aggregate_rank", "F_INST_06_value_proxy_rank", "F_INST_07_flow_to_volume"]:
    ic1 = daily_ic(feat, feature, "fwd_ret_t1")
    ic5 = daily_ic(feat, feature, "fwd_ret_t5")
    print(f"{feature}: t+1 mean_ic={ic1.mean():.4f}  t+5 mean_ic={ic5.mean():.4f}")

# incremental IC: residualize 06 and 07 against 05, check if residual still has IC
feat["_06_resid_vs_05"] = neutralize(feat, "F_INST_06_value_proxy_rank", ["F_INST_05_aggregate_rank"])
feat["_07_resid_vs_05"] = neutralize(feat, "F_INST_07_flow_to_volume", ["F_INST_05_aggregate_rank"])
ic_06resid = daily_ic(feat, "_06_resid_vs_05", "fwd_ret_t5")
ic_07resid = daily_ic(feat, "_07_resid_vs_05", "fwd_ret_t5")
print(f"\nF_INST_06 residual (after removing F_INST_05's linear effect) vs fwd_ret_t5: mean_ic={ic_06resid.mean():.4f}, icir={ic_06resid.mean()/ic_06resid.std():.4f}")
print(f"F_INST_07 residual (after removing F_INST_05's linear effect) vs fwd_ret_t5: mean_ic={ic_07resid.mean():.4f}, icir={ic_07resid.mean()/ic_07resid.std():.4f}")
print("(If these residual ICs are near zero, 06/07 add little beyond 05 despite their own raw IC.)")
