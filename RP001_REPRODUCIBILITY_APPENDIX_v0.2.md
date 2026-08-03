# RP-001 Reproducibility Appendix v0.2

Extends `RP001_REPRODUCIBILITY_APPENDIX_v0.1.md` (exploratory-phase, preserved unchanged) with Phase 2A. Full detail: `RP001_PHASE2A_REPRODUCIBILITY_REPORT.md` — this document is a pointer/summary, not a duplicate.

## Full-universe pipeline reproducibility

Every number in `RP001_PHASE2A_CONFIRMATORY_RESULTS.md` is deterministically reproducible from the committed raw data (`rp001_data/phase2a/raw/`, gitignored but locally present and SHA-256-hashed in `pull_manifest.csv`) by re-running, in order: `rp001_phase2a_build_panel.py` → `rp001_phase2a_build_features.py` → `rp001_phase2a_coverage_and_tests.py` → `rp001_phase2a_confirmatory_tests.py`. No random seed, no stochastic sampling anywhere in this pipeline.

## Dataset hash

Final confirmatory dataset SHA-256: `b945702f9e5f203703c1654b6657a24626747c1fd130a9d1070c5d6987917bb6` (5,718,238 rows × 39 columns). Recorded at build time in `rp001_data/phase2a/processed/rp001_dataset_snapshot.json`.

## Acquisition reproducibility

All 6,765 raw API responses individually SHA-256-hashed at download time (`rp001_data/phase2a/manifests/pull_manifest.csv`). 100% resolved (0 unresolved failures, 0 orphaned pairs). Batch-by-batch Integrity Gate audit trail: `RP001_PHASE2A_BATCH_TRACKER.md` (19 batches, each with a resolution section documenting every anomaly investigated).

## Test suite

21/21 unit and leakage-truncation tests pass on the confirmatory dataset (`RP001_PHASE2A_DATA_TEST_REPORT.md`) — rank bounds, F_INST_05 mathematical correctness, explicit-zero preservation, no forward-return leakage, no cross-date rank leakage, D-08 columns confirmed all-NaN.

## Environment

Python 3.14.5, pandas 3.0.3, numpy 2.4.6, scipy 1.17.1.

## Git commits (Phase 2A, chronological)

19 batch-acquisition commits (`0cfea80`–`9e71799`), the Integrity Gate summary (`8308400`), the D-08 deviation log (`25d8d4d`), the Confirmatory Dataset build (`87b0808`), and the H-C1–H-C5 results (`9228b98`) — all descend from the Protocol Lock commit `82bc4a3`. Full log: `git log --oneline 82bc4a3..HEAD`.
