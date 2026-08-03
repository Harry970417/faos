# ISOLATED_OBJECT_REGISTER_v0.1.md

71 fully isolated objects in knowledge_base_v0.2.psv (23.5% of 302), classified individually — not treated as a single "data error" finding. Isolated rate varies sharply by Root and Type, which is itself informative (see summary below).

**Categories:** Legitimately Atomic (LA) · Missing Expected Relationship (MER) · Underdeveloped Domain Cluster (UDC) · Misclassified/Duplicate (MD) · Insufficient Evidence (IE)

## By Root Taxonomy — isolated rate

| Root | Isolated / Total | Rate |
|---|---|---|
| Alternative Investments | 10/22 | 45.5% |
| Ethical & Professional Standards | 8/20 | 40.0% |
| Financial Statement Analysis | 10/26 | 38.5% |
| Derivatives | 10/34 | 29.4% |
| Corporate Issuers | 6/22 | 27.3% |
| Equity Investments | 6/22 | 27.3% |
| Quantitative Methods | 8/46 | 17.4% |
| Portfolio Management | 6/41 | 14.6% |
| Fixed Income | 6/44 | 13.6% |
| Economics | 1/25 | 4.0% |

Roots added fresh in v0.2 for coverage (Alternative Investments, Ethics, Financial Statement Analysis, Derivatives) carry the highest isolation — expected, since these had no pre-existing giant-component structure to attach to. Economics' near-zero rate is notable: its Theories/Models (Phillips Curve, Taylor Rule, IS-LM) were authored with immediate cross-references, unlike Standards/Frameworks elsewhere.

## By Object Type — isolated rate

| Type | Isolated / Total | Rate |
|---|---|---|
| Standard | 13/18 | 72.2% |
| Assumption | 11/18 | 61.1% |
| Framework | 8/16 | 50.0% |
| Concept | 25/65 | 38.5% |
| Metric | 12/47 | 25.5% |
| Pattern | 1/12 | 8.3% |
| Procedure | 1/35 | 2.9% |
| Theory | 0/25 | 0% |
| Model | 0/24 | 0% |
| Formula | 0/30 | 0% |
| Factor | 0/12 | 0% |

The pattern is structural, not random: **the four "connective" types (Theory, Model, Formula, Factor) have zero isolation.** Everything that got authored as a Theory/Model/Formula/Factor was, by construction, given at least one relationship. Isolation concentrates entirely in types that were added for breadth (Concept, Standard, Assumption, Framework) without matching investment in the objects that would reference them. This directly explains the Root-level pattern above and is the central input to the remediation plan.

## Classification (all 71)

### Missing Expected Relationship (31) — a specific edge should exist and can be named now

| ID | Name | Expected connection |
|---|---|---|
| A05, A06 | Continuous Trading, Constant Volatility | M02 Black-Scholes should depend-on both (standard BS assumptions, simply not wired) |
| A08 | Homogeneous Expectations | T03 MPT should depend-on |
| A12 | IID Returns | T24 Random Walk Theory currently depends on nothing — should depend-on |
| A14 | Stable Correlations | T03 MPT should depend-on |
| A16 | Covered Interest Rate Parity Holds | F28/PR31 (already their own 2-node island) should depend-on |
| C12 | Default Risk | M09 Merton Structural Credit Model (has a Distance-to-Default formula but never references this Concept) |
| C25 | Moneyness | ME13 Option Delta or M02 Black-Scholes should reference |
| C26 | Counterparty Risk | PR20 CDS Pricing should reference |
| C27 | Basis Risk | PR09 Delta Hedging or PR31 Currency Hedging should reference |
| C34 | Fiduciary Duty | PR28/PR29 or S03 CFA Code should reference |
| C47 | Heteroskedasticity | M17 GARCH Model exists specifically to model this — should reference directly |
| C49 | Overfitting | PR10 Backtesting already references C50/C51 (its sibling pitfalls) — should also reference C49 |
| C52–C55 | Accrual, Going Concern, Materiality, Off-Balance-Sheet Item | S01/S02 or PR12–14 (IFRS implementation) should reference |
| C56 | Term Premium | T07 Liquidity Preference Theory should reference |
| C65 | Tail Risk | ME18 Conditional VaR should reference (CVaR is literally a tail-risk measure) |
| C20, C63 | Vintage Year, Lock-Up Period | PR17 PE Waterfall Distribution should reference (sibling to C21 Carried Interest, already referenced) |
| C22 | Net Asset Value | ME22/23/24 (PE performance metrics) should reference |
| ME29, ME33, ME34 | Interest Coverage, Asset Turnover, Inventory Turnover | Need a Procedure — PR26/27 don't cover solvency/efficiency ratios, only liquidity/profitability |
| ME35, ME38 | EV/EBITDA, PEG Ratio | PR05 Comparable Company Analysis should reference (sibling to ME06 P/E, already referenced) |
| ME41, ME42 | T-Statistic, Standard Error | ME43 Sharpe Ratio Confidence Interval should depend-on both (a CI is built from exactly these) |

