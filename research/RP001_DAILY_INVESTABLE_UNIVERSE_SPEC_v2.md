# RP-001 Daily Investable Universe — Spec v2

**Date:** 2026-07-31. Supersedes the listing-date handling implicit in `research/RP001_FULL_UNIVERSE_SPEC.md` v1 with the evidence from `research/RP001_MARKET_MEMBERSHIP_AUDIT.md`. **Does not change any locked item** (F_INST_01 definition, rank normalization, return horizon, break interval, liquidity/volatility definitions) — this is universe-construction detail only, explicitly carved out as non-locked in `research/RP001_PHASE2A_PROTOCOL_LOCK.md`.

## Eligibility rule

A stock is in the Daily Investable Universe on date `t` if and only if:

1. `t >= max(institutional_floor, stock_eligibility_start)`, where `institutional_floor = 2012-05-02` (system-wide, per Phase 2A.1) and `stock_eligibility_start` is defined per §2 below.
2. `t < delisting_date` (if the stock has since delisted).
3. Price data exists for the stock on `t` with `Trading_Volume > 0` (excludes halted-that-day and non-trading dates automatically, per stock).
4. Not currently on a disposition-stock (處置股) list per the D-01 snapshot proxy (unchanged from v1 — no better source found this round either).

## §2 — `stock_eligibility_start`, by case

| Case | Rule | Source |
|---|---|---|
| Currently-listed, registry `listing_date` available | `= listing_date` (registry value, unchanged from v1) — **not** first-price-observation date, since pre-listing/興櫃 trading (confirmed real via the 6986 price/volume discontinuity test) must be excluded | `research/RP001_MARKET_MEMBERSHIP_AUDIT.md` §1 |
| Delisted, no registry entry | `= first price-observation date` (Deviation D-02, unchanged) | `research/RP001_PHASE2A_DEVIATION_LOG.md` D-02 |
| Suspected market-transfer stock (large gap between first price date and registry `listing_date`, e.g. 1256) | `= listing_date` (conservative — same as the ordinary case above), **NOT** the earlier first-price date, because the transfer cannot be documentarily confirmed (§2 audit) | `research/RP001_MARKET_MEMBERSHIP_AUDIT.md` §2, §5 |

**Practical effect of the conservative choice for suspected-transfer stocks:** these stocks lose a few years of pre-listing-date history from the exploratory-panel universe (e.g., 1256 loses 2012-09-05 to 2016-03-16). This is the same "biases toward under-inclusion, not fabrication" direction already established for other deviations, and — per §5 of the Market Membership Audit — has **zero effect on the 2025 confirmatory test window**, since these stocks are unambiguously investable via their current market for years before 2025 regardless of which floor is used.

## §3 — Regime-break heuristic (new, diagnostic only, not a gating rule)

A stock's transition into a new registry `listing_date` can be checked for a "loud" listing-day signature: same-day price gap exceeding roughly 10% combined with a volume multiple of roughly 5× the preceding 5-day average. Observed in 6986 (17.4% gap, 14× volume) and absent in 1256 (no gap, ordinary volume) around their respective transition dates. This is a **diagnostic aid for flagging future ambiguous cases during full-universe acquisition**, not a formal eligibility gate — it did not change any eligibility decision in this document; both cases already resolved to the same rule (§2) regardless of the heuristic's reading.

## §4 — What remains unverified (carried forward, not hidden)

TPEx stocks, TWSE→TPEx transfers, and re-listed stocks have **zero representation** in the current 85-86-stock cached sample — this rule is applied uniformly by construction (registry `listing_date` as the default floor) but has not been empirically stress-tested against any of those three case types. Flagged for attention during the first batches of full-universe acquisition that include TPEx-numbered stocks.
