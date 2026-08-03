"""RP-001 Milestone 1B-R: Data Integrity Remediation.
Builds an empirical trading calendar, classifies every institutional
data cell into a missing-state, and scans the full research period for
non-trading-day contamination (not just the one date already found).
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
INST_DIR = ROOT / "rp001_data" / "raw"
PRICE_DIR = ROOT / "rp001_data" / "raw_price"
OUT_DIR = ROOT / "rp001_data"

CATS = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging"]

# ---- Load raw data ----
inst = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(INST_DIR.glob("inst_*.csv"))], ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]

price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(PRICE_DIR.glob("price_*.csv"))], ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
price = price.rename(columns={"Trading_Volume": "volume"})

# ---- 1. Empirical Trading Calendar Gate ----
# A date is a real trading day iff at least one stock in the sample has a
# price row for it (any real trade recorded anywhere is proof the exchange was open).
trading_calendar = set(price["date"].unique())
print(f"Trading Calendar Gate: {len(trading_calendar)} confirmed trading days "
      f"({price['date'].min().date()} to {price['date'].max().date()})")

# ---- 2. Full-period scan for non-trading-day contamination (not just 06-19) ----
inst_dates = set(inst["date"].unique())
contaminated_dates = sorted(inst_dates - trading_calendar)
print(f"\nFull-period scan: institutional dates NOT in the Trading Calendar: {len(contaminated_dates)}")
for d in contaminated_dates:
    n_stocks = inst[inst["date"] == d]["stock_id"].nunique()
    n_nonzero = ((inst[inst["date"] == d]["buy"] != 0) | (inst[inst["date"] == d]["sell"] != 0)).sum()
    print(f"  {d.date()}: {n_stocks} stocks affected, {n_nonzero} rows with real non-zero values")

assert contaminated_dates == [pd.Timestamp("2026-06-19")], \
    f"Expected only 2026-06-19 as contaminated; found {contaminated_dates}"
print("\nConfirmed: 2026-06-19 is the ONLY non-trading-day contamination in the full sample period.")

# ---- 3. Missing-State Classification ----
# Build the full expected grid: (stock_id, date, category) for every date each
# stock has a PRICE row (i.e., every date the stock was actually tradeable).
stock_trading_days = price.groupby("stock_id")["date"].apply(set).to_dict()
stock_volume = price.set_index(["stock_id", "date"])["volume"]

grid_rows = []
for sid, days in stock_trading_days.items():
    for d in days:
        for cat in CATS:
            grid_rows.append((sid, d, cat))
grid = pd.DataFrame(grid_rows, columns=["stock_id", "date", "name"])
print(f"\nExpected grid (stock x tradeable-date x category): {len(grid)} cells")

inst_present = inst.set_index(["stock_id", "date", "name"])[["buy", "sell"]]
grid = grid.set_index(["stock_id", "date", "name"])
merged = grid.join(inst_present, how="left")
merged = merged.reset_index()

vol = price.set_index(["stock_id", "date"])["volume"]
merged["stock_volume"] = merged.set_index(["stock_id", "date"]).index.map(vol)

def classify(row):
    if row["date"] not in trading_calendar:
        return "non_trading_day"  # shouldn't occur given grid is built from price dates, safety net
    if pd.isna(row["buy"]):
        # no institutional row at all for this stock/date/category
        if row["stock_volume"] == 0:
            return "trading_halt"
        else:
            return "source_missing"
    if row["buy"] == 0 and row["sell"] == 0:
        return "observed_zero"
    return "active"

merged["missing_state"] = merged.apply(classify, axis=1)

print("\nMissing-state distribution (stock x tradeable-date x category grid):")
print(merged["missing_state"].value_counts())
merged.to_csv(OUT_DIR / "rp001_missing_state_classification.csv", index=False)

# ---- Also classify the contaminated 06-19 rows explicitly ----
contam = inst[inst["date"] == pd.Timestamp("2026-06-19")].copy()
contam["missing_state"] = "non_trading_day"
print(f"\n2026-06-19 rows explicitly classified as non_trading_day: {len(contam)} rows, "
      f"to be EXCLUDED from the feature pipeline entirely.")
contam.to_csv(OUT_DIR / "rp001_non_trading_day_exclusions.csv", index=False)

print("\n=== SUMMARY ===")
print(merged["missing_state"].value_counts(normalize=True).mul(100).round(3))
