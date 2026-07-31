# RP-001 Phase 2A.2-R: Institutional Category Historical Schema Audit

**Date:** 2026-07-31. **Sample:** all 86 stocks with a cached, successful `TaiwanStockInstitutionalInvestorsBuySell` pull from Batch 1 (85 of these also have complete Price+PER data; see `RP001_PHASE2A_BATCH_TRACKER.md`). No new API requests were made for this audit — entirely reuses Batch-1 cached raw JSON. Script: `rp001_institutional_schema_audit.py`; outputs in `rp001_data/phase2a/audits/`.

This supersedes the single-stock (1101-only) conclusion in `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` and directly investigates escalated Deviation **D-04**.

## 1. Category names observed (full sample)

Exactly six distinct `name` values across 1,176,356 rows: `Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer`, `Dealer_self`, `Dealer_Hedging`. No unexpected or malformed category strings, no whitespace/casing variants, no new categories beyond what Phase 2A.1 already catalogued.

## 2. Dealer occurrence — which stocks, which dates

85 of 86 stocks (98.8%) carry at least one undifferentiated `Dealer` row. **All of it is pre-cutover**, with one exception:

- **Pre-cutover (before 2014-12-01):** all 85 stocks, date ranges falling inside 2012-05-02 to 2014-11-28 — consistent with the originally-documented cutover.
- **Post-cutover (on/after 2014-12-01), full history through 2026-07:** only **1 of 86 stocks** — **stock 1342**, 15 rows, 2019-12-17 to 2020-10-26. This matches the specific case that triggered Batch 1's STOP; it is not a new finding, it is now confirmed as the *only* instance across the full 86-stock sample rather than an unexplained one-off.

**Methodology correction (caught before publication, not after):** a first-pass block-detection script flagged 85/86 stocks as "recurrence" by counting any >10-calendar-day gap between consecutive `Dealer` dates as a new "block," without checking whether the gap crossed the 2014-12-01 cutover line. Nearly all of these gaps are internal sparsity *within* the single pre-cutover era (Dealer wasn't reported on 100% of pre-cutover trading days for any stock — plausible index-inclusion/thin-trading effects, not examined further as immaterial). Re-run filtering strictly on `date >= CUTOVER` gives the correct, much narrower result above. This is flagged explicitly, not silently fixed, per the standing correction-note requirement.

## 3. Does Dealer/Dealer_self/Dealer_Hedging overlap on the same date?

**No. Zero same-day overlap, for all 85 stocks with any Dealer row.** On every date in the sample, a stock reports either the undifferentiated `Dealer` category or the split `Dealer_self`/`Dealer_Hedging` pair, never both. This is real, checked evidence (`dealer_split_overlap.csv`), not an assumption — the categories are mutually exclusive per stock-date in this sample.

## 4. Cutover, recurrence, or schema type?

- **Not a universal clean one-time cutover** — Phase 2A.1's conclusion (based on stock 1101 alone) is **revised, not retracted outright**: the cutover pattern *does* hold for 84 of 86 stocks with no exception found. It is **stock-specific recurrence, rare and isolated** — one stock (1342) out of 86 (1.16%) shows a Dealer window five years after the general cutover. No evidence of a *market-specific* schema (TWSE vs TPEx split not tested directly here since Batch 1's 85-86 stocks are overwhelmingly low-numbered TWSE codes — flagged as a full-universe-scale open question, see §7) or *endpoint-specific* schema (only one endpoint used).
- **Most decision-relevant finding: does Dealer recur inside the locked 2025 break-interval window (2025-08-01 to 2025-10-31, padded a few days each side of the point estimate 2025-09-25) for any of the 86 sampled stocks?** **Zero.** `break_window_schema_state.csv` confirms 0/86 stocks show a `Dealer` row anywhere in that window; all 86 report cleanly via `Dealer_self`/`Dealer_Hedging` (or their stock had no institutional trading that window, distinct from a schema issue) throughout the confirmatory test period. This is real, batch-scale evidence directly bearing on D-04, not a single-stock inference.

## 5. Foreign_Investor: drift, missingness, or definition change?

- **No name drift.** Only one canonical string, `Foreign_Investor`, ever observed — no variant spelling, no capitalization change.
- **No missingness.** All 86 sampled stocks have at least one `Foreign_Investor` row (`missing_fi` list is empty).
- **No definition change detected** in this sample — a drift would show up as a discontinuity in `Foreign_Investor`'s presence/coverage rate around some date; not observed. A full statistical continuity check (row-count-per-trading-day over time) is deferred to the missingness audit (`RP001_INSTITUTIONAL_MISSINGNESS_AUDIT.md`), which covers this more rigorously per stock.

