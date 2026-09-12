# -*- coding: utf-8 -*-
"""Regenerate faos_knowledge_graph as vector SVG (native-shape reconstruction of
109 nodes/129 edges is impractical -- explicit high-density exception per spec).
Identical logic/data to generate_charts.py's section 1, only the output format differs."""
import csv
from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).parent
OUT = Path(r"C:\Users\user\Desktop\推甄資料最新版\99_暫存")


def read_psv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


rows = read_psv(ROOT / "knowledge" / "knowledge_base_v0.2.psv")
G = nx.DiGraph()
for r in rows:
    G.add_node(r["ID"], type=r["Type"], name=r["Name"])
    for col in ["DependsOn", "References", "Implements", "DerivedFrom"]:
        for target in (r[col] or "").split(";"):
            target = target.split("(")[0].strip()
            if target and target in [x["ID"] for x in rows]:
                G.add_edge(r["ID"], target, kind=col)

core_nodes = [n for n, d in G.degree() if d >= 2]
Gc = G.subgraph(core_nodes).copy()
fig, ax = plt.subplots(figsize=(14, 11))
pos = nx.spring_layout(Gc, seed=42, k=0.6)
type_colors = {"Concept": "#4C72B0", "Theory": "#DD8452", "Model": "#55A868",
               "Formula": "#C44E52", "Metric": "#8172B2", "Framework": "#937860",
               "Assumption": "#DA8BC3", "Procedure": "#8C8C8C", "Pattern": "#CCB974",
               "Standard": "#64B5CD", "Factor": "#4C4C4C"}
type_labels_zh = {"Concept": "概念", "Theory": "理論", "Model": "模型",
                   "Formula": "公式", "Metric": "指標", "Framework": "框架",
                   "Assumption": "假設", "Procedure": "流程", "Pattern": "樣式",
                   "Standard": "標準", "Factor": "因子"}
node_colors = [type_colors.get(G.nodes[n].get("type"), "#999999") for n in Gc.nodes()]
nx.draw_networkx_edges(Gc, pos, alpha=0.3, arrows=True, arrowsize=8, ax=ax)
nx.draw_networkx_nodes(Gc, pos, node_color=node_colors, node_size=260, ax=ax)
nx.draw_networkx_labels(Gc, pos, font_size=6, ax=ax)
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=9, label=type_labels_zh[t])
           for t, c in type_colors.items() if t in [G.nodes[n]["type"] for n in Gc.nodes()]]
ax.legend(handles=handles, loc="upper left", fontsize=8, title="物件類型")
ax.set_title(f"FAOS 知識圖譜（核心子圖：degree>=2 節點，{len(Gc.nodes())}/{len(G.nodes())} 個，"
             f"{len(Gc.edges())}/{len(G.edges())} 條真實關係邊；僅示意整體規模，非用於逐node閱讀）", fontsize=14)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "faos_knowledge_graph.svg", format="svg")
plt.close(fig)
print("SVG written:", OUT / "faos_knowledge_graph.svg")
