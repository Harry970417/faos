# RP-001 Interaction Incremental-Information Tests (Milestone 1C-R, Part 4)

Method for each: residualize the interaction term against **both** constituent main effects simultaneously (not one at a time), then test whether the residual still predicts returns. A raw product term having a high IC proves nothing on its own — this is the test that actually distinguishes a genuine interaction from an additive recombination.

## F_INT_04 — Foreign × Liquidity (tested in Milestone 1C+, restated for completeness)

Raw IC 0.073 (t=6.41) → residualized against both components: **−0.005 (t=−0.04)**. Collapses to indistinguishable from zero.
**Verdict: Additive Recombination Artifact.**

## F_INT_05 — Foreign × Volatility

| Horizon | Raw IC (t_NW) | Residualized IC (t_NW) |
|---|---|---|
| t+1 | 0.020 (1.69) | −0.010 (−1.51) |
| t+3 | 0.041 (2.48) | −0.012 (−1.43) |
| t+5 | 0.065 (3.22) | −0.011 (−1.34) |

Residualized IC pre-break: −0.009 (n=292) — post-break: −0.014 (n=183). Residualized + sector-neutral (t+5): −0.006 (t=−1.09).

The raw signal fully disappears under proper residualization — and, notably, the residual isn't just near-zero, it's **consistently negative** across horizons and both break periods, which is if anything *stronger* evidence against a genuine positive interaction than a residual that merely vanished.
**Verdict: Inconclusive by the pre-set |t|>2 threshold, but leaning artifact** — the consistent negative sign across every cut argues against calling this "no effect either way."

## F_INT_06 — Foreign × Size

| Horizon | Raw IC (t_NW) | Residualized IC (t_NW) |
|---|---|---|
| t+1 | 0.017 (1.94) | −0.004 (−0.57) |
| t+3 | 0.027 (2.39) | −0.002 (−0.27) |
| t+5 | 0.037 (2.74) | −0.002 (−0.28) |

Residualized IC pre-break: −0.004 (n=302) — post-break: 0.0001 (n=183). Residualized + sector-neutral (t+5): −0.007 (t=−0.98).
**Verdict: Additive Recombination Artifact.** Clean collapse to zero across every cut, no ambiguity.

## F_INT_07 — Foreign × Momentum (the feature designated Experimental)

| Horizon | Raw IC (t_NW) | Residualized IC (t_NW) |
|---|---|---|
| t+1 | 0.026 (2.47) | 0.009 (1.18) |
| t+3 | 0.036 (2.48) | 0.005 (0.52) |
| t+5 | 0.056 (3.23) | 0.0004 (0.04) |

Residualized IC pre-break: **0.017** (n=282) — post-break: **−0.025** (n=183, sign flip). Residualized + sector-neutral (t+5): −0.007 (t=−0.87).

This is the most informative test in the set, given the instruction that F_INT_01/F_INT_07 stays Experimental regardless of outcome: its raw numbers were the strongest-looking of any interaction tested across both this milestone and Milestone 1C+, and it **still fully collapses under proper decomposition** — including a sign flip after the structural break. This is direct evidence, not a hunch, for why its Experimental status is appropriate rather than overly cautious.
**Verdict: Additive Recombination Artifact.**

## Summary

| Feature | Verdict |
|---|---|
| F_INT_04 (Liquidity) | Additive Recombination Artifact |
| F_INT_05 (Volatility) | Inconclusive, leaning Artifact (consistently negative residual) |
| F_INT_06 (Size) | Additive Recombination Artifact |
| F_INT_07/F_INT_01 (Momentum) | Additive Recombination Artifact |

**None of the four Foreign-interaction features tested show a genuine incremental interaction effect that survives proper decomposition.** The pattern is consistent: impressive raw products, explained away almost entirely by the two constituent main effects once both are controlled for simultaneously.
