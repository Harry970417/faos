import time
import json
from pathlib import Path
import pandas as pd
import requests

API_URL = "https://api.finmindtrade.com/api/v4/data"
START_DATE = "2024-07-01"
END_DATE = "2026-07-09"

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "raw"
RAW_DIR.mkdir(parents=True, exist_ok=True)

stocks = pd.read_csv(
    r"C:\Users\user\Desktop\taiwan-attention-signal\config\stock_list_50.csv",
    dtype={"stock_id": str},
)

results = []
for _, row in stocks.iterrows():
    sid = row["stock_id"]
    out_path = RAW_DIR / f"inst_{sid}.csv"
    if out_path.exists():
        df = pd.read_csv(out_path)
        results.append({"stock_id": sid, "ok": True, "n_rows": len(df), "err": ""})
        continue
    try:
        resp = requests.get(API_URL, params={
            "dataset": "TaiwanStockInstitutionalInvestorsBuySell",
            "data_id": sid, "start_date": START_DATE, "end_date": END_DATE,
        }, timeout=30)
        payload = resp.json()
        if payload.get("status") != 200:
            results.append({"stock_id": sid, "ok": False, "n_rows": 0, "err": f"status {payload.get('status')}: {payload.get('msg')}"})
            print(f"{sid}: FAIL {payload.get('msg')}")
            time.sleep(1)
            continue
        data = payload.get("data", [])
        df = pd.DataFrame(data)
        df.to_csv(out_path, index=False, encoding="utf-8-sig")
        results.append({"stock_id": sid, "ok": True, "n_rows": len(df), "err": ""})
        print(f"{sid}: OK n_rows={len(df)}")
    except Exception as e:
        results.append({"stock_id": sid, "ok": False, "n_rows": 0, "err": f"{type(e).__name__}: {e}"})
        print(f"{sid}: ERROR {e}")
    time.sleep(0.5)

summary = pd.DataFrame(results)
summary.to_csv(ROOT / "rp001_data" / "pull_summary.csv", index=False)
print("\n=== SUMMARY ===")
print(f"Total: {len(summary)}  OK: {summary['ok'].sum()}  Failed: {(~summary['ok']).sum()}")
if (~summary["ok"]).any():
    print(summary[~summary["ok"]])
