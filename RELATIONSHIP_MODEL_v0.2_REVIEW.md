# RELATIONSHIP_MODEL_v0.2_REVIEW.md

Based on knowledge_base_v0.2.psv (302 objects, 233 edges), after fixing two data bugs found during this review: a malformed row (M12 — a missing field separator had misfiled its relationship to M03 into the Implements column instead of References) and a content mismatch (PR35 Anti-Money Laundering Screening was linked to SEC Reg FD, which is about fair disclosure, not AML — redirected to FATCA/S16). Neither fix reflects a relationship-model problem; both were authoring errors, corrected before this review's numbers were computed.

---

## evaluated-by

1. **Usage:** 12 (up from 4 in v0.1)
2. **Type distribution:** 100% Factor→Metric (12/12), and every single instance targets the same Metric (Information Coefficient). No other type-pair tested despite tripling the object count.
3. **Semantic consistency:** Perfectly consistent — every instance means "this Factor's quality is assessed via IC."
4. **Validity-critical:** No — a weak-performing Factor is still a well-formed object.
5. **Cycle allowed:** Yes (references family).
6. **Interchangeable with existing relations:** No — distinct from depends-on (construction) and generic references.
7. **Recommendation: Adopt**, scope remains Factor→Metric specifically. 12/12 consistency is strong, but it is still evidence for one type-pair, not a general pattern — do not extend to Model/Procedure without separate evidence.

## extends — adopted, but not as clean as it looked

