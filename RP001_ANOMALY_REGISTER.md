# RP-001 Phase 2A.2-R: Anomaly Register

**Date:** 2026-07-31. Per-stock/per-finding anomalies surfaced during Phase 2A.2-R audits (schema, missingness, market membership), consolidated for tracking. This is a living register — append, don't overwrite, as full-universe acquisition surfaces more.

| ID | Stock(s) | Finding | Source Audit | Severity | Status |
|---|---|---|---|---|---|
| AR-01 | 1342 | Undifferentiated `Dealer` category recurs 2019-12-17 to 2020-10-26, five years after the general 2014-12-01 cutover. Does not overlap the 2025 break window. | Schema Audit §2 | Low (isolated, outside test window, does not touch F_INST_01) | Resolved — see D-04 correction note |
| AR-02 | 1213 | 65.82% missing institutional data over full history; 392 discrete gaps; worst single block 167 trading days (2022-02-11 to 2022-10-12). | Missingness Audit §6 | High (extreme, structurally sparse coverage) | Open — excluded under Missingness Policy Rule 3/6 |
| AR-03 | 1213 | Missing block 2025-09-26 to 2026-02-05 (89 trading days) falls inside/adjacent to the locked break-interval window. Not explained by trading halt (0 of these dates show `Trading_Volume=0`). | Missingness Audit §6 | **High — directly threatens break-interval test integrity if not excluded** | Open — must be excluded from H-C1–H-C4's break-window sample under Missingness Policy Rule 6 |
| AR-04 | 30 of 85 sampled stocks | Missing rate > 10% over full history (16 exceed 20%). | Missingness Audit §2 | Medium | Open — subject to Missingness Policy Rule 3 coverage gate at full-universe scale |
| AR-05 | 1256 | First price observation 2012-09-05 vs. registry `listing_date` 2016-03-17 — 1,289-day (3.5-year) gap, larger than the previously-documented 6986 case (~2.5 years). Suspected TPEx→TWSE market transfer. | Batch 1 Integrity Gate / Market Membership Audit | High (universe-eligibility-dating risk) | Open — investigated in `RP001_MARKET_MEMBERSHIP_AUDIT.md` |
| AR-06 | 1338, 1339, 1340 | Listing-date gaps of 352, 113, 39 days respectively vs. registry listing_date — smaller than 1256/6986, plausibly ordinary pre-listing/興櫃 trading but not individually verified. | Batch 1 Integrity Gate | Low-Medium | Open — covered by Market Membership Audit's general gating rule, not individually resolved |
| AR-07 | All 85 cached stocks | Sample is 100% TWSE, all long-listed, low `stock_id` — not representative of the full 2,255-stock universe (TPEx entirely absent; no newly-listed or delisted stocks). | Missingness Audit §5, Schema Audit (implicit) | Medium (external validity of every 85-stock finding in this document) | Open — resolved only by drawing further batches from elsewhere in the universe |
| AR-08 | FEATURE_REGISTRY.md vs. RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md | Documentation error: Phase 2A.1's Availability Audit incorrectly attributed `Dealer_self`/`Dealer_Hedging` to F_INST_01 (they belong to F_INST_03/F_INST_04). Caused D-04 to escalate on a mistaken premise. | Schema Audit §9 | Resolved (documentation only, no data/spec impact) | Closed — correction notes added to both source documents |

## Severity legend

- **High:** could change a confirmatory test's result or validity if not handled.
- **Medium:** affects interpretation/generalizability but not raw correctness of a specific computation.
- **Low:** documented for completeness, immaterial to any locked hypothesis or feature.