### Underdeveloped Domain Cluster (29) — no connecting object exists for the whole sub-area, not just one missing edge

- **13 Standards** (S02, S04, S05, S07, S09, S10, S11, S12, S13, S14, S15, S17, S18): only 5 of 18 Standards got a matching implementation Procedure in v0.2. The other 13 have no Procedure at all — this needs new connective Procedure objects, not rewiring existing ones.
- **8 Frameworks** (FR02, FR03, FR05, FR06, FR07, FR09, FR11, FR14): the "quantitative" Frameworks (DuPont, Altman Z-Score, Greeks, Risk Parity) were all wired to their component Metrics when authored; the "qualitative" strategy Frameworks (Five Forces, SWOT, Balanced Scorecard, Value Chain, BCG Matrix) and governance/rating Frameworks (CAMELS, Endowment Model, Three Lines of Defense) were not — a systematic gap in that sub-category, not five unrelated misses.
- C42 Economic Moat — ties directly to FR02 Porter's Five Forces, both stuck in the same underdeveloped cluster.
- C58 Sovereign Risk, C60 Backwardation — each is the sole representative of a sub-area (sovereign credit; futures curve shape beyond the one Pattern already covering Contango) with no Theory/Model of its own yet.
- ME21 Tracking Error; ME22, ME23, ME24, ME48 (PE/fund performance metrics) — "passive/benchmark management" and "PE performance measurement" are sub-areas with metrics but no connecting Procedure.

### Legitimately Atomic (5) — real terms, no forced edge needed yet

C13 Reinvestment Risk, C15 Par Value, C44 Market Capitalization, C45 Float, C61 Implied Correlation. Foundational vocabulary that doesn't yet have a Theory/Procedure in this seed that specifically needs them — reasonable to leave unconnected rather than invent a connection.

### Misclassified / Duplicate (3) — candidates for merging, not connecting

- **PR11 Monte Carlo Simulation Procedure** substantially overlaps with **M19 Monte Carlo Simulation Model** (already connected). Recommend clarifying the distinction (e.g. PR11 = generic method, M19 = specific derivatives application) or merging.
- **A04 No Taxes or Transaction Costs** and **A09 Perfect Capital Markets** both substantially overlap with **A01 Frictionless Markets**, which conventionally already implies both. Recommend a merge decision rather than wiring new edges to near-duplicates.

### Insufficient Evidence (3) — genuinely unclear, not a coverage gap

A17 No Model Risk, A18 Stable Regulatory Environment — generic risk caveats with no specific anchor object in the current seed; unclear what they should attach to without inventing new objects for the sole purpose of connecting them.
PA06 Post-Earnings Announcement Drift — its natural referent ("Earnings Surprise") doesn't exist as an object yet; the gap is upstream of PA06 itself.
