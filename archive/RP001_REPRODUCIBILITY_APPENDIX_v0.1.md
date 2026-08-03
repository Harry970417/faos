# RP-001 Reproducibility Appendix v0.1

## Environment

Python 3.14.5. Global environment: pandas 3.0.3, numpy 2.4.6, scipy 1.17.1, requests 2.34.2 (missing statsmodels). Recommended venv for statsmodels-dependent work: `taiwan-attention-signal/venv` (statsmodels 0.14.6, pandas 3.0.3, numpy 2.5.0, scipy 1.18.0). `ruptures` unavailable — no C++ build toolchain in this environment.

## Git Commit History (`Desktop/faos`, branch `master`)

| Commit | Milestone |
|---|---|
| 05ccedc | Initial commit — Alpha 0.2 baseline |
| e5491ea | Phase 0: Milestones 0A/0B/0C |
| 881c306 | Milestone 1A: Feature Construction |
| e9ae840 | Milestone 1B: Feature Validation |
| 9e57dfa | Milestone 1B-R: Data Integrity Remediation |
| 7bb90e8 | Milestone 1B-R decision log |
| c2b5bfc | Milestone 1C: Feature Diagnostics |
| b76eee5 | Milestone 1C+: Mechanism Analysis |
| 47fd687 | Milestone 1C-R: Robustness and Confirmation |
| fa522aa | Milestone 1D: Feature Freeze Review |

## Data Snapshots

- `research/RP001_DATA_SNAPSHOT.json` — Milestone 0B, characterization sample manifest, 50 raw institutional files SHA-256 hashed in `rp001_data/raw_manifest.json`
- Price data: `rp001_data/raw_price/price_{stock_id}.csv`
- Valuation (PBR/PER): `rp001_data/raw_valuation/val_{stock_id}.csv`
- Delisting reference (available, not yet joined at this sample scale): `TaiwanStockDelisting`, 337 rows, confirmed live 2026-07 session

## Feature Panels

`rp001_data/features/rp001_features_v0.1.parquet` (pre-remediation), `v0.2.parquet` (post Trading Calendar Gate), `rp001_features_1c_plus.parquet` (extended with sector/mcap/volatility/PBR/regime/interaction columns for mechanism analysis).

## Key Scripts (all committed, re-runnable)

`research/rp001_pull_characterization_sample.py`, `research/rp001_pull_price.py`, `research/rp001_pull_valuation.py`, `research/rp001_build_features.py` / `_v2.py`, `research/rp001_feature_tests.py`, `research/rp001_data_integrity_remediation.py`, `research/rp001_milestone_1c.py` / `_part2.py` / `_part3.py`, `research/rp001_1c_plus_setup.py` / `_analysis.py`, `research/rp001_breakpoint_analysis.py`, `research/rp001_regime_robustness.py`, `research/rp001_interaction_incremental.py`, `research/rp001_multiple_testing.py`.

## Regression Tests

`research/rp001_regression_test_20260619.py` — permanent guard against the 2026-06-19 non-trading-day contamination re-entering any future feature build.

## Full Decision Trail

`research/RP001_LOG.md` — every Research Decision from Milestone 0A through 1D, Decision/Reason/Evidence/Impact format, no entries removed or edited after the fact.
