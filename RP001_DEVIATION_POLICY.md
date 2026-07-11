# RP-001 Phase 2A: Deviation Policy

Governs any change to the locked specification (`RP001_FULL_UNIVERSE_SPEC.md`, `RP001_CONFIRMATORY_HYPOTHESES.md`) during Phase 2A execution.

## The rule

**Any deviation from the locked specification must be logged — with reasoning — before the confirmatory tests are run on the affected data, never after seeing whether it changes the result.** A deviation logged after results are known is not a deviation, it is post-hoc adjustment, and invalidates the confirmatory status of whatever hypothesis it touches.

## What counts as a legitimate reason for a deviation

- A specified data field or dataset is genuinely unavailable for part of the full universe (e.g., PBR data missing for some TPEx names)
- A specified rule cannot be mechanically implemented as written (e.g., no clean data source exists for daily disposition-stock status at full-universe scale)
- A specified threshold produces a degenerate result through no fault of calibration (e.g., a liquidity tercile that ends up empty for a specific date due to universe size)

## What does not count as a legitimate reason

- "The original threshold doesn't produce a significant result at full-universe scale"
- "A different volatility window fits the full-universe data better"
- "The break interval doesn't line up as cleanly, so we adjusted it"
- Any reason discovered by first running the test and then looking for a justification

## Deviation Log Format

Same structure as `RP001_LOG.md`, in a dedicated `RP001_PHASE2A_DEVIATION_LOG.md` to be created at the start of execution: **Deviation / Original Spec / Reason / Decided Before or After Seeing Results (must be "Before") / Impact on Which Hypothesis**. Every deviation is disclosed in the final Phase 2A report, not filtered to the ones that seem inconsequential.

## Escalation

Any deviation affecting the definition of F_INST_01 itself, rank normalization, return horizon construction, or the break interval's boundary dates requires explicit approval before proceeding — these are the "must not be reopened" items from your original instruction, and a deviation request on any of them pauses execution rather than proceeding with a logged note.
