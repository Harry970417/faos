# RP-001 Results Tables v0.2

Confirmatory-phase tables. Exploratory-phase tables (`archive/RP001_RESULTS_TABLES_v0.1.md`) preserved unchanged as the historical record — not reproduced here. Source: `rp001_data/phase2a/processed/rp001_confirmatory_test_results.json`.

## Table 1 — H-C1: Pre-break F_INST_01 IC by horizon

| Horizon | n (days) | Mean IC | Median IC | NW t | 95% CI | BH-FDR q |
|---|---|---|---|---|---|---|
| t+1 | 3,283 | 0.0000 | -0.0005 | 0.036 | [-0.0024, 0.0025] | 0.977 |
| t+3 | 3,283 | 0.0016 | 0.0020 | 1.190 | [-0.0010, 0.0043] | 0.468 |
| t+5 | 3,283 | 0.0011 | 0.0032 | 0.735 | [-0.0018, 0.0039] | 0.740 |

**Exploratory-phase comparison (v0.1 Table 1):** t+5 mean IC 0.029 (t=2.74) — confirmatory t+5 mean IC is 27× smaller, not significant.

## Table 2 — H-C2: Post-break F_INST_01 IC (t+5)

| n (days) | Mean IC | NW t | 95% CI | BH-FDR q |
|---|---|---|---|---|
| 197 | 0.0021 | 0.395 | [-0.0084, 0.0126] | 0.853 |

## Table 3 — H-C3: Liquidity Conditionality (t+5, full sample)

| Tercile | n (days) | Mean IC | NW t | BH-FDR q |
|---|---|---|---|---|
| Illiquid | 3,471 | 0.0041 | 1.827 | 0.155 |
| Mid | 3,471 | 0.0093 | 5.411 | 2.0e-07 |
| Liquid | 3,471 | -0.0001 | -0.029 | 0.977 |

**Exploratory-phase comparison (v0.1 Table 4, raw row):** Illiquid 0.034 (t=1.94), Mid 0.031 (t=1.94), Liquid 0.010 (t=0.63) — confirmatory magnitudes are ~5-8× smaller across all three terciles; the exploratory "Illiquid ≈ Mid" symmetry does not reproduce.

## Table 4 — H-C4: Volatility × Break Double-Sort (F_INST_01, t+5)

| Cell | n (days) | Mean IC | NW t | BH-FDR q |
|---|---|---|---|---|
| Low-vol & Pre-break | 1,692 | 0.0016 | 0.789 | 0.740 |
| Low-vol & Post-break | 46 | -0.0043 | -0.448 | 0.853 |
| High-vol & Pre-break | 1,581 | 0.0002 | 0.098 | 0.977 |
| High-vol & Post-break | 151 | 0.0041 | 0.660 | 0.741 |

**Exploratory-phase comparison (v0.1 Table 3):** Low-vol & Pre-break 0.069 (t=3.99) — confirmatory value is 43× smaller and not significant. None of the four cells replicate significance.

## Table 5 — H-C5: Interaction Feature Residualization (t+5)

| Feature | Raw IC (t) | Residual IC (t) | BH-FDR q | Exploratory raw IC (v0.1) | Verdict |
|---|---|---|---|---|---|
| F_INT_01 (agg × momentum) | -0.0084 (-2.77) | **0.0063 (7.06)** | 1.4e-11 | 0.044 (2.57) | Small residual survives — Not an exact artifact |
| F_INT_03 (agg × liquidity) | -0.0103 (-5.33) | **-0.0066 (-6.67)** | 1.0e-10 | 0.061 (3.18) | Small residual survives — Not an exact artifact |
| F_INT_04 (foreign × liquidity) | -0.0061 (-2.98) | **-0.0067 (-6.72)** | 9.8e-11 | 0.073 (6.41) | Small residual survives — Not an exact artifact |
| F_INT_05 (foreign × volatility) | -0.0260 (-6.97) | 0.0016 (1.99) | 0.124 | 0.065 (3.22) | Borderline — fails FDR |
| F_INT_07 (foreign × momentum) | -0.0052 (-1.75) | **0.0065 (7.49)** | 1.1e-12 | 0.056 (3.23) | Small residual survives — Not an exact artifact |
| F_INT_02 (agg × size) | — | — | — | 0.023 (1.68) | Not constructible (D-08) |
| F_INT_06 (foreign × size) | — | — | — | 0.037 (2.74) | Not constructible (D-08) |

Every residual IC magnitude is 75-95% smaller than the exploratory-phase raw IC for the same feature — the interactions are overwhelmingly additive, as originally found, but the residual is not exactly zero at full-universe sample size.

## Table 6 — Joint Multiple Testing Summary

16 primary confirmatory test statistics, Benjamini-Hochberg α=0.10. **5 of 16 survive:** H-C3 Mid tercile, and 4 of 5 testable H-C5 interaction residuals (all except F_INT_05).
