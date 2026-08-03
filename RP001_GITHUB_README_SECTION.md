# RP-001 — Standalone README Section

Drop-in section for a personal portfolio repo/site README, extracted from this repo's `README.md`. Self-contained — does not assume the reader has any other FAOS context.

---

## RP-001: Does Foreign Institutional Flow Predict Taiwan Stock Returns?

**Status: Completed** — a full pre-registered confirmatory validation cycle, from a promising 50-stock exploratory finding to a full-market, 14-year independent re-test.

**Research question:** Does foreign institutional net flow predict short-horizon cross-sectional returns in Taiwan equities?

**Design:** Exploratory phase (50 stocks, free hypothesis search) → Protocol Lock (factor definition, statistical methods, and five hypotheses fixed and hashed *before* touching full-market data) → full-universe confirmatory test (2,255 stocks, 2012–2026, independently constructed).

**Scale:** 6,765 API requests, 100% resolved, 34.2M raw rows, 21/21 unit and data-leakage tests passed on the final dataset.

**Result:** Of five pre-registered hypotheses, three did not replicate (including the central pre-break predictive claim), one partially replicated, one replicated but with weak evidentiary value. A separate, unexpected finding — small but statistically robust residual effects in interaction terms previously judged artifacts — is disclosed and explicitly reserved for an independent follow-up study, not pursued further here.

**What this demonstrates:** end-to-end data engineering (rate-limited API acquisition, two real pipeline bugs found and fixed, systematic data-quality auditing across 69 individually-verified schema-drift cases), rigorous statistical inference (Newey-West, cross-sectional residualization, Benjamini-Hochberg FDR), and — the part most student projects skip — reporting a negative result for the central hypothesis honestly, without adjusting methodology after seeing it.

**Full writeup:** `research/RP001_FINAL_RESEARCH_REPORT.md` · **One page:** `portfolio/RP001_PORTFOLIO_ONE_PAGE.md` · **Reproduce it:** `research/RP001_PHASE2A_REPRODUCIBILITY_REPORT.md`

*(Paths above are relative to the FAOS repo root — adjust if you copy this section into a different repo.)*
