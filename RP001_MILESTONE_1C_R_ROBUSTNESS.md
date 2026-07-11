# RP-001 Milestone 1C-R: Robustness and Confirmation — Executive Summary

Detail in `RP001_BREAKPOINT_ANALYSIS.md`, `RP001_REGIME_ROBUSTNESS.md`, `RP001_INTERACTION_INCREMENTAL_TESTS.md`, `RP001_MULTIPLE_TESTING_REGISTER.md`. This file synthesizes them into the classification you asked for. No Portfolio Construction, Backtest, Sharpe, Max Drawdown, trading strategy design, or Feature Freeze performed.

## What changed from Milestone 1C+'s framing

1C+ presented the structural break, the low-volatility effect, and the liquidity effect as three separate findings. This milestone's double-sorts show they are **not independent**: the break is the dominant fact, and both the volatility-regime effect and (to a lesser extent) the liquidity effect are conditional on being in the pre-break era — the "low-vol effect," tested in isolation post-break, collapses to zero. The corrected picture is one mechanism with a time boundary, not three separate mechanisms.

## A. Robust Findings

- **A structural break exists in F_INST_01's predictive power, dated to a break interval of roughly late-August to late-October 2025** (sup-Wald point estimate 2025-09-25). Survives permutation-corrected unknown-breakpoint testing (p=0.0105, properly accounting for searching across all candidate dates), ±40-day sensitivity (significant at 3 of 5 tested offsets), and two independent rolling-window smoothings (40d and 90d, both show the identical shape).
- **The illiquid > liquid asymmetry in F_INST_01's predictive power** survives market-cap neutralization (essentially unchanged) and sector-neutralization (strengthens for the Illiquid bucket specifically). Correct wording: **consistent with slower price discovery in illiquid names, not demonstrated** — no causal design was used.
- **None of the four tested Foreign-interaction features (Liquidity, Volatility, Size, Momentum) carry genuine incremental information beyond their additive components.** This is now confirmed for all four via residualization against both constituents jointly, not assumed by extension.

## B. Exploratory Findings — real, but not yet confirmed to the same standard

- The volatility-regime effect (low-vol IC 0.047 vs. high-vol 0.005) replicates across most operationalizations tested (market vol at two windows, smoothed cross-sectional dispersion) but **weakens materially under raw daily cross-sectional dispersion with a tercile split**, where the "high" regime also becomes significant. Real, but not uniform across every reasonable definition.
- The double-sort finding that the volatility effect is conditional on the pre-break regime, not independent of it, is well-supported by this milestone's data but is a single characterization-sample result — worth treating as a working hypothesis for the next phase, not a settled fact.
- Non-monotonic patterns by market-cap and value/growth tercile (strongest in the middle, not the extremes) remain unexplained — flagged in 1C+, not resolved here, still exploratory.
- F_INST_05_foreign_x_volatility's consistently negative (not just null) residual IC across every cut tested is suggestive of something systematic rather than pure noise, but wasn't investigated further this round — exploratory, not concluded.

## C. Confirmed Artifacts

- **F_INT_04 (Foreign × Liquidity)** — residual IC −0.005, indistinguishable from zero, confirmed in Milestone 1C+ and restated here.
- **F_INT_06 (Foreign × Size)** — residual IC collapses cleanly to near-zero (−0.002 to −0.004) across every horizon, break period, and sector-neutral cut tested. Unambiguous.
- **F_INT_07 / F_INT_01 (Foreign × Momentum)** — the strongest-looking raw interaction in the entire study, confirmed via residualization to be an additive artifact that even sign-flips after the structural break. Its Experimental status (set by your prior instruction) is now directly evidenced, not just cautious labeling.
- **F_INT_03 (Foreign × Liquidity, the 1C-vintage feature)** — statistically survives FDR correction on raw IC, but independently confirmed an artifact via sector-neutralization (75% of its IC explained away). The multiple-testing register documents this disagreement explicitly — passing FDR is not sufficient on its own.

## D. Recommended for Milestone 1D Freeze Review

**F_INST_01_foreign — as a conditional, not unconditional, candidate.** Any Freeze decision must carry these conditions explicitly attached, not summarized away:
- Valid pre-break era only (roughly through Aug–Oct 2025); no evidence it currently predicts anything.
- Strongest in low-volatility, pre-break conditions specifically — the two are intertwined, not separately additive.
- Strongest in illiquid/mid-liquidity names; weak in liquid, large-cap names.
- Survives FDR correction across multiple independent tests (yearly stability, regime split, plain feature×horizon, structural break) — this is the one feature in the entire study with that level of corroboration.

**F_INST_07_flow_to_volume — hold at Secondary Conditional, not yet 1D-ready.** Its own structural break is not independently statistically confirmed (permutation p=0.171) despite the suggestive date overlap with F_INST_01. Needs its own dedicated test before advancing.

**Everything else retains its Milestone 1C-R interim status** (F_INST_06 Deprecated; F_INST_02/04/09 Rejected; F_INT_02/03 Artifact/Redesign Required; F_INT_05/06 now resolved to Inconclusive-leaning-artifact / Confirmed Artifact respectively, no longer "pending"; F_INT_01 Experimental, now with direct supporting evidence).

Not proposing Freeze. Waiting on your review.
