"""
Sport Enthusiast Olympic Fan Dashboard for OLYMPIA.
Designed for sports fans, general audiences, and students.
Prioritizes high visual impact, simplicity, fast discovery, and interesting facts.
No database jargon or technical ML formulas.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
from warehouse.warehouse import get_denormalized_medals
from dashboard.components.metrics import render_kpi_row, render_forbes_masthead
from dashboard.components.charts import display_chart
from analytics.visualization import (
    create_bar_chart,
    create_line_chart,
    plot_gender_breakdown,
    MEDAL_COLORS
)


def render_page(df: pd.DataFrame = None):
    if df is None:
        df = get_denormalized_medals()

    # 1. Forbes Minimalist Editorial Masthead
    render_forbes_masthead(
        tag="The World's",
        title="Olympic Fan & Explorer Dashboard",
        subtitle="Celebrate the greatest moments, legendary nations, and iconic sports across modern Olympic history (1896 – 2024).",
        badge_text="53 Olympic Editions • Global Storyboards Active",
        badge_status="Dynasty Active"
    )

    # 1. High-Level Fan KPIs
    total_medals = len(df)
    total_countries = df["country"].nunique()
    total_sports = df["sport"].nunique()
    total_editions = df["games"].nunique()

    kpis = [
        {"title": "Olympic Editions", "value": f"{total_editions}", "subtitle": "From Athens 1896 to Paris 2024", "icon": "calendar"},
        {"title": "Podium Finishes", "value": f"{total_medals:,}", "subtitle": "Gold, Silver & Bronze moments", "icon": "trophy"},
        {"title": "Nations Represented", "value": f"{total_countries}", "subtitle": "Countries with Olympic medals", "icon": "globe"},
        {"title": "Olympic Sports", "value": f"{total_sports}", "subtitle": "Track, Aquatics, Gymnastics & more", "icon": "lightning"},
    ]
    render_kpi_row(kpis)

    # 2. "What Can I Explore?" Quick Jump Guide
    st.markdown("""
    <div style="background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 14px; padding: 1.1rem 1.4rem; margin: 1.2rem 0; box-shadow: var(--shadow-subtle);">
        <div style="font-weight: 800; color: #AA820A; font-size: 0.85rem; text-transform: uppercase; letter-spacing: 0.1em; margin-bottom: 0.4rem; font-family: 'Cinzel', serif;">
            Curated Historical Exploration Guide
        </div>
        <div style="color: #5A544A; font-size: 0.9rem; line-height: 1.6; font-family: 'Inter', sans-serif;">
            • <strong>Which countries rule the podium?</strong> Check out the All-Time Leaderboard below or visit <strong>Countries</strong> in the sidebar.<br>
            • <strong>How has India performed?</strong> See the dedicated India Spotlight below.<br>
            • <strong>Summer vs Winter Games?</strong> Compare both seasons side-by-side below.<br>
            • <strong>Want to see your favorite sport?</strong> Head to <strong>Sports</strong> in the sidebar for event and nation breakdowns.<br>
            • <strong>Compare two rivals?</strong> Use <strong>Head-to-Head Comparison</strong> in the sidebar.
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 3. All-Time Leaderboard & Summer vs Winter
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("All-Time Top 10 Olympic Nations")
        top_10 = (
            df.groupby("country")
            .size()
            .reset_index(name="medals")
            .sort_values(by="medals", ascending=False)
            .head(10)
        )
        fig_top = create_bar_chart(
            top_10,
            x="country",
            y="medals",
            title="Nations with the Most Olympic Medals in History",
            orientation="v"
        )
        display_chart(fig_top, key="enthusiast_top10")

    with col2:
        st.subheader("Summer vs Winter Olympics")
        season_summary = df.groupby(["season", "medal"]).size().reset_index(name="count")
        fig_season = create_bar_chart(
            season_summary,
            x="season",
            y="count",
            color="medal",
            title="Medal Distribution by Olympic Season",
            barmode="stack"
        )
        display_chart(fig_season, key="enthusiast_season")

    st.markdown("---")

    # 4. India Olympic Spotlight
    st.subheader("Spotlight: India's Olympic Journey")
    india_df = df[df["country"] == "India"]

    if not india_df.empty:
        i_col1, i_col2 = st.columns([1, 1])
        with i_col1:
            i_total = len(india_df)
            i_gold = int((india_df["medal"] == "Gold").sum())
            i_silver = int((india_df["medal"] == "Silver").sum())
            i_bronze = int((india_df["medal"] == "Bronze").sum())

            render_kpi_row([
                {"title": "Total Medals", "value": str(i_total), "icon": "trophy"},
                {"title": "Gold Medals", "value": str(i_gold), "icon": "gold_medal"},
                {"title": "Silver Medals", "value": str(i_silver), "icon": "silver_medal"},
                {"title": "Bronze Medals", "value": str(i_bronze), "icon": "bronze_medal"},
            ])

            india_sports = india_df.groupby("sport").size().reset_index(name="medals").sort_values(by="medals", ascending=False)
            fig_i_sports = create_bar_chart(
                india_sports,
                x="sport",
                y="medals",
                title="India: Medals Won by Sport Discipline"
            )
            display_chart(fig_i_sports, key="enthusiast_india_sports")

        with i_col2:
            india_yearly = india_df.groupby("year").size().reset_index(name="medals")
            fig_i_trend = create_line_chart(
                india_yearly,
                x="year",
                y="medals",
                title="India: Medal Trajectory Over Time (1900 – 2024)"
            )
            display_chart(fig_i_trend, key="enthusiast_india_trend")

            st.markdown("""
            **Key Highlights:**
            - **Field Hockey Dynasty:** India won an unprecedented 6 consecutive Olympic Golds in Field Hockey between 1928 and 1956.
            - **Modern Era Resurgence:** Multi-medal campaigns in Beijing 2008, London 2012, Tokyo 2020 (7 medals), and Paris 2024 across Athletics, Wrestling, Shooting, and Badminton.
            """)

    # 5. Fun Olympic Trivia & Facts
    st.markdown("---")
    st.subheader("Historical Olympic Milestones")
    t1, t2, t3 = st.columns(3)
    with t1:
        st.markdown("""
        <div style="background: #FFFFFF; border-radius: 12px; padding: 1.1rem; border: 1px solid #E5DED2; height: 160px; box-shadow: var(--shadow-subtle);">
            <div style="font-weight: 700; color: #D4AF37; margin-bottom: 0.3rem; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.08em; font-family: 'Cinzel', serif;">The Modern Revival</div>
            <div style="font-size: 0.85rem; color: #5A544A; line-height: 1.5; font-family: 'Inter', sans-serif;">
                The first modern Olympic Games were held in Athens, Greece, in 1896. Only 14 nations competed across 43 events. In Paris 2024, over 200 nations competed in 329 events.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with t2:
        st.markdown("""
        <div style="background: #FFFFFF; border-radius: 12px; padding: 1.1rem; border: 1px solid #E5DED2; height: 160px; box-shadow: var(--shadow-subtle);">
            <div style="font-weight: 700; color: #2E2A25; margin-bottom: 0.3rem; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.08em; font-family: 'Cinzel', serif;">Winter Games Debut</div>
            <div style="font-size: 0.85rem; color: #5A544A; line-height: 1.5; font-family: 'Inter', sans-serif;">
                The first Olympic Winter Games took place in Chamonix, France, in 1924. Until 1992, Summer and Winter Games were held in the very same calendar year.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with t3:
        st.markdown("""
        <div style="background: #FFFFFF; border-radius: 12px; padding: 1.1rem; border: 1px solid #E5DED2; height: 160px; box-shadow: var(--shadow-subtle);">
            <div style="font-weight: 700; color: #C41E3A; margin-bottom: 0.3rem; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.08em; font-family: 'Cinzel', serif;">Gender Parity Milestone</div>
            <div style="font-size: 0.85rem; color: #5A544A; line-height: 1.5; font-family: 'Inter', sans-serif;">
                Paris 2024 achieved full 50:50 athlete quota parity between men and women for the first time in Olympic history, representing a 128-year journey of expanding inclusion.
            </div>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    render_page()
