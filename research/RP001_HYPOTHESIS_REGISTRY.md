# RP001 Hypothesis Registry

A single canonical, machine-checkable-by-eye table of everything about H-C1–H-C5: what was tested, how, and what happened. This document is **new and additive** — it aggregates information that already exists in five locked/results documents (`research/RP001_CONFIRMATORY_HYPOTHESES.md`, `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`, `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`, `research/RP001_MULTIPLE_TESTING_REGISTER.md`) into one registry format; it does not change any hypothesis wording, threshold, method, or reported number in those documents. Standard errors shown below are derived (`SE = effect / NW t`, the algebraic inverse of how each t-statistic itself was computed) — they are not independently re-estimated.

**Classification correction (2026-09-13):** an earlier downstream summary (in the "05 FAOS" admissions portfolio document) described H-C5 as "secondary/exploratory" and H-C1–H-C4 as "core confirmatory." **That distinction does not exist in the locked source documents.** `research/RP001_PHASE2A_PROTOCOL_LOCK.md` states plainly: "the five hypotheses H-C1–H-C5 exactly as stated" are locked together; `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`'s multiple-testing summary applies Benjamini-Hochberg **jointly across all 16 primary test statistics spanning all five hypotheses** — H-C5 is not held to a separate or lesser standard. Per source, **all five (H-C1–H-C5) are Core, Confirmatory hypotheses.** H-C5 differs from H-C1–H-C4 only in *sample-construction mechanics* — it tests interaction features that don't use the same 80%-coverage liquidity/institutional-data gate H-C1–H-C4's sample is built on, and 2 of its 7 interaction features are untestable at full-universe scale for a data-availability reason (Deviation D-08), not a design choice to downgrade its rigor. This registry reflects the corrected classification; the portfolio and evidence-matrix documents are being updated to match (see final sync note at bottom).

## Quantitative definitions of verdict labels

From `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` — reproduced here so "weak replication" (弱複現) and "partial replication" (部分複現) have one unambiguous, checkable definition instead of being read as informal adjectives:

| Verdict | Operational definition (applies identically across all 5 hypotheses) |
|---|---|
| **Replicated** | Direction matches the original finding, and the primary significance measure (Newey-West t, BH-FDR q) clears the pre-specified threshold at the pre-specified horizon(s). |
| **Replicated (with caveat)** — informal gloss "weak replication" (弱複現) | Meets the letter of "Replicated" above, but the pre-registered comparison it was meant to provide is weakened by a *different* hypothesis's non-replication (specifically: H-C2's null-vs-null problem once H-C1 failed — see H-C2 below). Not a separate formal verdict tier in the Acceptance Criteria; a caveat attached to a Replicated verdict. |
| **Partially Replicated** — informal gloss "partial replication" (部分複現) | Direction matches but significance is inconsistent across horizons or measures (e.g., significant NW t but FDR q misses, or significant at some but not all of t+1/t+3/t+5; or, for multi-cell hypotheses, only some cells/terciles clear the bar). |
| **Not Replicated** | Direction contradicts the original finding, or the effect is null where the original found a real effect (and vice versa). |
| **Inconclusive** | Insufficient sample size or a required data field is unavailable for the relevant sub-group — reported as its own outcome, never folded into "Not Replicated." |

---

## H-C1 — Pre-break positive predictive power

| Field | Value |
|---|---|
| Hypothesis ID | H-C1 |
| Classification | **Core, Confirmatory** |
| Economic theory | Foreign institutional investors possess an information/processing advantage; their net buying/selling flow (F_INST_01) should positively predict short-horizon cross-sectional stock returns before the mechanism breaks down. |
| Estimand | Cross-sectional Spearman Rank IC between F_INST_01 and forward return, pre-break period, at t+1/t+3/t+5. |
| Sample | Full-universe confirmatory panel, pre-break subset: 3,283 trading days per horizon; 1,462 stocks (coverage-gate-passing subset of 2,096 stocks with any institutional-flow record, out of 2,255 acquired). |
| Horizon | t+1, t+3, t+5 |
| Success criterion (pre-specified) | **Replicated:** positive IC at all 3 horizons, NW t>1.96 at ≥2 of 3, BH-FDR q<0.10 at t+5. **Partially Replicated:** positive direction at ≥2/3 horizons but full bar not met. **Not Replicated:** negative/null IC at the majority of horizons. |
| Multiple-testing rule | Benjamini-Hochberg FDR, α=0.10, applied jointly across all 16 primary test statistics (H-C1–H-C5 combined). |

