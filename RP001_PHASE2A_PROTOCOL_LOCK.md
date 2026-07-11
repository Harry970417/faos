# RP-001 Phase 2A: Protocol Lock

**Locked 2026-07-11.** The six Phase 2A protocol documents below are frozen as of this commit and hash. Any future change to any of them must go through `RP001_DEVIATION_POLICY.md` and be recorded in `RP001_PHASE2A_DEVIATION_LOG.md` — none of these six files may be edited in place after this lock. If a change is genuinely needed, it is proposed, logged as a deviation with before/after content, and only then applied with a new commit and a note in this file's Amendment History.

**Approval:** "Phase 2A Confirmatory Protocol：Status: Approved" (user, this session).
**Locking Git commit:** `82bc4a3` — "RP-001: Exploratory Factor Research marked Complete. Two parallel workstreams established."
**FAOS product version at lock time:** FAOS Alpha 0.2 (`FAOS_ALPHA_0.2.md`).
**Verification performed:** `git diff 82bc4a3 -- <these 6 files>` returns empty — confirmed byte-identical to the approved commit, not modified since.

## Locked documents and hashes (SHA-256)

| Document | SHA-256 |
|---|---|
| `RP001_PHASE2A_CONFIRMATORY_PROTOCOL.md` | `dd23d310838dc1cbc1454715d49b2f866f869a5fc0cf93a6f13707eace262735` |
| `RP001_FULL_UNIVERSE_SPEC.md` | `20d4c4993fb188cc43d799d38ba86cd8a40870ee4bee4c6931980bc793d49b4f` |
| `RP001_CONFIRMATORY_HYPOTHESES.md` | `d94600f79422c3c386bbe9cbf901293f7a19f9e90ad375f5c9c828d8abcfc10e` |
| `RP001_DEVIATION_POLICY.md` | `98d811ca4f0759819a27252175602f383327c6ff949c87e156e66a7a0762b0a8` |
| `RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` | `643cf41f14fd988e931b1e9727498d0dadfc11b39142edd2824df5ff8a8f5a42` |
| `RP001_PHASE2A_EXECUTION_PLAN.md` | `630d416e41799411ce56df6cdd92ca5e77c5c337bcc4fa1e874c9a5b84490e5b` |

Recompute with `sha256sum <file>` (or equivalent) against this table at any point during Phase 2A execution to detect drift.

## What "locked" means operationally

The specific items these six documents themselves designate as immovable (restated here for a single point of reference, not a new list): F_INST_01's definition, rank normalization, return horizon construction, the break interval's boundary dates (late-Aug to late-Oct 2025, point estimate 2025-09-25), liquidity grouping definition, volatility regime definition, neutralization method (cross-sectional OLS residualization), multiple-testing method (Benjamini-Hochberg, α=0.10), the five hypotheses H-C1–H-C5 exactly as stated, and the six-phase execution sequence.

## Amendment history

None. No amendments have been made since lock.
