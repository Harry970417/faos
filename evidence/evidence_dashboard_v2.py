from collections import Counter, defaultdict

path = r"C:\Users\user\Desktop\faos\evidence_pilot_v0.1.psv"
lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
rows = [l.split("|") for l in lines[1:]]

evidence = {}
grounds = defaultdict(list)  # knowledge_obj_id -> [evidence_ids]
for r in rows:
    eid, etype, tier, citation, grounded, quality = r
    evidence[eid] = {"type": etype, "tier": tier, "citation": citation, "quality": quality}
    for k in grounded.split(";"):
        grounds[k].append(eid)

TOTAL_KB_OBJECTS = 299

n_evidence = len(evidence)
n_grounded_objects = len(grounds)
avg_evidence_per_grounded = sum(len(v) for v in grounds.values()) / n_grounded_objects

tier_counts = Counter(e["tier"] for e in evidence.values())
type_counts = Counter(e["type"] for e in evidence.values())
quality_counts = Counter(e["quality"] for e in evidence.values())

# journal/publisher diversity (rough proxy: distinct venue after last comma before year, using citation text)
venues = set()
for e in evidence.values():
    c = e["citation"]
    # crude venue extraction: text after the year+period, up to first period
    parts = c.split(". ")
    if len(parts) >= 3:
        venues.add(parts[2].split(",")[0].split(".")[0])

print("=== EVIDENCE COVERAGE ===")
print(f"Total Knowledge Objects: {TOTAL_KB_OBJECTS}")
print(f"Total Evidence Objects: {n_evidence}")
print(f"Knowledge Objects with >=1 Evidence: {n_grounded_objects}")
print(f"Coverage %: {n_grounded_objects/TOTAL_KB_OBJECTS*100:.1f}%")
print(f"Average Evidence per Grounded Object: {avg_evidence_per_grounded:.2f}")
print(f"Unsourced Objects: {TOTAL_KB_OBJECTS - n_grounded_objects} ({(TOTAL_KB_OBJECTS-n_grounded_objects)/TOTAL_KB_OBJECTS*100:.1f}%)")

print("\n=== EVIDENCE QUALITY ===")
print(f"Quality distribution: {dict(quality_counts)}")
print(f"High-quality ratio: {quality_counts['High']/n_evidence*100:.1f}%")

print("\n=== EVIDENCE DIVERSITY ===")
print(f"Tier distribution: {dict(tier_counts)}")
print(f"  Primary ratio: {tier_counts['Primary']/n_evidence*100:.1f}%")
print(f"  Secondary ratio: {tier_counts['Secondary']/n_evidence*100:.1f}%")
print(f"Type distribution: {dict(type_counts)}")
print(f"  Distinct types used: {len(type_counts)} of 7 defined")
print(f"Distinct venues/publishers (approx): {len(venues)}")

print("\n=== PER-OBJECT DETAIL ===")
for k in sorted(grounds):
    tiers = [evidence[e]["tier"] for e in grounds[k]]
    print(f"  {k}: {len(grounds[k])} evidence ({', '.join(tiers)})")

single_source = [k for k,v in grounds.items() if len(v)==1]
print(f"\nObjects with only 1 evidence source (triangulation risk): {len(single_source)} -> {single_source}")
