# RP-001 Phase 2A.1: Readiness Gate

**Verdict: CONDITIONAL PASS.** Phase 2A.1 (Full-Universe Data Readiness and Snapshot spec) is complete. This gate does **not** itself authorize Phase 2A.2 (full bulk download) — per the governing instruction, execution stops here; Phase 2A.2 requires a separate, explicit approval decision from you, informed by this document.

## What was done in Phase 2A.1

1. Protocol Lock — 6 documents hashed and git-verified unmodified (`research/RP001_PHASE2A_PROTOCOL_LOCK.md`)
2. Full-Universe Availability Audit — all 10 items, real API verification (`research/RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md`)
3. Daily Investable Universe — spec validation, look-ahead-bias check (`research/RP001_DAILY_UNIVERSE_VALIDATION.md`)
4. Data Quality Pilot — 7 diverse stocks, 3 datasets, real download (`research/RP001_PHASE2A_DATA_QUALITY_PILOT.md`)
5. Snapshot Architecture spec (`research/RP001_PHASE2A_DATA_SNAPSHOT_SPEC.md`)
6. Capacity Estimate from real pilot metrics (`research/RP001_PHASE2A_CAPACITY_ESTIMATE.md`)
7. Deviation Log opened, one entry (`research/RP001_PHASE2A_DEVIATION_LOG.md`)

No full-universe bulk download, feature construction, IC calculation, confirmatory hypothesis test, break comparison, or portfolio work was performed — consistent with the scope boundary you set.

## Answers to your five closing questions

**1. Protocol是否已完整鎖定？(Is the Protocol fully locked?)**

Yes. All six Workstream B documents are hashed (SHA-256) and verified byte-identical to the approval commit (`82bc4a3`) via `git diff`. See `research/RP001_PHASE2A_PROTOCOL_LOCK.md`.

**2. 完整股票池是否可無存活者偏誤建立？(Can the full universe be built survivorship-bias-free?)**

Yes, mechanically — with one open, non-blocking deviation and one confirmed implementation-discipline requirement:
- Listing/delisting join logic (the core survivorship-bias-free mechanism) is fully implementable from verified real sources (TWSE/TPEx company registries + `TaiwanStockDelisting`).
- Deviation D-01: disposition-stock daily history is not available as a full archive (only a 3-row current snapshot found) — logged, does not touch the survivorship-bias-free mechanism itself, only the disposition-exclusion sub-rule.
- Confirmed real hazard: pre-listing (興櫃) trading data exists under some stocks' `stock_id` before their official listing date (concrete example: 6986, ~2.5 years of pre-listing data). Resolved by strict adherence to the already-locked listing_date gate, not a spec change — but must be implemented carefully, with the unit test recommended in `research/RP001_DAILY_UNIVERSE_VALIDATION.md`.

**3. 預註冊研究期間是否可執行？(Is the pre-registered research period executable?)**

Yes, without adjustment. The pre-registered period (suggested start 2015, per `research/RP001_RESEARCH_DESIGN.md` §2) is fully executable: the institutional-data floor (2012-05-02, verified system-wide) is earlier than 2015, so no deviation is needed on the start date. The one real historical discontinuity found — the institutional-category schema split on 2014-12-01 (`Dealer` → `Dealer_self`+`Dealer_Hedging`) — predates 2015 entirely and is outside the confirmatory test window (the break interval is in 2025), so it does not affect period executability.

**4. 是否存在需要正式Deviation Approval的問題？(Are there issues requiring formal Deviation Approval?)**

One deviation logged (D-01, disposition-stock data), assessed against the Deviation Policy's own Escalation clause as **not** requiring a pause: it does not touch F_INST_01's definition, rank normalization, return horizon construction, or the break interval's boundary dates — the four items whose deviation explicitly triggers a stop. It is disclosed per the policy's "always disclosed, not filtered" rule, not brought to you as a blocking decision. If you want to review or override this classification before Phase 2A.2, say so — it is currently logged as a proceed-with-disclosure item, not a pending question.

No other stop-condition from your original instruction (F_INST_01's core definition unimplementable, break interval must be redefined, return horizon unreconstructable, liquidity grouping lacking data, survivorship-bias-free construction impossible, period materially shorter than pre-registered, irreconcilable institutional-field definitional change) was triggered.

**5. 是否建議批准Phase 2A.2 — Full Data Acquisition？(Should Phase 2A.2 be approved?)**

**Recommend: yes, conditional on the following being acceptable to you** (none are blocking findings, all are disclosed trade-offs):
- D-01's proxy approach to disposition-stock exclusion (current-snapshot-only; historical coverage genuinely incomplete) is acceptable as logged, pending a possible better source (MOPS T05ST domain, not yet checked) to be attempted first at the start of 2A.2.
- The pre-listing-data unit test (comparing first-date-with-data vs. official listing_date per stock) is built and run before the constructed universe is trusted, not skipped.
- The Capacity Estimate's ~2.0–2.5 hour full-universe pull (Mid scenario, 15–20% retry margin) is an acceptable time/resource commitment.
- The two residual, low-risk audit gaps (Item 4: financial-industry-taxonomy stability across the full period untested beyond one spot check; Item 8: ticker/rename crosswalk not exhaustively verified) are accepted as monitored risks, not resolved before proceeding.

## Summary table

| Question | Answer |
|---|---|
| Protocol locked | Yes — hashed, git-verified |
| Survivorship-bias-free universe buildable | Yes — 1 open deviation (non-blocking), 1 confirmed construction-discipline item |
| Pre-registered period executable | Yes — no adjustment needed |
| Formal Deviation Approval needed | 1 logged (D-01), does not meet Escalation criteria |
| Recommend Phase 2A.2 approval | Yes, conditional (see above) |

**This document does not start Phase 2A.2.** Awaiting your explicit decision.
