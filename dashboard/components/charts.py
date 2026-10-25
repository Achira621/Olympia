"""
Charts Bridge Component for OLYMPIA.
Integrates Plotly charts with Streamlit styling adhering to the
Legendary Olympic Intelligence Archive architectural marble & gold design system.
"""

import streamlit as st
import plotly.graph_objects as go

# Master Color Tokens for Visualizations
CHART_GOLD = "#D4AF37"
CHART_SANDSTONE = "#EBD9C3"
CHART_CHARCOAL = "#2E2A25"
CHART_RED = "#C41E3A"
CHART_GREY = "#8B857C"
CHART_BORDER = "#E5DED2"
CHART_SILVER = "#94A3B8"
CHART_BRONZE = "#B45309"

COLOR_DISCRETE_SEQUENCE = [
    CHART_GOLD,
    CHART_CHARCOAL,
    CHART_SANDSTONE,
    CHART_RED,
    CHART_GREY,
    CHART_SILVER,
    CHART_BRONZE
]


def apply_olympia_theme(fig: go.Figure, title: str = "", x_title: str = "", y_title: str = "") -> go.Figure:
    """
    Universal high-performance Plotly theme adhering to OLYMPIA Marble & Gold design:
    - Transparent viewport blending seamlessly with marble cards and white surfaces
    - JetBrains Mono tabular coordinates & tick fonts
    - High-contrast Imperial Gold hover boundaries & charcoal typography
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": f"<b>{title}</b>" if title else "",
            "font": {"size": 15, "color": "#2E2A25", "family": "Cinzel, Cormorant Garamond, Georgia, serif"},
            "x": 0.02,
            "xanchor": "left"
        } if title else None,
        font=dict(family="Inter, sans-serif", color="#2E2A25"),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color="#8B857C", size=11, family="Inter, sans-serif")) if x_title else None,
            gridcolor="rgba(46, 42, 37, 0.07)",
            zerolinecolor="rgba(46, 42, 37, 0.15)",
            tickfont=dict(color="#8B857C", family="JetBrains Mono, monospace", size=10)
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color="#8B857C", size=11, family="Inter, sans-serif")) if y_title else None,
            gridcolor="rgba(46, 42, 37, 0.07)",
            zerolinecolor="rgba(46, 42, 37, 0.15)",
            tickfont=dict(color="#8B857C", family="JetBrains Mono, monospace", size=10)
        ),
        legend=dict(
            bgcolor="rgba(250, 248, 242, 0.92)",
            bordercolor="#E5DED2",
            font=dict(color="#2E2A25", family="Inter, sans-serif", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#FAF8F2",
            bordercolor="#D4AF37",
            font=dict(family="JetBrains Mono, monospace", color="#2E2A25", size=12)
        ),
        colorway=COLOR_DISCRETE_SEQUENCE,
        margin=dict(l=30, r=20, t=45 if title else 25, b=30),
        autosize=True
    )
    return fig


def display_chart(fig: go.Figure, key: str = None):
    """Renders a Plotly chart with full responsive width and unified Olympic theme."""
    apply_olympia_theme(fig)
    st.plotly_chart(fig, use_container_width=True, key=key, config={"displayModeBar": False, "responsive": True})
