"""
RP-001 Phase 2A.2-R: Institutional missingness semantics audit.
Uses cached Batch-1 raw JSON only (no new API calls). For every stock with
complete Price+Institutional data, builds an eligible-trading-date calendar
from its own price history, compares against institutional row dates, and
classifies each missing date.
"""
import json
from pathlib import Path
import pandas as pd
import numpy as np

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "phase2a" / "raw"
MANIFEST = ROOT / "rp001_data" / "phase2a" / "manifests" / "pull_manifest.csv"
UNIVERSE = ROOT / "rp001_data" / "phase2a_acquisition_universe.csv"
OUT_DIR = ROOT / "rp001_data" / "phase2a" / "audits"
OUT_DIR.mkdir(parents=True, exist_ok=True)

INST_FLOOR = "2012-05-02"

m = pd.read_csv(MANIFEST, dtype=str)
universe = pd.read_csv(UNIVERSE, dtype=str).set_index("stock_id")

price_ok = set(m[(m["dataset"] == "TaiwanStockPrice") & (m["status"] == "success")]["stock_id"])
inst_ok = set(m[(m["dataset"] == "TaiwanStockInstitutionalInvestorsBuySell") & (m["status"] == "success")]["stock_id"])
stock_ids = sorted(price_ok & inst_ok)
print(f"Stocks with both Price and Institutional cached: {len(stock_ids)}")

def load(dataset, sid):
    p = RAW_DIR / f"{dataset}_{sid}.json"
    rows = json.loads(p.read_text(encoding="utf-8"))
    return pd.DataFrame(rows) if rows else pd.DataFrame()

records = []
block_records = []
for sid in stock_ids:
    price = load("TaiwanStockPrice", sid)
    inst = load("TaiwanStockInstitutionalInvestorsBuySell", sid)
    if price.empty:
        continue
    price = price.sort_values("date")
    eligible_dates = sorted(set(price[price["date"] >= INST_FLOOR]["date"]))
    if not eligible_dates:
        continue
    inst_dates = set(inst["date"].unique()) if not inst.empty else set()
    missing_dates = sorted(set(eligible_dates) - inst_dates)

    # explicit-zero vs source_missing among dates that DO have an inst row: any row with buy==0 and sell==0 for all categories that day
    inst_num = inst.copy()
    if not inst_num.empty:
        inst_num["buy"] = pd.to_numeric(inst_num["buy"], errors="coerce").fillna(0)
        inst_num["sell"] = pd.to_numeric(inst_num["sell"], errors="coerce").fillna(0)
        daily_sum = inst_num.groupby("date")[["buy", "sell"]].sum()
        explicit_zero_dates = set(daily_sum[(daily_sum["buy"] == 0) & (daily_sum["sell"] == 0)].index)
    else:
        explicit_zero_dates = set()

    # trading halt proxy: price row exists with Trading_Volume == 0
    price_num = price.copy()
    price_num["Trading_Volume"] = pd.to_numeric(price_num["Trading_Volume"], errors="coerce").fillna(0)
    halt_dates = set(price_num[price_num["Trading_Volume"] == 0]["date"])

    # pre-eligible: dates before this stock's own first price observation are not even in eligible_dates by construction;
    # but flag if listing_date_source == registry and first price date is far before registry listing_date (pre-listing trading)
    row = universe.loc[sid] if sid in universe.index else None
    market = row["market"] if row is not None else "UNKNOWN"

    n_eligible = len(eligible_dates)
    n_missing = len(missing_dates)
    missing_rate = n_missing / n_eligible if n_eligible else np.nan

    # classify each missing date
    cls_counts = {"observed_zero": 0, "source_missing": 0, "trading_halt": 0, "unmatched_unknown": 0}
    for d in missing_dates:
        if d in halt_dates:
            cls_counts["trading_halt"] += 1
        else:
            cls_counts["source_missing"] += 1  # no inst row, not a halt day -> genuine source gap, unexplained further without market-transfer data

    # explicit zero days are NOT missing (row exists) -- track separately as a distinct semantic bucket
    cls_counts["observed_zero"] = len(explicit_zero_dates)

    # longest missing streak (consecutive eligible trading dates, not calendar days) and blocks
    ed_index = {d: i for i, d in enumerate(eligible_dates)}
    missing_idx = sorted(ed_index[d] for d in missing_dates)
    longest = 0
    blocks = []
    if missing_idx:
        start = prev = missing_idx[0]
        cur_len = 1
        for i in missing_idx[1:]:
            if i == prev + 1:
                cur_len += 1
                prev = i
            else:
                blocks.append((eligible_dates[start], eligible_dates[prev], cur_len))
                longest = max(longest, cur_len)
                start = prev = i
                cur_len = 1
        blocks.append((eligible_dates[start], eligible_dates[prev], cur_len))
        longest = max(longest, cur_len)

    records.append({
        "stock_id": sid, "market": market,
        "n_eligible_dates": n_eligible, "n_inst_rows_dates": len(inst_dates),
        "n_missing_dates": n_missing, "missing_rate": round(missing_rate, 4),
        "longest_missing_streak": longest, "n_missing_blocks": len(blocks),
        "n_explicit_zero_days": cls_counts["observed_zero"],
        "n_missing_trading_halt": cls_counts["trading_halt"],
        "n_missing_source_missing": cls_counts["source_missing"],
        "first_eligible": eligible_dates[0], "last_eligible": eligible_dates[-1],
    })
    for b in blocks:
        block_records.append({"stock_id": sid, "block_start": b[0], "block_end": b[1], "n_dates": b[2]})

df = pd.DataFrame(records)
df.to_csv(OUT_DIR / "missingness_summary_per_stock.csv", index=False)
blocks_df = pd.DataFrame(block_records)
blocks_df.to_csv(OUT_DIR / "missingness_blocks.csv", index=False)

print("\n=== Missing-rate distribution ===")
print(df["missing_rate"].describe())
print("\nStocks with missing_rate > 0.10:", (df["missing_rate"] > 0.10).sum(), "/", len(df))

print("\n=== By market ===")
print(df.groupby("market")["missing_rate"].describe())

print("\n=== Top 10 highest missing_rate ===")
print(df.sort_values("missing_rate", ascending=False).head(10)[["stock_id", "market", "missing_rate", "longest_missing_streak", "n_missing_blocks"]])

# 1213 full case timeline
if "1213" in df["stock_id"].values:
    row1213 = df[df["stock_id"] == "1213"].iloc[0]
    print("\n=== Stock 1213 summary ===")
    print(row1213)
    b1213 = blocks_df[blocks_df["stock_id"] == "1213"].sort_values("n_dates", ascending=False)
    print(f"\n1213 missing blocks: {len(b1213)} total, top 15 by length:")
    print(b1213.head(15).to_string())
    b1213.to_csv(OUT_DIR / "stock_1213_missing_blocks_full.csv", index=False)

print("\nDone. Outputs in", OUT_DIR)
