# RP-001 Phase 2A.2-R: Feature Impact Matrix (Institutional Category Schema Findings)

**Date:** 2026-07-31. Companion to `research/RP001_INSTITUTIONAL_SCHEMA_AUDIT.md`. Classification categories per your instruction: Unaffected / Recoverable by deterministic mapping / Requires deviation / Not constructible.

| Feature / Hypothesis | Depends on Dealer categories? | Classification | Basis |
|---|---|---|---|
| **F_INST_01_foreign** | No — Foreign_Investor only | **Unaffected** | `FEATURE_REGISTRY.md` line 11; confirmed clean on Foreign_Investor across all 86 sampled stocks (no drift, no missingness, no name variants — §5 of Schema Audit) |
| F_INST_02_trust | No — Investment_Trust only | Unaffected | Same registry; Investment_Trust not touched by this audit's findings |
| F_INST_03_dealer_self | Yes — Dealer_self only | **Recoverable by deterministic mapping, with a caveat** | Dealer_self is cleanly reported post-2014-12-01 for 85/86 stocks with zero overlap against undifferentiated `Dealer` (§3). One stock (1342) has a 2019-2020 window where Dealer_self is replaced by undifferentiated `Dealer` — those specific stock-dates cannot be split and must be treated as missing for F_INST_03, not zero-filled. Already **Inconclusive** status per Feature Registry — not used by any locked hypothesis, so this caveat has no confirmatory impact |
| F_INST_04_dealer_hedge | Yes — Dealer_Hedging only | Recoverable by deterministic mapping, same caveat as F_INST_03 | Same reasoning. Already **Rejected** status — no confirmatory impact |
| F_INST_05_aggregate / F_INST_06_value_proxy | Yes — sums in Dealer_self + Dealer_Hedging | Recoverable by deterministic mapping, same caveat | Both already **Deprecated** per Feature Registry — no confirmatory impact |
| F_INST_07_flow_to_volume | Indirectly, via F_INST_05 | Recoverable by deterministic mapping | **Secondary Candidate** status, not used in H-C1–H-C4; only touches H-C5's residualization set (see below) |
| F_INT_01–F_INT_07 (all interaction features) | Indirectly, via F_INST_05 for F_INT_01–03; directly Foreign-based for F_INT_04–07 | Unaffected (F_INT_04–07, Foreign-based) / Recoverable (F_INT_01–03, via F_INST_05) | All seven already **Confirmed Artifact** or **Experimental-per-instruction** per Feature Registry — no confirmatory hypothesis depends on their raw signal being real |
| **H-C1, H-C2, H-C3, H-C4** | No — all defined directly on F_INST_01 | **Unaffected** | `research/RP001_CONFIRMATORY_HYPOTHESES.md` names only F_INST_01 as the tested feature for these four |
| **H-C5** (interaction residualization) | Indirectly, via F_INT_01–03's F_INST_05 dependency | **Unaffected in practice** | H-C5 tests whether interaction features collapse under residualization — the pre-registered expectation (per `research/RP001_MILESTONE_1D_FEATURE_FREEZE_REVIEW.md`) is that they are artifacts; a handful of stock-dates where F_INST_05 can't be fully computed (the 1342-style caveat) does not change H-C5's test design or its already-anticipated null-leaning result |

## Bottom line

**Not one locked hypothesis (H-C1–H-C5) or the one Frozen-Conditional feature (F_INST_01) is affected by the Dealer-category schema finding, on the 86-stock sample.** No feature in the "Requires deviation" or "Not constructible" tier exists for this finding. The prior escalation (D-04) is downgraded accordingly — see the correction notes in `research/RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` and `research/RP001_PHASE2A_DEVIATION_LOG.md`.

**Caveat carried forward, not dismissed:** this is an 86/2,255-stock (3.8%) sample. The rate of genuine post-cutover Dealer recurrence found here (1/86, isolated outside the break window) is evidence, not proof, that the full universe behaves the same way. Full-universe confirmation is a normal output of resuming Phase 2A.2 batch acquisition, not a precondition for resuming it — F_INST_01's own inputs (Foreign_Investor) show no schema risk at all, so there is nothing about *this specific finding* that requires seeing the full universe before proceeding.
