# RP-001 Multiple Testing Register (Milestone 1C-R, Part 5)

Full inventory: 56 tests spanning Milestone 1C's feature×horizon IC tests (44), stability/regime tests, structural-break tests, and interaction-incremental tests. Benjamini-Hochberg FDR correction applied at α=0.10. Full data in `multiple_testing_register.csv` — every test reported, not a filtered selection of the significant ones.

## Headline numbers

- **13 of 56 tests significant at raw p<0.05**
- **9 of 56 survive BH-FDR correction at q<0.10**

## The 9 that survive correction

| Test | t_NW | Raw p | q-value (BH) |
|---|---|---|---|
| F_INST_01 yearly stability (2024 vs 2026) | 3.41 | 0.0006 | 0.027 |
| F_INST_01 low-vol vs. high-vol regime | 3.19 | 0.0014 | 0.027 |
| F_INT_03 flow×liquidity, t+5 | 3.18 | 0.0015 | 0.027 |
| F_INT_03 flow×liquidity, t+2 | 2.91 | 0.0036 | 0.051 |
| F_INST_01 foreign, t+5 | 2.74 | 0.0061 | 0.065 |
| F_INST_01 foreign, t+2 | 2.66 | 0.0079 | 0.065 |
| F_INT_03 flow×liquidity, t+3 | 2.62 | 0.0087 | 0.065 |
| F_INT_01 flow×momentum, t+5 | 2.57 | 0.0101 | 0.065 |
| F_INST_01 structural break (permutation-corrected sup-Wald) | 3.45 | 0.0105 | 0.065 |

## The finding that matters most here: statistical survival ≠ genuine effect

**F_INT_03 (flow×liquidity) and F_INT_01 (flow×momentum) both survive FDR correction — the purely statistical bar — but were independently shown to be substantially artifacts** by other tests in this milestone and Milestone 1C+: F_INT_03's raw IC lost 75% of its magnitude under sector-neutralization (Milestone 1C); F_INT_01/F_INT_07's incremental IC collapsed to ~0 (and sign-flipped post-break) once properly residualized against both constituent main effects (this milestone, Part 4). **Passing multiple-testing correction is necessary but not sufficient — it rules out "found by chance from searching too many tests," but says nothing about "explained away by a simpler additive mechanism."** Both checks are needed together; neither alone is enough, and this register is the direct evidence that they can disagree.

**F_INST_01_foreign and its structural break are the only findings in this entire research program that survive both the FDR correction and the mechanism-level scrutiny (residualization, neutralization) applied elsewhere in this milestone** — and even those carry the break-interval and regime-conditionality qualifications documented in the other four files.

## What did NOT survive, reported without cherry-picking

47 of 56 tests did not survive FDR correction, including F_INST_03_dealer_self (t+5, raw p=0.019, q=0.10 — right at the edge), most F_INST_02/04/09 horizons (never close to significant at any stage), and the majority of individual feature×horizon combinations tested in Milestone 1C. These are reported in full in the CSV, not omitted because they're uninteresting.
