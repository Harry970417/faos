# RP-001 Limitations v0.2

`archive/RP001_LIMITATIONS_v0.1.md` (exploratory-phase limitations) is preserved unchanged — most of it (data-source share-count proxy, no causal design, no portfolio/backtest work) applies identically to Phase 2A and is not repeated here. This document adds what is new to Phase 2A specifically.

## The sample-scope limitation is resolved, not merely reduced

v0.1's headline limitation — "50 stocks, not the designed full universe" — **no longer applies.** Phase 2A used the actual full survivorship-bias-free TWSE+TPEx universe. This is the entire point of the confirmatory phase, and its results should be weighted accordingly heavier than the exploratory phase's.

## Market cap and sector data are unavailable at full-universe scale (Deviation D-08)

The only shares-outstanding source available (from the 50-stock exploratory work) covers just the 1,089 currently-listed TWSE companies, with corrupted text encoding, and no TPEx or delisted coverage. Re-acquiring and re-encoding a full-universe company-info source was judged out of scope rather than expanding the acquisition after seeing which features it would affect (see D-08's full reasoning). **Consequence:** F_INT_02 and F_INT_06 (the two size-based interaction features) were never tested at full-universe scale — H-C5's "Not Replicated" verdict is based on the five testable interactions, not all seven. Sector-neutral and value/growth (PBR) robustness cuts, which were informative in the exploratory phase, were not repeated.

## Coverage-gate exclusion reduces the effective confirmatory sample

Of 2,096 stocks with any institutional-data presence, only 1,462 (69.8%) pass the 80% coverage gate and enter H-C1–H-C4. This is a designed, disclosed, pre-committed threshold (not tuned post-hoc), but it means the confirmatory tests do not use the full 2,255-stock universe — sparser-coverage stocks (concentrated among smaller, more recently listed, and TPEx names, per the acquisition batch pattern) are systematically excluded from the hypothesis tests themselves, even though they remain in the universe-construction and coverage-audit outputs.

## The confirmatory tests found genuine new questions, not closed ones

H-C5's finding (4 of 5 testable interactions show a small, statistically robust residual effect) is itself a new, unexplained result — this report does not claim to know *why* the full-universe residual is nonzero when the 50-stock residual was indistinguishable from zero. Plausible candidates (pure statistical power from a much larger sample vs. a genuine full-universe-only phenomenon vs. an unmodeled confound not present in the 50-stock characterization panel) are not distinguished here — flagged as a direction for future work, not resolved.

## Statistical limitations (extending v0.1's)

The same 5-lag Newey-West specification and BH-FDR α=0.10 were applied at full-universe scale without re-testing lag sensitivity. With daily IC series now spanning ~3,470 trading days (vs. ~490 at exploratory scale) and cross-sections of up to ~1,700 stocks (vs. 50), statistical power is dramatically higher — meaning the confirmatory tests can detect much smaller effects than the exploratory tests could, which is both the point of a larger sample and a reason effect *magnitudes*, not just significance, should be weighed when interpreting H-C5's "Not Replicated" verdict (see `research/RP001_PHASE2A_CONFIRMATORY_RESULTS.md`'s magnitude caveat).

## Scope limitations — unchanged from v0.1

No investment performance, portfolio construction, transaction cost, or tradeability conclusion exists anywhere in RP-001 to date, including Phase 2A.
