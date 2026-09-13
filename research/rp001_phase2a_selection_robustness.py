"""
RP-001 Phase 2A — Selection-robustness extension (graduate-stage addendum,
NOT part of the locked Phase 2A.4 confirmatory protocol).

Purpose: the confirmatory sample (1,462 of 2,096 stocks with any
institutional-flow record, 69.8%) is known to differ systematically from the
excluded 30.2% on liquidity, price, and volatility (RP001_LIMITATIONS_v0.2.md).
This script asks a narrower, answerable question with data already on disk
(no new acquisition): *within* the included sample, does H-C1/H-C2/H-C4's
already-null result hold across the whole liquidity spectrum, or is it an
average masking a real effect concentrated in one liquidity slice?

Reuses, unchanged: `daily_ic`, `ic_stats`, `bh_fdr` from
rp001_phase2a_confirmatory_tests.py, and the exact same `liq_tercile` column
(same tercile definition already locked and used for H-C3) from the
confirmatory dataset. No new data pulled, no new feature defined, no change
to any H-C1-H-C5 locked result -- this is a new, separate, unlocked analysis.
"""
import json
import time
from pathlib import Path

import numpy as np
import pandas as pd

from rp001_phase2a_confirmatory_tests import daily_ic, ic_stats, bh_fdr, ROOT, PROC_DIR


def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def main():
    log("Loading confirmatory dataset...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_dataset_v0.1.parquet")
    sample = panel[panel["in_confirmatory_sample"] == True].copy()
    log(f"Confirmatory sample: {len(sample):,} rows, {sample['stock_id'].nunique()} stocks")

    tests = []  # (test_id, stat_dict)
    out = {"H-C1_by_tercile": {}, "H-C2_by_tercile": {}, "H-C4_defining_cells_by_tercile": {}}

    # ---- H-C1: pre-break, 3 horizons, by liquidity tercile ----
    pre = sample[sample["break_period"] == "pre"]
    for tercile in ["Illiquid", "Mid", "Liquid"]:
        sub = pre[pre["liq_tercile"] == tercile]
        cell = {}
        for h in [1, 3, 5]:
            ic_df = daily_ic(sub, "F_INST_01_foreign_rank", f"fwd_ret_t{h}")
            st = ic_stats(ic_df, f"H-C1 {tercile} t+{h}")
            cell[f"t{h}"] = st
            tests.append((f"SR_H-C1_{tercile}_t{h}", st))
            log(f"H-C1 {tercile} t+{h}: n={st['n']} mean_ic={st['mean_ic']} t_nw={st['t_nw']}")
        out["H-C1_by_tercile"][tercile] = cell

    # ---- H-C2: post-break, t+5, by liquidity tercile ----
    post = sample[sample["break_period"] == "post"]
    for tercile in ["Illiquid", "Mid", "Liquid"]:
        sub = post[post["liq_tercile"] == tercile]
        ic_df = daily_ic(sub, "F_INST_01_foreign_rank", "fwd_ret_t5")
        st = ic_stats(ic_df, f"H-C2 {tercile} t+5")
        out["H-C2_by_tercile"][tercile] = st
        tests.append((f"SR_H-C2_{tercile}_t5", st))
        log(f"H-C2 {tercile} t+5: n={st['n']} mean_ic={st['mean_ic']} t_nw={st['t_nw']}")

    # ---- H-C4: the two defining cells (Low-vol & Pre-break, Low-vol & Post-break), by tercile ----
    for bp in ["pre", "post"]:
        cell_key = f"LowVol_{bp}"
        out["H-C4_defining_cells_by_tercile"][cell_key] = {}
        for tercile in ["Illiquid", "Mid", "Liquid"]:
            sub = sample[(sample["market_vol_regime"] == "LowVol") &
                         (sample["break_period"] == bp) &
                         (sample["liq_tercile"] == tercile)]
            ic_df = daily_ic(sub, "F_INST_01_foreign_rank", "fwd_ret_t5")
            st = ic_stats(ic_df, f"H-C4 {cell_key} {tercile} t+5")
            out["H-C4_defining_cells_by_tercile"][cell_key][tercile] = st
            tests.append((f"SR_H-C4_{cell_key}_{tercile}_t5", st))
            log(f"H-C4 {cell_key} {tercile} t+5: n={st['n']} mean_ic={st['mean_ic']} t_nw={st['t_nw']}")

    # ---- BH-FDR across this addendum's own test family (separate from the locked 16) ----
    pvals = [st["raw_p"] if st and st.get("raw_p") is not None else np.nan for _, st in tests]
    qvals = bh_fdr(pvals, alpha=0.10)
    fdr_table = []
    for (test_id, st), q in zip(tests, qvals):
        fdr_table.append({"test_id": test_id, "n": st.get("n"), "mean_ic": st.get("mean_ic"),
                           "t_nw": st.get("t_nw"), "raw_p": st.get("raw_p"),
                           "q_bh": float(q) if pd.notna(q) else None,
                           "significant_q10": bool(pd.notna(q) and q < 0.10)})

    result = {
        "generated_utc": pd.Timestamp.now(tz="UTC").isoformat(),
        "note": "Graduate-stage selection-robustness addendum. NOT part of the locked Phase 2A.4 "
                "confirmatory protocol; a separate, unlocked analysis reusing the same dataset, "
                "tercile definition, and NW-HAC/BH-FDR methods.",
        "n_tests": len(tests),
        "results": out,
        "multiple_testing": {"method": "Benjamini-Hochberg", "alpha": 0.10,
                              "n_tests": len(tests), "table": fdr_table},
    }
    out_path = PROC_DIR / "rp001_selection_robustness_results.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, default=str)
    log(f"Saved: {out_path}")


if __name__ == "__main__":
    main()
