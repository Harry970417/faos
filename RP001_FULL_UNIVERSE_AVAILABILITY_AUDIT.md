# RP-001 Phase 2A.1: Full-Universe Availability Audit

> **Correction (logged during Phase 2A.2 Batch 1, do not delete or edit the sections below — this note stands alongside them for the audit trail):** the "Institutional-flow category schema change" finding below concluded the `Dealer` → `Dealer_self`+`Dealer_Hedging` split was a clean, universal, one-time cutover on 2014-12-01, based on a single-stock check (1101 only). Batch 1 of Phase 2A.2 found stock 1342 showing undifferentiated `Dealer` rows again from **2019-12-17 to 2020-10-26** — five years after the claimed cutover. **The "clean one-time cutover, non-material, does not require escalation" conclusion below is retracted.** This is now an open, unresolved historical-definition-drift question — see `RP001_LOG.md` (Phase 2A.2 Batch 1 STOP entry) and `RP001_PHASE2A_DEVIATION_LOG.md` for current status. Two other single-stock-based conclusions in this document (missing-value semantics: "explicit zero encoding," based on 1101; the ~2.5-year pre-listing gap being the expected magnitude, based on 6986) were also contradicted by Batch 1 evidence from other stocks (1213, 1256) and should not be relied on as universal until re-verified at scale.

**Status: Complete.** All 10 items verified with live API calls executed during this audit (2026-07-11), not assumed from documentation or memory. Raw evidence retained under `rp001_data/` (see file references per item).

## 1. TWSE/TPEx historical listed stock list availability

**Verified available.** TWSE OpenAPI `t187ap03_L` (company basic info, MOPS-sourced) returns 1,089 rows with a real 上市日期 (listing date) field, range 1962–2026. TPEx OpenAPI `mopsfin_t187ap03_O` (discovered via `swagger.json` after the naive endpoint guess `v1/t187ap03_O` returned an empty body) returns 891 rows with a `DateOfListing` field, range 1990-06-25 to 2026-06-26. Saved: `rp001_data/twse_company_info.json`, `rp001_data/tpex_company_info.json`.

FinMind's own `TaiwanStockInfo` dataset (4,276 rows; type breakdown twse=2,380 / tpex=1,367 / emerging=529) was checked as an alternative and **rejected as the listing-date source** — its `date` field is unreliable (does not consistently represent IPO/listing date). TWSE/TPEx OpenAPI company-info endpoints are the source of record for listing dates going forward.

## 2. Delisted stocks + delisting dates completeness

**Verified available.** `TaiwanStockDelisting` returns 337 rows (already noted in `RP001_FULL_UNIVERSE_SPEC.md`), spot-checked against real examples spanning the full range: stock 6806 delisted 2026-06-23 (recent), stock 1505 delisted 2001-01-20 (old) — both returned correctly, confirming the dataset is not truncated to recent years only.

## 3. IPO/listing dates availability

**Verified available** — same sources as Item 1. Both TWSE and TPEx expose real per-company listing dates, not just a coarse "currently listed" flag.

## 4. Financial-stock identification field stability

**Verified, with one open sub-item.** TWSE numeric industry code (used throughout the original 50-stock study) is present and populated for a spot-checked financial stock (2891) in `t187ap03_L`. Field structure did not show signs of definitional churn within the currently-available snapshot. **Not yet verified**: whether the industry-code *taxonomy itself* has been revised across the full 2015–2026 window (e.g., a company reclassified mid-period). This is a residual, low-probability risk carried into Phase 2A.2 rather than a blocking finding — industry classification changes are rare relative to daily price/institutional-flow data and TWSE's numeric codes have been stable in practice for the tested stock.

## 5. ETF/non-common-stock identification method

**Verified via a real negative result, not an assumption.** Stock 0050 (an ETF) is **absent** from the TWSE company registry (`t187ap03_L`) entirely — confirmed by direct set-membership check (`'0050' in ids` → `False`), while 2891 (a financial holding company) **is** present (`True`). This is a clean, structural distinction: `t187ap03_L` covers operating companies (issuers of common equity), not ETFs, because ETFs are not the kind of entity that dataset is registering. Practical consequence: the exclusion rule "not in the TWSE/TPEx company registry" mechanically doubles as the ETF filter — no separate ETF list is needed, and no shares-outstanding / market-cap approximation is possible for ETFs via this source (expected and consistent with ETFs being excluded from the universe by design, not merely by convention).

## 6. Disposition-stock (處置股) historical data availability

**Not available as a historical archive — logged as Deviation D-01.** TWSE OpenAPI `/announcement/punish` returns only 3 rows as of this audit — a small, current/near-term snapshot, not a queryable historical range. No endpoint discovered during this audit provides full-history daily disposition status. See `RP001_PHASE2A_DEVIATION_LOG.md` D-01 for the full reasoning and impact assessment (does not touch F_INST_01, rank normalization, return horizon, or the break interval — does not trigger the Escalation clause).

## 7. Daily volume/price/institutional/shares-outstanding historical coverage

**Verified, with one hard floor and one hard start-date reconciliation.**

