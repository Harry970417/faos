"""RP-001 permanent regression test: the 2026-06-19 non-trading-day
contamination must never re-enter the feature pipeline. Run this as part
of every future feature rebuild.
"""
import pandas as pd
from pathlib import Path

def test_20260619_excluded():
    feat_path = Path(r"C:\Users\user\Desktop\faos\rp001_data\features\rp001_features_v0.2.parquet")
    feat = pd.read_parquet(feat_path)
    n = (feat["date"] == "2026-06-19").sum()
    assert n == 0, f"REGRESSION: 2026-06-19 contamination has re-entered the feature panel ({n} rows found)"
    print("PASS: 2026-06-19 regression test — no contamination present")

def test_trading_calendar_gate_active():
    price_dir = Path(r"C:\Users\user\Desktop\faos\rp001_data\raw_price")
    price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted(price_dir.glob("price_*.csv"))], ignore_index=True)
    price["date"] = pd.to_datetime(price["date"])
    assert "2026-06-19" not in price["date"].astype(str).values, \
        "REGRESSION: price data now has 2026-06-19 — trading calendar assumption changed, re-verify"
    print("PASS: trading calendar still confirms 2026-06-19 as a non-trading day")

if __name__ == "__main__":
    test_20260619_excluded()
    test_trading_calendar_gate_active()
    print("\nAll regression tests passed.")