| Horizon | Effect (mean IC) | SE (derived) | NW t | Raw p | 95% CI | BH-FDR q | vs. threshold |
|---|---|---|---|---|---|---|---|
| t+1 | +0.0000 | 0.00125 | 0.036 | 0.971 | [-0.0024, 0.0025] | 0.977 | t<1.96, q>0.10 — fails |
| t+3 | +0.0016 | 0.00135 | 1.190 | 0.234 | [-0.0010, 0.0043] | 0.468 | t<1.96, q>0.10 — fails |
| t+5 | +0.0011 | 0.00150 | 0.735 | 0.462 | [-0.0018, 0.0039] | 0.740 | t<1.96, q>0.10 — fails |

**Decision:** Not Replicated. No horizon clears NW t>1.96 or BH-FDR q<0.10; mean IC ≈40–70× smaller than the exploratory pre-break IC (0.052, t=3.99, Milestone 1C-R). **Status: Closed, per locked verdict (`research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`).**

---

## H-C2 — Post-break null effect

| Field | Value |
|---|---|
| Hypothesis ID | H-C2 |
| Classification | **Core, Confirmatory** |
| Economic theory | The predictive mechanism in H-C1, if real, should have broken down after the identified structural break (point estimate 2025-09-25) — e.g. due to crowding, regulatory change, or arbitrage. |
| Estimand | Cross-sectional Spearman Rank IC between F_INST_01 and forward return, post-break period, at t+5. |
| Sample | Full-universe confirmatory panel, post-break subset: 197 trading days. |
| Horizon | t+5 (the horizon strongest in the original exploratory study) |
| Success criterion (pre-specified) | **Replicated:** \|mean IC\|<0.01 AND NW \|t\|<1.96. **Partially Replicated:** small-but-marginally-significant or not-small-but-not-significant (mixed). **Not Replicated:** IC clearly significant and comparable in magnitude to the pre-break effect. |
| Multiple-testing rule | Same joint BH-FDR (α=0.10, 16 statistics) as H-C1. |

| Horizon | Effect (mean IC) | SE (derived) | NW t | Raw p | 95% CI | BH-FDR q | vs. threshold |
|---|---|---|---|---|---|---|---|
| t+5 | +0.0021 | 0.00536 | 0.395 | 0.693 | [-0.0084, 0.0126] | 0.853 | \|IC\|<0.01 and \|t\|<1.96 — meets letter of criterion |

**Decision:** **Replicated (with caveat) — informal gloss "weak replication" (弱複現).** Meets the letter of the criterion, but this is a **null-vs-null comparison**: H-C1 (the pre-break effect H-C2 is testing the *disappearance* of) itself was Not Replicated, so there was no established pre-break effect for the post-break period to have lost. A pre-registered "the effect breaks down" test is far weaker evidence when the antecedent effect never appeared in the first place. **Status: Closed, per locked verdict — reported with this caveat exactly as constructed, not upgraded or downgraded.**

---

## H-C3 — Liquidity conditionality

| Field | Value |
|---|---|
| Hypothesis ID | H-C3 |
| Classification | **Core, Confirmatory** |
| Economic theory | An information-advantage effect should be strongest where prices are least efficient — illiquid/mid-liquidity names — and weakest/absent in liquid, heavily-arbitraged names. |
| Estimand | Cross-sectional Spearman Rank IC between F_INST_01 and forward return, by liquidity tercile (20-day rolling average trading value), full sample. |
| Sample | Full sample, 3,471 trading days per tercile. |
| Horizon | t+5 |
| Success criterion (pre-specified) | **Replicated:** Illiquid and Mid both show higher mean IC and higher NW t than Liquid, with Liquid not significant. **Partially Replicated:** direction correct but not clean (only one of Illiquid/Mid clearly stronger). **Not Replicated:** Liquid shows equal or stronger IC than Illiquid/Mid. |
| Multiple-testing rule | Same joint BH-FDR (α=0.10, 16 statistics). |

