import time
from pathlib import Path
import pandas as pd
import requests

API_URL = "https://api.finmindtrade.com/api/v4/data"
START_DATE = "2024-07-01"
END_DATE = "2026-07-09"
ROOT = Path(r"C:\Users\user\Desktop\faos")
OUT_DIR = ROOT / "rp001_data" / "raw_valuation"
OUT_DIR.mkdir(parents=True, exist_ok=True)

stocks = pd.read_csv(r"C:\Users\user\Desktop\taiwan-attention-signal\config\stock_list_50.csv", dtype={"stock_id": str})
for _, row in stocks.iterrows():
    sid = row["stock_id"]
    out_path = OUT_DIR / f"val_{sid}.csv"
    if out_path.exists():
        continue
    try:
        resp = requests.get(API_URL, params={"dataset": "TaiwanStockPER", "data_id": sid,
                                                "start_date": START_DATE, "end_date": END_DATE}, timeout=30)
        payload = resp.json()
        if payload.get("status") != 200:
            print(f"{sid}: FAIL {payload.get('msg')}")
            time.sleep(1); continue
        df = pd.DataFrame(payload.get("data", []))
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        print(f"{sid}: OK n_rows={len(df)}")
    except Exception as e:
        print(f"{sid}: ERROR {e}")
    time.sleep(0.5)
