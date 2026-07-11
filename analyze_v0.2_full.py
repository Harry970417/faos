import re
from collections import defaultdict, Counter

path = r"C:\Users\user\Desktop\faos\knowledge_base_v0.2.psv"
with open(path, encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]
rows = [l.split("|") for l in lines[1:]]
nodes = {r[0]: {"name": r[1], "type": r[2], "root": r[3], "region": r[4], "maturity": r[5]} for r in rows}

EDGE_COLS = {"DependsOn": 6, "References": 7, "Implements": 8, "DerivedFrom": 9}
def parse_cell(cell):
    out = []
    if not cell: return out
    for token in cell.split(";"):
        token = token.strip()
        if not token: continue
        m = re.match(r"([A-Za-z0-9]+)(\((.*)\))?", token)
        out.append((m.group(1), m.group(3) or ""))
    return out

edges = []
for r in rows:
    src = r[0]
    for et, idx in EDGE_COLS.items():
        cell = r[idx] if idx < len(r) else ""
        for tid, tag in parse_cell(cell):
            edges.append((src, tid, et, tag))

print("=== PART A: RELATIONSHIP CANDIDATE DETAIL ===\n")

def candidate_detail(tagname):
    inst = [(s,t,et) for (s,t,et,tag) in edges if tag.split(",")[0]==tagname]
    print(f"--- {tagname} ---")
    print(f"Count: {len(inst)}")
    pairs = Counter((nodes[s]["type"], nodes[t]["type"]) for s,t,et in inst)
    print(f"Source->Target type distribution: {dict(pairs)}")
    print(f"Native edge column used: {Counter(et for s,t,et in inst)}")
    for s,t,et in inst:
        print(f"    {s}({nodes[s]['type']}) -> {t}({nodes[t]['type']})  [{nodes[s]['name']} -> {nodes[t]['name']}]")
    print()
    return inst

ev = candidate_detail("semantic-evaluatedby")
ext = candidate_detail("semantic-extends")
impl = candidate_detail("semantic-standardimpl")
f1 = candidate_detail("informal-F1")

# check for untagged recurring patterns (candidates not yet named)
print("--- Untagged type-pairs (potential unnamed candidates) ---")
untagged = Counter((nodes[s]["type"], et, nodes[t]["type"]) for (s,t,et,tag) in edges if not tag)
for k,v in untagged.most_common(30):
    print(f"  {v:3d}  {k[0]} --{k[1]}--> {k[2]}")

print("\n\n=== PART B: CONNECTIVITY ===\n")

und = defaultdict(set)
for (s,t,et,tag) in edges:
    if s in nodes and t in nodes:
        und[s].add(t); und[t].add(s)

degrees = {n: len(und[n]) for n in nodes}
isolated = [n for n,d in degrees.items() if d==0]
print(f"Isolated count: {len(isolated)}")

# isolated rate by root and type
by_root_total = Counter(n["root"] for n in nodes.values())
by_root_iso = Counter(nodes[n]["root"] for n in isolated)
print("\nIsolated rate by Root:")
for root in by_root_total:
    tot = by_root_total[root]; iso = by_root_iso.get(root,0)
    print(f"  {root:40s} {iso}/{tot} = {iso/tot*100:.1f}%")

by_type_total = Counter(n["type"] for n in nodes.values())
by_type_iso = Counter(nodes[n]["type"] for n in isolated)
print("\nIsolated rate by Type:")
for typ in by_type_total:
    tot = by_type_total[typ]; iso = by_type_iso.get(typ,0)
    print(f"  {typ:12s} {iso}/{tot} = {iso/tot*100:.1f}%")

# connected components with full root/type composition
visited=set(); comps=[]
for n in nodes:
    if n not in visited:
        stack=[n]; comp=set()
        while stack:
            u=stack.pop()
            if u in comp: continue
            comp.add(u); visited.add(u)
            for v in und[u]:
                if v not in comp: stack.append(v)
        comps.append(comp)
comps.sort(key=len, reverse=True)
print(f"\nComponents (excluding singletons), with Root/Type composition:")
for c in comps:
    if len(c) > 1:
        roots = Counter(nodes[m]["root"] for m in c)
        types = Counter(nodes[m]["type"] for m in c)
        print(f"  n={len(c):3d}  roots={dict(roots.most_common(3))}  types={dict(types.most_common(3))}  members={sorted(c) if len(c)<=9 else str(sorted(c)[:9])+'...'}")

# articulation points and bridges (Tarjan)
adjlist = {n: list(und[n]) for n in nodes}
visited2 = {}
disc = {}
low = {}
parent = {}
ap = set()
bridges = []
timer = [0]

import sys
sys.setrecursionlimit(10000)

def tarjan(u):
    visited2[u] = True
    disc[u] = low[u] = timer[0]; timer[0]+=1
    children = 0
    for v in adjlist[u]:
        if v not in visited2:
            parent[v] = u
            children += 1
            tarjan(v)
            low[u] = min(low[u], low[v])
            if low[v] > disc[u]:
                bridges.append((u,v))
            if parent.get(u) is not None and low[v] >= disc[u]:
                ap.add(u)
            if parent.get(u) is None and children > 1:
                ap.add(u)
        elif v != parent.get(u):
            low[u] = min(low[u], disc[v])

for n in nodes:
    if n not in visited2:
        parent[n] = None
        tarjan(n)

print(f"\nArticulation points: {len(ap)} -> {sorted(ap)}")
print(f"Bridge edges: {len(bridges)}")
for u,v in bridges:
    print(f"    {u}({nodes[u]['name']}) -- {v}({nodes[v]['name']})")

giant = comps[0]
print(f"\nGiant component size: {len(giant)} / {len(nodes)} = {len(giant)/len(nodes)*100:.1f}%")
print("\nMost efficient reconnection targets (non-giant components, by size):")
for c in comps[1:]:
    if len(c) >= 2:
        roots = Counter(nodes[m]["root"] for m in c)
        print(f"  component n={len(c)}, root(s)={dict(roots)}, members={sorted(c)}  -> connecting with 1 edge adds {len(c)} nodes to giant, new share={((len(giant)+len(c))/len(nodes))*100:.1f}%")
