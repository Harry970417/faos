# RP-001 Reading Guide

This repo has ~90 RP-001 documents accumulated across exploratory and confirmatory phases. This guide gives each type of reader a short, ordered path — not "read everything."

## 教授 / Faculty reviewing an application

1. `research/RP001_RESEARCH_SUMMARY_3TO5P.md` — everything needed in one sitting
2. `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md` — the actual verdict reasoning, if you want the statistical detail
3. `research/RP001_FINAL_ACCEPTANCE_REPORT.md` — governance/closure, if you want to see how negative results were handled

## 推甄審查者 / Admissions reviewer (non-specialist, time-constrained)

1. `RP001_PORTFOLIO_ONE_PAGE.md`
2. `portfolio/RP001_PORTFOLIO_CARD.md` (if even less time)
3. One chart: `figures/Figure07_HypothesisVerdicts.png`

## Quant Researcher

1. `research/RP001_CONFIRMATORY_HYPOTHESES.md` + `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` — what was pre-registered
2. `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md` — full statistics
3. `research/RP001_RESULTS_TABLES_v0.2.md` — exploratory vs. confirmatory side-by-side
4. `research/RP001_PHASE2A_DEVIATION_LOG.md` — every methodological judgment call, in order
5. Code: `research/rp001_phase2a_confirmatory_tests.py`, `research/rp001_1c_plus_setup.py`

## Data Engineer

1. `research/RP001_PHASE2A_FINAL_DATASET.md` — acquisition summary
2. `research/RP001_PHASE2A_BATCH_TRACKER.md` — batch-by-batch integrity gate log, including the two real bugs found and fixed
3. Code, in pipeline order: `research/rp001_batch_acquire.py` → `research/rp001_phase2a_build_panel.py` → `research/rp001_phase2a_build_features.py` → `research/rp001_phase2a_coverage_and_tests.py`
4. `research/RP001_PHASE2A_DATA_TEST_REPORT.md` — test suite

## 一般讀者 / General reader

1. `README.md`'s RP-001 section
2. `RP001_FINAL_SHOWCASE.md` (Chinese, illustrated, A–O sections)

## 想重現研究的人 / Someone reproducing the study

1. `research/RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`
2. `research/RP001_ARCHIVE_MANIFEST.json` — hashes and exact reproduction entry points
3. Run the five pipeline scripts in order (see `README.md`'s "How to reproduce")

## What NOT to start with

`archive/RP001_RESEARCH_REPORT_v0.1.md` and the Milestone 0A–1D documents are the **exploratory-phase historical record** — genuinely useful for understanding how the hypotheses were generated, but they describe findings that mostly did not survive confirmatory testing. Reading them first without reading `archive/RP001_RESEARCH_REPORT_v0.2.md` alongside risks coming away with an outdated impression of what RP-001 concluded.
