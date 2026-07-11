# RP-001 Phase 2A.1: Daily Investable Universe — Spec Validation

**Status: Spec-validation only. No full-universe daily universe has been constructed or run.** This document confirms the exclusion/inclusion rules in `RP001_FULL_UNIVERSE_SPEC.md` can be mechanically implemented against real data, using the pilot stocks and registry data pulled during this audit — it does not execute the full-universe build (that is Phase 2A.2, step 6).

## Rules under validation (from `RP001_FULL_UNIVERSE_SPEC.md`)

A stock is in the investable universe on date *t* if: currently/actively listed on *t* (post-IPO, pre-delisting), non-ETF, non-financial, non-disposition, sufficient history (≥120 valid trading days), meets the liquidity threshold, normal trading status — with none of these determined using information not available as of *t*.

## Per-rule validation

**Listed / not-yet-delisted on date t:** Implementable — join `TaiwanStockDelisting` (337 rows, confirmed complete across old and recent examples, see Availability Audit Item 2) against listing dates (TWSE `t187ap03_L` / TPEx `mopsfin_t187ap03_O`, Item 1). Mechanism: stock in universe iff listing_date ≤ t < delisting_date (delisting stock excluded starting its confirmed delisting date, not before).

**Non-ETF:** Implementable, and verified via the ETF example itself — 0050 is absent from both company registries (Availability Audit Item 5), so "present in company registry" is a sufficient ETF filter with no separate list needed.

**Non-financial:** Implementable via TWSE numeric industry code (verified populated for 2891, Availability Audit Item 4), with the residual caveat that full-period taxonomy stability was spot-checked, not exhaustively verified across all 11 years.

**Non-disposition:** **Not cleanly implementable as a full daily history** — this is Deviation D-01 (`RP001_PHASE2A_DEVIATION_LOG.md`). The rule itself is well-defined; the data source to evaluate it day-by-day across history does not currently exist in a form this audit located.

**Sufficient history (≥120 trading days) / liquidity threshold:** Mechanically implementable from price data alone (available far enough back for this purpose per Availability Audit Item 7) — no data-availability blocker found.

## Look-ahead bias check: publication-timing risk in listing/delisting/disposition status

This was specifically flagged by the governing instruction as a risk to verify, not assume. Findings:

- **Listing status:** the listing_date field is the company's officially effective listing date (verified as a real, static, backward-looking field for both TWSE and TPEx sources) — using it to gate day-*t* eligibility does not leak future information, because it is set once at IPO and does not change based on later information.
- **Delisting status:** same structure — `TaiwanStockDelisting`'s delisting date is a fixed historical fact once it occurs; using it to exclude a stock starting exactly that date does not leak information about *future* delisting into earlier dates, provided the daily universe construction strictly uses "delisting_date > t" (not "will eventually delist") as the inclusion test. This is a construction-discipline requirement, not a data-availability gap — noted here for Phase 2A.2 implementation, not a finding that blocks the gate.
- **Disposition status:** the timing-risk question is currently moot given Deviation D-01 — there is no verified daily disposition-status source to even have a publication-timing property. Deferred until/unless D-01 is resolved with a genuine historical source.

## Material finding: pre-listing (興櫃) trading history embedded under the same stock_id

Discovered while checking two newly-"listed" pilot stocks' actual price-data date ranges against their official listing dates:

- Stock 7827 (official TWSE listing 2025-05-29 per company registry): price data available from **2025-06-20** — actually *after* its listing date in this case, no anomaly.
- Stock 6986 (official TPEx listing 2026-06-26 per company registry): price data available from **2023-11-29**, over two and a half years *before* its official listing date, n=631 rows.

**Interpretation:** 6986's pre-listing data almost certainly reflects 興櫃 (emerging board) trading under the same `stock_id`, which FinMind/TWSE continue to serve under one continuous code across the emerging→listed transition. **This is a real construction hazard, not a data-quality defect**: a naive universe rule that includes a stock "wherever its data exists" would incorrectly include ~2.5 years of pre-listing (emerging-board, non-investable-on-TWSE-terms) trading days for 6986, materially violating the survivorship-bias-free / no-future-information design intent even though no single day's data is wrong.

**Resolution (spec clarification, not a deviation):** the Daily Investable Universe rule must gate strictly on `listing_date` (Item 1's TWSE/TPEx company-registry field) — i.e., "data exists for stock_id on date t" is **not** sufficient for inclusion; "official listing_date ≤ t" is the actual test, exactly as already specified in `RP001_FULL_UNIVERSE_SPEC.md`. This finding does not change the locked spec — it confirms why the spec's listing-date gate (rather than a data-presence gate) is necessary, and flags it as a concrete implementation trap to guard against explicitly in the Phase 2A.2 build (a unit test comparing "first date with data" vs. "listing_date" per stock, flagging any stock where they differ by more than a small tolerance, is recommended before universe construction is trusted).

## Validation verdict

All rules are mechanically specifiable and implementable **except** non-disposition (Deviation D-01, logged, non-blocking per the Deviation Policy's own criteria). The pre-listing-data hazard is a confirmed real risk with a concrete example (6986) and is resolved by strict adherence to the already-locked listing_date gate — no spec change required, only an implementation-discipline note for Phase 2A.2.