| Tercile | Effect (mean IC) | SE (derived) | NW t | Raw p | BH-FDR q | vs. threshold |
|---|---|---|---|---|---|---|
| Illiquid | +0.0041 | 0.00224 | 1.827 | 0.068 | 0.155 | t<1.96, q>0.10 — directional only |
| Mid | +0.0093 | 0.00172 | **5.411** | 6.3e-08 | **2.0e-07** | clears both bars |
| Liquid | -0.0001 | 0.00345 | -0.029 | 0.977 | 0.977 | correctly null |

**Decision:** **Partially Replicated ("部分複現").** Direction is correct in the broad sense (Illiquid, Mid > Liquid; Liquid not significant), but only Mid independently clears both NW t>1.96 and q<0.10; Illiquid is directional but not significant on its own (t=1.83, q=0.155). Original exploratory pattern was "Illiquid ≈ Mid > Liquid" (roughly equal); full-universe pattern is "Mid ≫ Illiquid > Liquid" — the symmetry does not reproduce. **Status: Closed, per locked verdict.** See also Part 5 selection-robustness addendum (`research/RP001_PHASE2A_SELECTION_ROBUSTNESS.md`) for how H-C1/H-C2/H-C4 look under this same tercile split.

---

## H-C4 — Volatility effect is break-conditional, not independent

| Field | Value |
|---|---|
| Hypothesis ID | H-C4 |
| Classification | **Core, Confirmatory** |
| Economic theory | The exploratory-phase low-volatility effect was hypothesized to be an artifact of the break period, not an independent regime effect — i.e., it should disappear once break-period is controlled for. |
| Estimand | Cross-sectional Spearman Rank IC, double-sorted by volatility regime (median split) × break period, t+5. |
| Sample | 1,692 / 46 / 1,581 / 151 trading days across the four cells (see table). |
| Horizon | t+5 |
| Success criterion (pre-specified) | **Replicated:** Low-vol & Post-break shows \|mean IC\|<0.01 and NW \|t\|<1.96, while Low-vol & Pre-break remains significant. **Partially Replicated:** attenuation but not full collapse. **Not Replicated:** Low-vol & Post-break remains clearly significant. |
| Multiple-testing rule | Same joint BH-FDR (α=0.10, 16 statistics). |

| Cell | Effect (mean IC) | SE (derived) | NW t | Raw p | BH-FDR q | vs. threshold |
|---|---|---|---|---|---|---|
| Low-vol & Pre-break | +0.0016 | 0.00203 | 0.789 | 0.430 | 0.740 | not significant |
| Low-vol & Post-break | -0.0043 | 0.00960 | -0.448 | 0.654 | 0.853 | not significant |
| High-vol & Pre-break | +0.0002 | 0.00204 | 0.098 | 0.922 | 0.977 | not significant |
| High-vol & Post-break | +0.0041 | 0.00621 | 0.660 | 0.509 | 0.741 | not significant |

**Decision:** Not Replicated. The defining asymmetry requires Low-vol & Pre-break to remain significant — it does not (t=0.789) — so there is no significant effect left for break-conditionality to explain. None of the 4 cells is significant. **Status: Closed, per locked verdict.**

---

## H-C5 — No genuine interaction effects

| Field | Value |
|---|---|
| Hypothesis ID | H-C5 |
| Classification | **Core, Confirmatory** (sample-construction mechanics differ from H-C1–H-C4 — see classification correction above; this is not a rigor downgrade) |
| Economic theory | Apparent interaction effects (flow×momentum, flow×liquidity, foreign×liquidity, foreign×volatility, foreign×momentum, plus 2 size-based interactions) found in exploratory analysis were hypothesized to be additive artifacts, not genuine incremental signal, once jointly residualized against both constituent main effects. |
| Estimand | Residual cross-sectional IC (t+5) of each interaction feature after cross-sectional OLS residualization against both constituent factors. |
| Sample | Same full-universe confirmatory panel as H-C1–H-C4 for the 5 testable features; F_INT_02/F_INT_06 untestable (market cap unavailable at full-universe scale, Deviation D-08) — reported Inconclusive, not folded into the count. |
| Horizon | t+5 |
| Success criterion (pre-specified) | **Replicated:** all 7 features show residual NW \|t\|<1.96. **Partially Replicated:** 5–6 of 7 replicate. **Not Replicated:** 3 or more show genuine significant incremental IC. |
| Multiple-testing rule | Same joint BH-FDR (α=0.10, 16 statistics). |

