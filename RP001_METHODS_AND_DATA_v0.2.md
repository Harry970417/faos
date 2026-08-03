# RP-001 Methods and Data v0.2

Extends `RP001_METHODS_AND_DATA_v0.1.md` (exploratory, 50-stock sample, preserved unchanged) with Phase 2A's full-universe confirmatory methodology. Same statistical methods throughout — nothing redefined.

## Confirmatory Sample

2,255 stocks (1,980 currently-listed TWSE+TPEx + 275 delisted, survivorship-bias-free), 2012-01-01 through 2026-08-02 (query end date), Daily Investable Universe eligibility gate applied (`RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md`). After the 80% stock-level institutional-data-coverage gate (`RP001_MISSINGNESS_POLICY.md` Rule 3): **1,462 stocks, 3,934,274 panel rows** entered the actual H-C1–H-C4 tests.

## Data Sources

FinMind `TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice`, `TaiwanStockPER` — anonymous API tier, no token, 6,765 requests across 19 rate-limited batches, 100% resolved. Full detail: `RP001_PHASE2A_FINAL_DATASET.md`.

## Data Integrity (full-universe scale)

Trading Calendar Gate: 16,459 mis-dated institutional rows excluded (of 22.1M) — the same contamination class found at 50-stock scale (2026-06-19 and others), now characterized system-wide. Missing-state handling: `NaN` (never 0) for `source_missing`, explicit-zero preserved as a real observation (180,445 such rows confirmed), 80% coverage gate applied per-stock over each stock's own eligible history.

## Features Constructed (full universe)

F_INST_01 (primary), F_INST_05 (aggregate), F_INST_07 (secondary), and 5 of 7 interaction features (F_INT_01, 03, 04, 05, 07) — same locked formulas as `FEATURE_REGISTRY.md`. **F_INT_02 and F_INT_06 (size-based) not constructible** — Deviation D-08, market-cap data unavailable at full-universe scale (the 50-stock sample's shares-outstanding source, TWSE OpenAPI, covers only 1,089 currently-listed TWSE companies with corrupted text encoding, unusable for the 2,255-stock confirmatory universe).

## Statistical Methods (identical to v0.1, reused not redesigned)

- Daily cross-sectional Spearman Rank IC, forward returns t+1/t+3/t+5 (locked next-open-execution-proxy formula)
- Newey-West (1987) standard errors, 5 lags, for every significance test
- Cross-sectional OLS residualization (neutralization) against both interaction constituents jointly
- Benjamini-Hochberg FDR, α=0.10, applied jointly across all 16 primary confirmatory test statistics

**Implementation note:** the full-universe daily-IC computation was vectorized (closed-form per-date Pearson correlation on within-date ranks, mathematically identical to Spearman correlation) rather than looping `scipy.stats.spearmanr` per date, purely for runtime — verified to produce identical results to the loop-based method on the exploratory-scale data before use.

## Regime and Grouping Definitions (identical to v0.1, reused)

Market volatility: 20-day rolling realized volatility of the eligible-universe's mean daily return, median split over full history. Liquidity terciles: 20-day rolling average trading value, per-date cross-sectional tercile. Break period: locked point estimate 2025-09-25.

## What Was Not Done (unchanged from v0.1)

No portfolio construction, no backtest, no Sharpe/drawdown, no transaction-cost modeling, no causal identification design. Sector and PBR/value-growth cuts were not re-run at full-universe scale (data unavailable, Deviation D-08; both were Robustness-only, not required by any of the five locked hypotheses).
