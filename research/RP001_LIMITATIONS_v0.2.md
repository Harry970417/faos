# RP-001 Limitations v0.2

`archive/RP001_LIMITATIONS_v0.1.md` (exploratory-phase limitations) is preserved unchanged — most of it (data-source share-count proxy, no causal design, no portfolio/backtest work) applies identically to Phase 2A and is not repeated here. This document adds what is new to Phase 2A specifically.

## The sample-scope limitation is resolved, not merely reduced

v0.1's headline limitation — "50 stocks, not the designed full universe" — **no longer applies.** Phase 2A used the actual full survivorship-bias-free TWSE+TPEx universe. This is the entire point of the confirmatory phase, and its results should be weighted accordingly heavier than the exploratory phase's.

## Market cap and sector data are unavailable at full-universe scale (Deviation D-08)

The only shares-outstanding source available (from the 50-stock exploratory work) covers just the 1,089 currently-listed TWSE companies, with corrupted text encoding, and no TPEx or delisted coverage. Re-acquiring and re-encoding a full-universe company-info source was judged out of scope rather than expanding the acquisition after seeing which features it would affect (see D-08's full reasoning). **Consequence:** F_INT_02 and F_INT_06 (the two size-based interaction features) were never tested at full-universe scale — H-C5's "Not Replicated" verdict is based on the five testable interactions, not all seven. Sector-neutral and value/growth (PBR) robustness cuts, which were informative in the exploratory phase, were not repeated.

## Coverage-gate exclusion reduces the effective confirmatory sample

Of 2,096 stocks with any institutional-data presence, only 1,462 (69.8%) pass the 80% coverage gate and enter H-C1–H-C4. This is a designed, disclosed, pre-committed threshold (not tuned post-hoc), but it means the confirmatory tests do not use the full 2,255-stock universe. A 2026-09-08 quantitative comparison of the two groups (using `rp001_confirmatory_dataset_v0.1.parquet`, `rp001_stock_coverage.csv`, and `phase2a_acquisition_universe.csv`) confirms the excluded stocks are smaller by volume/trading-value proxy (median trading value ~11x lower, median volume ~5.9x lower) and skew heavily TPEx (67.6% TWSE among included vs. 15.9% among excluded). The listing-age direction is **not** confirmed by the data — the previous wording here claimed excluded stocks are "more recently listed," but the excluded group's median listing date (2005-07-17) is in fact *older* than the included group's (2007-11-12), and the included group has a *higher* share of post-2018 listings (24.5% vs. 16.0%). A plausible mechanism: recently-listed names may have more complete institutional-data reporting from the outset, while some older, persistently low-liquidity names (disproportionately TPEx) never reached the coverage threshold. This is not explained further here — flagged as an open question, not resolved.

## Institutional-flow publication-time assumption not verified against a primary source (2026-09-08)

The confirmatory pipeline treats institutional net-buy/sell data published on session t as tradable no earlier than t+1's close (`research/rp001_build_features_v2.py`, `research/rp001_phase2a_build_panel.py`: "buy at t+1 close (first point after flow is public)"). This is a conservative assumption — one session more cautious than the common "flow is known before t+1's open" convention — but its underlying premise (TWSE/FinMind publish same-day institutional flow only after that session's close, with no scenario in which it is public later than t+1's close) has never been cross-checked against a primary publication-time source, despite `research/RP001_RISK_AND_BIAS_REGISTER.md` explicitly requiring this check as a mandatory first Execution Plan step. Because the assumption's direction is conservative (it delays usability rather than assuming earlier availability), the realistic look-ahead risk from this specific gap is low, but the check itself was never performed and should not be represented as done.

## `market_vol_regime`'s high/low split uses a full-sample median, not a rolling one (2026-09-08)

`research/rp001_phase2a_build_features.py` classifies each trading day's volatility regime (used by H-C4) by comparing that day's 20-day realized volatility to the **median volatility of the entire sample period** (~2012–2026), not a rolling or expanding-window median computed only from data available as of that day. This means an early date's "HighVol"/"LowVol" label depends on volatility that had not yet occurred at the time. This is a pre-committed, locked specification (`research/RP001_PHASE2A_PROTOCOL_LOCK.md` lists "volatility regime definition" as locked; `research/rp001_regime_robustness.py` documents it as a primary spec stated before any robustness comparison, not selected after seeing results) — so it is not data snooping — but it is a hindsight element in the regime *label* itself. It does not affect H-C1, H-C2, or H-C3 (none depend on `market_vol_regime`). It does mean H-C4's volatility-conditional findings (e.g. "Low-vol & Post-break IC ≈ 0") describe a full-sample statistical partition, not a regime an investor could have identified in real time at any given historical date, and should not be read as an immediately-actionable signal-amplification condition.

## The confirmatory tests found genuine new questions, not closed ones

H-C5's finding (4 of 5 testable interactions show a small, statistically robust residual effect) is itself a new, unexplained result — this report does not claim to know *why* the full-universe residual is nonzero when the 50-stock residual was indistinguishable from zero. Plausible candidates (pure statistical power from a much larger sample vs. a genuine full-universe-only phenomenon vs. an unmodeled confound not present in the 50-stock characterization panel) are not distinguished here — flagged as a direction for future work, not resolved.

## Statistical limitations (extending v0.1's)

The same 5-lag Newey-West specification and BH-FDR α=0.10 were applied at full-universe scale without re-testing lag sensitivity. With daily IC series now spanning ~3,470 trading days (vs. ~490 at exploratory scale) and cross-sections of up to ~1,700 stocks (vs. 50), statistical power is dramatically higher — meaning the confirmatory tests can detect much smaller effects than the exploratory tests could, which is both the point of a larger sample and a reason effect *magnitudes*, not just significance, should be weighed when interpreting H-C5's "Not Replicated" verdict (see `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`'s magnitude caveat).

## Scope limitations — unchanged from v0.1

No investment performance, portfolio construction, transaction cost, or tradeability conclusion exists anywhere in RP-001 to date, including Phase 2A.
