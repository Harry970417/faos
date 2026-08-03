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
feat["mcap_tercile"] = feat.groupby("date")["mcap"].transform(lambda s: pd.qcut(s, 3, labels=["Small","Mid","Large"], duplicates="drop"))
mkt = price.groupby("date")["close"].mean().sort_index()
mkt_state = mkt.pct_change(60).apply(lambda x: "Bull" if x > 0 else ("Bear" if x <= 0 else np.nan))
feat["market_state"] = feat["date"].map(mkt_state)
feat["year"] = feat["date"].dt.year
feat["quarter"] = feat["date"].dt.to_period("Q").astype(str)

def daily_ic_by_group(df, feature, ret_col, group_col):
    out = []
    for gval, gdf in df.groupby(group_col):
        recs = []
        for d, g in gdf.groupby("date"):
            sub = g[[feature, ret_col]].dropna()
            if len(sub) < 8:
                continue
            ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
            recs.append(ic)
        if len(recs) >= 5:
            recs = np.array(recs)
            out.append({group_col: gval, "n_days": len(recs), "mean_ic": recs.mean(),
                        "icir": recs.mean()/recs.std() if recs.std()>0 else np.nan,
                        "pos_ratio": (recs>0).mean()})
    return pd.DataFrame(out)

FOCUS = ["F_INST_01_foreign_rank", "F_INT_02_flow_x_size", "F_INT_03_flow_x_liquidity", "F_INT_01_flow_x_momentum"]
ret_col = "fwd_ret_t5"  # use the horizon where signal was clearest

print("="*70)
print("STABILITY: by Year")
print("="*70)
for feature in FOCUS:
    print(f"\n-- {feature} --")
    print(daily_ic_by_group(feat, feature, ret_col, "year").round(4).to_string(index=False))

print("\n"+"="*70)
print("STABILITY: by Market-Cap Tercile")
print("="*70)
for feature in FOCUS:
    print(f"\n-- {feature} --")
    print(daily_ic_by_group(feat, feature, ret_col, "mcap_tercile").round(4).to_string(index=False))

print("\n"+"="*70)
print("STABILITY: by Market State (Bull/Bear, 60d trend)")
print("="*70)
for feature in FOCUS:
    print(f"\n-- {feature} --")
    print(daily_ic_by_group(feat, feature, ret_col, "market_state").round(4).to_string(index=False))

print("\n"+"="*70)
print("STABILITY: by Sector (TWSE code, only sectors with >=3 stocks)")
print("="*70)
sector_counts = feat.groupby("sector")["stock_id"].nunique()
big_sectors = sector_counts[sector_counts >= 3].index
for feature in ["F_INST_01_foreign_rank", "F_INT_03_flow_x_liquidity"]:
    print(f"\n-- {feature} --")
    sub = feat[feat["sector"].isin(big_sectors)]
    print(daily_ic_by_group(sub, feature, ret_col, "sector").round(4).to_string(index=False))
