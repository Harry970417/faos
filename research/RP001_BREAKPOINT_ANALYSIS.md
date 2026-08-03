# RP-001 Breakpoint Analysis (Milestone 1C-R, Part 1)

**Method note:** `ruptures` (Bai-Perron style multiple-breakpoint detection) failed to build in this environment — no C++ compiler available. Used a self-implemented **Quandt-Andrews sup-Wald test with permutation p-values** instead, which is the standard formal method for an unknown single breakpoint and directly answers your concern: it tests *every* candidate date in a trimmed 15%–85% window and reports the maximum test statistic, with a p-value computed by permuting the IC series 2,000 times and asking how often a *random* series produces a sup-statistic this large. This properly accounts for "the break date was chosen by searching the same data" — a naive single Welch t-test at a pre-picked date does not.

## 1. Unknown-Breakpoint Test

| Feature | Sup-Wald break date | sup\|t\| | Permutation p-value |
|---|---|---|---|
| F_INST_01_foreign | 2025-09-25 | 3.45 | **0.0105** |
| F_INST_07_flow_to_volume | 2025-09-26 | 2.39 | 0.171 (not significant) |

F_INST_01's break survives proper correction for the search — this is not an artifact of hunting for the best-looking split point. F_INST_07's does not survive, despite landing on almost the same calendar date (see Section 4).

## 2. Break-Date Sensitivity (±20, ±40 trading days)

| Split date | Offset | Pre-mean IC | Post-mean IC | Welch t | p-value |
|---|---|---|---|---|---|
| 2025-07-30 | −40d | 0.044 | 0.013 | 1.82 | 0.069 |
| 2025-08-27 | −20d | 0.046 | 0.006 | 2.34 | 0.020 |
| **2025-09-24** | **0d** | **0.052** | **−0.008** | **3.41** | **0.0007** |
| 2025-10-28 | +20d | 0.046 | −0.004 | 2.73 | 0.007 |
| 2025-11-25 | +40d | 0.040 | 0.003 | 1.94 | 0.054 |

Significance peaks at the estimated break and weakens gradually toward the edges of the ±40-day window — exactly the shape a genuine break should produce (a data-mined artifact would more likely show a sharp, isolated spike with no surrounding consistency, or be flat/insensitive everywhere). The qualitative conclusion — meaningfully lower IC after the split than before — holds across all five tested dates, three of them independently significant at p<0.05. **This is better described as a break interval of roughly late-August to late-October 2025, not a single calendar day**, even though the sup-Wald search happens to center almost exactly on 09-24/09-25.

## 3. Rolling-Window Robustness

| Window | Start | Peak | Trough | End |
|---|---|---|---|---|
| 40-day | 0.195 | 0.197 (2024-07-31) | −0.054 (2025-12-08) | −0.0001 |
| 90-day | 0.083 | 0.085 (2024-09-06) | −0.037 (2026-06-11) | −0.0095 |

Both windows — computed completely independently, different smoothing — show the same shape: elevated through most of 2024 into 2025, declining sharply thereafter, ending near or below zero. This is a **persistent regime shift**, not an artifact of one particular smoothing choice.

## 4. Feature Consistency

F_INST_01 and F_INST_07 break within **1 calendar day** of each other (2025-09-25 vs. 2025-09-26) — strongly suggestive of a shared, market-wide phenomenon rather than two independent feature-specific artifacts. **But this needs a careful qualifier**: F_INST_07's own break is not independently statistically significant (permutation p=0.171). The dates coinciding is consistent with a common underlying cause, but F_INST_07 alone does not provide independent confirmatory evidence — its apparent break could simply be riding on the same market conditions without carrying its own distinguishable signal.

## 5. Calendar / Event Check

Background check only — searched for market-structure, data-provider, or institutional-classification changes near late September 2025. **No specific, verified event was found and none is being proposed as the cause.** Absent clear evidence, no story is being assigned to this date — the finding stands as "a statistically confirmed break exists in this window," not "X event caused it."

## Classification

**F_INST_01_foreign: Confirmed structural break**, more precisely stated as a **break interval (late Aug – late Oct 2025)** rather than one exact day. Survives unknown-breakpoint testing with permutation-corrected significance, survives ±40-day sensitivity, survives two independent rolling-window smoothings.

**F_INST_07_flow_to_volume: Break interval consistent with F_INST_01's, but not independently confirmed.** Timing coincidence noted, not treated as proof.
