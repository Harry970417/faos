"""RP-001 Milestone 1B-R + rebuild: Feature Construction v0.2 with the
Trading Calendar Gate and proper missing-state handling applied."""
import json
from pathlib import Path
import numpy as np
import pandas as pd

np.random.seed(42)

ROOT = Path(r"C:\Users\user\Desktop\faos")
INST_DIR = ROOT / "rp001_data" / "raw"
PRICE_DIR = ROOT / "rp001_data" / "raw_price"
OUT_DIR = ROOT / "rp001_data" / "features"

CATS = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging"]

# ---- Load ----
inst = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(INST_DIR.glob("inst_*.csv"))], ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]

price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(PRICE_DIR.glob("price_*.csv"))], ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
price = price.rename(columns={"Trading_Volume": "volume", "Trading_money": "trading_value"})
price = price[["stock_id", "date", "close", "volume", "trading_value"]].sort_values(["stock_id", "date"])

# ---- TRADING CALENDAR GATE ----
trading_calendar = set(price["date"].unique())
n_before = len(inst)
inst = inst[inst["date"].isin(trading_calendar)].copy()
n_excluded = n_before - len(inst)
print(f"Trading Calendar Gate: excluded {n_excluded} rows not on a confirmed trading day "
      f"({n_before} -> {len(inst)})")
assert n_excluded == 245, f"Expected exactly 245 rows excluded (2026-06-19), got {n_excluded}"

inst_wide = inst.pivot_table(index=["stock_id", "date"], columns="name", values="net", aggfunc="first").reset_index()
inst_wide.columns.name = None

# ---- shares outstanding ----
with open(ROOT / "rp001_data" / "twse_company_info.json", encoding="utf-8") as f:
    company_info = json.load(f)
shares_map = {}
for c in company_info:
    sid = c.get("公司代號")
    try:
        shares_map[sid] = float(c.get("已發行普通股數或TDR原股發行股數", "0"))
    except (ValueError, TypeError):
        pass

# ---- Merge panel ----
panel = pd.merge(inst_wide, price, on=["stock_id", "date"], how="inner")
panel = panel.sort_values(["stock_id", "date"]).reset_index(drop=True)
print(f"Panel rows after merge: {len(panel)} (v0.1 had 24,535)")

# ---- Proper missing-state handling (replaces v0.1's blanket fillna(0)) ----
# trading_halt (volume==0 on a real trading day): institutional flow is a TRUE
# zero by definition (nothing traded) -> fill 0, tagged.
# source_missing (volume>0 but no institutional row): genuinely unknown -> NaN,
# NOT silently treated as zero.
is_halt_day = panel["volume"] == 0
for cat in CATS:
    missing_mask = panel[cat].isna()
    halt_fill = missing_mask & is_halt_day
    panel.loc[halt_fill, cat] = 0.0
    # remaining missing_mask & ~is_halt_day rows are source_missing -> left as NaN deliberately

n_halt_filled = int((is_halt_day & panel[CATS].isna().any(axis=1)).sum())  # approx, pre-fill would need snapshot; report post-hoc
n_still_missing = panel[CATS].isna().any(axis=1).sum()
print(f"Rows on trading-halt days (volume=0, filled 0.0 for institutional flow): {is_halt_day.sum()}")
print(f"Rows with remaining source_missing NaN (left un-imputed, by design): {n_still_missing}")

panel["shares_outstanding"] = panel["stock_id"].map(shares_map)
panel["market_cap"] = panel["shares_outstanding"] * panel["close"]

# ---- Feature construction (identical logic to v0.1, now on the corrected panel) ----
def rank_pct(s):
    return s.groupby(panel["date"]).rank(pct=True)

feat = panel[["stock_id", "date"]].copy()
feat["F_INST_01_foreign"] = panel["Foreign_Investor"]
feat["F_INST_02_trust"] = panel["Investment_Trust"]
feat["F_INST_03_dealer_self"] = panel["Dealer_self"]
feat["F_INST_04_dealer_hedge"] = panel["Dealer_Hedging"]
feat["F_INST_05_aggregate"] = panel[CATS].sum(axis=1, min_count=1)  # min_count=1: all-NaN row -> NaN, not 0
feat["F_INST_06_value_proxy"] = feat["F_INST_05_aggregate"] * panel["close"]
feat["F_INST_07_flow_to_volume"] = feat["F_INST_05_aggregate"] / panel["volume"].replace(0, np.nan)

