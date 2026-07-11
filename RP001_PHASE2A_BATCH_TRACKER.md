# RP-001 Phase 2A.2: Batch Acquisition Tracker

Batch size: 120 stocks (3 datasets/stock: `TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice`, `TaiwanStockPER`; full available history 2012-01-01 to present). Acquisition universe: 2,255 stock_ids (`rp001_data/phase2a_acquisition_universe.csv`) — see `RP001_PHASE2A_DEVIATION_LOG.md` D-02/D-03 for how this list was built (1,980 currently-listed via TWSE/TPEx registries + 275 delisted common stocks via `TaiwanStockDelisting` minus 62 ETF-pattern codes). 19 batches planned (18 × 120 + 1 × 95).

Each row = one batch, produced by `rp001_batch_acquire.py`. Integrity Gate must show PASS before the next batch starts — a STOP halts the table here and triggers a `RP001_LOG.md` entry plus a wait for your approval, per your instruction.

| Batch ID | Stock Range | # Stocks | Rows | Download Time | Retries | Failed Symbols | Integrity Status | Manifest Ref |
|---|---|---|---|---|---|---|---|---|
| 1 | idx 0–120 (`rp001_data/phase2a_acquisition_universe.csv` rows 0–119) | 120 | 1,769,256 | 9m47s | 3 | 104 (see below) | **STOP — Integrity Gate FAILED** | `rp001_data/phase2a/manifests/pull_manifest.csv` (batch_id=1), `batch_001_result.json` |

## Batch 1 — STOP detail

**Integrity Gate: FAILED.** Execution halted after Batch 1. Batch 2 has not been run. Full findings and disposition in `RP001_LOG.md` (this session's entry) — summarized here for the tracker.

**Failed symbols (104/360 requests):** all HTTP 402 (`"Requests reach the upper limit"`), starting at request #257 of 360 (stock 1459 onward — roughly stock 52 of the 120 in this batch, all 3 datasets for every subsequent stock). This is a **FinMind anonymous-API request quota ceiling**, not a per-stock data problem — confirmed by direct re-query returning the same 402 message. The Phase 2A.1 Capacity Estimate did not anticipate this because the 14–15 request pilot never approached the quota. **Real ceiling observed: 256 successful requests before the wall** — roughly consistent with a ~300/hour anonymous tier, partially pre-consumed by earlier pilot calls made the same day.

**Integrity Gate stop reasons (3 of 6 listed trigger conditions fired simultaneously):**
1. **Historical definition drift** — stock 1342 shows the undifferentiated `Dealer` category recurring **2019-12-17 to 2020-10-26**, five years after the "one-time 2014-12-01 cutover" concluded in Phase 2A.1's Availability Audit (which was based on a single-stock check, 1101 only). That conclusion is retracted as insufficiently general — see `RP001_LOG.md`.
2. **Unexpected missing pattern** — stock 1213: only 1,146 of 3,353 possible post-floor trading dates have *any* institutional record (2,207 dates with no row at all, scattered across the full 2012–2026 history, not a contiguous halt). This contradicts the Phase 2A.1 Data Quality Pilot's missing-value-semantics finding (explicit-zero encoding), which was based on stock 1101 only. 30 stocks in this batch exceeded the 10% missing-rate threshold.
3. **Listing-date violation** — 5 stocks flagged, largest being 1256 (first price data 2012-09-05 vs. registry listing_date 2016-03-17, a 1,289-day/3.5-year gap) — too large to plausibly be ordinary pre-listing/興櫃 trading (c.f. the ~2.5-year 6986 case documented in Phase 2A.1, itself already at the high end). Likely explanation: TPEx→TWSE market transfer, where the registry's listing_date reflects only the most recent market's listing, not original trading start under the same code — this is the previously-flagged, not-yet-resolved Availability Audit Item 8 gap materializing concretely. Not conclusively verified.

**No duplicated observations and no schema drift found in this batch** (2 of the 6 trigger conditions did not fire).
