# EVIDENCE_COMPLETION_CRITERIA_v0.1.md

Definition-of-Done per KOM type, not a schema. Deliberately not uniform — each type's requirements follow from what that type actually claims epistemically, reusing concepts already established (Maturity from Classification, the factor-zoo/overfitting concern already named in the Knowledge Base itself via C49/C50/C51, Standard's authority-by-issuance already distinguished from Theory's authority-by-validation).

## ECC by KOM Type

| Type | Min Evidence | Primary Requirement | Secondary Requirement | Triangulation Requirement | Completion Rule |
|---|---|---|---|---|---|
| **Theory** | 3 | ≥1 originating Primary (≥2 if co-discovered, e.g. Sharpe+Lintner for CAPM) | ≥1 Secondary | ≥2 independent authors/groups across all sources; **if Maturity = "contested," must include a critical/opposing source, not only supportive ones** | Count + independence + contested-source rule (if applicable) all met |
| **Model** | 3 | ≥1 originating Primary | Recommended ≥1 empirical/Dataset source | At least one source must be empirical/data-based, not purely derivational — a Model's claim is fundamentally "does this work," not just "is this logically derived" | Originating source + empirical validation both present |
| **Factor** | 3 | ≥1 originating Primary | ≥1 independent replication/out-of-sample study | **Must include independent replication or extension, not just the discovery paper** — this is the strictest requirement in the table, deliberately, because Factors are specifically prone to the replication-failure risk the KB's own Overfitting/Look-Ahead Bias/Survivorship Bias concepts warn about | Originating + independent replication both present |
| **Metric** | 2 | ≥1 Primary (formalizing source) | ≥1 Secondary (practitioner/adoption confirmation) | Secondary must be from a different author than Primary | Both present and independent |
| **Concept** | 2 | ≥1 Primary (originating/definitional source) | ≥1 Secondary (independent corroborating reference) | Primary and Secondary from different authors | Both present and independent |
| **Procedure** | 2 | ≥1 foundational Primary | ≥1 modern Secondary | Secondary should postdate Primary by a meaningful margin — confirms the procedure hasn't been superseded | Both present |
| **Framework** | 1 | Not required (often unavailable — many Frameworks originate as practitioner tools, not academic publications) | ≥1 Secondary (standard textbook/practitioner reference) | Not required | ≥1 Secondary confirming standard/accepted use |
| **Formula** | 1 | ≥1 Primary, **may be inherited** from the parent Theory/Model/Metric it formalizes | Not required | Not required — inherits parent's triangulation | Linked to a Primary source, own or inherited |
| **Assumption** | 1 | ≥1 Primary, **may be inherited/shared** from a dependent Theory/Model | Not required | Not required | Linked to a Primary source, own or shared |
| **Standard** | 1 | ≥1 Primary — **must be the Official Standard document itself**, not a secondary discussion of it | Optional | Replaced by a **Currency Check**: is this the current, effective version? Multiple "independent" sources don't strengthen a Standard's validity the way they would a Theory — there is only one authoritative source, the issuing body | Official Standard cited + confirmed current |
| **Pattern** | 1 | ≥1 Primary observational source | Not required while Maturity = Provisional | **Waived at Provisional maturity; required at Theory-equivalent strength if Maturity is upgraded beyond Provisional** | 1 source sufficient for Provisional status; promotion requires meeting Theory's bar |

Two types deliberately don't fit the "more evidence = more rigor" pattern: **Standard** (authority is institutional, not triangulated — currency matters more than independence) and **Pattern** (the honest move for a low-confidence type is to let its Maturity flag carry the epistemic humility, not force premature over-sourcing).

## Evidence Review Workflow

```
Knowledge → Attach Evidence → ECC Check → Triangulation → Approval → Publish
                  ↑______________________|         |
                  (fails ECC or Triangulation loops back, not force-published)
```

1. **Knowledge** — object already exists, KOM-compliant.
2. **Attach Evidence** — Evidence objects created/identified, linked via `grounded-by`.
3. **ECC Check** — mechanical: does the count and tier mix meet this type's minimums?
4. **Triangulation** — judgment, not mechanical: are sources actually independent (different authors/institutions), and for Theory/Factor, is genuine corroboration or contestation represented, not just volume?
5. **Approval** — human confirmation gate. Same principle as Invariant #8 (no Automation may create/modify Knowledge without human confirmation) — Evidence completion gets the same standard, not a lighter one.
6. **Publish** — only now does the object count as ECC-Complete in the Dashboard.

Failing step 3 or 4 returns to step 2, not to a forced pass.

**No ADR required.** This is operational quality policy — same category as the Relationship Model's Evidence Threshold criteria, which also didn't touch Frozen Architecture/KOM/Classification/Evidence Domain.

## Dashboard, expanded to four dimensions

Coverage, Quality, and Diversity are unchanged from EVIDENCE_COVERAGE_DASHBOARD.md. **Completeness (ECC)** is new: the share of evidence-bearing objects whose evidence actually meets *their type's* Definition-of-Done, not just "has something attached."

## Informal sanity check against Evidence Pilot v0.1 — not the formal v0.2 validation

You asked for that as a separate, later exercise, and I'm not substituting for it. But running the 20 already-piloted objects against ECC costs nothing and tells us whether the bar is even in a sane range before committing to it:

**6 of 20 pass: PR02 (DCF), S01 (IFRS), S03 (CFA Code), A01 (Frictionless Markets), F01 (CAPM Equation), FR01 (DuPont).** All either had Primary+Secondary from independent authors, or fell under Standard/Formula/Assumption's lighter, inheritance-aware rules.

**14 of 20 fail, and the pattern is informative, not random:**
- Every Theory in the pilot fails — T03 and T06 and T09 have only 1 source each (below Min 3 outright); T05 has 2 sources but both by the same authors (Modigliani & Miller both times — fails independence); T01 has 3 sources but none contest CAPM despite its own Maturity tag reading "contested"; T02 has 2 of the required 3, though its Secondary (Malkiel's explicit "and Its Critics" piece) is the one case that would genuinely satisfy the contested-source rule if the count were met.
- Both Models fail on count (2 of 3) and M02 additionally lacks any empirical/Dataset source.
- Both Factors fail on count alone (2 of 3) — worth noting FA03's Secondary (Asness et al. 2013) is a genuine independent replication, exactly what the triangulation rule wants, it's just one source short.
- ME01 Sharpe Ratio fails triangulation outright — both its sources are Sharpe himself.
- C01 Risk has 2 Primary sources but zero Secondary — right count, wrong tier mix.

This isn't a sign the pilot was low-quality — it's a sign ECC is a real bar, not a rubber stamp, which is what "Research Grade" has to mean if it's going to mean anything. Whether the specific numbers (Min 3 for Theory, independence-of-authors for Metric) are calibrated correctly is exactly the question the formal Evidence Pilot v0.2 should answer — this check just confirms the bar isn't vacuous.

**Completeness (ECC) dashboard reading right now:** 6/20 piloted objects (30%), 6/299 of the full Knowledge Base (2.0%).
