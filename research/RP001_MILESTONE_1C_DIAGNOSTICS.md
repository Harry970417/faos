# RP-001 Milestone 1C: Feature Diagnostics

All numbers below are computed from the real 24,535-row feature panel (v0.2, post-remediation), on the 50-stock characterization sample. No portfolio construction, backtest, or performance analysis performed anywhere in this milestone.

**Methodology note stated up front:** forward returns are cumulative t+1-open to t+(1+h)-open windows (h=1,2,3,5), not marginal single-day returns — "IC increasing with horizon" below describes cumulative-window predictability, not literal signal decay in the strictest econometric sense. This distinction matters for how the results are read.

## IC / ICIR / Significance — full results in `milestone1c_ic_summary.csv`

Headline pattern across nearly every feature: **IC is weak-to-absent at t+1 and strengthens toward t+5.** This runs opposite to the classic price-pressure-reversal story (Chordia & Subrahmanyam 2004, cited in RP001_EVIDENCE_MAP.md) and is more consistent with H1a (informed trading, slow price discovery) than H1b — a real, substantive result bearing directly on the original research question, not just a diagnostic footnote.

| Feature | t+1 IC (t_nw) | t+5 IC (t_nw) | Verdict at t+5 |
|---|---|---|---|
| F_INST_01_foreign | 0.011 (1.24) | 0.029 (2.74) | Significant, strengthens with horizon |
| F_INST_02_trust | −0.008 (−0.95) | −0.005 (−0.46) | No evidence of predictive power, either direction |
| F_INST_03_dealer_self | 0.013 (1.75) | 0.021 (2.36) | Significant only at t+5, weak elsewhere |
| F_INST_04_dealer_hedge | 0.013 (1.52) | 0.006 (0.75) | Not significant at any horizon |
| F_INST_05_aggregate | 0.0001 (0.02) | 0.015 (1.38) | Essentially zero at t+1/t+3, weak even at t+5 |
| F_INST_06_value_proxy | 0.002 (0.22) | 0.016 (1.43) | Weak, not significant |
| F_INST_07_flow_to_volume | 0.003 (0.33) | 0.022 (1.98) | Borderline significant at t+5 only |
| F_INST_08_streak | 0.003 (0.31) | 0.024 (1.77) | Weak, borderline at t+5 |
| F_INST_09_change_rate | −0.010 (−1.17) | 0.001 (0.07) | No evidence of predictive power |
| **F_INT_01_flow_x_momentum (Experimental)** | 0.019 (1.83) | 0.044 (2.57) | Strongest numbers in the set — **excluded from Freeze consideration regardless, per your instruction** |
| F_INT_02_flow_x_size | 0.009 (1.09) | 0.023 (1.68) | Marginally significant at t+2 only, weakens after neutralization (see below) |
| F_INT_03_flow_x_liquidity | 0.019 (1.66) | 0.061 (3.18) | Strongest raw numbers of any non-Experimental feature — but see neutralization below |

## Stability — this is where the raw IC table's optimism substantially breaks down

**By year — the single most important stability finding:** every feature tested shows sharp decay from 2024 to 2026. F_INST_01: 0.072 (2024) → 0.022 (2025) → **−0.001 (2026)**. F_INT_03: 0.122 → 0.034 → 0.056. The full-sample "significant" results are disproportionately driven by 2024; by 2026, F_INST_01's signal has effectively vanished. **This alone is enough to prevent calling any feature's predictive power "stable" without heavy qualification.**

**By market-cap tercile:** relatively flat across Small/Mid/Large for F_INST_01 (no strong size-conditionality — the original H3 hypothesis is not clearly supported by this evidence). F_INT_03 somewhat weaker in Large-cap (0.027 vs. 0.065–0.069 in Small/Mid).

**By market state:** consistent, substantial pattern across every feature tested — **institutional flow is 2–3× more informative in Bear periods than Bull.** F_INT_03: 0.139 (Bear) vs. 0.046 (Bull). Real and consistent, though based on a smaller Bear sample (90 vs. 335 days).

**By sector (2 largest sectors only, given sample composition):** sector 24 shows real positive IC, sector 25 near-zero-to-negative for the same features — a real difference, but tested on only 2 sectors given this sample's concentration, not a broad cross-sector result.

