# RELATIONSHIP_MODEL_v0.1_DRAFT.md

Based on: SEED_GRAPH_AUDIT_v0.1.md (knowledge_seed_v0.1.psv, 50 objects / 53 edges)

---

## Evidence Threshold for Adopting a Relationship Type (Stage 2.3 criteria — not Entry Schema fields)

1. ≥2 distinct real instances in the seed (not hypothetical)
2. Preferably spans more than one object-type pair — soft criterion; 100% coverage within a single type-pair (e.g. 4-for-4 Factor instances) can still be strong evidence
3. Semantically distinct from existing relationship types — not interchangeable
4. Direction is definable — no symmetric/ambiguous cases
5. Must state explicitly: validity-critical (joins the DAG-constrained depends-on family) or not (joins the references family, cycles permitted)
6. Must generalize beyond the single case that first surfaced it

---

## Candidate Review

### A. evaluated-by (Factor → Metric)

4/4 instances — every Factor object in the seed uses it, 100% coverage of that type-pair. Only tested against Factor→Metric; Model→Metric and Procedure→Metric were not tested (no such edges exist in the seed) — cannot confirm generalization beyond Factor.

One disambiguation surfaced during review: PR04 (Cross-Sectional IC Computation) → ME07 (IC) is a *different* relationship in disguise — the Procedure **computes/produces** the Metric, it isn't "evaluated by" it. Conflating these would be wrong. `evaluated-by` should stay scoped to "an object's quality/validity is assessed via this Metric," not "this Metric is an output of this Procedure."

Validity classification: **not validity-critical** — a poorly-performing Factor is still a well-formed Factor object, just empirically weak. Belongs in the `references` family, cycles permitted.

**Decision: Adopt** (references-family specialization). Scope explicitly to Factor→Metric for v0.1; extending to Model/Procedure needs its own evidence.

### B. extends vs. revises

2 instances, both `extends`: Fama-French 3-Factor extends CAPM (keeps the market-beta term, adds two factors — nothing removed or contradicted); Fama-French 5-Factor extends 3-Factor (same pattern — adds two more factors, keeps the original three). Both instances span *different* type-pairs (Model→Theory, Model→Model), which is a stronger signal than 2 instances of the same pair would be.

Zero instances of `revises` (something that modifies or replaces part of an existing object) exist anywhere in the seed. Splitting `extends`/`revises` now would be speculative — inventing a distinction the data hasn't produced a single example of yet. Not merging on principle either; simply reporting what's there.

Validity classification: **validity-critical** — if the extended object were invalidated, the extending object's validity is directly implicated. Joins the depends-on family; must remain acyclic (A extends B extends A is incoherent).

**Decision: Adopt `extends`** as a depends-on specialization, validity-critical. **Reject `revises` for now** — not deleted from consideration, just doesn't clear the evidence bar; watch for a genuine future instance (something that actually alters rather than adds to a prior object).

### C. Theory → Formula naming

Only 1 instance (CAPM → CAPM Equation) — fails the ≥2 threshold on its own. But the semantic argument is sound and worth recording: CAPM's *validity* doesn't hinge on the specific notation used to express it — the equation represents the theory, it doesn't structurally underpin it the way a Model's validity depends on its Formula. `depends-on` overstates the relationship; something like `formalized-by` is more accurate.

Checked for a naming collision with the Model concept: "Model" is already defined (ADR-033) as *the formalized, computable instantiation of a Theory*. A `Theory --formalized-by--> Formula` edge doesn't collapse into Model — it's a lighter, non-validity-critical link (this equation is *a* mathematical expression of the theory) versus Model's depends-on-Formula link, which *is* validity-critical (a Model without its formula isn't a Model). The two can coexist without contradiction.

**Decision: Defer.** Conceptually the strongest-argued candidate in this review, but only one real instance. Priority target for the next seed expansion — one more Theory-with-an-equation instance (e.g. Modern Portfolio Theory's variance-minimization equation) would clear the bar immediately.

### D. implements

Zero uses despite being in Frozen KOM since Stage 2.1. Checked all four suggested pairings against the actual seed:

| Pairing | Finding |
|---|---|
| Model implements Theory | **Tested and came up empty** — the one real Model→Theory edge in the seed (Fama-French → CAPM) needed `extends`, not `implements`. Meaningful negative signal, not just absence of data. |
| Procedure implements Framework | No Procedure references any Framework in this seed. No data either way. |
| Formula implements Model | Doesn't fit the existing tier structure — Formula is the more atomic, foundational object (Tier 0) that Models depend on; "Formula implements Model" would invert that relationship without a clear justification. Likely a mismatch, not just untested. |
| Standard implemented-by Procedure | Conceptually the strongest fit (a Procedure operationalizing an abstract Standard is exactly what "implements" usually means) — but **zero test coverage is structural, not incidental**: all 3 Standards are fully isolated nodes (Section 2 of the audit). This is the clearest case where absence of evidence really is just absence of data. |

**Decision: Dormant / Unvalidated** — not removed from Frozen KOM, not activated in Relationship Model v0.1. Its most promising untested pairing (Standard↔Procedure) is specifically blocked by this seed's composition, not by the concept being wrong — flagging as the top priority for a future seed expansion that actually includes compliance/standards-heavy Procedures.

---

## ADR Requirement

Checked whether any of the above amends something Frozen. **Adopting `evaluated-by` and `extends` does not require a new ADR** — ADR-036 (Frozen, part of KOM v1.0) already explicitly reserved exactly this expansion for Stage 2.3 ("supports/contradicts deferred to Stage 2.3"), so extending the relationship vocabulary here is executing that reservation, not amending it.

**One small ADR is needed**, but not for relationship content: the Decision Status vocabulary (ADR-029: Proposed / Accepted / Superseded) has no state for "evaluated, evidence inconclusive, intentionally parked" — which is exactly `implements`'s status now. Recommend:

**ADR-041** — Decision Status vocabulary extended with a fourth value: **Dormant** (evaluated, does not currently meet the Evidence Threshold, not rejected, eligible for reconsideration on new evidence). Status: proposed for your acceptance.

---

## Relationship Model v0.1 (draft)

| Relationship | Family | Validity-critical | Status |
|---|---|---|---|
| depends-on | structural | Yes (DAG) | Frozen (KOM v1.0) |
| references | structural | No | Frozen (KOM v1.0) |
| derived-from | depends-on specialization | Yes | Frozen (KOM v1.0), 1 confirmed instance |
| implements | depends-on specialization | Yes | **Dormant** (ADR-041 pending) |
| **extends** | depends-on specialization | Yes | **New — Adopted** |
| **evaluated-by** | references specialization | No | **New — Adopted**, scoped to Factor→Metric |
| formalized-by | references specialization | No | **Deferred** — needs 1 more instance |
| revises | (undefined) | — | **Rejected for now** — 0 instances |
| supports | (undefined) | — | Still deferred per original ADR-036, untouched by this audit |
| contradicts | (undefined) | — | Still deferred per original ADR-036, untouched by this audit |

Not proposing this as Frozen — draft, pending your review and the ADR-041 decision.
