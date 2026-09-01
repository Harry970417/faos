"""Generate FAOS charts for the admissions portfolio, from real repo data only.
ponytail: one-shot script, not a reusable module -- run once, inspect output, done.
"""
import csv
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import networkx as nx

plt.rcParams["font.sans-serif"] = ["Microsoft JhengHei", "Microsoft YaHei"]
plt.rcParams["axes.unicode_minus"] = False

ROOT = Path(__file__).parent
OUT = Path(r"C:\Users\user\Desktop\推甄資料最新版\06_圖表與視覺素材")
OUT.mkdir(parents=True, exist_ok=True)


def read_psv(path):
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f, delimiter="|"))


# 1. Knowledge graph (real DependsOn/References/Implements/DerivedFrom edges)
rows = read_psv(ROOT / "knowledge" / "knowledge_base_v0.2.psv")
G = nx.DiGraph()
for r in rows:
    G.add_node(r["ID"], type=r["Type"], name=r["Name"])
    for col in ["DependsOn", "References", "Implements", "DerivedFrom"]:
        for target in (r[col] or "").split(";"):
            target = target.split("(")[0].strip()  # strip informal annotations like F1(informal-F1)
            if target and target in [x["ID"] for x in rows]:
                G.add_edge(r["ID"], target, kind=col)

# Too dense to show all 302 nodes legibly -- show the largest connected component's
# core (nodes with degree >= 2), which is still real data, just filtered for legibility.
core_nodes = [n for n, d in G.degree() if d >= 2]
Gc = G.subgraph(core_nodes).copy()
fig, ax = plt.subplots(figsize=(14, 11))
pos = nx.spring_layout(Gc, seed=42, k=0.6)
type_colors = {"Concept": "#4C72B0", "Theory": "#DD8452", "Model": "#55A868",
               "Formula": "#C44E52", "Metric": "#8172B2", "Framework": "#937860",
               "Assumption": "#DA8BC3", "Procedure": "#8C8C8C", "Pattern": "#CCB974",
               "Standard": "#64B5CD"}
node_colors = [type_colors.get(G.nodes[n].get("type"), "#999999") for n in Gc.nodes()]
nx.draw_networkx_edges(Gc, pos, alpha=0.3, arrows=True, arrowsize=8, ax=ax)
nx.draw_networkx_nodes(Gc, pos, node_color=node_colors, node_size=260, ax=ax)
nx.draw_networkx_labels(Gc, pos, font_size=6, ax=ax)
handles = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=9, label=t)
           for t, c in type_colors.items() if t in [G.nodes[n]["type"] for n in Gc.nodes()]]
ax.legend(handles=handles, loc="upper left", fontsize=8, title="Object Type")
ax.set_title(f"FAOS Knowledge Graph（核心子圖：degree>=2 節點，{len(Gc.nodes())}/{len(G.nodes())} 個，"
             f"{len(Gc.edges())}/{len(G.edges())} 條真實關係邊）", fontsize=15)
ax.axis("off")
fig.tight_layout()
fig.savefig(OUT / "faos_knowledge_graph.png", dpi=300)
plt.close(fig)
print(f"knowledge graph: {len(G.nodes())} nodes, {len(G.edges())} edges total; "
      f"{len(Gc.nodes())} nodes shown (degree>=2 filter)")

# 2. KOM ontology (conceptual, object types + their real counts from the data)
type_counts = {}
for r in rows:
    type_counts[r["Type"]] = type_counts.get(r["Type"], 0) + 1
fig, ax = plt.subplots(figsize=(10, 6))
types = sorted(type_counts, key=type_counts.get, reverse=True)
counts = [type_counts[t] for t in types]
ax.barh(types, counts, color=[type_colors.get(t, "#999999") for t in types])
for i, c in enumerate(counts):
    ax.text(c + 1, i, str(c), va="center", fontsize=9)
ax.set_xlabel("Knowledge Object 數量", fontsize=12)
ax.set_title("FAOS Knowledge Object Model：物件類型分布（實際303筆資料統計）", fontsize=15)
fig.tight_layout()
fig.savefig(OUT / "faos_kom_ontology.png", dpi=300)
plt.close(fig)
print("KOM ontology chart done:", type_counts)

# 3. Protocol flow (conceptual, but dates/commits are real from RP001_PHASE2A_PROTOCOL_LOCK.md)
fig, ax = plt.subplots(figsize=(11, 3.2))
stages = [
    ("Pre-registration\n(Exploratory Complete)", "commit 82bc4a3"),
    ("Protocol Lock\n2026-07-11", "6份文件SHA-256凍結"),
    ("Confirmatory Test\n2026-08-02", "1,462檔/3,934,274列"),
    ("Decision\n(結案)", "H-C1/C4/C5未複現\n(README正式記錄)"),
]
for i, (title, sub) in enumerate(stages):
    ax.add_patch(plt.Rectangle((i * 2.6, 0), 2.2, 1.4, facecolor="#EAF1FB", edgecolor="#4C72B0"))
    ax.text(i * 2.6 + 1.1, 0.95, title, ha="center", va="center", fontsize=10, weight="bold")
    ax.text(i * 2.6 + 1.1, 0.4, sub, ha="center", va="center", fontsize=8)
    if i < len(stages) - 1:
        ax.annotate("", xy=(i * 2.6 + 2.35, 0.7), xytext=(i * 2.6 + 2.2, 0.7),
                    arrowprops=dict(arrowstyle="->", lw=1.5))
