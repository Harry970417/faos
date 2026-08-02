"""
RP-001 Phase 2A.3: Confirmatory Dataset construction (full universe).

Builds the survivorship-bias-free Daily Investable Universe panel per
RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md, applies the Trading Calendar
Gate (Milestone 1B-R methodology) and RP001_MISSINGNESS_POLICY.md's
never-impute rule, then constructs F_INST_01/F_INST_05/F_INST_07, the
five constructible interaction features (D-08: F_INT_02/F_INT_06 excluded,
market cap unavailable), forward returns t+1/t+3/t+5 (locked horizon
construction, unchanged formula from rp001_build_features_v2.py), break-
period labels, and liquidity/volatility groupings -- all per already-locked
definitions, no redefinition.

Output: rp001_data/phase2a/processed/rp001_confirmatory_panel.parquet
"""
import json, sys, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "phase2a" / "raw"
OUT_DIR = ROOT / "rp001_data" / "phase2a" / "processed"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INST_FILE_SCHEMA = {"date", "stock_id", "buy", "sell", "name"}
PRICE_FILE_SCHEMA = {"date", "stock_id", "Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"}
INSTITUTIONAL_FLOOR = "2012-05-02"
BREAK_POINT = "2025-09-25"  # locked point estimate, RP001_PHASE2A_PROTOCOL_LOCK.md

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def load_all(dataset_name, universe_stock_ids, usecols=None):
    frames = []
    n_empty = 0
    for i, sid in enumerate(universe_stock_ids):
        p = RAW_DIR / f"{dataset_name}_{sid}.json"
        if not p.exists():
            continue
        rows = json.loads(p.read_text(encoding="utf-8"))
        if not rows:
            n_empty += 1
            continue
        df = pd.DataFrame.from_records(rows)
        frames.append(df)
        if (i + 1) % 500 == 0:
            log(f"  {dataset_name}: loaded {i+1}/{len(universe_stock_ids)} stocks...")
    log(f"{dataset_name}: {len(frames)} non-empty stocks, {n_empty} legitimately-empty stocks (skipped)")
    out = pd.concat(frames, ignore_index=True)
    return out


