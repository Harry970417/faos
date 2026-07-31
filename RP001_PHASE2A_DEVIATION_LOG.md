# RP-001 Phase 2A: Deviation Log

Format per `RP001_DEVIATION_POLICY.md`: **Deviation / Original Spec / Reason / Decided Before or After Seeing Results / Impact on Which Hypothesis**. All entries logged before any confirmatory test is run on affected data, regardless of materiality.

---

**Deviation D-01: Disposition-stock (處置股) exclusion implemented via current-snapshot proxy, not a full historical daily archive.**

**Original Spec:** `RP001_FULL_UNIVERSE_SPEC.md` — "Disposition-stock exclusion rule maintained as originally designed... implementation detail to be confirmed during execution and logged as a deviation only if the original rule cannot be implemented as specified."

**Reason:** TWSE OpenAPI `/announcement/punish` returns only 3 rows as of this audit (2026-07-11) — a current/near-term snapshot, not a queryable historical archive with a `start_date`/`end_date` range. No TWSE or TPEx OpenAPI endpoint discovered during this audit provides a full-history daily disposition-status table. This matches the Deviation Policy's own listed example verbatim ("no clean data source exists for daily disposition-stock status at full-universe scale") — this is a pre-anticipated, legitimate deviation, not a discovered inconvenience.

**Decided Before or After Seeing Results:** Before — no confirmatory test has been run on any full-universe data. This is a data-availability finding from the Phase 2A.1 audit, not a post-hoc adjustment.

**Impact on Which Hypothesis:** Universe construction only (all five hypotheses inherit whichever universe is built). Does not touch F_INST_01's definition, rank normalization, return horizon, or the break interval boundary — does not trigger the Escalation clause. Practical effect: some stocks that were under disposition on some historical dates within the confirmatory test window may not be excluded on exactly those dates, because the only verifiable proxy is each stock's most recent disposition announcements (if any historical announcement archive can be located via MOPS 已公告注意/處置股票 pages during Phase 2A.2 execution) rather than a complete day-by-day flag. This is a coverage-completeness gap in a universe *exclusion* rule, not a fabrication risk — worst case, a small number of disposition-period stock-days remain in the universe that should have been excluded, which would work against finding the pre-registered effects (conservative direction), not toward manufacturing them.

**Resolution status:** Open. To be revisited at the start of Phase 2A.2 — if a genuine historical disposition archive is found (e.g., via MOPS T05ST domain, not yet checked), this deviation is superseded; if not, this snapshot-proxy approach proceeds as the logged deviation.

---

**Deviation D-02: Delisted-stock listing dates approximated via first price-observation date, not a verified official listing-date field.**

**Original Spec:** `RP001_FULL_UNIVERSE_SPEC.md` — daily universe requires "listing_date ≤ t < delisting_date," using "listing-date information from TWSE company info."

**Reason:** Discovered while building the Phase 2A.2 acquisition universe list (before any batch download): TWSE `t187ap03_L` (1,089 rows) and TPEx `mopsfin_t187ap03_O` (891 rows) are **current-listing-only snapshots** — verified by direct set check, **0 of the 337 `TaiwanStockDelisting` stock_ids appear in either registry**. FinMind's `TaiwanStockInfo` covers only 230/337 delisted stock_ids, and its `date` field was already established as unreliable for listing-date purposes (Availability Audit Item 1); spot-check on stock 4987 confirms its `date` value (2026-05-23) sits 6 days *before* its actual delisting date (2026-05-29), consistent with a last-trading/status-change date, not a listing date. No source located during this audit gives verified listing dates for delisted stocks.

**Reason this is a legitimate deviation, not a construction impossibility:** `TaiwanStockPrice`'s first available observation date for a given stock_id is a workable proxy for its listing date — available for all 337 delisted stocks (price history is not gated by the same registry limitation). This proxy carries the same caveat already documented for currently-listed stocks in `RP001_DAILY_UNIVERSE_VALIDATION.md` (pre-listing/興櫃 trading may predate official listing under the same stock_id for some names) — for delisted stocks this caveat is applied without the cross-check against an official listing_date field, since none exists for this subset.

