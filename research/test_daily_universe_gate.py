"""
RP-001 Phase 2A.2-R: regression test for the Daily Investable Universe
eligibility gate (RP001_DAILY_INVESTABLE_UNIVERSE_SPEC_v2.md §2).
Guards against 興櫃/pre-listing data or a mishandled market-transfer date
silently entering the formal universe. Run: python test_daily_universe_gate.py
"""
from datetime import date


def stock_eligibility_start(listing_date_source: str, listing_date: str, first_price_date: str) -> str:
    """Mirrors Spec v2 §2. listing_date_source in {"registry", "unavailable"}."""
    if listing_date_source == "registry":
        return listing_date
    return first_price_date  # delisted / no registry entry -> D-02 proxy


def is_eligible(t: str, listing_date_source: str, listing_date: str, first_price_date: str,
                 institutional_floor: str = "2012-05-02", delisting_date: str | None = None) -> bool:
    start = max(institutional_floor, stock_eligibility_start(listing_date_source, listing_date, first_price_date))
    if t < start:
        return False
    if delisting_date and t >= delisting_date:
        return False
    return True


def demo():
    # 6986: registry listing_date 2026-06-26, but price data exists back to 2023-11-29 (興櫃).
    # The 興櫃 period MUST be excluded even though price data exists.
    assert not is_eligible("2026-06-01", "registry", "2026-06-26", "2023-11-29"), \
        "6986 pre-listing (興櫃) date wrongly marked eligible"
    assert is_eligible("2026-06-26", "registry", "2026-06-26", "2023-11-29"), \
        "6986 listing date itself should be eligible"

    # 1256: registry listing_date 2016-03-17, first price date 2012-09-05 (suspected TPEx history,
    # not documentarily confirmed). Spec v2 conservative rule: use registry date, not first-price date.
    assert not is_eligible("2013-01-01", "registry", "2016-03-17", "2012-09-05"), \
        "1256 pre-2016 unconfirmed-transfer period wrongly marked eligible under the conservative rule"
    assert is_eligible("2025-09-25", "registry", "2016-03-17", "2012-09-05"), \
        "1256 should be eligible throughout the 2025 break interval regardless of the transfer ambiguity"

    # Delisted stock with no registry entry: D-02 proxy uses first price date directly.
    assert is_eligible("2018-01-01", "unavailable", "", "2017-06-01"), \
        "delisted stock with price-proxy start date wrongly excluded"
    assert not is_eligible("2017-01-01", "unavailable", "", "2017-06-01"), \
        "delisted stock before its own first price date wrongly included"

    # Institutional floor applies even to a stock whose registry listing predates it.
    assert not is_eligible("2011-01-01", "registry", "1962-02-09", "1962-02-09"), \
        "date before the system-wide institutional floor wrongly marked eligible"

    print("All Daily Investable Universe gate checks passed.")


if __name__ == "__main__":
    demo()
