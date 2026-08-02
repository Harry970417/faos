# RP-001 Phase 2A: Reproducibility Report

## Environment

Python 3.14.5, pandas 3.0.3, numpy 2.4.6, scipy 1.17.1. FinMind API v4 (`https://api.finmindtrade.com/api/v4/data`), anonymous access tier, no token.

## Pipeline, in exact execution order

| Step | Script | Output |
|---|---|---|
| 1 | `rp001_batch_acquire.py` × 19 batch invocations (via `rp001_batch_driver.py`) | `rp001_data/phase2a/raw/*.json` (gitignored), `rp001_data/phase2a/manifests/pull_manifest.csv` |
| 2 | `rp001_phase2a_build_panel.py` | `rp001_data/phase2a/processed/rp001_confirmatory_panel_raw.parquet` |
| 3 | `rp001_phase2a_build_features.py` | `rp001_data/phase2a/processed/rp001_confirmatory_features.parquet` |
| 4 | `rp001_phase2a_coverage_and_tests.py` | `rp001_data/phase2a/processed/rp001_confirmatory_dataset_v0.1.parquet`, `rp001_dataset_snapshot.json`, `rp001_stock_coverage.csv` |
| 5 | `rp001_phase2a_confirmatory_tests.py` | `rp001_data/phase2a/processed/rp001_confirmatory_test_results.json` |

Steps 2–5 are deterministic given the same raw data (no random sampling, no seeded stochastic process anywhere in the pipeline — every number in `RP001_PHASE2A_CONFIRMATORY_RESULTS.md` is exactly reproducible by re-running steps 2–5 against the committed raw manifest).

## Hashes

- **Final confirmatory dataset:** SHA-256 `b945702f9e5f203703c1654b6657a24626747c1fd130a9d1070c5d6987917bb6` (5,718,238 rows × 39 cols) — full detail in `rp001_data/phase2a/processed/rp001_dataset_snapshot.json`.
- **Every raw acquisition file:** individually SHA-256-hashed at download time in `rp001_data/phase2a/manifests/pull_manifest.csv` (6,765 unique (dataset, stock_id) pairs, 100% resolved, 0 unresolved failures).

## Git history

19 batch-acquisition commits (`0cfea80` through `9e71799`), plus dataset-construction and results commits, all on top of the Phase 2A.2-R remediation baseline (`2f49dd1`) and the original Phase 2A Protocol Lock (`82bc4a3`). Full log: `git log --oneline 82bc4a3..HEAD`. Raw data (`rp001_data/phase2a/raw/`) and derived parquet files (`rp001_data/phase2a/processed/*.parquet`) are gitignored per instruction (never commit raw or bulky derived data); every manifest, hash, script, log, and report is committed.

## What is NOT reproducible byte-for-byte

Re-running the acquisition batches against the live FinMind API today would pull additional history (new trading days since 2026-08-02) and would not reproduce the exact row counts in this report — the committed raw JSON files (locally present, gitignored) are the actual source of truth for exact reproduction, not a fresh API pull. A spot-check re-pull of a handful of files against a byte-identical hash (the pattern established in Phase 2A.1's pilot) was not repeated at full scale during Phase 2A.2's acquisition itself, consistent with `RP001_PHASE2A_DATA_SNAPSHOT_SPEC.md`'s "spot-check a small random sample, not all files" guidance.

## Known non-determinism sources: none identified

No `np.random`, no seeded sampling, no parallel-execution race condition affecting output ordering (rank computations are per-date-groupby, deterministic given pandas' stable sort). The two acquisition-tooling bugs found and fixed (Batches 8, 9) were investigated and confirmed not to have altered any already-committed batch's data.
