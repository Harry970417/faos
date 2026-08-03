# RP-001 Phase 2A.2-R: API Quota and Acquisition Feasibility

**Date:** 2026-07-31. **Status:** Complete — informs the Decision Gate (`research/RP001_PHASE2A2R_DECISION_GATE.md`).

## 1. Token status

**No FinMind token exists in this environment.** Checked: `.env` (absent), `.gitignore` (no token-file exclusion pattern beyond the raw-data directory itself), all shell environment variables (`FINMIND_TOKEN` not set), and every `.py` file in the repo (no token string, no `token=` parameter anywhere in `research/rp001_batch_acquire.py` or any other script). Access to date has been 100% anonymous. No token value is reproduced anywhere in this document or any other file, per instruction — only its *presence/absence* is reported.

## 2. Quota — official documentation

FinMind's own repository documentation (`github.com/FinMind/FinMind`, fetched live this session) states, verbatim in translation:

- **Anonymous:** 300 requests / hour.
- **Registered, with `token` parameter attached to each request:** 600 requests / hour.
- No published information on paid Sponsor/Backer tiers' request ceiling, or on the exact reset mechanism (fixed clock-hour vs. rolling window) — this repo README is the most authoritative public source located; it does not go further than the two numbers above.

This is **official information, not an inference** — reported per your instruction not to guess.

## 3. Quota — empirical confirmation

| Test | Result |
|---|---|
| Batch 1 (2026-07-11): 360 sequential anonymous requests | 256 succeeded, then every request returned HTTP 402 `"Requests reach the upper limit"` from request #257 onward. Consistent with the official 300/hr ceiling, partially pre-consumed by earlier same-day pilot calls (Phase 2A.1). |
| This session (2026-07-31, 09:02 UTC), single anonymous request, `TaiwanStockInstitutionalInvestorsBuySell`, stock 2330 | **HTTP 200, 45 rows returned.** Confirms the quota has reset since 2026-07-11 — anonymous access is currently live and usable. |
| This session: omitting `data_id` to test bulk/multi-stock-per-request retrieval, `TaiwanStockInstitutionalInvestorsBuySell` and `TaiwanStockPrice`, single date | **HTTP 400** both times: `"Your level is free. Please update your user level."` Bulk/all-market queries are a **paid Sponsor-tier feature**, not unlocked by a free registered token. This forecloses the "one request per day covers all stocks" optimization for both anonymous and free-registered tiers. |
| Response headers for rate-limit/quota telemetry | None present (`X-RateLimit-*` etc. absent from all responses checked) — the API gives no advance warning before the 402 wall; the only reliable exhaustion signal is the 402 itself. |
| Max date range per request | No cap encountered. Batch 1 and this session's tests both requested `2012-01-01` to the current date (14.5 years) in a single call and received full data back. Treated as effectively unbounded for this project's purposes. |

**Reset rule:** confirmed only as "hourly" per official docs; the precise mechanic (fixed wall-clock hour vs. rolling 60-minute window) was **not tested further**, to avoid spending anonymous quota on a question the official doc already answers well enough to plan around (pace requests to stay under 300/hr and treat any 402 as the authoritative stop signal, rather than trying to reverse-engineer window boundaries).

## 4. Acquisition volume vs. quota

- Full universe: 2,255 stock_ids × 3 datasets (`TaiwanStockInstitutionalInvestorsBuySell`, `TaiwanStockPrice`, `TaiwanStockPER`) = **6,765 requests**.
- 85 stocks (255 requests) are already fully cached from Batch 1 and do not need re-fetching (see §5). Remaining: **2,170 stocks / 6,510 requests.**
- At 300/hr (anonymous): **~21.7 hours** of API-active time, necessarily spread across many separate hourly windows.
- At 600/hr (free registered token): **~10.85 hours**, same spreading requirement, roughly half the wall-clock span.
- Neither tier supports bulk/multi-symbol requests (§3) — per-stock, per-dataset calls are the only available shape regardless of token.

This is not a "get a token or fail" situation — **anonymous access alone is a legally sufficient, reproducible acquisition path**; a free token only doubles throughput. Registering one requires your email verification, which is action only you can take (listed as a blocking-condition category in your standing instructions), so it is deferred to a single, explicit ask at the end of this phase rather than treated as a hard blocker now.

## 5. Acquisition-efficiency redesign

Current `research/rp001_batch_acquire.py` (Batch 1 version) already has: per-(dataset, stock) file caching, SHA-256 per file, an append-only manifest, and a 3-retry-with-1.5s-sleep loop. Gaps identified and to be closed before any further batch runs:

| Gap | Fix |
|---|---|
| No skip-existing check — re-running a batch id re-downloads files already on disk | Add: before each `fetch()` call, check `RAW_DIR / f"{dataset}_{sid}.json"` exists **and** has a corresponding `status=success` row in `pull_manifest.csv`; skip if so. |
| Batch script takes a fixed `start_idx:end_idx` range with no per-symbol resume | Add a **failed-symbol queue** (`rp001_data/phase2a/manifests/failed_queue.csv`) — any `status != success` row is appended; a queue-drain mode retries only queued (stock, dataset) pairs instead of re-running a whole batch. |
| Fixed `time.sleep(0.4)` pacing, no quota awareness | Add a **request counter with an hourly window tracker**: stop issuing new requests once 280/hr is reached (20-request safety margin under the documented 300 ceiling) and sleep until the next window opens, rather than running into the 402 wall and losing an entire batch's remaining symbols the way Batch 1 did. |
| Metadata (universe list, listing dates) re-derived per script run | Already shared via `rp001_data/phase2a_acquisition_universe.csv`, single source — no change needed. |
| No incremental manifest summary (only the raw append-only CSV) | Add a small rollup step after each drain cycle: total requested / cached / pending / failed, written to `research/RP001_PHASE2A_BATCH_TRACKER.md`'s table — already the pattern in place, just needs to run more often than once per 120-stock batch. |

These changes are acquisition-tooling only — they do not touch `F_INST_01`'s definition, normalization, horizon, or the break interval, and require no deviation.

## 6. Alternative data-source matrix

**Not proposed.** Per your instruction, this matrix is only to be built if FinMind proves infeasible under legal conditions. It has not — anonymous access works today, a free token is available if wanted, and the per-stock request shape is a throughput problem (hours, not a hard wall), not a feasibility problem. Revisit only if a future finding makes FinMind itself unusable (e.g., ToS change, sustained outage).

## 7. What this document does NOT resolve

Throughput being solved does not resolve **D-04** (Dealer/Dealer_self/Dealer_Hedging recurrence — whether it can strike inside the locked 2025 break-interval window) or the missingness/market-membership questions. Those are addressed in the companion audits and roll up into the Decision Gate.