1. **Usage:** 11 (up from 2)
2. **Type distribution:** Model→Theory (3), Model→Model (7), Theory→Theory (1) — spans 3 pairs now.
3. **Semantic consistency: not uniform.** Re-examining each instance individually surfaced real problems:
   - **Clean "extends" (preserves + adds):** M01→T01 (Fama-French 3F extends CAPM), M04→M01 (5F extends 3F), M10→M01 (Carhart extends 3F with momentum), M15→T01 (CAPM Int'l extends CAPM), M23→M05 (Ho-Lee extends Vasicek), M24→M23 (BDT extends Ho-Lee). **6 of 11.**
   - **Likely mistagged — should be `implements`, not `extends`:** M11→T04 (Arbitrage Pricing Model is the direct formal expression of its *own* Arbitrage Pricing Theory, not an extension of an adjacent theory the way Fama-French extends CAPM). This is the same relationship the Procedure→Standard cases capture (a concrete object formalizing/operationalizing an abstract one) — recommend retagging as `implements`, which also gives implements a second, structurally different type-pair (Model→Theory) beyond Procedure→Standard.
   - **Possibly `revises`, not `extends`:** M06→M05 (Cox-Ingersoll-Ross doesn't just add to Vasicek — it changes the core diffusion term specifically to prevent negative rates, a structural fix, not an addition). This may be the first real `revises` instance across both seeds.
   - **Doesn't fit either — a third, unnamed pattern:** M08→M02 (Binomial Option Pricing is a different computational method for the *same* problem Black-Scholes solves, not built on top of it — historically the two converge in the limit but neither extends the other). Possibly M20→M08 (Real Options applying binomial methodology to a new domain) is a second instance of the same pattern.
   - **Possible direction error:** T24→T02 (Random Walk Theory historically *precedes* and is generalized by EMH — the extends arrow may be backwards).
4. **Validity-critical:** Yes for the clean 6 — if the extended object is invalidated, so is the extension.
5. **Cycle allowed:** No — confirmed no cycles in current data, must stay enforced.
6. **Interchangeable with depends-on:** No, for the clean cases — they carry lineage information depends-on lacks.
7. **Recommendation: Adopt `extends`, but only for the 6 verified-clean instances.** The other 5 aren't evidence against extends — they're evidence that **one candidate relationship undersold what the data needed.** Three follow-on actions, not blocking adoption: retag M11→T04 as `implements`; treat M06→M05 as a `revises` candidate (see below); name the Binomial/Black-Scholes pattern as a new candidate (see below) rather than force-fitting it into extends.

## implements — your initial direction confirmed, with the fixes verified

1. **Usage:** 8 confirmed Procedure→Standard, +1 recommended retag from extends (M11→T04) = 9, spanning **2 type-pairs**.
2. **Type distribution:** Procedure→Standard is confirmed as the dominant/canonical pairing (8/9). Model→Theory (the retagged case) is a second, structurally distinct pairing that fits the same underlying semantic (concrete object formalizes/operationalizes an abstract one).
3. **Semantic consistency:** 7 of 8 original instances are clean (IFRS×3, GIPS, MiFID II, CFA Code×2). One (PR35→S07) was a genuine content mismatch, now corrected to PR35→S16.
4. **Validity-critical: Yes.** If a Standard is revised, a Procedure implementing the old version becomes non-compliant — that's a real validity failure, not just staleness. This confirms implements' original placement as a depends-on specialization from Stage 2.1 was correct.
5. **Cycle allowed:** No, consistent with depends-on family.
6. **Interchangeable with depends-on:** No — implements carries "formalizes/operationalizes an abstract source," which plain depends-on doesn't distinguish from ordinary structural dependency.
7. **All three of your verification conditions hold: majority of the 9 uses share one semantic, Procedure→Standard is confirmed canonical, a second reasonable pairing exists (Model→Theory), and the difference from depends-on is clearly statable (compliance/formalization vs. general structural dependency).**

**Recommendation: implements moves from Dormant to Adopted.** No KOM change required — it was already in the Frozen relationship vocabulary since Stage 2.1 (ADR-036); this is activation with evidence, not a new addition.

## formalized-by (Theory→Formula)

1. **Usage: still 1** (T01→F01, CAPM→CAPM Equation) — unchanged despite Theory count going 5→25.
2. This is suspicious, not just "still insufficient evidence." T22 (Fisher Effect) has a directly corresponding Formula object already in the seed (F27, Fisher Equation) that it doesn't reference — an authoring gap, not proof the pairing is rare. Likely several of the 20 new Theories have the same gap.
3–6: unchanged from v0.1 assessment.
7. **Recommendation: Defer, but flag as a remediation target** rather than passively waiting for organic evidence — wire T22→F27 (and check the other new Theories for the same gap) before re-evaluating.

## revises

1. **Usage: 0 confirmed, 1 candidate** (M06→M05, pending the extends retag above).
2. Previously rejected outright (0 instances in v0.1). Downgrading that to a firmer rejection would have been wrong — the evidence just hadn't arrived yet.
7. **Recommendation: upgrade from Rejected to Proposed.** One real candidate now exists. Still below the 2-instance threshold — needs either a second instance or an explicit decision to reclassify M06→M05 before Adopt.

## New candidate surfaced by this review: alternative-to / parallel-method

1. **Usage: 1–2** (M08→M02 confirmed; M20→M08 possibly the same pattern).
2. Two computational approaches solving the same problem without one building on the other (Binomial vs. Black-Scholes for option pricing).
3. Not validity-critical in the depends-on sense — invalidating one doesn't invalidate the other, they're independent.
4. Direction is genuinely ambiguous (which is symmetric, unlike extends) — this alone is a reason it can't simply be folded into extends.
7. **Recommendation: Proposed**, below evidence threshold (needs ≥2 clean instances and doesn't yet have a settled direction convention). Watch for more instances rather than naming it prematurely.

---

## Updated Relationship Model status

| Relationship | Status change |
|---|---|
| evaluated-by | Adopted (unchanged) |
| extends | Adopted, scope narrowed to 6 verified instances; 3 follow-ups spun out |
| **implements** | **Dormant → Adopted** |
| formalized-by | Deferred (unchanged), remediation target identified |
| revises | Rejected → Proposed (1 candidate instance) |
| alternative-to (new) | Proposed |

RELATIONSHIP_MODEL_v0.1_DRAFT remains **Draft** — this review changes candidate statuses in the register, it does not itself constitute the v1.0 freeze.
