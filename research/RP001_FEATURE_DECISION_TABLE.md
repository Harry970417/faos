# RP-001 Feature Decision Table (Milestone 1D)

Every cell below is a real, previously-computed result — nothing new asserted at Freeze time. Two interaction tests (F_INT_01, F_INT_02, F_INT_03 against their own constituents) were completed this milestone to close gaps the prior rounds left open; all others restate earlier findings for completeness.

| Feature ID | Name | Final Status | Raw IC (t+5) | Neutralized/Residualized | Pre-break IC | Post-break IC | FDR (q<0.10) | Incremental Info | Main Limitation |
|---|---|---|---|---|---|---|---|---|---|
| F_INST_01 | Foreign net flow | **Frozen — Conditional** | 0.029 (t=2.74) | Mcap-neutral 101%, sector-neutral 62% retained | 0.052 | −0.008 | Yes (multiple tests) | N/A (main effect) | Break-, regime-, and liquidity-conditional; never unconditional |
| F_INST_02 | Trust net flow | Rejected | −0.005 (t=−0.46) | Not tested (no signal to explain) | — | — | No | N/A | No evidence at any horizon |
| F_INST_03 | Dealer proprietary flow | Inconclusive | 0.021 (t=2.36 at t+5 only) | Not tested | — | — | No (q=0.10, borderline) | N/A | Only marginal, single horizon |
| F_INST_04 | Dealer hedging flow | Rejected | 0.006 (t=0.75) | Not tested | — | — | No | N/A | No evidence at any horizon |
| F_INST_05 | Aggregate (5-category sum) | Deprecated | 0.015 (t=1.38) | — | — | — | No | Diluted vs. F_INST_01 | Sums in non-informative categories, weakens the real signal |
| F_INST_06 | Value proxy | Deprecated | 0.016 (t=1.43) | Residual vs F_INST_05: ≈0.002 | — | — | No | **Confirmed ≈0 beyond F_INST_05** | Redundant, confirmed via incremental-IC test |
| F_INST_07 | Flow-to-volume | **Secondary Candidate** | 0.022 (t=1.98) | Retains ~60% of own raw IC beyond F_INST_05 | — | — | No | Real, moderate | Own structural break not permutation-confirmed (p=0.171) |
| F_INST_08 | Streak | Inconclusive | 0.024 (t=1.77) | Not tested | — | — | No | N/A | Weak, marginal only at t+5 |
| F_INST_09 | Change rate | Rejected | 0.001 (t=0.07) | Not tested | — | — | No | N/A | No evidence at any horizon |
| F_INT_01 | Aggregate × Momentum | **Confirmed Artifact** | 0.044 (t=2.57) | Residual (vs both constituents): −0.004 (t=−0.42) | 0.001 | −0.011 | Yes (raw only) | **Confirmed ≈0** | Passes FDR on raw IC, fails joint residualization — exactly the necessary-not-sufficient case |
| F_INT_02 | Aggregate × Size | **Confirmed Artifact** | 0.023 (t=1.68) | Residual (vs both constituents): −0.003 (t=−0.38) | −0.006 | 0.001 | No | **Confirmed ≈0** | Additive recombination of two weak main effects |
| F_INT_03 | Aggregate × Liquidity | **Confirmed Artifact** | 0.061 (t=3.18) | Residual (vs both constituents): −0.004 (t=−0.46) | −0.010 | 0.007 | Yes (raw only) | **Confirmed ≈0** | Strongest raw IC in the study; fully explained by its two components once jointly controlled |
| F_INT_04 | Foreign × Liquidity | **Confirmed Artifact** | 0.073 (t=6.41) | Residual: −0.005 (t=−0.04) | — | — | No | **Confirmed ≈0** | Highest raw t-stat of any feature tested; entirely additive |
| F_INT_05 | Foreign × Volatility | **Confirmed Artifact** | 0.065 (t=3.22) | Residual: −0.011 (t=−1.34), consistently negative pre/post break | −0.009 | −0.014 | No | **Confirmed ≈0** (consistently negative residual, not positive) | Raw signal fully explained by components; residual sign worth future note, not enough to claim a real negative effect |
| F_INT_06 | Foreign × Size | **Confirmed Artifact** | 0.037 (t=2.74) | Residual: −0.002 (t=−0.28) | −0.004 | 0.0001 | No | **Confirmed ≈0** | Clean collapse across every cut tested |
| F_INT_07 | Foreign × Momentum | **Experimental** (per instruction, additionally evidenced) | 0.056 (t=3.23) | Residual: 0.0004 (t=0.04), sign-flips negative post-break | 0.017 | −0.025 | Yes (raw only) | **Confirmed ≈0** | Strongest raw numbers of any interaction; fully collapses; held Experimental by explicit instruction, now directly evidenced rather than just cautious |

## Acceptable formal wording (required for any future reference to these features)

- F_INST_01: *"Foreign investor net flow showed conditional predictive power for cross-sectional returns, concentrated in a pre-break interval (through approximately Q3 2025), low-volatility regimes, and illiquid-to-mid-liquidity names."*
- Interaction features generally: *"Raw interaction terms showed elevated IC that did not survive joint residualization against their constituent main effects, consistent with additive recombination rather than genuine interaction."*

## Prohibited wording

- "Foreign flow predicts returns" (unqualified — omits the break/regime/liquidity conditions)
- "Demonstrates informed trading" or any causal claim (no causal identification design was used anywhere in RP-001)
- "Robust factor" applied to any interaction feature (all confirmed or functionally confirmed artifacts)
- "Statistically significant" used alone as a synonym for "real" or "tradeable" (F_INT_01/03/07's FDR survival despite being artifacts is the standing counterexample)
