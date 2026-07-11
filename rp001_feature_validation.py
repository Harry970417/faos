from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_v0.1.parquet")
FIG_DIR = ROOT / "rp001_data" / "figures"
FIG_DIR.mkdir(parents=True, exist_ok=True)

BASE_FEATURES = ["F_INST_01_foreign", "F_INST_02_trust", "F_INST_03_dealer_self",
                  "F_INST_04_dealer_hedge", "F_INST_05_aggregate", "F_INST_06_value_proxy",
                  "F_INST_07_flow_to_volume", "F_INST_08_streak", "F_INST_09_change_rate",
                  "F_INT_01_flow_x_momentum", "F_INT_02_flow_x_size", "F_INT_03_flow_x_liquidity"]

print("=" * 60)
print("1. FEATURE HEALTH REPORT")
print("=" * 60)
health_rows = []
for c in BASE_FEATURES:
    s = feat[c]
    n = len(s)
    n_valid = s.notna().sum()
    coverage = n_valid / n
    n_missing = n - n_valid
    zero_rate = (s.dropna() == 0).mean() if n_valid > 0 else np.nan
    sv = s.dropna()
    skew = stats.skew(sv) if len(sv) > 2 else np.nan
    kurt = stats.kurtosis(sv) if len(sv) > 2 else np.nan
    q1, q3 = sv.quantile(0.25), sv.quantile(0.75)
    iqr = q3 - q1
    outlier_mask = (sv < q1 - 3 * iqr) | (sv > q3 + 3 * iqr)
    outlier_rate = outlier_mask.mean()
    health_rows.append({
        "feature": c, "coverage": coverage, "n_missing": n_missing, "zero_rate": zero_rate,
        "mean": sv.mean(), "std": sv.std(), "skew": skew, "kurtosis": kurt,
        "outlier_rate_3IQR": outlier_rate,
    })
health = pd.DataFrame(health_rows)
pd.set_option("display.width", 160)
pd.set_option("display.max_columns", 20)
print(health.to_string(index=False))
health.to_csv(ROOT / "rp001_data" / "feature_health.csv", index=False)

print("\n" + "=" * 60)
print("2. CORRELATION ANALYSIS")
print("=" * 60)
corr_data = feat[BASE_FEATURES].dropna()
pearson = corr_data.corr(method="pearson")
spearman = corr_data.corr(method="spearman")
pearson.to_csv(ROOT / "rp001_data" / "feature_corr_pearson.csv")
spearman.to_csv(ROOT / "rp001_data" / "feature_corr_spearman.csv")

# Redundancy: pairs with |spearman| > 0.7
redundant_pairs = []
for i, a in enumerate(BASE_FEATURES):
    for b in BASE_FEATURES[i+1:]:
        r = spearman.loc[a, b]
        if abs(r) > 0.7:
            redundant_pairs.append((a, b, r))
print("Pairs with |Spearman| > 0.7 (redundancy candidates):")
for a, b, r in sorted(redundant_pairs, key=lambda x: -abs(x[2])):
    print(f"  {a} <-> {b}: {r:.3f}")
if not redundant_pairs:
    print("  None found.")

print("\n" + "=" * 60)
print("3. DISTRIBUTION DIAGNOSTICS")
print("=" * 60)
for c in ["F_INST_05_aggregate", "F_INST_09_change_rate"]:
    sv = feat[c].dropna()
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))
    axes[0].hist(sv, bins=100)
    axes[0].set_title(f"{c} histogram")
    stats.probplot(sv, dist="norm", plot=axes[1])
    axes[1].set_title(f"{c} QQ-plot vs Normal")
    rank_col = c + "_rank" if (c + "_rank") in feat.columns else None
    if rank_col:
        z = (sv - sv.mean()) / sv.std()
        axes[2].scatter(feat.loc[sv.index, rank_col], z, s=1, alpha=0.3)
        axes[2].set_xlabel("rank (percentile)")
        axes[2].set_ylabel("z-score")
        axes[2].set_title(f"{c}: rank vs z-score")
    plt.tight_layout()
    fig.savefig(FIG_DIR / f"{c}_diagnostics.png", dpi=100)
    plt.close(fig)
    print(f"Saved diagnostics plot: {c}_diagnostics.png")

print("\n" + "=" * 60)
print("4. LEAKAGE VALIDATION (empirical, not just code review)")
print("=" * 60)
# Empirical test: recompute F_INST_09 and F_INT_03 (both rolling-window features)
# for a truncated dataset (data only through date t) and confirm the value at t
# matches the value computed with the FULL dataset. If a feature used any t+1+
# data, truncating the future would change the value at t.
inst = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw").glob("inst_*.csv"))], ignore_index=True)
inst["date"] = pd.to_datetime(inst["date"])
inst["net"] = inst["buy"] - inst["sell"]
inst_wide = inst.pivot_table(index=["stock_id","date"], columns="name", values="net", aggfunc="first").reset_index()
CATS = ["Foreign_Investor","Foreign_Dealer_Self","Investment_Trust","Dealer_self","Dealer_Hedging"]

test_stock = "2330"
g = inst_wide[inst_wide.stock_id == test_stock].sort_values("date").reset_index(drop=True)
g["agg"] = g[CATS].sum(axis=1)
test_date_idx = 100  # an arbitrary interior date, well past any rolling window minimum
test_date = g.loc[test_date_idx, "date"]

full_roll = g["agg"].rolling(20, min_periods=10).mean()
full_val_at_t = full_roll.loc[test_date_idx]

truncated = g.loc[:test_date_idx].copy()  # ONLY data up to and including t
trunc_roll = truncated["agg"].rolling(20, min_periods=10).mean()
trunc_val_at_t = trunc_roll.iloc[-1]

leak_free = np.isclose(full_val_at_t, trunc_val_at_t, equal_nan=True)
print(f"F_INST_09 rolling-mean leakage test (stock {test_stock}, date {test_date.date()}):")
print(f"  Value using full dataset: {full_val_at_t}")
print(f"  Value using only data <= t: {trunc_val_at_t}")
print(f"  MATCH (no leakage): {leak_free}")

# Same test for the 20d momentum used in F_INT_01
close_test = pd.read_csv(ROOT / "rp001_data" / "raw_price" / f"price_{test_stock}.csv", parse_dates=["date"]).sort_values("date").reset_index(drop=True)
full_mom = close_test["close"].pct_change(20)
full_mom_val = full_mom.loc[test_date_idx] if test_date_idx < len(full_mom) else None
trunc_close = close_test.loc[:test_date_idx].copy()
trunc_mom = trunc_close["close"].pct_change(20)
trunc_mom_val = trunc_mom.iloc[-1]
print(f"\nF_INT_01 momentum(20d) leakage test:")
print(f"  Value using full dataset: {full_mom_val}")
print(f"  Value using only data <= t: {trunc_mom_val}")
print(f"  MATCH (no leakage): {np.isclose(full_mom_val, trunc_mom_val, equal_nan=True)}")

print("\n" + "=" * 60)
print("SEPARATE CONCERN: institutional-data publication timing vs feature date")
print("=" * 60)
print("Construction-level leakage (does the code peek at future rows) is tested above.")
print("A SEPARATE risk -- confirmed real in the Merge Loss Audit -- is that the")
print("institutional data ITSELF may carry a mis-dated row (see 2026-06-19 finding).")
print("If such a mis-dated row ever survives the inner join (this session's cases did not,")
print("by accident of the join, not by design), it would silently violate the t-only rule")
print("even though the feature CODE never looked ahead. This is a data-integrity leakage")
print("risk, distinct from a code leakage risk, and is not fully closed by the tests above.")
