import json
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_v0.2.parquet")

with open(ROOT / "rp001_data" / "twse_company_info.json", encoding="utf-8") as f:
    company_info = json.load(f)
sector_map = {c.get("公司代號"): c.get("產業別") for c in company_info}
shares_map = {}
for c in company_info:
    try: shares_map[c.get("公司代號")] = float(c.get("已發行普通股數或TDR原股發行股數","0"))
    except (ValueError,TypeError): pass
feat["sector"] = feat["stock_id"].map(sector_map)

price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw_price").glob("price_*.csv"))], ignore_index=True)
price = price.rename(columns={"Trading_Volume": "volume", "Trading_money": "trading_value"})
price["date"] = pd.to_datetime(price["date"])
price = price.sort_values(["stock_id","date"])
price["mcap"] = price["stock_id"].map(shares_map) * price["close"]
price["ret1d"] = price.groupby("stock_id")["close"].pct_change()
price["rvol20"] = price.groupby("stock_id", group_keys=False)["ret1d"].apply(lambda s: s.rolling(20, min_periods=10).std() * np.sqrt(252))
price["adv20"] = price.groupby("stock_id", group_keys=False)["trading_value"].apply(lambda s: s.rolling(20, min_periods=10).mean())

feat = pd.merge(feat, price[["stock_id","date","mcap","rvol20","adv20"]], on=["stock_id","date"], how="left")

val = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw_valuation").glob("val_*.csv"))], ignore_index=True)
val["date"] = pd.to_datetime(val["date"])
feat = pd.merge(feat, val[["stock_id","date","PBR","PER"]], on=["stock_id","date"], how="left")

# ---- cross-sectional groupings (per date) ----
feat["mcap_tercile"] = feat.groupby("date")["mcap"].transform(
    lambda s: pd.qcut(s.rank(method="first"), 3, labels=["Small","Mid","Large"]) if s.notna().sum() >= 15 else np.nan)
feat["pbr_tercile"] = feat.groupby("date")["PBR"].transform(
    lambda s: pd.qcut(s.rank(method="first"), 3, labels=["Value","Blend","Growth"]) if s.notna().sum() >= 15 else np.nan)
feat["liq_tercile"] = feat.groupby("date")["adv20"].transform(
    lambda s: pd.qcut(s.rank(method="first"), 3, labels=["Illiquid","Mid","Liquid"]) if s.notna().sum() >= 15 else np.nan)
feat["vol_tercile"] = feat.groupby("date")["rvol20"].transform(
    lambda s: pd.qcut(s.rank(method="first"), 3, labels=["LowVol","MidVol","HighVol"]) if s.notna().sum() >= 15 else np.nan)

# ---- market regime: Bull/Bear/Sideways (3-way, using magnitude threshold not just sign) + High/Low Vol ----
mkt = price.groupby("date")["close"].mean().sort_index()
mkt_ret60 = mkt.pct_change(60)
def regime3(x):
    if pd.isna(x): return np.nan
    if x > 0.03: return "Bull"
    if x < -0.03: return "Bear"
    return "Sideways"
mkt_regime = mkt_ret60.apply(regime3)
mkt_ret1d = mkt.pct_change()
mkt_rvol = mkt_ret1d.rolling(20, min_periods=10).std() * np.sqrt(252)
mkt_vol_median = mkt_rvol.median()
mkt_vol_regime = mkt_rvol.apply(lambda x: "HighVol" if x > mkt_vol_median else "LowVol")

feat["market_regime"] = feat["date"].map(mkt_regime)
feat["market_vol_regime"] = feat["date"].map(mkt_vol_regime)

# ---- new interaction features: Foreign x Liquidity, Foreign x Volatility, Foreign x Size ----
def rank_pct(s, dates):
    return s.groupby(dates).rank(pct=True)

feat["_foreign_rank"] = feat["F_INST_01_foreign_rank"]  # already rank
feat["_liq_rank"] = rank_pct(feat["adv20"], feat["date"])
feat["_vol_rank"] = rank_pct(feat["rvol20"], feat["date"])
feat["_size_rank"] = rank_pct(feat["mcap"], feat["date"])
feat["_mom_rank"] = rank_pct(feat["F_INT_01_flow_x_momentum"].notna() * 0, feat["date"])  # placeholder unused

feat["F_INT_04_foreign_x_liquidity"] = feat["_foreign_rank"] * feat["_liq_rank"]
feat["F_INT_05_foreign_x_volatility"] = feat["_foreign_rank"] * feat["_vol_rank"]
feat["F_INT_06_foreign_x_size"] = feat["_foreign_rank"] * feat["_size_rank"]
# Foreign x Momentum already exists as F_INT_01 (foreign is the input to F_INST_05 aggregate there;
# rebuild a foreign-specific version for consistency in this mechanism analysis)
mom20 = price.groupby("stock_id", group_keys=False)["close"].apply(lambda s: s.pct_change(20))
price["_mom20"] = mom20
feat = pd.merge(feat, price[["stock_id","date","_mom20"]], on=["stock_id","date"], how="left")
feat["_mom_rank_real"] = rank_pct(feat["_mom20"], feat["date"])
feat["F_INT_07_foreign_x_momentum"] = feat["_foreign_rank"] * feat["_mom_rank_real"]

feat = feat.drop(columns=["_mom_rank"])
feat.to_parquet(ROOT / "rp001_data" / "features" / "rp001_features_1c_plus.parquet", index=False)
print(f"Setup complete: {feat.shape[0]} rows x {feat.shape[1]} cols")
print("PBR coverage:", feat["PBR"].notna().mean())
print("Market regime distribution:", feat["market_regime"].value_counts(dropna=False).to_dict())
print("Market vol regime distribution:", feat["market_vol_regime"].value_counts(dropna=False).to_dict())
