# FAOS × RP-001 Case Study

RP-001 is FAOS's first real Research Production case — the first time the Architecture/Knowledge/Evidence infrastructure and governance tooling built in FAOS Alpha 0.1/0.2 was used to run an actual research program end to end, from hypothesis to formal closure. This document records what that stress test actually showed, not what it was expected to show.

## How FAOS supported RP-001

- **Method/Metric reuse:** ME07 (Information Coefficient), C06 (Correlation), C46/C47 (Autocorrelation/Heteroskedasticity), PR04 (Cross-Sectional IC Computation), ME41/ME42 (T-Statistic/Standard Error) — all reused directly from the existing Knowledge Base, unmodified, across both the exploratory and confirmatory phases.
- **Evidence grounding:** Fama-MacBeth (1973) was formally attached to M16/F12 during RP-001's design phase, the one piece of pre-positioned Evidence that reached full attachment during this program.
- **Governance tooling built for RP-001, now reusable:** the Deviation Policy format (Deviation / Original Spec / Reason / Before-or-After / Impact), the pre-registration + Protocol Lock pattern (six documents, SHA-256-hashed, locked before data acquisition), and the batch-based Integrity Gate pattern (each acquisition batch individually gated, anomalies investigated before proceeding) were all designed during RP-001 execution and are now templates any future FAOS research program can reuse directly.

## What worked without needing to change anything

Every core methodology object (IC computation, Newey-West correction, cross-sectional residualization, Benjamini-Hochberg FDR) transferred from the 50-stock exploratory scale to the 2,255-stock, 34-million-row confirmatory scale with zero structural friction. The only change needed at scale was a performance optimization (vectorizing the per-date IC loop into a closed-form correlation computation) — not a redesign of any method. This is the strongest evidence the underlying Architecture/Knowledge/Evidence design was sound: a two-orders-of-magnitude increase in data volume did not require touching the Knowledge Object Model itself.

## Where nothing needed to be modified (worth stating explicitly)

The Domain Model, Knowledge Object Model type system, and Classification scheme required zero changes throughout RP-001. Every gap found (below) was a **content** gap — missing objects — not a structural problem with how FAOS represents knowledge. This distinction matters: it means the architecture-design work done before RP-001 (the Architecture/Knowledge/Evidence Eras) was validated by actual use, not merely by internal review.

## How FAOS prevented wrong knowledge from being retained

This is RP-001's most concrete governance contribution. Three mechanisms did real work, not just process theater:

1. **The Deviation Policy's before/after discipline** caught and blocked what would otherwise have been a slow drift toward post-hoc rationalization. Every one of the eight logged deviations (D-01 through D-08) was recorded before the affected test ran — including D-08, discovered while *planning* the confirmatory dataset build, before a single line of construction code was written.
2. **Protocol Lock + hashing** made it structurally impossible to quietly redefine F_INST_01, the return horizon, or the break interval after seeing early full-universe results — any such change would have produced a hash mismatch, an auditable trigger, not a silent edit.
3. **The Research Log's decision/reason/evidence/impact format**, applied consistently across ~30 entries this program, meant that when the confirmatory results contradicted the exploratory findings, there was no ambiguity about what the original claim had been or why it was now being superseded rather than deleted. `FEATURE_REGISTRY.md`'s Milestone 1D table is still there, unedited, below the final status table — FAOS's discipline of "correct in place, preserve the record" is what made that possible without the document becoming self-contradictory.

## The value of pre-registration, Deviation Policy, and Research Log — demonstrated, not asserted

RP-001's central result (F_INST_01 does not replicate) is exactly the kind of finding a less disciplined process would be tempted to suppress, hedge into meaninglessness, or "fix" by loosening the confirmatory criteria after the fact. None of that happened, and the reason it didn't happen is traceable to specific FAOS mechanisms, not just researcher goodwill: the acceptance criteria were fixed and hashed before the test ran, so there was no criteria left to adjust.

## What FAOS's next Research Production case should do more efficiently

- The acquisition-tooling bugs found in Phase 2A.2 (Batches 8 and 9) were both generic data-pipeline patterns (incomplete-batch-treated-as-complete, legitimate-empty-response-treated-as-failure) with no FAOS object to check against — a future case would benefit from a small "Data Acquisition Pattern" checklist object, so these don't have to be independently rediscovered.
- Newey-West still has no Method/Formula object in the Knowledge Base despite being used in every confirmatory test this program ran — this gap, first flagged during RP-001's exploratory phase, persisted through the entire confirmatory phase without being fixed, correctly triaged as out-of-scope execution work each time. It should be the first object created before FAOS's next Research Production case begins, not deferred again.
- The batch-based Integrity Gate pattern (per-batch anomaly investigation, non-loosening rule, individual verification of repeat-pattern anomalies) proved valuable enough over 19 batches that it should be documented as a reusable procedure, not reinvented per research program.

No Frozen artifact was modified to produce any of the above. Full detail on specific findings: `research/RP001_FAOS_TRACE.md` (exploratory phase), `research/RP001_FAOS_TRACE_v0.2.md` (confirmatory phase).
