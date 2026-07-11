# CONNECTIVITY_REMEDIATION_PLAN_v0.1.md

Scope: **Knowledge Graph Remediation v0.1** (not "Knowledge Seed v0.3" — this stage is not about adding volume). Builds on ISOLATED_OBJECT_REGISTER_v0.1.md's classification of all 71 isolated objects.

## Structural findings feeding the plan

**Even the giant component is structurally fragile.** Of the giant component's internal edges, **132 are bridges** (removing any one splits the component) and **67 objects are articulation points** — the component has very little redundancy. This mostly overlaps with the centrality hub list (Frictionless Markets, CAPM, No Arbitrage, Risk, Intrinsic Value...), meaning the graph currently depends heavily on a small set of load-bearing objects. Worth addressing alongside isolation, not instead of it — remediation should add a small number of redundant cross-links within the giant component too, not only merge in isolated nodes.

**Most efficient reconnection targets** (ranked by nodes gained per edge, from the 33 non-giant multi-node components): merging the 9-node Fixed Income duration/convexity cluster (C14, F15–F17, ME08–ME10, PR08, PR21) into the giant component via a single well-justified edge (e.g. T19 Term Structure Theory → ME08 Macaulay Duration) raises giant share from 44.7% to 47.7% — the single largest available gain from one edge. The 6-node interest-rate-model cluster (Vasicek/CIR/Ho-Lee/BDT family) is the second largest (46.7% with one edge, e.g. connecting via T06 Pure Expectations Theory or a shared Assumption). In total, all 33 non-giant multi-node components (96 nodes) can be merged with roughly 33 edges — no new objects required for this part, since every member is an existing, real object.

## Quantitative success criteria for this stage

| Criterion | Target |
|---|---|
| Missing Expected Relationship (31 items) resolution | ≥90% resolved with the specific edges already named in the register — these require no new judgment calls, just execution |
| Giant component share | 44.7% → **≥70%**, achieved primarily by merging the 33 non-giant multi-node components (reaches ~76% alone if fully done) plus MER resolution |
| Isolated objects classified | 100% (already complete — this document's companion register) |
| New connective objects added | Bounded: **≤15**, concentrated on the Underdeveloped Domain Cluster findings — primarily Procedures that implement the 13 unconnected Standards (not all 13 need to be closed this round, but each new Procedure should close at least one) |
| Evidence-free edges added | **Zero.** Every new edge must trace to a named justification (as in the MER table), not be added solely to raise the connectivity number |
| Validity-critical DAG | Must still hold after all changes — re-run the cycle check as a gate before accepting any remediation batch |
| Legitimately Atomic / Insufficient Evidence objects | Left alone — 8 objects (5 LA + 3 IE) are expected to remain isolated at the end of this stage, and that's correct, not a shortfall |
| Misclassified/Duplicate objects | Resolved via merge decision (PR11/M19, A04 and A09 into A01), not via new edges |

## What this stage explicitly does not do

- Does not add bulk new objects (no push toward 500 or 1000)
- Does not add any edge whose only justification is "this raises giant component share"
- Does not touch Frozen KOM, Frozen Classification, or the already-Frozen Architecture Foundation
- Does not freeze Relationship Model v1.0 — that remains gated on this remediation plus whatever the Relationship Model Review track (revises, alternative-to, formalized-by gaps) still needs

## Sequencing

1. Resolve the 31 Missing Expected Relationships (pure edge-adding, zero new objects, immediately executable)
2. Merge the 33 non-giant multi-node components into the giant component (edge-adding, zero new objects)
3. Add ≤15 new Procedure/Theory/Framework objects to close the highest-value Underdeveloped Domain Cluster gaps (Standards implementation first, since it's the largest single cluster)
4. Resolve the 3 Misclassified/Duplicate cases via explicit merge decisions
5. Re-run full integrity + connectivity + centrality analysis; confirm DAG still holds and report actual giant-share achieved against the ≥70% target
