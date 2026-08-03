from pathlib import Path
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
INST_DIR = ROOT / "rp001_data" / "raw"
PRICE_DIR = ROOT / "rp001_data" / "raw_price"

inst = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(INST_DIR.glob("inst_*.csv"))], ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]
inst_wide = inst.pivot_table(index=["stock_id", "date"], columns="name", values="net", aggfunc="first").reset_index()
inst_keys = set(zip(inst_wide["stock_id"], inst_wide["date"]))

price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(PRICE_DIR.glob("price_*.csv"))], ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
price_keys = set(zip(price["stock_id"], price["date"]))

inst_only = inst_keys - price_keys   # in institutional data, missing from price
price_only = price_keys - inst_keys  # in price data, missing from institutional

print(f"Institutional-only keys (no matching price row): {len(inst_only)}")
print(f"Price-only keys (no matching institutional row): {len(price_only)}")

print("\n--- Institutional-only rows (sample, sorted by date) ---")
for sid, d in sorted(inst_only, key=lambda x: x[1])[:60]:
    print(sid, d.date())

print("\n--- Price-only rows (sample, sorted by date) ---")
for sid, d in sorted(price_only, key=lambda x: x[1])[:60]:
    print(sid, d.date())

# check: are inst_only dates concentrated at start/end of sample (listing/delisting-like) or scattered (holiday/halt-like)?
import collections
inst_only_by_stock = collections.Counter(sid for sid, d in inst_only)
price_only_by_stock = collections.Counter(sid for sid, d in price_only)
print("\ninst_only count by stock:", dict(inst_only_by_stock))
print("price_only count by stock:", dict(price_only_by_stock))
