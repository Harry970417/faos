import time
from pathlib import Path
import pandas as pd
import requests

API_URL = "https://api.finmindtrade.com/api/v4/data"
START_DATE = "2024-07-01"
END_DATE = "2026-07-09"

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "raw_price"
RAW_DIR.mkdir(parents=True, exist_ok=True)

stocks = pd.read_csv(
    r"C:\Users\user\Desktop\taiwan-attention-signal\config\stock_list_50.csv",
    dtype={"stock_id": str},
)

results = []
for _, row in stocks.iterrows():
    sid = row["stock_id"]
    out_path = RAW_DIR / f"price_{sid}.csv"
    if out_path.exists():
        df = pd.read_csv(out_path)
        results.append({"stock_id": sid, "ok": True, "n_rows": len(df)})
        continue
    try:
        resp = requests.get(API_URL, params={
            "dataset": "TaiwanStockPrice",
            "data_id": sid, "start_date": START_DATE, "end_date": END_DATE,
        }, timeout=30)
        payload = resp.json()
        if payload.get("status") != 200:
            results.append({"stock_id": sid, "ok": False, "n_rows": 0, "err": payload.get("msg")})
            print(f"{sid}: FAIL {payload.get('msg')}")
            time.sleep(1)
            continue
        df = pd.DataFrame(payload.get("data", []))
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        results.append({"stock_id": sid, "ok": True, "n_rows": len(df)})
        print(f"{sid}: OK n_rows={len(df)}")
    except Exception as e:
        results.append({"stock_id": sid, "ok": False, "n_rows": 0, "err": str(e)})
        print(f"{sid}: ERROR {e}")
    time.sleep(0.5)

summary = pd.DataFrame(results)
print(f"\nTotal: {len(summary)} OK: {summary['ok'].sum()}")
