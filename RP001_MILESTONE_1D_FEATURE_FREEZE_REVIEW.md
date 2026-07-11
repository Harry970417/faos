# RP-001 Milestone 1D: Feature Freeze Review

No Portfolio Construction, Backtest, Sharpe, Max Drawdown, Transaction Cost Analysis, Trading Strategy, or Investment Recommendation anywhere in this milestone. Full per-feature evidence in `RP001_FEATURE_DECISION_TABLE.md`.

## What Feature Freeze means here — stated explicitly, not left implicit

Freeze does **not** mean: permanently valid, directly tradeable, deployable, or performance-validated. Freeze means: **under the current sample, methods, and robustness tests applied, the research determination for this feature is stable enough that it should not be changed further by design preference alone** — any future change requires new evidence (a new sample, a new test), the same standard already applied to ECC itself.

## Status taxonomy applied

Frozen — Research-Grade / Frozen — Conditional / Secondary Candidate / Experimental / Deprecated / Rejected / Confirmed Artifact / Inconclusive — all eight used, none skipped for convenience (see decision table).

## F_INST_01 — Frozen, Conditional (the only feature reaching this tier)

**No feature in this study qualifies for unconditional "Frozen — Research-Grade."** F_INST_01 is Frozen — **Conditional**, and the following conditions are permanent, mandatory attachments to any citation of this result, not optional caveats:

- Effect concentrated before the structural-break interval (approx. through Q3 2025)
- Post-break IC is approximately zero, not merely smaller
- Stronger in illiquid / mid-liquidity names; weak in liquid, large-cap names
- The low-volatility result is **not independent of the break** — the double-sort in Milestone 1C-R showed Low-vol & Post-break IC ≈ 0
- Cannot be described as universally stable
- Cannot be described as a confirmed causal informed-trading mechanism — "consistent with," never "demonstrates"

These six conditions are now written into `FEATURE_REGISTRY.md` as permanent, not restated per-use text.

## F_INST_07 — held at Secondary Candidate

Remains Secondary Candidate, not elevated. Its own structural break does not survive permutation-corrected testing (p=0.171) — the one-day proximity to F_INST_01's break date is suggestive, not independent confirmation, and is not being treated as such. Would need its own full robustness pass (Milestone-1C-R-equivalent) to reach Conditional status.

## Interaction Features — all seven completed, all seven resolved

Per your instruction, checked whether each had completed joint residualization against its own constituent main effects (not a third control variable) before assigning status. **Three gaps existed and were closed this milestone rather than left as "Pending Test":** F_INT_01 (aggregate×momentum), F_INT_02 (aggregate×size), and F_INT_03 (aggregate×liquidity) had previously only been tested against sector/mcap as external controls, not against their own two constituents jointly. That test was run this round.

**Result: all seven interaction features are Confirmed Artifact.** No exceptions, no feature retained as Research-Grade because of raw IC or FDR survival alone — F_INT_01, F_INT_03, and F_INT_07 all passed raw-IC FDR correction and are Confirmed Artifact anyway, precisely because FDR survival was not treated as sufficient.

## Statistical Significance vs. Mechanism Validity — the standing principle for RP-001

Written explicitly, not left implicit:

- **FDR significance is necessary but not sufficient.** Three of nine FDR-surviving results in this study (F_INT_01, F_INT_03, F_INT_07) are Confirmed Artifacts.
- **Neutralization and residualization can overturn apparent significance.** Every interaction feature's headline IC was explained away this way.
- **Statistical significance does not equal incremental information.** A feature can be significant and entirely redundant (F_INST_06 vs. F_INST_05) or significant and entirely explained by its components (every interaction tested).
- **Incremental information does not equal tradeable performance.** Not tested in this milestone or any prior one — RP-001 has not yet made, and does not make here, any investment performance claim.
- **This milestone draws no investment performance conclusions of any kind.**
