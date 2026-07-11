# RP-001 Research Findings v0.1

Consolidated from Milestones 0A through 1D. Institutional flow research on a 50-stock TWSE/TPEx characterization sample, 2024-07-01 to 2026-07-09. No investment performance claims anywhere in this document.

## Robust Findings

1. **Foreign institutional net flow (F_INST_01) has real, if conditional, predictive power for 2-to-5-day-ahead cross-sectional stock returns**, surviving multiple-testing correction across several independent tests (yearly stability, volatility-regime split, plain feature×horizon IC, permutation-corrected structural break).
2. **A structural break in that predictive power exists**, confirmed via a properly-corrected unknown-breakpoint test (not a single post-hoc date), located in a break interval of roughly late-August to late-October 2025, robust to ±40-day sensitivity and to two independent rolling-window smoothings.
3. **All seven tested Foreign/Aggregate-interaction features (momentum, size, liquidity, volatility — in both aggregate-based and foreign-based forms) are Confirmed Artifacts** — impressive raw IC fully explained by their constituent main effects once jointly residualized. This is itself a robust, well-evidenced finding, not an absence of results.
4. **The illiquid > liquid asymmetry in F_INST_01's signal survives market-cap and sector neutralization.**

## Conditional Findings

1. F_INST_01's predictive power is conditional on: pre-break period, low-volatility regime, and illiquid-to-mid-liquidity names — and these conditions are **not independent of each other** (the low-vol effect itself is conditional on the pre-break regime, per the Milestone 1C-R double-sort).
2. F_INST_07 (flow-to-volume) retains real incremental information beyond F_INST_05, but its own structural break is unconfirmed — its status is conditional on a test not yet run.

## Exploratory Findings

1. IC strengthens with return horizon (t+1 weak, t+5 strongest) rather than decaying — more consistent with gradual price discovery than immediate price-pressure reversal, but based on cumulative-window returns, not marginal daily decay, and not confirmed with a dedicated horizon-decomposition test.
2. Non-monotonic patterns by market-cap tercile and value/growth (PBR) tercile — strongest in the middle, not the extremes — real in this sample, unexplained, not investigated further.
3. The volatility-regime effect replicates under most but not all tested definitions of volatility (weakens under raw daily cross-sectional dispersion with a tercile split).
4. F_INST_05_foreign_x_volatility's residual IC is consistently negative rather than merely null across every cut tested — suggestive of something systematic, not concluded.

## Rejected Hypotheses

1. **H0 (no predictive power) is rejected for F_INST_01**, but only within the conditions above — it is not rejected unconditionally.
2. **F_INST_02 (Trust), F_INST_04 (Dealer Hedging), and F_INST_09 (change rate) show no evidence of predictive power at any horizon tested** — H0 is not rejected for these.
3. **H3 (stronger effect in smaller-cap names) is not supported** — the market-cap pattern found was non-monotonic (strongest in Mid-cap), not a clean small-cap effect.
4. **The "genuine interaction" hypothesis is rejected for all seven tested interaction terms** — none carry incremental information beyond their additive components.

## Confirmed Artifacts

F_INST_06 (redundant with F_INST_05). F_INT_01, F_INT_02, F_INT_03, F_INT_04, F_INT_05, F_INT_06, F_INT_07 (all seven interaction features, confirmed via joint residualization against their own constituent main effects). Three of these (F_INT_01, F_INT_03, F_INT_07) separately survived Benjamini-Hochberg FDR correction on raw IC — documented proof that statistical significance and mechanism validity are not the same test and can disagree.

## Limitations

- **Sample is a 50-stock characterization panel** (taiwan-attention-signal's existing large-cap-weighted list), not RP-001's full designed research universe (TWSE/TPEx, survivorship-bias-free) specified in `RP001_RESEARCH_DESIGN.md`. All findings above are scoped to this sample and require re-verification at full-universe scale before being treated as final.
- **Sample period is 2 years**, containing exactly one detected structural break — a sample with a different period boundary could show a different break location or none at all.
- FinMind's free-tier institutional data reports shares, not NT$ value; value-denominated features are share-count proxies.
- No causal identification design was used anywhere — every "consistent with" finding is observational, not causal, and is worded accordingly throughout this project's documents.
- Sector coverage in this sample is concentrated in a small number of industries; sector-cut findings are based on 2 well-populated sectors, not a broad cross-sector test.
- No investment performance, transaction cost, or tradeability claim has been made or tested anywhere in RP-001 to date.
