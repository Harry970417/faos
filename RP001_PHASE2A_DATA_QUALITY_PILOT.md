# RP-001 Phase 2A.1: Data Quality Pilot

**Status: Pilot only. 7 stocks, 2 datasets each, full available history (2012-01-01 to 2026-07-09) pulled. No full-universe download has been performed.** Script: `rp001_pilot_pull.py`. Manifest: `rp001_data/pilot/pilot_pull_log.csv`. Raw files: `rp001_data/pilot/*.json`.

## Pilot composition (diversity coverage)

| stock_id | Selected for | Result |
|---|---|---|
| 1101 | TWSE, old (1962), high-liquidity | 18,873 rows, 2 datasets |
| 6986 | TPEx, newest listing (2026-06-26) | 1,629 rows |
| 4987 | Delisted (2026-05-29) | 10,058 rows |
| 7827 | TWSE newly listed (2025-05-29) | 903 rows |
| 2891 | Financial holding (TWSE) | 18,891 rows |
| 0050 | ETF (TWSE) | 18,856 rows |
| 1264 | Small-cap / lower-liquidity | 12,913 rows |

All 8 of the 9 requested diversity dimensions are represented (different markets: TWSE+TPEx; different eras: 1962 listing to 2026 listing; delisted; newly-listed; financial; ETF; high- and low-liquidity). **Not represented**: a halted (停牌) stock and a ticker/name-change stock — no confirmed example of either was identified within the 7-stock pilot; this is a coverage gap in the pilot's diversity, not a finding that a halted/renamed stock's data is unavailable (untested, not disconfirmed).

## Verification results

**Date alignment (institutional vs. price):** For 1101 (longest history, most stringent test): 3,471 unique institutional dates vs. 3,549 unique price dates. 82 dates have price but no institutional record; of those, 78 predate the institutional-data floor (2012-05-02, see Availability Audit Item 7) and are expected. The remaining **4 residual price-only dates** (2017-04-19, 2017-04-20, 2025-08-13, 2026-06-16) and **4 institutional-only dates** with no matching price record (2016-02-05, 2019-08-24, 2019-10-26, 2026-06-19) are genuine, small, isolated single-day misalignments — roughly 0.23% of trading days for this stock. **Conclusion: date alignment must be implemented as an explicit inner join with logged drop counts, not assumed to be a clean 1:1 calendar match** — the gap rate is small but real and non-zero.

**Institutional-category breakdown:** Confirmed 6 categories across all 7 pilot stocks (`Dealer`, `Dealer_Hedging`, `Dealer_self`, `Foreign_Dealer_Self`, `Foreign_Investor`, `Investment_Trust`), not the 5 used in the original exploratory study. Root-caused as a clean one-time schema cutover on 2014-12-01 (`Dealer` → `Dealer_self` + `Dealer_Hedging`, zero overlap). Full analysis and disposition in `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` — does not require Deviation escalation because the confirmatory test window (2025 break interval) postdates the cutover by over a decade.

**Missing-value semantics:** For 1101's institutional data, `buy`/`sell` fields have **zero NaN values** (0/15,324) — but 2,491/15,324 rows (16.3%) have both `buy=0` and `sell=0` simultaneously. This confirms the dataset encodes "no institutional activity that day" as an explicit numeric zero, not a null/missing marker — consistent with the missing-state classification already established in Milestone 1B-R (`observed_zero` / `source_missing` / `non_trading_day` / `trading_halt`). The pilot confirms `observed_zero` is a real, frequently-occurring state (not a rare edge case) and must be distinguished from `source_missing` using the same logic as the original study, not re-derived from scratch.

**Trading Calendar Gate:** Not independently re-run in this pilot (that is a Phase 2A.2 execution step per `RP001_PHASE2A_EXECUTION_PLAN.md` step 8, explicitly "same methodology as the original study"). The pilot confirms the empirical trading-calendar approach remains applicable — price data's own confirmed trading days are directly observable per stock (3,549 dates for 1101 across 14+ years), same structure as the original study.

**Corporate actions (ex-dividend / split adjustment):** `TaiwanStockPrice` returns raw OHLC fields (`open`, `max`, `min`, `close`, `spread`, `Trading_Volume`, `Trading_money`, `Trading_turnover`) with **no adjusted-close or dividend-adjustment field**. This confirms the same ex-dividend/rights adjustment methodology used in the original 50-stock study (per `RP001_RISK_AND_BIAS_REGISTER.md`'s pre-identified risk on this exact issue) must be reapplied identically in Phase 2A.2 — this is a confirmed carry-forward requirement, not a newly discovered problem, and not something this raw price API resolves automatically.

**Market-cap approximation:** Shares-outstanding fields are present in the TWSE/TPEx company-info registries for common stocks (confirmed for 2891) and absent for ETFs (confirmed for 0050) — consistent with, and additional confirmation of, the ETF-exclusion mechanism in Availability Audit Item 5.

**Chinese-language fields:** Confirmed valid UTF-8 throughout (company names, industry descriptions, disposition reasons). One recurring false alarm during this audit: printing raw Chinese text directly to this Windows terminal (cp950 stdout encoding) throws `UnicodeEncodeError` or displays mangled characters — this is a terminal display artifact only, already diagnosed in Milestone 0A, reconfirmed here by successfully using the same Chinese-keyed fields (e.g., `公司代號`) programmatically without issue.

**Raw-file hashing:** SHA-256 computed for all 14 pilot files at download time, recorded in `pilot_pull_log.csv` alongside query parameters, row count, elapsed time, retry count, and file size — this is the working pattern the Snapshot Architecture (`RP001_PHASE2A_DATA_SNAPSHOT_SPEC.md`) formalizes for full-universe scale.

**Repeated-download consistency:** Re-pulled 1101's institutional data independently; resulting SHA-256 (`677cbeda...16` — full hash in `pilot_pull_log.csv`) is **byte-identical** to the original pilot pull. Confirms deterministic downloads for this dataset/stock at this point in time — supports the Snapshot Architecture's reproducibility assumption, though this is a single re-pull on a single stock/dataset, not an exhaustive consistency guarantee across the full universe.

## Pilot-level summary

| Metric | Value |
|---|---|
| Requests | 14 (7 stocks × 2 datasets) |
| Successes | 14/14 (HTTP 200) |
| Retries | 0 |
| Total rows | 82,123 |
| Total API-active time | 9.56s |
| Total file size | 9,789,110 bytes (9.79 MB) |

These are the real per-stock ingredients used in `RP001_PHASE2A_CAPACITY_ESTIMATE.md`'s full-universe extrapolation.
