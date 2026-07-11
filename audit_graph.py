import re
from collections import defaultdict, Counter

path = r"C:\Users\user\Desktop\faos\knowledge_seed_v0.1.psv"
with open(path, encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]

header = lines[0].split("|")
rows = [l.split("|") for l in lines[1:]]

nodes = {}
for r in rows:
    rid = r[0]
    nodes[rid] = {
        "name": r[1], "type": r[2], "root": r[3], "region": r[4], "maturity": r[5]
    }

EDGE_COLS = {"DependsOn": 6, "References": 7, "Implements": 8, "DerivedFrom": 9}

def parse_cell(cell):
    # split on ; then extract id and optional (tag)
    out = []
    if not cell:
        return out
    for token in cell.split(";"):
        token = token.strip()
        if not token:
            continue
        m = re.match(r"([A-Za-z0-9]+)(\((.*)\))?", token)
        tid = m.group(1)
        tag = m.group(3) if m.group(3) else ""
        out.append((tid, tag))
    return out

edges = []  # (source, target, edge_type, tag)
for r in rows:
    src = r[0]
    for et, idx in EDGE_COLS.items():
        cell = r[idx] if idx < len(r) else ""
        for tid, tag in parse_cell(cell):
            edges.append((src, tid, et, tag))

print(f"Total nodes: {len(nodes)}")
print(f"Total edges: {len(edges)}")

# 1. Integrity: missing targets
missing = [(s,t,et) for (s,t,et,tag) in edges if t not in nodes]
print(f"\n--- Missing target IDs ---\n{missing if missing else 'None'}")

missing_src = [(s,t,et) for (s,t,et,tag) in edges if s not in nodes]
print(f"--- Missing source IDs ---\n{missing_src if missing_src else 'None'}")

# self loops
selfloops = [(s,t,et) for (s,t,et,tag) in edges if s == t]
print(f"\n--- Self-loops ---\n{selfloops if selfloops else 'None'}")

# duplicate edges (same s,t,et more than once)
edge_key_counts = Counter((s,t,et) for (s,t,et,tag) in edges)
dupes = [k for k,v in edge_key_counts.items() if v > 1]
print(f"\n--- Duplicate edges (same source,target,type) ---\n{dupes if dupes else 'None'}")

# direction inconsistency: A->B and B->A on same edge type (immediate 2-cycles)
edge_set = set((s,t,et) for (s,t,et,tag) in edges)
two_cycles = []
for (s,t,et) in edge_set:
    if (t,s,et) in edge_set and s != t:
        pair = tuple(sorted([s,t]))
        two_cycles.append((pair, et))
two_cycles = sorted(set(two_cycles))
print(f"\n--- Immediate 2-cycles (A->B and B->A, same edge type) ---\n{two_cycles if two_cycles else 'None'}")

# DAG check on validity-critical edges: DependsOn, Implements, DerivedFrom
validity_types = {"DependsOn", "Implements", "DerivedFrom"}
adj = defaultdict(list)
for (s,t,et,tag) in edges:
    if et in validity_types:
        adj[s].append(t)

WHITE, GRAY, BLACK = 0,1,2
color = {n: WHITE for n in nodes}
cycle_paths = []

def dfs(u, path):
    color[u] = GRAY
    path.append(u)
    for v in adj.get(u, []):
        if v not in nodes:
            continue
        if color[v] == GRAY:
            # found cycle: path from v to u, plus back to v
            idx = path.index(v)
            cycle_paths.append(path[idx:] + [v])
        elif color[v] == WHITE:
            dfs(v, path)
    path.pop()
    color[u] = BLACK

for n in nodes:
    if color[n] == WHITE:
        dfs(n, [])

print(f"\n--- DAG check on validity-critical edges (DependsOn+Implements+DerivedFrom) ---")
if cycle_paths:
    print(f"CYCLES FOUND: {cycle_paths}")
else:
    print("No cycles. Graph is a valid DAG.")

# 2. Connectivity - undirected, ALL edge types combined
und_adj = defaultdict(set)
for (s,t,et,tag) in edges:
    if s in nodes and t in nodes:
        und_adj[s].add(t)
        und_adj[t].add(s)

visited = set()
components = []
for n in nodes:
    if n not in visited:
        stack = [n]
        comp = set()
        while stack:
            u = stack.pop()
            if u in comp:
                continue
            comp.add(u)
            visited.add(u)
            for v in und_adj.get(u, []):
                if v not in comp:
                    stack.append(v)
        components.append(comp)

components.sort(key=len, reverse=True)
print(f"\n--- Connected components (undirected, all edge types) ---")
print(f"Number of components: {len(components)}")
print(f"Largest component size: {len(components[0])}")
print(f"Component sizes: {sorted([len(c) for c in components], reverse=True)}")
isolated = [c for c in components if len(c) == 1]
print(f"Isolated objects (degree 0, count={len(isolated)}): {sorted([list(c)[0] for c in isolated])}")

# in-degree / out-degree (directed, all edge types combined)
indeg = Counter()
outdeg = Counter()
for (s,t,et,tag) in edges:
    if s in nodes:
        outdeg[s]+=1
    if t in nodes:
        indeg[t]+=1

zero_in = sorted([n for n in nodes if indeg[n]==0])
zero_out = sorted([n for n in nodes if outdeg[n]==0])
print(f"\nIn-degree = 0 count: {len(zero_in)} -> {zero_in}")
print(f"Out-degree = 0 count: {len(zero_out)} -> {zero_out}")

fully_connected = (len(components) == 1)
print(f"\nIs the WHOLE graph connected (ignoring direction)? {fully_connected}")

# 3. Type-pair matrix
matrix = Counter()
for (s,t,et,tag) in edges:
    if s in nodes and t in nodes:
        st = nodes[s]["type"]
        tt = nodes[t]["type"]
        matrix[(st, et, tt, tag.split(",")[0] if tag else "")] += 1

print(f"\n--- Type-Pair Matrix (SourceType -> EdgeType -> TargetType [tag]) ---")
for k,v in sorted(matrix.items(), key=lambda x: -x[1]):
    print(f"{v:2d}  {k[0]} --{k[1]}--> {k[2]}   tag={k[3]}")
