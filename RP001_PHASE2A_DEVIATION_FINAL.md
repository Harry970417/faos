# RP-001 Phase 2A: Final Deviation Summary

Consolidates all deviations logged during Phase 2A (full detail and reasoning in `RP001_PHASE2A_DEVIATION_LOG.md`, never summarized away). None required pausing execution for approval; none touched F_INST_01's definition, rank normalization, return horizon, or the break interval's boundary dates — the four items whose modification would have triggered the Deviation Policy's Escalation clause.

| ID | Deviation | Escalated? | Impact |
|---|---|---|---|
| D-01 | Disposition-stock (處置股) exclusion via current-snapshot proxy only — no full historical daily archive exists | No | Universe construction only; biases toward over-inclusion (conservative), not fabrication |
| D-02 | Delisted-stock listing dates approximated via first price-observation date | No | Universe construction only, delisted stocks only |
| D-03 | ETF/ETN identification for delisted stocks via stock-code-prefix heuristic | No | Universe construction only |
| D-04 | Dealer/Dealer_self/Dealer_Hedging recurrence — originally escalated, then downgraded once confirmed F_INST_01 does not use Dealer categories at all | Initially yes, then corrected/downgraded | None on F_INST_01/H-C1–H-C5 |
| D-05 | Dealer vs. split-category schema is an ongoing per-stock choice, not a one-time cutover — **69 individually-verified instances across the full acquisition**, zero exceptions to `Foreign_Investor` completeness | No | None — F_INST_01 unaffected in 100% of checked cases |
| D-06/D-07 | Mis-dated institutional rows on specific calendar dates (system-wide, not stock-specific) | No | None — Trading Calendar Gate structurally excludes these regardless of cause |
| D-08 | Market-cap and sector data unavailable at full-universe scale | No | H-C1–H-C4 unaffected; H-C5 proceeds on 5 of 7 interaction features, F_INT_02/F_INT_06 reported Inconclusive |

## Two acquisition-tooling bugs (not spec deviations, disclosed for completeness)

1. **Batch 8:** the Integrity Gate could run over a batch left incomplete by a connectivity outage. Fixed before any downstream use of the affected data; retroactively confirmed not to have corrupted any already-resolved batch.
2. **Batch 9:** a legitimately-empty (HTTP 200, zero rows) API response for TDR-style codes triggered an infinite retry loop. Fixed; 391 resulting duplicate manifest rows cleaned up.

## What was never deviated from

F_INST_01's definition (`Foreign_Investor` net flow, rank-normalized), the return-horizon formula, the break interval's boundary dates (point estimate 2025-09-25), the liquidity-tercile and volatility-regime definitions, the neutralization method (cross-sectional OLS), and the multiple-testing method (Benjamini-Hochberg, α=0.10) — all applied identically to the exploratory-phase specification, unchanged by any full-universe finding, including the several results in `RP001_PHASE2A_CONFIRMATORY_RESULTS.md` that contradict the original study.
