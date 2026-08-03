# RP-001 Phase 2A.4: Confirmatory Results

**Date:** 2026-08-03. Full-universe confirmatory sample: **1,462 stocks, 3,934,274 panel rows** (coverage-gate-passing subset of the 5,718,238-row confirmatory dataset). All tests run exactly as pre-registered (`research/RP001_CONFIRMATORY_HYPOTHESES.md`), judged by pre-committed criteria (`research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`), methods locked before execution (Spearman rank IC, Newey-West t (5 lags), cross-sectional OLS residualization, Benjamini-Hochberg FDR α=0.10 applied jointly across all 16 primary test statistics). Full machine-readable output: `rp001_data/phase2a/processed/rp001_confirmatory_test_results.json`. Code: `research/rp001_phase2a_confirmatory_tests.py`.

**No methodology was changed after seeing these results.** The pipeline (panel construction → features → coverage gate → tests) was built and locked before any hypothesis test was run, per the Deviation Policy's before/after discipline. Several results below contradict the exploratory-phase findings; they are reported as computed, not adjusted.

## H-C1: Pre-break positive predictive power

| Horizon | n (days) | Mean IC | Median IC | NW t | 95% CI | Raw p | BH-FDR q |
|---|---|---|---|---|---|---|---|
| t+1 | 3,283 | 0.0000 | -0.0005 | 0.036 | [-0.0024, 0.0025] | 0.971 | 0.977 |
| t+3 | 3,283 | 0.0016 | 0.0020 | 1.190 | [-0.0010, 0.0043] | 0.234 | 0.468 |
| t+5 | 3,283 | 0.0011 | 0.0032 | 0.735 | [-0.0018, 0.0039] | 0.462 | 0.740 |

**No horizon reaches NW t>1.96 or survives BH-FDR at q<0.10.** Mean IC is statistically indistinguishable from zero at all three horizons — a factor of roughly 40-70× smaller than the exploratory study's pre-break mean IC of 0.052 (t=3.99, Milestone 1C-R). This is not a case of the effect surviving but weakening; it does not clear even the loosest significance bar at any horizon.

## H-C2: Post-break null effect

| Horizon | n (days) | Mean IC | NW t | 95% CI | Raw p | BH-FDR q |
|---|---|---|---|---|---|---|
| t+5 | 197 | 0.0021 | 0.395 | [-0.0084, 0.0126] | 0.693 | 0.853 |

`|mean IC| < 0.01` and `|NW t| < 1.96` — both conditions for Replicated are met. **Interpretive caveat, stated plainly:** this criterion is far less informative than intended, because H-C1 found no significant pre-break effect either — there is no established effect for the post-break period to have "lost." A null-vs-null comparison is not the same confirmatory signal as a null that follows a genuinely significant pre-break effect.

## H-C3: Liquidity conditionality (t+5, full sample)

| Tercile | n (days) | Mean IC | NW t | Raw p | BH-FDR q |
|---|---|---|---|---|---|
| Illiquid | 3,471 | 0.0041 | 1.827 | 0.068 | 0.155 |
| Mid | 3,471 | 0.0093 | **5.411** | 6.3e-08 | **2.0e-07** |
| Liquid | 3,471 | -0.0001 | -0.029 | 0.977 | 0.977 |

Direction replicates in the broad sense (Illiquid and Mid both exceed Liquid; Liquid is not significant), but the pattern is asymmetric — Mid is the only tercile clearing both NW t>1.96 and BH-FDR q<0.10; Illiquid is directionally positive but does not independently reach significance (t=1.83, q=0.155). The exploratory study found "Illiquid ≈ Mid > Liquid" (roughly equal strength); the full-universe result is "Mid ≫ Illiquid > Liquid."

## H-C4: Volatility-regime × break-period double-sort (t+5)

| Cell | n (days) | Mean IC | NW t | Raw p | BH-FDR q |
|---|---|---|---|---|---|
| Low-vol & Pre-break | 1,692 | 0.0016 | 0.789 | 0.430 | 0.740 |
| Low-vol & Post-break | 46 | -0.0043 | -0.448 | 0.654 | 0.853 |
| High-vol & Pre-break | 1,581 | 0.0002 | 0.098 | 0.922 | 0.977 |
| High-vol & Post-break | 151 | 0.0041 | 0.660 | 0.509 | 0.741 |

**None of the four cells is statistically significant.** The defining asymmetry the hypothesis depends on — Low-vol & Pre-break must remain significant (exploratory: t=3.99) while Low-vol & Post-break collapses — is not observed, because the Low-vol & Pre-break cell itself is not significant at full-universe scale (t=0.789). There is no significant effect left to test for break-conditionality.

## H-C5: Interaction-feature residualization (t+5, cross-sectional OLS against both constituents)

| Feature | Raw IC (t+5) | Raw t | Residual IC (t+5) | Residual NW t | BH-FDR q | Survives q<0.10? |
|---|---|---|---|---|---|---|
| F_INT_01 (flow×momentum) | -0.0084 | -2.77 | **0.0063** | **7.06** | 1.4e-11 | Yes |
| F_INT_03 (flow×liquidity) | -0.0103 | -5.33 | **-0.0066** | **-6.67** | 1.0e-10 | Yes |
| F_INT_04 (foreign×liquidity) | -0.0061 | -2.98 | **-0.0067** | **-6.72** | 9.8e-11 | Yes |
| F_INT_05 (foreign×volatility) | -0.0260 | -6.97 | 0.0016 | 1.99 | 0.124 | No (borderline) |
| F_INT_07 (foreign×momentum) | -0.0052 | -1.75 | **0.0065** | **7.49** | 1.1e-12 | Yes |
| F_INT_02 (flow×size) | — | — | — | — | — | **Not constructible (D-08)** |
| F_INT_06 (foreign×size) | — | — | — | — | — | **Not constructible (D-08)** |

**4 of 5 testable interactions show a statistically robust residual effect surviving both the |NW t|>1.96 bar and BH-FDR correction; a 5th (F_INT_05) is borderline on t (1.99) but misses FDR (q=0.124).** This is the opposite of the pre-registered expectation — the original study found these same interaction *forms* collapsed to near-zero, statistically indistinguishable-from-noise residuals on the 50-stock sample.

**Important magnitude caveat, reported for honest interpretation, not to soften the formal verdict:** the residual IC magnitudes here (0.0016 to 0.0067) are still 75–95% smaller than each feature's own pre-residualization raw IC (0.0052–0.0260), and an order of magnitude smaller than the raw interaction ICs reported in the exploratory mechanism analysis (0.037–0.073). The interactions are *overwhelmingly* additive, exactly as the original analysis concluded — but at full-universe scale (3,460+ trading days, ~1,400+ stocks per cross-section vs. the exploratory sample's ~50 stocks and ~500 days), the statistical power is great enough to detect that the small residual is not *exactly* zero. Whether a mean IC of 0.006 with t≈7 constitutes a "genuine interaction effect" in any economically meaningful sense is a separate question from whether it is statistically distinguishable from zero — and by the pre-registered criterion (a pure significance test), it is.

## Multiple-testing summary

16 primary test statistics, Benjamini-Hochberg α=0.10, applied jointly. **5 of 16 survive:** H-C3 Mid tercile, and 4 of the 5 testable H-C5 interaction residuals. Full table in the JSON output.
