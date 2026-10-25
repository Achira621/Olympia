"""
Charts Bridge Component for OLYMPIA.
Integrates Plotly charts with Streamlit styling adhering to the
Kinetic Olympic Telemetry Lab spatial design system.
"""

import streamlit as st
import plotly.graph_objects as go


def apply_olympia_theme(fig: go.Figure, title: str = "", x_title: str = "", y_title: str = "") -> go.Figure:
    """
    Universal high-performance Plotly theme adhering to OLYMPIA Kinetic Telemetry Lab design:
    - Transparent viewport blending seamlessly with Obsidian void & glass cards
    - JetBrains Mono tabular coordinates & tick fonts
    - High-contrast electric lime hover boundaries
    """
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        title={
            "text": f"<b>{title}</b>" if title else "",
            "font": {"size": 15, "color": "#F8FAFC", "family": "Space Grotesk, Inter, sans-serif"},
            "x": 0.02,
            "xanchor": "left"
        } if title else None,
        font=dict(family="Inter, sans-serif", color="#F8FAFC"),
        xaxis=dict(
            title=dict(text=x_title, font=dict(color="#94A3B8", size=11, family="Inter, sans-serif")) if x_title else None,
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", family="JetBrains Mono, monospace", size=10)
        ),
        yaxis=dict(
            title=dict(text=y_title, font=dict(color="#94A3B8", size=11, family="Inter, sans-serif")) if y_title else None,
            gridcolor="rgba(255, 255, 255, 0.05)",
            zerolinecolor="rgba(255, 255, 255, 0.12)",
            tickfont=dict(color="#94A3B8", family="JetBrains Mono, monospace", size=10)
        ),
        legend=dict(
            bgcolor="rgba(20, 22, 27, 0.75)",
            bordercolor="rgba(255, 255, 255, 0.08)",
            font=dict(color="#F8FAFC", family="Inter, sans-serif", size=11)
        ),
        hoverlabel=dict(
            bgcolor="#14161B",
            bordercolor="#5DD62C",
            font=dict(family="JetBrains Mono, monospace", color="#F8FAFC", size=12)
        ),
        margin=dict(l=30, r=20, t=45 if title else 25, b=30),
        autosize=True
    )
    return fig


def display_chart(fig: go.Figure, key: str = None):
    """Renders a Plotly chart with full responsive width and unified telemetry theme."""
    apply_olympia_theme(fig)
    st.plotly_chart(fig, use_container_width=True, key=key, config={"displayModeBar": False, "responsive": True})

