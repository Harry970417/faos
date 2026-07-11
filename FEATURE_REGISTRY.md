# RP-001 Feature Registry

Governs all 11 features from RP001_FEATURE_SPECIFICATION.md. Built and tested on the 50-stock characterization sample (24,535 panel rows, 2024-07-01 to 2026-07-09) — **not yet the full RP-001 research universe**, which is a separate, later data-engineering task. No IC, backtest, or portfolio construction performed against these features at this milestone.

**Version: v0.1** | **Build date:** recorded per-row in the feature file itself | **Source code:** `rp001_build_features.py` | **Test suite:** `rp001_feature_tests.py`, 15/15 passed | **Output:** `rp001_data/features/rp001_features_v0.1.{parquet,csv}`

## Registry

| Feature ID | Definition | Calculation | Missing Handling | Normalization | Unit Test |
|---|---|---|---|---|---|
| F_INST_01_foreign | Foreign_Investor net flow (shares) | `buy − sell`, Foreign_Investor category only | Panel gaps → 0 (legitimate no-flow, not unknown) | Rank (primary), `_rank` suffix column | Rank bounds [0,1] ✓ |
| F_INST_02_trust | Investment_Trust net flow | Same, Investment_Trust category | Same | Rank | Rank bounds ✓ |
| F_INST_03_dealer_self | Dealer proprietary net flow | Same, Dealer_self category | Same | Rank | Rank bounds ✓ |
| F_INST_04_dealer_hedge | Dealer hedging net flow | Same, Dealer_Hedging category | Same | Rank | Rank bounds ✓ |
| F_INST_05_aggregate | Sum across all 5 raw categories (Foreign_Dealer_Self included in the sum, not as its own feature — see Milestone 0C) | Row-wise sum | Same | Rank | **Verified equals true sum of all 5 raw categories, max diff = 0** |
| F_INST_06_value_proxy | Net shares × same-day close — **share-count proxy, not true NT$** (FinMind free-tier limitation) | `F_INST_05 × close` | Inherits F_INST_05's handling | Rank | Rank bounds ✓ |
| F_INST_07_flow_to_volume | Net flow ÷ total daily volume | `F_INST_05 / volume` | Division-by-zero guarded (volume=0 → NaN, not error) | Already bounded, no further normalization | 100% of observations within [−1.5, 1.5]; observed range [−0.83, 1.08] |
| F_INST_08_streak | Consecutive same-direction days, signed | Run-length encode on sign of F_INST_05 | N/A (derived from already-handled input) | Raw signed count (no rank — ordinal by construction) | **Verified sign always matches underlying flow sign, 0 mismatches** |
| F_INST_09_change_rate | (Flow − 20d rolling mean) / |20d rolling mean| | Pandas rolling, min_periods=10 | First 10 obs per stock are NaN by construction (rolling window not yet full) — not imputed, left NaN | Rank | Rank bounds ✓ |
| F_INT_01_flow_x_momentum | Rank(F_INST_05) × Rank(20d price return) | Product of two percentile ranks | Inherits component handling | Already a product of ranks | Included in "no infinite values" check |
| F_INT_02_flow_x_size | Rank(F_INST_05) × Rank(market cap) | Market cap = shares outstanding (TWSE OpenAPI) × close | 0% missing — all 50 stocks matched shares-outstanding data | Product of ranks | Included in infinite-values check |
| F_INT_03_flow_x_liquidity | Rank(F_INST_05) × Rank(20d avg trading value) | Rolling 20d mean of Trading_money | Same rolling-window NaN policy as F_INST_09 | Product of ranks | Included in infinite-values check |

## What's explicitly NOT in this registry

**Foreign_Dealer_Self does not have its own registry entry** — per Milestone 0C's evidence-driven decision (99.99% zero-rate, degenerate). It's summed into F_INST_05 (contributes ~0, harmless) but never standalone. Verified by unit test: no column name contains it as an individual feature.

## Test suite summary

15/15 checks passed, including two that would have caught real construction bugs if present: F_INST_05 mathematically verified against the raw category sum (not just eyeballed), and F_INST_08's streak sign cross-checked against the underlying flow sign for every row.

