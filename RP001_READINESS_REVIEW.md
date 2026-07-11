# RP-001 Phase -1: Research Readiness Review

Every finding below is from a real, live check performed this session — API calls, environment inspection, git status — not a hypothetical audit. Where something couldn't be fully resolved, it's stated as open, not assumed either way.

## 1. Data Readiness Audit

| Item | Finding | Status |
|---|---|---|
| **Coverage** | `TaiwanStockInstitutionalInvestorsBuySell` returns real data for a live-tested ticker (2330), 5 institution categories per day, consistent 5 rows/day across a 7-day window checked | Confirmed working |
| **Frequency consistency** | 5 rows/date, every date, in the sample window checked | Confirmed for this sample; not yet verified across the full universe or full date range |
| **Institutional category granularity** | **Real finding, not anticipated in the original Research Design:** the API returns 5 categories — `Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer_self`, `Dealer_Hedging` — not the 3-way 外資/投信/自營商 split the design assumed. Dealer_Hedging is often mechanically driven (options/warrant hedging), likely different signal content than Dealer_self. Logged in RP001_LOG.md as a design refinement, not a blocker. | Design refinement needed |
| **Missing value pattern** | In a 35-row spot check, 7 rows (20%) showed buy=0 and sell=0. **Not yet determined whether this is a genuine "no activity" zero or a data-quality gap** — needs systematic characterization across the full universe before Phase 0, not resolved by this single-ticker check | **Open — needs resolution before Phase 0** |
| **Publication timing** | Data available through 2026-07-09 as of this session's live check — consistent with a post-close publication lag, but only spot-checked against calendar dates, **not yet verified against Taiwan's actual trading calendar** (holidays, half-days) | **Open — Execution Plan Phase 0 Step 1 already anticipates this, not a new blocker** |
| **Corporate actions** | Not directly tested this session — adjusted price source not yet finalized (flagged in Data Requirements as an open decision) | **Open** |
| **Delisted stocks** | **Real finding: `TaiwanStockDelisting` dataset exists and returns 337 real rows**, with usable `stock_id` and `date` fields — survivorship-bias-free construction is achievable with this data source. `stock_name` field has the same encoding issue noted below, but that's cosmetic, not structural | **Confirmed available — de-risks the single biggest open question from the Bias Register** |
| **Ticker mapping** | `TaiwanStockInfo` dataset exists, 3,113 unique stock IDs, includes TWSE/TPEx type and industry category fields | Confirmed available, see encoding issue below |
| **Character encoding — real blocker** | `TaiwanStockInfo` and `TaiwanStockDelisting`'s Chinese-language fields (`stock_name`, `industry_category`) return as corrupted/unrecoverable text (`�` replacement characters) via a raw `requests` call. `stock_id` and `date` fields are unaffected. **This blocks using stock names or industry labels directly from this endpoint until fixed** — likely resolved by using FinMind's official Python SDK instead of raw HTTP calls, not yet confirmed | **Real, concrete blocker for the industry-classification robustness cut specifically; does not block stock_id-keyed joins** |
| **Look-ahead risk** | Design-level control already in the Bias Register (t+1-or-later target); this audit found nothing that changes that design, only confirms the publication-lag pattern is real, not theoretical | Confirmed consistent with design |
| **Survivorship bias** | See Delisted Stocks — data now confirmed available; correct integration into the universe-construction step is Execution Plan Phase 0-1, not yet done | On track, no new blocker |

## 2. Environment Readiness

| Item | Value |
|---|---|
| Python version | 3.14.5 (confirmed both globally and in taiwan-attention-signal's existing venv) |
| Package status | **Global environment is missing `statsmodels`** (required for Fama-MacBeth). **taiwan-attention-signal's own venv already has it** (statsmodels 0.14.6, pandas 3.0.3, numpy 2.5.0, scipy 1.18.0) — recommend extending that venv rather than building a new environment |
| Package lock | Not yet created for RP-001 specifically — to be generated from taiwan-attention-signal's venv once extended, in Phase 0 |
| Git commit | **Was completely uncommitted (47 files) prior to this session.** First commit made this session: `05ccedc2af023f93435d7741538b43dacd48b445` |
| FAOS version | Alpha 0.2 |
| Random seed | Set to 42 project-wide (see Log) |
| Data snapshot policy | **Not yet established** — needs a rule (e.g., every raw API pull saved with a pull-timestamp before any transformation) before Phase 0 begins, to keep results reproducible against a specific data vintage |

### Reproducibility Checklist

- [x] Python version pinned (3.14.5)
- [x] Working package set identified (taiwan-attention-signal's venv)
- [x] Git commit anchor established
- [x] FAOS version identified (Alpha 0.2)
- [x] Random seed policy set (42)
- [ ] Package lock file generated for RP-001 specifically
- [ ] Data snapshot policy defined and enforced
- [ ] Missing-value characterization completed across full universe

## 3. Research Log

`RP001_LOG.md` established — Decision/Reason/Evidence/Impact format, 6 entries logged this session, all future Research Decisions to be added there going forward.

## 4. Execution Readiness Report

**Can Data Collection genuinely start? Not yet — three concrete, resolvable blockers, not a redesign:**

1. **Character encoding on Chinese-text fields** (TaiwanStockInfo, TaiwanStockDelisting) — needs FinMind's official SDK or a working encoding fix before industry classification or human-readable stock names can be used. Does not block stock_id-keyed joins.
2. **Missing-value pattern (20% zero-rows in the spot check) uncharacterized at full-universe scale** — must be systematically resolved (genuine zero vs. data gap) before factor construction, or the institutional-flow factors risk being built on silently wrong assumptions.
3. **Data snapshot policy undefined** — starting to pull data without one would make Phase 0's own output non-reproducible, undermining the Reproducibility Checklist this review just established.

**None of these require touching Frozen Architecture, KOM, Classification, Evidence Domain, or ECC.** All three are Execution Plan Phase 0-level engineering tasks, already anticipated in kind (if not in this specific detail) by the Execution Plan's own Phase 0 step 1. The Research Design itself is not in question — what's not yet ready is the data engineering layer underneath it.

**Recommendation:** approve Phase 0 with these three items as its explicit first tasks, not as new obstacles requiring a design revision.
