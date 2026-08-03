# RP-001 Changelog v0.2

Covers this session's work: resuming Phase 2A.2 from Batch 7 through full completion, Confirmatory Dataset construction, and H-C1–H-C5 execution.

## Data acquisition (Phase 2A.2)

- Resumed and completed Batches 7–19 of full-universe acquisition (2,255 stocks, 6,765 requests, 34.2M rows, 100% coverage).
- Found and fixed 2 real acquisition-tooling bugs: an Integrity Gate that could run on an incomplete batch after a connectivity outage (Batch 8), and an infinite retry loop on legitimately-empty API responses (Batch 9).
- 69 individually-verified instances of the Dealer-schema recurrence pattern (D-05), 100% clean (F_INST_01 unaffected) across the entire acquisition.
- First TPEx-majority batch (10) closed a previously-open Decision Gate item on TPEx eligibility-gate behavior.
- Logged Deviation D-08: market-cap/sector data unavailable at full-universe scale, before writing any dataset-construction code.

## Confirmatory Dataset (Phase 2A.3)

- Built the full-universe Daily Investable Universe panel (5,718,238 eligible rows), applied the Trading Calendar Gate and Missingness Policy (never-impute, 80% coverage gate: 1,462/2,096 stocks pass).
- Constructed F_INST_01/F_INST_05/F_INST_07 and 5 of 7 interaction features per locked definitions (F_INT_02/F_INT_06 not constructible, D-08).
- 21/21 unit and leakage-truncation tests pass. Dataset SHA-256 hashed for reproducibility.

## Confirmatory Results (Phase 2A.4)

- Ran all five pre-registered hypotheses (H-C1–H-C5) on the full-universe confirmatory sample.
- **Verdicts: H-C1 Not Replicated, H-C2 Replicated (weak), H-C3 Partially Replicated, H-C4 Not Replicated, H-C5 Not Replicated.**
- RP-001's formal core conclusion updated (v0.2) to reflect that F_INST_01's central exploratory finding does not survive full-universe confirmatory validation, while noting a new, unexpected finding: 4 of 5 testable interaction features show small but statistically robust residual signal, contradicting the exploratory "all artifacts" conclusion.

## Documents added or updated this session

New: `RP001_PHASE2A_API_AND_SOURCE_FEASIBILITY` chain continuation, `research/RP001_PHASE2A_FINAL_DATASET.md`, `research/RP001_PHASE2A_DATA_MANIFEST.json`, `research/RP001_PHASE2A_CONFIRMATORY_DATASET.md`, `research/RP001_PHASE2A_FEATURE_REGISTRY.md`, `research/RP001_PHASE2A_DATA_TEST_REPORT.md`, `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`, `research/RP001_PHASE2A_DEVIATION_FINAL.md`, `research/RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`, and this v0.2 report set (`archive/RP001_RESEARCH_REPORT_v0.2.md`, `research/RP001_EXECUTIVE_SUMMARY_v0.2.md`, `research/RP001_METHODS_AND_DATA_v0.2.md`, `research/RP001_RESULTS_TABLES_v0.2.md`, `research/RP001_LIMITATIONS_v0.2.md`, `research/RP001_REPRODUCIBILITY_APPENDIX_v0.2.md`, `research/RP001_FAOS_TRACE_v0.2.md`).

Updated (append-only, originals preserved): `research/RP001_PHASE2A_BATCH_TRACKER.md`, `research/RP001_PHASE2A_DEVIATION_LOG.md`, `research/RP001_LOG.md`, `research/RP001_MARKET_MEMBERSHIP_AUDIT.md` (correction note added, §6).

## What was NOT changed

F_INST_01's definition, rank normalization, return horizon construction, the break interval's boundary dates, liquidity/volatility group definitions, and the statistical methods (Newey-West, BH-FDR) — identical throughout, unchanged by any result, favorable or unfavorable.
