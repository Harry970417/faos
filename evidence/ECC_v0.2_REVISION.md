# ECC_v0.2_REVISION.md

Scoped to exactly the three gaps found in ECC_VALIDATION_REPORT_v0.1.md. No other rule touched.

## 1. Theory Primary Source — peer-review clarified

**Finding that motivated this:** T05's pass relied partly on Cline (2015), a real, independently-authored, but non-peer-reviewed Peterson Institute working paper.

**Revised rule:** At least one Primary source for a Theory must be peer-reviewed (a journal article or equivalent formal academic publication) — this cannot be waived. Additional Primary or corroborating sources *may* be non-peer-reviewed if from a named, reputable institution (central bank, recognized research institute, NBER-class working paper series), but must be tagged **Quality: Medium**, not High, and cannot by themselves satisfy the independence requirement in place of a peer-reviewed source.

**Retroactive check against T05:** still Pass — Modigliani & Miller (1958, 1963) are both peer-reviewed (American Economic Review), so the mandatory peer-reviewed anchor is satisfied; Cline (2015) correctly sits as a Medium-quality supplementary source, exactly as it was already tagged. No object's verdict changes; the rule that was previously implicit is now explicit.

## 2. Standard Currency Check — operationalized

**Finding that motivated this:** the rule existed on paper but was never exercised — both passing Standards (S01, S03) succeeded on citation presence alone.

**Revised rule, three concrete steps:**
1. Identify the issuing body's current effective edition/version of the Standard.
2. Confirm the cited Evidence object references that current version, not a superseded one.
3. **Check for known, imminent superseding changes** (not just "is today's citation valid today") — a Standard undergoing active revision should be flagged even if the currently-cited version is technically still in force.

Step 3 is new relative to the original rule text, which only asked "is this the current version" — the small validation below shows why a purely present-tense check misses real, material risk.

## 3. Pattern Provisional Waiver — refined, and extended to Disputed

**Two findings that motivated this:**
- The waiver as written ("1 source sufficient at Provisional") doesn't distinguish a source that *affirmatively observes* the pattern from one that reports an inconclusive or non-significant result. A single non-significant finding technically satisfies "1 source exists" while providing no real support for the pattern's existence.
- The original rule only defined Provisional's requirement. **Disputed was left completely unaddressed** — a real gap, since Disputed is already an active Maturity value in the Knowledge Base (T01, T02, PA02).

**Revised rule:**
- **Provisional:** 1 source still sufficient, but it must show an *affirmative, if limited or context-bound, observation* of the pattern — a purely inconclusive or non-significant result does not satisfy the waiver on its own; it should be logged but the object stays below even Provisional-Pass until a genuinely supportive source exists.
- **Disputed** (new, was previously unaddressed): requires **both** a supporting source and an opposing/limiting source — Disputed is a stronger epistemic claim than Provisional (it asserts active disagreement, not just insufficient evidence), and representing that honestly requires showing both sides, the same logic already applied to Theory's contested-source rule.
- Promotion beyond Disputed/Provisional to Verified still requires Theory-equivalent triangulation, unchanged from v0.1.

## Evidence Strength — new, not a replacement for Evidence Quality

**Quality** is a property of a *source* (is this citation itself credible — High/Medium/Low). **Strength** is a property of a *claim* — given the current evidence, is this specific claim, as worded, adequately supported? Strong / Moderate / Weak.

The distinction matters because the same object can support claims of different strength depending on wording:

- *"CAPM predicts expected return rises linearly with beta, though this relationship has been empirically challenged — Fama & French (1992) find a flat beta-return relationship once other characteristics are controlled for."* → **Strong.** The claim is qualified to match exactly what the evidence shows, including its contested status.
- *"CAPM predicts expected return rises linearly with beta."* (unqualified) → **Moderate.** Technically supported by the originating sources, but the claim omits a well-evidenced contestation that's already in the object's own evidence — it understates uncertainty the evidence itself contains.

An object being ECC-Pass doesn't automatically make every claim about it Strong — a Pass object can still support a Weak claim if the claim overreaches what the cited evidence actually establishes. Evidence Strength will feed Research Answer Confidence as one input among others, not defined further here — that's downstream work, not part of this revision.