**Decided Before or After Seeing Results:** Before — discovered and logged during acquisition-universe construction, before any Batch 1 download.

**Impact on Which Hypothesis:** Universe construction only, and only for the minimum-120-trading-day-history gate and initial-eligibility-date determination of delisted stocks specifically (currently-listed stocks are unaffected — their listing dates remain verified via the registries, Availability Audit Item 1). Does not touch F_INST_01's definition, rank normalization, return horizon, or the break interval boundary. Practical effect: a delisted stock's entry into the daily universe may be dated slightly earlier than its true official listing date (if pre-listing trading data exists under its stock_id), which — like D-01 — biases toward over-inclusion rather than fabrication, and only affects the stock's eligibility window, not its price/return values on any given day.

**Resolution status:** Open, proceeding with the price-first-observation proxy for all 337 delisted stocks, flagged as `listing_date_source = price_proxy` (vs. `registry` for the 1,980 currently-listed stocks) in the acquisition universe manifest, for full auditability.

---

**Deviation D-03: ETF/ETN identification for delisted stocks via stock-code-prefix heuristic, not registry absence (since registries exclude ALL delisted entities regardless of asset class).**

**Original Spec:** `RP001_FULL_UNIVERSE_SPEC.md` — ETFs and ETNs excluded from the universe. For currently-listed stocks, "absent from the TWSE/TPEx company registry" is a verified, structural ETF filter (Availability Audit Item 5). That mechanism does not work for delisted entities, because the registries exclude delisted stocks of *every* asset class, not just delisted ETFs.

**Reason:** 62 of the 337 delisted stock_ids follow Taiwan's conventional ETF/ETN numbering pattern (codes starting with `0`, e.g. `00732`, `00747B`, `0081`) — consistent with the same prefix convention used by every currently-listed ETF checked in this study (e.g., `0050`). This is a naming-convention heuristic, not a field-level confirmation (no per-stock "is this an ETF" flag exists for delisted entities in any source checked).

**Decided Before or After Seeing Results:** Before — applied to the acquisition universe list before any download, to avoid pulling data for entities that would be excluded from every downstream test regardless.

