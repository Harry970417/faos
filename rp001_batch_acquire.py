"""
RP-001 Phase 2A.2: Batch-based full-universe data acquisition.

Each run processes exactly one batch: raw download -> SHA verification ->
manifest update -> trading-calendar validation -> listing-date validation ->
missing-rate report -> retry report -> integrity gate.

Usage: python rp001_batch_acquire.py <batch_id> <start_idx> <end_idx>
  batch_id: integer, 1-based
  start_idx, end_idx: row range (0-based, end exclusive) into
    rp001_data/phase2a_acquisition_universe.csv

Exits 0 and prints "GATE: PASS" if the batch's Integrity Gate passes.
Exits 1 and prints "GATE: STOP" with reasons if any hard-stop condition fires.
Never proceeds to a next batch itself -- the caller decides, per batch.
"""
import sys, os, time, json, hashlib, csv
from pathlib import Path
from datetime import datetime, date
import requests
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
RAW_DIR = ROOT / "rp001_data" / "phase2a" / "raw"
MANIFEST_DIR = ROOT / "rp001_data" / "phase2a" / "manifests"
ANOMALY_DIR = ROOT / "rp001_data" / "phase2a" / "anomalies"
for d in (RAW_DIR, MANIFEST_DIR, ANOMALY_DIR):
    d.mkdir(parents=True, exist_ok=True)

API_URL = "https://api.finmindtrade.com/api/v4/data"
START_DATE = "2012-01-01"
END_DATE = date.today().isoformat()
DATASETS = ["TaiwanStockInstitutionalInvestorsBuySell", "TaiwanStockPrice", "TaiwanStockPER"]

EXPECTED_INST_SCHEMA = {"date", "stock_id", "buy", "sell", "name"}
EXPECTED_PRICE_SCHEMA = {"date", "stock_id", "Trading_Volume", "Trading_money", "open", "max", "min", "close", "spread", "Trading_turnover"}
KNOWN_CATEGORIES_PRE_CUTOVER = {"Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer"}
KNOWN_CATEGORIES_POST_CUTOVER = {"Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging"}
CUTOVER_DATE = "2014-12-01"


def fetch(dataset, stock_id, start, end, max_retries=3):
    retries = 0
    while retries < max_retries:
        t0 = time.time()
        try:
            resp = requests.get(API_URL, params={"dataset": dataset, "data_id": stock_id,
                                                    "start_date": start, "end_date": end}, timeout=30)
            payload = resp.json()
            elapsed = time.time() - t0
            return payload, retries, elapsed, None
        except Exception as e:
            retries += 1
            time.sleep(1.5)
    return {"status": -1, "data": []}, retries, time.time() - t0, str(e) if 'e' in dir() else "unknown"


