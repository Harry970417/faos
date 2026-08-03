# FAOS + RP-001

**RP-001 — Does foreign institutional net flow predict Taiwan stock returns? Status: Completed.**

A 50-stock exploratory study found a conditional "yes." A full-market, 14-year confirmatory re-test — pre-registered before the data was touched — found the central claim **does not replicate**. Reported honestly, not softened. That's the whole story in one sentence; everything below just backs it up.

## What was done

Two-phase research design: (1) exploratory hypothesis search on 50 stocks, (2) a Protocol Lock — factor definition, statistical methods, and five hypotheses fixed and SHA-256-hashed *before* acquiring any full-market data — followed by an independent confirmatory test on the complete TWSE + TPEx universe.

## Research question

Does foreign institutional net flow (外資買賣超) predict short-horizon cross-sectional returns in Taiwan equities, and under what conditions does the relationship hold or break down?

## Data scale

| | Exploratory | Confirmatory |
|---|---|---|
| Stocks | 50 | **2,255** (1,980 listed + 275 delisted) |
| Period | ~2 years | **~14 years** (2012–2026) |
| Final test sample | 491 trading days | **1,462 stocks, 3,934,274 rows** |

6,765 API requests, 100% resolved, 34.2M raw rows, 21/21 unit and data-leakage tests pass on the final dataset.

## Main findings

| Hypothesis | Verdict |
|---|---|
| H-C1 (pre-break positive IC) | **Not Replicated** |
| H-C2 (post-break null) | Replicated (weak — see caveat in `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`) |
| H-C3 (liquidity conditionality) | Partially Replicated |
| H-C4 (volatility break-conditionality) | **Not Replicated** |
| H-C5 (no genuine interactions) | **Not Replicated** (unexpected finding — small residual effects survive at full-universe scale) |

> 本研究在 50 檔探索樣本中觀察到外資買賣超的條件式預測能力，但該結果未能在完整 TWSE 與 TPEx 股票池中複現。低波動機制亦未獲支持，流動性條件僅部分複現。部分交互作用項在完整樣本中出現小量級殘差效果，但屬確認性樣本中的意外發現，必須由新的預註冊研究獨立驗證。整體證據不支持將外資買賣超視為穩定、普遍或可直接交易的無條件因子。

**RP-001 does not claim to have found a stable, tradeable alpha.** It demonstrates a full, honest pre-registered confirmatory validation cycle — including reporting that the central exploratory finding does not survive full-universe testing.

## Why worth reading

Most student factor-research projects report only the version of the study that "worked." This one ran the same five hypotheses twice — once to discover them, once to test them independently — and reports what happened both times, including a negative result for the central claim. Two real data-engineering bugs were found and fixed mid-acquisition; both are documented, not hidden.

## Where to go next

| Need | Go to |
|---|---|
| One-page version | `portfolio/RP001_PORTFOLIO_ONE_PAGE.md` |
| 3–5 page summary | `research/RP001_RESEARCH_SUMMARY_3TO5P.md` |
| Full research report | `research/RP001_FINAL_RESEARCH_REPORT.md` |
| Formal closure record | `research/RP001_FINAL_ACCEPTANCE_REPORT.md` |
| Illustrated showcase (Chinese) | `portfolio/RP001_FINAL_SHOWCASE.md` |
| Role-specific reading paths | `RP001_READING_GUIDE.md` |
| Every document, indexed | `MASTER_DOCUMENT_INDEX.md` |
| Reproduce it | `research/RP001_PHASE2A_REPRODUCIBILITY_REPORT.md` |

---

## Repository map

```
architecture/    FAOS Domain Model, Knowledge Object Model, Relationship Model, product versions
knowledge/       The Knowledge Base itself + build/audit scripts
evidence/        Evidence Object Model, Evidence Completion Criteria, Evidence Pilots
research/        RP-001's full record: exploratory phase, Phase 2A protocol/acquisition/results, pipeline code
portfolio/       Showcase, one-pager, portfolio card, paragraph banks
applications/    Five school-specific positioning documents
interview/       Interview scripts and Q&A bank
figures/         11 charts, generated from real results only
archive/         Superseded versions and duplicates, preserved not deleted
```

Root-level navigation files: this README, `PROJECT_STATUS.md`, `ROADMAP.md`, `CHANGELOG.md`, `TERMINOLOGY.md`, `MASTER_DOCUMENT_INDEX.md`, `FIGURE_MANIFEST.md`, `ARCHIVE_INDEX.md`, `PUBLICATION_CHECKLIST.md`, `RP001_READING_GUIDE.md`, `RP001_GITHUB_README_SECTION.md` (a portable drop-in excerpt for other repos), `FEATURE_REGISTRY.md` (kept at root — referenced by name throughout nearly every document, moving it would create the highest-risk broken reference in the repo for no real benefit).

## How to reproduce

```
python research/rp001_batch_acquire.py <batch_id> <start_idx> <end_idx>   # 19 batches, see research/RP001_PHASE2A_BATCH_TRACKER.md
python research/rp001_phase2a_build_panel.py
python research/rp001_phase2a_build_features.py
python research/rp001_phase2a_coverage_and_tests.py
python research/rp001_phase2a_confirmatory_tests.py
python research/rp001_phase2a_build_charts.py
```

No random seed or stochastic step anywhere in the pipeline — deterministic given the same raw data.

## What large data is NOT in this repo

`rp001_data/phase2a/raw/` (3.7GB of raw API responses) and `rp001_data/phase2a/processed/*.parquet` (derived datasets, up to ~760MB each) are gitignored. Every raw file is individually SHA-256-hashed in `research/RP001_PHASE2A_BATCH_TRACKER.md`'s manifests; the final dataset is hashed in `research/RP001_ARCHIVE_MANIFEST.json`. Nothing about the results is unverifiable — the hashes just aren't distributed via git.

## Research limitations

Market-cap/sector data unavailable at full-universe scale (2 of 7 interaction features untestable); only 69.8% of stocks with panel presence pass the coverage gate and enter the confirmatory tests; no causal identification design anywhere in the study; no portfolio, backtest, or transaction-cost analysis anywhere in RP-001. Full detail: `research/RP001_LIMITATIONS_v0.2.md`.

## Research Integrity Statement

No methodology was changed after seeing any result, at any stage. Every finding that contradicts the exploratory-phase conclusions — including the central result that F_INST_01 does not replicate — is reported in full, with no adjustment or omission. All exploratory-phase documents remain unmodified as the historical record. Every deviation from the locked protocol, however small, was logged before the affected test ran. Full version: `research/RP001_FINAL_ACCEPTANCE_REPORT.md`.

## What FAOS is

FAOS is the research-production framework RP-001 was built on: a Knowledge Object Model + governance layer (Methods, Metrics, Factors, Evidence objects with dependency tracking and Evidence Completion Criteria) plus the pre-registration/Deviation-Policy/Integrity-Gate tooling that made RP-001's honest negative result possible rather than quietly rationalized away. See `architecture/FAOS_RP001_CASE_STUDY.md` for what held up under real use and `architecture/FAOS_ALPHA_0.3_PROPOSAL.md` for the small, evidence-backed improvements RP-001 surfaced.

---

*Status snapshot: `PROJECT_STATUS.md`. What's next: `ROADMAP.md`, `research/RP002_CANDIDATE_RESEARCH_BRIEF.md`. Version history: `CHANGELOG.md`. Terminology: `TERMINOLOGY.md`.*
