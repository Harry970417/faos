# Figure Manifest

11 figures, all in `figures/`, all generated directly from real computed results (no illustrative or placeholder data). Source script: `research/rp001_phase2a_build_charts.py` — re-running it regenerates every figure byte-for-byte (no randomness anywhere in the pipeline). Deeper per-figure reading notes (question answered, key finding, common misreadings): `figures/RP001_FIGURE_INDEX.md`.

| Figure | 用途 | 來源 | 使用文件 |
|---|---|---|---|
| `Figure01_UniverseCoverage.png` | Acquired universe vs. eligible-panel stock counts, by market | `rp001_data/phase2a_acquisition_universe.csv` + confirmatory panel | `research/RP001_PHASE2A_FINAL_DATASET.md` |
| `Figure02_MissingnessDistribution.png` | Per-stock institutional-data coverage distribution and the 80% gate | `research/rp001_data/phase2a/processed/rp001_stock_coverage.csv` | `research/RP001_PHASE2A_CONFIRMATORY_DATASET.md`, `research/RP001_LIMITATIONS_v0.2.md` |
| `Figure03_InstitutionalCategoryHistory.png` | Market-wide Dealer vs. split-category schema history | Confirmatory raw panel | `research/RP001_PHASE2A_DEVIATION_LOG.md` |
| `Figure04_RollingIC.png` | F_INST_01's 60-day rolling IC, full 2012–2026 history | Confirmatory dataset | `RP001_GITHUB_README_SECTION.md`, `portfolio/RP001_PORTFOLIO_ONE_PAGE.md`, `README.md` |
| `Figure05_BreakBeforeAfter.png` | Break-period IC, exploratory vs. confirmatory | Confirmatory test results + exploratory-phase figures | `research/RP001_RESULTS_TABLES_v0.2.md` |
| `Figure06_LiquidityGroups.png` | H-C3 liquidity-tercile IC and significance | Confirmatory test results | H-C3 discussion in any report |
| `Figure07_HypothesisVerdicts.png` | H-C1–H-C5 verdict scorecard | Fixed verdict labels | `README.md`, `portfolio/RP001_PORTFOLIO_ONE_PAGE.md`, interview prep |
| `Figure08_ExploratoryVsConfirmatory.png` | Five-statistic exploratory vs. confirmatory magnitude comparison | Confirmatory test results + exploratory-phase figures | `portfolio/RP001_FINAL_SHOWCASE.md` |
| `Figure09_InteractionResidualization.png` | H-C5 raw vs. residual IC, before/after residualization | Confirmatory test results | `research/RP001_RESULTS_TABLES_v0.2.md`, H-C5 discussion |
| `Figure10_DataQualitySummary.png` | Counts of data-quality issues found and resolved during acquisition | Acquisition manifests + deviation log | `applications/RP001_APPLICATION_NTUST_FINANCE.md`, `applications/RP001_APPLICATION_TAIPEITECH_IMFIN.md` |
| `Figure11_ResearchLifecycleTimeline.png` | Full RP-001 lifecycle, actual commit dates | Git commit history | Process/methodology sections, application materials |

## Naming convention

`FigureNN_ShortDescription.png`, zero-padded two-digit sequence, PascalCase description, no spaces or version-number suffixes (no `chart1.png`, `test.png`, `new_final2.png` anywhere in this repo).
