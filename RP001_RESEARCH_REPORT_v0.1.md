# RP-001 Research Report v0.1

**Status: RP-001 Exploratory Factor Research — Complete. RP-001 overall — Open**, pending Phase 2A Confirmatory Validation (Workstream B). This report documents exploratory and robustness-tested findings on a 50-stock characterization sample. Nothing in this report should be read as confirmed — confirmation requires the full-universe, pre-registered validation specified in the Phase 2A protocol, not yet executed.

## Formal Core Conclusion (fixed wording, not to be paraphrased)

> Foreign investor net flow showed conditional predictive power for Taiwan cross-sectional stock returns, concentrated before the identified break interval and among illiquid-to-mid-liquidity stocks. The effect disappeared after the break and was not shown to be causal. None of the seven interaction terms provided genuine incremental information after controlling for their constituent main effects.

## Why this is Exploratory, not yet Confirmatory — stated plainly

The break interval, the volatility-regime condition, and the liquidity condition were all **discovered on the same 50-stock sample** used to test them. This is a legitimate way to generate hypotheses; it is not a legitimate way to confirm them — a break found by searching a dataset and then "confirmed" by testing sub-periods of that same dataset is not independent evidence, even with permutation-corrected significance. This is precisely why Phase 2A exists as a separate, pre-registered, full-universe study rather than simply scaling up the same analysis.

## Findings by evidentiary category

**Exploratory** (hypothesis-generating, this study's primary output): the existence of a foreign-flow signal, its apparent liquidity- and volatility-conditionality, and the interaction-feature program's uniformly negative result.

**Robustness-tested** (survived multiple internal checks on this sample, still not independent confirmation): the structural break survived permutation-corrected unknown-breakpoint testing, ±40-day sensitivity, and two rolling-window smoothings. The seven interaction artifacts survived joint residualization against their own constituents, not just single-variable controls.

**Confirmatory** — none yet. This category is intentionally empty in this report; it is the deliverable of Phase 2A, not this study.

**Conditional findings:** F_INST_01's predictive power, in full: pre-break only, low-volatility-regime only (and not independently of the break), illiquid-to-mid-liquidity only. F_INST_07 retains real incremental information beyond F_INST_05 but its own break is statistically unconfirmed.

**Negative findings:** F_INST_02 (Trust), F_INST_04 (Dealer Hedging), F_INST_09 (change rate) show no evidence of predictive power at any tested horizon. H3 (small-cap concentration) is not supported — the market-cap pattern found was non-monotonic.

**Confirmed artifacts:** F_INST_06 (redundant with F_INST_05). All seven interaction features (F_INT_01–F_INT_07), including three that separately survived FDR correction on raw IC — the clearest demonstration in this study that statistical significance and mechanism validity are different tests.

## What this report does not claim

No portfolio, backtest, Sharpe ratio, drawdown, transaction-cost, or investment-performance conclusion appears anywhere in RP-001 to date. No causal claim is made about foreign flow's information content — every mechanism statement uses "consistent with," never "demonstrates."

Detail: `RP001_METHODS_AND_DATA_v0.1.md`, `RP001_RESULTS_TABLES_v0.1.md`, `RP001_LIMITATIONS_v0.1.md`, `RP001_REPRODUCIBILITY_APPENDIX_v0.1.md`.
