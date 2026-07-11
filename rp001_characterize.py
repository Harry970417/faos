import pandas as pd
import numpy as np
from pathlib import Path
from collections import Counter

RAW_DIR = Path(r"C:\Users\user\Desktop\faos\rp001_data\raw")
files = sorted(RAW_DIR.glob("inst_*.csv"))
print(f"Files found: {len(files)}")

frames = []
for f in files:
    df = pd.read_csv(f, dtype={"stock_id": str})
    frames.append(df)
all_df = pd.concat(frames, ignore_index=True)
all_df["date"] = pd.to_datetime(all_df["date"])
print(f"Total rows: {len(all_df)}")

print("\n=== TIME COVERAGE ===")
print(f"Date range: {all_df['date'].min().date()} to {all_df['date'].max().date()}")
n_trading_days = all_df["date"].nunique()
print(f"Unique trading days observed: {n_trading_days}")

print("\n=== STOCK COVERAGE ===")
print(f"Unique stock_id: {all_df['stock_id'].nunique()} / 50 requested")
rows_per_stock = all_df.groupby("stock_id").size()
print(f"Rows per stock: min={rows_per_stock.min()} max={rows_per_stock.max()} mean={rows_per_stock.mean():.1f}")
short_stocks = rows_per_stock[rows_per_stock < rows_per_stock.median() - 20]
print(f"Stocks with notably fewer rows than median: {dict(short_stocks)}")

print("\n=== INSTITUTIONAL CATEGORY CHARACTERISTICS ===")
cat_counts = all_df["name"].value_counts()
print(cat_counts)
# expected: 5 categories x n_trading_days x n_stocks
expected_per_stock = n_trading_days * 5
print(f"\nExpected rows/stock if fully populated (5 categories x {n_trading_days} days): {expected_per_stock}")

print("\n=== MISSING VALUES (at row level: are buy/sell null?) ===")
print(f"Null buy: {all_df['buy'].isna().sum()}  Null sell: {all_df['sell'].isna().sum()}")

print("\n=== MISSING VALUES (at panel level: expected date x stock x category cells) ===")
full_index = pd.MultiIndex.from_product(
    [all_df["stock_id"].unique(), sorted(all_df["date"].unique()), cat_counts.index],
    names=["stock_id", "date", "name"]
)
actual_index = pd.MultiIndex.from_frame(all_df[["stock_id", "date", "name"]])
missing_cells = full_index.difference(actual_index)
print(f"Expected cells: {len(full_index)}  Actual cells present: {len(actual_index)}  Missing cells: {len(missing_cells)} ({len(missing_cells)/len(full_index)*100:.2f}%)")
missing_by_cat = Counter(x[2] for x in missing_cells)
print(f"Missing cells by category: {dict(missing_by_cat)}")

print("\n=== ZERO VALUES ===")
all_df["net"] = all_df["buy"] - all_df["sell"]
zero_rows = ((all_df["buy"] == 0) & (all_df["sell"] == 0))
print(f"Rows with buy=0 AND sell=0: {zero_rows.sum()} / {len(all_df)} ({zero_rows.mean()*100:.2f}%)")
zero_by_cat = all_df.groupby("name").apply(lambda g: ((g["buy"]==0)&(g["sell"]==0)).mean()*100)
print("Zero-rate by category (%):")
print(zero_by_cat.sort_values(ascending=False))

print("\n=== DISTRIBUTION (net = buy - sell, shares) ===")
for cat in cat_counts.index:
    sub = all_df[all_df["name"] == cat]["net"]
    print(f"{cat}: mean={sub.mean():,.0f} std={sub.std():,.0f} p1={sub.quantile(0.01):,.0f} p50={sub.median():,.0f} p99={sub.quantile(0.99):,.0f} max_abs={sub.abs().max():,.0f}")

print("\n=== ZERO-RATE BY STOCK (top 5 highest, to check if concentrated in specific names) ===")
zero_by_stock = all_df.groupby("stock_id").apply(lambda g: ((g["buy"]==0)&(g["sell"]==0)).mean()*100)
print(zero_by_stock.sort_values(ascending=False).head(5))
print(zero_by_stock.sort_values(ascending=False).tail(5))
