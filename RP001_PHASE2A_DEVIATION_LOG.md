# RP-001 Phase 2A: Deviation Log

Format per `RP001_DEVIATION_POLICY.md`: **Deviation / Original Spec / Reason / Decided Before or After Seeing Results / Impact on Which Hypothesis**. All entries logged before any confirmatory test is run on affected data, regardless of materiality.

---

**Deviation D-01: Disposition-stock (處置股) exclusion implemented via current-snapshot proxy, not a full historical daily archive.**

**Original Spec:** `RP001_FULL_UNIVERSE_SPEC.md` — "Disposition-stock exclusion rule maintained as originally designed... implementation detail to be confirmed during execution and logged as a deviation only if the original rule cannot be implemented as specified."

**Reason:** TWSE OpenAPI `/announcement/punish` returns only 3 rows as of this audit (2026-07-11) — a current/near-term snapshot, not a queryable historical archive with a `start_date`/`end_date` range. No TWSE or TPEx OpenAPI endpoint discovered during this audit provides a full-history daily disposition-status table. This matches the Deviation Policy's own listed example verbatim ("no clean data source exists for daily disposition-stock status at full-universe scale") — this is a pre-anticipated, legitimate deviation, not a discovered inconvenience.

**Decided Before or After Seeing Results:** Before — no confirmatory test has been run on any full-universe data. This is a data-availability finding from the Phase 2A.1 audit, not a post-hoc adjustment.

**Impact on Which Hypothesis:** Universe construction only (all five hypotheses inherit whichever universe is built). Does not touch F_INST_01's definition, rank normalization, return horizon, or the break interval boundary — does not trigger the Escalation clause. Practical effect: some stocks that were under disposition on some historical dates within the confirmatory test window may not be excluded on exactly those dates, because the only verifiable proxy is each stock's most recent disposition announcements (if any historical announcement archive can be located via MOPS 已公告注意/處置股票 pages during Phase 2A.2 execution) rather than a complete day-by-day flag. This is a coverage-completeness gap in a universe *exclusion* rule, not a fabrication risk — worst case, a small number of disposition-period stock-days remain in the universe that should have been excluded, which would work against finding the pre-registered effects (conservative direction), not toward manufacturing them.

**Resolution status:** Open. To be revisited at the start of Phase 2A.2 — if a genuine historical disposition archive is found (e.g., via MOPS T05ST domain, not yet checked), this deviation is superseded; if not, this snapshot-proxy approach proceeds as the logged deviation.
