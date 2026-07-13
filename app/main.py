"""
Flood Risk Priority Mapper -- Streamlit entrypoint.

Run with:
    streamlit run app/main.py
"""

import pandas as pd
import streamlit as st
from streamlit_folium import st_folium

from app.data.localities import load_localities
from app.map_utils import build_map
from app.scoring import DEFAULT_WEIGHTS, FACTOR_KEYS, score_localities

st.set_page_config(
    page_title="Flood Risk Priority Mapper",
    layout="wide",
    initial_sidebar_state="expanded",
)

FACTOR_LABELS = {
    "elevation": "Low elevation",
    "drainage": "Drain proximity & encroachment",
    "lakebed": "Former lake-bed",
    "density": "Population density",
}
FACTOR_DESCRIPTIONS = {
    "elevation": "Areas sitting in natural basins / low-lying terrain relative to surrounding wards.",
    "drainage": "Closeness to rajakaluves with reported siltation, narrowing, or encroachment.",
    "lakebed": "Built on or adjacent to historically filled lakes / tank beds.",
    "density": "People & structures exposed per sq. km.",
}

# --- Sidebar: city switcher + weight controls -------------------------------
st.sidebar.markdown("### City")
city = st.sidebar.selectbox(
    "City", ["Bengaluru", "Mumbai (coming soon)", "Chennai (coming soon)"],
    label_visibility="collapsed",
)
if city != "Bengaluru":
    st.sidebar.warning(f"{city.split(' (')[0]} data isn't loaded yet — showing Bengaluru.")

st.sidebar.markdown("### Scoring weights")
weights = {}
for key in FACTOR_KEYS:
    weights[key] = st.sidebar.slider(
        FACTOR_LABELS[key], 0, 100, DEFAULT_WEIGHTS[key], help=FACTOR_DESCRIPTIONS[key]
    )

total = sum(weights.values()) or 1
st.sidebar.caption(
    "Normalized: " + " · ".join(f"{FACTOR_LABELS[k].split()[0]} {round(weights[k]/total*100)}%" for k in FACTOR_KEYS)
)

if st.sidebar.button("Reset to default weights"):
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.markdown("**Priority tiers**")
st.sidebar.markdown(
    "🔴 Critical (75+) · 🟠 High (60-74) · 🟡 Medium (40-59) · 🟢 Low (<40)"
)

# --- Score + render -----------------------------------------------------------
localities = load_localities()
scored = score_localities(localities, weights)

st.title("Flood Risk Priority Mapper")
st.caption(
    "Intervention planning prototype — Bengaluru. "
    "Composite scores are illustrative estimates, not verified BBMP measurements."
)

col_map, col_table = st.columns([1.6, 1])

with col_map:
    fmap = build_map(scored)
    st_folium(fmap, use_container_width=True, height=620, returned_objects=[])

with col_table:
    st.markdown("#### Ranked localities")
    search = st.text_input("Filter by name", "")
    df = pd.DataFrame(scored)
    if search:
        df = df[df["name"].str.contains(search, case=False)]

    for i, row in df.reset_index(drop=True).iterrows():
        st.markdown(
            f"**#{i+1} {row['name']}** — {row['tier']} ({row['composite']})  \n"
            f"<span style='font-size:12px;color:#666'>{row['note']}</span>",
            unsafe_allow_html=True,
        )
        st.divider()

st.caption(
    "Data: illustrative composite estimates from public reporting patterns "
    "(BBMP flood-prone lists, lake-bed encroachment, drainage news) — not official measurements. "
    "See docs/architecture.md for the plan to swap in satellite, rainfall, and drain-vector data."
)
