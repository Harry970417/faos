# Publication Checklist

Final item-by-item quality gate for the repository's publication-ready state. Checked 2026-08-03 as part of the Final Publication Pass.

## README

- [x] 5-minute read or less at the top level
- [x] States what was done, research question, data scale, main findings, why worth reading, and entry points in the first screen
- [x] No overclaiming ("does not claim to have found a stable, tradeable alpha" stated explicitly)
- [x] All internal references use current post-reorganization paths
- [x] Repository map matches the actual directory structure

## Portfolio materials

- [x] One-page, 3–5 page, full-report, and micro-card versions all exist and are consistent with each other
- [x] Same fixed core conclusion wording used verbatim across all versions
- [x] No negative result reframed as a success
- [x] At least one figure embedded in the one-page version

## Research report

- [x] Full structure present (background, question, methods, results, limitations, integrity statement, conclusion, future work, reproducibility)
- [x] H-C1–H-C5 verdicts match `research/RP001_PHASE2A_HYPOTHESIS_VERDICTS.md` exactly
- [x] Exploratory and confirmatory findings clearly distinguished throughout
- [x] No claim of a stable alpha anywhere

## Application documents

- [x] All five schools represented, each genuinely differentiated (verified in `research/RP001_FINAL_CONSISTENCY_AUDIT.md` item 10)
- [x] Each includes "what not to emphasize" guidance
- [x] Each includes anticipated follow-up questions
- [x] None overstates investment/tradeability implications

## Interview materials

- [x] 30-second, 90-second, and 3-minute scripts all present and mutually consistent
- [x] Q&A bank covers all 20 required questions with correct answer, wrong answer to avoid, and likely follow-up
- [x] No answer implies the research produced a tradeable signal

## GitHub navigation

- [x] `README.md`, `PROJECT_STATUS.md`, `ROADMAP.md`, `CHANGELOG.md` all present at root
- [x] `RP001_READING_GUIDE.md` gives role-specific paths
- [x] `MASTER_DOCUMENT_INDEX.md` covers every file in the repository
- [x] `TERMINOLOGY.md` defines every term the reorganization was asked to unify

## Figures

- [x] All 11 figures renamed to `FigureNN_Description.png` convention, no `chart1.png`/`test.png`/`new_final2.png`-style names anywhere
- [x] `FIGURE_MANIFEST.md` covers purpose/source/using-document for every figure
- [x] `figures/RP001_FIGURE_INDEX.md` covers per-figure misreading risks
- [x] Chart-generation script (`research/rp001_phase2a_build_charts.py`) updated to write to the new `figures/` location and new filenames
- [x] No illustrative/placeholder data in any figure (verified at creation time, re-confirmed here)

## Links and references

- [x] Global reference-path fix applied across all `.md`/`.json` files for every moved document (183 renames, 84 files updated)
- [x] One real broken-link bug found during the fix (a markdown hyperlink's display text was updated but its target path was not) — found and corrected in `RP001_GITHUB_README_SECTION.md`
- [x] Remaining bare (non-backtick) filename mentions checked; genuine cross-directory stale references corrected; same-directory mentions in historical documents left as-is (not broken, just not path-prefixed)
- [x] No markdown hyperlinks anywhere else point to a pre-move path

## Citations and figures-to-documents mapping

- [x] Every figure's usage claim in `FIGURE_MANIFEST.md` verified against the documents that actually embed or discuss it

## Consistency

- [x] `2,255` / `1,462` / `5,718,238` / `3,934,274` verified identical across all current-tier documents post-move
- [x] H-C1–H-C5 verdicts verified identical across all current-tier documents post-move, including newly archived files (still correct, just superseded in role)
- [x] No duplicate file content beyond the one already-identified and archived pair (`eval_results.txt` / `evidence/EVALUATION_SUITE_v0.1_raw_results.txt`)

## Markdown quality

- [x] Spot-checked heading hierarchy, table formatting, list formatting in the newly-authored document set — no broken tables or skipped heading levels found
- [x] One full-width/half-width parenthesis inconsistency found and fixed (`portfolio/RP001_FINAL_SHOWCASE.md`)
- [x] One missing space between Chinese and English text found and fixed (`interview/RP001_INTERVIEW_QA_BANK.md`)
- [ ] Full line-by-line proofread of the ~85 legacy exploratory-phase documents was **not** performed — they are preserved as historical record per the project's own established principle (correct in place with a note, don't silently rewrite); a future pass could still spellcheck them without touching their conclusions

## Git

- [x] Reorganization performed with `git mv` throughout (history preserved on every moved file)
- [x] No raw data, large parquet files, tokens, secrets, caches, or temporary files staged
- [x] Commits split into logical groups per the requested structure
- [x] `git status --short` clean after the final commit
- [x] Not pushed
