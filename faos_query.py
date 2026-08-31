#!/usr/bin/env python
"""FAOS query CLI: search Knowledge Objects, inspect Evidence Objects,
show the RP-001 protocol timeline, and compare exploratory vs confirmatory results.

ponytail: reads the PSV/JSON/MD files directly at call time (no cache/DB) --
303 knowledge rows and 36 evidence rows are small enough that a full scan
per query is fine. Revisit only if the knowledge base grows by orders of magnitude.
"""
import argparse
import csv
import json
import sys
from pathlib import Path

ROOT = Path(__file__).parent
KB_PATH = ROOT / "knowledge" / "knowledge_base_v0.2.psv"
EVIDENCE_PATH = ROOT / "evidence" / "evidence_pilot_v0.2.psv"
CONFIRMATORY_JSON = ROOT / "rp001_data" / "phase2a" / "processed" / "rp001_confirmatory_test_results.json"
PROTOCOL_LOCK_MD = ROOT / "research" / "RP001_PHASE2A_PROTOCOL_LOCK.md"


def read_psv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


def cmd_search(args):
    rows = read_psv(KB_PATH)
    term = args.term.lower()
    hits = [r for r in rows if term in r["Name"].lower() or term in r["Type"].lower()
            or term in r["RootTaxonomy"].lower()]
    if not hits:
        print(f"No Knowledge Objects match '{args.term}'.")
        return
    print(f"{len(hits)} match(es) for '{args.term}':\n")
    for r in hits:
        print(f"  [{r['ID']}] {r['Name']}  ({r['Type']}, {r['RootTaxonomy']}, {r['Maturity']})")


def cmd_show_evidence(args):
    rows = read_psv(EVIDENCE_PATH)
    hits = [r for r in rows if r["EvidenceID"] == args.evidence_id
            or args.evidence_id in (r["GroundedObjects"] or "").split(";")]
    if not hits:
        print(f"No Evidence Object found for '{args.evidence_id}'.")
        return
    for r in hits:
        print(f"[{r['EvidenceID']}] {r['Type']} ({r['Tier']}, quality={r['Quality']}, stance={r['Stance']})")
        print(f"  Citation: {r['Citation']}")
        print(f"  Grounds: {r['GroundedObjects']}")
        print()


def cmd_protocol_history(args):
    if not PROTOCOL_LOCK_MD.exists():
        print("No protocol lock record found.")
        return
    text = PROTOCOL_LOCK_MD.read_text(encoding="utf-8")
    print("RP-001 Phase 2A protocol timeline (from research/RP001_PHASE2A_PROTOCOL_LOCK.md):\n")
    for line in text.splitlines():
        if line.startswith("**") and ":**" in line:
            print(" ", line.strip("*").replace(":**", ":"))


def cmd_rp001_summary(args):
    with open(CONFIRMATORY_JSON, encoding="utf-8") as f:
        d = json.load(f)
    print("RP-001: exploratory (50 stocks) vs confirmatory (full-market) comparison\n")
    print(f"  Confirmatory sample: {d['confirmatory_sample_stocks']} stocks, "
          f"{d['confirmatory_sample_rows']:,} rows (generated {d['generated_utc']})")
    def print_leaf(r, indent):
        print(f"{' ' * indent}{r['label']:<28} n={r['n']:>5}  mean_ic={r['mean_ic']:+.4f}  "
              f"t_nw={r['t_nw']:+.2f}  p={r['raw_p']:.3f}")

    def walk(node, indent):
        # ponytail: result nesting depth varies by hypothesis (H-C1..H-C4 are 1-level,
        # H-C5 has an extra feature/raw-vs-other level) -- recurse until a 'label' leaf shows up
        if isinstance(node, dict) and "label" in node:
            print_leaf(node, indent)
        elif isinstance(node, dict):
            for k, v in node.items():
                print(f"{' ' * indent}{k}:")
                walk(v, indent + 2)

    print("  Hypothesis results (Newey-West t-stat, raw p-value, per horizon):")
    for h, horizons in d["results"].items():
        print(f"    {h}:")
        walk(horizons, 6)


def main():
    p = argparse.ArgumentParser(description="Query FAOS Knowledge/Evidence Objects.")
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("search", help="Search Knowledge Objects by name/type/taxonomy")
    s.add_argument("term")
    s.set_defaults(func=cmd_search)

    e = sub.add_parser("show-evidence", help="Show Evidence Object(s) by ID or grounded object ID")
    e.add_argument("evidence_id")
    e.set_defaults(func=cmd_show_evidence)

    sub.add_parser("protocol-history", help="Show RP-001 Phase 2A protocol lock timeline").set_defaults(
        func=cmd_protocol_history)

    sub.add_parser("rp001-summary", help="Compare RP-001 exploratory vs confirmatory results").set_defaults(
        func=cmd_rp001_summary)

    args = p.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