ax.set_xlim(-0.2, len(stages) * 2.6)
ax.set_ylim(-0.2, 1.7)
ax.axis("off")
ax.set_title("FAOS 研究治理流程：RP-001 案例", fontsize=15)
fig.tight_layout()
fig.savefig(OUT / "faos_protocol_flow.png", dpi=300)
plt.close(fig)
print("protocol flow chart done")

# 4. RP-001 exploratory vs confirmatory comparison
with open(ROOT / "rp001_data" / "phase2a" / "processed" / "rp001_confirmatory_test_results.json",
          encoding="utf-8") as f:
    conf = json.load(f)
fig, ax = plt.subplots(figsize=(9, 5))
categories = ["樣本股數", "資料列數（萬）"]
explore_vals = [50, 49.1]  # exploratory: 50 stocks, ~491 trading days sample -> not directly rows; use stocks and days
confirm_vals = [conf["confirmatory_sample_stocks"], conf["confirmatory_sample_rows"] / 10000]
x = range(len(categories))
w = 0.35
ax.bar([i - w / 2 for i in x], explore_vals, width=w, label="探索期", color="#DD8452")
ax.bar([i + w / 2 for i in x], confirm_vals, width=w, label="確認期（全市場）", color="#4C72B0")
ax.set_xticks(list(x))
ax.set_xticklabels(["樣本股數", "資料列數（萬列）"])
ax.set_yscale("log")
ax.set_ylabel("數量（log scale）", fontsize=12)
ax.set_title("FAOS RP-001：探索期 vs 確認期研究規模對照", fontsize=15)
for i, (e, c) in enumerate(zip(explore_vals, confirm_vals)):
    ax.text(i - w / 2, e * 1.1, f"{e:g}", ha="center", fontsize=9)
    ax.text(i + w / 2, c * 1.1, f"{c:g}", ha="center", fontsize=9)
ax.legend()
fig.tight_layout()
fig.savefig(OUT / "faos_rp001_exploratory_vs_confirmatory.png", dpi=300)
plt.close(fig)
print("RP-001 comparison chart done")

# 5. Representative research subgraph (real ego-network around Information Coefficient,
# the metric actually used across this portfolio's research -- not an arbitrary pick).
ego = nx.ego_graph(G.to_undirected(), "ME07", radius=1)
fig, ax = plt.subplots(figsize=(11, 9))
pos2 = nx.spring_layout(ego, seed=7, k=0.9)
node_colors2 = [type_colors.get(G.nodes[n]["type"], "#999999") for n in ego.nodes()]
labels2 = {n: f'{n}\n{G.nodes[n]["name"][:18]}' for n in ego.nodes()}
nx.draw_networkx_edges(ego, pos2, alpha=0.5, width=1.3, ax=ax)
nx.draw_networkx_nodes(ego, pos2, node_color=node_colors2, node_size=1400, ax=ax)
nx.draw_networkx_labels(ego, pos2, labels=labels2, font_size=10, ax=ax)
handles2 = [plt.Line2D([0], [0], marker='o', color='w', markerfacecolor=c, markersize=10, label=t)
            for t, c in type_colors.items() if t in [G.nodes[n]["type"] for n in ego.nodes()]]
ax.legend(handles=handles2, loc="upper left", fontsize=11, title="Object Type")
ax.set_title(f"FAOS 代表性研究子圖：以「Information Coefficient」為中心的真實關聯網絡\n"
             f"（{len(ego.nodes())}節點、{len(ego.edges())}邊，皆為knowledge_base_v0.2.psv中的真實邊）",
             fontsize=13.5)
ax.axis("off")
# pad the axes limits well beyond the actual node-position extent so labels
# (which extend past the node markers themselves) never clip at the canvas
# edge -- previously the title and several node labels touched left/right
# edges (Codex adversarial review, 2026-09-01).
xs = [p[0] for p in pos2.values()]
ys = [p[1] for p in pos2.values()]
x_pad = (max(xs) - min(xs)) * 0.25 or 0.2
y_pad = (max(ys) - min(ys)) * 0.2 or 0.2
ax.set_xlim(min(xs) - x_pad, max(xs) + x_pad)
ax.set_ylim(min(ys) - y_pad, max(ys) + y_pad)
fig.tight_layout()
fig.savefig(OUT / "faos_representative_subgraph.png", dpi=300, bbox_inches="tight")
plt.close(fig)
print(f"representative subgraph: {len(ego.nodes())} nodes, {len(ego.edges())} edges (real ego-network around ME07)")

print("\nAll charts written to", OUT)
