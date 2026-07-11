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
