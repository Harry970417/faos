import re
from collections import defaultdict, Counter
import random

path = r"C:\Users\user\Desktop\faos\knowledge_base_v0.2.psv"
with open(path, encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f if l.strip()]

rows = [l.split("|") for l in lines[1:]]
nodes = {}
for r in rows:
    nodes[r[0]] = {"name": r[1], "type": r[2], "root": r[3], "region": r[4], "maturity": r[5]}

EDGE_COLS = {"DependsOn": 6, "References": 7, "Implements": 8, "DerivedFrom": 9}

def parse_cell(cell):
    out = []
    if not cell:
        return out
    for token in cell.split(";"):
        token = token.strip()
        if not token:
            continue
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

print(f"=== BASIC ===")
print(f"Total nodes: {len(nodes)}")
print(f"Total edges: {len(edges)}")

missing_t = [(s,t,et) for (s,t,et,tag) in edges if t not in nodes]
missing_s = [(s,t,et) for (s,t,et,tag) in edges if s not in nodes]
selfloops = [(s,t,et) for (s,t,et,tag) in edges if s==t]
dupes = [k for k,v in Counter((s,t,et) for (s,t,et,tag) in edges).items() if v>1]
print(f"Missing targets: {missing_t or 'None'}")
print(f"Missing sources: {missing_s or 'None'}")
print(f"Self-loops: {selfloops or 'None'}")
print(f"Duplicate edges: {dupes or 'None'}")

# DAG check on validity-critical
validity_types = {"DependsOn","Implements","DerivedFrom"}
adj = defaultdict(list)
for (s,t,et,tag) in edges:
    if et in validity_types and t in nodes:
        adj[s].append(t)
WHITE,GRAY,BLACK=0,1,2
color = {n:WHITE for n in nodes}
cycles=[]
def dfs(u,path):
    color[u]=GRAY; path.append(u)
    for v in adj.get(u,[]):
        if color[v]==GRAY:
            idx=path.index(v); cycles.append(path[idx:]+[v])
        elif color[v]==WHITE:
            dfs(v,path)
    path.pop(); color[u]=BLACK
for n in nodes:
    if color[n]==WHITE: dfs(n,[])
print(f"DAG check: {'CYCLES: '+str(cycles) if cycles else 'No cycles - valid DAG'}")

print(f"\n=== OBJECT DISTRIBUTION ===")
print("By Type:", dict(Counter(n["type"] for n in nodes.values()).most_common()))
print("By Root:", dict(Counter(n["root"] for n in nodes.values()).most_common()))

print(f"\n=== RELATIONSHIP FREQUENCY ===")
et_counts = Counter(et for (s,t,et,tag) in edges)
print("By edge type:", dict(et_counts))
matrix = Counter()
for (s,t,et,tag) in edges:
    if s in nodes and t in nodes:
        matrix[(nodes[s]["type"], et, nodes[t]["type"])] += 1
print("Top 15 type-pairs:")
for k,v in matrix.most_common(15):
    print(f"  {v:3d}  {k[0]} --{k[1]}--> {k[2]}")

# semantic tag counts
tagcounts = Counter(tag.split(",")[0] for (s,t,et,tag) in edges if tag)
print("Semantic tags:", dict(tagcounts))

# degree distribution (undirected, all edges)
und = defaultdict(set)
indeg = Counter(); outdeg = Counter()
for (s,t,et,tag) in edges:
    if s in nodes: outdeg[s]+=1
    if t in nodes: indeg[t]+=1
    if s in nodes and t in nodes:
        und[s].add(t); und[t].add(s)

degrees = {n: len(und[n]) for n in nodes}
print(f"\n=== DEGREE DISTRIBUTION (undirected) ===")
deg_hist = Counter(degrees.values())
for d in sorted(deg_hist):
    print(f"  degree {d}: {deg_hist[d]} objects")
print(f"Mean degree: {sum(degrees.values())/len(degrees):.2f}")
print(f"Max degree: {max(degrees.values())}")
isolated = [n for n,d in degrees.items() if d==0]
print(f"Isolated objects: {len(isolated)} -> {isolated}")

print(f"\n=== TOP 15 BY DEGREE CENTRALITY (undirected degree) ===")
top_deg = sorted(degrees.items(), key=lambda x:-x[1])[:15]
for n,d in top_deg:
    print(f"  {d:3d}  {n:6s} {nodes[n]['name']} [{nodes[n]['type']}]")

# Betweenness centrality (Brandes, unweighted, undirected)
def brandes_betweenness(adj_undirected, node_list):
    C = {v:0.0 for v in node_list}
    for s in node_list:
        S=[]
        P={v:[] for v in node_list}
        sigma={v:0 for v in node_list}; sigma[s]=1
        d={v:-1 for v in node_list}; d[s]=0
        Q=[s]
        qi=0
        while qi < len(Q):
            v=Q[qi]; qi+=1
            S.append(v)
            for w in adj_undirected[v]:
                if d[w] < 0:
                    Q.append(w); d[w]=d[v]+1
                if d[w]==d[v]+1:
                    sigma[w]+=sigma[v]
                    P[w].append(v)
        delta={v:0.0 for v in node_list}
        while S:
            w=S.pop()
            for v in P[w]:
                delta[v] += (sigma[v]/sigma[w])*(1+delta[w])
            if w!=s:
                C[w]+=delta[w]
    for v in C:
        C[v] /= 2.0
    return C

node_list = list(nodes.keys())
btw = brandes_betweenness(und, node_list)
print(f"\n=== TOP 15 BY BETWEENNESS CENTRALITY ===")
top_btw = sorted(btw.items(), key=lambda x:-x[1])[:15]
for n,b in top_btw:
    print(f"  {b:8.2f}  {n:6s} {nodes[n]['name']} [{nodes[n]['type']}]")

# Community structure: connected components + label propagation within giant component
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
print(f"\n=== CONNECTED COMPONENTS ===")
print(f"Number of components: {len(comps)}")
print(f"Largest component size: {len(comps[0])} ({len(comps[0])/len(nodes)*100:.1f}% of graph)")
print(f"Component sizes: {sorted([len(c) for c in comps], reverse=True)[:20]}")
isolated_comps = [c for c in comps if len(c)==1]
print(f"Fully isolated objects: {len(isolated_comps)}")

# label propagation on giant component
random.seed(42)
giant = comps[0]
labels = {n:n for n in giant}
for _ in range(50):
    order = list(giant); random.shuffle(order)
    changed=False
    for n in order:
        neighbor_labels = Counter(labels[v] for v in und[n] if v in giant)
        if not neighbor_labels: continue
        maxc = max(neighbor_labels.values())
        best = [l for l,c in neighbor_labels.items() if c==maxc]
        newlabel = sorted(best)[0] if labels[n] not in best else labels[n]
        if newlabel != labels[n]:
            labels[n]=newlabel; changed=True
    if not changed: break

communities = defaultdict(list)
for n,l in labels.items():
    communities[l].append(n)
comm_sizes = sorted([len(v) for v in communities.values()], reverse=True)
print(f"\n=== COMMUNITY STRUCTURE (label propagation, giant component only) ===")
print(f"Communities found: {len(communities)}")
print(f"Community sizes (top 10): {comm_sizes[:10]}")
big_comms = sorted(communities.items(), key=lambda x: -len(x[1]))[:6]
for label, members in big_comms:
    roots = Counter(nodes[m]["root"] for m in members)
    types = Counter(nodes[m]["type"] for m in members)
    print(f"  Community (n={len(members)}): dominant roots={roots.most_common(3)}, dominant types={types.most_common(3)}")
