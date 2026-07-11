# RP-001 Data Requirements

## Institutional trading data

**Source: FinMind, `TaiwanStockInstitutionalInvestorsBuySell`** — confirmed real, open, documented, covers both TWSE and TPEx (see Evidence Map). **Confirmed limitation, verified two independent ways** (FinMind's own documentation pattern and taiwan-attention-signal's existing code comments): the free tier reports **shares bought/sold, not NT$ value**. Any "buy/sell amount" factor in this design is therefore a share-count-based proxy, not a true monetary figure, and must be labeled as such in every output — this is not a cosmetic caveat, it directly affects the "買賣超金額標準化" factor's validity.

**Registered-token tier** raises the rate limit to 600 requests/hour — needed at full-universe scale (likely 1,500+ tickers × multi-year daily data), a free/unregistered pull would be impractically slow or rate-limited.

## Price and return data

Daily OHLC, adjusted for corporate actions (splits, dividends, capital changes) — required for accurate close-to-close and open-to-close return calculation. Source not yet finalized between FinMind's own price dataset and TWSE/TPEx official OpenAPI — a real decision for the Execution Plan, not resolved here.

## Universe construction data

Listing/delisting dates (for survivorship-bias-free universe construction), 全額交割/處置股 status history (for exclusion), industry classification (for the industry-robustness cut), market cap history (for the size-robustness cut and size-effect hypothesis H3).

## Reuse assessment — direct answer to your question

**taiwan-attention-signal has substantially the right infrastructure already**, not taiwan-stock-analyzer or stock-ai-project:

- `fetch_institutional_breakdown.py` — already fetches exactly this FinMind dataset, with the shares-not-value limitation already documented in its own code comments (a second, independent confirmation of the Data Requirements finding above).
- `ic_analysis.py`, `v03_fama_macbeth.py` — working IC and Fama-MacBeth implementations, methodologically sound (the codebase's own comments show it already handles degenerate model specifications honestly, e.g. its Model 5 fix).

**What needs adaptation, not rebuilding:**
1. **Frequency mismatch** — existing code is weekly (`attention_weekly_panel`); RP-001 needs daily (next-day prediction target). The IC/Fama-MacBeth *logic* transfers; the panel construction does not, as-is.
2. **Universe mismatch** — existing config (`stock_list_50.csv`) is a 50-stock panel; RP-001 needs the full TWSE/TPEx universe with the exclusion criteria in Section 1 of the Research Design.
3. **Date range** — existing fetcher starts 2021-01-01; RP-001's proposed period (2015–2026) needs an earlier start, subject to data availability.

**Recommendation:** fork/extend taiwan-attention-signal's data and methodology layer rather than building new pipeline code from scratch in stock-ai-project or taiwan-stock-analyzer — this is a real, code-level reuse opportunity, not a generic "yes you can reuse things" answer.
