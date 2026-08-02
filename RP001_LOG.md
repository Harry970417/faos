# RP-001 Research Log

Every Research Decision from this point forward is recorded here: **Decision / Reason / Evidence / Impact.** Retroactive entries below cover key decisions already made in RP-001's design phase.

---

**Decision:** Research question framed as competing hypotheses (H1a continuation vs. H1b reversal), not a single directional hypothesis.
**Reason:** ECC v1.0 and this project's own PA01 precedent require not presupposing significance or direction.
**Evidence:** Chordia & Subrahmanyam (2004) establishes a real, literature-grounded reversal mechanism competing with the informed-trading continuation story.
**Impact:** Statistical design must be able to distinguish the two mechanisms, not just test "any effect."

---

**Decision:** Prediction target anchored at t+1 open-or-later; close-to-close treated as a non-executable reference case only.
**Reason:** Institutional flow data publishes after market close — using it to predict the same day's close is look-ahead bias.
**Evidence:** Live check this session shows FinMind's institutional data available through 2026-07-09 as of the check date, consistent with a post-close publication pattern.
**Impact:** All "predictive power" claims in the final research must be qualified by which return definition they use.

---

**Decision:** taiwan-attention-signal selected as the reuse base, not stock-ai-project or taiwan-stock-analyzer.
**Reason:** Already has a working FinMind institutional-breakdown fetcher and IC/Fama-MacBeth code.
**Evidence:** Direct code inspection of `fetch_institutional_breakdown.py`, `ic_analysis.py`, `v03_fama_macbeth.py`.
**Impact:** Execution Plan Phase 0-3 built around adapting this codebase, not building new pipeline code.

---

**Decision:** Institutional-flow factor definitions widened from a 3-way (外資/投信/自營商) split to a 5-way split.
**Reason:** Live FinMind data returns 5 categories, not 3 — `Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer_self`, `Dealer_Hedging`. Dealer_Hedging in particular is often mechanically driven (options/warrant hedging), not a directional view, and likely has different signal content than Dealer_self.
**Evidence:** Live API check, this session, stock 2330, 2026-07-01 to 2026-07-09.
**Impact:** RP001_RESEARCH_DESIGN.md's factor table understates the real granularity available — needs a minor revision before Phase 0 (not a Frozen-artifact issue, a research-design refinement, in scope for this project).

---

**Decision:** git commit created for the FAOS repository (first commit ever).
**Reason:** Reproducibility Checklist requires a git anchor point; none existed after 47 files had accumulated uncommitted.
**Evidence:** `git log` showed "does not have any commits yet" prior to this session.
**Impact:** Commit `05ccedc2af023f93435d7741538b43dacd48b445` is now the reproducibility reference point for everything in Alpha 0.2 and RP-001 to date.

---

**Decision:** Random seed policy set to 42 project-wide for RP-001.
**Reason:** No prior policy existed; needed before any stochastic step (train/validation splits, bootstrap if used in robustness checks).
**Evidence:** Consistent with the seed already used in this project's own community-detection script (`audit_graph_v0.2.py`) — reusing an existing convention rather than inventing a new one.
**Impact:** Must be applied consistently across every script touching RP-001 data from Phase 0 onward.

---

**Decision:** Foreign_Dealer_Self excluded as a standalone feature; kept only inside aggregate sums.
**Reason:** Real characterization data, not assumption.
**Evidence:** 99.99% zero-rate across 122,920 real observations (50 stocks, 492 trading days) — see RP001_DATA_PROFILE.md.
**Impact:** Feature Specification reduced from an implicit ~9-factor set to 4 single-category + 5 derived + 3 interaction = 11 precisely-defined features.

---

**Decision:** Rank-based standardization set as primary method; z-score demoted to a robustness-only variant.
**Reason:** Real distribution data, not the Research Design's original assumption of z-score as default.
**Evidence:** Every institutional category shows severe mean/median divergence and fat tails in the real 122,920-row sample.
**Impact:** Feature Specification and future Phase 1 IC computation must use rank standardization as the primary result, z-score only for comparison.

---

**Decision:** Phase -1's "Chinese-text encoding corruption" finding reclassified from real blocker to resolved misdiagnosis.
**Reason:** Root-caused this session — terminal stdout encoding (cp950), not a data-source problem. Raw bytes confirmed valid UTF-8 both from FinMind and TWSE's official OpenAPI.
**Evidence:** Direct byte-level decode test, cross-verified against TWSE OpenAPI returning correct, complete company records (臺灣水泥, 亞洲水泥, etc.).
**Impact:** Execution Readiness improves — one of three Phase -1 blockers was never real. Industry classification confirmed usable via TWSE's coded 產業別 field, recommended over FinMind's free-text field for stability.

---

