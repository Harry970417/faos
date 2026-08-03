import re

path = r"C:\Users\user\Desktop\faos\knowledge_base_remediated_v0.1.psv"
with open(path, encoding="utf-8") as f:
    lines = [l.rstrip("\n") for l in f]

header = lines[0]
rows = {}
order = []
for l in lines[1:]:
    if not l.strip():
        continue
    parts = l.split("|")
    while len(parts) < 10:
        parts.append("")
    rows[parts[0]] = parts
    order.append(parts[0])

# 1. Remove duplicate/near-duplicate objects (all isolated, no redirects needed)
REMOVE = ["A04", "A09", "PR11"]
for rid in REMOVE:
    assert rid in rows, rid
    del rows[rid]
order = [r for r in order if r not in REMOVE]

def add(rid, col, target):
    """col: 6=DependsOn 7=References 8=Implements 9=DerivedFrom"""
    cell = rows[rid][col]
    existing = [t.strip() for t in cell.split(";") if t.strip()]
    ids = [re.match(r"[A-Za-z0-9]+", e).group(0) for e in existing]
    if target in ids:
        return
    existing.append(target)
    rows[rid][col] = ";".join(existing)

DEP, REF = 6, 7

# --- Missing Expected Relationships (existing objects only) ---
add("M02",DEP,"A05"); add("M02",DEP,"A06")
add("T03",DEP,"A08"); add("T03",DEP,"A14")
add("T24",DEP,"A12")
add("PR31",DEP,"A16")
add("M09",REF,"C12")
add("M02",REF,"C25")
add("PR20",REF,"C26")
add("PR09",REF,"C27")
add("PR28",REF,"C34")
add("M17",REF,"C47")
add("PR10",REF,"C49")
for c in ["C52","C53","C54","C55"]:
    add("S01",REF,c)
add("T07",REF,"C56")
add("ME18",REF,"C65")
add("PR17",REF,"C20"); add("PR17",REF,"C63")
add("ME22",REF,"C22")
add("ME35",REF,"PR05")
add("ME38",REF,"PR05")
add("ME43",DEP,"ME41"); add("ME43",DEP,"ME42")

# --- Additional existing-object connections for Standards / Frameworks (no new objects) ---
for c in ["C52","C53","C54","C55"]:
    add("S02",REF,c)
add("S07",REF,"C54")
add("S10",REF,"C20"); add("S10",REF,"C63")
add("S11",REF,"C26")
add("S12",REF,"C53"); add("S12",REF,"C54")
add("S13",REF,"C26"); add("S13",REF,"C27")
add("S14",REF,"C54")
add("S15",REF,"C01")
add("FR02",REF,"C42")
add("C42",REF,"C08")
add("FR09",REF,"C03")
add("FR11",REF,"C19")

with open(path, "w", encoding="utf-8") as f:
    f.write(header + "\n")
    for rid in order:
        f.write("|".join(rows[rid]) + "\n")

print(f"Done. {len(order)} objects remain (removed {len(REMOVE)}).")
