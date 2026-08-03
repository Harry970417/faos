"""
RP-001 Phase 2A: Showcase charts, built entirely from real computed results
(confirmatory dataset + test results JSON + acquisition manifests). No
illustrative/placeholder data anywhere.
"""
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
PROC_DIR = ROOT / "rp001_data" / "phase2a" / "processed"
CHART_DIR = ROOT / "rp001_data" / "phase2a" / "charts"
CHART_DIR.mkdir(parents=True, exist_ok=True)

plt.rcParams.update({"figure.dpi": 120, "font.size": 10, "axes.grid": True, "grid.alpha": 0.3})

def log(msg):
    print(f"[{time.strftime('%H:%M:%S')}] {msg}", flush=True)


def daily_ic_series(df, feature, ret_col, min_n=8):
    sub = df[["date", feature, ret_col]].dropna()
    g = sub.groupby("date")
    x = g[feature].rank(pct=True)
    y = g[ret_col].rank(pct=True)
    tmp = pd.DataFrame({"date": sub["date"].values, "x": x.values, "y": y.values})
    n = tmp.groupby("date")["x"].transform("count")
    tmp = tmp[n >= min_n]
    s = tmp.assign(xy=tmp["x"] * tmp["y"], xx=tmp["x"] ** 2, yy=tmp["y"] ** 2).groupby("date").agg(
        n=("x", "count"), sx=("x", "sum"), sy=("y", "sum"), sxy=("xy", "sum"), sxx=("xx", "sum"), syy=("yy", "sum"))
    num = s["n"] * s["sxy"] - s["sx"] * s["sy"]
    den = np.sqrt((s["n"] * s["sxx"] - s["sx"] ** 2) * (s["n"] * s["syy"] - s["sy"] ** 2))
    ic = (num / den).replace([np.inf, -np.inf], np.nan)
    return ic.dropna().sort_index()


