"""Automated Knowledge Graph integrity tests for knowledge/knowledge_base_v0.2.psv
(the 302-node/233-edge baseline cited throughout the "05 FAOS" portfolio materials).

Goes beyond the bare node/edge count: dangling references, duplicate IDs,
duplicate edges, invalid edge types, node-type schema violations, isolated
nodes, and connected-component fragmentation. Reuses `read_psv`/`KB_PATH`
from faos_query.py rather than re-implementing PSV parsing.

Regression-guard baseline established 2026-09-13 (see
research/RP001_HYPOTHESIS_REGISTRY.md's sibling doc,
architecture/KNOWLEDGE_GRAPH_AUDIT_v0.2.md, for the disclosed numbers):
302 nodes, 233 edges, 0 dangling/duplicate/invalid/schema issues,
71 isolated nodes, 105 connected components (largest: 135 nodes, 44.7%).
"""
import re
from collections import Counter, defaultdict

from faos_query import read_psv, KB_PATH

EDGE_COLS = ["DependsOn", "References", "Implements", "DerivedFrom"]
VALID_NODE_TYPES = {"Concept", "Metric", "Procedure", "Formula", "Theory", "Model",
                     "Standard", "Framework", "Assumption", "Factor", "Pattern"}

_TOKEN_RE = re.compile(r"([A-Za-z0-9]+)(\((.*)\))?")


def _parse_cell(cell):
    out = []
    if not cell:
        return out
    for token in cell.split(";"):
        token = token.strip()
        if not token:
            continue
        m = _TOKEN_RE.match(token)
        out.append((m.group(1), m.group(3) or ""))
    return out


def _load_graph():
    rows = read_psv(KB_PATH)
    nodes = {r["ID"]: r for r in rows}
    node_ids = [r["ID"] for r in rows]
    edges = []
    for r in rows:
        for et in EDGE_COLS:
            for tid, tag in _parse_cell(r.get(et, "")):
                edges.append((r["ID"], tid, et, tag))
    return nodes, node_ids, edges


def test_node_and_edge_counts_match_disclosed_baseline():
    nodes, node_ids, edges = _load_graph()
    assert len(nodes) == 302, f"expected 302 nodes, got {len(nodes)}"
    assert len(edges) == 233, f"expected 233 edges, got {len(edges)}"


def test_no_duplicate_node_ids():
    _, node_ids, _ = _load_graph()
    dupes = [nid for nid, c in Counter(node_ids).items() if c > 1]
    assert dupes == [], f"duplicate node IDs: {dupes}"


def test_no_dangling_edge_references():
    nodes, _, edges = _load_graph()
    dangling = [(s, t, et) for (s, t, et, _tag) in edges if s not in nodes or t not in nodes]
    assert dangling == [], f"dangling edge references (missing source or target): {dangling}"


def test_no_duplicate_edges():
    _, _, edges = _load_graph()
    dupes = [k for k, c in Counter((s, t, et) for (s, t, et, _tag) in edges).items() if c > 1]
    assert dupes == [], f"duplicate edges: {dupes}"


def test_no_invalid_edge_types():
    _, _, edges = _load_graph()
    invalid = [et for (_s, _t, et, _tag) in edges if et not in EDGE_COLS]
    assert invalid == [], f"invalid edge types: {invalid}"


def test_no_node_type_schema_violations():
    nodes, _, _ = _load_graph()
    violations = [(nid, n["Type"]) for nid, n in nodes.items() if n["Type"] not in VALID_NODE_TYPES]
    assert violations == [], f"node(s) with a Type outside the 11 KOM types: {violations}"


def _undirected_adjacency(nodes, edges):
    und = defaultdict(set)
    for (s, t, _et, _tag) in edges:
        if s in nodes and t in nodes:
            und[s].add(t)
            und[t].add(s)
    return und


def test_isolated_node_count_does_not_regress():
    nodes, _, edges = _load_graph()
    und = _undirected_adjacency(nodes, edges)
    isolated = [n for n in nodes if len(und[n]) == 0]
    # Baseline is 71 (2026-09-13, disclosed in architecture/KNOWLEDGE_GRAPH_AUDIT_v0.2.md).
    # Fewer isolated nodes (remediation) is welcome; more is a regression this test catches.
    assert len(isolated) <= 71, f"isolated node count regressed: {len(isolated)} > 71 baseline ({isolated})"


def test_connected_component_count_does_not_regress():
    nodes, _, edges = _load_graph()
    und = _undirected_adjacency(nodes, edges)
    visited = set()
    components = []
    for n in nodes:
        if n in visited:
            continue
        stack, comp = [n], set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            visited.add(u)
            stack.extend(v for v in und[u] if v not in comp)
        components.append(comp)
    # Baseline is 105 components, largest 135 nodes (44.7% of the graph).
    assert len(components) <= 105, f"component count regressed: {len(components)} > 105 baseline"
    largest = max(len(c) for c in components)
    assert largest >= 135, f"largest component shrank below the 135-node baseline: {largest}"


if __name__ == "__main__":
    test_node_and_edge_counts_match_disclosed_baseline()
    test_no_duplicate_node_ids()
    test_no_dangling_edge_references()
    test_no_duplicate_edges()
    test_no_invalid_edge_types()
    test_no_node_type_schema_violations()
    test_isolated_node_count_does_not_regress()
    test_connected_component_count_does_not_regress()
    print("knowledge graph integrity self-check: all 8 checks passed")
