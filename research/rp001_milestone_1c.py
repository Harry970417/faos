import json
from pathlib import Path
import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(r"C:\Users\user\Desktop\faos")
feat = pd.read_parquet(ROOT / "rp001_data" / "features" / "rp001_features_v0.2.parquet")

RANK_FEATURES = ["F_INST_01_foreign_rank", "F_INST_02_trust_rank", "F_INST_03_dealer_self_rank",
                  "F_INST_04_dealer_hedge_rank", "F_INST_05_aggregate_rank", "F_INST_06_value_proxy_rank",
                  "F_INST_09_change_rate_rank"]
NON_RANK_FEATURES = ["F_INST_07_flow_to_volume", "F_INST_08_streak",
                       "F_INT_01_flow_x_momentum", "F_INT_02_flow_x_size", "F_INT_03_flow_x_liquidity"]
ALL_FEATURES = RANK_FEATURES + NON_RANK_FEATURES
HORIZONS = [1, 2, 3, 5]

# ---- sector / market-cap groupings ----
with open(ROOT / "rp001_data" / "twse_company_info.json", encoding="utf-8") as f:
    company_info = json.load(f)
sector_map = {c.get("公司代號"): c.get("產業別") for c in company_info}
feat["sector"] = feat["stock_id"].map(sector_map)

price = pd.concat([pd.read_csv(f, dtype={"stock_id": str}) for f in sorted((ROOT/"rp001_data"/"raw_price").glob("price_*.csv"))], ignore_index=True)
price["date"] = pd.to_datetime(price["date"])
shares_map = {}
for c in company_info:
    try: shares_map[c.get("公司代號")] = float(c.get("已發行普通股數或TDR原股發行股數","0"))
    except (ValueError,TypeError): pass
price["mcap"] = price["stock_id"].map(shares_map) * price["close"]
feat = pd.merge(feat, price[["stock_id","date","mcap"]], on=["stock_id","date"], how="left")
feat["mcap_tercile"] = feat.groupby("date")["mcap"].transform(lambda s: pd.qcut(s, 3, labels=["Small","Mid","Large"], duplicates="drop"))

# market state: equal-weighted 50-stock avg daily return, 60d rolling sign
mkt = price.groupby("date")["close"].mean().sort_index()
mkt_ret60 = mkt.pct_change(60)
mkt_state = mkt_ret60.apply(lambda x: "Bull" if x > 0 else ("Bear" if x <= 0 else np.nan))
feat["market_state"] = feat["date"].map(mkt_state)

feat["year"] = feat["date"].dt.year
feat["quarter"] = feat["date"].dt.to_period("Q").astype(str)

def daily_ic(df, feature, ret_col):
    """Daily cross-sectional Spearman IC between feature and forward return."""
    recs = []
    for d, g in df.groupby("date"):
        sub = g[[feature, ret_col]].dropna()
        if len(sub) < 10:
            continue
        ic, _ = stats.spearmanr(sub[feature], sub[ret_col])
        recs.append({"date": d, "ic": ic, "n": len(sub)})
    return pd.DataFrame(recs)

def newey_west_tstat(ic_series, lags=5):
    """Newey-West adjusted t-stat for mean(IC) != 0."""
    x = ic_series.values
    n = len(x)
    mean_ic = x.mean()
    resid = x - mean_ic
    gamma0 = np.sum(resid**2) / n
    nw_var = gamma0
    for lag in range(1, lags+1):
        w = 1 - lag/(lags+1)
        gamma_l = np.sum(resid[lag:] * resid[:-lag]) / n
        nw_var += 2 * w * gamma_l
    se_nw = np.sqrt(nw_var / n)
    t_nw = mean_ic / se_nw if se_nw > 0 else np.nan
    return t_nw, se_nw

print("=" * 70)
print("MILESTONE 1C: IC / ICIR / t-stat / Newey-West / Decay")
print("=" * 70)
summary_rows = []
ic_store = {}
for feature in ALL_FEATURES:
    for h in HORIZONS:
        ret_col = f"fwd_ret_t{h}"
        ic_df = daily_ic(feat, feature, ret_col)
        if len(ic_df) == 0:
            continue
        mean_ic = ic_df["ic"].mean()
        median_ic = ic_df["ic"].median()
        std_ic = ic_df["ic"].std()
        icir = mean_ic / std_ic if std_ic > 0 else np.nan
        pos_ratio = (ic_df["ic"] > 0).mean()
        t_raw, p_raw = stats.ttest_1samp(ic_df["ic"], 0)
        t_nw, se_nw = newey_west_tstat(ic_df["ic"])
        ci_low = mean_ic - 1.96 * se_nw
        ci_high = mean_ic + 1.96 * se_nw
        summary_rows.append({
            "feature": feature, "horizon": h, "n_days": len(ic_df),
            "mean_ic": mean_ic, "median_ic": median_ic, "icir": icir,
            "pos_ic_ratio": pos_ratio, "t_raw": t_raw, "t_nw": t_nw,
            "ci95_low": ci_low, "ci95_high": ci_high,
        })
        if h == 1:
            ic_store[feature] = ic_df

summary = pd.DataFrame(summary_rows)
summary.to_csv(ROOT / "rp001_data" / "milestone1c_ic_summary.csv", index=False)
pd.set_option("display.width", 200)
pd.set_option("display.max_rows", 100)
print(summary.round(4).to_string(index=False))
