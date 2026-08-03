# Terminology

Canonical definitions for terms used across FAOS and RP-001. All formal documents should use these terms consistently; where an older document uses a variant, that document is historical record and is not rewritten, but new documents should follow this glossary.

## FAOS-level terms

**Research Production** — the phase of FAOS's lifecycle that begins once Architecture, Knowledge Object Model, and Classification are Frozen: actually running a research program (RP-001) on top of the frozen infrastructure, as opposed to designing the infrastructure itself.

**Knowledge Base** — the populated store of Knowledge Objects (`knowledge/knowledge_base_v0.2.psv`, `knowledge/knowledge_base_remediated_v0.1.psv`). Distinct from **Knowledge Object Model (KOM)**, which is the *type system* (11 object types) the Knowledge Base is an instance of. "Knowledge Seed" is a retired term for early, small-scale precursors to the Knowledge Base (see `architecture/DESIGN_APPROVAL.md`'s naming decision) — do not use "Seed" for anything past that pilot stage.

**Knowledge Object** — a single typed entry in the Knowledge Base (e.g., a Theory, Model, Metric, Factor). Always capitalized when referring to the formal KOM concept.

**Evidence** — the FAOS Domain Model concept (Frozen since ADR-021) covering the three-tier taxonomy Primary/Secondary/Derived, plus the anti-laundering rule. Not the same as an **Evidence Object**.

**Evidence Object** — a specific typed citation/source record (Company Filing, Dataset, Official Statistics, Official Standard, etc. — see `evidence/EVIDENCE_OBJECT_MODEL_v0.1.md`) that grounds a Knowledge Object. An Evidence `Standard` object (the literal published regulatory text) is distinct from a KOM `Standard` object (FAOS's own structured understanding of what that regulation requires) — always disambiguate if both appear in the same sentence.

**ECC (Evidence Completion Criteria)** — the definition-of-done rules, per KOM type, for when a Knowledge Object counts as adequately evidenced (minimum source count, tier requirements, triangulation/independence rules). Not a schema — deliberately non-uniform across types.

## RP-001-level terms

**Protocol Lock** — the act of freezing a set of governing documents (factor definitions, statistical methods, hypotheses, etc.) and recording their SHA-256 hashes *before* the data they will be tested against is acquired or examined. Capitalized as a proper noun when referring to RP-001's specific locking event (`research/RP001_PHASE2A_PROTOCOL_LOCK.md`, 2026-07-11).

**Deviation** — any point where a locked specification cannot be mechanically applied as written and a documented workaround is used instead, logged in a Deviation Log (`research/RP001_PHASE2A_DEVIATION_LOG.md`) *before* the affected test runs. Distinguished from an **Escalating Deviation** — one that would touch a "must not be reopened" item (F_INST_01's definition, rank normalization, return horizon, break-interval boundary), which pauses execution for approval rather than proceeding on a logged note.

**Integrity Gate** — the automated per-batch check applied during data acquisition: schema drift, duplicate observations, trading-calendar inconsistency, and (in the narrowed v2 script) Dealer-in-break-window recurrence are hard-stop conditions; missing-rate and listing-date-gap patterns are downgraded to warnings once characterized. A batch does not proceed until its gate result is PASS (directly or after investigation).

**Exploratory** — a finding, hypothesis, or test where the condition being tested was discovered on the same sample used to test it. Exploratory findings are hypothesis-generating, not confirmatory, regardless of how statistically significant they appear.

**Confirmatory** — a finding, hypothesis, or test that was fixed and locked *before* the data used to test it was examined. Only Phase 2A's five hypotheses (H-C1–H-C5) carry this status in RP-001.

**Replicated / Partially Replicated / Not Replicated / Inconclusive** — the four possible verdicts for a confirmatory hypothesis (`research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`). "Replicated" requires the pre-specified significance bar to be met at the pre-specified horizon(s); "Inconclusive" is reserved for genuine data-insufficiency (too few observations, a required data field unavailable), not for an unclear result.

## Feature-status terms (apply to any Knowledge Object or RP-001 feature)

**Frozen** — a status is stable under current evidence and will not change by preference alone; only new evidence revises it. Freezing does *not* mean validated for deployment, tradeable, or permanently correct. RP-001's Milestone 1D "Frozen — Conditional" status for F_INST_01 was itself later superseded by confirmatory testing — Frozen describes stability of a determination given the evidence available *at that time*, not permanence.

**Conditional** — a finding or status that holds only under specific, named sub-conditions (e.g., F_INST_01's exploratory-phase "Frozen — Conditional" required pre-break period, low-volatility regime, and illiquid-to-mid-liquidity names simultaneously). Never state a Conditional finding without its conditions.

**Experimental** — a status applied to a feature retained for further testing despite already-negative internal evidence, per explicit instruction rather than a natural conclusion of the evidence itself (e.g., F_INT_07 in the Milestone 1D freeze table).

**Deprecated** — superseded or made redundant by another feature/object (e.g., F_INST_06 deprecated as redundant with F_INST_05). Different from **Rejected**.

**Rejected** — no evidence of the tested property (e.g., predictive power) was found at any horizon or condition tested. Stronger than Deprecated: a Rejected feature was tested and failed, not merely superseded.

**Not Replicated** — RP-001's confirmatory-specific terminal status: a finding that held at exploratory scale did not hold under independent, pre-registered testing at full scale. Distinct from Rejected (which describes an exploratory-only finding never confirmed at all) — Not Replicated specifically means a confirmatory test was run and failed.
