# FAOS Alpha 0.1

First product version. From this point, FAOS is versioned as a whole product — a coherent, dated bundle of components — not tracked as a set of independently-drifting documents. Individual component versions still exist underneath (Architecture v1.0, KOM v1.0, etc.) and keep their own governance; a product version is a named, fixed snapshot of which component versions ship together.

## Bundle contents

| Component | Version | Status |
|---|---|---|
| Product Specification | v1.0 | Frozen |
| Architecture Foundation | v1.0 | Frozen |
| Knowledge Object Model (KOM) | v1.0 | Frozen |
| Knowledge Classification | v1.0 | Frozen |
| Knowledge Base | v0.2 | Locked Baseline |
| Relationship Model | v0.1 | Draft |
| Knowledge Graph Audit | v0.2 | Complete |
| Design Approval | — | Approved |

## Scope note: what Alpha 0.1 does and doesn't include

**Alpha 0.1 is the snapshot at the moment Design Approval was granted** — it bundles Knowledge Base **v0.2** (the Baseline), not the remediated output produced immediately after. Knowledge Graph Remediation v0.1 (`REMEDIATION_REPORT_v0.1.md`, `knowledge_base_remediated_v0.1.psv`) was executed under Alpha 0.1's approval but is not retroactively folded into it — a product version is a fixed point, not a moving target. Once the Remediation Report is reviewed and accepted, its output becomes the Knowledge Base component of the **next** product version.

## What "Alpha" and "0.1" mean here

- **Alpha:** the Architecture, KOM, and Classification layers are Frozen and stable; the Knowledge Base and Relationship Model are still actively under construction. Not yet suitable for use beyond this project.
- **0.1:** first tracked product version. Product version numbers are independent of any single component's version (Knowledge Base is at v0.2, Architecture at v1.0, yet the product is 0.1) — this mirrors the Stage/Version/Status independence already established for individual documents (ADR-027), applied one level up.

## Versioning going forward

Future work is tracked as product version increments (Alpha 0.2, 0.3, ... eventually Beta), each a named bundle of component versions at a point in time. Component-level Freezes, ADRs, and registers continue exactly as before — the product version is a wrapper around them, not a replacement for their individual governance.
