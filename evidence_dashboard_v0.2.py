from collections import Counter, defaultdict

path = r"C:\Users\user\Desktop\faos\evidence_pilot_v0.2.psv"
lines = [l.rstrip("\n") for l in open(path, encoding="utf-8") if l.strip()]
rows = [l.split("|") for l in lines[1:]]

evidence = {}
grounds = defaultdict(list)
for r in rows:
    eid, etype, tier, citation, locator, grounded, indep, stance, quality = r
    evidence[eid] = {"type": etype, "tier": tier, "locator": locator, "indep": indep, "stance": stance, "quality": quality}
    for k in grounded.split(";"):
        grounds[k].append(eid)

TOTAL_KB = 299

n_evidence = len(evidence)
n_grounded = len(grounds)
avg_ev = sum(len(v) for v in grounds.values()) / n_grounded

tier_counts = Counter(e["tier"] for e in evidence.values())
verified_locators = sum(1 for e in evidence.values() if "WEB-VERIFIED" in e["locator"])
pending_locators = n_evidence - verified_locators

print("=== v0.2 DASHBOARD ===")
print(f"Total Evidence Objects: {n_evidence}")
print(f"Objects Grounded (Pilot Coverage): {n_grounded}/20")
print(f"Average Evidence per Object: {avg_ev:.2f}")
print(f"Primary: {tier_counts['Primary']} ({tier_counts['Primary']/n_evidence*100:.1f}%)")
print(f"Secondary: {tier_counts['Secondary']} ({tier_counts['Secondary']/n_evidence*100:.1f}%)")
print(f"Web-verified locators this round: {verified_locators}/{n_evidence}")
print(f"Locator Pending (carried from v0.1, not re-checked): {pending_locators}/{n_evidence}")

# independence
indep_yes = sum(1 for e in evidence.values() if e["indep"].startswith("Yes"))
print(f"Marked independent-of-prior-source: {indep_yes}/{n_evidence}")

single_sourced = [k for k,v in grounds.items() if len(v)==1]
print(f"\nSingle-sourced objects: {len(single_sourced)} -> {single_sourced}")

print(f"\nFull-KB Completeness: {n_grounded}/{TOTAL_KB} = {n_grounded/TOTAL_KB*100:.1f}%")

print("\n=== PER-OBJECT ===")
for k in sorted(grounds):
    n = len(grounds[k])
    tiers = [evidence[e]["tier"] for e in grounds[k]]
    print(f"  {k}: n={n} tiers={tiers}")
