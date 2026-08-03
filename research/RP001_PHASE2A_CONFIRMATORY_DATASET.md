# RP-001 Phase 2A.3: Confirmatory Dataset

**Date:** 2026-08-02/03. **Status:** Complete. Built from the full-universe raw data (`research/RP001_PHASE2A_FINAL_DATASET.md`), all steps locked-definition-only per `FEATURE_REGISTRY.md` / `research/RP001_PHASE2A_EXECUTION_PLAN.md` Phase 2A.3. Build code: `research/rp001_phase2a_build_panel.py` → `research/rp001_phase2a_build_features.py` → `research/rp001_phase2a_coverage_and_tests.py`. Output: `rp001_data/phase2a/processed/rp001_confirmatory_dataset_v0.1.parquet` (SHA-256 `b945702f9e5f2037...`, full hash in `rp001_dataset_snapshot.json`).

## 1. Daily Investable Universe

Eligibility gate per `research/RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md`: `date >= max(2012-05-02, stock_eligibility_start)`, `date < delisting_date`, `Trading_Volume > 0`. Applied to 6,267,742 raw price rows → **5,718,238 eligible rows (91.2%)**, across 2,098 stocks with any price data (of 2,255 in the acquisition universe; 157 stocks returned zero price rows, mostly TDR-style/delisted codes with no retrievable history).

## 2. Trading Calendar Gate

Global market-wide trading calendar built from all price dates; institutional rows not falling on a confirmed trading day for *any* stock are excluded before the merge (catches the D-06/D-07 mis-dated-row contamination class). **16,459 institutional rows excluded** (of 22,127,036) — proportionally consistent with the single-digit-per-batch counts found during acquisition, now aggregated across the full universe.

## 3. Missing-state handling

Per `research/RP001_MISSINGNESS_POLICY.md`: price (eligible-universe) is the panel backbone; institutional data is **left-joined**, so a stock-date with no institutional row becomes `NaN` (`source_missing`), never `0`. Explicit-zero rows (`buy=0, sell=0`, a real reported "no net flow") are preserved as `F_INST_01 = 0` — 180,445 such observations confirmed present, not collapsed into the missing category. Overall F_INST_01 coverage across all eligible rows: **84.1%**.

**Rule 3 coverage gate (80% threshold, per-stock, over each stock's own eligible history):** **1,462 of 2,096 stocks with any panel presence pass (69.8%)**. Stock 1213 (the known AR-03 sparse case from Batch 1) is correctly excluded — coverage rate 34.6%. Only stocks passing this gate are included in H-C1–H-C4; `rp001_data/phase2a/processed/rp001_stock_coverage.csv` records every stock's rate for full auditability.

## 4. Features constructed

| Feature | Status |
|---|---|
| F_INST_01_foreign (primary) | Built, locked definition (`Foreign_Investor` net flow, rank-normalized per day) |
| F_INST_05_aggregate | Built (sum of all 6 raw categories, `min_count=1`; verified by unit test to equal the true sum with zero deviation) |
| F_INST_07_flow_to_volume (secondary) | Built (`F_INST_05 / volume`) |
| F_INT_01 (flow×momentum), F_INT_03 (flow×liquidity), F_INT_04 (foreign×liquidity), F_INT_05 (foreign×volatility), F_INT_07 (foreign×momentum) | Built, locked product-of-ranks formulas, all pass bounds/no-infinite-values tests |
| F_INT_02 (flow×size), F_INT_06 (foreign×size) | **Not constructible — Deviation D-08** (market-cap data unavailable at full-universe scale). Present as all-`NaN` columns, not silently dropped, so downstream code fails loudly rather than misreading absence as zero. |

## 5. Return targets

`fwd_ret_t1/t3/t5` — locked "next-open execution proxy" formula, unchanged from the exploratory-phase code (`close.shift(-(h+1)) / close.shift(-1) - 1`, computed on each stock's full raw price series before eligibility filtering, then merged onto the eligible panel so no genuine future trading day is lost at the eligibility boundary).

## 6. Break-period, liquidity, and volatility labels

- **Break period:** `pre` (date < 2025-09-25, locked point estimate) / `post` (date ≥ 2025-09-25). 5,324,795 pre-break rows, 393,443 post-break rows (post-break window is Sept 2025–Aug 2026, ~11 months, vs. pre-break's ~13.5 years — expected imbalance, not adjusted).
- **Liquidity tercile:** 20-day rolling average trading value, per-date cross-sectional tercile split (`Illiquid`/`Mid`/`Liquid`), locked definition. Roughly even thirds (1.90M/1.90M/1.90M rows).
- **Market volatility regime:** market-wide realized volatility (20-day rolling std of the eligible-universe's mean daily close return, annualized), median split over full history (`LowVol`/`HighVol`), locked definition. 2.76M LowVol / 2.94M HighVol rows.

## 7. Unit tests and leakage-truncation tests

**21/21 passed** — full detail in `rp001_data/phase2a/processed/rp001_dataset_snapshot.json`. Covers: rank bounds [0,1] for all rank/interaction columns, no infinite values, F_INST_05 mathematically re-verified against its raw category sum, explicit-zero preservation, break-period split correctness, D-08 columns confirmed all-NaN (not silently zero), no forward-return leakage past each stock's series end, no cross-date rank leakage.

## 8. What this dataset does not include

Sector classification and PBR (value/growth) data — neither was part of the Phase 2A.2 acquisition (see D-08); both are Robustness-only cuts under `research/RP001_RESEARCH_DESIGN.md` §6, not required by any of the five locked confirmatory hypotheses.
