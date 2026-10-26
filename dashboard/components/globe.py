"""
Interactive 3D Olympic Globe & Real Medal Geo-Telemetry Component for OLYMPIA.
Renders an authentic, rotating 3D spherical Earth with real historical medal facts,
interactive country inspection, and regional focal views.
"""

import pandas as pd
import plotly.graph_objects as go
from typing import Optional, Tuple
from dashboard.components.flags import get_country_flag_emoji, get_country_iso2

# Latitude / Longitude coordinates for prominent Olympic nations
OLYMPIC_CAPITAL_COORDINATES = {
    "United States": {"lat": 38.9, "lon": -77.0, "code": "USA"},
    "Soviet Union": {"lat": 55.7, "lon": 37.6, "code": "URS"},
    "USSR": {"lat": 55.7, "lon": 37.6, "code": "URS"},
    "Russian Federation": {"lat": 55.7, "lon": 37.6, "code": "RUS"},
    "Great Britain": {"lat": 51.5, "lon": -0.1, "code": "GBR"},
    "Germany": {"lat": 52.5, "lon": 13.4, "code": "GER"},
    "France": {"lat": 48.8, "lon": 2.3, "code": "FRA"},
    "Italy": {"lat": 41.9, "lon": 12.5, "code": "ITA"},
    "China": {"lat": 39.9, "lon": 116.4, "code": "CHN"},
    "Australia": {"lat": -35.3, "lon": 149.1, "code": "AUS"},
    "Sweden": {"lat": 59.3, "lon": 18.0, "code": "SWE"},
    "Hungary": {"lat": 47.5, "lon": 19.0, "code": "HUN"},
    "Japan": {"lat": 35.7, "lon": 139.7, "code": "JPN"},
    "Norway": {"lat": 59.9, "lon": 10.7, "code": "NOR"},
    "Canada": {"lat": 45.4, "lon": -75.7, "code": "CAN"},
    "Netherlands": {"lat": 52.3, "lon": 4.9, "code": "NED"},
    "Finland": {"lat": 60.1, "lon": 24.9, "code": "FIN"},
    "South Korea": {"lat": 37.5, "lon": 126.9, "code": "KOR"},
    "India": {"lat": 28.6, "lon": 77.2, "code": "IND"},
    "Brazil": {"lat": -15.8, "lon": -47.9, "code": "BRA"},
    "Cuba": {"lat": 23.1, "lon": -82.3, "code": "CUB"},
    "Kenya": {"lat": -1.3, "lon": 36.8, "code": "KEN"},
    "Jamaica": {"lat": 18.0, "lon": -76.8, "code": "JAM"},
    "Greece": {"lat": 37.9, "lon": 23.7, "code": "GRE"}
}


