# RP-001 Phase 2A: Execution Plan

**Not started. Awaiting Protocol approval.** No full-universe data has been pulled.

## Phase 2A.0 — Pre-execution checklist (before any data pull)
1. Confirm this Protocol (this document + the other 5) is approved as-is.
2. Create `research/RP001_PHASE2A_DEVIATION_LOG.md`, empty, ready to receive entries per `research/RP001_DEVIATION_POLICY.md`.
3. Re-confirm the locked spec items are unambiguous enough to implement without judgment calls (flag anything unclear as a question, not a default assumption, before pulling data).

## Phase 2A.1 — Full-universe construction
4. Pull `TaiwanStockInfo` and `TaiwanStockDelisting` for the complete TWSE+TPEx universe (not a curated subset).
5. Apply exclusion rules from `research/RP001_FULL_UNIVERSE_SPEC.md` (ETF, financial, disposition-stock, liquidity/history thresholds) — log any rule that can't be mechanically implemented as a deviation before proceeding.
6. Build the daily survivorship-bias-free investable universe.

## Phase 2A.2 — Data pull (full universe, full history)
7. Institutional flow, price, valuation data for the full constructed universe.
8. Trading Calendar Gate applied (same methodology as the original study) — full-period scan for contamination dates, same as Milestone 1B-R.

## Phase 2A.3 — Feature construction (locked spec only)
9. F_INST_01, F_INST_05, F_INST_06, F_INST_07 and the seven interaction features, built exactly per `FEATURE_REGISTRY.md` — no redefinition, no new features.
10. Unit tests re-run (same test suite pattern as Milestone 1A) on the full-universe panel.

## Phase 2A.4 — Confirmatory testing (H-C1 through H-C5 only)
11. Run exactly the five pre-registered hypothesis tests, using the pre-committed acceptance criteria. No exploratory sub-cuts beyond what H-C1–H-C5 specify.

## Phase 2A.5 — Reporting
12. Produce `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md` — verdict (Replicated/Partially Replicated/Not Replicated/Inconclusive) for each of the five hypotheses, full deviation log disclosed regardless of materiality, updated RP-001 formal conclusion reflecting what did and didn't replicate.

## Explicitly out of scope for Phase 2A (repeated from your instruction, binding)

No portfolio optimization, no long-short strategy tuning, no Sharpe/drawdown conclusions, no transaction-cost optimization, no new interaction discovery, no new breakpoint search, no re-selection of favorable conditions using the full universe's added data.

## Gate

Each numbered step above is sequential; this plan does not authorize autonomous execution through all steps. Step 4 (the first real data pull) does not begin until you approve this Protocol.
