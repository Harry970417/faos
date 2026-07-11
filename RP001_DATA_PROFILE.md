# RP-001 Milestone 0A: Data Characterization

Real pull, not a spot check: 50 stocks (taiwan-attention-signal's existing curated list), `TaiwanStockInstitutionalInvestorsBuySell`, 2024-07-01 to 2026-07-09, 122,920 rows, 0 pull failures. No IC, backtest, or portfolio construction performed — characterization only.

## Correction to the Phase -1 Readiness Review

The Readiness Review flagged Chinese-text field corruption (`stock_name`, `industry_category`) as a real blocker. **That was a misdiagnosis, now corrected with evidence.** Root cause traced this session: this terminal's `stdout` encoding is `cp950` (Windows legacy Traditional Chinese codepage), not UTF-8. The raw API bytes were always valid UTF-8 — confirmed by decoding `r.content` directly and writing to a UTF-8 file, which produced perfectly correct Chinese text (verified against TWSE's official OpenAPI: 臺灣水泥, 亞洲水泥, 嘉新水泥, etc., matching real company names exactly). **The corruption only ever existed in this terminal's print output, never in the data files.** This is a real correction, not a minor caveat — it changes the Execution Readiness verdict, see bottom.

## Coverage

50/50 requested stocks returned data. 0 pull failures.

## Time Coverage

2024-07-01 to 2026-07-09, 492 unique trading days observed.

## Stock Coverage

Rows per stock: min 2,425, max 2,460, mean 2,458.4. One stock (2327, 國巨) notably short (2,425 vs. ~2,460 for most) — not investigated further at this milestone, flagged for Phase 1.

## Institutional Category Characteristics — the most important finding

| Category | Zero-rate (buy=0 AND sell=0) | Interpretation |
|---|---|---|
| Foreign_Dealer_Self | **99.99%** | Structurally near-constant / degenerate — not FinMind's original 3-way split, and not the same as Foreign_Investor |
| Investment_Trust | 2.62% | Genuinely active |
| Dealer_self | 0.85% | Genuinely active |
| Dealer_Hedging | 0.08% | Genuinely active, almost always trading |
| Foreign_Investor | 0.00% | Always active — the dominant, highest-volume category |

**This fully explains the 20% aggregate zero-rate flagged as "open" in the Readiness Review.** It was never a general data-quality problem — it's one degenerate category (Foreign_Dealer_Self) dragging the aggregate down. Confirmed at full-universe scale, not a hypothesis anymore.

**Direct consequence for Feature Specification:** Foreign_Dealer_Self carries essentially zero variance and should not be treated as a standalone factor — a feature that's constant 99.99% of the time breaks z-score standardization (near-zero denominator) and contributes no real signal.

## Missing Values (panel-level: expected stock × date × category cells)

123,000 expected cells, 122,920 present, **80 missing (0.07%)**, evenly spread across all 5 categories (16 each) — low, structurally unremarkable, likely isolated trading-halt or reporting-lapse days. Not a material concern.

## Missing Values (row-level: null buy/sell within present rows)

Zero nulls. Every present row has real, non-null buy/sell values.

## Distribution (net = buy − sell, shares)

Every category shows substantial mean/median divergence and fat tails — e.g. Foreign_Investor: mean 49,657 but median −53,198, p1/p99 at −30.3M/+33.3M shares. This is a genuine, structural feature of institutional flow data, not noise. **Direct consequence for Feature Specification:** raw z-score standardization will be distorted by extreme days; rank-based or winsorized standardization should be the *primary* choice, not a robustness-check afterthought as the original Research Design implied.

## Industry Mapping Availability

**Confirmed available via two independent sources**, both genuinely clean once decoded correctly:
- TWSE official OpenAPI (`openapi.twse.com.tw/v1/opendata/t187ap03_L`) — returns structured, complete company records including a coded `產業別` field (e.g., "01" = Cement, verified against three real cement companies returned together).
- FinMind's `TaiwanStockInfo` — also usable once the terminal-display red herring is set aside; text-based industry category, less structured than TWSE's numeric code but independently corroborating.

**Recommendation:** use TWSE's numeric industry code as the primary classification (more stable for joins than free text), FinMind's category as a cross-check.

## Execution Readiness — revised

The Phase -1 "real blocker" on Chinese-text encoding is **resolved, not open** — it was never a data problem. The remaining two Phase -1 items (missing-value characterization, data snapshot policy) are **now closed by this milestone**: missing-value pattern is fully characterized above, and the Data Snapshot is established in `RP001_DATA_SNAPSHOT.json`. No blockers remain from Phase -1.
