"""Minimal self-check for faos_query.py: known IDs must resolve to known data."""
from faos_query import read_psv, KB_PATH, EVIDENCE_PATH, CONFIRMATORY_JSON
import json


def test_knowledge_base_has_known_concept():
    rows = read_psv(KB_PATH)
    risk = [r for r in rows if r["ID"] == "C01"]
    assert risk and risk[0]["Name"] == "Risk"


def test_evidence_has_known_citation():
    rows = read_psv(EVIDENCE_PATH)
    ev01 = [r for r in rows if r["EvidenceID"] == "EV01"]
    assert ev01 and "Sharpe" in ev01[0]["Citation"]


def test_confirmatory_results_cover_all_five_hypotheses():
    with open(CONFIRMATORY_JSON, encoding="utf-8") as f:
        d = json.load(f)
    assert set(d["results"].keys()) == {"H-C1", "H-C2", "H-C3", "H-C4", "H-C5"}
    assert d["confirmatory_sample_stocks"] == 1462


if __name__ == "__main__":
    test_knowledge_base_has_known_concept()
    test_evidence_has_known_citation()
    test_confirmatory_results_cover_all_five_hypotheses()
    print("faos_query self-check: all 3 checks passed")
