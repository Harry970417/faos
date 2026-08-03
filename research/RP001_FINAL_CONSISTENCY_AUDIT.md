# RP-001 Final Consistency Audit

**Date:** 2026-08-03. Scope: every file added or modified during the post-closure portfolio/documentation phase (audit, core reports, application materials, interview prep, GitHub docs, charts, FAOS case study, RP-002 brief), cross-checked against the already-closed RP-001 research record. Performed as direct grep/read against the repo, not from memory.

## Method

Grepped every specified term across all `.md` files: `RP-001`, `F_INST_01`, `Frozen — Conditional`, `confirmed factor`, `stable signal`, `alpha`, `outperform`, `predictive`, `significant`, `replicated`, `H-C1`–`H-C5`, `50 stocks`, `2,255 stocks`, `1,462 stocks`, `5,718,238`, `3,934,274`.

## Findings

1. **Numeric consistency:** `2,255`, `1,462`, `5,718,238`, `3,934,274` appear identically across every document that cites them, including all newly-added application, summary, and portfolio documents. No discrepancy found.

2. **Status consistency:** No document states or implies H-C1, H-C4, or H-C5 replicated. Every mention of H-C2 that appears outside `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md` itself is either silent on the caveat (acceptable — a one-line application document isn't required to restate it) or explicitly includes "weak"/"caveat"/"未複現" context. No document claims a clean five-for-five or even a clean majority replication.

3. **"confirmed factor" / "stable signal":** zero matches anywhere in the repository.

4. **"alpha" as an investment claim:** zero matches outside `FAOS_ALPHA_0.x` version naming. Every prose use of "alpha" in the new documents is in the fixed sentence "不宣稱找到穩定的 Alpha" / "does not claim to have found a stable alpha" — a negation, not a claim.

5. **"outperform":** one match, in `research/RP001_FEATURE_SPECIFICATION.md` (exploratory-phase, Milestone 0C), referring to comparing functional forms for an interaction term — not a performance claim, and the document is historical record, not a current-status document.

6. **Profitability/investment-advice framing:** zero matches for 投資建議, 建議買進/賣出, 穩賺, 保證 anywhere. The one match for 獲利 (`applications/RP001_APPLICATION_NTU_FINANCE.md`) is inside a "what not to emphasize" warning, explicitly telling the reader not to frame the research this way.

7. **Exploratory vs. confirmatory conflation:** checked every new document (applications, interview QA bank, paragraph banks) for exploratory-phase numbers (0.052, 0.069, 3.99, "50 stocks") presented without confirmatory context. None found — every exploratory figure that appears in the new documents is in an explicit before/after or exploratory/confirmatory comparison framing.

8. **Statistical-significance-as-tradeable conflation:** the interview QA bank (`interview/RP001_INTERVIEW_QA_BANK.md`) questions 12 and 20 directly test this distinction and answer it correctly (FDR survival ≠ mechanism validity; statistical significance ≠ backtest-worthy). No document elsewhere asserts the reverse.

9. **Placeholder/incomplete content:** grepped for TODO/PLACEHOLDER/FIXME/XXX/lorem ipsum across all ~35 newly-added files. Zero matches.

10. **Application-document differentiation:** read all five `RP001_APPLICATION_*.md` files side by side — each has a genuinely distinct positioning (research rigor / market-institution knowledge / fintech-data-engineering / systems-and-reproducibility / decision-governance), distinct "what not to emphasize" guidance, and distinct likely follow-up questions. None is a template with only the school name changed.

## Correction Log

**No corrections were required.** Every check above found the new documentation set consistent with the already-closed, non-rescindable research record.
