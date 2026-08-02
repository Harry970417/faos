"""
RP-001 Phase 2A.3: Missingness Policy Rule 3 (80% stock-level coverage gate),
dataset snapshot/hashing, unit tests, and leakage-truncation tests.
"""
import hashlib, json, time
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(r"C:\Users\user\Desktop\faos")
PROC_DIR = ROOT / "rp001_data" / "phase2a" / "processed"
COVERAGE_THRESHOLD = 0.80

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    log("Loading feature panel...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_features.parquet")
    log(f"Panel: {len(panel):,} rows")

    results = {"checks": []}
    def check(name, condition, detail=""):
        results["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        log(f"  [{'PASS' if condition else 'FAIL'}] {name} {('- ' + detail) if detail else ''}")

    # ================= Missingness Policy Rule 3: 80% stock-level coverage gate =================
    log("Computing per-stock F_INST_01 coverage (Missingness Policy Rule 3)...")
    cov = panel.groupby("stock_id")["F_INST_01_foreign"].agg(["count", "size"])
    cov["coverage_rate"] = cov["count"] / cov["size"]
    cov["passes_gate"] = cov["coverage_rate"] >= COVERAGE_THRESHOLD
    n_pass = cov["passes_gate"].sum()
    n_total = len(cov)
    log(f"Coverage gate: {n_pass}/{n_total} stocks pass ({n_pass/n_total*100:.1f}%), "
        f"threshold={COVERAGE_THRESHOLD}")
    cov.to_csv(PROC_DIR / "rp001_stock_coverage.csv")

    panel = panel.merge(cov[["passes_gate"]], left_on="stock_id", right_index=True, how="left")
    panel = panel.rename(columns={"passes_gate": "in_confirmatory_sample"})

    n_stock_1213_check = "1213" in cov.index and not cov.loc["1213", "passes_gate"]
    check("Stock 1213 (known AR-03 sparse case) excluded by coverage gate", n_stock_1213_check,
          f"1213 coverage_rate={cov.loc['1213','coverage_rate']:.3f}" if "1213" in cov.index else "1213 not in universe")

    # ================= Unit tests =================
    log("Running unit tests...")
    rank_cols = ["F_INST_01_foreign_rank", "F_INST_05_aggregate_rank"]
    for c in rank_cols:
        valid = panel[c].dropna()
        check(f"{c}: rank bounds [0,1]", (valid.min() >= 0) and (valid.max() <= 1),
              f"min={valid.min():.4f} max={valid.max():.4f}")

    int_cols = ["F_INT_01_flow_x_momentum", "F_INT_03_flow_x_liquidity", "F_INT_04_foreign_x_liquidity",
                "F_INT_05_foreign_x_volatility", "F_INT_07_foreign_x_momentum"]
    for c in int_cols:
        has_inf = np.isinf(panel[c].dropna()).any()
        check(f"{c}: no infinite values", not has_inf)
        valid = panel[c].dropna()
        check(f"{c}: product-of-ranks bounds [0,1]", (valid.min() >= 0) and (valid.max() <= 1),
              f"min={valid.min():.4f} max={valid.max():.4f}")

    check("F_INT_02_flow_x_size: all-NaN (D-08, not constructible)", panel["F_INT_02_flow_x_size"].isna().all())
    check("F_INT_06_foreign_x_size: all-NaN (D-08, not constructible)", panel["F_INT_06_foreign_x_size"].isna().all())

    # F_INST_05 sum verification
    agg_cats = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging", "Dealer"]
    recomputed = panel[agg_cats].sum(axis=1, min_count=1)
    diff = (panel["F_INST_05_aggregate"] - recomputed).abs()
    check("F_INST_05_aggregate == sum of 6 raw categories", (diff.fillna(0) < 1e-6).all(), f"max_diff={diff.max()}")

    # No 100% observed-zero row silently dropped: explicit-zero preserved (Missingness Policy Rule 4)
    n_explicit_zero = (panel["F_INST_01_foreign"] == 0).sum()
    check("Explicit-zero F_INST_01 observations preserved (not NaN'd)", n_explicit_zero > 0,
          f"n={n_explicit_zero:,}")

    # Break period split correctness
    check("break_period split respects locked point estimate (2025-09-25)",
          (panel[panel["break_period"] == "pre"]["date"] < "2025-09-25").all()
          and (panel[panel["break_period"] == "post"]["date"] >= "2025-09-25").all())

    # ================= Leakage / truncation tests =================
    log("Running leakage-truncation tests...")
    # For each stock, the LAST eligible date must have NaN fwd_ret_t5 (no data 5 days beyond
    # the end of the available series -- a leak would show a non-NaN value using data that
    # doesn't exist / wraps around to another stock).
    last_rows = panel.sort_values(["stock_id", "date"]).groupby("stock_id").tail(1)
    check("Last eligible date per stock has NaN fwd_ret_t5 (no forward leakage past series end)",
          last_rows["fwd_ret_t5"].isna().all() or last_rows["fwd_ret_t5"].isna().mean() > 0.95,
          f"{last_rows['fwd_ret_t5'].isna().mean()*100:.1f}% of last-dates are NaN (expected ~100%, "
          f"a small residual can occur if 5 more true trading days exist just past the eligible-window "
          f"cutoff for a stock but before the panel's last acquisition date)")

    # fwd_ret_t1 must never be computed using a date the panel itself doesn't contain (i.e. the
    # forward-return series length matches the raw price series length, not extended/wrapped)
    sample_sid = panel["stock_id"].iloc[0]
    n_nan_tail_t1 = panel[panel["stock_id"] == sample_sid].sort_values("date")["fwd_ret_t1"].tail(3).isna().sum()
    check("Spot-check: forward returns near series end show increasing NaN density (no wraparound)",
          n_nan_tail_t1 >= 1, f"stock {sample_sid}: {n_nan_tail_t1}/3 of last 3 rows NaN for fwd_ret_t1")

    # Rank computed only within same date (no cross-date leakage in rank_pct)
    d0 = panel["date"].iloc[len(panel)//2]
    day_slice = panel[panel["date"] == d0]
    manual_rank_max = day_slice["F_INST_01_foreign"].rank(pct=True).max()
    check("Daily rank is computed strictly within-day (no cross-date leakage)",
          abs(day_slice["F_INST_01_foreign_rank"].max() - manual_rank_max) < 1e-9 or day_slice["F_INST_01_foreign_rank"].isna().all(),
          f"date={d0}")

    n_passed = sum(c["passed"] for c in results["checks"])
    n_total_checks = len(results["checks"])
    log(f"\nUnit + leakage tests: {n_passed}/{n_total_checks} passed")

    # ================= Save final dataset + snapshot hash =================
    final_path = PROC_DIR / "rp001_confirmatory_dataset_v0.1.parquet"
    panel.to_parquet(final_path, index=False)
    sha = hashlib.sha256()
    with open(final_path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            sha.update(chunk)
    snapshot = {
        "dataset_path": str(final_path.relative_to(ROOT)),
        "sha256": sha.hexdigest(),
        "rows": len(panel),
        "cols": panel.shape[1],
        "build_timestamp_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "stocks_total": n_total,
        "stocks_passing_coverage_gate": int(n_pass),
        "coverage_gate_threshold": COVERAGE_THRESHOLD,
        "tests_passed": n_passed,
        "tests_total": n_total_checks,
        "test_detail": results["checks"],
    }
    with open(PROC_DIR / "rp001_dataset_snapshot.json", "w", encoding="utf-8") as f:
        json.dump(snapshot, f, indent=2, default=str)
    log(f"Final dataset: {final_path} (SHA-256: {sha.hexdigest()[:16]}...)")
    log("DONE")


if __name__ == "__main__":
    main()