**Decision:** F_INT_01's momentum component built as a 20-trading-day price return, not yet formally linked to KB objects FA03/FA04.
**Reason:** FA03/FA04 (Momentum Factor) exist as KOM objects but don't have a single precise, code-ready formula attached; needed a concrete definition to build Milestone 1A now rather than block on that linkage.
**Evidence:** N/A — this is a construction-convenience placeholder, not evidence-driven; flagged explicitly so it isn't mistaken for a validated choice.
**Impact:** F_INT_01 as currently built is provisional. Formal reconciliation with FA03/FA04's KB definition is required before Milestone 1C diagnostics are treated as final.

---

**Decision:** Market cap computed from TWSE OpenAPI shares-outstanding (mostly static) × daily close, not from a dedicated daily market-cap dataset.
**Reason:** No dedicated market-cap-history dataset was checked this session; shares outstanding is a reasonable approximation since share count changes far less often than price.
**Evidence:** TWSE OpenAPI `t187ap03_L` confirmed to return real, complete shares-outstanding data for all 50 sample stocks (0% missing after join).
**Impact:** F_INT_02 (size interaction) does not reflect intra-period share count changes (buybacks, capital increases) — acceptable approximation for this construction pass, should be revisited if any sample stock had a material capital event during 2024-07 to 2026-07.

---

**Decision:** F_INST_05/06/07 flagged as one redundancy cluster for Milestone 1C reporting, not three independent features.
**Reason:** Real, not assumed — mechanically expected given their construction, now confirmed empirically.
**Evidence:** Spearman correlation 0.88-0.91 between all three pairs, computed on the real 24,535-row panel.
**Impact:** Milestone 1C IC/ICIR reporting must treat this cluster as one signal group, or risk overstating how many independent predictive features exist.

---

**Decision:** Trading-calendar validation flagged as required before Milestone 1C, not yet implemented.
**Reason:** Found a real mis-dated institutional data row (2026-06-19, a confirmed non-trading day with genuine non-zero buy/sell values) in the Merge Loss Audit. It didn't reach the current feature panel, but only incidentally (inner join with price happened to drop it), not by deliberate design.
**Evidence:** Price data confirms zero rows for 2026-06-19 across all 50 stocks (clean holiday gap, 06-18 to 06-22); institutional data for the same date contains real, substantial buy/sell figures for 49 of 50 stocks.
**Impact:** This is a data-integrity leakage risk distinct from the code-level leakage already empirically ruled out (rolling-window truncation test passed cleanly). Must be closed with an explicit safeguard, not left to incidental protection, before Milestone 1C results are treated as final.

---

**Decision:** Trading Calendar Gate implemented as an explicit filter (not relying on incidental inner-join protection); feature panel rebuilt as v0.2.
**Reason:** Milestone 1B's leakage validation found the 2026-06-19 protection was accidental, not designed.
**Evidence:** Full-period scan (all 24,584 institutional rows) confirms 2026-06-19 is the ONLY non-trading-day contamination across the entire 2-year sample — not a recurring pattern, but still required a permanent regression test given it happened once.
**Impact:** Feature panel version bumped to v0.2. Regression check confirmed 0 unexpected changes to existing feature values (only the already-excluded 06-19 rows differ). 5/5 pipeline tests pass.

---

**Decision:** Only F_INST_01_foreign (and secondarily F_INST_07) recommended for Milestone 1D Freeze Review; no feature recommended for unconditional Freeze.
**Reason:** Real diagnostic evidence, not a design preference.
**Evidence:** Year-by-year stability check shows F_INST_01's IC decaying from 0.072 (2024) to -0.001 (2026); sector-neutralization strips 75% of F_INT_03's and flips the sign of F_INT_02's raw IC; incremental-IC test confirms F_INST_06 is redundant with F_INST_05 (residual IC ~0.002).
**Impact:** Milestone 1C report explicitly recommends against treating any feature as unconditionally stable. F_INT_01 stays Experimental per instruction despite having the strongest raw numbers in the set.

---

**Decision:** F_INT_04_foreign_x_liquidity reclassified from "strongest raw signal" to "likely data artifact."
**Reason:** Residualization test, not assumption.
**Evidence:** Raw IC 0.073 (t=6.41) drops to -0.005 (icir -0.04) once both plain Foreign rank and plain Liquidity rank are jointly controlled for -- the apparent amplification is almost entirely additive, not a genuine multiplicative interaction.
**Impact:** Same suspicion extended to F_INT_05/06 (foreign x volatility, foreign x size) which were not individually tested this round but show the same raw-IC shape that turned out artifactual for liquidity. None of the four Foreign-interaction features are recommended for Freeze without individual residualization testing.

---

**Decision:** Structural break at 2025-09-24 established as the central fact governing any Freeze decision on F_INST_01.
**Reason:** CUSUM break detection + Welch t-test, not a visual read of a declining trend line.
**Evidence:** Pre-break mean IC 0.052 vs post-break -0.008, t=3.41, p=0.0007.
**Impact:** Any future Freeze recommendation for F_INST_01 must carry this break as an explicit condition (era-specific, not unconditional), plus the low-volatility-regime dependence found in the same milestone.

