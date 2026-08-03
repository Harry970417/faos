# Master Document Index

Every file in this repository, categorized by purpose. Built by direct reading of the repo (not conversation memory) as part of the Final Publication Pass. Reorganization mapping (old path → new path) is documented per section; the physical move happens alongside this index, see `CHANGELOG.md` for the commit that executed it.

**Legend — 是否最新:** ✅ current/canonical · 🕰 historical, superseded for status but preserved · **是否應保留:** Keep (active folder) · Archive (moved to `archive/`, never deleted)

---

## Architecture (`architecture/`)

FAOS's Domain Model, Knowledge Object Model, Classification, and Relationship Model design work. All Frozen (v1.0) unless noted.

| File | 用途 | 閱讀順序 | 是否最新 | 是否應保留 |
|---|---|---|---|---|
| `architecture/DESIGN_APPROVAL.md` | Formal gate confirming Architecture/KOM/Classification Frozen before Remediation began | 1 | ✅ | Keep |
| `architecture/SEED_GRAPH_AUDIT_v0.1.md` | Graph integrity audit of the 50-object pilot seed | 2 | 🕰 (pilot, superseded in scale by `architecture/KNOWLEDGE_GRAPH_AUDIT_v0.2.md`, not in content — different object count, both real) | Keep (distinct pilot-scale finding, not a version pair) |
| `architecture/ISOLATED_OBJECT_REGISTER_v0.1.md` | Classifies all 71 isolated objects in KB v0.2 | 3 | ✅ | Keep |
| `architecture/RELATIONSHIP_MODEL_v0.1_DRAFT.md` | First relationship-type evidence pass (50-object seed) | 4 | 🕰 (pilot scale) | Keep (feeds v0.2 review, not replaced) |
| `architecture/RELATIONSHIP_MODEL_v0.2_REVIEW.md` | Relationship-type evidence at 302-object scale | 5 | ✅ | Keep |
| `architecture/RELATIONSHIP_CANDIDATE_REGISTER.md` | Live lifecycle tracker for candidate relationship types | 6 | ✅ (living document) | Keep |
| `architecture/KNOWLEDGE_GRAPH_AUDIT_v0.2.md` | Graph integrity + structure audit at 302-object scale, Baseline v0.2 | 7 | ✅ | Keep |
| `architecture/VALIDATION_REPORT_v1.md` | Reference-implementation validation of Architecture/KOM/Classification | 8 | ✅ | Keep |
| `architecture/CONNECTIVITY_REMEDIATION_PLAN_v0.1.md` | Plan to reconnect isolated objects, built on the Isolated Object Register | 9 | ✅ | Keep |
| `architecture/REMEDIATION_REPORT_v0.1.md` | Executed remediation (edges added, 3 duplicates merged) | 10 | ✅ | Keep |
| `architecture/FAOS_ALPHA_0.1.md` | First product version bundle | 11 | 🕰 (superseded by 0.2 as the live bundle) | Keep (version history, not an error) |
| `architecture/FAOS_ALPHA_0.2.md` | Current product version bundle | 12 | ✅ | Keep |
| `architecture/FAOS_RP001_CASE_STUDY.md` | What RP-001 proved/found about the FAOS architecture in practice | 13 | ✅ | Keep |
| `architecture/FAOS_ALPHA_0.3_PROPOSAL.md` | Small, evidence-backed proposal for the next product version | 14 | ✅ (proposal, not adopted) | Keep |

**Supporting data:** `architecture/final_analysis_output.txt` (raw relationship-candidate analysis output underlying `architecture/RELATIONSHIP_MODEL_v0.2_REVIEW.md`) — Keep, moves alongside.

---

## Knowledge (`knowledge/`)

The Knowledge Base itself (data files) and the scripts that built/audited it.

