# RP-001 Phase 2A: Confirmatory Acceptance Criteria

Fixed before execution, per hypothesis. No single p-value is ever the sole criterion — each verdict requires agreement across multiple, independently-checkable measures: effect direction, mean IC, Newey-West t-stat, 95% CI, BH-FDR q-value, and (where applicable) break-period contrast or monotonicity.

## Verdict definitions (used identically across all five hypotheses)

- **Replicated:** direction matches the original finding, and the primary significance measure (Newey-West t, BH-FDR q) clears the threshold at the pre-specified horizon(s).
- **Partially Replicated:** direction matches but significance is inconsistent across horizons or measures (e.g., significant NW t but FDR q misses, or significant at some but not all of t+1/t+3/t+5).
- **Not Replicated:** direction contradicts the original finding, or the effect is null where the original found a real effect (and vice versa).
- **Inconclusive:** insufficient sample size in the relevant sub-group (e.g., a liquidity tercile or break-period cell with too few full-universe observations to test reliably) — reported as its own outcome, not folded into "Not Replicated."

## H-C1 (pre-break positive IC)

Replicated: positive IC at all 3 horizons (t+1/t+3/t+5), NW t>1.96 at ≥2 of 3, and BH-FDR q<0.10 survives at t+5 (the horizon strongest in the original study). Partially Replicated: positive direction at ≥2/3 horizons but full significance bar not met. Not Replicated: negative or null IC at the majority of horizons.

## H-C2 (post-break null)

Replicated: |mean IC| < 0.01 at t+5 AND NW |t| < 1.96. Partially Replicated: IC small but marginally significant, or not small but also not significant (mixed). Not Replicated: IC clearly significant and comparable in magnitude to the pre-break effect (i.e., the break did not hold).

## H-C3 (liquidity conditionality)

Replicated: Illiquid and Mid terciles both show higher mean IC and higher NW t than Liquid tercile, with Liquid tercile NW t not significant. Partially Replicated: direction correct but not clean (e.g., only one of Illiquid/Mid clearly stronger). Not Replicated: Liquid tercile shows equal or stronger IC than Illiquid/Mid.

## H-C4 (volatility effect is break-conditional)

Replicated: Low-vol & Post-break cell shows |mean IC| < 0.01 and NW |t| < 1.96, while Low-vol & Pre-break remains significant (replicating the double-sort asymmetry). Partially Replicated: Low-vol & Post-break shows attenuation but not full collapse. Not Replicated: Low-vol & Post-break remains clearly significant (would mean volatility is an independent effect after all, contradicting the original finding).

## H-C5 (no genuine interactions)

Replicated: all seven interaction features show residual (jointly-controlled) NW |t| < 1.96 at t+5. Partially Replicated: 5 or 6 of 7 replicate, 1–2 show unexpected significant residual. Not Replicated: 3 or more interactions show genuine significant incremental IC.

## Overall Phase 2A verdict

No single hypothesis result determines whether Phase 2A "succeeds" — the final Phase 2A report states each of H-C1 through H-C5's verdict independently, and the RP-001 formal conclusion is updated to reflect exactly which conditions replicated and which did not. A mix of Replicated/Partially Replicated/Not Replicated across the five is a valid, reportable outcome, not a failure requiring re-analysis.
