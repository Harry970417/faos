# EVIDENCE_PILOT_v0.2.md

Same 20 objects as v0.1, no sample expansion, no swapping out hard cases. 8 of the 14 originally-failing objects got genuine re-verification via real web search this round (T01, T05, M02, FA01, ME01, ME07, C01, C08); 6 (T02, T03, T06, T09, M01, FA03) were **not** re-attempted and honestly remain Fail — not because the bar was too high, but because search effort ran out, and that distinction matters (see ECC_VALIDATION_REPORT_v0.1.md item 8).

## Integrity method — real, this time

Every new citation was located via WebSearch and, where possible, confirmed via WebFetch — not asserted from memory. Where I could confirm volume/issue/pages/DOI, they're recorded (marked `[WEB-VERIFIED]`). Where I could not (e.g. Qian/Hua/Sorensen's exact edition year), it's marked **Locator Pending**, not guessed. One source (Cline 2015, Peterson Institute working paper) is real and independently authored but not peer-reviewed — flagged Quality: Medium rather than folded silently into "High." Full citation-by-citation detail, including independence and stance (supports/limits/contests/background) for every one of the 33 evidence entries, is in `evidence_pilot_v0.2.psv`.

## Verdicts — Pass, Partial, Fail, honestly distributed

| Verdict | Objects |
|---|---|
| **Pass (13)** | T01, T05, M02, FA01, ME01, C01, C08, PR02, S01, S03, A01, F01, FR01 |
| **Partial (1)** | ME07 — structurally meets count/independence, but one source's publication year is unconfirmed |
| **Fail (6)** | T02, T03, T06, T09, M01, FA03 — all fail on count alone (still at 1–2 sources against a Min of 3), not on quality of what exists |

No object was force-passed. T05's pass rests partly on a non-peer-reviewed working paper — flagged explicitly as a calibration question in the Validation Report, not hidden.

## Before / After Dashboard (vs. v0.1, v0.1 file untouched as fixed baseline)

| Metric | v0.1 | v0.2 |
|---|---|---|
| Pilot Coverage | 20/20 (100%) | 20/20 (100%) — unchanged, scope wasn't expanded |
| ECC Completeness (Pass) | 6/20 (30%) | 13/20 (65%) |
| ECC Completeness (Pass+Partial) | 6/20 (30%) | 14/20 (70%) |
| Total Evidence Objects | 28 | 33 |
| Average Evidence per Object | 1.60 | 2.05 |
| Primary Source Ratio | 78.6% | 72.7% |
| Secondary Source Ratio | 21.4% | 27.3% |
| Independent-source-marked entries | not tracked in v0.1 | 13/33 (39%) |
| Single-Sourced Object Count | 9 | 7 (S01, A01, T03, T09, FR01, T06, S03 — each legitimately, per type rules or un-attempted Theories) |
| Contested Objects with Opposing Evidence | 0 | 1 (T01 — Fama-French 1992 vs. CAPM) |
| Locator-Verified Ratio | 0/28 (0%) | 6/33 (18%) — the rest carried forward from v0.1 as Locator Pending, not newly fabricated |
| Full-KB Completeness | 20/299 (6.7%)* | 20/299 (6.7%) — Coverage unchanged by design; Completeness (Pass) is the metric that moved |

\* v0.1's dashboard reported this as plain "Coverage"; distinguishing it from ECC Completeness is itself new in v0.2.

## Cost and scalability (Section 6)

- **New evidence per touched object:** 0–2 new citations added per re-verified object; several passes came from *recognizing reuse* (Bodie/Kane/Marcus already covered CAPM, extended to Sharpe Ratio and Risk at zero new search cost) rather than new sourcing — reuse is a real cost lever, not just a tidiness property.
- **Verification steps:** ~11 real tool calls (9 searches + 2 fetches) across 8 objects, ≈1.4 per object, though unevenly distributed — Theory-tier objects needed multi-step searches (find candidate → confirm authorship/venue via fetch), while reused Secondary sources needed zero additional steps.
- **Hardest type: Theory.** Every Theory that passed needed a genuinely independent second source *and*, where contested, a specifically critical one — this is real research work, not lookup. The four Theories that stayed Fail (T02, T03, T06, T09) are exactly the ones I didn't have bandwidth to search this round, which is itself the clearest signal of where cost concentrates.
- **Reuse rate:** 7 of 33 evidence entries (21%) ground more than one Knowledge Object.
- **Scalability flag:** the full Knowledge Base has 25 Theory + 12 Factor objects (37 total) that would need this same strict treatment. At this pilot's real rate (~1–2 search operations per object, several needing a dedicated independent-replication or contested-source search), fully sourcing just those 37 objects at Research Grade implies on the order of 60–100 real search/verification operations — a substantial, genuinely manual research effort. **This is the actual cost ECC's strictness carries at scale, and it's a legitimate input to whether v1.0 Freeze makes sense now versus after building some kind of verification tooling.**

## Formal recommendation (not self-decided — awaiting your approval)

Checking against your five Freeze conditions:

| Condition | Met? |
|---|---|
| Representative testing across Knowledge Types | **Partial** — Theory, Model, Factor, Metric, Concept, Procedure, Standard, Assumption, Formula, Framework all appeared; Pattern was never tested (deliberately excluded from the pilot both times) |
| ECC-Pass shows clear positive difference in answer quality | **Yes** — Research Answer Comparison shows every Pass-anchored answer could disclose a limitation or opposing view using only its own cited evidence; every Fail-anchored answer could not, even where partial independent evidence existed |
| No Type systematically mis-judged | **Mostly yes** — but Standard's Currency Check and Pattern's Provisional waiver were never actually exercised, so "not mis-judged" is unproven for those two, not confirmed correct |
| Standard executable at reasonable cost | **Open question, not yet answered** — cost is real and concentrated in Theory/Factor; whether it's "reasonable" at 37-object scale hasn't been tested against an actual time/effort budget |
| All modifications supported by Pilot evidence | Yes — the two calibration issues found (peer-review distinction, Currency Check untested) are both traceable to specific pilot findings, not asserted |

**My recommendation: ECC v0.2 revision, not v1.0 Freeze, not v0.1 retention.**

Retention (keep v0.1 as-is) would ignore two real, evidence-based findings (the peer-review gray area, the untested Currency Check). Freezing to v1.0 now would lock in two rules that were never actually exercised (Standard, Pattern) and one unresolved calibration question (Theory-tier peer-review status) — exactly what your Freeze conditions are designed to prevent. A small, targeted v0.2 revision — clarify Primary's peer-review expectation for Theory, and run a dedicated (even if small) test of the Currency Check and the Pattern waiver — would close all three gaps with evidence, not assertion, before Freeze becomes justified.
