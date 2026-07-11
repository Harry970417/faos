# KNOWLEDGE_GRAPH_AUDIT_v0.2.md

**Audits:** knowledge_base_v0.2.psv — 302 objects, 233 edges (extends v0.1's 50 objects, unchanged, plus 252 new)
**Method:** computed programmatically, same methodology as v0.1

---

## Integrity (re-verified at scale)

No missing sources/targets, no self-loops, no duplicate edges. Validity-critical subgraph (depends-on + implements + derived-from, 122 edges) is a confirmed DAG — full cycle search, no cycles found even after tripling the object count.

## Object Distribution

By Type: Concept 65, Metric 47, Procedure 35, Formula 30, Theory 25, Model 24, Assumption 18, Standard 18, Framework 16, Factor 12, Pattern 12
By Root: Quantitative Methods 46, Fixed Income 44, Portfolio Management 41, Derivatives 34, Financial Statement Analysis 26, Economics 25, Corporate Issuers 22, Equity Investments 22, Alternative Investments 22, Ethical & Professional Standards 20

All 10 roots now represented (v0.1 had 2 at zero). Coverage is far more even, though Quantitative Methods/Fixed Income/Portfolio Management are still the deepest.

## Relationship Frequency

| Edge type | v0.1 (n=50) | v0.2 (n=302) |
|---|---|---|
| depends-on | 29 | 110 |
| references | 23 | 111 |
| implements | 0 | **9** |
| derived-from | 1 | 3 |

**`implements` is no longer empty.** 8 of the 9 new instances are `Procedure --Implements--> Standard` — exactly the pairing flagged Dormant in the candidate register, specifically because v0.1's Standards were fully isolated. v0.2 deliberately added Procedures that operationalize Standards (compliance reviews, disclosure procedures, AML screening), and the pairing held up immediately once tested. This is the register's "reconsider when" condition being met, not a coincidence.

## Degree Distribution

Mean degree 1.54, max 14 (Information Coefficient). **71 objects (23.5%) remain fully isolated** — same count as at n=253, though the specific membership shifted as some old isolates gained edges and some new additions arrived isolated.

## Centrality

Top by degree: IC (14), Long-Short Factor Construction (9), Risk (8), Intrinsic Value (8), No Arbitrage (8), Frictionless Markets (7), CAPM (7).

Top by betweenness: **Frictionless Markets and CAPM stayed #1/#2 even after the graph tripled in size** — this is the strongest evidence in either seed that these aren't small-sample artifacts, they're structurally load-bearing. New entrants to the top tier: Rational Investors, Rational Expectations Theory, Monetary Policy, Taylor Rule Model — the new Economics content formed real structure, not an unconnected appendage.

## Community Structure

32 communities detected (label propagation) within the 135-node giant component. Communities align with taxonomy roots more often than not, with one notable cross-domain result: Fixed Income and Economics theories cluster **together**, not separately — because Pure Expectations Theory, Purchasing Power Parity, and Uncovered Interest Rate Parity all share the No-Arbitrage assumption. That's a real structural finding, not noise: arbitrage-free pricing is genuinely a shared foundation across those two domains in practice.

## The one finding that matters most for how to grow this further

**Connectivity got relatively worse as the seed grew, not better.** Giant component share: 80% at n=50 → 47% at n=253 → 44.7% at n=302. This isn't random — it's a direct consequence of *how* the seed was expanded: each growth round added many atomic reference objects (Concepts, Standards, Assumptions) faster than it added the higher-level objects (Theories, Procedures, Models, Frameworks) that would actually cross-reference them. Breadth-first term addition fragments a knowledge graph; it's the connective objects that hold it together. Actionable for any future expansion (v0.3, or Stage 3 content authoring generally): prioritize adding objects that reference existing ones over adding new atomic terms, or connectivity will keep degrading as the corpus grows.
