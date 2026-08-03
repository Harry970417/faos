# FAOS + RP-001

This repository contains two related things: **FAOS** (a research-production framework: Architecture/Knowledge/Evidence infrastructure plus governance tooling for running disciplined empirical research), and **RP-001**, the first full research program built on top of it. If you're here for the research, skip straight to [RP-001](#rp-001-external-institutional-flow-and-taiwan-stock-returns) below.

## What FAOS is

FAOS ("Alpha 0.2" at RP-001's start) is a Knowledge Object Model + governance layer built before RP-001, covering Methods, Metrics, Factors, and Evidence objects with dependency tracking and an Evidence Completion Criteria (ECC) process. RP-001 is the first real stress test of that architecture against an actual research question. See `FAOS_RP001_CASE_STUDY.md` for what held up and what didn't, and `FAOS_ALPHA_0.3_PROPOSAL.md` for the (small, evidence-backed) improvements RP-001 surfaced.

## RP-001: External Institutional Flow and Taiwan Stock Returns

**Status: Completed.** Final commit `40a2be9`.

### Research question

Does foreign institutional net flow (外資買賣超) predict short-horizon cross-sectional returns in Taiwan equities, and under what conditions does the relationship hold or break down?

### Research lifecycle

1. **Exploratory phase** (50 stocks, ~2 years) — free hypothesis search: found a conditional signal (pre-break, low-volatility, illiquid-to-mid-liquidity).
2. **Protocol Lock** (2026-07-11) — six governing documents locked and SHA-256-hashed *before* any full-universe data was touched: factor definition, return-horizon construction, break-interval boundary, grouping definitions, statistical methods, and five confirmatory hypotheses (H-C1–H-C5).
3. **Phase 2A full-universe acquisition** — 2,255 stocks, 6,765 API requests, 100% resolved, 34.2M raw rows, 19 rate-limited batches, every anomaly individually investigated per the Deviation Policy.
4. **Confirmatory Dataset construction** — Daily Investable Universe, missing-state handling, feature construction, 21/21 unit and leakage tests.
5. **H-C1–H-C5 confirmatory tests** — run exactly as locked, no post-hoc adjustment.
6. **Formal closure** — final feature statuses, fixed core conclusion, archive manifest.

### Data scale

| | Exploratory | Confirmatory |
|---|---|---|
| Stocks | 50 | **2,255** (1,980 listed + 275 delisted) |
| Period | ~2 years | **~14 years** (2012–2026) |
| Final test sample | 491 trading days | **1,462 stocks, 3,934,274 rows** |

### H-C1–H-C5 verdicts

| Hypothesis | Verdict |
|---|---|
| H-C1 (pre-break positive IC) | **Not Replicated** |
| H-C2 (post-break null) | Replicated (weak — see caveat in `RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`) |
| H-C3 (liquidity conditionality) | Partially Replicated |
| H-C4 (volatility break-conditionality) | **Not Replicated** |
| H-C5 (no genuine interactions) | **Not Replicated** (unexpected finding — see below) |

### Final conclusion (fixed wording)

> 本研究在 50 檔探索樣本中觀察到外資買賣超的條件式預測能力，但該結果未能在完整 TWSE 與 TPEx 股票池中複現。低波動機制亦未獲支持，流動性條件僅部分複現。部分交互作用項在完整樣本中出現小量級殘差效果，但屬確認性樣本中的意外發現，必須由新的預註冊研究獨立驗證。整體證據不支持將外資買賣超視為穩定、普遍或可直接交易的無條件因子。

**RP-001 does not claim to have found a stable, tradeable alpha.** It demonstrates a full, honest pre-registered confirmatory validation cycle — including reporting that the central exploratory finding does not survive full-universe testing.

### Where to start reading

See `RP001_READING_GUIDE.md` for role-specific reading paths (professor, admissions reviewer, quant researcher, data engineer, general reader, reproducer). Quick links:

- **One page:** `RP001_PORTFOLIO_ONE_PAGE.md`
- **3–5 pages:** `RP001_RESEARCH_SUMMARY_3TO5P.md`
- **Full report:** `RP001_FINAL_RESEARCH_REPORT.md`
- **Formal closure record:** `RP001_FINAL_ACCEPTANCE_REPORT.md`
- **Visual showcase (Chinese, with charts):** `RP001_FINAL_SHOWCASE.md`

### Project structure (RP-001-relevant)

```
RP001_*.md                          Exploratory-phase docs (Milestones 0A-1D) -- historical record, preserved unmodified
RP001_PHASE2A_*.md                  Phase 2A protocol, acquisition, dataset, results docs
RP001_*_v0.1.md / RP001_*_v0.2.md   Report suites -- v0.1 exploratory, v0.2 final (supersedes v0.1 for status, does not delete it)
RP001_FINAL_*.md                    Closure-phase documents (this README's primary pointers)
RP001_ARCHIVE_MANIFEST.json         Final hashes, commit reference, reproduction entry points
rp001_batch_acquire.py, rp001_phase2a_*.py   Pipeline code (acquisition -> panel -> features -> tests -> charts)
rp001_data/phase2a/
  raw/            gitignored -- raw API responses, SHA-256-hashed in manifests/pull_manifest.csv
  manifests/      acquisition manifests, per-batch Integrity Gate results
  processed/      gitignored (*.parquet only) -- derived datasets; snapshot hash committed separately
  charts/         8 committed PNG charts, generated from real results only
```

### How to reproduce

```
python rp001_batch_acquire.py <batch_id> <start_idx> <end_idx>   # 19 batches, see RP001_PHASE2A_BATCH_TRACKER.md
python rp001_phase2a_build_panel.py
python rp001_phase2a_build_features.py
python rp001_phase2a_coverage_and_tests.py
python rp001_phase2a_confirmatory_tests.py
python rp001_phase2a_build_charts.py
```

No random seed or stochastic step anywhere in the pipeline — deterministic given the same raw data. Full detail: `RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`.

### What large data is NOT in this repo

`rp001_data/phase2a/raw/` (3.7GB of raw API responses) and `rp001_data/phase2a/processed/*.parquet` (derived datasets, up to ~760MB each) are gitignored. Every raw file is individually SHA-256-hashed in `pull_manifest.csv`; the final dataset is hashed in `rp001_dataset_snapshot.json` and `RP001_ARCHIVE_MANIFEST.json`. Nothing about the results is unverifiable — the hashes just aren't distributed via git.

### Research limitations (see `RP001_LIMITATIONS_v0.2.md` for full detail)

Market-cap/sector data unavailable at full-universe scale (2 of 7 interaction features untestable); only 69.8% of stocks with panel presence pass the coverage gate and enter the confirmatory tests; no causal identification design anywhere in the study; no portfolio, backtest, or transaction-cost analysis anywhere in RP-001.

### Research Integrity Statement

No methodology was changed after seeing any result, at any stage. Every finding that contradicts the exploratory-phase conclusions — including the central result that F_INST_01 does not replicate — is reported in full, with no adjustment or omission. All exploratory-phase documents remain unmodified as the historical record. Every deviation from the locked protocol, however small, was logged before the affected test ran. See `RP001_FINAL_ACCEPTANCE_REPORT.md`'s integrity statement for the complete version.

### Key charts

All in `rp001_data/phase2a/charts/`, generated from real computed results only (no illustrative data): universe coverage, missingness distribution, institutional-category schema history, F_INST_01 rolling IC (2012–2026), break-period comparison, liquidity groups, hypothesis-verdict scorecard, exploratory-vs-confirmatory magnitude comparison. Index and reading notes: `RP001_FIGURE_INDEX.md`.

---

*For the full FAOS/RP-001 status snapshot, see `PROJECT_STATUS.md`. For what comes next, see `ROADMAP.md` and `RP002_CANDIDATE_RESEARCH_BRIEF.md`. For version history, see `CHANGELOG.md`.*
