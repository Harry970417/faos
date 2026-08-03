# RP-001 Phase 2A: Full-Universe Specification

Locked before execution. Reuses `research/RP001_RESEARCH_DESIGN.md` Section 1 as the authoritative source for universe rules — this document operationalizes those rules for actual data construction, it does not redefine them.

## Universe

TWSE (上市) + TPEx (上櫃) common stocks. ETFs and ETNs excluded. Financial holding / bank stocks excluded, using TWSE's numeric industry code (same classification source used throughout this study). Disposition-stock (處置股) exclusion rule maintained as originally designed in `research/RP001_RESEARCH_DESIGN.md` — implementation detail (exact data source for daily disposition status) to be confirmed during execution and logged as a deviation only if the original rule cannot be implemented as specified, not adjusted for convenience.

## Survivorship-Bias-Free Construction

Daily investable universe built dynamically: a stock is included on date *t* if it was actively listed (post-IPO, pre-delisting) on *t*, using `TaiwanStockDelisting` (confirmed available, 337 rows) joined against listing-date information from TWSE company info. Delisted stocks remain in the universe up to their actual delisting date, not excluded retroactively.

## IPO and Delisting Handling

A stock enters the daily universe only after satisfying the minimum-history threshold (below) from its listing date. A stock exits the universe on its confirmed delisting date; data after that date is not included.

## Liquidity and Minimum-History Thresholds

Same principle as the original design: 60-day average trading value percentile threshold (exact percentile to be calibrated on Train-period data only, per `research/RP001_RESEARCH_DESIGN.md` Section 1 — not re-optimized against Phase 2A results). Minimum 120 valid trading days of history before a stock is eligible.

## What is locked and must not be adjusted post-hoc

Liquidity tercile definition, volatility regime definition (market realized vol, 20-day window, median split as primary spec), value/growth (PBR) definition, sector classification source (TWSE numeric code), neutralization method (cross-sectional OLS residualization), multiple-testing method (Benjamini-Hochberg, α=0.10) — all inherited unchanged from the exploratory study. Any case where the full-universe data genuinely cannot support one of these definitions (e.g., a data field unavailable for TPEx stocks that was available for the 50-stock sample) must be logged as a deviation per `research/RP001_DEVIATION_POLICY.md` before proceeding, not silently substituted.

## Break Interval Treatment

The break interval (late-August to late-October 2025, point estimate 2025-09-25) is inherited as a **locked input**, not re-searched. H-C1/H-C2 test whether the *effect* replicates on each side of this pre-specified boundary — they do not re-run breakpoint detection on the full-universe data. A full-universe breakpoint search is explicitly out of scope for Phase 2A (see Section V of the protocol — "禁止事項").
