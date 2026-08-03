"""RP-001 Milestone 1A: Feature Construction.
Builds all 11 features from RP001_FEATURE_SPECIFICATION.md on the 50-stock
characterization sample. No IC/backtest/portfolio here — construction and
unit tests only.
"""
import json
from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)

ROOT = Path(r"C:\Users\user\Desktop\faos")
INST_DIR = ROOT / "rp001_data" / "raw"
PRICE_DIR = ROOT / "rp001_data" / "raw_price"
OUT_DIR = ROOT / "rp001_data" / "features"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# ---- Load institutional data (long format: stock_id, date, name, buy, sell) ----
inst_frames = [pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(INST_DIR.glob("inst_*.csv"))]
inst = pd.concat(inst_frames, ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]

# Pivot to wide: one column per category's net flow
inst_wide = inst.pivot_table(index=["stock_id", "date"], columns="name", values="net", aggfunc="first").reset_index()
inst_wide.columns.name = None

# ---- Load price data ----
price_frames = [pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(PRICE_DIR.glob("price_*.csv"))]
price = pd.concat(price_frames, ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
price = price.rename(columns={"Trading_Volume": "volume", "Trading_money": "trading_value"})
price = price[["stock_id", "date", "close", "volume", "trading_value"]].sort_values(["stock_id", "date"])

# ---- Load TWSE company info for shares outstanding (size proxy) ----
with open(ROOT / "rp001_data" / "twse_company_info.json", encoding="utf-8") as f:
    company_info = json.load(f)
shares_map = {}
for c in company_info:
    sid = c.get("公司代號")
    shares_str = c.get("已發行普通股數或TDR原股發行股數", "0")
    try:
        shares_map[sid] = float(shares_str)
    except (ValueError, TypeError):
        pass

# ---- Merge panel ----
panel = pd.merge(inst_wide, price, on=["stock_id", "date"], how="inner")
panel = panel.sort_values(["stock_id", "date"]).reset_index(drop=True)

print(f"Panel rows after merge: {len(panel)}")
print(f"Institutional rows: {len(inst_wide)}, Price rows: {len(price)}, merged (inner join): {len(panel)}")
merge_loss = len(inst_wide) - len(panel)
print(f"Rows lost in inner join (inst-only dates with no matching price, or vice versa): {merge_loss} ({merge_loss/len(inst_wide)*100:.2f}%)")

CATS = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging"]

# ---- Missing handling: explicit policy ----
# Institutional net flow: missing panel cells (0.07% per Milestone 0A) -> treat as
# 0 net flow (no trading that day is a legitimate economic zero, not an unknown).
# This is a DECISION, logged, not a silent default.
missing_before = panel[CATS].isna().sum().sum()
panel[CATS] = panel[CATS].fillna(0.0)
print(f"\nMissing institutional cells filled with 0.0 (legitimate 'no flow'): {missing_before}")

price_missing_before = panel[["close", "volume", "trading_value"]].isna().sum().sum()
panel = panel.dropna(subset=["close", "volume"])  # cannot construct price-dependent features without these
print(f"Rows dropped for missing price/volume (cannot impute price): {price_missing_before}")

panel["shares_outstanding"] = panel["stock_id"].map(shares_map)
n_no_shares = panel["shares_outstanding"].isna().sum()
print(f"Rows with no shares-outstanding match (market cap will be NaN): {n_no_shares} ({n_no_shares/len(panel)*100:.2f}%)")
panel["market_cap"] = panel["shares_outstanding"] * panel["close"]

# ---- Feature construction ----
def rank_pct(s: pd.Series) -> pd.Series:
    """Cross-sectional percentile rank within each date, in [0,1]."""
    return s.groupby(panel["date"]).rank(pct=True)

feat = panel[["stock_id", "date"]].copy()

# F-INST-01..04: single-category net flow (Foreign_Dealer_Self excluded per Milestone 0C)
feat["F_INST_01_foreign"] = panel["Foreign_Investor"]
feat["F_INST_02_trust"] = panel["Investment_Trust"]
feat["F_INST_03_dealer_self"] = panel["Dealer_self"]
feat["F_INST_04_dealer_hedge"] = panel["Dealer_Hedging"]

# F-INST-05: aggregate (all 5, including the near-dead Foreign_Dealer_Self, per spec)
feat["F_INST_05_aggregate"] = panel[CATS].sum(axis=1)

# F-INST-06: value-proxy (net shares x close price) -- explicitly a proxy, not true NT$
feat["F_INST_06_value_proxy"] = feat["F_INST_05_aggregate"] * panel["close"]

# F-INST-07: flow-to-volume ratio (already bounded, no further standardization)
feat["F_INST_07_flow_to_volume"] = feat["F_INST_05_aggregate"] / panel["volume"].replace(0, np.nan)

# F-INST-08: consecutive same-direction days (on aggregate flow sign)
def consecutive_streak(s: pd.Series) -> pd.Series:
    sign = np.sign(s)
    streak = sign.groupby((sign != sign.shift()).cumsum()).cumcount() + 1
    return streak * sign

feat["F_INST_08_streak"] = panel.groupby("stock_id", group_keys=False).apply(
    lambda g: consecutive_streak(feat.loc[g.index, "F_INST_05_aggregate"])
)

# F-INST-09: flow change rate vs 20-day rolling mean (N=20 placeholder, calibration deferred per spec)
def rolling_change_rate(g_idx):
    s = feat.loc[g_idx, "F_INST_05_aggregate"]
    roll_mean = s.rolling(20, min_periods=10).mean()
    return (s - roll_mean) / roll_mean.abs().replace(0, np.nan)

feat["F_INST_09_change_rate"] = panel.groupby("stock_id", group_keys=False).apply(
    lambda g: rolling_change_rate(g.index)
)

# F-INT-01: flow x momentum (20-day price return as momentum placeholder, pending KB FA03/FA04 formal linkage)
def momentum_20d(g_idx):
    c = panel.loc[g_idx, "close"]
    return c.pct_change(20)

feat["_momentum_20d"] = panel.groupby("stock_id", group_keys=False).apply(lambda g: momentum_20d(g.index))
feat["F_INT_01_flow_x_momentum"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(feat["_momentum_20d"])

# F-INT-02: flow x size
feat["F_INT_02_flow_x_size"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(panel["market_cap"])

# F-INT-03: flow x liquidity (ADV = 20d rolling avg trading value)
def adv_20d(g_idx):
    v = panel.loc[g_idx, "trading_value"]
    return v.rolling(20, min_periods=10).mean()

panel["_adv_20d"] = panel.groupby("stock_id", group_keys=False).apply(lambda g: adv_20d(g.index))
feat["F_INT_03_flow_x_liquidity"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(panel["_adv_20d"])

feat = feat.drop(columns=["_momentum_20d"])

# ---- Rank normalization (primary, per Milestone 0C) for the base single/derived features ----
RANK_TARGETS = ["F_INST_01_foreign", "F_INST_02_trust", "F_INST_03_dealer_self",
                 "F_INST_04_dealer_hedge", "F_INST_05_aggregate", "F_INST_06_value_proxy",
                 "F_INST_09_change_rate"]
for col in RANK_TARGETS:
    feat[col + "_rank"] = rank_pct(feat[col])

feat["version"] = "v0.1"
feat["build_date"] = pd.Timestamp.now("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")

out_path = OUT_DIR / "rp001_features_v0.1.parquet"
feat.to_parquet(out_path, index=False)
feat.to_csv(OUT_DIR / "rp001_features_v0.1.csv", index=False)
print(f"\nFeature panel built: {feat.shape[0]} rows x {feat.shape[1]} cols")
print(f"Saved: {out_path}")
print("\nColumns:", list(feat.columns))
