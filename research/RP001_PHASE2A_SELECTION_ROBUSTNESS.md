# RP-001 Selection-Robustness Extension (Graduate-Stage Addendum)

**Status: NOT part of the locked Phase 2A protocol.** This is a new, separate, unlocked analysis added 2026-09-13 in response to a research-governance review ("05 FAOS — Research Governance Graduate-Level Upgrade"), motivated by `research/RP001_LIMITATIONS_v0.2.md`'s finding that the 69.8% confirmatory sample differs systematically from the excluded 30.2% on liquidity, price, and volatility. It does not change, re-run, or re-open any of H-C1–H-C5's locked verdicts (`research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`) — those stand exactly as reported. Code: `research/rp001_phase2a_selection_robustness.py`. Full output: `rp001_data/phase2a/processed/rp001_selection_robustness_results.json`.

## What this asks

Not "is the 69.8%-vs-30.2% inclusion split itself biased" (already answered, quantitatively, in `RP001_LIMITATIONS_v0.2.md`) — but a narrower, directly answerable question using data already on disk: **within the included, coverage-gate-passing sample, is H-C1/H-C2/H-C4's reported null/near-null average result uniform across the liquidity spectrum, or is it an average masking offsetting effects?**

Method: exactly the same liquidity tercile column (`liq_tercile`, 20-day rolling average trading value) already locked and used for H-C3, and the same `daily_ic`/`ic_stats` (Spearman rank IC, Newey-West HAC t, 5 lags) and `bh_fdr` (Benjamini-Hochberg, α=0.10) functions from `research/rp001_phase2a_confirmatory_tests.py` — no new feature, no new data pull, no new tercile definition. BH-FDR is applied jointly across this addendum's own 18 tests, as a separate family from the locked 16 confirmatory tests (mixing locked and unlocked tests into one correction would itself be a protocol deviation).

**Inverse-probability weighting: not attempted.** IPW requires a reliable model of each stock's inclusion probability. The actual inclusion mechanism here is a hard data-availability gate (has an institutional-flow record at all, then ≥80% panel coverage) rather than a stochastic selection process with an estimable propensity score — fitting a propensity model on top of a deterministic gate would manufacture false precision, not add robustness. Left as a graduate-stage extension if a future study wants to model the >80%-coverage boundary itself.

## H-C1 (pre-break), by liquidity tercile

| Tercile | Horizon | n (days) | Mean IC | NW t | Raw p | BH-FDR q | Sig. q<0.10 |
|---|---|---|---|---|---|---|---|
| Illiquid | t+1 | 3,274 | +0.0105 | 5.963 | 2.5e-09 | 1.5e-08 | **Yes** |
| Illiquid | t+3 | 3,274 | +0.0067 | 3.049 | 0.0023 | 0.0059 | **Yes** |
| Illiquid | t+5 | 3,274 | +0.0045 | 1.948 | 0.051 | 0.103 | No (borderline) |
| Mid | t+1 | 3,274 | +0.0109 | 7.322 | 2.4e-13 | 2.2e-12 | **Yes** |
| Mid | t+3 | 3,274 | +0.0125 | 7.444 | 9.8e-14 | 1.8e-12 | **Yes** |
| Mid | t+5 | 3,274 | +0.0100 | 5.591 | 2.3e-08 | 1.0e-07 | **Yes** |
| Liquid | t+1 | 3,274 | **-0.0057** | **-3.812** | 1.4e-04 | 4.1e-04 | **Yes (negative)** |
| Liquid | t+3 | 3,274 | -0.0016 | -0.922 | 0.357 | 0.494 | No |
| Liquid | t+5 | 3,274 | -0.0005 | -0.269 | 0.788 | 0.834 | No |

