# RP-001 Research Report v0.2

**Status: RP-001 — Confirmatory validation (Phase 2A) complete. Formal conclusion updated.** This report supersedes v0.1's "nothing confirmed yet" status. Phase 2A ran all five pre-registered confirmatory hypotheses on the full TWSE+TPEx universe (2,255 stocks, 2012–2026), independent of the 50-stock exploratory sample. v0.1's findings are preserved below exactly as originally written, not rewritten — the new Confirmatory section states plainly which of them did and did not survive.

## Formal Core Conclusion (v0.2, FIXED WORDING — final, not to be paraphrased)

> 本研究在 50 檔探索樣本中觀察到外資買賣超的條件式預測能力，但該結果未能在完整 TWSE 與 TPEx 股票池中複現。低波動機制亦未獲支持，流動性條件僅部分複現。部分交互作用項在完整樣本中出現小量級殘差效果，但屬確認性樣本中的意外發現，必須由新的預註冊研究獨立驗證。整體證據不支持將外資買賣超視為穩定、普遍或可直接交易的無條件因子。

**English restatement, for reference only — the Chinese text above is the fixed, authoritative wording:** Foreign investor net flow's exploratory-phase predictive relationship with cross-sectional Taiwan stock returns — discovered on a 50-stock, ~2-year sample — does not replicate on the full survivorship-bias-free universe and full available history (2012–2026). The low-volatility mechanism is likewise unsupported; liquidity conditionality only partially replicates. A small-magnitude residual effect appears in some interaction terms on the full sample, but this is an unexpected confirmatory-phase finding requiring independent, separately pre-registered validation — not a basis for further work under RP-001. Overall, the evidence does not support treating foreign net flow as a stable, universal, or directly tradeable unconditional factor.

## v0.1's original formal conclusion (preserved verbatim, not deleted)

> Foreign investor net flow showed conditional predictive power for Taiwan cross-sectional stock returns, concentrated before the identified break interval and among illiquid-to-mid-liquidity stocks. The effect disappeared after the break and was not shown to be causal. None of the seven interaction terms provided genuine incremental information after controlling for their constituent main effects.

## Findings by evidentiary category (v0.2)

**Confirmatory — no longer empty, per the whole purpose of Phase 2A:**
- H-C1 (pre-break positive IC): **Not Replicated**
- H-C2 (post-break null): **Replicated** (weak evidentiary value given H-C1's failure — see `RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`)
- H-C3 (liquidity conditionality): **Partially Replicated**
- H-C4 (volatility break-conditionality): **Not Replicated**
- H-C5 (no genuine interactions): **Not Replicated** — new positive finding of small, statistically robust residual interaction effects at full-universe scale, opposite of the exploratory-phase expectation

**Exploratory** (v0.1's original hypothesis-generating findings, preserved as historical record — see v0.1's own text above): the discovery of the foreign-flow signal, its apparent liquidity/volatility conditionality, and the interaction-feature "artifact" conclusion. **These are now known to have not survived confirmatory testing at full scale for three of the five specific claims tested (H-C1, H-C4, H-C5), and to have partially survived for one (H-C3).**

**Robustness-tested (exploratory scale only, unchanged from v0.1):** the structural break survived permutation-corrected unknown-breakpoint testing on the 50-stock sample. This robustness was internal to the exploratory sample and is exactly the thing Phase 2A was designed to test independently — it is superseded in evidentiary weight by the confirmatory result, not contradicted in kind (internal robustness and external replication are different questions, and this study now has an answer to both).

**Negative findings (from v0.1, unchanged):** F_INST_02 (Trust), F_INST_04 (Dealer Hedging), F_INST_09 (change rate) — no evidence of predictive power at any tested horizon, at exploratory scale (not re-tested at full-universe scale — outside Phase 2A's five locked hypotheses).

**Confirmed artifacts (from v0.1, status changed for the interaction features by H-C5):** F_INST_06 remains redundant with F_INST_05 (unchanged, not re-tested). The seven interaction features' "Confirmed Artifact" status from Milestone 1D is **now partially superseded** — F_INT_01, F_INT_03, F_INT_04, and F_INT_07 show a statistically significant (though economically small) residual effect at full-universe scale that did not appear on the 50-stock sample. F_INT_02/F_INT_06 remain untested (Deviation D-08). F_INT_05 remains a borderline/inconclusive case (NW t=1.99, just misses BH-FDR).

## What this report does not claim

No portfolio, backtest, Sharpe ratio, drawdown, transaction-cost, or investment-performance conclusion appears anywhere in RP-001. No causal claim is made about foreign flow's information content. The full-universe confirmatory results do not establish that F_INST_01 or the interaction features are "false" in any absolute sense — they establish that the specific, quantified relationships found in the exploratory sample do not reproduce at the scale and specification pre-registered for testing them.

Detail: `RP001_METHODS_AND_DATA_v0.2.md`, `RP001_RESULTS_TABLES_v0.2.md`, `RP001_LIMITATIONS_v0.2.md`, `RP001_REPRODUCIBILITY_APPENDIX_v0.2.md`, `RP001_PHASE2A_CONFIRMATORY_RESULTS.md`, `RP001_PHASE2A_HYPOTHESIS_VERDICTS.md`.
