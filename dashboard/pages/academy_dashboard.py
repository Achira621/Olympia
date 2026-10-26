"""
Professional Player / Academy High-Performance Intelligence Dashboard for OLYMPIA.
Tailored for athletes, coaches, national sports federations, and sports science academies.
Focuses on performance analytics, discipline competitiveness, and historical benchmarks.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
from warehouse.warehouse import get_denormalized_medals
from dashboard.components.metrics import render_kpi_row, render_viva_note, render_forbes_masthead
from dashboard.components.charts import display_chart
from dashboard.components.coach_strategy_ui import render_coach_strategy_studio
from analytics.visualization import (
    create_bar_chart,
    create_line_chart,
    create_scatter_plot
)


def render_page(df: pd.DataFrame | None = None):
    if df is None:
        df = get_denormalized_medals()

    # 1. Forbes Minimalist Editorial Masthead
    render_forbes_masthead(
        tag="The World's",
        title="High-Performance Academy Intelligence",
        subtitle="Olympic competitive landscape, discipline depth, historical benchmarks, and national talent distribution across 1896 – 2026.",
        badge_text="Biomechanical Benchmarks • SQLite Star Schema Live",
        badge_status="Performance Active"
    )

    acad_mode = st.radio(
        "Academy Workspace View:",
        options=[
            "🎯 Coach Strategy & Player Inclination Studio",
            "📊 Discipline Depth & Parity Benchmarks"
        ],
        index=0,
        horizontal=True,
        key="acad_workspace_toggle"
    )

    if "Strategy" in acad_mode or "Coach" in acad_mode:
        render_coach_strategy_studio(df)
        return

    # 1. High Performance KPIs
    total_medals = len(df)
    unique_nations = df["country"].nunique()
    gold_medals = int((df["medal"] == "Gold").sum())
    total_points = int(df["medal_points"].sum())
    top_3_concentration = (
        df.groupby("country").size().nlargest(3).sum() / max(total_medals, 1) * 100
    )

    kpis = [
        {"title": "Analyzed Podium Finishes", "value": f"{total_medals:,}", "subtitle": "1896 – 2024 Olympic history", "icon": "trophy"},
        {"title": "Podium Winning Nations", "value": f"{unique_nations}", "subtitle": "Nations reaching top-3", "icon": "globe"},
        {"title": "Total Medal Points", "value": f"{total_points:,}", "subtitle": "Gold=3, Silver=2, Bronze=1", "icon": "star"},
        {"title": "Top-3 Podium Share", "value": f"{top_3_concentration:.1f}%", "subtitle": "All-time concentration", "icon": "trend_up"},
    ]
    render_kpi_row(kpis)

    render_viva_note(
        "Performance Benchmarking Methodology",
        "This platform analyzes national sporting performance through quantitative podium outcomes, discipline specialization ratios, and multi-edition historical stability.",
        "Crucial Academy Disclosure: All metrics are computed strictly from verified official Olympic Games medal history. This platform provides historical competitive baselines to benchmark international sporting standards."
    )

    st.markdown("---")

    # 2. Performance Matrix: Discipline Depth & Competitive Parity
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Discipline Depth: Medals vs Winning Nations")
        sport_metrics = (
            df.groupby("sport")
            .agg(
                total_medals=("medal_fact_id", "count"),
                unique_countries=("country", "nunique"),
                unique_events=("event_name", "nunique")
            )
            .reset_index()
        )
        sport_metrics["parity_ratio"] = (
            sport_metrics["unique_countries"] / sport_metrics["total_medals"]
        ).round(3)

        fig_scatter = create_scatter_plot(
            sport_metrics,
            x="total_medals",
            y="unique_countries",
            title="Sport Competitiveness: Total Medals vs Nation Breadth"
        )
        display_chart(fig_scatter, key="academy_parity_scatter")
        st.caption("Sports in the upper right (e.g. Athletics) feature wide international competition, whereas lower-volume sports exhibit specialized national concentration.")

    with col2:
        st.subheader("Gold Medal Conversion Efficiency (Top 12 Nations)")
        top_nations = (
            df.groupby("country")
            .agg(
                total=("medal", "count"),
                golds=("medal", lambda m: (m == "Gold").sum())
            )
            .reset_index()
            .sort_values(by="total", ascending=False)
            .head(12)
        )
        top_nations["gold_pct"] = (top_nations["golds"] / top_nations["total"] * 100).round(1)

        fig_conv = create_bar_chart(
            top_nations,
            x="country",
            y="gold_pct",
            title="Gold Medal Conversion Rate (% of All Medals Won)",
            orientation="v"
        )
        display_chart(fig_conv, key="academy_conversion_chart")

    st.markdown("---")

    # 3. Modern Momentum (2000–2024 Olympic Era)
    st.subheader("Modern Era Performance Momentum (Sydney 2000 – Paris 2024)")
    modern_df = df[df["year"] >= 2000]
    modern_top = (
        modern_df.groupby("country")
        .agg(
            modern_medals=("medal", "count"),
            modern_golds=("medal", lambda m: (m == "Gold").sum()),
            sports_won=("sport", "nunique")
        )
        .reset_index()
        .sort_values(by="modern_medals", ascending=False)
        .head(15)
    )
    st.dataframe(modern_top, use_container_width=True, hide_index=True)

    # 4. Academy Scope, Data Boundaries & Future Roadmap
    st.markdown("---")
    st.subheader("Sports Science Boundaries & Future Scope Roadmap")

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""
        <div style="background: #141414; border-left: 4px solid #10b981; border: 1px solid #262626; border-left-width: 4px; border-radius: 8px; padding: 1.1rem 1.3rem;">
            <div style="font-weight: 700; color: #10b981; margin-bottom: 0.4rem; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.06em;">
                Current Supported Capabilities
            </div>
            <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5;">
                • Official Olympic podium history (1896 – 2024)<br>
                • National discipline specialization and medal points<br>
                • Country-level competitive clusters & historical regression baselines<br>
                • Event gender expansion & global podium parity analysis
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div style="background: #141414; border-left: 4px solid #f59e0b; border: 1px solid #262626; border-left-width: 4px; border-radius: 8px; padding: 1.1rem 1.3rem;">
            <div style="font-weight: 700; color: #f59e0b; margin-bottom: 0.4rem; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.06em;">
                Future Scope Roadmap (Athlete-Level Telemetry)
            </div>
            <div style="font-size: 0.88rem; color: #94A3B8; line-height: 1.5;">
                • <strong>Biometric Integration:</strong> Heart rate variability, VO2 max, and recovery telemetry.<br>
                • <strong>In-Event Kinematics:</strong> Velocity profiles, split times, and stroke/stride rates.<br>
                • <strong>Injury Surveillance:</strong> Longitudinal training load and injury risk modeling.<br>
                • <em>Note: Wearable sensor telemetry is outside the official historical IOC medal dataset.</em>
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_page()
