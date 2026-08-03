from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")

def bh_fdr(pvals, alpha=0.10):
    """Benjamini-Hochberg FDR correction."""
    p = np.asarray(pvals)
    n = len(p)
    order = np.argsort(p)
    ranked_p = p[order]
    q = np.empty(n)
    prev = 1.0
    for i in range(n-1, -1, -1):
        val = ranked_p[i] * n / (i+1)
        prev = min(prev, val)
        q[i] = prev
    q_final = np.empty(n)
    q_final[order] = q
    return q_final, q_final <= alpha

# ---- Compile test inventory from Milestone 1C's IC summary ----
ic_summary = pd.read_csv(ROOT / "rp001_data" / "milestone1c_ic_summary.csv")
ic_summary["p_raw"] = 2 * (1 - stats.norm.cdf(ic_summary["t_nw"].abs()))
ic_summary["test_id"] = ic_summary["feature"] + "_t" + ic_summary["horizon"].astype(str)
ic_summary["test_family"] = "1C_feature_horizon_IC"

# ---- Additional tests from 1C+ and 1C-R (compiled manually from computed results) ----
additional = [
    {"test_id": "F_INST_01_yearly_2024vs2026", "test_family": "1C_stability", "t_nw": 3.412, "p_raw": None},
    {"test_id": "F_INST_01_lowvol_vs_highvol", "test_family": "1C_plus_regime", "t_nw": 3.185, "p_raw": None},
    {"test_id": "F_INST_01_bear_vs_bull", "test_family": "1C_plus_regime", "t_nw": None, "p_raw": None},
    {"test_id": "F_INT_04_foreign_x_liquidity_residual", "test_family": "interaction_incremental", "t_nw": -0.035, "p_raw": None},
    {"test_id": "F_INT_05_foreign_x_volatility_residual", "test_family": "interaction_incremental", "t_nw": -1.341, "p_raw": None},
    {"test_id": "F_INT_06_foreign_x_size_residual", "test_family": "interaction_incremental", "t_nw": -0.283, "p_raw": None},
    {"test_id": "F_INT_07_foreign_x_momentum_residual", "test_family": "interaction_incremental", "t_nw": 0.038, "p_raw": None},
    {"test_id": "F_INST_01_breakpoint_sup_wald", "test_family": "structural_break", "t_nw": 3.453, "p_raw": 0.0105},
    {"test_id": "F_INST_07_breakpoint_sup_wald", "test_family": "structural_break", "t_nw": 2.390, "p_raw": 0.1710},
]
add_df = pd.DataFrame(additional)
add_df["p_raw"] = add_df.apply(
    lambda r: r["p_raw"] if pd.notna(r["p_raw"]) else (2*(1-stats.norm.cdf(abs(r["t_nw"]))) if pd.notna(r["t_nw"]) else np.nan),
    axis=1)

full = pd.concat([
    ic_summary[["test_id","test_family","t_nw","p_raw"]],
    add_df[["test_id","test_family","t_nw","p_raw"]],
], ignore_index=True).dropna(subset=["p_raw"])

q, sig = bh_fdr(full["p_raw"].values, alpha=0.10)
full["q_value_BH"] = q
full["significant_after_FDR_10pct"] = sig
full = full.sort_values("p_raw")
full.to_csv(ROOT / "rp001_data" / "multiple_testing_register.csv", index=False)

print(f"Total tests in inventory: {len(full)}")
print(f"Significant at raw p<0.05: {(full['p_raw']<0.05).sum()}")
print(f"Significant after BH-FDR correction (q<0.10): {full['significant_after_FDR_10pct'].sum()}")
print()
pd.set_option("display.width", 150)
print(full.round(4).to_string(index=False))
