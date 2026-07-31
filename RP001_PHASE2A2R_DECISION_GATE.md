# RP-001 Phase 2A.2-R: Decision Gate

**Date:** 2026-07-31. Answers the seven required questions based on `RP001_API_AND_SOURCE_FEASIBILITY.md`, `RP001_INSTITUTIONAL_SCHEMA_AUDIT.md` + `RP001_FEATURE_IMPACT_MATRIX.md`, `RP001_INSTITUTIONAL_MISSINGNESS_AUDIT.md` + `RP001_MISSINGNESS_POLICY.md` + `RP001_ANOMALY_REGISTER.md`, `RP001_MARKET_MEMBERSHIP_AUDIT.md` + `RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md`, and `RP001_PHASE2A1_REAUDIT.md`.

## 1. 合法且可重現的 API acquisition path 是否存在？

**Yes.** Anonymous FinMind access (300 req/hr, official + empirically confirmed) is legal, reproducible, and live today. No token, payment, or ToS exception is required. A free registered token (600 req/hr) is available as an optional accelerant, not a requirement.

## 2. F_INST_01 是否可在完整股票池跨期一致建構？

**Yes, on all evidence gathered so far (86-stock sample); full-universe confirmation is a natural byproduct of resuming acquisition, not a precondition for it.** F_INST_01 depends solely on `Foreign_Investor`, which shows zero schema drift, zero missing stocks, and no name variants across the sample. The one real institutional-schema anomaly found (Dealer recurrence, stock 1342) does not touch F_INST_01 at all — that was a documentation error in Phase 2A.1, now corrected (`RP001_INSTITUTIONAL_SCHEMA_AUDIT.md` §9).

## 3. H-C1～H-C5 中哪些仍可原規格執行？

**All five**, unchanged from their locked specification, subject to two operational (non-spec) rules now in force: (a) the Missingness Policy's coverage gate and NaN-not-zero handling, (b) exclusion of stock 1213 from any break-window test per its confirmed 89-day gap overlapping the break interval (`RP001_ANOMALY_REGISTER.md` AR-03). Neither changes F_INST_01's definition, normalization, horizon, or the break boundary.

## 4. Missingness 是否能建立一致且不偏誤的處理規則？

**Yes.** `RP001_MISSINGNESS_POLICY.md`: never impute (NaN, not 0), drop from cross-section, 80% stock-level coverage gate for the confirmatory window (set before seeing window-specific pass rates), explicit-zero kept as a real 0, unresolved gap types treated conservatively as `source_missing`. Not itself a deviation from the locked protocol — it fills a gap the protocol left undefined.

## 5. TWSE／TPEx 歷史市場資格是否可重建？

**Methodology established and validated where testable; empirically unverified for TPEx.** The eligibility-gate logic (`RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md`) is sound and automated-test-covered (`test_daily_universe_gate.py`, 5/5 assertions pass) for the cases the current sample contains (ordinary TWSE, suspected TPEx→TWSE transfer, 興櫃→TPEx, delisted-proxy). **Zero TPEx stocks exist in the current cached sample** — the rule is applied uniformly by construction but not yet stress-tested against a real TPEx stock, a TWSE→TPEx transfer, or a re-listed stock. This closes naturally as soon as batches drawn from elsewhere in the universe are acquired.

## 6. D-01、D-04 是否需要升級為 Escalating Deviation？

- **D-04: No — downgraded, not escalated.** Its original escalation basis was a documentation error (F_INST_01 does not use Dealer categories at all). Corrected in place in both `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` and `RP001_PHASE2A_DEVIATION_LOG.md`. Real residual risk (Dealer recurrence affecting F_INST_03/F_INST_04, both already non-Frozen and unused by any locked hypothesis) is immaterial.
- **D-01: No change — remains logged, non-escalated, unresolved.** Not re-investigated this round (outside Phase 2A.2-R's four audit areas); its original non-blocking assessment (doesn't touch F_INST_01/normalization/horizon/break boundary) still holds on the same reasoning as Phase 2A.1.

## 7. Phase 2A.2 應該：

**Resume, with approved (non-escalating) deviations** — specifically: (a) acquisition proceeds under the real, documented anonymous-tier throughput (300 req/hr, ~21.7 hours of paced requests for the remaining 2,170 stocks) rather than the retracted 2.0-2.5-hour estimate; (b) the Missingness Policy and Market Membership Spec v2 (both new, both non-locked operational rules) govern universe/feature construction going forward; (c) the Batch Integrity Gate's stop-trigger set is narrowed for the three anomaly types fully characterized this round (Dealer recurrence, missing-rate patterns, listing-date gaps) — a batch encountering *more of the same, already-understood* pattern logs and continues; a batch encountering a **new** anomaly type not covered by this round's findings still halts immediately, exactly as originally specified.

**None of the seven true-blocker conditions from your standing instructions are met:** no paid service is required, F_INST_01's definition is untouched, the break interval is untouched, return horizon/normalization/hypotheses are untouched, a survivorship-bias-free universe is buildable, a legal reproducible acquisition path exists, and no result yet exists to be inexplicable. A token would help (halves throughput time) but is not required — resumption does not wait on it.

**Execution note:** full remaining acquisition is a genuinely multi-hour, rate-limited operation that cannot complete inside a single tool call (~21.7 hours of paced anonymous requests, vs. this environment's ~10-minute per-call ceiling). Batch acquisition resumes now with the redesigned tooling (skip-existing, failed-symbol queue, rate-aware pacing — `RP001_API_AND_SOURCE_FEASIBILITY.md` §5) and continues across scheduled follow-up turns until the full universe is acquired, per your explicit Batch-based, no-wait-for-approval instruction.