- **Institutional flow** (`TaiwanStockInstitutionalInvestorsBuySell`): earliest available date confirmed as **2012-05-02, system-wide** — verified identically for two independent stocks (1101, 2330) across multiple probe date-ranges extending back to 2005; all queries before 2012-05-02 return zero rows. This is a real data floor, not a query-parameter artifact.
- **Price** (`TaiwanStockPrice`): available substantially earlier than 2012 for long-listed stocks (e.g., 1101 back to the 1960s per its listing date), so institutional flow is the binding constraint on any feature requiring both series jointly.
- **Shares outstanding / market-cap proxy**: available via the TWSE/TPEx company-info endpoints for common stocks (confirmed present for 2891), unavailable for ETFs (confirmed absent for 0050, see Item 5) — consistent with ETFs' planned exclusion.
- **Reconciliation against the pre-registered period** (`RP001_RESEARCH_DESIGN.md` §2: "建議期間 2015–2026，實際起點依資料可得性調整"): the 2012-05-02 institutional-data floor is **before** the suggested 2015 start, so **no deviation is required on this point** — the pre-registered period is fully executable as originally suggested.

## 8. Ticker code changes / company renames / market transfers

**Partially verified — residual gap, non-blocking.** TWSE/TPEx company-info endpoints key on `公司代號`/stock code, which is FinMind's and this study's persistent join key throughout (F_INST_01 and all downstream tests are defined on `stock_id`, never on company name). No dedicated historical rename/transfer crosswalk was located or exhaustively tested during this audit — this is the one audit item not brought to full closure. Expected impact is low: the study's identity key (`stock_id`) is stable under a rename even when the display name changes, and market transfers (TPEx→TWSE, the most common transfer type) do not change `stock_id`. This residual gap is logged as a known limitation to revisit if any full-universe anomaly (e.g., a stock_id with two inconsistent registry entries) surfaces during Phase 2A.2, not as a blocking finding now.

## 9. API query limits / rate limits / retry needs

**Verified via the real pilot pull, not a rate-limit stress test.** The 7-stock, 14-request pilot (`rp001_pilot_pull.py`, moderate pace, 0.4s inter-request delay) completed with **0 retries, 0 failures, 14/14 HTTP 200** across both `TaiwanStockInstitutionalInvestorsBuySell` and `TaiwanStockPrice`. No rate-limiting behavior (HTTP 429, throttling, or degraded response) was observed at this scale. A dedicated high-throughput stress test (the pace required for a ~2,000+ stock full pull) was **not** run in this audit — the pilot's pace-per-request is the basis for the Capacity Estimate's time projection, with retry-cost margin built in per `RP001_PHASE2A_CAPACITY_ESTIMATE.md`, not a verified upper bound on FinMind's actual rate limit.

## 10. Earliest common usable research start date

**Determined: 2012-05-02** is the system-wide institutional-flow floor (Item 7). Since this is earlier than the pre-registered period's suggested 2015 start, **the pre-registered 2015 start date is confirmed executable as-is** — no adjustment or deviation needed on the research period's starting boundary.

## Material finding surfaced during this audit (not one of the 10 checklist items, but directly relevant to Item 7 and to universe/feature construction): institutional-flow category schema change

The Data Quality Pilot (`RP001_PHASE2A_DATA_QUALITY_PILOT.md`) found a **sixth** institutional-investor category, `'Dealer'`, not present in the original 50-stock exploratory-phase data (which used 5: `Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer_self`, `Dealer_Hedging`). Investigation (stock 1101, full 2012–2026 history) resolved this as a **clean, one-time schema cutover, not an ongoing inconsistency**:

- `'Dealer'` appears **only** 2012-05-02 to 2014-11-28 (642 rows).
- `'Dealer_self'` and `'Dealer_Hedging'` appear **only** 2014-12-01 onward (2,829 rows each).
- **Zero calendar-date overlap** between `'Dealer'` and its two successor categories — confirmed by pivoting on date and checking no row has all three populated simultaneously.

**Assessment:** this is a real, irreconcilable definitional change in the institutional-data field across years (the combined "Dealer" category was split into self-trading and hedging sub-categories on 2014-12-01) — exactly the category of issue the governing instruction flagged as a mandatory Deviation Review trigger. **However, it does not require escalation**, because:
1. The confirmatory test window is anchored to the pre-registered break interval (late-Aug to late-Oct 2025, point estimate 2025-09-25, per `RP001_FULL_UNIVERSE_SPEC.md`) — over a decade after the 2014-12-01 cutover.
2. F_INST_01's locked definition uses `Dealer_self` and `Dealer_Hedging` as separate inputs, which is exactly what exists throughout the entire confirmatory test window.
3. The only way this schema change becomes live is if a feature or universe rule needs institutional data from 2012–2014 specifically — no locked spec item does.

**Disposition:** logged here as a documented, resolved audit finding, not escalated to the Deviation Log, because it does not touch F_INST_01's definition, rank normalization, return horizon, or the break interval boundary within the actual data range the confirmatory tests will use. If Phase 2A.2's minimum-120-trading-day history requirement ever pulls a newly-listed stock's *institutional* eligibility window back into the 2012–2014 range (implausible given the break interval is in 2025, but stated for completeness), this disposition should be re-examined.

## Audit summary

| Item | Status |
|---|---|
| 1. TWSE/TPEx listing lists | Verified available |
| 2. Delisted stocks + dates | Verified available |
| 3. IPO/listing dates | Verified available |
| 4. Financial-stock field stability | Verified for spot-check; full-period taxonomy stability not exhaustively tested (low-risk residual) |
| 5. ETF identification | Verified — absence from company registry is the mechanism |
| 6. Disposition-stock history | **Not available — Deviation D-01 logged** |
| 7. Full historical coverage | Verified — institutional floor 2012-05-02, before pre-registered 2015 start |
| 8. Ticker/name/market-transfer changes | Partially verified — residual gap, non-blocking |
| 9. Rate limits | No throttling observed at pilot scale; full-scale stress test not run |
| 10. Earliest usable start date | 2012-05-02 (pre-registered 2015 start confirmed executable) |
| — Institutional category schema change | Found, resolved, does not require escalation |