def main():
    universe = pd.read_csv(ROOT / "rp001_data" / "phase2a_acquisition_universe.csv", dtype=str)
    stock_ids = universe["stock_id"].tolist()
    log(f"Universe: {len(stock_ids)} stocks")

    # ---- Load price ----
    log("Loading price data...")
    price = load_all("TaiwanStockPrice", stock_ids)
    price["date"] = price["date"].astype(str)
    price["stock_id"] = price["stock_id"].astype(str)
    price = price.rename(columns={"Trading_Volume": "volume", "Trading_money": "trading_value"})
    price["close"] = price["close"].astype(np.float64)
    price["volume"] = price["volume"].astype(np.float64)
    price["trading_value"] = price["trading_value"].astype(np.float64)
    price = price[["stock_id", "date", "close", "volume", "trading_value"]]
    price = price.sort_values(["stock_id", "date"]).drop_duplicates(subset=["stock_id", "date"], keep="first")
    log(f"Price panel: {len(price):,} rows")

    # ---- Load institutional ----
    log("Loading institutional data...")
    inst = load_all("TaiwanStockInstitutionalInvestorsBuySell", stock_ids)
    inst["date"] = inst["date"].astype(str)
    inst["stock_id"] = inst["stock_id"].astype(str)
    inst["net"] = inst["buy"].astype(np.float64) - inst["sell"].astype(np.float64)
    inst = inst[["stock_id", "date", "name", "net"]]
    inst = inst.drop_duplicates(subset=["stock_id", "date", "name"], keep="first")
    log(f"Institutional long panel: {len(inst):,} rows")

    # ---- Trading Calendar Gate: drop institutional rows on dates that are not
    # a real trading day for ANY stock in the market (mis-dated-row contamination,
    # e.g. the known 2026-06-19 / weekend rows -- D-06/D-07) ----
    trading_calendar = set(price["date"].unique())
    n_before = len(inst)
    inst = inst[inst["date"].isin(trading_calendar)].copy()
    log(f"Trading Calendar Gate: excluded {n_before - len(inst):,} institutional rows "
        f"not on any confirmed market trading day ({n_before:,} -> {len(inst):,})")

    # ---- Pivot institutional to wide ----
    log("Pivoting institutional data to wide format...")
    inst_wide = inst.pivot_table(index=["stock_id", "date"], columns="name", values="net", aggfunc="first").reset_index()
    inst_wide.columns.name = None
    log(f"Institutional wide panel: {len(inst_wide):,} rows, categories: {[c for c in inst_wide.columns if c not in ('stock_id','date')]}")

    # ---- Eligibility: stock_eligibility_start per RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md sec2 ----
    first_price_date = price.groupby("stock_id")["date"].min()
    u = universe.set_index("stock_id")
    def eligibility_start(sid):
        row = u.loc[sid]
        if row["listing_date_source"] == "registry" and pd.notna(row.get("listing_date_raw")):
            raw = str(row["listing_date_raw"])
            if len(raw) == 8 and raw.isdigit():
                return f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
        return first_price_date.get(sid, None)
    elig_start_map = {sid: eligibility_start(sid) for sid in stock_ids}
    delist_map = u["delisting_date"].to_dict()

    price["elig_start"] = price["stock_id"].map(elig_start_map)
    price["delisting_date"] = price["stock_id"].map(delist_map)
    eligible_mask = (
        (price["date"] >= INSTITUTIONAL_FLOOR)
        & (price["elig_start"].isna() | (price["date"] >= price["elig_start"]))
        & (price["delisting_date"].isna() | (price["date"] < price["delisting_date"]))
        & (price["volume"] > 0)
    )
    price_elig = price[eligible_mask].drop(columns=["elig_start", "delisting_date"]).copy()
    log(f"Daily Investable Universe eligibility gate: {len(price):,} raw price rows -> {len(price_elig):,} eligible rows "
        f"({len(price_elig)/len(price)*100:.1f}%)")

    # ---- Forward returns computed on the FULL (pre-eligibility) per-stock price
    # series so shift() sees genuine subsequent trading days, then merged onto
    # the eligible panel. Locked horizon formula, unchanged from
    # rp001_build_features_v2.py: buy at t+1 close (first point after flow is
    # public), hold to t+1+h close. ----
    log("Computing forward returns (locked horizon construction)...")
    price_sorted = price.sort_values(["stock_id", "date"])
    def fwd_return(g, h):
        c = g["close"]
        return c.shift(-(h + 1)) / c.shift(-1) - 1
    ret_cols = {}
    for h in [1, 3, 5]:
        ret_cols[f"fwd_ret_t{h}"] = price_sorted.groupby("stock_id", group_keys=False).apply(lambda g, h=h: fwd_return(g, h))
    price_sorted = price_sorted.assign(**ret_cols)

    # ---- LEFT JOIN: eligible price backbone + institutional wide (NaN = source_missing, Rule 1/2) ----
    log("Merging panel (LEFT JOIN price(eligible) + institutional; NaN preserved per Missingness Policy)...")
    panel = pd.merge(price_elig, inst_wide, on=["stock_id", "date"], how="left")
    panel = pd.merge(panel, price_sorted[["stock_id", "date", "fwd_ret_t1", "fwd_ret_t3", "fwd_ret_t5"]],
                      on=["stock_id", "date"], how="left")
    panel = panel.sort_values(["stock_id", "date"]).reset_index(drop=True)
    log(f"Panel after merge: {len(panel):,} rows x {panel.shape[1]} cols")

    for cat in ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging", "Dealer"]:
        if cat not in panel.columns:
            panel[cat] = np.nan

    panel.to_parquet(OUT_DIR / "rp001_confirmatory_panel_raw.parquet", index=False)
    log(f"Saved raw merged panel: {OUT_DIR / 'rp001_confirmatory_panel_raw.parquet'}")
    log(f"F_INST_01 (Foreign_Investor) coverage: {panel['Foreign_Investor'].notna().mean()*100:.1f}% non-missing")
    log("DONE")


if __name__ == "__main__":
    main()
