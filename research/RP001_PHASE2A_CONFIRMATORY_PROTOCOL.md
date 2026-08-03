# RP-001 Phase 2A: Confirmatory Validation Protocol

**Status: Protocol only. Not started. No full-universe data has been pulled.** This document is the master reference for Phase 2A — it does not duplicate the other five files, it states what they are for and how they fit together.

## Purpose

Milestone 1D closed RP-001's exploratory factor-research phase with one conditional finding (F_INST_01) whose defining conditions — the structural break, the volatility-regime dependency, the liquidity dependency — were all discovered on the same 50-stock sample used to test them. Phase 2A exists to ask, on independent data with a locked specification, whether those same conditions hold. **This is a confirmatory study. It is not a second round of feature discovery, and it is not a step toward portfolio construction** — those are separate, later decisions this Protocol does not authorize.

## The five hypotheses (detail: `research/RP001_CONFIRMATORY_HYPOTHESES.md`)

H-C1 (pre-break positive IC), H-C2 (post-break null), H-C3 (liquidity conditionality), H-C4 (volatility effect is break-conditional, not independent), H-C5 (all seven interactions remain artifacts). Nothing beyond these five is tested. No new feature, no new grouping variable, no new breakpoint search.

## What is locked and what can move

**Locked, not to be reopened without pausing execution** (per `research/RP001_DEVIATION_POLICY.md`'s escalation rule): F_INST_01's definition, rank normalization, return horizon construction, the break interval's boundary dates, liquidity grouping definition, volatility regime definition, neutralization method, multiple-testing method.

**What Phase 2A newly builds**: the full-universe, survivorship-bias-free stock pool itself (`research/RP001_FULL_UNIVERSE_SPEC.md`) — this is genuinely new construction work, not a reuse of the 50-stock characterization panel, because confirmatory validation on the same sample would prove nothing.

## How deviations are handled

Any point where the locked specification cannot be mechanically applied to full-universe data must be logged **before** the affected test is run, with an explicit reason, using the criteria in `research/RP001_DEVIATION_POLICY.md`. A deviation adopted because it produces a better-looking result is not a deviation — it is disqualifying for whichever hypothesis it touches.

## How success and failure are judged

Each of the five hypotheses gets an independent verdict — Replicated / Partially Replicated / Not Replicated / Inconclusive — using the multi-measure criteria in `research/RP001_CONFIRMATORY_ACCEPTANCE_CRITERIA.md` (direction, mean IC, Newey-West t, CI, BH-FDR q, and hypothesis-specific structural checks like monotonicity or break-period contrast). No hypothesis is judged on a single p-value. A mixed outcome across the five — some replicating, some not — is a valid, complete result, not something to be resolved by re-testing.

## Sequencing

`research/RP001_PHASE2A_EXECUTION_PLAN.md` — six phases, gated, starting with pre-execution checklist and universe construction, ending in a confirmatory results report. **Execution does not begin until this Protocol (all six documents) is approved.**

## What this Protocol explicitly does not authorize

Portfolio optimization, long-short strategy tuning, Sharpe/drawdown conclusions, transaction-cost analysis, new interaction discovery, new breakpoint search, or re-selecting favorable conditions once full-universe data is available. These require a separate, later decision — approving this Protocol is not approving any of them.
