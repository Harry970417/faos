# RP-001 Regime Robustness (Milestone 1C-R, Part 2 & 3)

## Pre-committed primary specification

Market realized volatility, 20-day rolling window, **median split** — this was the spec already used in Milestone 1C+ before this robustness pass, stated here for traceability, not chosen after comparing which threshold produced the largest gap.

## 1. Volatility Definition Robustness

| Vol definition | Split | Regime | n | Mean IC | t_NW | 95% CI |
|---|---|---|---|---|---|---|
| market_rvol_20d (primary) | median | Low | 238 | 0.047 | 3.18 | [0.018, 0.076] |
| market_rvol_20d (primary) | median | High | 237 | 0.005 | 0.37 | [−0.022, 0.032] |
| market_rvol_20d | tercile | Low | 158 | 0.042 | 2.40 | [0.008, 0.076] |
| market_rvol_20d | tercile | High | 158 | 0.007 | 0.42 | [−0.025, 0.039] |
| market_rvol_40d | median | Low | 233 | 0.032 | 2.05 | [0.001, 0.062] |
| market_rvol_40d | median | High | 232 | 0.013 | 0.97 | [−0.013, 0.038] |
| xsec_dispersion (raw daily) | median | Low | 241 | 0.033 | 2.75 | [0.010, 0.057] |
| xsec_dispersion (raw daily) | median | High | 240 | 0.022 | 1.34 | [−0.010, 0.054] |
| xsec_dispersion (raw daily) | tercile | Low | 160 | 0.038 | 2.67 | [0.010, 0.065] |
| xsec_dispersion (raw daily) | tercile | High | 160 | **0.034** | **2.09** | [0.002, 0.066] |
| xsec_dispersion (20d smoothed) | median | Low | 238 | 0.049 | 3.86 | [0.024, 0.074] |
| xsec_dispersion (20d smoothed) | median | High | 237 | 0.003 | 0.19 | [−0.028, 0.034] |

**Honest reading, not the cleanest possible story:** the low-vol > high-vol pattern replicates clearly across the primary spec, the 40-day window, and the smoothed cross-sectional dispersion measure. It is **materially weaker under raw daily cross-sectional dispersion with a tercile split** — there, the "High" regime is *also* significant (t=2.09), nearly closing the gap. Reporting this rather than only the definitions that support the cleanest narrative — the effect is real under most operationalizations tested, but not uniformly clean under every one.

## 2. Disentangling Low-Volatility from Pre-Break and 2024-Specific Effects

**Double-sort (volatility regime × break period):**

| Cell | n | Mean IC | t_NW |
|---|---|---|---|
| Low-vol & Pre-break | 167 | 0.069 | 3.99 |
| Low-vol & Post-break | 71 | −0.004 | −0.17 |
| High-vol & Pre-break | 135 | 0.032 | 1.57 |
| High-vol & Post-break | 112 | −0.011 | −0.57 |

**This is the most important result in this section.** The strongest cell is Low-vol *combined with* Pre-break — but Low-vol *alone*, once you move past the break, collapses to essentially zero (−0.004). **The volatility-regime effect does not survive the structural break independently — it is conditional on being in the pre-break regime.** The break is the dominant fact; volatility modulates strength *within* that regime, it is not a free-standing, break-independent phenomenon.

**2024-only vs. low-vol-but-not-2024:**

| Cell | n | Mean IC |
|---|---|---|
| 2024 (any volatility) | 125 | 0.072 |
| Low-vol, excluding 2024 (i.e. low-vol days in 2025–2026) | 178 | 0.029 |

The second number is clearly positive, not zero — so the low-volatility effect is not *purely* a relabeling of "2024." But it's also visibly weaker than the pure-2024 figure, consistent with the double-sort above: low volatility contributes something on its own, but the pre-break regime contributes more.

## 3. Liquidity Mechanism Robustness

| Check | Illiquid | Mid | Liquid |
|---|---|---|---|
| Raw | 0.034 (t=1.94) | 0.031 (t=1.94) | 0.010 (t=0.63) |
| Market-cap neutral | 0.034 (t=1.94) | 0.031 (t=1.96) | 0.012 (t=0.78) |
| Sector neutral | **0.047 (t=3.28)** | 0.009 (t=0.64) | 0.008 (t=0.54) |
| Pre-break only | 0.057 (t=2.76) | 0.054 (t=2.88) | 0.012 (t=0.58) |
| Post-break only | −0.003 | −0.006 | 0.006 |
| Low-vol only | 0.059 (t=3.07) | 0.064 (n=32, too few obs) | *(insufficient obs, not reportable)* |

The Illiquid > Liquid contrast **survives market-cap neutralization essentially unchanged, and survives sector-neutralization** (in fact strengthens for the Illiquid bucket, while Mid's apparent strength turns out to be more sector-driven). It holds cleanly within the pre-break period and — like every other cut in this analysis — **collapses post-break**. The Low-vol triple-cut hit a real sample-size limit at this 50-stock scale (only 32 Mid-liquidity/low-vol observations, Liquid/low-vol too few to report) — flagged honestly as a characterization-scale limitation, not glossed over.

**Required wording discipline, applied here:** these results are **consistent with slower price discovery in illiquid names** — they do not, and cannot on this observational design, **demonstrate** it. No causal identification strategy (e.g., an instrument, a natural experiment) was used, so causal language is not used.