## Neutralization — the finding that most changes the picture

| Feature | Raw IC (t+5) | Mcap-neutral retention | Sector-neutral retention |
|---|---|---|---|
| F_INST_01_foreign | 0.029 | 101% | 62% |
| F_INT_02_flow_x_size | 0.023 | 58% | **−29% (sign flips)** |
| F_INT_03_flow_x_liquidity | 0.061 | 88% | **25%** |

**F_INT_03 — the strongest-looking feature in the raw table — loses 75% of its IC once sector is controlled for.** Its apparent strength is substantially a sector-composition artifact, not a robust flow-liquidity interaction. F_INT_02 is worse: sector-neutral IC actually flips sign. F_INST_01 is the most robust of the three — market-cap neutralization barely touches it, and even sector-neutralization leaves the majority of its signal intact.

## Redundancy Diagnostics — F_INST_05/06/07

Residualizing F_INST_06 against F_INST_05 leaves almost nothing: incremental IC ≈ 0.002 (icir ≈ 0.01) — **F_INST_06 adds essentially no information beyond F_INST_05**, confirming Milestone 1B's correlation-based redundancy flag with a direct incremental-IC test, not just a correlation coefficient. F_INST_07 fares better: incremental IC ≈ 0.0135 after removing F_INST_05's effect, retaining roughly 60% of its own raw t+5 IC — **F_INST_07 carries real information beyond the aggregate; F_INST_06 does not.**

Also worth stating plainly: F_INST_05 (aggregate) itself is nearly flat at t+1/t+3, while its component F_INST_01 (foreign only) shows real signal at those same horizons. **Summing all institution types appears to dilute the one component that actually carries information** — a genuine construction-level finding, not just a redundancy note.

## Final Assessment

**Which features show stable predictive power:** None, without qualification. F_INST_01_foreign is the closest — significant at t+2/t+5, robust to market-cap neutralization, retains most of its signal after sector-neutralization — but even it decayed from IC=0.072 in 2024 to statistically indistinguishable from zero in 2026. Calling it "stable" would overstate what the data shows.

**Which features are conditional on market state or grouping:** All of them, to varying degrees. Every feature tested is 2–3× stronger in Bear markets. F_INT_02 and F_INT_03's raw strength is substantially sector-driven, not unconditional.

**Which results may be affected by correlated features or data anomalies:** F_INST_06 (redundant with F_INST_05, near-zero incremental IC). F_INT_02 and F_INT_03 (raw IC substantially explained away by sector-neutralization — F_INT_02's sign even flips). The 2026-06-19 data anomaly itself is already excluded per Milestone 1B-R and does not affect these results.

**Recommended for Milestone 1D Freeze Review:** **F_INST_01_foreign** only, and even that should carry the year-over-year decay and sector-partiality as explicit conditions attached to any Freeze decision, not a clean pass. **F_INST_07_flow_to_volume** is a secondary candidate — weaker raw signal, but confirmed to carry real incremental information beyond F_INST_05.

**Recommended Experimental:** F_INT_01_flow_x_momentum (per your instruction, regardless of its strong numbers). F_INST_03_dealer_self and F_INST_08_streak (weak, inconsistent, only marginal at t+5 — not enough evidence either way).

**Recommended Deprecated:** F_INST_06_value_proxy (confirmed redundant with F_INST_05 via incremental-IC test, not just correlation). F_INST_05_aggregate itself is a candidate for reconstruction rather than outright deprecation — the aggregation method, not the underlying data, appears to be diluting a real signal.

**Recommended Rejected:** F_INST_02_trust (consistently negative-to-zero, never significant at any horizon). F_INST_04_dealer_hedge (never significant at any horizon). F_INST_09_change_rate (no evidence of predictive power at any horizon tested).

**F_INT_02_flow_x_size and F_INT_03_flow_x_liquidity:** neither Freeze-ready nor cleanly Rejected — their raw IC is real but substantially sector-driven per the neutralization test. Recommend holding at Experimental pending a sector-neutral-by-construction redesign, not advancing to 1D as currently specified.
