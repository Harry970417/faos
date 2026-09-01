#!/usr/bin/env python
"""FAOS web viewer: Streamlit UI over the same data faos_query.py reads.

ponytail: reuses faos_query's read_psv/paths directly instead of a new data layer.
"""
import json
import streamlit as st
from faos_query import KB_PATH, EVIDENCE_PATH, CONFIRMATORY_JSON, PROTOCOL_LOCK_MD, read_psv

st.set_page_config(page_title="FAOS Viewer", layout="wide")
st.title("FAOS — Financial Research Knowledge Governance")

tab1, tab2, tab3, tab4 = st.tabs(
    ["Search Object", "Evidence Trace", "Protocol Timeline", "RP-001 Research Summary"]
)

with tab1:
    st.subheader("Search Knowledge Objects")
    term = st.text_input("Keyword (matches Name / Type / RootTaxonomy)", value="Momentum")
    if term:
        rows = read_psv(KB_PATH)
        t = term.lower()
        hits = [r for r in rows if t in r["Name"].lower() or t in r["Type"].lower()
                or t in r["RootTaxonomy"].lower()]
        st.write(f"{len(hits)} match(es)")
        for r in hits:
            with st.expander(f"[{r['ID']}] {r['Name']} ({r['Type']})"):
                st.json(r)

with tab2:
    st.subheader("Evidence Trace")
    eid = st.text_input("Evidence ID or grounded object ID", value="")
    if eid:
        rows = read_psv(EVIDENCE_PATH)
        hits = [r for r in rows if r["EvidenceID"] == eid
                or eid in (r["GroundedObjects"] or "").split(";")]
        if not hits:
            st.info(f"No Evidence Object found for '{eid}'.")
        for r in hits:
            st.markdown(f"**[{r['EvidenceID']}] {r['Type']}** ({r['Tier']}, quality={r['Quality']}, stance={r['Stance']})")
            st.write(f"Citation: {r['Citation']}")
            st.write(f"Grounds: {r['GroundedObjects']}")
    else:
        st.caption("Enter an Evidence ID (see Search tab for object IDs) to trace Hypothesis → Evidence → Result.")

with tab3:
    st.subheader("RP-001 Phase 2A Protocol Timeline")
    if not PROTOCOL_LOCK_MD.exists():
        st.info("No protocol lock record found.")
    else:
        text = PROTOCOL_LOCK_MD.read_text(encoding="utf-8")
        for line in text.splitlines():
            if line.startswith("**") and ":**" in line:
                st.write(line.strip("*").replace(":**", ":"))

with tab4:
    st.subheader("RP-001: Exploratory (50 stocks) vs Confirmatory (full-market)")
    with open(CONFIRMATORY_JSON, encoding="utf-8") as f:
        d = json.load(f)
    st.write(f"Confirmatory sample: **{d['confirmatory_sample_stocks']} stocks**, "
             f"{d['confirmatory_sample_rows']:,} rows (generated {d['generated_utc']})")

    def flatten(node, prefix=""):
        if isinstance(node, dict) and "label" in node:
            yield prefix, node
        elif isinstance(node, dict):
            for k, v in node.items():
                yield from flatten(v, f"{prefix}{k} / " if prefix else f"{k} / ")

    for h, horizons in d["results"].items():
        st.markdown(f"**{h}**")
        table = []
        for path, leaf in flatten(horizons):
            table.append({
                "path": path.rstrip(" /"),
                "n": leaf["n"],
                "mean_ic": round(leaf["mean_ic"], 4),
                "t_nw": round(leaf["t_nw"], 2),
                "raw_p": round(leaf["raw_p"], 3),
            })
        st.dataframe(table, use_container_width=True)
