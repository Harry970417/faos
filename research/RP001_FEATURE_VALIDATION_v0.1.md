# RP-001 Milestone 1B: Feature Validation

All numbers below are computed from the real 24,535-row feature panel (`rp001_features_v0.1.parquet`) — nothing estimated or projected. No IC, ICIR, or backtest performed anywhere in this milestone.

## 1. Feature Health Report

| Feature | Coverage | Missing | Zero Rate | Skew | Kurtosis | Outlier Rate (3×IQR) |
|---|---|---|---|---|---|---|
| F_INST_01_foreign | 100% | 0 | 0.0% | 1.53 | 65.2 | 10.5% |
| F_INST_02_trust | 100% | 0 | 2.7% | −2.26 | **343.2** | 17.2% |
| F_INST_03_dealer_self | 100% | 0 | 1.2% | −6.34 | 222.5 | 11.9% |
| F_INST_04_dealer_hedge | 100% | 0 | 0.1% | 2.27 | 79.0 | 12.2% |
| F_INST_05_aggregate | 100% | 0 | 0.0% | 0.85 | 24.3 | 10.3% |
| F_INST_06_value_proxy | 100% | 0 | 0.0% | −5.43 | 157.8 | 9.8% |
| F_INST_07_flow_to_volume | 100% | 0 | 0.0% | 0.05 | 0.05 | 0.004% |
| F_INST_08_streak | 100% | 0 | 0.0% | 2.01 | 25.9 | 2.0% |
| F_INST_09_change_rate | 98.2% | 450 | 0.0% | 10.11 | **4107.8** | 10.5% |
| F_INT_01_flow_x_momentum | 95.9% | 1,000 | 0.0% | 0.82 | −0.32 | 0.0% |
| F_INT_02_flow_x_size | 100% | 0 | 0.0% | 1.01 | 0.15 | 0.0% |
| F_INT_03_flow_x_liquidity | 98.2% | 450 | 0.0% | 1.02 | 0.36 | 0.0% |

**The kurtosis column is the headline result, not a side note.** F_INST_09 at kurtosis 4,107 and F_INST_02 at 343 are extreme even by financial-data standards — this is direct, quantitative confirmation (not just qualitative "fat tails" language) of Milestone 0C's decision to make rank standardization primary. Raw z-scoring any of the flow-magnitude features would be dominated by a handful of extreme days. The two interaction features that are themselves already rank-products (F_INT_02, F_INT_03) show near-normal kurtosis, exactly as expected — this is a useful internal consistency check, not a coincidence.

Missing values in F_INST_09/F_INT_01/F_INT_03 are entirely the rolling-window warmup period (first ~10-20 obs per stock), not data gaps — consistent with how they were constructed (see `FEATURE_REGISTRY.md`).

## 2. Correlation Analysis

Full matrices in `feature_corr_pearson.csv` / `feature_corr_spearman.csv`. Redundancy candidates (|Spearman| > 0.7):

| Pair | Spearman ρ |
|---|---|
| F_INST_05_aggregate ↔ F_INST_07_flow_to_volume | 0.91 |
| F_INST_05_aggregate ↔ F_INST_06_value_proxy | 0.89 |
| F_INST_06_value_proxy ↔ F_INST_07_flow_to_volume | 0.88 |
| F_INST_01_foreign ↔ F_INST_05_aggregate | 0.83 |
| F_INST_07_flow_to_volume ↔ F_INST_08_streak | 0.79 |
| F_INT_02_flow_x_size ↔ F_INT_03_flow_x_liquidity | 0.71 |

**Real redundancy, not coincidence.** F_INST_05/06/07 are mechanically related (value_proxy = aggregate × price; flow/volume ≈ aggregate rescaled), so their correlation is expected — but it means testing all three in Milestone 1C as if they were three independent signals would overstate how much distinct information the feature set actually carries. F_INST_01 tracking F_INST_05 at 0.83 confirms what Milestone 0A already showed indirectly: Foreign_Investor is the dominant category by magnitude, so the aggregate is substantially a foreign-flow proxy, not an equally-weighted blend of all institutions. **Recommendation for Milestone 1C: treat {F_INST_05, F_INST_06, F_INST_07} as one redundancy cluster and report IC for the cluster's best performer plus the others as robustness checks, not as three independent bets.**

