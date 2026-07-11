# RP-001 Milestone 1C+: Mechanism Analysis

Goal per your instruction: understand why the signal exists, when, and when it disappears — not re-verify performance. No Portfolio Construction, Backtest, Sharpe, or Max Drawdown anywhere below.

## 1. Structural Break

**Rolling 60-day IC (F_INST_01_foreign, t+5) collapses over the sample**: starts at 0.089, ends at 0.006. CUSUM break detection identifies a statistically significant single break point at **2025-09-24** (Welch t=3.41, p=0.0007): pre-break mean IC = 0.052, post-break mean IC = **−0.008**. This is not a gradual fade dressed up as a "break" — it's a real, testable discontinuity, and it's the single most important fact in this analysis. Whatever "the signal" is, it materially stopped existing around late September 2025, roughly 15 months into the 2-year sample.

## 2. Cross-sectional Stability

| Dimension | Pattern | Note |
|---|---|---|
| Market Cap | Mid (0.043) > Large (0.031) > Small (0.022) | **Non-monotonic** — contradicts a simple "stronger in small caps" story; mid-cap names show the strongest signal |
| Industry | Sector 24 strong (0.044), Sector 25 near-zero (−0.008) | Real heterogeneity, though only 2 sectors have enough sample depth to test with this stock count |
| Value/Growth (PBR) | Blend (0.040) > Value (0.025) > Growth (0.016) | Also non-monotonic — strongest in the middle, not at either extreme |
| Liquidity | Illiquid (0.034) ≈ Mid (0.031) > Liquid (0.010) | **Monotonic and economically sensible** — the one cross-sectional cut that fits a clean "slower price discovery in illiquid names" story |

## 3. Market Regime

| Regime | Mean IC |
|---|---|
| Bear | 0.038 |
| Sideways | 0.032 |
| Bull | 0.018 |
| **Low Volatility** | **0.051** |
| **High Volatility** | **0.006** |

Volatility regime is the sharper of the two splits — IC is essentially zero in high-volatility periods and strong in low-volatility ones. Directionally consistent with Bear > Bull, since Bear periods in this sample weren't necessarily the highest-volatility ones (a real distinction between "market is falling" and "market is chaotic" that this dataset lets us separate).

## 4. Interaction Analysis — the raw numbers are misleading, and I'm not passing them through uncritically

All four Foreign-interactions show higher raw IC than plain Foreign flow (0.029):

| Interaction | Raw IC | t-stat |
|---|---|---|
| Foreign × Liquidity | 0.073 | 6.41 |
| Foreign × Volatility | 0.065 | 5.46 |
| Foreign × Momentum | 0.056 | 5.44 |
| Foreign × Size | 0.037 | 4.25 |

**Tested whether this is a genuine interaction effect, using the same residualization method Milestone 1C applied to F_INT_02/03.** For Foreign × Liquidity: after controlling for plain Foreign rank alone, IC only drops modestly (0.073 → 0.066) — but after controlling for **both** plain Foreign rank and plain Liquidity rank together, residual IC collapses to **−0.005** (icir −0.04, indistinguishable from zero). **The apparent 2.5× amplification is almost entirely additive, not multiplicative** — it's substantially liquidity's own well-documented return premium combined with foreign flow's own effect, not evidence that foreign flow "matters more" when liquidity is high. I did not run the identical decomposition for the other three interactions given time, but given the parallel pattern already found for F_INT_02/F_INT_03 in Milestone 1C, **the same caution should apply to all four until each is individually tested** — none of these interaction numbers should be read at face value.

## 5. Economic Interpretation

Putting the pieces together, not just listing them:

**What the evidence is consistent with:** foreign institutional investors carried a real, if modest, information advantage through roughly mid-2025 — reflected in returns building over 1-to-5 days rather than reversing (informed trading, not price pressure), strongest in calm markets and less-liquid names (conditions where a genuine informational edge has time to be reflected before being arbitraged away or drowned out by noise), and weakest in mega-caps and high-volatility periods (conditions where the edge is already competed away or swamped).

**What the evidence is NOT consistent with:** a clean, permanent, unconditional predictive relationship. The structural break is the dominant fact here — a signal that worked from 2024 through September 2025 and then stopped is more consistent with **either** a genuine shift in Taiwan market efficiency/foreign flow composition (e.g., a rising share of passive/index-driven foreign flow diluting the informed-trading component over time — a real, testable hypothesis for a future study, not confirmed here) **or** a regime-specific effect tied to the market conditions that happened to prevail pre-September 2025 (lower volatility, per the volatility-regime finding) rather than a standalone "foreign flow" effect at all.

**Most honest single-sentence summary:** the data is more consistent with "foreign flow predicts returns when markets are calm and prices are slow to adjust" than with "foreign flow predicts returns."

## 6. Freeze Recommendation — Research-Grade vs. Data Artifact

**Research-Grade (real, but conditional — not unconditionally Freeze-ready):**
- **F_INST_01_foreign** — the underlying relationship is real and economically interpretable (informed trading, price discovery), but it is regime-dependent (low-vol only) and time-limited (pre-Sept-2025 only). Any Freeze decision on this feature must carry both conditions explicitly, not present it as a standalone predictor.
- **F_INST_07_flow_to_volume** — retained independent information beyond F_INST_05 in Milestone 1C; not separately mechanism-tested this round, carries the same regime-dependence caveats by inheritance until tested.

**Likely Data Artifact, not a genuine effect:**
- **F_INT_04_foreign_x_liquidity** — confirmed via residualization: the raw IC is substantially decomposable into its additive components, not a real interaction effect.
- **F_INT_02_flow_x_size, F_INT_03_flow_x_liquidity** (from Milestone 1C) — sector-neutralization already showed the same pattern (75%+ of raw IC explained away).
- By extension, **F_INT_05_foreign_x_volatility and F_INT_06_foreign_x_size** should be treated as *suspected* artifacts pending the same test, not assumed genuine because they weren't individually checked.

**F_INST_05_aggregate and F_INST_06_value_proxy** remain what Milestone 1C already found: the aggregate dilutes the one real component (F_INST_01), and F_INST_06 is redundant with F_INST_05. Nothing in this mechanism analysis changes that.

**F_INT_01/F_INT_07_foreign_x_momentum** stays Experimental as instructed, and this round adds a reason beyond the original instruction: its strong raw numbers are exactly the shape that turned out to be artifactual for the liquidity interaction — worth treating with the same suspicion until individually residualized.

Stopping here — no Portfolio Construction, Backtest, Sharpe, Max Drawdown, or Feature Freeze performed.
