# RP-001 Phase 2A.2-R: Historical Market Membership Audit

**Date:** 2026-07-31. Investigates whether a stock's true "first eligible date" for the Daily Investable Universe should be its *current* market's registry `listing_date`, or an earlier date reflecting formal-market history under the same `stock_id` (TPEx→TWSE transfer, etc.) — not just current listing_date, per your instruction.

## 1. Case: stock 6986 (興櫃 → TPEx formal listing)

- `TaiwanStockInfo` (live check, this session): **two** entries — `type="emerging"` (興櫃) dated 2026-06-25, `type="tpex"` dated 2026-07-31 (current). Registry `listing_date_raw` = 2026-06-26.
- Price data: continuous from 2023-11-29 (興櫃 trading) through the present. **A sharp regime break exactly at 2026-06-26**: close 54.50 (06-25) → open 45.00 (06-26), a 17.4% gap, with volume jumping from ~144K to ~2.05M shares (14×) — the classic signature of a formal listing day (price-discovery reset, liquidity surge), not ordinary trading.
- **Conclusion: 6986's pre-2026-06-26 data is 興櫃 (emerging-market) trading, not formal-market trading, and must be excluded from the Daily Investable Universe.** This confirms Phase 2A.1's original disposition (use registry `listing_date`, not first-price-date, for currently-listed stocks) was correct for this case — verified with sharper evidence (the volume/price discontinuity) than the original audit had.

## 2. Case: stock 1256 (suspected TPEx→TWSE transfer)

- `TaiwanStockInfo` (live check, this session): only **one** entry, `type="twse"`, dated 2026-07-31 (today — i.e., current status only, no historical `type` entries retained). `TaiwanStockDelisting` (live check): **empty** for 1256 — FinMind holds no delisting/transfer record for it.
- **FinMind provides no documentary confirmation either way for 1256's pre-2016 market status.** This is a real, unresolved data-availability gap, not a solved case.
- Price data: **continuous, uninterrupted daily trading from 2012-09-05 straight through 2016-03-17 and beyond** — no gap, no halt, no listing-day-style price/volume discontinuity around the registry `listing_date`. This pattern is the opposite of 6986's — consistent with an uninterrupted market transfer (trading never stopped) rather than a fresh listing (which characteristically shows a volume/price shock, per §1).
- **Assessment: TPEx→TWSE transfer is plausible and evidenced indirectly (continuous trading, no listing-day shock), but not documentarily confirmed by any FinMind endpoint checked.** Logged as an open item, not resolved by assumption.

## 3. General cases (per your requirement to check each)

| Case | Verified? | Evidence |
|---|---|---|
| Ordinary TWSE stock (e.g., 1101) | Yes | Registry listing_date 1962-02-09; continuous price history from institutional floor 2012-05-02 onward, no gap-vs-registry issue in Batch 1's Integrity Gate | 
| Ordinary TPEx stock | **Not verified — no TPEx stock present in the cached 85-stock sample** (§4 limitation, same as noted in Missingness Audit §5) | — |
| TPEx→TWSE transfer | Plausible (1256), not documentarily confirmed | §2 |
| TWSE→TPEx transfer | **Not observed in Batch 1's flagged cases; not separately tested** | — |
| 興櫃→listed (TPEx) | Confirmed (6986) | §1 |
| Delisted stock | Covered by existing Deviation D-02 (price-first-observation proxy, since registries exclude delisted names entirely) | `RP001_PHASE2A_DEVIATION_LOG.md` D-02 |
| Re-listed stock | **Not observed in the current sample** | — |
| Renamed, code unchanged | Not separately tested — `stock_id` is the study's persistent join key throughout (per Phase 2A.1's own Item 8 note), so a rename alone does not affect eligibility-date logic | `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` Item 8 |

**Four of eight required cases could not be verified with the current 85-stock, all-TWSE cached sample.** This is stated plainly, not glossed over — see §4.

## 4. Limitation

Same root cause as the Missingness Audit: Batch 1's 120-stock slice (85-86 with complete cached data) happens to be entirely low-numbered TWSE codes. **No TPEx stock, no TWSE→TPEx transfer, and no re-listed stock exists in the current sample to check.** Closing this gap requires acquiring batches from elsewhere in the 2,255-stock universe — a normal, expected outcome of resuming Phase 2A.2, not a precondition for it.

## 5. Does this block the 2025 confirmatory hypotheses?

**No — and this is the load-bearing conclusion of this audit.** The market-membership ambiguity that exists (1256's pre-2016 status, and by extension any similarly-affected stock in the full universe) only matters for determining a stock's *earliest* eligible date, which governs (a) inclusion in the full 2012-onward exploratory panel, and (b) "listing age" as a control variable. **It does not matter for whether a stock is validly in the universe as of the 2025 break-interval window** — any stock with an ambiguous pre-2016 eligibility floor has, by construction, been trading on a formal market (TWSE at minimum, per its current registry entry) for approximately a decade before 2025. Using the conservative registry `listing_date` (i.e., NOT crediting the disputed earlier period) still leaves the stock validly investable throughout 2025. **The ambiguity biases toward excluding a few extra years of pre-2025 history for affected stocks, never toward incorrectly including them in — or excluding them from — the 2025 test window itself.**

Genuinely 興櫃-sourced pre-listing data (the 6986 pattern) is the one case that *could* threaten universe integrity if mishandled, and it is already correctly excluded by the existing listing_date gate (§1) — confirmed, not merely assumed, this round.
