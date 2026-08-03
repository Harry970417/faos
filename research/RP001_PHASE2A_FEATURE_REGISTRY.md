# RP-001 Phase 2A: Full-Universe Feature Registry

Extends `FEATURE_REGISTRY.md` (50-stock characterization sample) to the full Phase 2A confirmatory universe. Same definitions, no redefinition — this document records what was actually built and its full-universe statistics, per `research/RP001_PHASE2A_EXECUTION_PLAN.md` step 9.

| Feature ID | Definition | Full-universe coverage | Notes |
|---|---|---|---|
| F_INST_01_foreign | `Foreign_Investor` net flow (shares), rank-normalized per day | 84.1% non-missing (all eligible rows); 1,462/2,096 stocks pass the 80% stock-level coverage gate | Primary, locked. `Foreign_Investor`'s constructibility independently verified across all 19 acquisition batches (69 individually-checked Dealer-schema edge cases, zero exceptions) |
| F_INST_05_aggregate | Sum of `Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer_self`, `Dealer_Hedging`, `Dealer` (`min_count=1`) | Verified equal to the true row-wise sum, max deviation = 0.0 | `Dealer` category added to the sum vs. the 50-stock registry (which never encountered it) — safe because `Dealer` and `Dealer_self`/`Dealer_Hedging` are confirmed mutually exclusive per stock (D-05) |
| F_INST_07_flow_to_volume | `F_INST_05 / volume` | Division-by-zero guarded (volume=0 rows already excluded by the eligibility gate) | Secondary candidate |
| F_INT_01_flow_x_momentum | Rank(F_INST_05) × Rank(20d price momentum) | Built, bounds [0, 0.997] | |
| F_INT_02_flow_x_size | Rank(F_INST_05) × Rank(market cap) | **Not built** | Deviation D-08 — market cap unavailable at full-universe scale |
| F_INT_03_flow_x_liquidity | Rank(F_INST_05) × Rank(20d ADV) | Built, bounds [0.0001, 1.0] | |
| F_INT_04_foreign_x_liquidity | Rank(F_INST_01) × Rank(20d ADV) | Built, bounds [0.0001, 1.0] | |
| F_INT_05_foreign_x_volatility | Rank(F_INST_01) × Rank(stock-level 20d realized vol) | Built, bounds [0, 0.984] | Distinct from the market-level vol regime used for H-C4 |
| F_INT_06_foreign_x_size | Rank(F_INST_01) × Rank(market cap) | **Not built** | Deviation D-08 |
| F_INT_07_foreign_x_momentum | Rank(F_INST_01) × Rank(20d price momentum) | Built, bounds [0, 0.997] | |

## Grouping variables

| Variable | Definition | Distribution (rows) |
|---|---|---|
| `liq_tercile` | 20d ADV, per-date cross-sectional tercile | Illiquid 1,900,955 / Mid 1,898,637 / Liquid 1,899,782 / NaN 18,864 (thin cross-sections, <15 stocks that day) |
| `market_vol_regime` | Market realized vol (20d, annualized), full-history median split | LowVol 2,764,117 / HighVol 2,940,745 / NaN 13,376 |
| `break_period` | Locked point estimate 2025-09-25 | pre 5,324,795 / post 393,443 |
| `in_break_window` | Boolean, 2025-08-01 to 2025-10-31 inclusive | Diagnostic flag, not used to exclude rows from H-C1/H-C2's pre/post split |

## Return targets

`fwd_ret_t1`, `fwd_ret_t3`, `fwd_ret_t5` — locked next-open-execution-proxy formula, unchanged from the exploratory-phase build.

## Not in this registry (by design, per Deviation D-08)

Sector classification, PBR/value-growth tercile, market-cap tercile — none required by H-C1–H-C5, all Robustness-only per `research/RP001_RESEARCH_DESIGN.md` §6, none of the three underlying data fields available for the full universe.