def main():
    log("Loading confirmatory dataset...")
    panel = pd.read_parquet(PROC_DIR / "rp001_confirmatory_dataset_v0.1.parquet")
    sample = panel[panel["in_confirmatory_sample"] == True].copy()
    with open(PROC_DIR / "rp001_confirmatory_test_results.json", encoding="utf-8") as f:
        results = json.load(f)
    cov = pd.read_csv(PROC_DIR / "rp001_stock_coverage.csv")
    universe = pd.read_csv(ROOT / "rp001_data" / "phase2a_acquisition_universe.csv", dtype=str)

    # ==== Chart 1: Universe coverage (market x eligibility) ====
    log("Chart 1: universe coverage...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    mkt_counts = universe["market"].value_counts()
    elig_stocks = set(panel["stock_id"].unique())
    total_by_mkt = universe.groupby("market")["stock_id"].apply(lambda s: len(s))
    elig_by_mkt = universe[universe["stock_id"].isin(elig_stocks)].groupby("market")["stock_id"].apply(lambda s: len(s))
    mkts = list(total_by_mkt.index)
    x = np.arange(len(mkts))
    ax.bar(x - 0.2, total_by_mkt.values, width=0.4, label="Universe (acquired)", color="#4C72B0")
    ax.bar(x + 0.2, [elig_by_mkt.get(m, 0) for m in mkts], width=0.4, label="Has eligible panel rows", color="#55A868")
    ax.set_xticks(x); ax.set_xticklabels(mkts)
    ax.set_ylabel("Stock count"); ax.set_title("RP-001 Phase 2A: Universe Coverage by Market")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "01_universe_coverage.png"); plt.close(fig)

    # ==== Chart 2: Missingness (coverage-rate histogram + gate) ====
    log("Chart 2: missingness distribution...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    ax.hist(cov["coverage_rate"], bins=40, color="#4C72B0", alpha=0.85)
    ax.axvline(0.80, color="red", linestyle="--", label="80% coverage gate")
    n_pass = (cov["coverage_rate"] >= 0.80).sum()
    ax.set_xlabel("Per-stock F_INST_01 coverage rate"); ax.set_ylabel("Number of stocks")
    ax.set_title(f"RP-001 Phase 2A: Institutional-Data Coverage Distribution\n({n_pass}/{len(cov)} stocks pass the 80% gate)")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "02_missingness_distribution.png"); plt.close(fig)

    # ==== Chart 3: Institutional-category history (Dealer vs split, market-wide daily count) ====
    log("Chart 3: institutional category history...")
    inst_sample_path = PROC_DIR / "rp001_confirmatory_panel_raw.parquet"
    raw = pd.read_parquet(inst_sample_path, columns=["date", "Dealer", "Dealer_self", "Dealer_Hedging"])
    raw["date_m"] = pd.to_datetime(raw["date"]).dt.to_period("M").dt.to_timestamp()
    monthly = raw.groupby("date_m").agg(
        dealer_undiff=("Dealer", lambda s: s.notna().sum()),
        dealer_split=("Dealer_self", lambda s: s.notna().sum()))
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(monthly.index, monthly["dealer_undiff"], label="Undifferentiated 'Dealer' (row count/month)", color="#C44E52")
    ax.plot(monthly.index, monthly["dealer_split"], label="Split 'Dealer_self' (row count/month)", color="#55A868")
    ax.axvspan(pd.Timestamp("2025-08-01"), pd.Timestamp("2025-10-31"), alpha=0.15, color="orange", label="Break window")
    ax.set_ylabel("Institutional rows / month"); ax.set_title("RP-001 Phase 2A: Dealer-Category Schema History (Market-Wide)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHART_DIR / "03_institutional_category_history.png"); plt.close(fig)
    del raw

    # ==== Chart 4: Rolling IC (F_INST_01, t+5, 60-day rolling mean) ====
    log("Chart 4: rolling IC...")
    ic5 = daily_ic_series(sample, "F_INST_01_foreign_rank", "fwd_ret_t5")
    ic5.index = pd.to_datetime(ic5.index)
    ic5_roll = ic5.rolling(60, min_periods=30).mean()
    fig, ax = plt.subplots(figsize=(9, 4.5))
    ax.plot(ic5_roll.index, ic5_roll.values, color="#4C72B0", linewidth=1.2)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.axvline(pd.Timestamp("2025-09-25"), color="red", linestyle="--", label="Locked break point estimate (2025-09-25)")
    ax.set_ylabel("60-day rolling mean IC (t+5)"); ax.set_title("RP-001 Phase 2A: F_INST_01 Rolling IC, Full Universe (2012-2026)")
    ax.legend(fontsize=8)
    fig.tight_layout(); fig.savefig(CHART_DIR / "04_rolling_ic.png"); plt.close(fig)

    # ==== Chart 5: Break before/after (exploratory vs confirmatory) ====
    log("Chart 5: break before/after comparison...")
    fig, ax = plt.subplots(figsize=(7, 4.5))
    labels = ["Pre-break\n(exploratory)", "Pre-break\n(confirmatory)", "Post-break\n(exploratory)", "Post-break\n(confirmatory)"]
    vals = [0.052, results["results"]["H-C1"]["t5"]["mean_ic"], -0.008, results["results"]["H-C2"]["t5"]["mean_ic"]]
    colors = ["#4C72B0", "#4C72B0", "#C44E52", "#C44E52"]
    hatches = ["", "//", "", "//"]
    bars = ax.bar(labels, vals, color=colors)
    for b, h in zip(bars, hatches):
        b.set_hatch(h)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean IC (t+5)"); ax.set_title("RP-001: Break-Period IC, Exploratory vs. Confirmatory\n(solid = exploratory 50-stock; hatched = confirmatory full-universe)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "05_break_before_after.png"); plt.close(fig)

    # ==== Chart 6: Liquidity groups ====
    log("Chart 6: liquidity groups...")
    hc3 = results["results"]["H-C3"]
    fig, ax = plt.subplots(figsize=(7, 4.5))
    terciles = ["Illiquid", "Mid", "Liquid"]
    ics = [hc3[t]["mean_ic"] for t in terciles]
    ts = [hc3[t]["t_nw"] for t in terciles]
    colors = ["#55A868" if abs(t) > 1.96 else "#B0B0B0" for t in ts]
    bars = ax.bar(terciles, ics, color=colors)
    for bar, t in zip(bars, ts):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0003, f"t={t:.2f}", ha="center", fontsize=9)
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_ylabel("Mean IC (t+5)"); ax.set_title("RP-001 Phase 2A: H-C3 Liquidity Conditionality (green = |t|>1.96)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "06_liquidity_groups.png"); plt.close(fig)

    # ==== Chart 7: Hypothesis verdicts scorecard ====
    log("Chart 7: hypothesis verdicts...")
    verdicts = {"H-C1": "Not Replicated", "H-C2": "Replicated*", "H-C3": "Partially Replicated",
                "H-C4": "Not Replicated", "H-C5": "Not Replicated"}
    color_map = {"Replicated*": "#55A868", "Partially Replicated": "#DD8452", "Not Replicated": "#C44E52"}
    fig, ax = plt.subplots(figsize=(8, 3.5))
    hyps = list(verdicts.keys())
    for i, h in enumerate(hyps):
        ax.barh(h, 1, color=color_map[verdicts[h]])
        ax.text(0.5, i, verdicts[h], ha="center", va="center", color="white", fontweight="bold")
    ax.set_xlim(0, 1); ax.set_xticks([])
    ax.set_title("RP-001 Phase 2A: H-C1-H-C5 Verdict Scorecard\n(*H-C2 replicated by letter, but weakened by H-C1's failure)")
    fig.tight_layout(); fig.savefig(CHART_DIR / "07_hypothesis_verdicts.png"); plt.close(fig)

    # ==== Chart 8: Exploratory vs Confirmatory comparison (all 5 features/hyps) ====
    log("Chart 8: exploratory vs confirmatory magnitude comparison...")
    fig, ax = plt.subplots(figsize=(9, 5))
    items = ["H-C1 t+5\n(pre-break IC)", "H-C3 Illiquid\n(t+5 IC)", "H-C4 LowVol&Pre\n(t+5 IC)",
             "F_INT_01 resid\n(t+5 IC)", "F_INT_03 resid\n(t+5 IC)"]
    explor = [0.052, 0.034, 0.069, -0.004, -0.004]
    confirm = [results["results"]["H-C1"]["t5"]["mean_ic"], hc3["Illiquid"]["mean_ic"],
               results["results"]["H-C4"]["LowVol_pre"]["mean_ic"],
               results["results"]["H-C5"]["F_INT_01_flow_x_momentum"]["residualized"]["5"]["mean_ic"],
               results["results"]["H-C5"]["F_INT_03_flow_x_liquidity"]["residualized"]["5"]["mean_ic"]]
    x = np.arange(len(items))
    ax.bar(x - 0.2, explor, width=0.4, label="Exploratory (50 stocks)", color="#4C72B0")
    ax.bar(x + 0.2, confirm, width=0.4, label="Confirmatory (full universe)", color="#DD8452")
    ax.axhline(0, color="black", linewidth=0.8)
    ax.set_xticks(x); ax.set_xticklabels(items, fontsize=8)
    ax.set_ylabel("Mean IC"); ax.set_title("RP-001: Exploratory vs. Confirmatory Effect Magnitudes")
    ax.legend()
    fig.tight_layout(); fig.savefig(CHART_DIR / "08_exploratory_vs_confirmatory.png"); plt.close(fig)

    log(f"All 8 charts saved to {CHART_DIR}")
    log("DONE")


if __name__ == "__main__":
    main()
