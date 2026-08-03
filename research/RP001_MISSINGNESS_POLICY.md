# RP-001 Phase 2A.2-R: Missingness Policy

**Date:** 2026-07-31. Proposed rule set, stated **before** any confirmatory test is run on full-universe data — consistent with the Deviation Policy's before/after discipline even though this isn't formally a spec deviation (the locked protocol documents do not define a coverage threshold at all; checked directly, no match for "coverage" or "missing" in `research/RP001_FULL_UNIVERSE_SPEC.md`, `research/RP001_PHASE2A_CONFIRMATORY_PROTOCOL.md`, or `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md`). This document fills that gap; it is a new operational rule, not a change to anything already locked.

## Rule 1 — never impute

A missing institutional-data date (`source_missing`, `trading_halt`, or any other missing category) produces **`NaN`** for that stock's F_INST_01 (and any other institutional feature) on that date — never `0`. This applies uniformly regardless of missing-type classification. Per your explicit instruction, this is non-negotiable and requires no further justification.

## Rule 2 — cross-sectional handling

A stock-date with `NaN` F_INST_01 is **dropped from that date's cross-section** for rank computation and IC calculation — it does not participate, is not assigned a default rank, and does not shrink other stocks' ranks. This is the standard, conservative approach for panel data with genuine gaps and requires no deviation from the locked rank-normalization method (it changes *which rows* enter the rank, not the rank formula itself).

## Rule 3 — stock-level coverage gate for the confirmatory test window

**Proposed threshold: a stock must have institutional data on at least 80% of its eligible trading dates within the confirmatory test's relevant sample window (the period spanning the pre/post break comparison, not full 2012–2026 history) to be included in H-C1–H-C4 at all.** Below 80%, the stock is excluded from the confirmatory universe entirely for the affected window (not merely NaN'd date-by-date) — a stock this sparse cannot support a within-stock pre/post comparison.

**Why 80%, and why this is not post-hoc tuning:** this is a standard minimum-completeness convention in empirical panel finance (comparable to, e.g., minimum-trading-days-per-year screens used broadly in the literature), chosen before computing what fraction of the 85-stock sample would pass it. It was **not** picked by checking which threshold keeps the most stocks or produces a nicer number — the audit numbers in §2 of `research/RP001_INSTITUTIONAL_MISSINGNESS_AUDIT.md` were already computed over full history before this threshold was set, and this document does not go back and adjust the 80% figure after seeing them.

**Descriptive check (not calibration):** applying 80% coverage to the 85-stock sample's *full-history* missing rate (not yet the narrower test-window rate, which requires the market-membership work in Task 4 to compute correctly) would exclude roughly 16-19 of 85 stocks (those with >20% missing rate, §2). This is reported transparently, not hidden — a real cost of the rule, evaluated after the fact, not a target it was designed to hit.

## Rule 4 — explicit-zero is not missing

`observed_zero` dates (a real row with `buy=0, sell=0`) are **kept as-is**, F_INST_01 = 0 for that stock-date, no special handling — this is a genuine, reported "no net flow" observation, not a data gap.

## Rule 5 — unresolved missing-type categories are treated conservatively

`market_transfer` and `pre_eligible` dates cannot yet be distinguished from generic `source_missing` (Task 4 dependency, not yet cross-referenced — see `research/RP001_INSTITUTIONAL_MISSINGNESS_AUDIT.md` §4). Until that cross-reference is done, all unclassified gaps are treated as `source_missing` under Rule 1/Rule 2 (NaN, dropped) — the conservative default, since misclassifying a genuine gap as an artificially-benign category (e.g., silently assuming it's just a market holiday) would risk exactly the kind of unverified assumption your instructions prohibit.

## Rule 6 — stocks with 100%-relevant-window loss are excluded, not asterisked

If a stock's coverage gate failure (Rule 3) means it has **zero** usable institutional observations inside the break-interval comparison window specifically (as Stock 1213 appears to, per its block #5 in the missingness audit, pending exact window-boundary confirmation), it is excluded from H-C1–H-C4's sample for that window, full stop — not included with an asterisk, not partially weighted. `research/RP001_ANOMALY_REGISTER.md` logs this per-stock, so the exclusion is auditable, not silent.

## What this policy does NOT do

- Does not touch F_INST_01's definition, rank normalization method, return horizon, or the break interval's boundary dates.
- Does not exclude any stock from the *universe* (market membership / investability) — only from the *confirmatory sample* for hypotheses that need institutional-data completeness. A stock failing Rule 3 can still appear in market-membership/universe-construction outputs; it just doesn't contribute an F_INST_01 observation.
- Is not itself an Escalating Deviation — it fills a gap the locked protocol left open, rather than changing something the protocol specified.
