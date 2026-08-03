# RP-001 FAOS Trace

Records actual use of the existing system for this research design — not a parallel report written outside it.

## Knowledge Objects used (from `knowledge/knowledge_base_remediated_v0.1.psv`)

| Object | Role in RP-001 |
|---|---|
| ME07 Information Coefficient | Primary evaluation metric for every candidate factor |
| ME01 Sharpe Ratio | Long-short portfolio performance evaluation |
| C06 Correlation | Underlies Spearman Rank IC |
| C46 Autocorrelation, C47 Heteroskedasticity | Justify the Newey-West correction requirement in the statistical method section |
| C49 Overfitting, C50 Look-Ahead Bias, C51 Survivorship Bias | Directly reused for the Bias Register, not redefined |
| FA03, FA04 Momentum Factor (general, Taiwan) | Precedent factor family; FA04 specifically informs the interaction-factor design (institutional flow × momentum, echoing taiwan-attention-signal's Conclusion B) |
| ME41 T-Statistic, ME42 Standard Error | Underlie the significance-testing framework |

## Method Objects used

| Object | Role |
|---|---|
| PR04 Cross-Sectional IC Computation | Directly reused as the IC methodology, not redesigned |
| M16 Fama-MacBeth Regression Model, F12 Fama-MacBeth Two-Pass Regression Formula | Directly reused; newly evidenced this session (EV35) |
| PR01 Portfolio Sorting Procedure, PR06 Long-Short Factor Portfolio Construction | Directly reused for the quantile-portfolio design |

## Evidence Objects used

Five real, this-session-verified sources — full detail in RP001_EVIDENCE_MAP.md. Four are pre-positioned (no Knowledge Object to attach to yet); one (Fama-MacBeth 1973) is formally attached to existing objects M16/F12.

## Knowledge Graph traversal path

Starting anchors: ME07 (IC) → PR04 (Cross-Sectional IC Computation, depends-on ME07) → FA03/FA04 (Factor, depends-on PR04-equivalent construction procedure + ME07 evaluated-by) → M16 (Fama-MacBeth, depends-on F12) → C46/C47 (referenced by M16's implicit assumptions). This traversal directly mirrors the exact pattern already proven in the Evaluation Suite (Q002, Q015) — reused methodology, not reinvented.

## Which objects pass ECC

M16 and F12 are now evidenced with a peer-reviewed Primary source (Fama-MacBeth 1973) meeting ECC v1.0's clause requiring at least one peer-reviewed anchor. A full formal ECC re-run (count, independence, contested-source check) was not performed — that's execution-phase work, not part of a design-only pass, and is on the Execution Plan's first step.

## Which key knowledge still lacks Evidence

- Newey-West correction itself (source now verified, but has no object to attach to — see Finding #2 below)
- Every one of the 9 candidate institutional-flow factor definitions — no Knowledge Object of any kind exists for them yet

## Research Production Findings — real architecture gaps found through actual use, not fixed now

**Finding #1 — No Institutional Flow Factor family exists in KOM/Knowledge Base.** The entire Factor family (FA01–FA12) covers value, size, momentum, quality, low-vol, profitability, investment, carry, liquidity, term, default — zero coverage of institutional trading flow, despite it being one of the most commonly discussed factor classes in Taiwan specifically. This isn't a KOM type gap (Factor as a type handles this fine) — it's a Knowledge Base content gap, discovered by trying to actually use the system for a real question the content roster never anticipated. Recorded, not fixed — creating these objects is execution work, not design commentary.

**Finding #2 — No Method/Formula object exists for the Newey-West correction**, despite it being standard, unavoidable methodology for exactly the kind of daily panel regression this research requires (and arguably underlying several existing Metrics' t-stat calculations that were never flagged before now). This surfaced only because a real research design forced the statistical-method section to be concrete rather than generic.

**Finding #3 — No Max Drawdown object exists**, despite VaR (ME17) and CVaR (ME18) already existing as risk metrics — a real, if minor, sibling gap in the Metric family.

**Finding #4 — Confirms rather than breaks the architecture:** every core methodology (IC, Fama-MacBeth, Portfolio Sorting, bias concepts) transferred directly with zero friction — the gaps found are all missing *content*, not structural problems with Domain Model, KOM, or Classification. This is itself worth stating: the first real stress test of the frozen architecture against a genuinely new research question found the architecture sound and the content roster incomplete, which is exactly the distinction the whole Architecture/Knowledge/Evidence Era discipline was designed to produce.

No Frozen artifact was modified to produce any of the above.
