# RP-001 Executive Summary v0.2

**One-paragraph answer:** RP-001 asked whether foreign institutional net flow predicts short-horizon Taiwan stock returns. An exploratory study on 50 large-cap stocks (2024–2026) found a conditional "yes" — positive, pre-break, illiquid-and-calm-market-only. A confirmatory study on the full TWSE+TPEx universe (2,255 stocks, 2012–2026, independently constructed) found the core effect **does not replicate**: pre-break predictive power is statistically indistinguishable from zero at every horizon tested. One secondary hypothesis (liquidity conditionality) partially replicates. A separate, unexpected finding emerged: interaction features previously dismissed as statistical artifacts show small but robust residual signal at full-universe scale.

## Verdict scorecard

| # | Hypothesis | Verdict |
|---|---|---|
| H-C1 | Pre-break positive IC | Not Replicated |
| H-C2 | Post-break null | Replicated (weak — see caveat) |
| H-C3 | Liquidity conditionality | Partially Replicated |
| H-C4 | Volatility break-conditionality | Not Replicated |
| H-C5 | No genuine interactions | Not Replicated (new positive finding) |

## Scale of this confirmation

- **Exploratory sample:** 50 stocks, ~2 years, 491 trading days
- **Confirmatory sample:** 1,462 stocks (coverage-gate-passing), ~14 years, 3,283 pre-break trading days — roughly **30× the stocks, 7× the calendar history**
- **Full raw acquisition underlying this:** 2,255 stocks, 6,765 API requests, 34.2M rows, 100% coverage, zero unresolved acquisition failures

## Why this matters more than "the factor didn't work"

This is the intended, designed outcome of a confirmatory-validation research program, not a failure of execution. The exploratory phase's own governance (`research/RP001_PHASE2A_CONFIRMATORY_PROTOCOL.md`) explicitly anticipated that a finding discovered and tested on the same sample might not survive independent testing — that is precisely why Phase 2A was built as a separate, pre-registered workstream rather than skipped. A research program that only ever reports confirmations is one that never runs a real confirmatory test.

## What is now known with more confidence than before

1. Foreign flow's predictive relationship, if it exists at all, is **not a stable, universe-wide, multi-year phenomenon** — it does not survive the jump from 50 hand-picked large caps to the full market.
2. The interaction-feature program's original "all seven are artifacts" conclusion was **too strong** — four of the seven (the five testable ones minus one borderline case) carry a small, statistically real residual effect once the dataset is large enough to detect it. This does not make them tradeable or economically important; it means "collapses to exactly zero" was the wrong characterization.

## What has not changed

The break interval, F_INST_01's definition, the return-horizon construction, the liquidity/volatility group definitions, and the statistical methods (Newey-West, BH-FDR) are identical to the locked exploratory-phase specification throughout. No result influenced any methodological choice.

Full detail: `archive/RP001_RESEARCH_REPORT_v0.2.md`, `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`.
