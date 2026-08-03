# RP-001 Phase 2A.2: Full Data Acquisition — Final Dataset

**Date:** 2026-08-02. **Status:** Complete. Full-universe acquisition Integrity Gate: **PASS** (all 19 batches). Machine-readable summary: `research/RP001_PHASE2A_DATA_MANIFEST.json`.

## 1. Scope

- **Universe:** 2,255 stock_ids (`rp001_data/phase2a_acquisition_universe.csv`) — 1,980 currently-listed (1,089 TWSE + 891 TPEx, per registry) + 275 delisted common stocks (via `TaiwanStockDelisting`, ETF-pattern codes excluded per D-03).
- **Datasets:** `TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice`, `TaiwanStockPER` — 3 per stock, 6,765 requests total.
- **Date range:** 2012-01-01 to acquisition-day end_date (2026-08-02), full available history per request, no server-side date-range cap encountered.
- **19 batches:** 18 × 120 stocks + 1 × 95 stocks. All resolved via `research/rp001_batch_acquire.py` v2's Integrity Gate.

## 2. Coverage

| Metric | Value |
|---|---|
| Universe stock_ids | 2,255 / 2,255 (100%) |
| (dataset, stock_id) pairs resolved | 6,765 / 6,765 (100%) |
| Pairs with zero manifest rows | 0 |
| Pairs stuck on a permanent failure (never resolved) | 0 |
| `status = success` (real data returned) | 6,261 |
| `status = empty` (HTTP 200, legitimately zero rows) | 504 — breakdown: 188 `TaiwanStockPER` (mostly TDR-style codes with no P/E data), 159 `TaiwanStockInstitutionalInvestorsBuySell` (stocks with no institutional activity ever recorded, e.g. very thin/short-lived listings), 157 `TaiwanStockPrice` (delisted stocks with no retrievable price history under FinMind's coverage) |
| Total data rows downloaded | 34,236,687 |
| Raw data on disk | 3.7 GB, 6,765 JSON files (`rp001_data/phase2a/raw/`, gitignored per instruction) |
| Total retries logged | 21 (all resolved; 0 unresolved) |

## 3. Integrity Gate outcome, per batch

Full detail in `research/RP001_PHASE2A_BATCH_TRACKER.md`. Summary: 16 of 19 batches raised at least one genuinely-new Integrity Gate STOP requiring individual investigation before resolution (none required a Deviation Policy Escalation); 3 batches (4, 17, 18) and the final batch (19) passed clean on the first evaluation.

- **Dealer-in-break-window (D-05 pattern):** 69 individually-verified instances across Batches 2, 5–16. Every single instance confirmed `Foreign_Investor` present on every break-window date carrying any institutional-category row — F_INST_01's constructibility is unaffected in 100% of checked cases, universe-wide.
- **Trading-calendar inconsistency (D-06/D-07 pattern):** 2 instances (stocks 1589, 2380, Batches 2–3), both root-caused to a shared, system-wide mis-dated-row phenomenon already structurally excluded by the existing Trading Calendar Gate.
- **Two acquisition-tooling bugs found and fixed** (Batch 8: gate could run over an incomplete batch after a connectivity outage; Batch 9: an infinite retry loop on legitimately-empty API responses) — both acquisition-only, no protocol impact, both retroactively verified not to have corrupted any already-resolved batch.
- **Zero occurrences** of schema drift beyond the known 6 institutional categories, duplicated observations, or any anomaly type not already characterized by Phase 2A.2-R.

## 4. Market-membership validation

Batch 10 (111/120 TPEx) and Batch 16 (mixed, includes stock 6986) provided the first real TPEx and 興櫃→TPEx test cases at scale — closing the two open items flagged by `research/RP001_PHASE2A2R_DECISION_GATE.md` §5. Zero schema-drift flags across any TPEx-heavy batch confirms F_INST_01 is market-agnostic, not a TWSE-only property. See `research/RP001_MARKET_MEMBERSHIP_AUDIT.md` §6.

## 5. Segment-level missingness pattern (observed, not a defect)

Missing-rate and listing-date-gap warning counts rose steadily from Batch 8 (73%/N-A) through a peak around Batch 15–16 (up to 111/120 stocks over threshold), then fell sharply in the final three batches (18: 23/120, 19: 18/95). This tracks the acquisition universe's composition — small-cap, recent-IPO, and TPEx-heavy stock segments cluster in the middle of the universe list — not a data-quality defect. Fully governed by `research/RP001_MISSINGNESS_POLICY.md`'s coverage gate throughout; no batch's warning count triggered a hard stop.

## 6. Directory structure

```
rp001_data/phase2a/
  raw/            6,765 JSON files, gitignored (per instruction: raw data never committed)
  manifests/
    pull_manifest.csv        one row per (batch, dataset, stock_id) attempt -- SHA-256, timestamp, row count, retry count, status
    failed_queue.csv         retry log -- every non-terminal failure, with timestamp
    batch_0XX_result.json    19 files -- per-batch Integrity Gate verdict, stop reasons, warnings
    acquisition_summary.json full-run rollup (source for RP001_PHASE2A_DATA_MANIFEST.json)
  anomalies/                 (reserved; anomaly detail lives in RP001_PHASE2A_DEVIATION_LOG.md / RP001_ANOMALY_REGISTER.md)
```

`universe/` and `logs/` per the original spec are represented by `rp001_data/phase2a_acquisition_universe.csv` (repo root) and `research/RP001_LOG.md` respectively — no separate subdirectory was needed since these are single, already-existing files.

## 7. What this does not resolve

Full acquisition establishes that the raw data exists, is complete, and passes every integrity check run against it. It does **not** by itself construct the Daily Investable Universe, merge datasets, or apply the Missingness Policy's coverage gate at the panel level — that is Confirmatory Dataset construction, tracked separately (`research/RP001_PHASE2A_CONFIRMATORY_DATASET.md`, not yet started as of this document).
