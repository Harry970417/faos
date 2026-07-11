# RP-001 Phase 2A: Data Snapshot Architecture Spec

**Status: Specification only. No full-universe bulk download begins until the Readiness Gate (`RP001_PHASE2A_READINESS_GATE.md`) passes.** This document defines the directory layout and manifest schema for Phase 2A.2's data pull; it does not execute it. The pilot (`RP001_PHASE2A_DATA_QUALITY_PILOT.md`) already exercises this pattern at small scale under `rp001_data/pilot/` — this spec formalizes and extends it to full-universe scope.

## Directory layout

```
rp001_data/phase2a/
  raw/                  # untouched API responses, one file per (dataset, stock_id) pull
  processed/            # cleaned/joined panels derived from raw/ (post date-alignment, missing-state classification)
  manifests/            # one manifest row per raw file pulled (see schema below)
  universe/             # constructed daily investable universe (per-date stock membership)
  anomalies/            # flagged data issues found during construction (date-alignment gaps, pre-listing data, disposition edge cases)
  logs/                 # execution logs (start/end time, error traces, retry history)
```

`raw/` is never edited after write — any correction happens by re-pulling and re-manifesting, not by modifying a raw file in place, preserving the audit trail.

## Manifest schema (one row per raw file, `manifests/pull_manifest.csv`)

| Field | Description |
|---|---|
| `dataset` | e.g. `TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice` |
| `stock_id` | queried stock code |
| `query_start_date` / `query_end_date` | exact parameters sent to the API |
| `download_timestamp` | UTC timestamp of the request |
| `row_count` | rows returned |
| `sha256` | hash of the raw response body as written to disk |
| `source_endpoint` | full URL/base used (FinMind `v4/data`, TWSE `openapi.twse.com.tw`, TPEx `www.tpex.org.tw/openapi`) |
| `retry_count` | number of retries before success (0 if first attempt succeeded) |
| `status` | `success` / `failed` / `partial` (partial reserved for datasets returning fewer rows than expected without an explicit error) |
| `file_path` | relative path under `raw/` |

This is a direct extension of the pattern already used and proven in the pilot (`pilot_pull_log.csv` — same fields: query params, row count, elapsed time, retries, SHA-256, file size), scaled from 14 rows to the full-universe request count estimated in `RP001_PHASE2A_CAPACITY_ESTIMATE.md`.

## `anomalies/` — what gets logged there

Not a catch-all; three specific, already-identified categories from this audit, each with its own file so Phase 2A.2 doesn't have to rediscover them:

1. `date_alignment_gaps.csv` — per-stock count and list of dates present in one dataset (price or institutional) but not the other, following the pattern found in the pilot (1101: 4 residual post-floor gaps each direction).
2. `pre_listing_data_flags.csv` — per-stock flag where "first date with data" differs materially from "official listing_date" (the 6986-type hazard documented in `RP001_DAILY_UNIVERSE_VALIDATION.md`), so universe construction can be checked against this list rather than trusting the join silently.
3. `disposition_coverage_notes.csv` — running log of which stocks/dates Deviation D-01's proxy approach could and could not verify, so the deviation's practical impact is auditable after the fact, not just asserted in the log.

## Reproducibility

Two-part requirement, both already demonstrated at pilot scale: (1) SHA-256 of every raw file recorded at write time; (2) re-pulling the same (dataset, stock_id, date range) produces a byte-identical file — verified once in the pilot (1101 institutional data, identical hash on re-pull). Full-universe execution should spot-check a small random sample (not all files) for hash-reproducibility after the bulk pull completes, as a cheap integrity check against silent API-side data changes between pulls.

## What this spec does not authorize

Creating these directories and beginning the bulk pull is Phase 2A.2, step 4 in `RP001_PHASE2A_EXECUTION_PLAN.md` — gated on Protocol approval (already given) and this Readiness Gate (`RP001_PHASE2A_READINESS_GATE.md`) passing. This document is the blueprint, not the trigger.
