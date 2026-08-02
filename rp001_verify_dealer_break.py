"""
D-05 pattern verification: for each flagged stock_id, confirm Foreign_Investor
is present on every date any institutional category reports (the invariant
that makes Dealer-vs-split-category schema irrelevant to F_INST_01).
Usage: python rp001_verify_dealer_break.py <stock_id> [<stock_id> ...]
"""
import sys, json
import pandas as pd

BREAK_START, BREAK_END = "2025-08-01", "2025-10-31"


def verify(sid):
    inst = pd.DataFrame(json.loads(open(f"rp001_data/phase2a/raw/TaiwanStockInstitutionalInvestorsBuySell_{sid}.json", encoding="utf-8").read()))
    price = pd.DataFrame(json.loads(open(f"rp001_data/phase2a/raw/TaiwanStockPrice_{sid}.json", encoding="utf-8").read()))
    brk = inst[(inst["date"] >= BREAK_START) & (inst["date"] <= BREAK_END)]
    pbrk = price[(price["date"] >= BREAK_START) & (price["date"] <= BREAK_END)]

    any_cat_dates = set(brk["date"].unique())
    fi_dates = set(brk[brk["name"] == "Foreign_Investor"]["date"].unique())
    fi_gap = sorted(any_cat_dates - fi_dates)  # dates with SOME category but no Foreign_Investor -- the only thing that would matter

    dealer_all = inst[inst["name"] == "Dealer"]["date"]
    split_all = inst[inst["name"].isin(["Dealer_self", "Dealer_Hedging"])]["date"]

    return {
        "stock_id": sid,
        "dealer_range": (dealer_all.min() if len(dealer_all) else None, dealer_all.max() if len(dealer_all) else None),
        "split_range": (split_all.min() if len(split_all) else None, split_all.max() if len(split_all) else None),
        "price_trading_dates_in_window": len(pbrk),
        "any_institutional_dates_in_window": len(any_cat_dates),
        "fi_specific_gap_dates": fi_gap,
        "fi_unaffected": len(fi_gap) == 0,
    }


if __name__ == "__main__":
    results = [verify(sid) for sid in sys.argv[1:]]
    n_ok = sum(r["fi_unaffected"] for r in results)
    for r in results:
        print(r)
    print(f"\n{n_ok}/{len(results)} stocks: Foreign_Investor unaffected (zero FI-specific gaps)")
    bad = [r["stock_id"] for r in results if not r["fi_unaffected"]]
    if bad:
        print(f"NEEDS ESCALATION -- FI-specific gaps found for: {bad}")
