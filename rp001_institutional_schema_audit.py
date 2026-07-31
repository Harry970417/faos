"""
RP-001 Phase 2A.2-R: Institutional-category historical schema audit.
Reads cached Batch-1 raw JSON (no new API calls) for every stock with a
successful TaiwanStockInstitutionalInvestorsBuySell pull, builds
stock_id x date x institutional_category coverage, and answers:
Dealer occurrence, Dealer/Dealer_self/Dealer_Hedging overlap, cutover vs
recurrence, Foreign_Investor drift, and 2025 break-interval schema state.
"""
import json, csv
from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "phase2a" / "raw"
MANIFEST = ROOT / "rp001_data" / "phase2a" / "manifests" / "pull_manifest.csv"
OUT_DIR = ROOT / "rp001_data" / "phase2a" / "audits"
OUT_DIR.mkdir(parents=True, exist_ok=True)

BREAK_START, BREAK_END = "2025-08-01", "2025-10-31"  # late-Aug to late-Oct interval, widened by a few days each side for safety
CUTOVER = "2014-12-01"

m = pd.read_csv(MANIFEST, dtype=str)
inst_success = m[(m["dataset"] == "TaiwanStockInstitutionalInvestorsBuySell") & (m["status"] == "success")]
stock_ids = sorted(inst_success["stock_id"].unique().tolist())
print(f"Stocks with cached institutional data: {len(stock_ids)}")

frames = []
for sid in stock_ids:
    p = RAW_DIR / f"TaiwanStockInstitutionalInvestorsBuySell_{sid}.json"
    rows = json.loads(p.read_text(encoding="utf-8"))
    if not rows:
        continue
    df = pd.DataFrame(rows)
    df["stock_id"] = sid
    frames.append(df)
inst = pd.concat(frames, ignore_index=True)
print("Total rows:", len(inst))
print("All category names observed:", sorted(inst["name"].unique().tolist()))

# 1. Dealer occurrence: which stocks, which date ranges
dealer = inst[inst["name"] == "Dealer"]
dealer_by_stock = dealer.groupby("stock_id")["date"].agg(["min", "max", "count"])
dealer_by_stock.to_csv(OUT_DIR / "dealer_occurrence_by_stock.csv")
print(f"\nStocks with any 'Dealer' (undifferentiated) row: {dealer['stock_id'].nunique()} / {len(stock_ids)}")
print(dealer_by_stock)

# 2. Same-day overlap: Dealer vs Dealer_self/Dealer_Hedging, per stock
overlap_rows = []
for sid, g in inst.groupby("stock_id"):
    dealer_dates = set(g[g["name"] == "Dealer"]["date"])
    split_dates = set(g[g["name"].isin(["Dealer_self", "Dealer_Hedging"])]["date"])
    overlap = dealer_dates & split_dates
    if dealer_dates:
        overlap_rows.append({"stock_id": sid, "dealer_dates": len(dealer_dates),
                              "split_dates_total": len(split_dates), "overlap_dates": len(overlap)})
overlap_df = pd.DataFrame(overlap_rows)
overlap_df.to_csv(OUT_DIR / "dealer_split_overlap.csv", index=False)
print("\nDealer vs Dealer_self/Dealer_Hedging same-day overlap (per stock with any Dealer row):")
print(overlap_df)

# 3. Cutover vs recurrence classification per stock (only stocks with any Dealer row)
pattern_rows = []
for sid in dealer["stock_id"].unique():
    g = inst[inst["stock_id"] == sid].sort_values("date")
    dealer_dates = sorted(g[g["name"] == "Dealer"]["date"].unique())
    # contiguous blocks (gap > 10 calendar days => new block)
    blocks = []
    cur = [dealer_dates[0]]
    for d in dealer_dates[1:]:
        if (pd.to_datetime(d) - pd.to_datetime(cur[-1])).days > 10:
            blocks.append((cur[0], cur[-1]))
            cur = [d]
        else:
            cur.append(d)
    blocks.append((cur[0], cur[-1]))
    pattern = "clean_cutover_only" if len(blocks) == 1 and blocks[0][0] < CUTOVER else "recurrence"
    pattern_rows.append({"stock_id": sid, "n_blocks": len(blocks), "blocks": blocks, "pattern": pattern})
pattern_df = pd.DataFrame(pattern_rows)
pattern_df.to_csv(OUT_DIR / "dealer_pattern_classification.csv", index=False)
print("\nDealer temporal pattern per stock (clean_cutover_only vs recurrence):")
print(pattern_df[["stock_id", "n_blocks", "pattern"]])

# 4. Foreign_Investor drift check: any name variants close to 'Foreign_Investor'?
fi_variants = [n for n in inst["name"].unique() if "Foreign" in n]
print("\nForeign*-prefixed category names observed:", fi_variants)
fi = inst[inst["name"] == "Foreign_Investor"]
fi_coverage = inst.groupby("stock_id").apply(lambda g: "Foreign_Investor" in set(g["name"])).rename("has_foreign_investor")
missing_fi = fi_coverage[~fi_coverage].index.tolist()
print("Stocks with ZERO Foreign_Investor rows at all:", missing_fi)

# 5. Schema state inside the locked 2025 break interval, per stock
break_rows = []
for sid, g in inst.groupby("stock_id"):
    gb = g[(g["date"] >= BREAK_START) & (g["date"] <= BREAK_END)]
    cats_in_break = set(gb["name"].unique())
    has_dealer_in_break = "Dealer" in cats_in_break
    has_split_in_break = {"Dealer_self", "Dealer_Hedging"}.issubset(cats_in_break) or bool({"Dealer_self","Dealer_Hedging"} & cats_in_break)
    n_break_dates = gb["date"].nunique()
    break_rows.append({"stock_id": sid, "n_break_window_dates": n_break_dates,
                        "categories_in_break": sorted(cats_in_break),
                        "dealer_recurs_in_break_window": has_dealer_in_break})
break_df = pd.DataFrame(break_rows)
break_df.to_csv(OUT_DIR / "break_window_schema_state.csv", index=False)
n_affected = break_df["dealer_recurs_in_break_window"].sum()
print(f"\n*** Stocks where undifferentiated 'Dealer' recurs INSIDE the locked 2025 break window ({BREAK_START} to {BREAK_END}): {n_affected} / {len(break_df)} ***")
if n_affected:
    print(break_df[break_df["dealer_recurs_in_break_window"]])

print("\nDone. Outputs in", OUT_DIR)
