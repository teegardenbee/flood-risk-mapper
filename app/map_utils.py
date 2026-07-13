"""
Map rendering helpers.

Uses Folium, which generates a Leaflet map under the hood -- but the app
never hand-writes JS. All logic (colors, sizing, popups) is plain Python,
computed server-side, and only the final rendered map is sent to the
browser.
"""

import folium

from app.scoring import ScoredLocality

TIER_COLORS = {
    "Critical": "#C1442B",
    "High": "#E0842E",
    "Medium": "#D9B23C",
    "Low": "#2E8B7A",
}


def build_map(scored: list[ScoredLocality], center=(12.9716, 77.6412), zoom=11.4) -> folium.Map:
    fmap = folium.Map(
        location=center,
        zoom_start=zoom,
        tiles="CartoDB positron",
        control_scale=True,
    )

    for rank, row in enumerate(scored, start=1):
        color = TIER_COLORS[row["tier"]]
        radius = 8 + (row["composite"] / 100) * 14

        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 190px;">
          <b>#{rank} {row['name']}</b><br>
          Composite score: <b>{row['composite']}</b> ({row['tier']})<br>
          <span style="font-size:11.5px; color:#555;">
            Elevation: {row['elevation']} &middot; Drainage: {row['drainage']}<br>
            Lake-bed: {row['lakebed']} &middot; Density: {row['density']}
          </span><br>
          <span style="font-size:11.5px; color:#777;">{row['note']}</span>
        </div>
        """

        folium.CircleMarker(
            location=(row["lat"], row["lng"]),
            radius=radius,
            color="#12324f",
            weight=1.2,
            fill=True,
            fill_color=color,
            fill_opacity=0.75,
            popup=folium.Popup(popup_html, max_width=260),
            tooltip=f"#{rank} {row['name']} — {row['composite']}",
        ).add_to(fmap)

    return fmap
