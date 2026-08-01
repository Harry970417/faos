"""
Thin wrapper around rp001_batch_acquire.run_batch: retries through HTTP 402
rate-limit pauses (exit code 2) automatically, sleeping for the quota reset
window, and only returns once a batch reaches a real PASS/STOP verdict.

Usage: python rp001_batch_driver.py <batch_id> <start_idx> <end_idx> [max_requests]
Exit codes pass through from run_batch: 0 PASS, 1 STOP (needs investigation).
"""
import sys, time
from datetime import datetime, timezone
from rp001_batch_acquire import run_batch

RETRY_SLEEP_SECONDS = 65 * 60  # a bit over an hour, safely past any reset window


def log(msg):
    print(f"[{datetime.now(timezone.utc).isoformat()}] {msg}", flush=True)


def main():
    batch_id = int(sys.argv[1])
    start_idx = int(sys.argv[2])
    end_idx = int(sys.argv[3])
    max_requests = int(sys.argv[4]) if len(sys.argv) > 4 else 250

    attempt = 0
    while True:
        attempt += 1
        log(f"Batch {batch_id}: attempt {attempt}")
        rc = run_batch(batch_id, start_idx, end_idx, max_requests)
        if rc == 2:
            log(f"Batch {batch_id}: rate-limited, sleeping {RETRY_SLEEP_SECONDS}s before retry")
            time.sleep(RETRY_SLEEP_SECONDS)
            continue
        log(f"Batch {batch_id}: resolved, exit code {rc}")
        sys.exit(rc)


if __name__ == "__main__":
    main()