**Impact on Which Hypothesis:** Universe construction only. These 62 stock_ids are excluded from the Phase 2A.2 acquisition universe entirely (not downloaded) — same practical effect as excluding currently-listed ETFs, just via a different (heuristic rather than structural) detection method. If the heuristic is wrong for any of the 62 (a non-ETF security that happens to start with '0', considered unlikely given Taiwan's numbering conventions but not verified per-entity), that stock is simply absent from the acquired dataset — a coverage gap in the same conservative direction as D-01/D-02, not a fabrication risk.

**Resolution status:** Closed for acquisition purposes — applied. Not revisited unless a specific stock_id is challenged.

---

**Deviation D-04 (ESCALATED — execution paused, awaiting approval): institutional-category `Dealer`/`Dealer_self`+`Dealer_Hedging` split is not a universal one-time cutover; it recurs per-stock at unpredictable dates, status and full extent unknown.**

**Original Spec:** F_INST_01's locked definition (`RP001_PHASE2A_PROTOCOL_LOCK.md`) uses `Dealer_self` and `Dealer_Hedging` as separate inputs. Phase 2A.1's Availability Audit concluded this pairing is available throughout the entire confirmatory test window (2025 break interval) based on a single stock's history (1101), finding a clean cutover on 2014-12-01 with the undifferentiated `Dealer` category never recurring after that date.

**Reason (why this is now escalated, not logged-and-continued like D-01/D-02/D-03):** Phase 2A.2 Batch 1 (120 stocks) found stock 1342 reporting undifferentiated `Dealer` rows again from **2019-12-17 to 2020-10-26** — five years after the claimed cutover, for a stock not in the original 1101 check. This directly contradicts the "one-time, universal, non-recurring" characterization the Phase 2A.1 disposition relied on to avoid escalation. **The true pattern is unknown**: whether `Dealer` reappears only in isolated historical windows for specific stocks (as with 1342), whether it could recur during the actual 2025 confirmatory test window for some stocks (unverified — not yet checked for any stock), and what fraction of the full universe is affected, are all open questions. If `Dealer` recurs for any stock during the 2025 break-interval window, F_INST_01 cannot be constructed for that stock-date from `Dealer_self`+`Dealer_Hedging` as specified — this would be a direct, mechanical failure of the locked feature definition, not a peripheral universe-construction issue.

**Decided Before or After Seeing Results:** Before — found during Phase 2A.2 Batch 1's Integrity Gate check, before any confirmatory test has touched this data. Execution stopped immediately per your instruction; no attempt was made to "explain away" the finding before logging it.

**Escalation basis:** This deviation is assessed as touching F_INST_01's definition directly (per `RP001_DEVIATION_POLICY.md`'s Escalation clause: "any deviation affecting the definition of F_INST_01 itself... requires explicit approval before proceeding, pauses execution rather than proceeding with a logged note"). Unlike D-01/D-02/D-03 (which affect universe-membership rules, a step removed from F_INST_01's own construction), this could affect whether F_INST_01 can be computed at all for specific stock-dates within the locked test window.

**Impact on Which Hypothesis:** Potentially H-C1 through H-C4 (all of which depend on F_INST_01). Extent unknown pending further investigation — could range from "isolated, immaterial, a handful of stock-days" to "systemic enough to require a defined fallback rule for how to treat `Dealer`-only dates." No hypothesis test has been run on any full-universe data, so nothing is invalidated yet — this is a pre-execution pause, exactly as the Deviation Policy intends.

**Resolution status:** OPEN — execution paused. Batch 2 has not started. Awaiting your decision on how to investigate/resolve before Phase 2A.2 resumes (see `RP001_LOG.md` for the specific open questions and possible next steps).

> **Correction note (added 2026-07-31, Phase 2A.2-R):** This deviation's escalation basis is preserved above unedited, but was built on a factual error inherited from `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` (see that file's own correction note, same date): F_INST_01 is Foreign_Investor-only (`FEATURE_REGISTRY.md` line 11) and never reads `Dealer`/`Dealer_self`/`Dealer_Hedging`. Dealer-category drift cannot affect F_INST_01's constructibility. Full re-investigation on 86 cached stocks (`RP001_INSTITUTIONAL_SCHEMA_AUDIT.md`) additionally found: post-cutover Dealer recurrence is real but rare (1/86 stocks, stock 1342, isolated to 2019-12-17–2020-10-26) and does **not** recur inside the locked 2025 break-interval window for any of the 86 sampled stocks (0/86). Given both the corrected escalation basis and the empirical batch-scale evidence, **this deviation is downgraded from Escalated to Logged-and-Resolved for F_INST_01 and all of H-C1–H-C5** — it remains open only as a narrower, non-blocking note about F_INST_03/F_INST_04 (already non-Frozen features, not used by any locked hypothesis) and about full-universe generalizability (86/2,255 stocks checked; full-universe confirmation deferred to Phase 2A.2 batch acquisition, not required before resuming). See `RP001_PHASE2A1_REAUDIT.md` for the formal re-audit entry.

---

**Deviation D-05: `Dealer` vs. `Dealer_self`+`Dealer_Hedging` is not a one-time historical event at all — it is an ongoing, per-stock schema choice that can switch at any date, including inside the 2025 break window and as recently as 2026.**

**Original Spec:** N/A — this corrects the *characterization* established by D-04's re-investigation (`RP001_INSTITUTIONAL_SCHEMA_AUDIT.md`), not the locked protocol itself.

