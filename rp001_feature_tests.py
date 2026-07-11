"""RP-001 Milestone 1A: Feature unit tests. Real checks against the built
feature panel, not tautologies."""
import numpy as np
import pandas as pd

feat = pd.read_parquet(r"C:\Users\user\Desktop\faos\rp001_data\features\rp001_features_v0.1.parquet")
inst = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in
                   sorted((__import__("pathlib").Path(r"C:\Users\user\Desktop\faos\rp001_data\raw")).glob("inst_*.csv"))],
                  ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]
inst_wide = inst.pivot_table(index=["stock_id", "date"], columns="name", values="net", aggfunc="first").reset_index()

results = []
def check(name, cond, detail=""):
    results.append((name, bool(cond), detail))
    print(f"{'PASS' if cond else 'FAIL'}: {name} {detail}")

# 1. Row count sanity
check("Row count within expected merge-loss bound (<1%)",
      len(feat) >= 24584 * 0.99, f"n={len(feat)}")

# 2. F_INST_05_aggregate == true sum of all 5 raw categories (incl. Foreign_Dealer_Self)
merged_check = pd.merge(feat[["stock_id", "date", "F_INST_05_aggregate"]], inst_wide, on=["stock_id", "date"], how="inner")
cats = ["Foreign_Investor", "Foreign_Dealer_Self", "Investment_Trust", "Dealer_self", "Dealer_Hedging"]
true_sum = merged_check[cats].sum(axis=1)
diff = (merged_check["F_INST_05_aggregate"] - true_sum).abs()
check("F_INST_05_aggregate matches true sum of all 5 raw categories",
      diff.max() < 1e-6, f"max_diff={diff.max()}")

# 3. Rank columns in [0,1]
rank_cols = [c for c in feat.columns if c.endswith("_rank")]
for c in rank_cols:
    vals = feat[c].dropna()
    check(f"{c} in [0,1]", (vals.min() >= 0) and (vals.max() <= 1),
          f"min={vals.min():.4f} max={vals.max():.4f}")

# 4. Flow-to-volume ratio bounded (net flow can't exceed total volume in absolute value under normal reporting)
ratio = feat["F_INST_07_flow_to_volume"].dropna()
check("F_INST_07 within [-1.5, 1.5] for 99.9% of obs (loose bound, flags gross violations)",
      (ratio.between(-1.5, 1.5).mean() > 0.999),
      f"share_in_bound={ratio.between(-1.5,1.5).mean():.4f} min={ratio.min():.2f} max={ratio.max():.2f}")

# 5. Streak sign matches underlying flow sign
streak_sign = np.sign(feat["F_INST_08_streak"])
flow_sign = np.sign(feat["F_INST_05_aggregate"])
mismatch = (streak_sign != flow_sign) & (flow_sign != 0)
check("F_INST_08 streak sign matches aggregate flow sign",
      mismatch.sum() == 0, f"mismatches={mismatch.sum()}")

# 6. No infinite values anywhere
numeric_cols = feat.select_dtypes(include=[np.number]).columns
n_inf = np.isinf(feat[numeric_cols]).sum().sum()
check("No infinite values in any numeric feature", n_inf == 0, f"n_inf={n_inf}")

# 7. Version and build_date populated for every row
check("version populated for all rows", feat["version"].notna().all())
check("build_date populated for all rows", feat["build_date"].notna().all())

# 8. Foreign_Dealer_Self excluded as standalone feature (Milestone 0C decision actually implemented)
fds_present = any("dealer_self" in c.lower() and "foreign" in c.lower() for c in feat.columns)
check("Foreign_Dealer_Self NOT present as a standalone feature column",
      not fds_present, f"columns checked, none matched")

n_pass = sum(r[1] for r in results)
print(f"\n{n_pass}/{len(results)} checks passed")
if n_pass < len(results):
    print("FAILURES:", [r[0] for r in results if not r[1]])