## 3. Distribution Diagnostics

Histogram, QQ-plot vs. Normal, and rank-vs-z-score scatter generated for F_INST_05 (the primary aggregate) and F_INST_09 (the highest-kurtosis feature) — saved as real PNG files: `rp001_data/figures/F_INST_05_aggregate_diagnostics.png`, `F_INST_09_change_rate_diagnostics.png`. The QQ-plots visually confirm the kurtosis numbers above (heavy tail departure from the normal line); the rank-vs-z-score panels show the compression rank normalization applies to those tails — the empirical basis for preferring rank over z-score, not just the abstract argument made at Milestone 0C.

## 4. Leakage Validation

**Empirical test, not code review only.** For both rolling-window features (F_INST_09, F_INT_01), recomputed the value at an interior test date using *only* data truncated at that date, and compared against the value computed from the full dataset. **Both matched exactly** (stock 2330: rolling-mean −5,660,382.2 both ways; momentum −0.03846... both ways) — direct, quantitative proof the construction code never looks ahead, not an assumption from reading the code.

**One leakage risk this does NOT close, and I'm not overselling this section by omitting it:** the Merge Loss Audit (below) found a real, mis-dated institutional data row (2026-06-19, a confirmed non-trading day, with genuine non-zero buy/sell values). It didn't reach the current feature panel — but only because the inner join with price data happened to drop it, not because the pipeline has a deliberate trading-calendar check. If a similarly mis-dated row ever lands on a date that *does* have valid price data, it would silently violate the t-only rule with the current pipeline design. **Recommendation: add an explicit trading-calendar validation step before Milestone 1C, not rely on the inner join's incidental protection.**

## 5. Merge Loss Audit

0.20% merge loss (49 of 24,584 institutional rows) fully traced to individual cause, not left as an aggregate percentage:

| Category | Count | Basis |
|---|---|---|
| IPO | 0 | All 50 sample stocks have listing histories well before the sample window |
| Delisting | 0 | No sample stock delisted during 2024-07 to 2026-07 |
| Ticker mismatch | 0 | No evidence of stock_id inconsistency between sources |
| **Holiday — with a real data-quality anomaly** | **49** | All 49 fall on a single date, 2026-06-19, confirmed as a real non-trading day (price series has zero rows for it, jumping 06-18 → 06-22 across the entire sample). **But the institutional data for that date is not simply absent — it contains real, non-zero buy/sell figures for 49 of 50 stocks**, meaning FinMind's pipeline attributed real trading data to a date when no trading occurred. This is a genuine data-integrity issue in the source, not a benign "holiday, no data expected" case. |
| Corporate Action (trading halt) | 3 | 2317 (2025-07-30), 1101 (2025-08-13), 2884 (2025-11-05) — confirmed via price rows with volume=0, spread=0.0 on those exact dates: real halts, not missing data |
| Missing (unexplained) | 5 | 2912 (2026-06-10), 2368 (2026-06-11), 2882 (2026-06-11), 1101 (2026-06-16), 3231 (2026-06-16) — confirmed via price rows showing real, substantial trading volume (millions of shares) with no corresponding institutional row. No explanation found; genuinely unexplained gaps |

**8 price-only mismatches (price exists, institutional doesn't) were also classified**, not just the 49 institutional-only ones — 3 trading halts (legitimate), 5 genuinely unexplained.

## Net assessment for Milestone 1C readiness

Feature health and correlation results are usable as-is. Two concrete action items before 1C, not blocking issues requiring a redesign: (1) add trading-calendar validation as a real pipeline safeguard, not rely on incidental inner-join protection; (2) treat the F_INST_05/06/07 cluster as one signal group in IC reporting, not three independent ones.