| Feature | Raw IC | Raw t | Residual IC (effect) | SE (derived) | Residual NW t | BH-FDR q | Survives q<0.10? |
|---|---|---|---|---|---|---|---|
| F_INT_01 (flow×momentum) | -0.0084 | -2.77 | **+0.0063** | 0.00089 | **7.06** | 1.4e-11 | Yes |
| F_INT_03 (flow×liquidity) | -0.0103 | -5.33 | **-0.0066** | 0.00099 | **-6.67** | 1.0e-10 | Yes |
| F_INT_04 (foreign×liquidity) | -0.0061 | -2.98 | **-0.0067** | 0.00100 | **-6.72** | 9.8e-11 | Yes |
| F_INT_05 (foreign×volatility) | -0.0260 | -6.97 | +0.0016 | 0.00080 | 1.99 | 0.124 | No (borderline) |
| F_INT_07 (foreign×momentum) | -0.0052 | -1.75 | **+0.0065** | 0.00087 | **7.49** | 1.1e-12 | Yes |
| F_INT_02 (flow×size) | — | — | — | — | — | — | **Inconclusive — market cap unavailable (D-08)** |
| F_INT_06 (foreign×size) | — | — | — | — | — | — | **Inconclusive — market cap unavailable (D-08)** |

**Decision:** Not Replicated (4 of 5 testable interactions, ≥3 threshold met). Residual ICs (0.0016–0.0067) are 75–95% smaller than each feature's own raw IC and an order of magnitude smaller than the exploratory mechanism analysis's raw interaction ICs (0.037–0.073) — overwhelmingly additive, but statistically distinguishable from zero at full-universe sample size (~3,460 days × ~1,400+ stocks). **This is a genuine new finding requiring independent follow-up research, reported here as part of RP-001's confirmatory results — not a softer or "exploratory-tier" result.** **Status: Closed for the confirmatory verdict itself, per locked verdict; the newly-found residual interaction effect is explicitly flagged as out of scope for RP-001 (no new feature work — `PROJECT_STATUS.md` prohibits it) and is the natural candidate for a future RP-002-style study.**

---

## Overall multiple-testing summary

16 primary test statistics across H-C1–H-C5, Benjamini-Hochberg α=0.10, applied jointly (not per-hypothesis). **5 of 16 survive:** H-C3's Mid tercile, and 4 of H-C5's 5 testable interaction residuals (F_INT_01, 03, 04, 07). Full machine-readable table: `rp001_data/phase2a/processed/rp001_confirmatory_test_results.json`; register: `research/RP001_MULTIPLE_TESTING_REGISTER.md`.

## Final decision table

| ID | Decision | Status |
|---|---|---|
| H-C1 | Not Replicated | Closed |
| H-C2 | Replicated (with caveat) | Closed |
| H-C3 | Partially Replicated | Closed |
| H-C4 | Not Replicated | Closed |
| H-C5 | Not Replicated (+ new residual-interaction finding) | Closed (confirmatory verdict); new finding open for future RP-002 |

## Provenance

Built 2026-09-13 from: `research/RP001_CONFIRMATORY_HYPOTHESES.md`, `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`, `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`, `research/RP001_PHASE2A_PROTOCOL_LOCK.md`, `research/RP001_MULTIPLE_TESTING_REGISTER.md`. See `research/RP001_PHASE2A_SELECTION_ROBUSTNESS.md` for the liquidity-stratified H-C1/H-C2/H-C4 extension. Sync targets after this registry: `推甄資料最新版/04_金融專案作品集/05_FAOS_專案作品集.md` (Page 4/5), `推甄資料最新版/04_金融專案作品集/08_GRP001_研究主線整合.md`, `推甄資料最新版/00_總覽與索引/Project_Evidence_Matrix.md`, `財金專案研究報告_教授審閱版_2026/05_FAOS/`.
