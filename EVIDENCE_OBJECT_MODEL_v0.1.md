# EVIDENCE_OBJECT_MODEL_v0.1.md

Parallel to KOM (Stage 2.1), but for the `Evidence` Domain Model concept instead of `Knowledge`/`Method`. Evidence has been a Frozen, cross-cutting Architecture concept since ADR-021 (3-tier taxonomy: Primary/Secondary/Derived, plus the anti-laundering rule). This document does the same "what kinds of objects exist" work KOM did for Knowledge — it does not touch or reopen ADR-021.

## One collision caught before going further

Your list includes **Official Standard**. KOM v1.0 already has a `Standard` Knowledge Object type (S01 IFRS, S03 CFA Code, etc., already populated in the Knowledge Base). These are not the same thing and the name needs to stay distinguishable: a KOM `Standard` object is FAOS's own structured understanding of what a regulation requires; an Evidence `Official Standard` object is the literal published source document that understanding should cite (e.g., the actual IFRS 15 text issued by the IASB). Every Knowledge `Standard` object should, in the mature system, cite exactly one Evidence `Official Standard` object — this is in fact the cleanest, most natural Knowledge↔Evidence pairing in the whole model, precisely because a regulatory Standard's authority comes entirely from its official text. Keeping the name but flagging the distinction explicitly, so it doesn't get conflated later the way "Constraint" and "Status" did earlier in this project.

## Evidence Object types (v1, flat list — no sub-families)

| Type | Typical tier | Notes |
|---|---|---|
| Company Filing | Primary | 10-K, prospectus, annual report — original disclosure from the entity itself |
| Dataset | Primary | Raw price series, financial statement data, survey data |
| Official Statistics | Primary | GDP, CPI, unemployment — raw output from a statistical authority |
| Official Standard | Primary | The published regulation/standard text itself |
| Government Report | Primary or Secondary | Depends on content — a raw data release is Primary, an analytical central-bank report is Secondary |
| Journal Paper | Secondary (usually) | Interpretation/analysis of underlying data — Primary only if it's the original source reporting genuinely new proprietary data |
| Book | Secondary | Synthesizes and interprets rather than originates |

**Tier is not determined by Type.** This directly reuses the principle already established for Knowledge Classification (ADR-037: taxonomy placement is instance-level, never type-level) — a Government Report or Journal Paper can legitimately be Primary or Secondary depending on its actual content, not its category. No new principle invented here, just the same rule applied one level over.

**Not adding, and why:** *Working Paper/Preprint* — real and common in factor research (SSRN, NBER), but it's a maturity distinction (not-yet-peer-reviewed) on Journal Paper, not a structurally different object — better handled as a Maturity value than a new Type, consistent with how KOM avoided multiplying types for what's really a classification dimension. *News/Press Release* — considered and rejected for v1: too weak relative to the Evidence-over-Opinion principle and the anti-laundering rule to warrant formal Evidence status without a specific justified use case (e.g. event-study validation) — can be added later with real justification, not by default.

## The one necessary connecting mechanism

Evidence Coverage can't be measured without *some* edge from a Knowledge object to the Evidence that grounds it. This is not a reopening of the paused Relationship Model track (extends/implements/supports/contradicts) — those refine relationships *within* the Knowledge Graph; this crosses from Knowledge into Evidence, and Evidence Coverage is unmeasurable without it.

**Decision: reuse the existing Frozen `references` edge type**, tagged `grounded-by`, rather than inventing a new native relationship column. Non-validity-critical (an Evidence source being superseded doesn't retroactively invalidate the Knowledge object's basic definition, though it does affect its grounding status) — same family as `evaluated-by` and `extends` were, minimal addition, no new mechanism invented.

## ADRs

- **ADR-042** — Evidence Object Model established (7 types), parallel to KOM, does not reopen ADR-021. Status: Accepted.
- **ADR-043** — Evidence Tier assignment is instance-level, not type-level (extends ADR-037's principle to the Evidence domain). Status: Accepted.
- **ADR-044** — Knowledge→Evidence grounding uses the existing `references` edge, tagged `grounded-by`; not a Relationship Model reopening. Status: Accepted.

## Deliberately not done here

No Evidence Entry Schema (citation fields, identifiers, retrieval metadata) — same discipline as KOM v1.0 preceding Knowledge Entry Schema by several stages. No Evidence objects populated yet — that's the next KnowledgeOps action, not part of this design pass.
