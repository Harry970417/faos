# FAOS Alpha 0.3 Proposal

**Scope discipline:** this proposal contains only improvements RP-001's actual execution produced concrete evidence for. It does not reopen Architecture, Knowledge Object Model, or Classification design — RP-001 found that layer sound (see `FAOS_RP001_CASE_STUDY.md`, "What worked without needing to change anything"). Nothing here is speculative.

## 1. Add a Newey-West Method/Formula object

**Evidence:** used in every significance test across both RP-001 phases (56 exploratory tests, 16 confirmatory tests), flagged as a gap in `RP001_FAOS_TRACE.md` at the start of RP-001, still absent at closure. This is the single most-reused piece of methodology in the entire program with no corresponding Knowledge Object.

**Proposed action:** create a Method object for Newey-West (1987) standard errors, with the Fama-MacBeth-style Evidence attachment pattern already established for M16/F12 as the template.

## 2. Add a "Data Acquisition Pattern" checklist, seeded with two real patterns

**Evidence:** two real acquisition-tooling bugs occurred during Phase 2A.2 (Batch 8: an incomplete batch treated as complete after a connectivity outage; Batch 9: a legitimate empty API response treated as a failure, causing an infinite retry loop). Both are generic patterns any future API-based data acquisition would risk repeating, not RP-001-specific.

**Proposed action:** a small checklist (not a full object type) covering: (a) explicitly distinguish "empty but valid" from "failed" response states before writing retry logic; (b) never treat "every request attempted" as "batch complete" — require an explicit success/terminal-state count. Seeded from these two cases only; not a general-purpose QA framework.

## 3. Document the batch-based Integrity Gate as a reusable procedure

**Evidence:** used successfully across all 19 acquisition batches — every batch's anomalies individually investigated before proceeding, a non-loosening rule enforced even for repeat-pattern anomalies (69 individually-verified Dealer-schema instances, no batch was ever waved through by pattern-matching alone).

**Proposed action:** write up the procedure (batch-sized chunks, hard-stop on genuinely new anomaly types, downgrade-to-warning only for fully-characterized repeat patterns, individual re-verification never skipped) as a named, reusable process template, so the next Research Production case doesn't have to reinvent batch-acquisition governance from scratch.

## 4. Formalize the Protocol Lock + Deviation Log pattern as the default for any future confirmatory research

**Evidence:** this pattern is the direct, traceable reason RP-001's negative result was reported honestly rather than rationalized away (see `FAOS_RP001_CASE_STUDY.md`, "value of pre-registration... demonstrated, not asserted"). It was designed ad hoc for RP-001; it should not need to be designed ad hoc again.

**Proposed action:** extract the six-document Protocol Lock structure and the Deviation Log format (Deviation / Original Spec / Reason / Before-or-After / Impact) into a template, usable by any future FAOS research program that involves a confirmatory (as opposed to purely exploratory) phase.

## What is explicitly NOT proposed

No new Knowledge Object type, no change to the Domain Model or Classification scheme, no Max Drawdown object (flagged as a minor gap in the exploratory-phase trace but never actually needed by RP-001's confirmatory work — not evidenced by this program, deferred), no general-purpose data-quality framework beyond the two specific patterns in item 2. Adopting this proposal does not require reopening the Architecture, Knowledge, or Evidence Era work.

## Status

**Proposal only. Not adopted.** Requires separate review and approval before any of the above is implemented.