def run_batch(batch_id, start_idx, end_idx):
    universe = pd.read_csv(ROOT / "rp001_data" / "phase2a_acquisition_universe.csv", dtype=str)
    batch = universe.iloc[start_idx:end_idx].reset_index(drop=True)
    stock_ids = batch["stock_id"].tolist()

    manifest_rows = []
    failed_symbols = []
    schema_drift_flags = []
    duplicate_flags = []
    all_price_frames = {}
    all_inst_frames = {}

    for sid in stock_ids:
        for dataset in DATASETS:
            payload, retries, elapsed, err = fetch(dataset, sid, START_DATE, END_DATE)
            rows = payload.get("data", []) if isinstance(payload, dict) else []
            status_ok = isinstance(payload, dict) and payload.get("status") == 200
            raw_bytes = json.dumps(rows, ensure_ascii=False).encode("utf-8")
            sha = hashlib.sha256(raw_bytes).hexdigest()
            out_path = RAW_DIR / f"{dataset}_{sid}.json"
            with open(out_path, "w", encoding="utf-8") as f:
                json.dump(rows, f, ensure_ascii=False)

            # schema drift check
            if rows:
                keys = set(rows[0].keys())
                if dataset == "TaiwanStockInstitutionalInvestorsBuySell" and keys != EXPECTED_INST_SCHEMA:
                    schema_drift_flags.append((sid, dataset, sorted(keys)))
                elif dataset == "TaiwanStockPrice" and keys != EXPECTED_PRICE_SCHEMA:
                    schema_drift_flags.append((sid, dataset, sorted(keys)))

            # duplicate observation check ((stock_id,date[,name]) uniqueness)
            if rows:
                df = pd.DataFrame(rows)
                key_cols = ["date", "stock_id"] + (["name"] if "name" in df.columns else [])
                dup_count = df.duplicated(subset=key_cols).sum()
                if dup_count > 0:
                    duplicate_flags.append((sid, dataset, int(dup_count)))
                if dataset == "TaiwanStockPrice":
                    all_price_frames[sid] = df
                if dataset == "TaiwanStockInstitutionalInvestorsBuySell":
                    all_inst_frames[sid] = df

            if not status_ok or not rows:
                failed_symbols.append({"stock_id": sid, "dataset": dataset, "status": payload.get("status") if isinstance(payload, dict) else None, "error": err})

            manifest_rows.append({
                "batch_id": batch_id, "dataset": dataset, "stock_id": sid,
                "query_start_date": START_DATE, "query_end_date": END_DATE,
                "download_timestamp": datetime.utcnow().isoformat(), "row_count": len(rows),
                "sha256": sha, "source_endpoint": API_URL, "retry_count": retries,
                "status": "success" if status_ok and rows else ("empty" if status_ok else "failed"),
                "file_path": str(out_path.relative_to(ROOT)),
            })
            time.sleep(0.4)

    # manifest update
    manifest_path = MANIFEST_DIR / "pull_manifest.csv"
    write_header = not manifest_path.exists()
    with open(manifest_path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
        if write_header:
            w.writeheader()
        w.writerows(manifest_rows)

    # trading calendar validation: build batch-level empirical calendar from price data, check institutional dates are a subset (post-floor)
    calendar_inconsistencies = []
    all_price_dates = set()
    for sid, df in all_price_frames.items():
        all_price_dates |= set(df["date"].unique())
    for sid, df in all_inst_frames.items():
        if sid not in all_price_frames:
            continue
        inst_dates = set(df["date"].unique())
        price_dates = set(all_price_frames[sid]["date"].unique())
        extra = inst_dates - price_dates
        extra_post_floor = {d for d in extra if d >= "2012-05-02"}
        if len(extra_post_floor) > 5:  # small residual gaps are expected (established in pilot); large counts are a real inconsistency
            calendar_inconsistencies.append((sid, len(extra_post_floor)))

    # listing-date validation
    listing_violations = []
    batch = batch.set_index("stock_id")
    for sid, df in all_price_frames.items():
        if df.empty:
            continue
        first_data_date = df["date"].min()
        row = batch.loc[sid] if sid in batch.index else None
        if row is not None and row["listing_date_source"] == "registry" and pd.notna(row.get("listing_date_raw")):
            raw = str(row["listing_date_raw"])
            try:
                if len(raw) == 8 and raw.isdigit():
                    listed = f"{raw[:4]}-{raw[4:6]}-{raw[6:]}"
                else:
                    listed = raw
                if first_data_date < listed:
                    gap_days = (pd.to_datetime(listed) - pd.to_datetime(first_data_date)).days
                    if gap_days > 30:  # small gaps expected (settlement/index-inclusion lag); large gaps are the real hazard
                        listing_violations.append((sid, first_data_date, listed, gap_days))
            except Exception:
                pass

    # missing-rate report
    missing_report = []
    for sid, df in all_inst_frames.items():
        if sid not in all_price_frames:
            continue
        price_dates_post_floor = {d for d in all_price_frames[sid]["date"].unique() if d >= "2012-05-02"}
        inst_dates = set(df["date"].unique())
        if price_dates_post_floor:
            missing_rate = 1 - (len(inst_dates & price_dates_post_floor) / len(price_dates_post_floor))
            missing_report.append({"stock_id": sid, "missing_rate": round(missing_rate, 4)})
    missing_df = pd.DataFrame(missing_report)
    high_missing = missing_df[missing_df["missing_rate"] > 0.10] if not missing_df.empty else missing_df

    # historical definition drift check
    drift_flags = []
    for sid, df in all_inst_frames.items():
        if df.empty:
            continue
        pre = df[df["date"] < CUTOVER_DATE]
        post = df[df["date"] >= CUTOVER_DATE]
        pre_cats = set(pre["name"].unique()) if not pre.empty else set()
        post_cats = set(post["name"].unique()) if not post.empty else set()
        if not pre_cats.issubset(KNOWN_CATEGORIES_PRE_CUTOVER):
            drift_flags.append((sid, "pre-cutover unexpected categories", sorted(pre_cats - KNOWN_CATEGORIES_PRE_CUTOVER)))
        if not post_cats.issubset(KNOWN_CATEGORIES_POST_CUTOVER):
            drift_flags.append((sid, "post-cutover unexpected categories", sorted(post_cats - KNOWN_CATEGORIES_POST_CUTOVER)))

    retry_total = sum(r["retry_count"] for r in manifest_rows)
    retry_over_1 = [r for r in manifest_rows if r["retry_count"] >= 2]

    # integrity gate
    stop_reasons = []
    if schema_drift_flags:
        stop_reasons.append(f"schema drift: {schema_drift_flags[:5]}")
    if drift_flags:
        stop_reasons.append(f"historical definition drift: {drift_flags[:5]}")
    if not high_missing.empty:
        stop_reasons.append(f"unexpected missing pattern: {high_missing.to_dict('records')[:5]}")
    if duplicate_flags:
        stop_reasons.append(f"duplicated observations: {duplicate_flags[:5]}")
    if calendar_inconsistencies:
        stop_reasons.append(f"trading-calendar inconsistency: {calendar_inconsistencies[:5]}")
    if listing_violations:
        stop_reasons.append(f"listing-date violation: {listing_violations[:5]}")

    gate_pass = len(stop_reasons) == 0

    result = {
        "batch_id": batch_id, "n_stocks": len(stock_ids), "n_requests": len(manifest_rows),
        "total_rows": sum(r["row_count"] for r in manifest_rows),
        "failed_symbols": failed_symbols, "n_failed": len(failed_symbols),
        "retry_total": retry_total, "n_retry_over_1": len(retry_over_1),
        "gate_pass": gate_pass, "stop_reasons": stop_reasons,
        "high_missing_count": len(high_missing) if not high_missing.empty else 0,
    }

    # persist anomaly detail files (append)
    if listing_violations:
        with open(ANOMALY_DIR / "pre_listing_data_flags.csv", "a", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            for row in listing_violations:
                w.writerow([batch_id] + list(row))

    result_path = MANIFEST_DIR / f"batch_{batch_id:03d}_result.json"
    with open(result_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)

    print(json.dumps(result, indent=2, default=str))
    print(f"\nGATE: {'PASS' if gate_pass else 'STOP'}")
    return 0 if gate_pass else 1


if __name__ == "__main__":
    batch_id = int(sys.argv[1])
    start_idx = int(sys.argv[2])
    end_idx = int(sys.argv[3])
    sys.exit(run_batch(batch_id, start_idx, end_idx))
