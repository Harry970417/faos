# RP-001 Phase 2A.2-R: Institutional Missingness Semantics Audit

**Date:** 2026-07-31. **Sample:** 85 stocks with complete cached Price + Institutional data from Batch 1 (all TWSE — see §5 limitation). No new API calls. Script: `rp001_missingness_audit.py`; outputs in `rp001_data/phase2a/audits/`.

## 1. Method

For each stock: eligible trading dates = every date the stock's own `TaiwanStockPrice` data has a row, restricted to on/after the system-wide institutional-data floor (2012-05-02, established in Phase 2A.1). Missing dates = eligible dates with zero institutional rows of any category. This is a genuine per-stock trading calendar (not a shared market calendar), so it correctly excludes real non-trading days without needing a separate calendar source.

## 2. Missing-rate distribution (85 stocks, full available history)

| Statistic | Value |
|---|---|
| Mean | 10.29% |
| Median | 3.05% |
| Max | 65.82% (stock 1213) |
| Stocks > 10% missing | 30 / 85 (35.3%) |
| Stocks > 20% missing | 16 / 85 (18.8%) |
| Stocks ≤ 5% missing | 46 / 85 (54.1%) |

This **confirms, at 85-stock scale, that Batch 1's "unexpected missing pattern" trigger was real and broadly distributed** — not an artifact of one or two outlier stocks. A third of the sample exceeds a 10% missing-rate bar.

## 3. What kind of missing?

Two genuinely different phenomena, kept separate rather than lumped together as "missing":

- **`observed_zero`** — a `Foreign_Investor` row *exists* for the date with `buy=0, sell=0`. Confirmed real on 84/85 stocks (mean 1.76% of a stock's Foreign_Investor rows, up to 11.6% for stock 1418). This validates Phase 2A.1's single-stock (1101) "explicit zero encoding" finding as a real, generalizable FinMind behavior, not a one-stock artifact — see `rp001_data/phase2a/audits/foreign_investor_explicit_zero_check.csv`.
- **`source_missing`** — no institutional row of any category exists for an eligible trading date, and price data shows the stock actually traded (`Trading_Volume > 0`). This is the dominant category by far: **28,631 of 29,103 total missing dates (98.4%)** across the 85-stock sample.
- **`trading_halt`** — price row exists with `Trading_Volume = 0` (the stock's own market was suspended that day). Explains only **472 of 29,103 missing dates (1.6%)**.
- **`non_trading_day` / `pre_eligible` / `market_transfer`** — not directly computable from this audit alone; a stock's own price-date list already excludes true non-trading days and dates before its own first observation by construction, so these categories are largely folded into "not eligible" rather than "missing." `pre_eligible` and `market_transfer` require the historical market-membership model built in `RP001_MARKET_MEMBERSHIP_AUDIT.md` (Task 4) to identify — not yet cross-referenced here; flagged as a follow-up, not silently assumed absent.
- **`structural_omission` / `unmatched_unknown`** — not separately identified in this pass; the entire `source_missing` bucket (98.4% of gaps) is, honestly, of unknown root cause at this point. **This is stated as a limitation, not resolved by assumption.** FinMind gives no error code or flag distinguishing "institutional data was never collected this day" from any other omission reason.

**Bottom line: the dominant missing-data phenomenon (`source_missing`, 98.4% of gaps) is real, unexplained by halts, and must not be treated as zero.** Per your explicit prohibition, none of these 28,631 gaps have been or will be filled with 0.

## 4. Grouping

- **By market:** all 85 sampled stocks are TWSE (see §5 — Batch 1's first 120 acquisition-universe rows happen to be entirely low-numbered TWSE codes; **no TPEx stock is in this sample**, so a TWSE-vs-TPEx missingness comparison cannot be made yet).
- **By year, category, listing age, liquidity:** per-stock summary (`missingness_summary_per_stock.csv`) and block-level detail (`missingness_blocks.csv`) support these cuts; a full multi-dimensional breakdown is deferred to full-universe scale (Phase 2A.2 proper) where TPEx and a wider listing-age/liquidity spread actually exist to compare — cutting 85 same-market, mostly-old, low-numbered stocks by "liquidity group" or "listing age" now would not be representative of the real universe and risks a false sense of having answered this section.

## 5. Explicit limitation: sample is not market-representative

Batch 1's acquisition order (by `stock_id` ascending) means the 85-stock cached sample is entirely TWSE, entirely low-numbered (mostly listed decades ago). **No conclusion in this audit about missingness "by market" or "by listing age" should be read as covering TPEx or newly-listed stocks** — those require batches drawn from elsewhere in the 2,255-stock universe, which have not been downloaded.

## 6. Stock 1213 — full case timeline

**Missing rate: 65.82%** (2,207 of 3,353 eligible dates), the worst in the sample. 392 discrete missing blocks — not one contiguous gap, but a chronically intermittent coverage pattern spanning the stock's entire history (2012-05-02 to 2026-07-09).

| Rank | Block | Length (trading days) |
|---|---|---|
| 1 | 2022-02-11 to 2022-10-12 | 167 |
| 2 | 2021-05-27 to 2022-01-18 | 164 |
| 3 | 2022-12-07 to 2023-05-16 | 99 |
| 4 | 2020-02-26 to 2020-07-16 | 96 |
| **5** | **2025-09-26 to 2026-02-05** | **89** |
| 6 | 2023-09-04 to 2023-12-18 | 73 |
| 7 | 2026-02-09 to 2026-05-25 | 65 |
| 8 | 2020-08-21 to 2020-11-18 | 61 |
| 9 | 2019-09-24 to 2019-12-10 | 53 |
| 10 | 2021-03-02 to 2021-05-12 | 49 |

Full 392-block list: `rp001_data/phase2a/audits/stock_1213_missing_blocks_full.csv`.

**Decision-relevant finding, not buried in the appendix:** block #5, **2025-09-26 to 2026-02-05, sits directly inside and just after the locked break-interval window** (2025-08-01 to 2025-10-31 padded range; point estimate 2025-09-25). Stock 1213 has essentially **no institutional data for the second half of the confirmatory test's most important period.** Of the 39 total halt-explained missing dates in the whole 85-stock sample's tally, none are attributed to 1213 specifically in this block — checked and none of 1213's missing dates in this block show `Trading_Volume = 0`, so this is `source_missing`, not a trading halt. Root cause unknown. **This single stock alone would materially degrade or invalidate any break-interval test that includes it without a coverage rule** — see `RP001_MISSINGNESS_POLICY.md` for the resulting rule and `RP001_ANOMALY_REGISTER.md` for the formal anomaly entry.

## 7. Re-audit of Phase 2A.1's missingness conclusion

Phase 2A.1's Data Quality Pilot concluded institutional missingness follows "explicit zero encoding," based on stock 1101 alone. **Revised, not retracted:** explicit-zero encoding *is* real and present in 84/85 stocks (§3) — that part generalizes. What does **not** generalize is the implicit assumption that missingness is otherwise negligible: 1101 itself has a low missing rate (not in the top-10 list), and the pilot did not surface that `source_missing` (not `observed_zero`) is the dominant gap type sample-wide, nor that it reaches 65.82% for at least one stock. See `RP001_PHASE2A1_REAUDIT.md` item for the formal Confirmed/Revised/Retracted classification.
