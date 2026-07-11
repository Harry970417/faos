# RP-001 Methods and Data v0.1

## Sample

50 stocks (taiwan-attention-signal's existing curated list, large-cap-weighted, includes 3 financial holding stocks retained for characterization completeness but excluded from the actual research universe per `RP001_RESEARCH_DESIGN.md`). 2024-07-01 to 2026-07-09, 491 confirmed trading days. This is **not** RP-001's designed full research universe — see Limitations.

## Data Sources (all real, web-verified this session — see individual milestone reports for verification detail)

- FinMind `TaiwanStockInstitutionalInvestorsBuySell` — 5 institutional categories (Foreign_Investor, Foreign_Dealer_Self, Investment_Trust, Dealer_self, Dealer_Hedging), shares not NT$ value
- FinMind `TaiwanStockPrice` — OHLC, volume, trading value
- FinMind `TaiwanStockPER` — PBR/PER for value-growth classification
- FinMind `TaiwanStockDelisting` — 337 rows, confirmed available for survivorship-bias-free construction (not yet used at this sample scale)
- TWSE official OpenAPI (`openapi.twse.com.tw`) — company info, shares outstanding, industry classification

## Data Integrity

Trading Calendar Gate built from the price data's own confirmed trading days; one contamination date found and permanently excluded (2026-06-19, a real non-trading day with erroneous non-zero institutional data — see `RP001_READINESS_REVIEW.md` and `RP001_MILESTONE_1B_R` materials). Missing-state classification distinguishes `observed_zero`, `source_missing`, `non_trading_day`, and `trading_halt` — `source_missing` is never silently imputed as zero.

## Features Constructed

11 base features (F_INST_01–09, F_INT_01–03) per `RP001_FEATURE_SPECIFICATION.md` and `FEATURE_REGISTRY.md`, plus 4 additional interaction features (F_INT_04–07) built during mechanism analysis. Foreign_Dealer_Self excluded as a standalone feature (99.99% zero-rate, degenerate — Milestone 0A finding). Rank (percentile) standardization used as primary normalization, not z-score, based on confirmed extreme kurtosis (up to 4,107) in the raw distributions.

## Statistical Methods

- **Daily cross-sectional Spearman Rank IC**, forward returns at t+1/t+2/t+3/t+5 (cumulative windows from the first tradeable point after flow data publishes, not same-day close-to-close)
- **ICIR** = mean(IC)/std(IC); **Newey-West (1987)** standard errors (5 lags) for all significance tests, not naive t-stats
- **Unknown-breakpoint testing**: self-implemented Quandt-Andrews sup-Wald test with permutation p-values (2,000 reps) — `ruptures`/Bai-Perron unavailable (no C++ compiler in this environment)
- **Neutralization/residualization**: cross-sectional OLS regression of the target on control variables within each date, residual retained
- **Multiple testing**: Benjamini-Hochberg FDR correction, α=0.10, applied to a 56-test inventory (not a selected subset)

## Regime and Grouping Definitions

Market volatility: 20-day rolling realized volatility of an equal-weighted 50-stock price index, median split (pre-committed primary spec, stated before the robustness pass). Market regime (Bull/Bear/Sideways): 60-day trend with ±3% thresholds. Liquidity terciles: 20-day rolling average trading value. Value/Growth terciles: PBR. Sector: TWSE official numeric industry code.

## What Was Not Done

No portfolio construction, no backtest, no Sharpe/drawdown, no transaction-cost modeling, no causal identification design (instrument, natural experiment, or similar) anywhere in this study.
