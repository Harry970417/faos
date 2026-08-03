# RELATIONSHIP_CANDIDATE_REGISTER.md

Tracks the lifecycle of candidate relationship types under evaluation for Stage 2.3. Distinct from Decision Status (ADR-029, which governs architectural decisions and changes only by deliberate governance action). Entries here change state automatically as seed evidence accumulates — no ADR required for routine updates. An ADR is only triggered when a candidate is formally adopted into a Frozen Relationship Model.

**States:** Proposed → {Adopted | Deferred | Dormant | Rejected}, any state revisable on new evidence.

| Candidate | Family | State | Evidence (v0.2) | Reconsider when |
|---|---|---|---|---|
| evaluated-by | references | **Adopted** (draft) | 12/12 instances, Factor→Metric only | extend scope if Model/Procedure→Metric evidence appears |
| extends | depends-on | **Adopted** (draft), scope narrowed | 6 of 11 tagged instances verified clean on re-examination; 5 spun into follow-up candidates below | — |
| **implements** | depends-on | **Adopted** (upgraded from Dormant) | 9 uses, 2 type-pairs (Procedure→Standard canonical, Model→Theory secondary) | — |
| formalized-by | references | **Deferred** | still 1 instance despite Theory count 5→25 — flagged as likely authoring gap, not rarity | wire T22→F27 (Fisher) and re-check other Theories in remediation |
| revises | undefined | **Proposed** (upgraded from Rejected) | 1 candidate instance (M06 CIR revises M05 Vasicek, pending retag decision) | a second instance, or explicit reclassification of M06→M05 |
| alternative-to / parallel-method (new) | undefined, direction ambiguous | **Proposed** | 1–2 instances (M08↔M02 confirmed; M20↔M08 possible) | ≥2 clean instances and a settled direction convention |
| supports | undefined | Proposed | not tested in v0.2 either | — |
| contradicts | undefined | Proposed | not tested in v0.2 either | — |

No changes to ADR-029. No ADR-041 — implements' Dormant→Adopted transition is a register update, not a KOM change (implements has been in the Frozen relationship vocabulary since Stage 2.1 / ADR-036).
