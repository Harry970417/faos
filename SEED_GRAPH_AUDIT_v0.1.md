# SEED_GRAPH_AUDIT_v0.1.md

**Audits:** knowledge_seed_v0.1.psv (50 objects, 53 edges)
**Method:** computed programmatically (Python graph traversal), not estimated
**Correction to prior claim:** the previous message asserted "53 edges therefore connected." That was never verified. Section 2 below disproves it directly.

---

## 1. Graph Integrity

| Check | Result |
|---|---|
| All edge sources exist as nodes | Pass — 0 missing |
| All edge targets exist as nodes | Pass — 0 missing |
| Self-loops | None found |
| Duplicate edges (same source, target, type) | None found |
| Immediate 2-cycles (A→B and B→A, same edge type) | None found |
| DAG check on validity-critical edges (depends-on + implements + derived-from, 30 edges) | **No cycles — valid DAG** |

The DAG check ran a full directed-cycle search (DFS with white/gray/black coloring) over the combined validity-critical edge set, not a spot check. No cycle paths to report.

## 2. Connectivity — corrected

**The graph is NOT fully connected.** Ignoring direction:

- **9 connected components** (not 1)
- **Largest component: 40 nodes** (80% of the graph)
- **1 mid-size component: 3 nodes** — {ROE, ROA, DuPont Analysis}, isolated from everything else because nothing else in the seed references ROE/ROA/DuPont
- **7 fully isolated objects** (zero edges — no in, no out, no reference either direction): Volatility (C04), WACC Formula (F05), Porter's Five Forces (FR02), SWOT Analysis (FR03), IFRS (S01), US GAAP (S02), CFA Code of Ethics (S03)

All 3 Standard objects are isolated — no Procedure, Framework, or other object in this seed touches them. This is the single most consequential integrity finding for the candidate review below (Section 4D).

**In-degree = 0:** 22 objects — includes legitimate terminal/derived objects (Patterns, most Theories not yet extended by any Model) and objects genuinely unreferenced this round (isolated Standards/Frameworks).
**Out-degree = 0:** 24 objects — expected for atomic Tier-0 types (Concept, Assumption, Formula) that nothing depends *from*, plus the isolated Standards.

## 3. Type-Pair Matrix

Full counts (Source --edge--> Target), ordered by frequency:

```
 8  Theory --DependsOn--> Assumption
 7  Theory --References--> Concept
 5  Metric --References--> Concept
 4  Factor --DependsOn--> Procedure
 4  Factor --DependsOn--> Metric        [tag: semantic-evaluatedby]
 3  Procedure --References--> Concept
 2  Model --DependsOn--> Factor
 2  Model --DependsOn--> Formula
 2  Model --DependsOn--> Assumption
 2  Framework --References--> Metric
 1  Theory --References--> Formula      [tag: informal-F1]
 1  Model --References--> Theory        [tag: semantic-extends]
 1  Model --DependsOn--> Concept
 1  Model --DependsOn--> Model          [tag: semantic-extends]
 1  Model --References--> Concept
 1  Metric --DependsOn--> Formula
 1  Metric --References--> Metric
 1  Metric --DependsOn--> Concept
 1  Factor --References--> Concept
 1  Procedure --DependsOn--> Formula
 1  Procedure --DependsOn--> Procedure
 1  Procedure --DependsOn--> Metric
 1  Pattern --DerivedFrom--> Factor
 1  Pattern --References--> Factor
```

**Stable patterns** (recurring across multiple distinct instances of the same type-pair, not one object repeated): Theory→Assumption (8, across 5 Theories), Theory→Concept (7, across 5 Theories), Metric→Concept (5, across 3 Metrics), Factor→Procedure (4, across **all 4** Factor instances — 100% coverage), Factor→Metric/evaluated-by (4, also 100% coverage of Factor instances).

**Single-instance patterns** — everything else. One occurrence is not evidence of a stable semantic pattern on its own; treated accordingly in the candidate review.

## 6. Sample Bias — scope of every conclusion above

- **Zero coverage:** Fixed Income, Alternative Investments
- **Minimal coverage:** Derivatives (2 objects), Economics (3), Ethical & Professional Standards (1)
- **Structurally isolated:** all 3 Standards — meaning any candidate relationship involving Standard (e.g. Standard↔Procedure) has **no data either way** in this seed, not weak data
- Every "0 occurrences" finding in this audit means *this seed didn't produce an instance*, not *this relationship doesn't exist in finance*. Absence here is not evidence of absence.
- Every "N occurrences" finding is scoped to a sample skewed toward Portfolio Management (15/50) and Quantitative Methods (13/50) — conclusions should be read as "true for this sample," pending confirmation from a more balanced future seed.
