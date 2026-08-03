# RP-001 Research Findings v0.2 — Final, Post-Closure

**RP-001 Status: Completed.** Supersedes `archive/RP001_RESEARCH_FINDINGS_v0.1.md` (preserved unchanged as the exploratory-phase historical record — its findings are not deleted, only re-classified below by what confirmatory testing did or did not support). No investment performance claim appears anywhere in this document.

## Exploratory Findings (50-stock sample, 2024-07 to 2026-07 — hypothesis-generating only, never independently confirmed on their own)

1. Foreign institutional net flow (F_INST_01) appeared to have conditional predictive power for 2-to-5-day-ahead cross-sectional returns.
2. A structural break in that apparent predictive power was detected via a permutation-corrected unknown-breakpoint test, located in a break interval of roughly late-August to late-October 2025.
3. The apparent signal was stronger in illiquid-to-mid-liquidity names and in low-volatility regimes, with the volatility effect itself conditional on the pre-break period.
4. All seven tested interaction features (momentum, size, liquidity, volatility, in both aggregate- and foreign-based forms) appeared to be fully explained by their constituent main effects (Confirmed Artifact) on this sample.
5. IC strengthened with return horizon rather than decaying; market-cap and value/growth cuts showed non-monotonic (middle-strongest) patterns, unexplained.

## Confirmatory Findings (full TWSE+TPEx universe, 2012–2026, 1,462-stock coverage-gate-passing sample — the actual pre-registered test)

1. **F_INST_01's pre-break predictive power does not replicate** — mean IC statistically indistinguishable from zero at t+1, t+3, and t+5 (H-C1).
2. **The volatility-regime break-conditionality mechanism does not replicate** — the defining Low-vol & Pre-break cell is itself not significant at full-universe scale, leaving nothing for the break-conditionality claim to explain (H-C4).
3. **Liquidity conditionality partially replicates** — direction correct (Illiquid, Mid both exceed Liquid; Liquid null), but asymmetric: only the Mid tercile independently reaches significance (H-C3).
4. **Post-break IC is null** — technically satisfies H-C2's Replicated criterion, but this comparison carries little evidentiary weight once H-C1 itself found no significant pre-break effect to contrast it against.
5. **Four of five testable interaction features show a small but statistically robust residual effect** surviving joint residualization and BH-FDR correction (H-C5 Not Replicated, in the opposite direction from the exploratory expectation) — see Unexpected Findings below.

## Not Replicated Findings

- **H-C1** (pre-break positive IC): Not Replicated.
- **H-C4** (volatility effect is break-conditional): Not Replicated.
- **H-C5** (no genuine interaction effects): Not Replicated — see Unexpected Findings.

## Partially Replicated Findings

- **H-C3** (liquidity conditionality): Partially Replicated — correct direction, incomplete significance pattern.
- **H-C2** (post-break null): Replicated by the letter of the pre-registered criterion, but flagged here as evidentially weak given H-C1's failure — not treated as a clean confirmatory success.

## Unexpected Findings

**Four interaction features previously characterized as fully-explained additive artifacts (F_INT_01, F_INT_03, F_INT_04, F_INT_07) show a residual IC that survives joint cross-sectional residualization against both constituents and Benjamini-Hochberg FDR correction (q<0.10) at full-universe scale.** Magnitude is small — 75–95% smaller than each feature's own raw IC, and an order of magnitude smaller than the exploratory-phase raw interaction ICs. This finding was not sought, was not part of any pre-registered expectation, and is reported in full rather than minimized. **It does not license any new investigation under RP-001** — per the Deviation Policy and this closure's own governance, an incidental confirmatory-phase finding is not grounds for ad hoc follow-up analysis; it requires its own independently pre-registered study.

## Confirmed Negative Findings (exploratory scale, unchanged, not re-tested at full-universe scale)

F_INST_02 (Trust), F_INST_04 (Dealer Hedging), and F_INST_09 (change rate) — no evidence of predictive power at any tested horizon. F_INST_06 — confirmed redundant with F_INST_05. H3 (small-cap concentration hypothesis) — not supported, market-cap pattern was non-monotonic.

## Data and Protocol Limitations

- Market-cap and sector classification data were unavailable at full-universe scale (Deviation D-08) — F_INT_02 and F_INT_06 were never confirmatory-tested; sector-neutral and value/growth robustness cuts could not be repeated.
- Only 1,462 of 2,096 stocks with panel presence (69.8%) passed the pre-committed 80% institutional-data-coverage gate and entered H-C1–H-C4; this threshold was fixed before computation, not tuned to the result.
- The unexpected H-C5 residual-effect finding has no established causal or mechanical explanation — whether it reflects a genuine full-universe-scale phenomenon or is an artifact of vastly greater statistical power than the exploratory sample is not determined here.
- No causal identification design was used anywhere in RP-001, exploratory or confirmatory. No portfolio, backtest, Sharpe, drawdown, or transaction-cost claim exists anywhere in this research program.

## Formal Core Conclusion (fixed wording, final)

> 本研究在 50 檔探索樣本中觀察到外資買賣超的條件式預測能力，但該結果未能在完整 TWSE 與 TPEx 股票池中複現。低波動機制亦未獲支持，流動性條件僅部分複現。部分交互作用項在完整樣本中出現小量級殘差效果，但屬確認性樣本中的意外發現，必須由新的預註冊研究獨立驗證。整體證據不支持將外資買賣超視為穩定、普遍或可直接交易的無條件因子。
