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

## Feature Status — as of Milestone 1C-R (interim, no Freeze)

Status reflects IC/ICIR diagnostics (1C), mechanism analysis (1C+), and robustness/confirmation testing (1C-R) — see `RP001_MILESTONE_1C_R_ROBUSTNESS.md` for full reasoning.

| Feature | Status | Basis |
|---|---|---|
| F_INST_01_foreign | **Conditional Candidate** (recommended for 1D Freeze Review) | Robust across FDR correction, break-detection, and neutralization — but valid only pre-break (~through Aug–Oct 2025), low-vol regime, illiquid/mid-liquidity names. Never unconditional. |
| F_INST_07_flow_to_volume | **Secondary Conditional Candidate** | Retains incremental info beyond F_INST_05 (Milestone 1C), but its own structural break not independently confirmed (permutation p=0.171) |
| F_INST_02_trust | Rejected | No evidence of predictive power at any horizon tested |
| F_INST_03_dealer_self | Experimental (insufficient evidence either way) | Marginal, only significant at t+5 |
| F_INST_04_dealer_hedge | Rejected | No evidence of predictive power at any horizon tested |
| F_INST_05_aggregate | Deprecated (reconstruction candidate) | Dilutes F_INST_01's real signal by summing in non-informative categories |
| F_INST_06_value_proxy | Deprecated | Confirmed redundant with F_INST_05 via incremental-IC test (residual IC ≈ 0.002) |
| F_INST_08_streak | Experimental (insufficient evidence either way) | Weak, marginal only at t+5 |
| F_INST_09_change_rate | Rejected | No evidence of predictive power at any horizon tested |
| F_INT_01 / F_INT_07 (Foreign × Momentum) | **Experimental** (per explicit instruction) | Confirmed Additive Recombination Artifact via residualization — strongest raw numbers in the study, fully explained by its two components, sign-flips post-break |
| F_INT_02_flow_x_size | Artifact / Redesign Required | Sector-neutral IC flips sign |
| F_INT_03_flow_x_liquidity | Artifact / Redesign Required | Survives FDR correction on raw IC, but sector-neutralization explains away 75% — statistical survival is not sufficient on its own |
| F_INT_04_foreign_x_liquidity | **Confirmed Artifact** | Residual IC ≈ 0 after joint residualization |
| F_INT_05_foreign_x_volatility | Inconclusive, leaning Artifact | Residual IC consistently negative (not just null) across every cut tested |
| F_INT_06_foreign_x_size | **Confirmed Artifact** | Residual IC collapses cleanly to ~0 across every cut tested |
