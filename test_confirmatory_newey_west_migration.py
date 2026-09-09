"""2026-09-09: migrate rp001_phase2a_confirmatory_tests.py's hand-rolled
newey_west_tstat/ic_stats off bespoke inline arithmetic onto quant_formulas
(Desktop/quant-system-core). Pure refactor -- RP-001 is a formally closed,
locked confirmatory protocol, so this must produce byte-identical t-stats/
p-values, not just "close": max_lags=5 (matching the original's hardcoded
lags=5) and df=None (so t_stat_and_pvalue falls back to the normal
distribution, matching the original's scipy.stats.norm.cdf p-value, not a
t-distribution p-value which would silently change every locked H-C1-H-C5
number)."""
import numpy as np
import pandas as pd
import pytest

from quant_formulas.factor_stats import newey_west_se, t_stat_and_pvalue
from research.rp001_phase2a_confirmatory_tests import ic_stats, newey_west_tstat


def _synthetic_ic_df(values):
    return pd.DataFrame({"ic": values, "n": [50] * len(values)})


def test_newey_west_tstat_matches_quant_formulas_with_matching_lags_and_normal_pvalue():
    rng = np.random.default_rng(42)
    x = pd.Series(rng.normal(0.02, 0.05, size=80))

    t_old, se_old = newey_west_tstat(x, lags=5)

    se_new = newey_west_se(x, max_lags=5)
    t_new, _ = t_stat_and_pvalue(x.mean(), se_new, df=None)

    assert se_new == pytest.approx(se_old, abs=1e-12)
    assert t_new == pytest.approx(t_old, abs=1e-12)


def test_ic_stats_matches_quant_formulas_end_to_end():
    rng = np.random.default_rng(7)
    ic_values = rng.normal(0.03, 0.06, size=60)
    ic_df = _synthetic_ic_df(ic_values)

    old = ic_stats(ic_df, "test-label")

    se_new = newey_west_se(pd.Series(ic_values), max_lags=5)
    t_new, p_new = t_stat_and_pvalue(float(np.mean(ic_values)), se_new, df=None)

    assert old["t_nw"] == pytest.approx(t_new, abs=1e-9)
    assert old["raw_p"] == pytest.approx(p_new, abs=1e-9)


def test_ic_stats_empty_input_unchanged():
    empty_df = pd.DataFrame(columns=["date", "ic", "n"]).set_index("date")
    result = ic_stats(empty_df, "empty-label")
    assert result["n"] == 0
    assert np.isnan(result["t_nw"])
