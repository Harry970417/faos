# RP-001 Phase 2A: Protocol Lock

**Locked 2026-07-11.** The six Phase 2A protocol documents below are frozen as of this commit and hash. Any future change to any of them must go through `research/RP001_DEVIATION_POLICY.md` and be recorded in `research/RP001_PHASE2A_DEVIATION_LOG.md` — none of these six files may be edited in place after this lock. If a change is genuinely needed, it is proposed, logged as a deviation with before/after content, and only then applied with a new commit and a note in this file's Amendment History.

**Approval:** "Phase 2A Confirmatory Protocol：Status: Approved" (user, this session).
**Locking Git commit:** `82bc4a3` — "RP-001: Exploratory Factor Research marked Complete. Two parallel workstreams established."
**FAOS product version at lock time:** FAOS Alpha 0.2 (`architecture/FAOS_ALPHA_0.2.md`).
**Verification performed at lock time:** `git diff 82bc4a3 -- <these 6 files>` returned empty — confirmed byte-identical to the approved commit as of 2026-07-11.

**Verification status as of 2026-09-08 (see Deviation D-09 in `research/RP001_PHASE2A_DEVIATION_LOG.md`):** commit `190c568` (2026-08-03, repository reorganization) moved 5 of these 6 files into `research/` and rewrote their internal cross-reference paths, changing their byte content and therefore their SHA-256 hashes. A direct content diff against the `82bc4a3` versions confirmed the changes are limited to cross-reference path prefixes (e.g. `` `RP001_FULL_UNIVERSE_SPEC.md` `` → `` `research/RP001_FULL_UNIVERSE_SPEC.md` ``) — zero changes to any hypothesis wording, threshold, or method definition. The hash table below reflects the current (post-move) values, not the `82bc4a3` root-layout values. `RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` had no cross-references to the other five files and is still byte-identical to `82bc4a3`.

## Locked documents and hashes (SHA-256)

| Document | SHA-256 (current, verified 2026-09-08) |
|---|---|
| `research/RP001_PHASE2A_CONFIRMATORY_PROTOCOL.md` | `2cb7e9369c0d5d28834d5fcfb5f154e1639f24e8902e4c6e41fb25335aa2441e` |
| `research/RP001_FULL_UNIVERSE_SPEC.md` | `dcf56e89af94423d51d5184a95e971ab9ac5864ee81eca53f64201805b1adea0` |
| `research/RP001_CONFIRMATORY_HYPOTHESES.md` | `7d15480602ea160a0a3a4a146f45fe267f4151bfe5d2b61c34f4f97d86e0d00b` |
| `research/RP001_DEVIATION_POLICY.md` | `c7c01395f6ebc128b1de6dd52e12116506dcf3e586b73af40bf54a928744dc2f` |
| `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` | `643cf41f14fd988e931b1e9727498d0dadfc11b39142edd2824df5ff8a8f5a42` |
| `research/RP001_PHASE2A_EXECUTION_PLAN.md` | `b400c77737c7bb66a92e7adb014d6400925975f57e6c5516f0332c0b2368b903` |

Recompute with `sha256sum <file>` (or equivalent) against this table at any point during Phase 2A execution to detect drift. If a mismatch is found, first check `research/RP001_PHASE2A_DEVIATION_LOG.md` for a corresponding entry (as with D-09) before assuming tampering — a logged, content-verified path change is not the same as an unlogged substantive edit.

## What "locked" means operationally

The specific items these six documents themselves designate as immovable (restated here for a single point of reference, not a new list): F_INST_01's definition, rank normalization, return horizon construction, the break interval's boundary dates (late-Aug to late-Oct 2025, point estimate 2025-09-25), liquidity grouping definition, volatility regime definition, neutralization method (cross-sectional OLS residualization), multiple-testing method (Benjamini-Hochberg, α=0.10), the five hypotheses H-C1–H-C5 exactly as stated, and the six-phase execution sequence.

## Amendment history

**2026-09-08:** Hash table updated to reflect commit `190c568`'s (2026-08-03) path-only relocation of 5 of the 6 files into `research/`. See Deviation D-09, `research/RP001_PHASE2A_DEVIATION_LOG.md`, for the full account and confirmation that no substantive content changed. Prior to this amendment, the table and "Verification performed" statement incorrectly implied the six files remained byte-identical to the `82bc4a3` lock commit.

**2026-09-13:** `research/RP001_CONFIRMATORY_HYPOTHESES.md`'s hash updated (`30ad7bd0...` → `7d154806...`) following a title/intro-line terminology clarification — "Pre-Registered Confirmatory Hypotheses" is now labeled explicitly as a **post-exploration prospective confirmatory protocol lock**, to prevent the standalone title from being read as claiming the entire RP-001 study (including the exploratory phase that produced the original hypotheses) was preregistered before any data was seen. See Deviation D-10, `research/RP001_PHASE2A_DEVIATION_LOG.md`. No hypothesis, threshold, sample definition, or method changed.
