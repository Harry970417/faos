import time, json, hashlib
from pathlib import Path
import requests
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
PILOT_DIR = ROOT / "rp001_data" / "pilot"
PILOT_DIR.mkdir(parents=True, exist_ok=True)
API_URL = "https://api.finmindtrade.com/api/v4/data"

PILOT_STOCKS = {
    "1101": "TWSE, old (1962), high-liquidity",
    "6986": "TPEx, newest listing (2026-06-26)",
    "4987": "Delisted 2026-05-29",
    "7827": "TWSE newly listed (2026-05-29)",
    "2891": "Financial holding (TWSE)",
    "0050": "ETF (TWSE)",
    "1264": "Small-cap / lower-liquidity candidate",
}

log = []
for sid, desc in PILOT_STOCKS.items():
    for dataset, start, end in [
        ("TaiwanStockInstitutionalInvestorsBuySell", "2012-01-01", "2026-07-09"),
        ("TaiwanStockPrice", "2012-01-01", "2026-07-09"),
    ]:
        t0 = time.time()
        retries = 0
        while retries < 3:
            try:
                resp = requests.get(API_URL, params={"dataset": dataset, "data_id": sid,
                                                        "start_date": start, "end_date": end}, timeout=30)
                payload = resp.json()
                break
            except Exception as e:
                retries += 1
                time.sleep(1)
                payload = {"status": -1, "msg": str(e), "data": []}
        elapsed = time.time() - t0
        rows = payload.get("data", [])
        raw_bytes = json.dumps(rows, ensure_ascii=False).encode("utf-8")
        sha = hashlib.sha256(raw_bytes).hexdigest()
        out_path = PILOT_DIR / f"{dataset}_{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        log.append({
            "stock_id": sid, "desc": desc, "dataset": dataset, "status": payload.get("status"),
            "n_rows": len(rows), "elapsed_sec": round(elapsed, 3), "retries": retries,
            "sha256": sha, "file_size_bytes": out_path.stat().st_size,
        })
        print(f"{sid} ({desc}) / {dataset}: status={payload.get('status')} n_rows={len(rows)} "
              f"elapsed={elapsed:.2f}s retries={retries}")
        time.sleep(0.4)

log_df = pd.DataFrame(log)
log_df.to_csv(PILOT_DIR / "pilot_pull_log.csv", index=False)
print(f"\nTotal pilot requests: {len(log_df)}  Total rows: {log_df['n_rows'].sum()}  "
      f"Total time: {log_df['elapsed_sec'].sum():.1f}s  Total bytes: {log_df['file_size_bytes'].sum():,}")