**Per your explicit instruction: F_INST_01 uses only `Foreign_Investor`, and its constructibility is judged on `Foreign_Investor`'s own evidence (§5), not inferred from the unrelated Dealer-category finding.** On the 86-stock sample, `Foreign_Investor` shows no schema problem of any kind.

## 6. 2025 break-interval schema change (any category)

Checked: category set present in every stock's break-window slice. All 86 stocks show only categories from the expected post-cutover set (`Foreign_Investor`, `Foreign_Dealer_Self`, `Investment_Trust`, `Dealer_self`, `Dealer_Hedging`) during the break window — no category-set change coincident with the break, in this sample.

## 7. Old `Dealer` field — handling rule

For the 85 stocks with pre-cutover `Dealer` rows (all before 2014-12-01, entirely outside any confirmatory hypothesis's data window, since the earliest hypothesis-relevant period is defined by the locked break interval in 2025):

- **Keep the raw value**, unmapped — do not attempt to split `Dealer` into `Dealer_self`/`Dealer_Hedging` retroactively; no deterministic mapping rule exists in the source data to do so.
- **Cannot be used standalone** for any Frozen/Confirmatory feature that specifies `Dealer_self`/`Dealer_Hedging` individually (none of H-C1–H-C5 do, per §8).
- **Usable only inside an aggregate** if a future feature needs "all dealer activity regardless of split," by summing `Dealer` OR (`Dealer_self` + `Dealer_Hedging`) depending on which is present that date — not needed by any currently-locked feature.
- **Research periods affected:** 2012-05-02 to 2014-11-28 for the 85-stock pre-cutover era (irrelevant to Phase 2A confirmatory tests, which only touch the 2025 break interval and its surrounding sample window); 2019-12-17 to 2020-10-26 for stock 1342 specifically (also outside the locked break interval).

## 8. Feature Impact Matrix

See `RP001_FEATURE_IMPACT_MATRIX.md` for the full table. Summary: **F_INST_01 is Unaffected** by every finding in this audit, on the 86-stock sample — it depends only on `Foreign_Investor` (§5, clean) and never touches `Dealer`/`Dealer_self`/`Dealer_Hedging`.

## 9. A documentation error found, not a spec contradiction — D-04's escalation basis was imprecise

Direct read of the actual locked registry, `FEATURE_REGISTRY.md` line 11: *"F_INST_01_foreign | Foreign_Investor net flow (shares) | `buy − sell`, Foreign_Investor category only."* `Dealer_self` and `Dealer_Hedging` are the defining inputs of **F_INST_03_dealer_self** and **F_INST_04_dealer_hedge** (registry lines 13-14) — two separate, already-`Inconclusive`/`Rejected` features, not F_INST_01, and not referenced by any of H-C1–H-C5 (checked against `RP001_CONFIRMATORY_HYPOTHESES.md`, which names only F_INST_01).

`RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` (Phase 2A.1) contains a factual error: its Item-7 discussion states *"F_INST_01's locked definition uses `Dealer_self` and `Dealer_Hedging` as separate inputs, which is exactly what exists throughout the entire confirmatory test window."* This conflates F_INST_01 with F_INST_03/F_INST_04. Escalated Deviation **D-04** (`RP001_PHASE2A_DEVIATION_LOG.md`) inherited this error, escalating on the grounds that Dealer-category drift "could affect F_INST_01's constructibility directly" — it cannot, since F_INST_01 never reads the Dealer categories at all.

**This is a real correction to a prior document, not a new ambiguity to defer to you** — it does not touch the locked specification itself (F_INST_01's actual definition is unchanged and was never in question), so it does not require Deviation Policy escalation to fix. A correction note (preserving the original text) has been added directly to `RP001_FULL_UNIVERSE_AVAILABILITY_AUDIT.md` and to D-04's entry in the Deviation Log — see `RP001_PHASE2A1_REAUDIT.md` for the full re-audit entry. **Net effect: D-04's true remaining concern is narrower than originally escalated** — whether Dealer-category recurrence could ever contaminate a *Dealer-based* feature (F_INST_03/F_INST_04, both already non-Frozen) during the test window, not F_INST_01. §6 above already shows zero Dealer recurrence in the break window across the 86-stock sample regardless.
