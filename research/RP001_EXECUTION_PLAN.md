# RP-001 Execution Plan

Not started. Sequenced for after Research Design approval.

## Phase 0 — Infrastructure verification (before any data pull)
1. Confirm FinMind institutional-data publication timing empirically (not assumed) — pull a small sample, check actual timestamp vs. t+1 market open.
2. Fork taiwan-attention-signal's data layer; adapt `fetch_institutional_breakdown.py` from the 50-stock panel to the full exclusion-rule-based universe.
3. Verify the survivorship-bias-free universe construction actually executes as designed (see Risk Register — this is the step most likely to silently fail).

## Phase 1 — Universe and panel construction
4. Build the full TWSE/TPEx daily panel with exclusion rules applied and frozen.
5. Calibrate the liquidity threshold on Train-period data only; freeze before touching Validation/Test.

## Phase 2 — Factor construction
6. Build the 9 candidate institutional-flow factors + interaction terms.
7. Create the corresponding Knowledge Objects (Institutional Flow Factor family) in the Knowledge Base — this is where Research Production Finding #1 gets resolved, driven by actual need, not speculative pre-design.

## Phase 3 — Methodology extension
8. Adapt `ic_analysis.py` and `v03_fama_macbeth.py` from weekly to daily frequency.
9. Implement Newey-West correction — create the corresponding Method/Formula object (resolving Finding #2), grounded on the already-verified Newey-West (1987) citation from the Evidence Map.

## Phase 4 — Estimation (Train/Validation only)
10. Run IC, ICIR, Fama-MacBeth on Train; calibrate on Validation. No Test-set access yet.

## Phase 5 — Robustness (still pre-Test)
11. Run all Robustness cuts (period, size, industry, market regime, outlier handling, standardization method) on Train/Validation only.

## Phase 6 — Single Test-set run
12. One, and only one, formal Test-period evaluation, with multiple-testing correction applied to all 9+ candidates simultaneously — no re-running after seeing results.

## Phase 7 — Reporting
13. Compile findings into a formal research output (thesis-extension / portfolio format per your original request), explicitly reporting whichever of H0/H1a/H1b/H2/H3/H4 the evidence actually supports — including a null or negative result, stated as plainly as a positive one would be.

Each phase gate requires your review before proceeding to the next — this plan does not authorize autonomous execution through all seven phases.
