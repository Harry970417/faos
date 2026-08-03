# RP-001 Milestone 0C: Feature Specification

Formal definitions only. No IC, backtest, or portfolio construction performed — every number in this document comes from Milestone 0A's characterization (real, already computed), not from testing these features against returns.

## Revisions from the original Research Design, driven by Milestone 0A evidence

1. **Foreign_Dealer_Self dropped as a standalone factor.** 99.99% zero-rate across 122,920 real observations — no variance, no signal, breaks standardization. Still included in aggregate sums (contributes ~0, harmless there) but not defined as its own feature.
2. **自營商買賣超 split into two features, not one.** Dealer_self (proprietary, near-always active) and Dealer_Hedging (near-always active but mechanically driven by options/warrant hedging) are structurally different — collapsing them into one "dealer" number would mix a directional signal with a mechanical one.
3. **Rank-based standardization is now the primary method, not a robustness variant.** Every category shows severe mean/median divergence and fat tails (Milestone 0A). Raw z-scores would be dominated by extreme days; percentile rank is specified as primary, z-score kept only as a comparison variant in Robustness.

## Feature Definitions

| ID | Name | Formula (informal) | Standardization | Source category |
|---|---|---|---|---|
| F-INST-01 | Foreign net flow | Foreign_Investor: buy − sell (shares) | Rank (primary), z-score (robustness) | Foreign_Investor |
| F-INST-02 | Trust net flow | Investment_Trust: buy − sell | Rank / z-score | Investment_Trust |
| F-INST-03 | Dealer proprietary net flow | Dealer_self: buy − sell | Rank / z-score | Dealer_self |
| F-INST-04 | Dealer hedging net flow | Dealer_Hedging: buy − sell | Rank / z-score | Dealer_Hedging |
| F-INST-05 | Aggregate institutional net flow | Sum of all 5 categories (Foreign_Dealer_Self included in sum, negligible) | Rank / z-score | All |
| F-INST-06 | Value-proxy net flow | Net shares × same-day close price (**proxy, not true NT$ — FinMind free tier limitation, must be labeled in every output**) | Rank | Any of F-INST-01–05 |
| F-INST-07 | Flow-to-volume ratio | Net shares / total daily traded volume | Already bounded, no further standardization needed | Any of F-INST-01–05 |
| F-INST-08 | Consecutive same-direction days | Count of consecutive days with same-sign net flow | Raw count + separate z-score | Any of F-INST-01–05 |
| F-INST-09 | Flow change rate | (Net flow − N-day rolling mean) / N-day rolling mean | Rank | Any of F-INST-01–05 |
| F-INT-01 | Flow × Momentum interaction | F-INST-05 × FA03/FA04 (existing KB Momentum Factor) | Product of two rank-standardized inputs | F-INST-05, FA03/FA04 |
| F-INT-02 | Flow × Size interaction | F-INST-05 × market cap rank | Same | F-INST-05, market cap |
| F-INT-03 | Flow × Liquidity interaction | F-INST-05 × ADV rank | Same | F-INST-05, avg. daily volume |

11 features total: 4 single-category (F-INST-01–04), 5 derived/transformed (F-INST-05–09), 3 interaction (F-INT-01–03) — down from the original design's implicit 9-ish undifferentiated candidates, now precisely specified against real category structure rather than an assumed 3-way split.

## What is explicitly deferred to Phase 1

Rolling window length N for F-INST-08/09 (needs Train-period calibration, not a design-time constant), exact interaction-term functional form beyond simple products (e.g., whether a nonlinear or quantile-interaction form outperforms), any IC/ICIR computation, any portfolio construction. None of this is computed here.

## ECC status of these features

None of these are yet Knowledge Objects in the KB — consistent with Research Production Finding #1 (RP001_FAOS_TRACE.md). Formal object creation, with proper depends-on/references relationships and Evidence grounding (from RP001_EVIDENCE_MAP.md's pre-positioned citations), is a Phase 1 task, not done at this milestone.