**Reason:** Batch 2 (stocks idx 120–239) surfaced two stocks with undifferentiated `Dealer` rows falling **inside** the locked break window (2025-08-01 to 2025-10-31) — a condition the 86-stock Phase 2A.2-R sample found zero instances of. Investigated immediately, not waved through:
- **Stock 2072** (listed 2020-11-30): reports `Dealer` for its **entire history through 2026-03-25** (624 rows, 87.6% of its institutional rows), then switches cleanly to `Dealer_self`/`Dealer_Hedging` from 2026-03-26 onward (88 rows). Zero same-day overlap between the two. The entire 2025 break window falls on the `Dealer` side of this stock's own, much-later personal cutover.
- **Stock 1623** (listed 2024-05-28): same pattern — `Dealer` from 2024-05-28 to 2026-01-20 (93 rows), clean switch to split categories from 2026-01-22 (125 rows), zero overlap. Two of its four break-window dates fall in the `Dealer` period.
- Both cutover dates (2026-01-22, 2026-03-26) are **not the 2014-12-01 date** — this is not the same event as D-04's original finding, and not explainable as "old data still using the legacy category." It is direct evidence that FinMind's choice of `Dealer` vs. the split pair is a **per-stock, potentially per-provider-feed decision that can change at any time**, not a single historical migration.

**Decided Before or After Seeing Results:** Before — found and investigated during Batch 2's Integrity Gate check, before any confirmatory test touches this data. `rp001_batch_acquire.py` v2's gate correctly hard-stopped on this (it is exactly the "genuinely new anomaly type" condition the v2 script was designed to still stop on, distinct from the three conditions already characterized and downgraded to warnings).

**Impact on Which Hypothesis: None, verified, not assumed.** `Foreign_Investor` rows are present and complete for both stocks across their entire break-window date range (2072: 55/55 dates; 1623: 2/2 dates) — checked directly, not inferred from the Dealer finding. F_INST_01 and H-C1–H-C5 are unaffected for both stocks. The only features this could affect are F_INST_03/F_INST_04 (Dealer_self/Dealer_Hedging-based, already non-Frozen, used by no locked hypothesis) — same conclusion as D-04, reached independently this time with direct evidence rather than inherited from a documentation error.

**Resolution status:** Logged and resolved for F_INST_01/H-C1–H-C5, same as D-04. **Not auto-generalized to future batches** — `rp001_batch_acquire.py`'s Integrity Gate deliberately continues to hard-stop on any future Dealer-in-break-window occurrence rather than being loosened to silently pass, since two data points is not enough to establish that `Foreign_Investor` will always remain unaffected; each future occurrence gets the same direct verification this one received, not a blanket assumption.

---

**Deviation D-06: Stock 1589 has institutional-data rows on 10 dates with no matching price row (10-date trading-calendar-inconsistency Integrity Gate trigger, Batch 2).**

**Original Spec:** N/A — universe/pipeline-construction diagnostic, not a locked-spec item.

**Reason:** Investigated the 10 flagged dates directly. Two (2019-08-24, 2019-10-26) are Saturdays — non-trading days with an erroneous institutional row, the same class of mis-dated-row contamination already root-caused and permanently guarded against by the Trading Calendar Gate built in Milestone 1B-R (`RP001_LOG.md`). One (2026-06-19) matches the exact date already identified in Milestone 1B as a known system-wide mis-dated-row date. The remaining seven (2026-06-10 to 2026-07-03) coincide with a **complete absence of price data for 1589 from 2026-04-02 onward** — the stock appears to have stopped trading (delisted or suspended) around early April 2026, while institutional reporting continued sporadically for a few more months. All 10 dates are **outside the 2025 break-interval window** (nearest is roughly 9 months before it, the rest 6+ years before or 8+ months after).

**Decided Before or After Seeing Results:** Before — found during Batch 2's Integrity Gate check.

**Impact on Which Hypothesis:** None. The existing Trading Calendar Gate (Milestone 1B-R, already part of the locked pipeline) structurally admits only dates present in **both** price and institutional data into any feature panel — these 10 institutional-only dates are excluded by that mechanism regardless of root cause, and none fall inside the break window regardless. 1589's apparent 2026-04 trading stoppage is noted for the Market Membership work (a candidate future delisting-date entry) but does not itself touch F_INST_01 or the break interval.

**Resolution status:** Logged and resolved. Same non-generalization caveat as D-05 — the Integrity Gate continues to flag, not silently ignore, future trading-calendar-inconsistency triggers.