---

**Decision:** Structural break reclassified from a single-date finding to a break INTERVAL (late Aug - late Oct 2025), and confirmed via a properly-corrected unknown-breakpoint test, not a single post-hoc Welch t-test.
**Reason:** Original 1C+ test picked one candidate date and ran one t-test on it -- vulnerable to the "break date chosen from the same data" critique.
**Evidence:** Quandt-Andrews sup-Wald test (self-implemented; ruptures/Bai-Perron failed to build, no C++ compiler in this environment) with permutation p-value (2000 reps): p=0.0105 for F_INST_01, properly accounting for the search across all candidate dates. Break-date sensitivity confirms the qualitative conclusion holds across +/-40 trading days. Two independent rolling windows (40d, 90d) show the identical persistent shape.
**Impact:** F_INST_01's Freeze candidacy must state a break interval, not a precise date, and must not be presented as unconditional.

---

**Decision:** Low-volatility effect and structural break determined to be intertwined, not independent findings.
**Reason:** Double-sort test, not assumption carried over from Milestone 1C+.
**Evidence:** Low-vol & Post-break cell: mean IC = -0.004 (t=-0.17) -- the low-vol effect vanishes once you move past the break, even though volatility itself stayed low in parts of the post-break period.
**Impact:** Milestone 1C+'s framing (three separate findings: break, low-vol, liquidity) revised to one primary mechanism (the break) with volatility and liquidity as within-regime modulators, not free-standing effects.

---

**Decision:** All four tested Foreign-interaction features (Liquidity, Volatility, Size, Momentum) confirmed or strongly suspected as additive recombination artifacts, none show genuine incremental interaction.
**Reason:** Residualization against BOTH constituent main effects simultaneously (not one at a time), for every interaction, not just the ones that looked suspicious.
**Evidence:** F_INT_04 residual IC -0.005 (confirmed 1C+); F_INT_06 residual IC -0.002 to -0.004 across all cuts (confirmed this round); F_INT_07/F_INT_01 residual IC 0.0004 at t+5 with a sign flip post-break (confirmed this round, despite having the strongest raw numbers in the entire study); F_INT_05 residual IC consistently negative across every cut (inconclusive-leaning-artifact).
**Impact:** No interaction feature is a Freeze candidate. F_INT_01's Experimental status is now directly evidenced rather than just a cautious default.

---

**Decision:** Multiple testing register built (56 tests, BH-FDR at q<0.10); F_INT_03 and F_INT_01 flagged as passing statistical correction while independently confirmed as mechanism-level artifacts.
**Reason:** Requested full test inventory, not selective reporting of significant results.
**Evidence:** 9/56 tests survive FDR correction, including F_INT_03 (t+2,t+3,t+5) and F_INT_01 (t+5) -- both separately shown to be artifacts via neutralization/residualization.
**Impact:** Established as a standing principle for this project: statistical significance surviving multiple-testing correction is necessary but not sufficient -- mechanism-level tests (neutralization, residualization) are required in addition, not as a substitute.

---