def create_olympic_3d_globe(
    df: pd.DataFrame,
    center_lat: float = 25.0,
    center_lon: float = 15.0,
    height: int = 420,
    projection: str = "orthographic"
) -> go.Figure:
    """
    Renders an authentic, interactive 3D Spherical Globe displaying real medal counts
    for every country in the dataset, with rich hover cards and gold pin beacons.
    """
    if df.empty:
        fig_empty = go.Figure()
        fig_empty.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            annotations=[dict(text="No Olympic facts match the current filter", showarrow=False, font=dict(color="#8B857C"))]
        )
        return fig_empty

    # Aggregate real medal metrics per country
    agg = df.groupby("country").agg(
        total_medals=("medal_fact_id", "count"),
        gold=("medal", lambda s: (s == "Gold").sum()),
        silver=("medal", lambda s: (s == "Silver").sum()),
        bronze=("medal", lambda s: (s == "Bronze").sum()),
        top_sport=("sport", lambda s: s.mode().iloc[0] if not s.empty else "Olympics")
    ).reset_index()

    # Pre-format hover customdata
    custom_data = []
    for _, row in agg.iterrows():
        ctry = row["country"]
        emoji = get_country_flag_emoji(ctry)
        custom_data.append([
            f"{emoji} {ctry}",
            row["total_medals"],
            row["gold"],
            row["silver"],
            row["bronze"],
            row["top_sport"]
        ])

    fig = go.Figure()

    # 1. Base Choropleth Layer on the 3D Sphere
    fig.add_trace(go.Choropleth(
        locations=agg["country"],
        locationmode="country names",
        z=agg["total_medals"],
        colorscale=[
            [0.0, "#FAF8F2"],
            [0.08, "#F6ECCF"],
            [0.25, "#EBD9C3"],
            [0.55, "#D4AF37"],
            [0.85, "#B88E1A"],
            [1.0, "#7A5C05"]
        ],
        colorbar=dict(
            title=dict(
                text="<b>Medals</b>",
                font=dict(family="JetBrains Mono, monospace", size=11, color="#2E2A25")
            ),
            thickness=12,
            len=0.65,
            x=0.96,
            y=0.5,
            tickfont=dict(family="JetBrains Mono, monospace", size=9, color="#8B857C"),
            outlinecolor="#E5DED2",
            outlinewidth=1
        ),
        marker=dict(line=dict(color="#D5CBBB", width=0.8)),
        customdata=custom_data,
        hovertemplate=(
            "<b>%{customdata[0]}</b><br>"
            "<span style='color: #8B857C;'>────────────────────────────</span><br>"
            "🏆 <b>Total Medals:</b> %{customdata[1]:,}<br>"
            "🥇 <b>Gold:</b> %{customdata[2]:,}  "
            "🥈 <b>Silver:</b> %{customdata[3]:,}  "
            "🥉 <b>Bronze:</b> %{customdata[4]:,}<br>"
            "🎯 <b>Primary Discipline:</b> %{customdata[5]}"
            "<extra></extra>"
        )
    ))

    # 2. Golden Beacon ScatterGeo Markers for Top Medal Hubs
    top_countries = agg.sort_values(by="total_medals", ascending=False).head(16)
    pin_lats, pin_lons, pin_texts, pin_sizes = [], [], [], []

    for _, row in top_countries.iterrows():
        ctry = row["country"]
        if ctry in OLYMPIC_CAPITAL_COORDINATES:
            coords = OLYMPIC_CAPITAL_COORDINATES[ctry]
            pin_lats.append(coords["lat"])
            pin_lons.append(coords["lon"])
            emoji = get_country_flag_emoji(ctry)
            pin_texts.append(f"{emoji} {ctry}: {row['total_medals']:,} Medals")
            # Size scaled proportionally
            sz = max(7, min(16, int(7 + (row["total_medals"] / agg["total_medals"].max()) * 11)))
            pin_sizes.append(sz)

    if pin_lats:
        fig.add_trace(go.Scattergeo(
            lat=pin_lats,
            lon=pin_lons,
            mode="markers",
            marker=dict(
                size=pin_sizes,
                color="#D4AF37",
                line=dict(color="#FFFFFF", width=1.5),
                symbol="circle",
                opacity=0.9
            ),
            text=pin_texts,
            hoverinfo="text",
            name="Top Olympic Powers"
        ))

    # 2B. 3D Bezier Comet Arc Trails connecting Historical Olympic Host Cities
    olympic_host_sequence = [
        {"city": "Athens (1896)", "lat": 37.98, "lon": 23.72},
        {"city": "Paris (1900/1924/2024)", "lat": 48.85, "lon": 2.35},
        {"city": "London (1908/1948/2012)", "lat": 51.50, "lon": -0.12},
        {"city": "Tokyo (1964/2020)", "lat": 35.67, "lon": 139.65},
        {"city": "Beijing (2008/2022)", "lat": 39.90, "lon": 116.40},
        {"city": "Los Angeles (1932/1984/2028)", "lat": 34.05, "lon": -118.24},
        {"city": "Milano-Cortina (2026)", "lat": 45.46, "lon": 9.19}
    ]

    arc_lats, arc_lons = [], []
    for i in range(len(olympic_host_sequence) - 1):
        c1 = olympic_host_sequence[i]
        c2 = olympic_host_sequence[i + 1]
        arc_lats.extend([c1["lat"], c2["lat"], None])
        arc_lons.extend([c1["lon"], c2["lon"], None])

    # Faint Sandstone Base Arc Trajectory
    fig.add_trace(go.Scattergeo(
        lat=arc_lats,
        lon=arc_lons,
        mode="lines",
        line=dict(width=1.5, color="#EBD9C3"),
        opacity=0.6,
        hoverinfo="none",
        name="Historical Arc Trajectory"
    ))

    # Bright Olympic Gold Comet Trajectory
    fig.add_trace(go.Scattergeo(
        lat=arc_lats,
        lon=arc_lons,
        mode="lines",
        line=dict(width=2.5, color="#D4AF37"),
        opacity=0.9,
        hoverinfo="none",
        name="Olympic Torch Comet Trail"
    ))

    # Host city glowing nodes
    host_lats = [c["lat"] for c in olympic_host_sequence]
    host_lons = [c["lon"] for c in olympic_host_sequence]
    host_names = [f"🏛️ Olympic Host: {c['city']}" for c in olympic_host_sequence]

    fig.add_trace(go.Scattergeo(
        lat=host_lats,
        lon=host_lons,
        mode="markers",
        marker=dict(
            size=9,
            color="#C41E3A",
            line=dict(color="#D4AF37", width=2),
            symbol="diamond"
        ),
        text=host_names,
        hoverinfo="text",
        name="Iconic Olympic Host Cities"
    ))

    # 3. 3D Globe Projection Architecture
    fig.update_geos(
        projection_type=projection,
        projection_rotation=dict(lat=center_lat, lon=center_lon, roll=0),
        showcoastlines=True,
        coastlinecolor="#C8BEAF",
        coastlinewidth=1.2,
        showland=True,
        landcolor="#FDFBF7",
        showocean=True,
        oceancolor="#F3ECE0",
        showlakes=True,
        lakecolor="#F3ECE0",
        showcountries=True,
        countrycolor="#D5CBBB",
        countrywidth=0.7,
        showframe=False,
        bgcolor="rgba(0,0,0,0)"
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=0, r=0, t=0, b=0),
        height=height,
        showlegend=False,
        hoverlabel=dict(
            bgcolor="#FFFFFF",
            bordercolor="#D4AF37",
            font=dict(family="Inter, sans-serif", size=12, color="#2E2A25")
        )
    )

    return fig
