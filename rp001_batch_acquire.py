"""
RP-001 Phase 2A.2 (resumed under Phase 2A.2-R Decision Gate): Batch-based
full-universe data acquisition, v2.

v2 changes vs. the Batch-1 version (RP001_API_AND_SOURCE_FEASIBILITY.md §5):
  - skip-existing: won't re-download a (dataset, stock_id) already `success`
    in the manifest.
  - rate-aware pacing: stops issuing new requests once `max_requests` is hit
    in this run (default 260, a safety margin under the documented 300/hr
    anonymous ceiling) rather than running into a 402 wall mid-symbol.
  - failed-symbol queue: any non-success (dataset, stock_id) pair is written
    to rp001_data/phase2a/manifests/failed_queue.csv for a later retry pass,
    instead of being silently dropped when a batch ends early.
  - Integrity Gate narrowed per RP001_PHASE2A2R_DECISION_GATE.md §7: the
    three anomaly types fully characterized in Phase 2A.2-R (Dealer
    recurrence OUTSIDE the break window, missing-rate patterns, listing-date
    gaps) now WARN and log instead of hard-STOP, since they're governed by
    RP001_MISSINGNESS_POLICY.md / RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md.
    Genuinely new anomaly types (schema drift beyond the known 6 categories,
    duplicated observations, trading-calendar inconsistency, or Dealer
    recurrence INSIDE the break window) still hard-STOP.

Usage: python rp001_batch_acquire.py <batch_id> <start_idx> <end_idx> [max_requests]
Exits 0 and prints "GATE: PASS" (batch fully done, no new-anomaly stop).
Exits 2 and prints "PAUSED: rate limit" if max_requests was hit before the
  batch finished -- not a failure, just needs another invocation to continue.
Exits 1 and prints "GATE: STOP" if a genuinely new anomaly type fires.
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
KNOWN_CATEGORIES = {"Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer", "Dealer_self", "Dealer_Hedging"}
CUTOVER_DATE = "2014-12-01"
BREAK_START, BREAK_END = "2025-08-01", "2025-10-31"
MANIFEST_PATH = MANIFEST_DIR / "pull_manifest.csv"
FAILED_QUEUE_PATH = MANIFEST_DIR / "failed_queue.csv"


def load_existing_success():
    """(dataset, stock_id) pairs already successfully downloaded, per the manifest."""
    if not MANIFEST_PATH.exists():
        return set()
    m = pd.read_csv(MANIFEST_PATH, dtype=str)
    ok = m[m["status"] == "success"]
    return set(zip(ok["dataset"], ok["stock_id"]))


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


def run_batch(batch_id, start_idx, end_idx, max_requests=260):
    universe = pd.read_csv(ROOT / "rp001_data" / "phase2a_acquisition_universe.csv", dtype=str)
    batch = universe.iloc[start_idx:end_idx].reset_index(drop=True)
    stock_ids = batch["stock_id"].tolist()

    already_done = load_existing_success()
    todo = [(sid, ds) for sid in stock_ids for ds in DATASETS if (ds, sid) not in already_done]
    skipped = len(stock_ids) * len(DATASETS) - len(todo)
    print(f"Batch {batch_id}: {len(stock_ids)} stocks, {len(todo)} requests needed ({skipped} already cached, skipped)")

    manifest_rows = []
    failed_rows = []
    n_requests_this_run = 0
    hit_rate_cap = False

    for sid, dataset in todo:
        if n_requests_this_run >= max_requests:
            hit_rate_cap = True
            break
        payload, retries, elapsed, err = fetch(dataset, sid, START_DATE, END_DATE)
        n_requests_this_run += 1
        rows = payload.get("data", []) if isinstance(payload, dict) else []
        status_ok = isinstance(payload, dict) and payload.get("status") == 200
        raw_bytes = json.dumps(rows, ensure_ascii=False).encode("utf-8")
        sha = hashlib.sha256(raw_bytes).hexdigest()
        out_path = RAW_DIR / f"{dataset}_{sid}.json"
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)

        status = "success" if status_ok and rows else ("empty" if status_ok else "failed")
        row = {
            "batch_id": batch_id, "dataset": dataset, "stock_id": sid,
            "query_start_date": START_DATE, "query_end_date": END_DATE,
            "download_timestamp": datetime.utcnow().isoformat(), "row_count": len(rows),
            "sha256": sha, "source_endpoint": API_URL, "retry_count": retries,
            "status": status, "file_path": str(out_path.relative_to(ROOT)),
        }
        manifest_rows.append(row)
        if status != "success":
            failed_rows.append({"batch_id": batch_id, "dataset": dataset, "stock_id": sid,
                                 "http_status": payload.get("status") if isinstance(payload, dict) else None,
                                 "error": err, "queued_at": datetime.utcnow().isoformat()})
            if payload.get("status") == 402:
                print(f"  HTTP 402 (quota) at request {n_requests_this_run}/{len(todo)} -- stopping this run early.")
                hit_rate_cap = True
                break
        time.sleep(0.4)

    if manifest_rows:
        write_header = not MANIFEST_PATH.exists()
        with open(MANIFEST_PATH, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(manifest_rows[0].keys()))
            if write_header:
                w.writeheader()
            w.writerows(manifest_rows)

    if failed_rows:
        write_header = not FAILED_QUEUE_PATH.exists()
        with open(FAILED_QUEUE_PATH, "a", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(failed_rows[0].keys()))
            if write_header:
                w.writeheader()
            w.writerows(failed_rows)

    n_success_this_run = sum(1 for r in manifest_rows if r["status"] == "success")
    print(f"This run: {n_requests_this_run} requests issued, {n_success_this_run} succeeded, {len(failed_rows)} failed/queued")

    remaining = len(todo) - n_requests_this_run
    non_402_failures = [r for r in failed_rows if r.get("http_status") != 402]
    if hit_rate_cap or remaining > 0:
        print(f"PAUSED: rate limit -- {remaining} requests still pending for batch {batch_id}. Re-run the same command to continue.")
        return 2
    if non_402_failures:
        # Real failures (network/connectivity, not quota) leave the batch incomplete --
        # these pairs stay non-"success" in the manifest, so the next invocation's
        # todo list picks them up automatically via load_existing_success(). Do not
        # run the Integrity Gate over a batch with known-missing data.
        print(f"PAUSED: {len(non_402_failures)} non-quota failures (connectivity?) left {len(non_402_failures)} pairs incomplete -- see failed_queue.csv. Re-run the same command to retry.")
        return 2

    # --- Batch complete: run Integrity Gate over the FULL batch (not just this run's slice) ---
    return _integrity_gate(batch_id, stock_ids, batch)


def _integrity_gate(batch_id, stock_ids, batch):
    m = pd.read_csv(MANIFEST_PATH, dtype=str)
    batch_manifest = m[(m["stock_id"].isin(stock_ids))]

    all_price_frames, all_inst_frames = {}, {}
    schema_drift_flags, duplicate_flags = [], []
    for sid in stock_ids:
        for dataset, store in (("TaiwanStockPrice", all_price_frames), ("TaiwanStockInstitutionalInvestorsBuySell", all_inst_frames)):
            p = RAW_DIR / f"{dataset}_{sid}.json"
            if not p.exists():
                continue
            rows = json.loads(p.read_text(encoding="utf-8"))
            if not rows:
                continue
            df = pd.DataFrame(rows)
            store[sid] = df
            keys = set(rows[0].keys())
            expected = EXPECTED_INST_SCHEMA if dataset == "TaiwanStockInstitutionalInvestorsBuySell" else EXPECTED_PRICE_SCHEMA
            if keys != expected:
                schema_drift_flags.append((sid, dataset, sorted(keys)))
            key_cols = ["date", "stock_id"] + (["name"] if "name" in df.columns else [])
            dup_count = df.duplicated(subset=key_cols).sum()
            if dup_count > 0:
                duplicate_flags.append((sid, dataset, int(dup_count)))
            if dataset == "TaiwanStockInstitutionalInvestorsBuySell":
                unexpected_cats = set(df["name"].unique()) - KNOWN_CATEGORIES
                if unexpected_cats:
                    schema_drift_flags.append((sid, "unexpected category", sorted(unexpected_cats)))

    # Dealer recurrence -- WARN unless it lands inside the break window (new/dangerous)
    dealer_in_break = []
    for sid, df in all_inst_frames.items():
        post = df[(df["name"] == "Dealer") & (df["date"] >= CUTOVER_DATE)]
        if post.empty:
            continue
        in_break = post[(post["date"] >= BREAK_START) & (post["date"] <= BREAK_END)]
        if not in_break.empty:
            dealer_in_break.append(sid)

    # trading-calendar inconsistency -- unchanged hard-stop condition (residual gaps > 5 are still a real inconsistency)
    calendar_inconsistencies = []
    all_price_dates = set()
    for sid, df in all_price_frames.items():
        all_price_dates |= set(df["date"].unique())
    for sid, df in all_inst_frames.items():
        if sid not in all_price_frames:
            continue
        extra = set(df["date"].unique()) - set(all_price_frames[sid]["date"].unique())
        extra_post_floor = {d for d in extra if d >= "2012-05-02"}
        if len(extra_post_floor) > 5:
            calendar_inconsistencies.append((sid, len(extra_post_floor)))

    # --- Hard-stop conditions (genuinely new, not characterized by Phase 2A.2-R) ---
    stop_reasons = []
    if schema_drift_flags:
        stop_reasons.append(f"schema drift (new/unexpected): {schema_drift_flags[:5]}")
    if duplicate_flags:
        stop_reasons.append(f"duplicated observations: {duplicate_flags[:5]}")
    if calendar_inconsistencies:
        stop_reasons.append(f"trading-calendar inconsistency: {calendar_inconsistencies[:5]}")
    if dealer_in_break:
        stop_reasons.append(f"Dealer recurrence INSIDE the locked break window (new -- not seen in Phase 2A.2-R's 86-stock check): {dealer_in_break}")

    # --- Downgraded-to-WARN conditions (logged, do not stop) ---
    warnings = []
    high_missing = []
    for sid, df in all_inst_frames.items():
        if sid not in all_price_frames:
            continue
        price_dates_post_floor = {d for d in all_price_frames[sid]["date"].unique() if d >= "2012-05-02"}
        inst_dates = set(df["date"].unique())
        if price_dates_post_floor:
            rate = 1 - (len(inst_dates & price_dates_post_floor) / len(price_dates_post_floor))
            if rate > 0.10:
                high_missing.append({"stock_id": sid, "missing_rate": round(rate, 4)})
    if high_missing:
        warnings.append(f"missing-rate > 10% (governed by RP001_MISSINGNESS_POLICY.md, not a stop): {len(high_missing)} stocks")

    listing_violations = []
    batch_idx = batch.set_index("stock_id")
    for sid, df in all_price_frames.items():
        if df.empty or sid not in batch_idx.index:
            continue
        row = batch_idx.loc[sid]
        if row["listing_date_source"] == "registry" and pd.notna(row.get("listing_date_raw")):
            raw = str(row["listing_date_raw"])
            try:
                listed = f"{raw[:4]}-{raw[4:6]}-{raw[6:]}" if len(raw) == 8 and raw.isdigit() else raw
                first_data_date = df["date"].min()
                if first_data_date < listed:
                    gap_days = (pd.to_datetime(listed) - pd.to_datetime(first_data_date)).days
                    if gap_days > 30:
                        listing_violations.append((sid, first_data_date, listed, gap_days))
            except Exception:
                pass
    if listing_violations:
        warnings.append(f"listing-date gap > 30 days (governed by RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md, not a stop): {len(listing_violations)} stocks")

    dealer_recurrence_outside_break = [sid for sid, df in all_inst_frames.items()
                                        if not df[(df["name"] == "Dealer") & (df["date"] >= CUTOVER_DATE)].empty
                                        and sid not in dealer_in_break]
    if dealer_recurrence_outside_break:
        warnings.append(f"Dealer recurrence outside break window (governed by D-04 downgrade, not a stop): {dealer_recurrence_outside_break}")

    gate_pass = len(stop_reasons) == 0
    result = {
        "batch_id": batch_id, "n_stocks": len(stock_ids),
        "gate_pass": gate_pass, "stop_reasons": stop_reasons, "warnings": warnings,
        "high_missing_count": len(high_missing), "listing_violation_count": len(listing_violations),
    }
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
    max_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 260
    sys.exit(run_batch(batch_id, start_idx, end_idx, max_requests))
