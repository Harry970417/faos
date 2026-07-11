# EVALUATION_SUITE_v0.1.md

First KnowledgeOps deliverable: use the Knowledge Base to answer real questions, not design it further. 100 financial research questions, answered against `knowledge_base_remediated_v0.1.psv` (the Remediation v0.1 output — chosen deliberately over the older Baseline v0.2, since this is what Alpha 0.2 will actually ship).

## Methodology — what's automatic vs. judgment

No retrieval or reasoning capability exists yet (Stage 4 hasn't started) — there's no system that "answers" a question on its own. Each question was given 1–5 **anchor objects** (the real KB entries a competent analyst would start from), then a graph traversal (breadth-first, depth 2) from those anchors was run programmatically to find every object actually reachable. That traversal is objective, computed from the real edge data, not estimated. **Sufficiency** is then a judgment call applied consistently: conceptually sufficient requires the traversal to reach ≥3 objects spanning ≥2 KOM types, with every anchor itself non-isolated. This is a floor, not a quality guarantee — it tests whether the graph has enough connected structure to support an answer, not whether the answer would be good.

## Headline results

**Conceptually sufficient: 84/100.** The Knowledge Base can structurally support the majority of realistic questions across all 10 taxonomy roots.

**Evidence-grounded: 0/100.** This is the finding that matters most. Every one of the 84 "sufficient" answers would have to cite Theories, Models, and Factors that carry no actual Evidence objects — Primary/Secondary/Derived tiers were designed at the Architecture level (ADR-021) but never populated as real citations attached to any Factor, Theory, or Model in the Knowledge Base. This isn't a per-question gap, it's systemic and uniform: **the entire content-population effort so far built structure and definitions, never sourcing.** Before FAOS can make an empirically defensible claim like "does momentum work in Taiwan," every relevant object needs real citations, not just a well-connected graph.

## By root

| Root | Sufficient / Total |
|---|---|
| Financial Statement Analysis | 9/9 |
| Economics | 8/8 |
| Derivatives | 10/11 |
| Quantitative Methods | 14/15 |
| Equity Investments | 7/8 |
| Portfolio Management | 11/13 |
| Fixed Income | 11/14 |
| Corporate Issuers | 5/7 |
| Ethical & Professional Standards | 5/8 |
| Alternative Investments | 4/7 |

Matches the Remediation Report's isolated-object pattern directly — Alternative Investments and Ethics remain the weakest roots because their unresolved isolated Standards/Metrics are exactly the ones this evaluation's questions land on.

## The 16 insufficient questions

| Gap type | Count | Meaning |
|---|---|---|
| Missing Relationship | 8 | The needed content exists in the KB, just not connected to it |
| Missing Knowledge | 8 | No object currently holds the needed content at all |
| Missing Classification | 0 | No question failed specifically on Difficulty/Maturity/Tag/Region grounds |
| Missing Evidence | 100 (all) | Systemic, see above — not counted per-question since it's uniform |

**Missing Relationship (8):** Q014 Stationarity (isolated Concept, never wired to the models that assume it — GARCH, Vasicek), Q025 Yield curve bootstrapping, Q028 Credit spread widening, Q039 Black-Litterman, Q040 Kelly Criterion (all four: real Procedure+Formula pairs sitting as 2-node islands, disconnected from the broader theory context they belong to), Q084 ESG integration, Q089 Agency Theory, Q092 Working Capital Management.

**One specific new finding from this exercise, not caught by the prior remediation pass:** Q084 revealed that ESG content exists in **two separate disconnected islands** — `PR30`/`ME47` (screening procedure + score) and `C62`/`FR15`/`PA12` (the concept, materiality framework, and premium-persistence pattern) — neither references the other despite both being about the same topic. This is exactly the kind of gap only surfaces by trying to actually answer a question, not by auditing the graph in the abstract.

**Missing Knowledge (8):** Q029 Sovereign risk (no sovereign-credit Theory/Model exists at all), Q052 Contango/backwardation (no futures term-structure Theory exists), Q077 Post-Earnings Announcement Drift (its natural referent, "earnings surprise," isn't an object), Q081 IRR vs. MOIC comparison (both metrics exist but nothing holds the *comparison itself*), Q082 Real estate income approach (only a bare Procedure, no supporting valuation Theory), Q097 MiFID II best execution, Q098 FATCA/AML (both: Standard+Procedure pairs with no explanatory Concept layer around them), Q099 Three Lines of Defense (fully isolated, no risk-governance Concepts exist to connect it to).

## What this means for Alpha 0.2

Two different kinds of work are now visibly needed, and they're not the same kind of work as anything done so far:

1. **Structural Remediation, round 2** — 8 Missing Relationship gaps, all connecting existing objects, no new content required. Same discipline as Remediation v0.1.
2. **Evidence population** — the actual blocker for real research use. Every "conceptually sufficient" answer is currently unsourced. This is new work, not yet attempted anywhere in this project: populating real Evidence objects (Primary/Secondary/Derived, per the Frozen Architecture) and attaching them to the Theories/Models/Factors this evaluation exercised.

Raw traversal data for all 100 questions: `EVALUATION_SUITE_v0.1_raw_results.txt`.