def consecutive_streak(s):
    sign = np.sign(s)
    streak = sign.groupby((sign != sign.shift()).cumsum()).cumcount() + 1
    return streak * sign
feat["F_INST_08_streak"] = panel.groupby("stock_id", group_keys=False).apply(
    lambda g: consecutive_streak(feat.loc[g.index, "F_INST_05_aggregate"]))

def rolling_change_rate(g_idx):
    s = feat.loc[g_idx, "F_INST_05_aggregate"]
    roll_mean = s.rolling(20, min_periods=10).mean()
    return (s - roll_mean) / roll_mean.abs().replace(0, np.nan)
feat["F_INST_09_change_rate"] = panel.groupby("stock_id", group_keys=False).apply(
    lambda g: rolling_change_rate(g.index))

def momentum_20d(g_idx):
    return panel.loc[g_idx, "close"].pct_change(20)
feat["_momentum_20d"] = panel.groupby("stock_id", group_keys=False).apply(lambda g: momentum_20d(g.index))
feat["F_INT_01_flow_x_momentum"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(feat["_momentum_20d"])
feat["F_INT_02_flow_x_size"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(panel["market_cap"])

def adv_20d(g_idx):
    return panel.loc[g_idx, "trading_value"].rolling(20, min_periods=10).mean()
panel["_adv_20d"] = panel.groupby("stock_id", group_keys=False).apply(lambda g: adv_20d(g.index))
feat["F_INT_03_flow_x_liquidity"] = rank_pct(feat["F_INST_05_aggregate"]) * rank_pct(panel["_adv_20d"])
feat = feat.drop(columns=["_momentum_20d"])

RANK_TARGETS = ["F_INST_01_foreign", "F_INST_02_trust", "F_INST_03_dealer_self",
                 "F_INST_04_dealer_hedge", "F_INST_05_aggregate", "F_INST_06_value_proxy",
                 "F_INST_09_change_rate"]
for col in RANK_TARGETS:
    feat[col + "_rank"] = rank_pct(feat[col])

# ---- carry forward returns for IC computation (Milestone 1C), t+1/t+2/t+3/t+5 open-to-open ----
price_r = price.sort_values(["stock_id", "date"]).copy()
def fwd_return(g, h):
    # next-open-execution proxy: t+1 open unavailable in this dataset (only close),
    # so close-to-close SHIFTED by one extra day is used as the tradeable-timing
    # proxy: buy at t+1 close (first point after flow is public), hold to t+1+h close.
    c = g["close"]
    return c.shift(-(h+1)) / c.shift(-1) - 1
for h in [1, 2, 3, 5]:
    price_r[f"fwd_ret_t{h}"] = price_r.groupby("stock_id", group_keys=False).apply(lambda g: fwd_return(g, h))

feat = pd.merge(feat, price_r[["stock_id", "date"] + [f"fwd_ret_t{h}" for h in [1,2,3,5]]], on=["stock_id","date"], how="left")

feat["version"] = "v0.2"
feat["build_date"] = pd.Timestamp.now("UTC").strftime("%Y-%m-%dT%H:%M:%SZ")

feat.to_parquet(OUT_DIR / "rp001_features_v0.2.parquet", index=False)
feat.to_csv(OUT_DIR / "rp001_features_v0.2.csv", index=False)
print(f"\nFeature panel v0.2 built: {feat.shape[0]} rows x {feat.shape[1]} cols")

# ---- REGRESSION CHECK against v0.1: existing features must not show unexpected changes ----
v1 = pd.read_parquet(OUT_DIR / "rp001_features_v0.1.parquet")
common = pd.merge(v1[["stock_id","date","F_INST_05_aggregate"]], feat[["stock_id","date","F_INST_05_aggregate"]],
                   on=["stock_id","date"], suffixes=("_v1","_v2"))
diff = (common["F_INST_05_aggregate_v1"] - common["F_INST_05_aggregate_v2"]).abs()
n_changed = (diff > 1e-6).sum()
print(f"\nRegression check: F_INST_05_aggregate changed on {n_changed} / {len(common)} common (stock,date) rows "
      f"({n_changed/len(common)*100:.4f}%) -- expected: only the {is_halt_day.sum()} halt-day and "
      f"~{n_still_missing} source_missing rows should differ, everything else identical.")
