"""
RP-001 Phase 2A.3: Feature construction on the full-universe Confirmatory
panel. Locked definitions only (FEATURE_REGISTRY.md, rp001_1c_plus_setup.py's
exact interaction formulas) -- no redefinition. F_INT_02/F_INT_06 (size-based)
excluded per D-08 (market cap unavailable at full-universe scale).
"""
import time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
PROC_DIR = ROOT / "rp001_data" / "phase2a" / "processed"
BREAK_POINT = "2025-09-25"
BREAK_START, BREAK_END = "2025-08-01", "2025-10-31"
AGG_CATS = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging", "Dealer"]

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)

def rank_pct(s, dates):
    return s.groupby(dates).rank(pct=True)

def main():
    log("Loading raw merged panel...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_panel_raw.parquet")
    panel = panel.sort_values(["stock_id", "date"]).reset_index(drop=True)
    log(f"Panel: {len(panel):,} rows")

    # ---- F_INST_01 (primary, locked) ----
    panel["F_INST_01_foreign"] = panel["Foreign_Investor"]

    # ---- F_INST_05 aggregate (all 6 categories -- Dealer and Dealer_self/Dealer_Hedging
    # are mutually exclusive per stock, confirmed across 69 individually-verified
    # instances in RP001_PHASE2A_DEVIATION_LOG.md D-05, so summing all 6 with
    # min_count=1 correctly captures whichever schema a stock uses without double-counting) ----
    panel["F_INST_05_aggregate"] = panel[AGG_CATS].sum(axis=1, min_count=1)

    # ---- F_INST_07 flow-to-volume (secondary) ----
    panel["F_INST_07_flow_to_volume"] = panel["F_INST_05_aggregate"] / panel["volume"].replace(0, np.nan)

    log("Computing rolling stock-level series (adv20, rvol20, mom20)...")
    g = panel.groupby("stock_id", group_keys=False)
    panel["ret1d"] = g["close"].apply(lambda s: s.pct_change())
    panel["adv20"] = g["trading_value"].apply(lambda s: s.rolling(20, min_periods=10).mean())
    panel["rvol20"] = panel.groupby("stock_id", group_keys=False)["ret1d"].apply(
        lambda s: s.rolling(20, min_periods=10).std() * np.sqrt(252))
    panel["mom20"] = g["close"].apply(lambda s: s.pct_change(20))

    log("Computing daily cross-sectional ranks...")
    panel["F_INST_01_foreign_rank"] = rank_pct(panel["F_INST_01_foreign"], panel["date"])
    panel["F_INST_05_aggregate_rank"] = rank_pct(panel["F_INST_05_aggregate"], panel["date"])
    panel["_adv20_rank"] = rank_pct(panel["adv20"], panel["date"])
    panel["_rvol20_rank"] = rank_pct(panel["rvol20"], panel["date"])
    panel["_mom20_rank"] = rank_pct(panel["mom20"], panel["date"])

    # ---- Interaction features (5 of 7 constructible -- D-08) ----
    panel["F_INT_01_flow_x_momentum"] = panel["F_INST_05_aggregate_rank"] * panel["_mom20_rank"]
    panel["F_INT_03_flow_x_liquidity"] = panel["F_INST_05_aggregate_rank"] * panel["_adv20_rank"]
    panel["F_INT_04_foreign_x_liquidity"] = panel["F_INST_01_foreign_rank"] * panel["_adv20_rank"]
    panel["F_INT_05_foreign_x_volatility"] = panel["F_INST_01_foreign_rank"] * panel["_rvol20_rank"]
    panel["F_INT_07_foreign_x_momentum"] = panel["F_INST_01_foreign_rank"] * panel["_mom20_rank"]
    panel["F_INT_02_flow_x_size"] = np.nan   # D-08: not constructible, market cap unavailable
    panel["F_INT_06_foreign_x_size"] = np.nan  # D-08: not constructible, market cap unavailable

    # ---- Liquidity tercile (locked definition: 20d ADV, per-date cross-sectional tercile) ----
    log("Computing liquidity terciles and market volatility regime...")
    def tercile(s, labels):
        return pd.qcut(s.rank(method="first"), 3, labels=labels) if s.notna().sum() >= 15 else pd.Series(np.nan, index=s.index)
    panel["liq_tercile"] = panel.groupby("date")["adv20"].transform(lambda s: tercile(s, ["Illiquid", "Mid", "Liquid"]))

    # ---- Market volatility regime (locked definition: mkt realized vol, 20d, median split) ----
    mkt_close = panel.groupby("date")["close"].mean().sort_index()
    mkt_ret = mkt_close.pct_change()
    mkt_rvol20 = mkt_ret.rolling(20, min_periods=10).std() * np.sqrt(252)
    mkt_vol_median = mkt_rvol20.median()
    mkt_vol_regime = mkt_rvol20.apply(lambda x: "HighVol" if pd.notna(x) and x > mkt_vol_median else ("LowVol" if pd.notna(x) else np.nan))
    panel["market_vol_regime"] = panel["date"].map(mkt_vol_regime)

    # ---- Break-period labels (locked boundary, point estimate 2025-09-25) ----
    panel["break_period"] = np.where(panel["date"] < BREAK_POINT, "pre", "post")
    panel["in_break_window"] = (panel["date"] >= BREAK_START) & (panel["date"] <= BREAK_END)

    panel = panel.drop(columns=["ret1d"])
    panel["version"] = "phase2a_v0.1"
    panel["build_date"] = pd.Timestamp.now(tz="UTC").strftime("%Y-%m-%dT%H:%M:%SZ")

    out_path = PROC_DIR / "rp001_confirmatory_features.parquet"
    panel.to_parquet(out_path, index=False)
    log(f"Saved: {out_path} -- {panel.shape[0]:,} rows x {panel.shape[1]} cols")
    log(f"F_INST_01_foreign non-missing: {panel['F_INST_01_foreign'].notna().mean()*100:.1f}%")
    log(f"liq_tercile distribution: {panel['liq_tercile'].value_counts(dropna=False).to_dict()}")
    log(f"market_vol_regime distribution: {panel['market_vol_regime'].value_counts(dropna=False).to_dict()}")
    log(f"break_period distribution: {panel['break_period'].value_counts(dropna=False).to_dict()}")
    log("DONE")


if __name__ == "__main__":
    main()