| File | 用途 | 是否最新 | 是否應保留 |
|---|---|---|---|
| `knowledge/knowledge_seed_v0.1.psv` | 50-object pilot seed data | 🕰 (pilot) | Keep (audited by `architecture/SEED_GRAPH_AUDIT_v0.1.md`, referenced as historical baseline) |
| `knowledge/knowledge_base_v0.2.psv` | 302-object Baseline (locked reference point) | ✅ | Keep |
| `knowledge/knowledge_base_remediated_v0.1.psv` | Post-remediation Knowledge Base (Alpha 0.2's actual shipped KB) | ✅ | Keep |
| `knowledge/append_seed.py` | Script that built the v0.1 seed | ✅ (tool, still valid) | Keep |
| `knowledge/audit_graph.py` | Audit script, v0.1 seed | ✅ (tool) | Keep |
| `knowledge/audit_graph_v0.2.py` | Audit script, v0.2 scale | ✅ (tool) | Keep |
| `knowledge/audit_remediated.py` | Audit script, post-remediation | ✅ (tool) | Keep |
| `knowledge/remediate.py` | Remediation execution script | ✅ (tool) | Keep |

---

## Evidence (`evidence/`)

Evidence Object Model design, Evidence Completion Criteria (ECC), and the two Evidence Pilots.

| File | 用途 | 是否最新 | 是否應保留 |
|---|---|---|---|
| `evidence/EVIDENCE_OBJECT_MODEL_v0.1.md` | Defines Evidence object types (parallel to KOM) | ✅ | Keep |
| `evidence/EVIDENCE_COMPLETION_CRITERIA_v0.1.md` | ECC rules by KOM type | ✅ (base rules; see revision below) | Keep |
| `evidence/ECC_v0.2_REVISION.md` | Amends 3 specific ECC gaps found in validation — an addendum, not a full replacement | ✅ | Keep (reads alongside the v0.1 base rules, not instead of) |
| `evidence/ECC_VALIDATION_REPORT_v0.1.md` | Checks ECC rules against Evidence Pilot v0.2 results | ✅ | Keep |
| `evidence/ECC_v0.2_SMALL_VALIDATION.md` | Tests 2 previously-unexercised ECC rules | ✅ | Keep |
| `evidence/ECC_TARGETED_REMEDIATION_v0.1.md` | Content/Maturity remediation for 3 specific objects (S01, S08, PA01) | ✅ | Keep |
| `archive/EVIDENCE_PILOT_v0.1.md` | First 20-object evidence-sourcing pass | 🕰 (superseded by v0.2's genuine re-verification of failing objects) | Archive |
| `evidence/EVIDENCE_PILOT_v0.2.md` | Second pass, same 20 objects, real re-verification | ✅ | Keep |
| `evidence/EVIDENCE_COVERAGE_DASHBOARD.md` | Evidence-grounding coverage metric (Day Zero baseline) | ✅ | Keep |
| `evidence/EVALUATION_SUITE_v0.1.md` | 100-question KB stress test (84/100 conceptually sufficient) | ✅ | Keep |
| `evidence/EVALUATION_SUITE_v0.1_raw_results.txt` | Raw per-question results | ✅ | Keep |
| `archive/eval_results.txt` | **Byte-identical duplicate of `evidence/EVALUATION_SUITE_v0.1_raw_results.txt`** (verified via `diff`, zero difference) | — duplicate | Archive (redundant copy, content preserved in the kept file) |
| `evidence/RESEARCH_ANSWER_COMPARISON_v0.1.md` | Does ECC-Pass produce a better answer than ECC-Fail? | ✅ | Keep |
| `archive/evidence_pilot_v0.1.psv` | Data underlying the v0.1 pilot | 🕰 | Archive (pairs with v0.1 doc above) |
| `evidence/evidence_pilot_v0.2.psv` | Data underlying the v0.2 pilot | ✅ | Keep |
| `evidence/evidence_dashboard_v0.2.py` / `evidence/evidence_dashboard_v2.py` | Dashboard computation scripts (two versions found — see Duplicate Content Review) | ✅ both | Keep both (near-identical names, not identical content — see below) |
| `evidence/analyze_v0.2_full.py`, `evidence/eval_suite.py` | Analysis/evaluation scripts | ✅ | Keep |
| `architecture/final_analysis_output.txt` | *(cross-referenced from Architecture — physically stored once, listed in both sections)* | ✅ | Keep in `architecture/` |

---

## Research (`research/`)

RP-001's full research record: exploratory phase, Phase 2A protocol/execution/results, and pipeline code.

### Exploratory phase (Milestones 0A–1D) — 🕰 historical record, preserved unmodified, Keep

`research/RP001_RESEARCH_BRIEF.md`, `research/RP001_RESEARCH_DESIGN.md`, `research/RP001_DATA_REQUIREMENTS.md`, `research/RP001_EVIDENCE_MAP.md`, `research/RP001_EXECUTION_PLAN.md`, `research/RP001_RISK_AND_BIAS_REGISTER.md`, `research/RP001_READINESS_REVIEW.md`, `research/RP001_DATA_PROFILE.md`, `research/RP001_FEATURE_SPECIFICATION.md`, `research/RP001_FEATURE_VALIDATION_v0.1.md`, `research/RP001_DAILY_UNIVERSE_VALIDATION.md`, `research/RP001_MILESTONE_1C_DIAGNOSTICS.md`, `research/RP001_BREAKPOINT_ANALYSIS.md`, `research/RP001_REGIME_ROBUSTNESS.md`, `research/RP001_INTERACTION_INCREMENTAL_TESTS.md`, `research/RP001_MULTIPLE_TESTING_REGISTER.md`, `research/RP001_MILESTONE_1C_R_ROBUSTNESS.md`, `research/RP001_MILESTONE_1C_PLUS_MECHANISM.md`, `research/RP001_MILESTONE_1D_FEATURE_FREEZE_REVIEW.md`, `research/RP001_FEATURE_DECISION_TABLE.md`, `FEATURE_REGISTRY.md` (root-level, kept there deliberately — see note below).

**Note on `FEATURE_REGISTRY.md`:** stays at repo root, not moved into `research/`, because it is directly and heavily cross-referenced by name (bare, no path) throughout dozens of documents across every era — moving it would create the single highest-risk broken-reference point in the whole repo for the lowest reorganization benefit. Documented here as a deliberate exception, not an oversight.

### Confirmatory phase — Protocol, Deviation Policy, Acceptance Criteria — ✅ current, Keep

`research/RP001_PHASE2A_CONFIRMATORY_PROTOCOL.md`, `research/RP001_FULL_UNIVERSE_SPEC.md`, `research/RP001_CONFIRMATORY_HYPOTHESES.md`, `research/RP001_DEVIATION_POLICY.md`, `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`, `research/RP001_PHASE2A_EXECUTION_PLAN.md`, `research/RP001_PHASE2A_PROTOCOL_LOCK.md`, `research/RP001_PHASE2A_READINESS_GATE.md`, `research/RP001_PHASE2A_CAPACITY_ESTIMATE.md`, `research/RP001_PHASE2A_DATA_QUALITY_PILOT.md`, `research/RP001_PHASE2A_DATA_SNAPSHOT_SPEC.md`.

### Confirmatory phase — Full-universe audits and remediation — ✅ current, Keep

`research/RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md`, `research/RP001_INSTITUTIONAL_SCHEMA_AUDIT.md`, `research/RP001_INSTITUTIONAL_MISSINGNESS_AUDIT.md`, `research/RP001_MARKET_MEMBERSHIP_AUDIT.md`, `research/RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md`, `research/RP001_MISSINGNESS_POLICY.md`, `research/RP001_ANOMALY_REGISTER.md`, `research/RP001_FEATURE_IMPACT_MATRIX.md`, `research/RP001_API_AND_SOURCE_FEASIBILITY.md`, `research/RP001_PHASE2A1_REAUDIT.md`, `research/RP001_PHASE2A2R_DECISION_GATE.md`.

### Confirmatory phase — Acquisition, dataset, results — ✅ current, Keep

`research/RP001_PHASE2A_BATCH_TRACKER.md`, `research/RP001_PHASE2A_DEVIATION_LOG.md`, `research/RP001_PHASE2A_FINAL_DATASET.md`, `research/RP001_PHASE2A_DATA_MANIFEST.json`, `research/RP001_PHASE2A_CONFIRMATORY_DATASET.md`, `research/RP001_PHASE2A_FEATURE_REGISTRY.md`, `research/RP001_PHASE2A_DATA_TEST_REPORT.md`, `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`, `research/RP001_PHASE2A_DEVIATION_FINAL.md`, `research/RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`.

### Closure and final governance — ✅ current, definitive, Keep

`research/RP001_FINAL_ACCEPTANCE_REPORT.md`, `research/RP001_ARCHIVE_MANIFEST.json`, `RP001_FINAL_CONTENT_AUDIT.md`, `research/RP001_FINAL_CONSISTENCY_AUDIT.md`, `research/RP001_LOG.md`.

### Report suites — mixed, see reasoning

| File | 是否最新 | 是否應保留 |
|---|---|---|
| `archive/RP001_RESEARCH_REPORT_v0.1.md`, `archive/RP001_METHODS_AND_DATA_v0.1.md`, `archive/RP001_RESULTS_TABLES_v0.1.md`, `archive/RP001_LIMITATIONS_v0.1.md`, `archive/RP001_REPRODUCIBILITY_APPENDIX_v0.1.md`, `archive/RP001_RESEARCH_FINDINGS_v0.1.md` | 🕰 superseded by v0.2 | **Archive** |
| `archive/RP001_RESEARCH_REPORT_v0.2.md` | 🕰 superseded in practice by `research/RP001_FINAL_RESEARCH_REPORT.md` (same audience/purpose, FINAL is the more complete version) | **Archive** (judgment call, reasoning above) |
| `research/RP001_EXECUTIVE_SUMMARY_v0.2.md`, `research/RP001_METHODS_AND_DATA_v0.2.md`, `research/RP001_RESULTS_TABLES_v0.2.md`, `research/RP001_LIMITATIONS_v0.2.md`, `research/RP001_REPRODUCIBILITY_APPENDIX_v0.2.md`, `research/RP001_FAOS_TRACE_v0.2.md`, `research/RP001_CHANGELOG_v0.2.md` | ✅ — **no FINAL-tier document duplicates this specific content** (methods detail, results tables, limitations, reproducibility appendix, FAOS trace, changelog) | **Keep** — living exception to a blind "archive all v0.2" sweep; each provides content nothing else in the repo provides |
| `research/RP001_RESEARCH_FINDINGS_v0.2.md` | ✅ (this IS the current findings taxonomy — Exploratory/Confirmatory/Not Replicated/etc.) | Keep |
| `research/RP001_FINAL_RESEARCH_REPORT.md`, `research/RP001_RESEARCH_SUMMARY_3TO5P.md` | ✅ | Keep |
| `research/RP001_FAOS_TRACE.md` (no version suffix, the original) | 🕰 exploratory-phase | Keep (paired with, not replaced by, `_v0.2`) |

### Pipeline code and data — Keep, all current

All `rp001_*.py` files, `research/test_daily_universe_gate.py`, and `rp001_data/` (raw gitignored, manifests, processed gitignored parquet + committed JSON/CSV summaries, charts — see Figures section).

---

## Portfolio (`portfolio/`)

| File | 用途 | 是否應保留 |
|---|---|---|
| `RP001_FINAL_SHOWCASE.md` | Chinese-language illustrated showcase, sections A–O | Keep |
| `RP001_PORTFOLIO_ONE_PAGE.md`, `portfolio/RP001_PORTFOLIO_CARD.md` | One-page and micro-card portfolio versions | Keep |
| `RP001_PORTFOLIO_LAYOUT_GUIDE.md`, `RP001_IMAGES_NEEDED.md` | Layout planning and figure-selection guidance | Keep |
| `portfolio/RP001_AUTOBIOGRAPHY_PARAGRAPH.md`, `portfolio/RP001_STUDY_PLAN_PARAGRAPH.md`, `portfolio/RP001_RESEARCH_MOTIVATION_PARAGRAPH.md`, `portfolio/RP001_FUTURE_RESEARCH_PARAGRAPH.md` | Reusable paragraph banks (formal/concise/conversational) | Keep |

## Applications (`applications/`)

`applications/RP001_APPLICATION_NTU_FINANCE.md`, `applications/RP001_APPLICATION_NCCU_FINANCE.md`, `applications/RP001_APPLICATION_NTUST_FINANCE.md`, `applications/RP001_APPLICATION_TAIPEITECH_IMFIN.md`, `applications/RP001_APPLICATION_NTNU_MANAGEMENT.md` — all Keep, all current, each independently positioned (verified in `research/RP001_FINAL_CONSISTENCY_AUDIT.md` item 10).

## Interview (`interview/`)

`interview/RP001_INTERVIEW_30SEC.md`, `interview/RP001_INTERVIEW_90SEC.md`, `interview/RP001_INTERVIEW_3MIN.md`, `interview/RP001_INTERVIEW_QA_BANK.md` — all Keep, all current.

## Figures (`figures/`)

11 PNG charts, renamed per `FIGURE_MANIFEST.md` (built alongside this index — see that document for the old→new filename mapping and per-figure detail). Chart-generation script (`rp001_phase2a_build_charts.py`) updated to write to the new location.

## GitHub / repo-root navigation (stays at root — these are meant to be found immediately)

`README.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `CHANGELOG.md`, `RP001_GITHUB_README_SECTION.md`, `RP001_READING_GUIDE.md`, `TERMINOLOGY.md`, `MASTER_DOCUMENT_INDEX.md` (this file), `FIGURE_MANIFEST.md`, `ARCHIVE_INDEX.md`, `PUBLICATION_CHECKLIST.md`.

## Logs (stay with their subject matter, not a separate top-level folder)

`research/RP001_LOG.md` (research/), `research/RP001_PHASE2A_DEVIATION_LOG.md` (research/) — both are living decision records, not archived, and are referenced by path/name too often to relocate away from their subject area.

## Archive (`archive/`)

See `ARCHIVE_INDEX.md` for the full list and reasoning per item — built alongside this index.
