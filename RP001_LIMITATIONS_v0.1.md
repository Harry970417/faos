# RP-001 Limitations v0.1

## Sample scope (the most important limitation)

50 stocks, taiwan-attention-signal's existing large-cap-weighted panel — not RP-001's designed full research universe (`RP001_RESEARCH_DESIGN.md` specifies full TWSE + TPEx, survivorship-bias-free). Every finding in this report is scoped to this sample and requires re-verification at full scale before being treated as final — this is the entire reason Phase 2A exists as a separate workstream rather than a formality.

## The break/regime/liquidity conditions were discovered in-sample

The structural break, the volatility-regime condition, and the liquidity condition were all found by analyzing the same 50-stock dataset they are reported as holding in. Internal robustness testing (permutation-corrected breakpoint tests, ±40-day sensitivity, two rolling windows, joint residualization) reduces but does not eliminate this concern — it is not equivalent to independent, out-of-sample confirmation. This is a research-design limitation, distinct from and in addition to any data-leakage risk (which was separately tested and ruled out at the construction level in Milestone 1B).

## Data-source limitations

FinMind's free tier reports institutional flow in shares, not NT$ value — value-denominated features are share-count proxies. Company-level Chinese-text fields required a workaround for a local terminal-display encoding issue (resolved, not a data problem — see Milestone 0A correction). Sector coverage in this sample is concentrated in 2 well-populated industries; sector-cut findings are not a broad cross-sector test.

## Statistical limitations

56-test multiple-testing inventory reflects tests actually run in this research program — a different set of researchers testing a different set of hypotheses on the same data could reach a different FDR-adjusted picture. Newey-West correction uses 5 lags throughout; not tested for sensitivity to lag choice. The Quandt-Andrews break test is a single-break specification — genuine multiple breaks were not tested (attempted via `ruptures`/Bai-Perron, unavailable in this environment).

## Causal limitations

No causal identification design (instrument, natural experiment, regression discontinuity, or similar) was used anywhere in RP-001. Every mechanism statement is observational and worded as "consistent with," never "demonstrates."

## Scope limitations — what RP-001 has never claimed

No investment performance, portfolio construction, transaction cost, or tradeability conclusion exists anywhere in this research program to date. No claim about live deployability. No claim about performance net of any implementation cost.