## Full-universe scale-up — explicitly deferred

This registry and its build reflect the 50-stock characterization sample. Extending to RP-001's actual research universe (full TWSE/TPEx, survivorship-bias-free, per RP001_RESEARCH_DESIGN.md) requires the delisted-stock integration and full-universe pull that Milestone 0A confirmed is *available* (`TaiwanStockDelisting`, 337 rows) but not yet *executed*. That's a Milestone 1A follow-up, not done here.

## Feature Status — FROZEN as of Milestone 1D (Feature Freeze Review)

Freeze does not mean permanently valid, tradeable, deployable, or performance-validated — it means the research determination below is stable under current sample/methods/robustness tests and will not change by design preference alone; only new evidence can revise it. Full basis in `RP001_MILESTONE_1D_FEATURE_FREEZE_REVIEW.md` and `RP001_FEATURE_DECISION_TABLE.md`.

| Feature | Frozen Status | Basis |
|---|---|---|
| F_INST_01_foreign | **Frozen — Conditional** (the only Research-Grade-tier result in the study) | See mandatory conditions below |
| F_INST_07_flow_to_volume | **Secondary Candidate** | Retains incremental info beyond F_INST_05, but own structural break not permutation-confirmed (p=0.171) — proximity to F_INST_01's break date is not treated as independent confirmation |
| F_INST_02_trust | **Rejected** | No evidence of predictive power at any horizon tested |
| F_INST_03_dealer_self | **Inconclusive** | Marginal, only significant at t+5, not further tested |
| F_INST_04_dealer_hedge | **Rejected** | No evidence of predictive power at any horizon tested |
| F_INST_05_aggregate | **Deprecated** | Dilutes F_INST_01's real signal by summing in non-informative categories |
| F_INST_06_value_proxy | **Deprecated** | Confirmed redundant with F_INST_05 (residual IC ≈ 0.002) |
| F_INST_08_streak | **Inconclusive** | Weak, marginal only at t+5, not further tested |
| F_INST_09_change_rate | **Rejected** | No evidence of predictive power at any horizon tested |
| F_INT_01 (aggregate × momentum) | **Confirmed Artifact** | Residual vs. both own constituents ≈ 0 (tested Milestone 1D) |
| F_INT_02 (aggregate × size) | **Confirmed Artifact** | Residual vs. both own constituents ≈ 0 (tested Milestone 1D) |
| F_INT_03 (aggregate × liquidity) | **Confirmed Artifact** | Residual vs. both own constituents ≈ 0 (tested Milestone 1D) — survives FDR on raw IC, artifact regardless |
| F_INT_04 (foreign × liquidity) | **Confirmed Artifact** | Residual ≈ 0 |
| F_INT_05 (foreign × volatility) | **Confirmed Artifact** | Residual consistently negative, not positive — raw signal not real |
| F_INT_06 (foreign × size) | **Confirmed Artifact** | Residual collapses cleanly to ~0 |
| F_INT_07 (foreign × momentum) | **Experimental** (per explicit instruction; independently evidenced as artifact) | Strongest raw numbers in the study, fully collapses under residualization, sign-flips post-break |

### F_INST_01 — mandatory permanent conditions (never omit, never summarize away)

1. Effect concentrated before the structural-break interval (approx. through Q3 2025)
2. Post-break IC is approximately zero, not merely smaller
3. Stronger in illiquid / mid-liquidity names; weak in liquid, large-cap names
4. The low-volatility result is not independent of the break (Low-vol & Post-break IC ≈ 0)
5. Cannot be described as universally stable
6. Cannot be described as a confirmed causal informed-trading mechanism — "consistent with," never "demonstrates"

**Acceptable wording:** *"Foreign investor net flow showed conditional predictive power for cross-sectional returns, concentrated in a pre-break interval (through approximately Q3 2025), low-volatility regimes, and illiquid-to-mid-liquidity names."*
**Prohibited wording:** "Foreign flow predicts returns" (unqualified); any causal claim; "robust factor" applied to any interaction feature; "statistically significant" used as a synonym for "real" or "tradeable."
