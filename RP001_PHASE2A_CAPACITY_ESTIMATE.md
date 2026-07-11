# RP-001 Phase 2A: Capacity Estimate

**Based on real pilot measurements, not theoretical throughput.** Source: `rp001_data/pilot/pilot_pull_log.csv` (7 stocks × 2 datasets, `RP001_PHASE2A_DATA_QUALITY_PILOT.md`) plus one additional real single-stock measurement of the third required dataset (`TaiwanStockPER`, stock 1101) taken during this estimate's preparation.

## Real per-stock ingredients

**Institutional + Price (7-stock pilot average):**
- Rows/stock: 82,123 / 7 = 11,732
- Bytes/stock: 9,789,110 / 7 = 1,398,444 (1.40 MB)
- API-active time/stock: 9.56s / 7 = 1.366s (2 requests)

**Valuation (`TaiwanStockPER`, single-stock measurement, 1101 only — lower confidence, see caveat below):**
- Rows: 3,552
- Bytes: 335,946 (0.34 MB)
- API-active time: 0.512s

**Combined per-stock, 3 datasets** (institutional + price + valuation — all three are needed: valuation for the locked PBR value/growth definition per `RP001_FULL_UNIVERSE_SPEC.md`):
- Rows: ~15,284/stock
- Bytes: ~1,734,390/stock (1.73 MB)
- API-active time: ~1.878s/stock + 3 × 0.4s inter-request delay (pilot's pace) = ~3.08s/stock wall time

**Caveat on representativeness:** the 7 pilot stocks were deliberately chosen for *diversity* (Item list in the Data Quality Pilot), which skews toward several long-history, high-activity names (1101, 2891, 0050 each carry ~14 years / ~15,000+ institutional rows). The true full-universe average is likely **lower** than this per-stock figure, because most TPEx and smaller-cap names have materially shorter listing histories. These estimates should be read as **upper-bound-leaning**, not a tight prediction.

## Universe size scenarios

| Scenario | Stock count | Basis |
|---|---|---|
| Low | 1,980 | Current TWSE (1,089) + TPEx (891) company registries only |
| Mid | 2,300 | + delisted stocks not already in current registries (337 total delisted per `RP001_FULL_UNIVERSE_SPEC.md`, conservatively ~320 net-new) |
| High | 2,500 | + buffer for edge cases (Item 8's residual ticker/rename gap, any registry undercounting) |

## Extrapolated full-universe capacity

| Metric | Low (1,980) | Mid (2,300) | High (2,500) |
|---|---|---|---|
| API requests | 5,940 | 6,900 | 7,500 |
| Total rows | ~30.3M | ~35.2M | ~38.2M |
| Total storage (raw) | ~3.4 GB | ~4.0 GB | ~4.3 GB |
| API-active time | ~62 min | ~72 min | ~78 min |
| Wall time (incl. pilot's 0.4s inter-request pacing) | ~102 min (1.7 hr) | ~118 min (2.0 hr) | ~128 min (2.1 hr) |

## Failure / retry cost

The pilot observed **0 retries and 0 failures across 14 requests** — too small a sample to estimate a real failure rate (a 0/14 result is consistent with failure rates anywhere from 0% to several percent within normal confidence bounds). No rate-limiting was observed at pilot pace (Availability Audit Item 9), but a dedicated high-throughput stress test at full-universe request volume was not run. **Recommendation:** budget a 15–20% time margin for retries at full scale as a standard engineering safety margin, not a measured rate — i.e., plan for ~2.0–2.5 hours wall time at the Mid scenario rather than the bare 2.0-hour figure.

## Incremental download / resume strategy

Per the Snapshot Architecture (`RP001_PHASE2A_DATA_SNAPSHOT_SPEC.md`), each raw pull is manifested with `(dataset, stock_id, query_start_date, query_end_date, status)`. A resume run checks the manifest first and skips any `(dataset, stock_id)` pair already marked `success` with the target date range fully covered — re-requesting only `failed`/`partial` entries or newly-added stocks. This is the same manifest already proven at pilot scale (`pilot_pull_log.csv`), scaled up rather than redesigned.

## What this estimate does not cover

Processing time (date-alignment joins, missing-state classification, universe construction) is not included — this is a raw-data-acquisition estimate only, matching Phase 2A.2 step 4 (`RP001_PHASE2A_EXECUTION_PLAN.md`), not the full Phase 2A.2–2A.5 pipeline.
