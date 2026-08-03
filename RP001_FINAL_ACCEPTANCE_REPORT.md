# RP-001 Final Acceptance Report

**RP-001 Status: Completed**

**Accepted by:** User, 2026-08-03. This report is the formal closure record — it does not introduce new analysis, and no further Feature Discovery, Breakpoint Optimization, Threshold Tuning, Portfolio Backtest, Trading Strategy, Investment Recommendation, or rescue analysis of H-C1 is performed here or authorized under this research ID going forward.

## Research Question

Does foreign institutional net flow predict short-horizon cross-sectional returns in Taiwan equities, and if so, under what conditions does the relationship hold or break down?

## Protocol Status

`RP001_PHASE2A_PROTOCOL_LOCK.md` locked 2026-07-11 (commit `82bc4a3`). All six locked documents remained unmodified in place throughout Phase 2A execution; every deviation was logged before the affected test ran, per `RP001_DEVIATION_POLICY.md`. No Escalating Deviation was ever triggered — F_INST_01's definition, rank normalization, return-horizon construction, and the break interval's boundary dates were never reopened.

## Final Dataset Scale

- **Acquisition universe:** 2,255 stocks (1,980 currently-listed TWSE+TPEx + 275 delisted), 6,765 API requests, 100% resolved, 34,236,687 raw rows.
- **Confirmatory panel:** 5,718,238 eligible Daily Investable Universe rows.
- **Confirmatory test sample:** 1,462 stocks (80% coverage-gate-passing), 3,934,274 rows.
- **Final dataset SHA-256:** `b945702f9e5f203703c1654b6657a24626747c1fd130a9d1070c5d6987917bb6`.

## H-C1–H-C5 Verdicts

| Hypothesis | Verdict |
|---|---|
| H-C1 (pre-break positive IC) | Not Replicated |
| H-C2 (post-break null) | Replicated (weak — see `RP001_PHASE2A_HYPOTHESIS_VERDICTS.md` caveat) |
| H-C3 (liquidity conditionality) | Partially Replicated |
| H-C4 (volatility break-conditionality) | Not Replicated |
| H-C5 (no genuine interactions) | Not Replicated |

## Deviations

Eight deviations logged across Phase 2A (D-01 through D-08), full detail in `RP001_PHASE2A_DEVIATION_LOG.md` and consolidated in `RP001_PHASE2A_DEVIATION_FINAL.md`. None escalated. The last, D-08 (market-cap/sector data unavailable at full-universe scale), left F_INT_02 and F_INT_06 untestable under H-C5 — reported as such, not approximated or silently dropped.

## Reproducibility Status

Fully reproducible from committed raw data and code: `rp001_phase2a_build_panel.py` → `rp001_phase2a_build_features.py` → `rp001_phase2a_coverage_and_tests.py` → `rp001_phase2a_confirmatory_tests.py` → `rp001_phase2a_build_charts.py`. No stochastic step anywhere in the pipeline. Every raw acquisition file individually SHA-256-hashed; final dataset hashed; 21/21 unit and leakage-truncation tests pass. Full detail: `RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`.

## Final Feature Decisions

See `FEATURE_REGISTRY.md`'s "Feature Status — FINAL, post-Phase 2A Confirmatory Closure" section (authoritative, supersedes the Milestone 1D table for status purposes; the Milestone 1D table itself is preserved unchanged as historical record):

- **F_INST_01:** Not Replicated — Exploratory Only
- **F_INST_07:** Inconclusive / Secondary Research Candidate
- **F_INST_06:** Deprecated — Redundant
- **F_INST_02 / F_INST_04 / F_INST_09:** Rejected
- **F_INST_03 / F_INST_08:** Inconclusive
- **F_INST_05:** Deprecated
- **Interaction Family (F_INT_01–F_INT_07):** Exploratory conclusions not uniformly replicated; newly observed residual effects require a separate pre-registered study

## Research Integrity Statement

No methodology was changed after any result was seen, at any stage of Phase 2A. Every finding that contradicts the exploratory-phase conclusions — including the central, headline result that F_INST_01 does not replicate — is reported in full in `RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `RP001_RESEARCH_FINDINGS_v0.2.md`, and this report, with no adjustment, softening, or omission. All exploratory-phase documents (`RP001_RESEARCH_REPORT_v0.1.md`, `RP001_RESEARCH_FINDINGS_v0.1.md`, `FEATURE_REGISTRY.md`'s Milestone 1D table) remain unmodified in place as the historical record, superseded in status but not deleted or rewritten. Every deviation, however small, was logged before the affected test ran and disclosed regardless of materiality. The unexpected H-C5 residual-effect finding, surfaced during closure, is disclosed in full and explicitly ruled out as grounds for further ad hoc analysis under this research ID.

## Formal Core Conclusion (fixed, final)

> 本研究在 50 檔探索樣本中觀察到外資買賣超的條件式預測能力，但該結果未能在完整 TWSE 與 TPEx 股票池中複現。低波動機制亦未獲支持，流動性條件僅部分複現。部分交互作用項在完整樣本中出現小量級殘差效果，但屬確認性樣本中的意外發現，必須由新的預註冊研究獨立驗證。整體證據不支持將外資買賣超視為穩定、普遍或可直接交易的無條件因子。

## Formal Closure Decision

**RP-001 is formally closed as Completed.** The research question was answered — with a negative result for the central hypothesis at full-universe confirmatory scale. No further work is authorized under this research ID: no new feature discovery, no breakpoint re-optimization, no threshold re-tuning, no portfolio backtest, no trading strategy development, no investment recommendation, and no rescue analysis of H-C1. Any future work on the unexpected H-C5 residual-effect finding requires an independently pre-registered new study, not a reopening of RP-001.
