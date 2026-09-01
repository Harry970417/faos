"""Minimal self-check for faos_viewer.flatten(): the RP-001 result-tree walker."""
from faos_viewer import flatten


def test_flatten_one_level_leaf():
    node = {"h1": {"label": "x", "n": 5}}
    out = list(flatten(node))
    assert out == [("h1 / ", {"label": "x", "n": 5})]


def test_flatten_nested_leaf():
    node = {"feature": {"raw": {"label": "y", "n": 3}}}
    out = list(flatten(node))
    assert out == [("feature / raw / ", {"label": "y", "n": 3})]


if __name__ == "__main__":
    test_flatten_one_level_leaf()
    test_flatten_nested_leaf()
    print("faos_viewer self-check: all 2 checks passed")