**Finding:** H-C1's reported pre-break IC ≈ 0.00 at all horizons (the locked, full-sample average across all three terciles) is not a uniform null — it is an average of **offsetting, individually significant effects**: a robust positive relationship concentrated in Mid-liquidity names (significant at all 3 horizons, surviving FDR) and, more weakly, in Illiquid names (significant at t+1/t+3), against a **significant negative** relationship in Liquid names at t+1. This is directionally consistent with, and reinforces, H-C3's already-reported "Mid ≫ Illiquid > Liquid" pattern — H-C1 alone, tested unconditionally, could not see this because it averages across the full liquidity spectrum rather than conditioning on it.

## H-C2 (post-break, t+5), by liquidity tercile

| Tercile | n (days) | Mean IC | NW t | Raw p | BH-FDR q | Sig. q<0.10 |
|---|---|---|---|---|---|---|
| Illiquid | 197 | -0.0036 | -0.551 | 0.582 | 0.722 | No |
| Mid | 197 | -0.0008 | -0.112 | 0.911 | 0.911 | No |
| Liquid | 197 | +0.0075 | 1.330 | 0.184 | 0.300 | No |

**Finding:** unlike H-C1, H-C2's post-break null holds uniformly across all three liquidity terciles — no tercile is significant. This strengthens H-C2's null-vs-null verdict specifically for the post-break period: it is not masking an offsetting liquidity-conditional effect the way H-C1 was.

## H-C4's defining cells (Low-vol × break period, t+5), by liquidity tercile

| Cell | Tercile | n (days) | Mean IC | NW t | Raw p | BH-FDR q | Sig. q<0.10 |
|---|---|---|---|---|---|---|---|
| Low-vol & Pre-break | Illiquid | 1,692 | +0.0057 | 1.695 | 0.090 | 0.162 | No (borderline) |
| Low-vol & Pre-break | Mid | 1,692 | +0.0117 | 4.798 | 1.6e-06 | 5.8e-06 | **Yes** |
| Low-vol & Pre-break | Liquid | 1,692 | +0.0010 | 0.385 | 0.701 | 0.788 | No |
| Low-vol & Post-break | Illiquid | 46 | **-0.0308** | **-2.609** | 0.0091 | 0.020 | **Yes (negative)** |
| Low-vol & Post-break | Mid | 46 | -0.0159 | -1.251 | 0.211 | 0.316 | No |
| Low-vol & Post-break | Liquid | 46 | +0.0056 | 0.522 | 0.601 | 0.722 | No |

**Finding:** the locked H-C4 result (Low-vol & Pre-break not significant, t=0.789, full sample) is itself an average across liquidity groups — the Mid tercile alone *is* significant (t=4.80), consistent with H-C1's Mid-tercile finding above. The Low-vol & Post-break cell, thin at only 46 days, shows a significant negative IC concentrated in Illiquid names (t=-2.61) — a reversal, not a null, in that one slice. Given n=46 days for this cell, this is reported as a directional signal worth a larger post-break sample, not a robust standalone finding.

## What this changes, and what it does not

- **Does not overturn any locked H-C1–H-C5 verdict.** The full-sample average that determines each locked verdict is unchanged; this addendum decomposes *why* H-C1 in particular averages to near-zero.
- **Does change the interpretation of H-C1's "Not Replicated" verdict**, honestly stated: the pre-break effect is not simply absent — it is real and significant in Mid (and partly Illiquid) liquidity names, canceled in the full-sample average by a significant negative effect in Liquid names. A future study isolating liquidity-conditional cross-sectional prediction (rather than testing F_INST_01 unconditionally) would have a defensible starting point here, not from H-C1 as currently specified.
- **Reinforces, rather than contradicts, H-C3.** The two analyses are consistent: both find the effect (whatever direction) is liquidity-concentrated, strongest in Mid names.
- Per Deviation Policy discipline: this addendum was written and run *after* seeing the locked H-C1–H-C5 results (it directly responds to them), so it is explicitly **exploratory relative to this specific question**, not a second confirmatory test — its own significant findings above would need independent out-of-sample confirmation before being treated as confirmatory, exactly as H-C1–H-C5 themselves required relative to the original 50-stock exploratory study.
