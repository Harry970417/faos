# RP-001 Phase 2A: Post-Exploration Prospective Confirmatory Hypotheses

**Terminology note (added per Deviation D-10, does not change any hypothesis, threshold, or method below):** these five hypotheses are a *post-exploration prospective confirmatory protocol lock* — they were formed from, and locked after, the completed exploratory-phase analysis (50-stock sample, ~2-year period), then fixed and locked (2026-07-11, `research/RP001_PHASE2A_PROTOCOL_LOCK.md`) before any full-universe confirmatory data was pulled or seen. This is prospective registration relative to the confirmatory test, not a claim that the entire RP-001 research process — including the exploratory phase that motivated these hypotheses — was pre-registered before any data was examined. The former title ("Pre-Registered Confirmatory Hypotheses") remains technically correct about the confirmatory phase but was ambiguous on this point standing alone.

Fixed after exploratory analysis and before any full-universe data is pulled. This is a confirmatory study — no new feature discovery, no new grouping hypotheses, no new breakpoint search. Only the five hypotheses below are tested.

## H-C1: Pre-break positive predictive power

F_INST_01 shows positive cross-sectional Rank IC at t+1, t+3, and t+5 during the pre-break period (dates before the locked break interval, per `research/RP001_DEVIATION_POLICY.md`'s treatment of the break date).

## H-C2: Post-break null effect

F_INST_01's IC is approximately zero (not merely smaller) during the post-break period, at t+5 (the horizon where the original effect was strongest).

## H-C3: Liquidity conditionality

F_INST_01's IC is stronger in illiquid-to-mid-liquidity stocks than in liquid stocks, using the same liquidity tercile definition as the original study (20-day rolling average trading value).

## H-C4: Volatility effect is break-conditional, not independent

The low-volatility-regime effect on F_INST_01's IC does not hold independently of the break — specifically, the Low-volatility & Post-break cell shows IC statistically indistinguishable from zero, replicating the original double-sort result.

## H-C5: No genuine interaction effects

None of the seven interaction features (F_INT_01–F_INT_07) show incremental IC beyond their constituent main effects after joint residualization.

## What is explicitly excluded from this hypothesis set

No new feature. No new grouping variable. No new breakpoint search — the break interval is inherited from the original study as a locked input (see `research/RP001_FULL_UNIVERSE_SPEC.md` and `research/RP001_DEVIATION_POLICY.md` for how the break date is handled when full-universe data may not align perfectly with the original sample's calendar). No portfolio, performance, or trading-strategy hypothesis of any kind.
