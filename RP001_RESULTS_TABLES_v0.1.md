# RP-001 Results Tables v0.1

Consolidated from Milestones 1C, 1C+, 1C-R, 1D. Source CSVs: `milestone1c_ic_summary.csv`, `regime_robustness_full.csv`, `multiple_testing_register.csv`, `rp001_missing_state_classification.csv`.

## Table 1 — Full-Sample IC by Feature and Horizon (Rank Spearman, Newey-West t-stat)

| Feature | t+1 IC (t) | t+2 IC (t) | t+3 IC (t) | t+5 IC (t) |
|---|---|---|---|---|
| F_INST_01_foreign | 0.011 (1.24) | 0.023 (2.66) | 0.015 (1.65) | 0.029 (2.74) |
| F_INST_02_trust | −0.008 (−0.95) | −0.010 (−1.09) | −0.010 (−0.97) | −0.005 (−0.46) |
| F_INST_03_dealer_self | 0.013 (1.75) | 0.010 (1.13) | 0.006 (0.71) | 0.021 (2.36) |
| F_INST_04_dealer_hedge | 0.013 (1.52) | 0.011 (1.33) | 0.012 (1.48) | 0.006 (0.75) |
| F_INST_05_aggregate | 0.0001 (0.02) | 0.008 (0.94) | 0.0000 (0.00) | 0.015 (1.38) |
| F_INST_06_value_proxy | 0.002 (0.22) | 0.007 (0.84) | 0.007 (0.77) | 0.016 (1.43) |
| F_INST_07_flow_to_volume | 0.003 (0.33) | 0.009 (0.99) | 0.006 (0.61) | 0.022 (1.98) |
| F_INST_08_streak | 0.003 (0.31) | 0.007 (0.72) | 0.011 (0.98) | 0.024 (1.77) |
| F_INST_09_change_rate | −0.010 (−1.17) | −0.004 (−0.42) | −0.008 (−0.93) | 0.001 (0.07) |
| F_INT_01_flow_x_momentum (agg) | 0.019 (1.83) | 0.029 (2.32) | 0.026 (1.80) | 0.044 (2.57) |
| F_INT_02_flow_x_size (agg) | 0.009 (1.09) | 0.021 (2.03) | 0.016 (1.38) | 0.023 (1.68) |
| F_INT_03_flow_x_liquidity (agg) | 0.019 (1.66) | 0.041 (2.91) | 0.042 (2.62) | 0.061 (3.18) |

## Table 2 — Structural Break (Unknown Breakpoint, Permutation-Corrected)

| Feature | Sup-Wald date | sup\|t\| | Permutation p |
|---|---|---|---|
| F_INST_01 | 2025-09-25 | 3.45 | **0.0105** |
| F_INST_07 | 2025-09-26 | 2.39 | 0.171 |

## Table 3 — Regime Robustness (F_INST_01, t+5, primary vol spec: market rvol 20d, median split)

| Regime | n | Mean IC | t_NW | 95% CI |
|---|---|---|---|---|
| Low volatility | 238 | 0.047 | 3.18 | [0.018, 0.076] |
| High volatility | 237 | 0.005 | 0.37 | [−0.022, 0.032] |
| Low-vol & Pre-break | 167 | 0.069 | 3.99 | — |
| Low-vol & Post-break | 71 | **−0.004** | −0.17 | — |
| High-vol & Pre-break | 135 | 0.032 | 1.57 | — |
| High-vol & Post-break | 112 | −0.011 | −0.57 | — |

## Table 4 — Liquidity Mechanism (F_INST_01, t+5)

| Cut | Illiquid | Mid | Liquid |
|---|---|---|---|
| Raw | 0.034 (1.94) | 0.031 (1.94) | 0.010 (0.63) |
| Mcap-neutral | 0.034 (1.94) | 0.031 (1.96) | 0.012 (0.78) |
| Sector-neutral | 0.047 (3.28) | 0.009 (0.64) | 0.008 (0.54) |
| Pre-break | 0.057 (2.76) | 0.054 (2.88) | 0.012 (0.58) |
| Post-break | −0.003 | −0.006 | 0.006 |

## Table 5 — All Seven Interaction Features, Joint Residualization (t+5)

| Feature | Raw IC (t) | Residual IC (t) | Pre-break resid | Post-break resid | Verdict |
|---|---|---|---|---|---|
| F_INT_01 (agg × momentum) | 0.044 (2.57) | −0.004 (−0.42) | 0.001 | −0.011 | Confirmed Artifact |
| F_INT_02 (agg × size) | 0.023 (1.68) | −0.003 (−0.38) | −0.006 | 0.001 | Confirmed Artifact |
| F_INT_03 (agg × liquidity) | 0.061 (3.18) | −0.004 (−0.46) | −0.010 | 0.007 | Confirmed Artifact |
| F_INT_04 (foreign × liquidity) | 0.073 (6.41) | −0.005 (−0.04) | — | — | Confirmed Artifact |
| F_INT_05 (foreign × volatility) | 0.065 (3.22) | −0.011 (−1.34) | −0.009 | −0.014 | Confirmed Artifact |
| F_INT_06 (foreign × size) | 0.037 (2.74) | −0.002 (−0.28) | −0.004 | 0.0001 | Confirmed Artifact |
| F_INT_07 (foreign × momentum) | 0.056 (3.23) | 0.0004 (0.04) | 0.017 | −0.025 | Confirmed Artifact |

## Table 6 — Multiple Testing Summary

56 tests total. 13 significant at raw p<0.05. **9 survive Benjamini-Hochberg FDR at q<0.10** (full list in `multiple_testing_register.csv`), of which 3 (F_INT_01, F_INT_03, F_INT_07 raw IC) are independently confirmed artifacts by Table 5 — direct evidence that FDR survival is necessary but not sufficient.