**Decision:** F_INT_01, F_INT_02, F_INT_03 (aggregate-based interactions) tested via joint residualization against their own constituents for the first time at Milestone 1D, closing a gap the prior rounds had only partially addressed (sector/mcap neutrality had been tested, not joint-residualization against the interaction's own two components).
**Reason:** Your explicit rule: incomplete joint-residualization tests must be marked Inconclusive/Pending, not assumed to transfer from a similar feature's result.
**Evidence:** F_INT_01 residual t+5 IC -0.004 (t=-0.42); F_INT_02 residual -0.003 (t=-0.38); F_INT_03 residual -0.004 (t=-0.46) -- all collapse to zero, same pattern as the four features already tested in Milestone 1C-R.
**Impact:** All seven interaction features (F_INT_01 through F_INT_07) now uniformly Confirmed Artifact -- no exceptions, no feature retained as Research-Grade due to raw IC or FDR survival alone. F_INT_03's FDR-significant raw IC and F_INT_01's FDR-significant raw IC are both now documented as artifacts despite passing the purely statistical bar.

---

**Decision:** RP-001 Feature Freeze completed at Milestone 1D. F_INST_01 is the only feature reaching Frozen status, and only as Frozen-Conditional with six permanent, mandatory conditions written into FEATURE_REGISTRY.md.
**Reason:** Full research program (Milestones 0A through 1C-R) applied consistently -- no feature reached unconditional Research-Grade status.
**Evidence:** Full decision table in RP001_FEATURE_DECISION_TABLE.md; every cell traceable to a specific prior milestone's computation.
**Impact:** RP-001's factor-research phase concludes with one conditional signal, one secondary candidate, and a fully-documented, dead-end interaction-feature family (all seven confirmed artifacts) -- itself a legitimate, evidenced research conclusion, not a null result to be hidden.

---

**Decision:** RP-001 Exploratory Factor Research marked Complete; RP-001 overall remains Open pending Phase 2A. Two parallel workstreams established: Research Report v0.1 (documenting exploratory results as exploratory, not confirmatory) and Phase 2A Confirmatory Protocol (pre-registered, not yet executed).
**Reason:** The break/volatility/liquidity conditions were all discovered on the same 50-stock sample used to test them -- internal robustness testing reduces but does not eliminate this concern, so a genuinely independent confirmatory pass is required before treating any finding as final.
**Evidence:** N/A -- this is a governance/sequencing decision, not an empirical finding.
**Impact:** Research Report v0.1 explicitly states its "Confirmatory" findings category is empty by design. Phase 2A Protocol locks F_INST_01's definition, normalization, horizon, break interval, liquidity/volatility definitions, and statistical methods before any full-universe data is touched -- deviations require pre-registration per RP001_DEVIATION_POLICY.md, not post-hoc adjustment. No full-universe data pulled yet; execution awaits Protocol approval.

---

**Decision:** Phase 2A.1 (Full-Universe Data Readiness and Snapshot) approved and completed. Verdict: Conditional Pass. Phase 2A.2 (full bulk download) not started -- remains a separate, explicit decision.
**Reason:** Your instruction required real verification (live API calls) of 10 full-universe availability items, a data-quality pilot on diverse real data, a capacity estimate from real pilot metrics (not theoretical), and a Protocol Lock with actual hashes -- not assumptions carried over from the exploratory phase.
**Evidence:** Six Workstream B documents hashed (SHA-256) and confirmed byte-identical to approval commit 82bc4a3 via `git diff`. Institutional-data floor confirmed system-wide at 2012-05-02 (before the pre-registered 2015 start -- no deviation needed). TWSE (`t187ap03_L`, 1,089 rows) and TPEx (`mopsfin_t187ap03_O`, 891 rows) confirmed as real listing-date sources; `TaiwanStockInfo`'s own date field confirmed unreliable for this purpose. 7-stock diverse pilot pull: 14 requests (later extended to 15 with a `TaiwanStockPER` check), 0 retries, 0 failures, 82,123 rows / 9.79MB / 9.56s API-active time -- the real basis for the Capacity Estimate (Mid scenario: ~2,300 stocks, ~35M rows, ~4.0GB, ~2.0-2.5hr wall time incl. retry margin). Re-download of 1101's institutional data produced a byte-identical SHA-256, confirming deterministic downloads.
**Impact:** Two real findings surfaced and were resolved without requiring Deviation escalation: (1) a 6th institutional category (`Dealer`) found across all pilot stocks, root-caused as a clean one-time schema cutover on 2014-12-01 (`Dealer` -> `Dealer_self`+`Dealer_Hedging`, zero date overlap) -- immaterial because the confirmatory test window (2025 break interval) postdates it by over a decade; (2) newly-"listed" stocks (e.g., 6986) found to carry pre-listing (興櫃) trading data under the same stock_id up to ~2.5 years before their official listing date -- resolved by strict adherence to the already-locked listing_date gate (not a spec change), with a unit test recommended before Phase 2A.2's universe construction is trusted. One deviation logged (D-01: disposition-stock exclusion has no full historical archive, only a 3-row current-snapshot proxy found) -- assessed against the Deviation Policy's own Escalation clause as non-blocking (does not touch F_INST_01's definition, normalization, horizon, or break boundary). Full detail and the five closing-question answers in `RP001_PHASE2A_READINESS_GATE.md`. Phase 2A.2 (full bulk download, feature construction, confirmatory testing) remains explicitly not started, awaiting your separate approval.

---

**Decision:** Phase 2A.2 (Full Data Acquisition) started under your batch-based execution requirement. Batch 1 (120 stocks, 360 requests) run and its Integrity Gate FAILED. Execution stopped immediately, per your instruction, without running Batch 2. Awaiting your approval before resuming.
**Reason:** Your instruction was explicit and is being followed literally: any batch finding schema drift, historical-definition drift, unexpected missing pattern, duplicated observations, trading-calendar inconsistency, or listing-date violation halts all subsequent batches immediately, logs to this file, and waits -- "不要因為 Batch 3 正常就假設 Batch 12 也正常." Batch 1 triggered three of the six conditions simultaneously, plus a separate operational blocker (API quota) not on your original list but severe enough to report alongside them.
**Evidence:**
1. **API quota ceiling (new, not anticipated in the Phase 2A.1 Capacity Estimate):** 256 of 360 requests succeeded before every subsequent request returned HTTP 402 (`"Requests reach the upper limit"`, confirmed via direct re-query, not a data-not-found response). Batch 1 alone (an unauthenticated/anonymous FinMind API session) exhausted the available quota mid-batch. The full-universe pull needs ~6,765 requests (2,255 stocks x 3 datasets); at this ceiling the Phase 2A.1 Capacity Estimate's "~2.0-2.5 hour wall time" figure is invalidated -- it was extrapolated from a 14-15 request pilot that never approached the quota. Real full-universe acquisition will require either an authenticated/higher-quota API token, or spreading batches across quota-reset windows over multiple days.
2. **Historical definition drift (retracts a Phase 2A.1 conclusion):** stock 1342 shows the undifferentiated `Dealer` category recurring 2019-12-17 to 2020-10-26 -- five years after the "clean one-time 2014-12-01 cutover" the Availability Audit concluded from a single-stock (1101) check. That conclusion ("does not require escalation") is retracted; see the correction note added to `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` and new Deviation D-04 (escalated) in `RP001_PHASE2A_DEVIATION_LOG.md`.
3. **Unexpected missing pattern:** stock 1213 has institutional records on only 1,146 of 3,353 possible post-floor trading dates (2,207 dates entirely absent, scattered across its full 2012-2026 history, not a contiguous halt) -- contradicts the Phase 2A.1 Data Quality Pilot's "explicit zero encoding" missing-value-semantics finding, which was based on stock 1101 only. 30 of 120 batch-1 stocks exceeded a 10% missing-rate threshold.
4. **Listing-date violation:** 5 stocks flagged; largest is stock 1256 (first price data 2012-09-05 vs. registry listing_date 2016-03-17, a 1,289-day/3.5-year gap) -- larger than the ~2.5-year 6986 case documented in Phase 2A.1 and too large to comfortably attribute to ordinary pre-listing/興櫃 trading. Suspected but unverified explanation: TPEx-to-TWSE market transfer, where the registry's listing_date reflects only the most recent market, not original trading start under the same code -- this is Availability Audit Item 8's previously-flagged, not-yet-resolved gap (ticker/market-transfer history) materializing concretely.
5. **No duplicated observations and no schema drift found** in Batch 1 -- 2 of the 6 listed trigger conditions did not fire.
**Impact:** Batch 2 has not been run. `RP001_PHASE2A_BATCH_TRACKER.md` records Batch 1 as STOP with full detail. Three open questions need your direction before resuming: (a) how to proceed given the API quota ceiling (authenticated token vs. multi-day spread vs. other); (b) whether/how to investigate D-04's full extent (does `Dealer` recur during the actual 2025 test window for any stock, and for how many stocks total) before continuing acquisition, given it could affect F_INST_01's constructibility directly; (c) whether the missing-pattern and listing-date-violation findings warrant a broader review of Phase 2A.1's single-stock-based conclusions before trusting any further batch's output. No hypothesis test has touched any data -- this is a pre-execution pause, not an invalidated result.

---

**Decision:** Resumed Phase 2A.2 batch acquisition under your standing autonomous-execution instruction (no per-step approval, only true blockers halt). Batch 7 completed and resolved (PASS after investigation); driving Batches 8-19 to full-universe completion, each still individually gated per the Decision Gate's non-loosening rule.
**Reason:** Repo state (git log, `RP001_PHASE2A2R_DECISION_GATE.md`) shows the Decision Gate already passed on 2026-07-31 -- all seven true-blocker conditions checked and none met -- and Batches 1-6 already acquired and resolved. This session picked up an in-progress, uncommitted Batch 7 (interrupted mid-run by an HTTP 402 quota wall at 2026-08-01T13:47 UTC) rather than assuming the stale "paused at Batch 1" premise from an outdated chat summary, per your explicit instruction to trust repo state only.
**Evidence:** Batch 7 resumed at 14:56 UTC (>1hr after the 402, quota confirmed reset), completed its remaining 181/360 requests with zero further failures. Integrity Gate raw result STOP on stock 6272 (Dealer recurrence inside the break window) -- investigated directly, confirmed the 9th individually-verified instance of the D-05 pattern (own cutover date 2025-12-19 to 2025-12-22 postdates the entire break window; `Foreign_Investor` present on 49/49 non-gap break-window dates; the window's other 13 dates are whole-day `source_missing`, not `Foreign_Investor`-specific, already governed by the Missingness Policy). Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-7 addendum, `RP001_PHASE2A_BATCH_TRACKER.md` Batch 7 row + resolution section.
**Impact:** F_INST_01/H-C1-H-C5 unaffected. No new anomaly type introduced -- the Integrity Gate's hard-stop set is unchanged, each future Dealer-in-break-window or trading-calendar-inconsistency occurrence still gets the same individual verification, not a blanket pass. Proceeding to Batch 8 (idx 840-960) and onward.

---

**Decision:** Batch 8 completed and resolved (PASS after investigation). Found and fixed a real acquisition-tooling bug along the way: `rp001_batch_acquire.py` could run the Integrity Gate over a batch that wasn't actually fully downloaded.
**Reason:** A ~2.5-hour unattended background wait (retrying through an HTTP 402 quota pause) coincided with a connectivity outage on this machine; 236 requests came back as generic connection failures rather than clean 402s. The script's pause condition only checked for explicit 402s, so it treated "every request attempted" as "batch done" and ran the Integrity Gate over a batch that was only 34% genuinely downloaded (124/360). A direct follow-up API call confirmed this was a local connectivity blip, not an API-side or quota problem -- both were fine immediately after.
**Evidence:** `rp001_batch_acquire.py`'s `run_batch` now also returns PAUSED (2) when non-402 failures remain, forcing a retry (which the skip-existing logic already handles correctly) before the gate runs. Batch 8 re-driven to a true 360/360 complete state; re-run gate found 7 Dealer-in-break-window stocks (6614, 6722, 6831, 6908, 6934, 7610, 7711), each individually verified per the established D-05 protocol -- `Foreign_Investor` present on every date carrying any institutional row, zero exceptions across all 7. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-8 addendum, `RP001_PHASE2A_BATCH_TRACKER.md` Batch 8 resolution section.
**Impact:** F_INST_01/H-C1-H-C5 unaffected. This batch's stock range also runs materially sparser overall (88/120 stocks over the missing-rate warning threshold) -- flagged as a segment-level pattern for the Missingness Policy's coverage gate to handle as designed, not a new anomaly type or a reason to revisit the policy. The tooling fix is acquisition-only and applies retroactively-safe to all future batches (Batches 1-7's manifests were already fully complete before their gates ran, so this bug did not affect any already-resolved batch). Proceeding to Batch 9 (idx 960-1080) and onward.

---

**Decision:** Batch 9 completed and resolved (PASS after investigation). Found and fixed a second acquisition-tooling bug: a genuinely empty (but valid) API response could trigger an infinite retry loop.
**Reason:** Batch 9's driver got stuck 5 attempts / ~5 hours retrying the same 10 `TaiwanStockPER` requests. Direct follow-up confirmed the API was correctly returning HTTP 200 with zero rows for 10 TDR-style stock codes -- not a transient failure, a genuine "no data for this stock/dataset" answer that would never change on retry. The script recorded this correctly as `status="empty"` but then treated it the same as a real failure for retry-queueing purposes (checked `status != "success"` instead of `status == "failed"`), so it could never resolve.
**Evidence:** Fixed `load_existing_success()` to treat `"empty"` as terminal (same as `"success"`), and narrowed the retry-queue condition to `status == "failed"` only. Cleaned up 391 duplicate manifest rows across Batches 1-9 that had accumulated from the stuck loop (kept final-state row per pair, no data lost -- duplicates were byte-identical repeat downloads of the same empty/success result). Re-ran the Integrity Gate on the now-genuinely-complete Batch 9: STOP on Dealer-in-break-window, 16 stocks (largest single-batch count yet, concentrated in a 2024-2025-IPO-heavy stock range where this is the structurally expected pattern). All 16 individually verified via a new reusable checker (`rp001_verify_dealer_break.py`) -- `Foreign_Investor` present on every date any institutional category reports, zero exceptions. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-9 addendum, `RP001_PHASE2A_BATCH_TRACKER.md` Batch 9 resolution section.
**Impact:** F_INST_01/H-C1-H-C5 unaffected. Running total of individually-verified Dealer-in-break-window instances: 35 across Batches 2, 5-9, zero `Foreign_Investor` exceptions found -- the pattern is now clearly correlated with listing recency, not random, but the non-loosening rule stays in force: every future occurrence still gets full individual verification. Proceeding to Batch 10 (idx 1080-1200) and onward.

---

**Decision:** Batch 10 completed and resolved (PASS after investigation). Separately, this batch closes an open item from the Phase 2A.2-R Decision Gate: real TPEx data now verified.
**Reason:** Batch 10 (`rp001_data/phase2a_acquisition_universe.csv` idx 1080-1200) is 111/120 TPEx stocks -- the Decision Gate (`RP001_PHASE2A2R_DECISION_GATE.md` §5) had explicitly logged TPEx eligibility-gate behavior as "empirically unverified" since zero TPEx stocks existed in any sample up to that point, closing "naturally as soon as batches drawn from elsewhere in the universe are acquired" -- exactly what happened here, not something specifically sought out.
**Evidence:** Zero schema-drift flags across all 120 TPEx-majority stocks -- same institutional-category set as TWSE. Two Dealer-in-break-window stocks (1780, 3158) individually verified clean, same protocol as all 37 prior instances. Missing-rate-warning incidence is the highest of any batch so far (95/120, 79%), consistent with TPEx's generally thinner institutional coverage. Full detail: `RP001_MARKET_MEMBERSHIP_AUDIT.md` §6 (correction note added, original "not verified" finding preserved verbatim above it), `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-10 addendum, `RP001_PHASE2A_BATCH_TRACKER.md` Batch 10 resolution section.
**Impact:** F_INST_01/H-C1-H-C5 unaffected and now confirmed market-agnostic (not a TWSE-only property, as it could plausibly have been before this batch). "TWSE→TPEx transfer" and "re-listed stock" remain open/unverified -- not assumed resolved by extension. Proceeding to Batch 11 (idx 1200-1320) and onward.

---

**Decision:** Batch 11 completed and resolved (PASS after investigation) -- routine, one Dealer-in-break-window stock (3485), same protocol, 38th consecutive clean instance. Full detail in `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-11 addendum and `RP001_PHASE2A_BATCH_TRACKER.md`. Proceeding to Batch 12 (idx 1320-1440) and onward.

---

**Decision:** Batch 12 completed and resolved (PASS after investigation) -- routine, one Dealer-in-break-window stock (4166), 39th consecutive clean instance. Missing-rate warning count sets a new high (99/120, 82.5%), continuing the trend seen since Batch 8; still fully governed by the Missingness Policy. Also noted: background acquisition processes in this environment have been getting killed mid-sleep well before their intended retry interval (observed across Batches 9-12) -- not a data-integrity issue (all state is persisted to disk and resumed correctly each time via skip-existing logic), but shortened the driver's retry sleep from 65 to 12 minutes (`rp001_batch_driver.py`) so each relaunch wastes less time if killed again. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-12 addendum. Proceeding to Batch 13 (idx 1440-1560) and onward.

---

**Decision:** Batch 13 completed and resolved (PASS after investigation) -- routine, one Dealer-in-break-window stock (5547), 40th consecutive clean instance. The shortened 12-minute driver retry interval completed this batch in a single background run (6 attempts, ~1hr9min), confirming the earlier tooling change is working as intended. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-13 addendum. Proceeding to Batch 14 (idx 1560-1680) and onward.

---

**Decision:** Batch 14 completed and resolved (PASS after investigation) -- routine, one Dealer-in-break-window stock (6028), 41st consecutive clean instance. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-14 addendum. Proceeding to Batch 15 (idx 1680-1800) and onward.

---

**Decision:** Batch 15 completed and resolved (PASS after investigation). Four Dealer-in-break-window stocks (6474, 6620, 6725, 6730), 42nd-45th consecutive clean instances. Both warning counts (missing-rate, listing-date-gap) set new highs (110/120 and 111/120) -- this stock range is almost entirely thin, recently-listed issuers, consistent with the trend since Batch 8, still fully governed by existing policy. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-05 Batch-15 addendum. Proceeding to Batch 16 (idx 1800-1920) and onward.

---

**Decision:** Batch 16 completed and resolved (PASS after investigation). 23 Dealer-in-break-window stocks -- the largest single-batch count by far -- including stock 6986, already documented in Phase 2A.1's Availability Audit as a 興櫃→TPEx transfer case.
**Reason:** All 23 flagged stocks are 2023-2025 IPOs, the same structural pattern established since Batch 9 (new-issuer segments haven't reached their personal Dealer→split cutover before or during the break window).
**Evidence:** All 23 individually verified via `rp001_verify_dealer_break.py` -- zero `Foreign_Investor`-specific gaps in any case, including 4 stocks (6884, 6961, 7716, 7842) with only 1 institutional-bearing date in the entire 62-day break window (these will very likely fail the Missingness Policy's 80% coverage gate and be excluded from the confirmatory universe -- the correct designed outcome, not a defect). 6986's Dealer/split pattern (cutover 2026-06-26) does not interact with its already-documented 興櫃 pre-listing history.
**Impact:** F_INST_01/H-C1-H-C5 unaffected. Running total: 68 individually-verified Dealer-in-break-window instances, zero exceptions. Proceeding to Batch 17 (idx 1920-2040) and onward.

---

**Decision:** Batch 17 completed and resolved -- clean PASS, first batch since Batch 4 with zero new anomalies. Proceeding to Batch 18 (idx 2040-2160) and onward.

---

**Decision:** Batch 18 completed and resolved -- clean PASS, second consecutive clean batch. Missing-rate warning count drops sharply to 23/120, the lowest since Batch 7, and zero listing-date-gap warnings -- this batch's stock segment (idx 2040-2160, near the end of the currently-listed universe before the delisted-stock tail) looks structurally different from the sparse mid-range batches. Proceeding to Batch 19 (idx 2160-2255, the final batch, 95 stocks) and onward.

---

**Decision:** Batch 19 (final batch) completed and resolved -- clean PASS, third consecutive clean batch. **Full-universe Phase 2A.2 acquisition is now complete: all 19 batches, 2,255 stocks, 6,765 requests, Integrity Gate PASS on every batch (10 required individual investigation and resolution per the Deviation Policy; 3 were clean on the first pass).**
**Reason:** This completes the batch-based, no-wait-for-approval acquisition your instruction authorized, continuing from the Phase 2A.2-R Decision Gate's PASS verdict.
**Evidence:** Full batch-by-batch detail in `RP001_PHASE2A_BATCH_TRACKER.md`. Summary: 69 total Dealer-in-break-window instances individually verified across the run (D-05's addenda, Batches 2 and 5-16), 100% clean (`Foreign_Investor` present on every date any institutional category reports, zero exceptions) -- F_INST_01's constructibility holds across the entire universe, not a sample-specific property. Two real acquisition-tooling bugs found and fixed along the way (Batch 8: gate could run on an incomplete batch after a connectivity outage; Batch 9: an infinite retry loop on legitimately-empty API responses) -- both fixes are acquisition-only, no protocol impact. First real TPEx-majority batch (10) closed a previously-open Decision Gate item. Missing-rate and listing-date-gap warning counts track stock-segment composition (rising through the small-cap/recent-IPO/TPEx-heavy middle of the universe, falling again near its end) -- fully governed by existing policy throughout, never requiring escalation.
**Impact:** No deviation required escalation. No change to F_INST_01's definition, normalization, horizon, or the break interval at any point across all 19 batches. Proceeding to the Full Data Acquisition Integrity Gate summary and final manifest, then the Confirmatory Dataset build.

---

**Decision:** Logged Deviation D-08 before writing any Confirmatory Dataset construction code: market-cap and sector data are unavailable at full-universe scale, making F_INT_02 (flow×size) and F_INT_06 (foreign×size) not constructible.
**Reason:** Reviewed all locked feature/hypothesis definitions (`FEATURE_REGISTRY.md`, `RP001_1c_plus_setup.py`'s exact interaction formulas) against what Phase 2A.2 actually acquired (`TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice`, `TaiwanStockPER` only) before starting to build the panel, per the Deviation Policy's before/after discipline.
**Evidence:** The only shares-outstanding source in the repo (`rp001_data/twse_company_info.json`) covers just the 1,089 currently-listed TWSE companies (0 TPEx, 0 delisted) and has corrupted text encoding throughout. No shares-outstanding or industry-code field exists in any of the three FinMind datasets pulled -- confirmed against `rp001_batch_acquire.py`'s own schema constants.
**Impact:** H-C1-H-C4 and F_INST_01 fully unaffected (neither uses market cap or sector). H-C5 proceeds on 5 of 7 interaction features (all liquidity/volatility/momentum-based, fully constructible); the 2 size-based interactions are reported as Inconclusive due to data unavailability, not silently dropped or approximated. Full detail: `RP001_PHASE2A_DEVIATION_LOG.md` D-08. Proceeding to Confirmatory Dataset construction.

---

**Decision:** Ran H-C1 through H-C5 on the full-universe Confirmatory Dataset. Verdicts: H-C1 Not Replicated, H-C2 Replicated (with caveat), H-C3 Partially Replicated, H-C4 Not Replicated, H-C5 Not Replicated. No methodology was adjusted after seeing these results.
**Reason:** This is the entire purpose of Phase 2A -- test whether the exploratory-phase findings (all discovered on a 50-stock, ~2-year sample) hold on independently-constructed, full-universe, full-history data.
**Evidence:** Full statistics (mean/median IC, Newey-West t, 95% CI, raw p, BH-FDR q, sample size, per hypothesis and sub-cut) in `RP001_PHASE2A_CONFIRMATORY_RESULTS.md`. Headline: F_INST_01's pre-break IC is statistically indistinguishable from zero at all three horizons (t+1/t+3/t+5, NW t ranging 0.04-1.19) -- roughly 40-70x smaller than the exploratory study's pre-break IC (0.052, t=3.99). The volatility double-sort's defining cell (Low-vol & Pre-break) is also not significant (t=0.789 vs. the original's t=3.99), so H-C4's break-conditionality claim has no significant effect left to test. H-C3's liquidity pattern partially holds (Illiquid/Mid both exceed Liquid, Liquid null) but is asymmetric (only Mid independently significant). H-C5 finds the opposite of what was expected: 4 of 5 testable interaction features (F_INT_01, 03, 04, 07) show residual IC surviving both NW t>1.96 and BH-FDR q<0.10 after joint residualization -- small in magnitude (75-95% smaller than each feature's raw IC) but not statistically zero at this sample size.
**Impact:** RP-001's central exploratory finding (F_INST_01's conditional predictive power) does not survive independent confirmatory validation on ~30x more stocks and ~7x more history. This is reported as the confirmatory study's actual result, not adjusted, hidden, or reframed -- exactly what Phase 2A existed to test for. Full verdict table: `RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`. Consolidated deviation summary: `RP001_PHASE2A_DEVIATION_FINAL.md`. Reproducibility detail: `RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`.
