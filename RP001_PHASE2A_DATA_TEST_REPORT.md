# RP-001 Phase 2A: Confirmatory Dataset Test Report

**Date:** 2026-08-03. Full detail (machine-readable): `rp001_data/phase2a/processed/rp001_dataset_snapshot.json`. Test code: `rp001_phase2a_coverage_and_tests.py`.

## Result: 21/21 checks passed

| Category | Checks | Result |
|---|---|---|
| Coverage gate correctness | Stock 1213 (known AR-03 sparse case) excluded | PASS — coverage_rate 0.346, well below 0.80 threshold |
| Rank bounds | F_INST_01_foreign_rank, F_INST_05_aggregate_rank ∈ [0,1] | PASS both |
| Interaction feature integrity | No infinite values; product-of-ranks bounds [0,1] — F_INT_01, F_INT_03, F_INT_04, F_INT_05, F_INT_07 | PASS all 5 |
| D-08 deviation correctness | F_INT_02, F_INT_06 are all-NaN (not silently zero or fabricated) | PASS both |
| F_INST_05 mathematical correctness | Recomputed sum of the 6 raw categories matches stored F_INST_05, max deviation | PASS — max_diff = 0.0 |
| Explicit-zero preservation | `buy=0, sell=0` days remain F_INST_01=0, not converted to NaN | PASS — 180,445 such rows confirmed |
| Break-period split correctness | pre-break rows all `date < 2025-09-25`; post-break rows all `date >= 2025-09-25` | PASS |
| Forward-return leakage | Each stock's last eligible date has NaN `fwd_ret_t5` (no data invented past series end) | PASS — 100.0% |
| Forward-return leakage (spot-check) | Increasing NaN density near series end for a sample stock, no wraparound to another stock's data | PASS |
| Rank leakage | Daily rank computed strictly within-day, no cross-date contamination | PASS |

## What these tests do and do not establish

They confirm the dataset is **internally consistent and free of the specific leakage/construction defects checked** — not that the confirmatory hypotheses will replicate. No IC, t-stat, or hypothesis test is computed in this report; that is Phase 2A.4 (`RP001_PHASE2A_CONFIRMATORY_RESULTS.md`).

## Known, disclosed limitations (not test failures)

- Coverage gate passes 69.8% of stocks with any panel presence (1,462/2,096) — lower than the 80%+ that might have been hoped, reported as-is, not adjusted after seeing the number (Missingness Policy Rule 3 threshold was fixed before this computation).
- `liq_tercile` and `market_vol_regime` have small NaN pockets (18,864 and 13,376 rows respectively) on dates/cells with too few eligible stocks (<15) to form a reliable tercile or where the rolling volatility window hadn't yet filled — excluded from the relevant hypothesis tests on those specific rows, not imputed.
