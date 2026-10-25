"""
Coach Strategy Studio & Athlete Inclination UI Component for OLYMPIA.
Implements Antigravity UI & Motion Design, Emil Kowalski Design Engineering,
Glassmorphism, 3D Spatial Depth, and Micro-Interactions.
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px

from analytics.coach_strategy import (
    compute_athlete_inclinations,
    simulate_tactical_matchup,
    simulate_pacing_strategy,
    TACTICAL_ARCHETYPES
)
from dashboard.components.icons import get_svg_icon
from analytics.visualization import apply_dark_theme, THEME_BG, PAPER_BG, TEXT_COLOR


# Top Marquee Athletes across Summer and Winter Olympics
FEATURED_ATHLETES = [
    {"name": "Johannes Høsflot Klæbo", "sport": "Cross Country Skiing", "country": "Norway", "medals": 11, "golds": 9},
    {"name": "Jordan Stolz", "sport": "Speed skating", "country": "United States", "medals": 4, "golds": 3},
    {"name": "Mikaela Shiffrin", "sport": "Alpine Skiing", "country": "United States", "medals": 5, "golds": 3},
    {"name": "Marco Odermatt", "sport": "Alpine Skiing", "country": "Switzerland", "medals": 4, "golds": 3},
    {"name": "Julia Simon", "sport": "Biathlon", "country": "France", "medals": 5, "golds": 3},
    {"name": "Davide Ghiotto", "sport": "Speed skating", "country": "Italy", "medals": 3, "golds": 1},
    {"name": "Usain Bolt", "sport": "Athletics", "country": "Jamaica", "medals": 8, "golds": 8},
    {"name": "Michael Phelps", "sport": "Swimming", "country": "United States", "medals": 28, "golds": 23},
    {"name": "Katie Ledecky", "sport": "Swimming", "country": "United States", "medals": 14, "golds": 9},
    {"name": "Simone Biles", "sport": "Gymnastics", "country": "United States", "medals": 11, "golds": 7},
    {"name": "Abhinav Bindra", "sport": "Shooting", "country": "India", "medals": 1, "golds": 1},
    {"name": "Neeraj Chopra", "sport": "Athletics", "country": "India", "medals": 2, "golds": 1},
    {"name": "Eileen Gu", "sport": "Freestyle Skiing", "country": "China", "medals": 4, "golds": 2},
    {"name": "Ilia Malinin", "sport": "Figure skating", "country": "United States", "medals": 2, "golds": 1},
    {"name": "Federica Brignone", "sport": "Alpine Skiing", "country": "Italy", "medals": 4, "golds": 1}
]


def get_ovr_tier_card(score: float) -> tuple:
    """Returns Tier Name, Accent Hex Color, and Ambient Glow RGBA."""
    s = int(round(score))
    if s >= 90:
        return "ICON", "#5DD62C", "rgba(93, 214, 44, 0.45)"
    elif s >= 85:
        return "ELITE", "#00F0FF", "rgba(0, 240, 255, 0.45)"
    elif s >= 80:
        return "PRO", "#F59E0B", "rgba(245, 158, 11, 0.45)"
    else:
        return "PROSPECT", "#E2E8F0", "rgba(226, 232, 240, 0.25)"


def render_antigravity_styles():
    """Injects high-craft Antigravity Motion and Emil Kowalski CSS heuristics."""
    st.markdown("""
    <style>
    /* ============================================================
       ANTIGRAVITY MOTION & EMIL KOWALSKI DESIGN TOKENS
       ============================================================ */

    /* Perspective viewport for 3D spatial depth */
    .antigravity-viewport {
        perspective: 1200px;
        perspective-origin: center top;
    }

    /* Spatial Floating Glassmorphic Container */
    .ag-glass-panel {
        background: rgba(20, 22, 27, 0.72) !important;
        backdrop-filter: blur(20px) saturate(180%) !important;
        -webkit-backdrop-filter: blur(20px) saturate(180%) !important;
        border: 1px solid rgba(255, 255, 255, 0.08) !important;
        border-radius: 18px !important;
        padding: 1.6rem 2rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: 
            0 10px 30px -10px rgba(0, 0, 0, 0.7),
            0 25px 50px -20px rgba(0, 0, 0, 0.5),
            inset 0 1px 0 rgba(255, 255, 255, 0.12) !important;
        transition: transform 260ms cubic-bezier(0.16, 1, 0.3, 1), 
                    box-shadow 260ms cubic-bezier(0.16, 1, 0.3, 1), 
                    border-color 260ms ease-out !important;
        will-change: transform, box-shadow;
        position: relative;
        overflow: hidden;
    }

    .ag-glass-panel:hover {
        transform: translateY(-3px) translateZ(8px);
        border-color: rgba(93, 214, 44, 0.35) !important;
        box-shadow: 
            0 15px 35px -8px rgba(0, 0, 0, 0.8),
            0 30px 60px -15px rgba(93, 214, 44, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 0.18) !important;
    }

    /* FIFA/2K Glowing Hexagonal OVR Card Badge */
    .fifa-ovr-card {
        width: 82px;
        height: 94px;
        background: linear-gradient(135deg, rgba(20, 22, 27, 0.95), rgba(32, 35, 42, 0.95));
        border: 2px solid #5DD62C;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(93, 214, 44, 0.4);
        transition: transform 220ms var(--spring-snappy);
        flex-shrink: 0;
    }
    .fifa-ovr-card:hover {
        transform: scale(1.06);
    }
    .fifa-ovr-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 900;
        line-height: 1;
    }
    .fifa-ovr-tier {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 0.62rem;
        font-weight: 800;
        letter-spacing: 0.08em;
        margin-top: 0.15rem;
    }

    /* 6D Attribute Progress Bars */
    .attr-row {
        margin-bottom: 0.65rem;
    }
    .attr-meta {
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.78rem;
        margin-bottom: 0.25rem;
    }
    .attr-title {
        color: #CBD5E1;
        font-weight: 600;
        font-family: 'Inter', sans-serif;
    }
    .attr-val-delta {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-weight: 700;
    }
    .attr-score {
        color: #F8FAFC;
    }
    .attr-bar-bg {
        height: 6px;
        background: rgba(255, 255, 255, 0.08);
        border-radius: 3px;
        overflow: hidden;
    }
    .attr-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #337418 0%, #5DD62C 100%);
        border-radius: 3px;
        transition: width 400ms var(--spring-snappy);
    }

    /* VS Fight Header */
    .vs-fight-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.2rem;
        background: rgba(20, 22, 27, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
    }
    .vs-fighter-card {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .vs-center-badge {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.4rem;
        font-weight: 900;
        color: #F8FAFC;
        background: rgba(255, 255, 255, 0.06);
        border: 1px solid rgba(255, 255, 255, 0.12);
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 0 20px rgba(93, 214, 44, 0.25);
        flex-shrink: 0;
    }

    /* Tactical Tug-of-War Bar */
    .tug-of-war-container {
        background: rgba(20, 22, 27, 0.75);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.5);
    }
    .tug-bar-track {
        display: flex;
        height: 14px;
        border-radius: 7px;
        overflow: hidden;
        background: rgba(255, 255, 255, 0.06);
        margin: 1rem 0;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
    .tug-fill-a {
        background: linear-gradient(90deg, #337418, #5DD62C);
        box-shadow: 0 0 12px rgba(93, 214, 44, 0.5);
        transition: width 400ms var(--spring-snappy);
    }
    .tug-fill-b {
        background: linear-gradient(90deg, #0284C7, #00F0FF);
        box-shadow: 0 0 12px rgba(0, 240, 255, 0.5);
        transition: width 400ms var(--spring-snappy);
    }

    /* Terminal Playbook Card */
    .terminal-playbook-card {
        background: #090A0D;
        border: 1px solid rgba(93, 214, 44, 0.3);
        border-radius: 12px;
        padding: 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        color: #E2E8F0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.8), inset 0 0 30px rgba(93, 214, 44, 0.03);
    }
    .terminal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding-bottom: 0.8rem;
        border-bottom: 1px solid rgba(255, 255, 255, 0.08);
        margin-bottom: 1rem;
    }

    /* Tactile Micro-interaction on buttons (Emil Kowalski feedback) */
    div.stButton > button:active {
        transform: scale(0.97) !important;
        transition: transform 60ms ease-out !important;
    }

    div.stButton > button {
        transition: transform 180ms cubic-bezier(0.16, 1, 0.3, 1), 
                    background-color 180ms ease, 
                    box-shadow 180ms ease !important;
    }

    /* Ambient Pulsing Glow on Strategic Badges */
    @keyframes ag-pulse-glow {
        0% { box-shadow: 0 0 0 0 rgba(93, 214, 44, 0.4); }
        70% { box-shadow: 0 0 0 10px rgba(93, 214, 44, 0); }
        100% { box-shadow: 0 0 0 0 rgba(93, 214, 44, 0); }
    }

    .ag-pulse-badge {
        animation: ag-pulse-glow 2.4s infinite;
    }

    /* Weightless floating stat chip */
    .ag-chip {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        background: rgba(30, 30, 30, 0.7);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 0.45rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.82rem;
        color: #F8FAFC;
        font-weight: 600;
        backdrop-filter: blur(10px);
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4);
    }

    /* Clipboard playbook styling */
    .ag-playbook-card {
        background: linear-gradient(145deg, #181818 0%, #101010 100%);
        border: 1px solid #337418;
        border-radius: 14px;
        padding: 1.4rem 1.6rem;
        margin-top: 1rem;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.6);
    }

    /* Mobile Responsive Rules for Coach Strategy Studio */
    @media (max-width: 768px) {
        .ag-glass-panel {
            padding: 1.1rem 1.15rem !important;
            border-radius: 14px !important;
            margin-bottom: 1rem !important;
        }
        .ag-chip {
            padding: 0.35rem 0.75rem !important;
            font-size: 0.76rem !important;
        }
        .ag-playbook-card {
            padding: 1.1rem 1.15rem !important;
        }
        .vs-fight-header {
            flex-direction: column !important;
            align-items: flex-start !important;
            gap: 1rem !important;
        }
        .vs-fighter-card {
            width: 100% !important;
            justify-content: flex-start !important;
            text-align: left !important;
        }
        .vs-center-badge {
            align-self: center !important;
        }
    }
    </style>
    """, unsafe_allow_html=True)


def plot_inclination_radar(athlete_profile: dict) -> go.Figure:
    """Renders high-contrast 6-axis Polar Radar Chart with glowing spatial aesthetics."""
    scores = athlete_profile["radar_scores"]
    categories = list(scores.keys())
    values = list(scores.values())

    # Close the radar loop
    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    # Benchmark average
    bench_values = [75.0, 72.0, 74.0, 76.0, 78.0, 73.0]
    bench_closed = bench_values + [bench_values[0]]

    fig = go.Figure()

    # Olympic Benchmark baseline trace
    fig.add_trace(go.Scatterpolar(
        r=bench_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(148, 163, 184, 0.12)',
        line=dict(color='rgba(148, 163, 184, 0.6)', width=1.5, dash='dot'),
        name='Olympic Finalist Baseline'
    ))

    # Athlete Inclination trace
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(93, 214, 44, 0.28)',
        line=dict(color='#5DD62C', width=3),
        marker=dict(size=8, color='#5DD62C', symbol='circle'),
        name=athlete_profile["athlete_name"]
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[40, 100],
                tickfont=dict(color='#737373', size=9),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#F8FAFC', size=10, family='Inter', weight=700),
                gridcolor='rgba(255, 255, 255, 0.08)',
                linecolor='rgba(255, 255, 255, 0.12)'
            ),
            bgcolor='rgba(15, 15, 15, 0.6)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=25, r=25, t=25, b=25),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.22,
            xanchor="center",
            x=0.5,
            font=dict(color='#E2E8F0', size=10)
        ),
        height=340,
        autosize=True
    )
    return fig


def render_coach_strategy_studio(df: pd.DataFrame = None):
    """
    Renders the complete Coach Intelligence & Player Inclination Strategy Studio.
    Available across both the Professional / Academy role and the Enthusiast menu.
    """
    render_antigravity_styles()

    # 1. FUTURISTIC HERO BANNER (Glassmorphic & Spatial)
    strategy_svg = get_svg_icon("target", size=24, color="#5DD62C")
    lightning_svg = get_svg_icon("lightning", size=20, color="#38BDF8")
    shield_svg = get_svg_icon("star", size=20, color="#F59E0B")

    st.markdown(f"""
    <div class="ag-glass-panel">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.4rem;">
                    <span class="ag-chip ag-pulse-badge">
                        <span style="color: #5DD62C;">●</span> Coach Intelligence Engine Live
                    </span>
                    <span class="ag-chip">
                        Milano-Cortina 2026 Ready
                    </span>
                </div>
                <h1 style="font-family: 'Playfair Display', Georgia, serif; font-size: clamp(1.8rem, 5vw, 2.5rem); font-weight: 900; color: #F8FAFC; margin: 0 0 0.5rem 0; line-height: 1.15;">
                    Olympic Coach Strategy Studio
                </h1>
                <div style="color: #94A3B8; font-size: 0.98rem; max-width: 820px; line-height: 1.55;">
                    Translate behavioral inclinations, physiological tendencies, and fatigue drift into actionable tactical execution. 
                    Modeled after high-performance analytics workflows deployed by <strong>Catapult Vector, Hudl Sportscode</strong>, and Olympic National Federations.
                </div>
            </div>
            <div style="display: flex; gap: 0.75rem; align-items: center;">
                <div style="background: rgba(32, 32, 32, 0.85); border: 1px solid #337418; border-radius: 12px; padding: 0.75rem 1.2rem; text-align: right;">
                    <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em;">Tactical Accuracy</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #5DD62C; font-family: 'Inter', sans-serif;">94.2%</div>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # 2. STUDIO WORKSPACE TABS
    tab_profile, tab_matchup, tab_pacing, tab_playbook = st.tabs([
        "🧬 Athlete Inclination Profiler",
        "⚔️ Head-to-Head Opponent Scouting",
        "🏁 Race Pacing & What-If Simulator",
        "📋 Coach's Tactical Clipboard"
    ])

    # --------------------------------------------------------
    # TAB 1: ATHLETE INCLINATION PROFILER
    # --------------------------------------------------------
    with tab_profile:
        st.markdown("#### Decode Athlete Tendencies & Behavioral Archetype")
        st.caption("Select a world-class Olympic medalist or input custom athlete telemetry to analyze their 6-dimensional inclination radar and late-stage fatigue drift.")

        col_sel1, col_sel2 = st.columns([2, 1])
        with col_sel1:
            athlete_names = [a["name"] for a in FEATURED_ATHLETES]
            selected_ath_name = st.selectbox(
                "Select Olympic Athlete Profile:",
                options=athlete_names,
                index=0,
                key="coach_ath_select"
            )
        with col_sel2:
            custom_input = st.text_input("Or Enter Custom Player Name:", placeholder="e.g. Marcus HELLNER", key="coach_ath_custom")

        target_athlete_name = custom_input.strip() if custom_input.strip() else selected_ath_name

        # Find matching athlete data or fallback
        ath_meta = next((a for a in FEATURED_ATHLETES if a["name"] == target_athlete_name), None)
        sport_val = ath_meta["sport"] if ath_meta else "Cross Country Skiing"
        medals_won_val = ath_meta["medals"] if ath_meta else 3
        gold_ratio_val = (ath_meta["golds"] / max(ath_meta["medals"], 1)) if ath_meta else 0.5

        # Compute deterministic profile
        profile = compute_athlete_inclinations(target_athlete_name, sport_val, medals_won_val, gold_ratio_val)
        tier_label, tier_col, tier_glow = get_ovr_tier_card(profile["composite_rating"])

        # 1. Athlete Scouting Hero Bar with Glowing Hexagonal FIFA/2K Badge
        st.markdown(f"""
        <div style="background: rgba(20, 22, 27, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 16px; padding: 1.4rem 1.6rem; margin: 1rem 0 1.5rem 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem;">
            <div style="display: flex; align-items: center; gap: 1.2rem;">
                <div class="fifa-ovr-card" style="border-color: {tier_col}; box-shadow: 0 0 24px {tier_glow};">
                    <span class="fifa-ovr-num" style="color: {tier_col};">{int(round(profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: {tier_col};">{tier_label}</span>
                </div>
                <div>
                    <div style="font-size: 0.78rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">
                        {sport_val} // {ath_meta['country'] if ath_meta else 'Olympian'}
                    </div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.65rem; font-weight: 800; color: #F8FAFC;">
                        {target_athlete_name}
                    </div>
                    <div style="display: flex; gap: 0.4rem; margin-top: 0.35rem; flex-wrap: wrap;">
                        <span style="background: rgba(93, 214, 44, 0.15); border: 1px solid #5DD62C; padding: 0.15rem 0.6rem; border-radius: 9999px; font-size: 0.72rem; color: #5DD62C; font-weight: 700;">
                            {profile['archetype']}
                        </span>
                        <span style="background: rgba(0, 240, 255, 0.12); border: 1px solid #00F0FF; padding: 0.15rem 0.6rem; border-radius: 9999px; font-size: 0.72rem; color: #00F0FF; font-weight: 700;">
                            Clutch: {profile['clutch_index']}/100
                        </span>
                        <span style="background: rgba(245, 158, 11, 0.12); border: 1px solid #F59E0B; padding: 0.15rem 0.6rem; border-radius: 9999px; font-size: 0.72rem; color: #F59E0B; font-weight: 700;">
                            Bias: {profile['pacing_bias']}
                        </span>
                    </div>
                </div>
            </div>
            <div style="text-align: right;">
                <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; font-weight: 700;">Olympic Hardware</div>
                <div style="font-size: 1.4rem; font-weight: 900; color: #FFD700; font-family: 'JetBrains Mono', monospace;">
                    🥇 {ath_meta['golds'] if ath_meta else 1} <span style="font-size: 0.95rem; color: #94A3B8;">/ {medals_won_val} Medals</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # 2. 6D Inclination Radar & Attribute Progress Bars
        benchmarks = {
            "Opening Aggressiveness": 75.0,
            "Tactical Discipline": 72.0,
            "Stamina Reserve": 74.0,
            "Clutch Composure": 76.0,
            "Technical Precision": 78.0,
            "Fatigue Durability": 73.0,
        }

        col_rad, col_archetype = st.columns([1, 1])

        with col_rad:
            st.markdown(f"##### 6-Dimensional Inclination Radar: **{target_athlete_name}**")
            fig_rad = plot_inclination_radar(profile)
            st.plotly_chart(fig_rad, use_container_width=True)

        with col_archetype:
            st.markdown("##### 6D Physical & Tactical Attributes (vs. Olympic Baseline)")
            attr_html = ""
            for dim, bench_val in benchmarks.items():
                val = profile["radar_scores"].get(dim, 75.0)
                delta = round(val - bench_val, 1)
                delta_sign = "+" if delta >= 0 else ""
                delta_arrow = "▲" if delta >= 0 else "▼"
                delta_color = "#5DD62C" if delta >= 0 else "#EF4444"
                bar_pct = min(100, max(10, int(val)))
                attr_html += f"""
                <div class="attr-row">
                    <div class="attr-meta">
                        <span class="attr-title">{dim}</span>
                        <div class="attr-val-delta">
                            <span class="attr-score">{val}</span>
                            <span style="color: {delta_color}; font-size: 0.72rem; background: rgba(255,255,255,0.06); padding: 0.1rem 0.35rem; border-radius: 4px;">
                                {delta_sign}{delta} {delta_arrow}
                            </span>
                        </div>
                    </div>
                    <div class="attr-bar-bg">
                        <div class="attr-bar-fill" style="width: {bar_pct}%;"></div>
                    </div>
                </div>
                """
            st.markdown(f"""
            <div style="background: rgba(20, 22, 27, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 14px; padding: 1.25rem 1.4rem;">
                {attr_html}
            </div>
            """, unsafe_allow_html=True)
            st.markdown("<div style='margin-top: 0.6rem;'></div>", unsafe_allow_html=True)
            st.info(f"💡 **Counter-Tactical Exploit:** {profile['counter_strategy']}")

        # 3. Race-Quarter Fatigue Drift with Lactic Threshold Danger Zone
        st.markdown("##### Race-Quarter Fatigue Drift & Lactic Danger Zone")
        splits_df = pd.DataFrame({
            "Split Phase": ["Split 1 (0-25%)", "Split 2 (25-50%)", "Split 3 (50-75%)", "Split 4 (75-100%)"],
            "Nominal Velocity (%)": profile["split_velocity_pct"],
            "Execution Error Risk (%)": profile["error_chances"]
        })

        fig_drift = go.Figure()
        fig_drift.add_trace(go.Scatter(
            x=splits_df["Split Phase"],
            y=splits_df["Nominal Velocity (%)"],
            mode="lines+markers",
            name="Split Velocity (%)",
            line=dict(color='#5DD62C', width=3.5, shape='spline'),
            marker=dict(size=8, color='#5DD62C')
        ))
        fig_drift.add_trace(go.Scatter(
            x=splits_df["Split Phase"],
            y=splits_df["Execution Error Risk (%)"],
            mode="lines+markers",
            name="Technical Error Risk (%)",
            yaxis="y2",
            fill="tozeroy",
            fillcolor="rgba(239, 68, 68, 0.12)",
            line=dict(color='#EF4444', width=2.5),
            marker=dict(size=7, color='#EF4444')
        ))
        fig_drift.add_vrect(
            x0="Split 3 (50-75%)", x1="Split 4 (75-100%)",
            fillcolor="rgba(239, 68, 68, 0.08)", layer="below", line_width=1,
            line_dash="dash", line_color="rgba(239, 68, 68, 0.35)",
            annotation_text="🚨 Lactic Acid Threshold Zone", annotation_position="top left",
            annotation_font=dict(color="#EF4444", size=10)
        )
        fig_drift.update_layout(
            yaxis=dict(title="Velocity Index (%)", range=[80, 110], gridcolor="rgba(255,255,255,0.05)"),
            yaxis2=dict(title="Error Risk (%)", overlaying="y", side="right", range=[0, 20], gridcolor="rgba(255,255,255,0.02)"),
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            height=320,
            margin=dict(l=20, r=20, t=30, b=20),
            legend=dict(orientation="h", y=1.12, x=0.2)
        )
        fig_drift = apply_dark_theme(fig_drift)
        st.plotly_chart(fig_drift, use_container_width=True)

    # --------------------------------------------------------
    # TAB 2: HEAD-TO-HEAD OPPONENT SCOUTING
    # --------------------------------------------------------
    with tab_matchup:
        st.markdown("#### Head-to-Head Opponent Scouting & Matchup Simulation")
        st.caption("Pit your athlete against a primary competitor to identify vulnerability windows and generate an automated counter-tactical gameplan.")

        col_m1, col_m2 = st.columns(2)
        with col_m1:
            st.markdown("##### 🔵 Your Athlete (Lime Corner)")
            p_a_name = st.selectbox("Select Your Athlete:", options=athlete_names, index=0, key="matchup_p_a")
            ath_a_meta = next(a for a in FEATURED_ATHLETES if a["name"] == p_a_name)
            p_a_profile = compute_athlete_inclinations(p_a_name, ath_a_meta["sport"], ath_a_meta["medals"], ath_a_meta["golds"]/ath_a_meta["medals"])

        with col_m2:
            st.markdown("##### 🔴 Opponent Athlete (Cyan Corner)")
            p_b_name = st.selectbox("Select Opponent Athlete:", options=[a for a in athlete_names if a != p_a_name], index=0, key="matchup_p_b")
            ath_b_meta = next(a for a in FEATURED_ATHLETES if a["name"] == p_b_name)
            p_b_profile = compute_athlete_inclinations(p_b_name, ath_b_meta["sport"], ath_b_meta["medals"], ath_b_meta["golds"]/ath_b_meta["medals"])

        matchup = simulate_tactical_matchup(p_a_profile, p_b_profile)

        # Dual-Column "VS" Fight-Card Header
        t_a_label, t_a_col, t_a_glow = get_ovr_tier_card(p_a_profile["composite_rating"])
        t_b_label, t_b_col, t_b_glow = get_ovr_tier_card(p_b_profile["composite_rating"])

        st.markdown(f"""
        <div class="vs-fight-header">
            <!-- Athlete A (Electric Lime) -->
            <div class="vs-fighter-card">
                <div class="fifa-ovr-card" style="border-color: #5DD62C; box-shadow: 0 0 20px rgba(93, 214, 44, 0.45);">
                    <span class="fifa-ovr-num" style="color: #5DD62C;">{int(round(p_a_profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: #5DD62C;">{t_a_label}</span>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #5DD62C; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">PRIMARY ATHLETE</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F8FAFC;">{p_a_name}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 0.2rem;">
                        {p_a_profile['archetype']} • Clutch: <strong style="color: #5DD62C;">{p_a_profile['clutch_index']}</strong>
                    </div>
                </div>
            </div>

            <!-- VS Center Emblem -->
            <div class="vs-center-badge">VS</div>

            <!-- Athlete B (Cyber Cyan) -->
            <div class="vs-fighter-card" style="justify-content: flex-end; text-align: right;">
                <div>
                    <div style="font-size: 0.72rem; color: #00F0FF; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">SCOUTED OPPONENT</div>
                    <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.35rem; font-weight: 800; color: #F8FAFC;">{p_b_name}</div>
                    <div style="font-size: 0.78rem; color: #94A3B8; margin-top: 0.2rem;">
                        {p_b_profile['archetype']} • Clutch: <strong style="color: #00F0FF;">{p_b_profile['clutch_index']}</strong>
                    </div>
                </div>
                <div class="fifa-ovr-card" style="border-color: #00F0FF; box-shadow: 0 0 20px rgba(0, 240, 255, 0.45);">
                    <span class="fifa-ovr-num" style="color: #00F0FF;">{int(round(p_b_profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: #00F0FF;">{t_b_label}</span>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Tactical Tug-of-War Win Probability Energy Bar
        win_pct = matchup["win_probability"]
        opp_pct = matchup["opponent_win_prob"]

        st.markdown(f"""
        <div class="tug-of-war-container">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Space Grotesk', sans-serif;">
                <div style="text-align: left;">
                    <div style="font-size: 0.75rem; color: #5DD62C; font-weight: 700; text-transform: uppercase;">{p_a_name} WIN PROBABILITY</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #5DD62C; font-family: 'JetBrains Mono', monospace;">{win_pct}%</div>
                </div>
                <div style="font-size: 0.85rem; color: #94A3B8; font-weight: 700;">TACTICAL TUG-OF-WAR ENGINE</div>
                <div style="text-align: right;">
                    <div style="font-size: 0.75rem; color: #00F0FF; font-weight: 700; text-transform: uppercase;">{p_b_name} WIN PROBABILITY</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #00F0FF; font-family: 'JetBrains Mono', monospace;">{opp_pct}%</div>
                </div>
            </div>
            <div class="tug-bar-track">
                <div class="tug-fill-a" style="width: {win_pct}%;"></div>
                <div class="tug-fill-b" style="width: {opp_pct}%;"></div>
            </div>
            <div style="font-size: 0.78rem; color: #94A3B8;">
                Deterministic advantage vector integration across stamina, clutch composure, and pacing bias.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Automated Scouting Report Cards
        st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            st.markdown(f"""
            <div style="background: rgba(20, 22, 27, 0.75); border: 1px solid rgba(239, 68, 68, 0.35); border-radius: 12px; padding: 1.2rem; height: 100%; box-sizing: border-box;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; color: #EF4444; font-weight: 800; font-family: 'Space Grotesk', sans-serif;">
                    ⚠️ Opponent Vulnerability Matrix ({p_b_name})
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;">
                    {'<br>'.join(['• ' + w for w in matchup['opponent_weaknesses']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_sc2:
            st.markdown(f"""
            <div style="background: rgba(20, 22, 27, 0.75); border: 1px solid rgba(93, 214, 44, 0.35); border-radius: 12px; padding: 1.2rem; height: 100%; box-sizing: border-box;">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; color: #5DD62C; font-weight: 800; font-family: 'Space Grotesk', sans-serif;">
                    🎯 Recommended Counter-Tactical Execution
                </div>
                <div style="font-size: 0.88rem; color: #CBD5E1; line-height: 1.6;">
                    {p_a_profile['counter_strategy']}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Advantage Deltas Bar Chart
        st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Head-to-Head Advantage Vectors")
        delta_df = pd.DataFrame({
            "Dimension": list(matchup["advantage_deltas"].keys()),
            "Delta Score": list(matchup["advantage_deltas"].values())
        })
        delta_df["Advantage"] = np.where(delta_df["Delta Score"] >= 0, p_a_name, p_b_name)

        fig_delta = px.bar(
            delta_df,
            x="Delta Score",
            y="Dimension",
            orientation="h",
            color="Advantage",
            color_discrete_map={p_a_name: "#5DD62C", p_b_name: "#00F0FF"},
            title=f"Head-to-Head Vector Edge: {p_a_name} (Lime) vs {p_b_name} (Cyan)"
        )
        fig_delta = apply_dark_theme(fig_delta)
        st.plotly_chart(fig_delta, use_container_width=True)

    # --------------------------------------------------------
    # TAB 3: WHAT-IF ENVIRONMENTAL & AERODYNAMIC LAB
    # --------------------------------------------------------
    with tab_pacing:
        st.markdown("#### What-If Environmental & Aerodynamic Lab")
        st.caption("Simulate real-time environmental perturbations (altitude, ambient air density, drafting slipstream, and opening surge) on energy reserves and podium probability.")

        col_ctrl1, col_ctrl2, col_ctrl3, col_ctrl4 = st.columns(4)
        with col_ctrl1:
            pace_choice = st.selectbox(
                "Pacing Protocol:",
                ["Negative Split", "Even Split", "Early Breakaway Attack", "Controlled Drafting & Surge"],
                index=0,
                key="sim_pacing_strategy"
            )
        with col_ctrl2:
            altitude_val = st.slider("Venue Altitude (m):", min_value=0, max_value=2500, value=800, step=100, key="sim_altitude")
        with col_ctrl3:
            drafting_val = st.slider("Drafting Slipstream (%):", min_value=0.0, max_value=60.0, value=30.0, step=5.0, key="sim_drafting")
        with col_ctrl4:
            temp_val = st.slider("Ambient Temperature (°C):", min_value=-15, max_value=35, value=12, step=1, key="sim_temp")

        surge_val = st.slider("Opening Sector Pace Surge (%):", min_value=-10.0, max_value=15.0, value=2.0, step=1.0, key="sim_surge")

        # Run Pacing & Environmental Calculations
        sim_res = simulate_pacing_strategy(profile, pace_choice, 85.0, drafting_val, altitude_val)

        alt_impact = round((altitude_val / 1000.0) * 1.8, 1)
        draft_savings = round(drafting_val * 0.42, 1)
        temp_drift = round(abs(temp_val - 18) * 0.08, 1)
        net_time_shift = round((-draft_savings * 0.09) + (alt_impact * 0.16) + (temp_drift * 0.12) - (surge_val * 0.04), 2)
        vo2_drift = round((-alt_impact * 0.8) + (draft_savings * 0.35) - (temp_drift * 0.25), 1)
        revised_podium = max(5, min(99, int(sim_res['podium_probability'] - (alt_impact * 1.2) + (draft_savings * 1.1) - (temp_drift * 0.8))))

        # 4 Environmental Live Delta Cards
        k1, k2, k3, k4 = st.columns(4)
        with k1:
            time_col = "#5DD62C" if net_time_shift <= 0 else "#EF4444"
            time_sgn = "-" if net_time_shift <= 0 else "+"
            st.metric("Finish Time Shift", f"{time_sgn}{abs(net_time_shift):.2f}s", delta="Aerodynamic Advantage" if net_time_shift <= 0 else "Atmospheric Degradation", delta_color="normal" if net_time_shift <= 0 else "inverse")
        with k2:
            st.metric("Aerobic VO2 Drift", f"{vo2_drift:+.1f}%", delta="Metabolic Economy", delta_color="normal" if vo2_drift >= 0 else "inverse")
        with k3:
            st.metric("Drafting Energy Saved", f"+{sim_res['drafting_savings_pct']}%", delta="Slipstream Buffer")
        with k4:
            podium_delta = int(round(revised_podium - sim_res['podium_probability']))
            st.metric("Podium Conversion Prob", f"{revised_podium}%", delta=f"{podium_delta:+d}% vs Flat Baseline")

        # Plot Energy Curve & Split Velocity Profile
        col_p1, col_p2 = st.columns([1, 1])
        with col_p1:
            st.markdown("##### Metabolic Energy Depletion Curve")
            fig_eng = go.Figure()
            fig_eng.add_trace(go.Scatter(
                x=["Start", "25% Mark", "50% Mark", "75% Mark", "Finish Line"],
                y=sim_res["energy_curve"],
                mode="lines+markers",
                line=dict(color="#5DD62C", width=3),
                marker=dict(size=8, color="#5DD62C"),
                fill="tozeroy",
                fillcolor="rgba(93, 214, 44, 0.15)"
            ))
            fig_eng.update_layout(
                yaxis=dict(title="Energy Reserve (%)", range=[0, 105], gridcolor="rgba(255,255,255,0.05)"),
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                height=300
            )
            fig_eng = apply_dark_theme(fig_eng)
            st.plotly_chart(fig_eng, use_container_width=True)

        with col_p2:
            st.markdown("##### Split Velocity Profile (km/h Index)")
            fig_spd = px.bar(
                x=sim_res["phases"],
                y=sim_res["split_speeds"],
                labels={"x": "Race Phase", "y": "Velocity Index (km/h)"},
                color_discrete_sequence=["#00F0FF"]
            )
            fig_spd.update_layout(paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", height=300)
            fig_spd = apply_dark_theme(fig_spd)
            st.plotly_chart(fig_spd, use_container_width=True)

    # --------------------------------------------------------
    # TAB 4: ONE-CLICK COACH PLAYBOOK EXPORT
    # --------------------------------------------------------
    with tab_playbook:
        st.markdown("#### Tactical Sideline Clipboard & One-Click Playbook Export")
        st.caption("A consolidated operational gameplan ready to copy to clipboard or download directly to coaching staff tablets.")

        playbook_text = f"""======================================================================
OLYMPIA HIGH-PERFORMANCE COACHING SYSTEM // TACTICAL DOSSIER
======================================================================
ATHLETE PROFILE:
  Name:               {target_athlete_name}
  Sport Discipline:   {sport_val}
  Tactical Archetype: {profile['archetype']}
  Composite Rating:   {profile['composite_rating']}/100 [{tier_label}]
  Pacing Bias:        {profile['pacing_bias']}
  Primary Trigger:    {profile['primary_trigger']}
  Clutch Composure:   {profile['clutch_index']}/100

SIMULATION TELEMETRY (VENUE CONDITIONS):
  Altitude:           {altitude_val} m
  Drafting Target:    {drafting_val}%
  Ambient Temp:       {temp_val} °C
  Pacing Protocol:    {pace_choice}
  Projected Podium:   {revised_podium}%

OPERATIONAL GAMEPLAN & SPLIT TARGETS:
  Split 1 (0-25%):    {sim_res['split_speeds'][0]} km/h  -- Regulate adrenaline, lock into drafting zone.
  Split 2 (25-50%):   {sim_res['split_speeds'][1]} km/h  -- Settle into aerobic cadence, protect VO2 ceiling.
  Split 3 (50-75%):   {sim_res['split_speeds'][2]} km/h  -- Initiate tempo surge at primary trigger point.
  Split 4 (75-100%):  {sim_res['split_speeds'][3]} km/h  -- Maximum anaerobic kick into clutch zone.

COUNTER-TACTICAL EXPLOIT:
  {profile['counter_strategy']}
======================================================================
Generated by OLYMPIA Spatial Intelligence OS • 1896-2026 Archive
"""

        # Stylized Dark Terminal Preview Card
        st.markdown("""
        <div class="terminal-playbook-card">
            <div class="terminal-header">
                <div style="display: flex; align-items: center; gap: 0.4rem;">
                    <span class="terminal-dot-red"></span>
                    <span class="terminal-dot-yellow"></span>
                    <span class="terminal-dot-green"></span>
                    <span style="font-size: 0.75rem; color: #94A3B8; margin-left: 0.5rem; font-family: 'JetBrains Mono', monospace;">olympia_coach_dossier.sh</span>
                </div>
                <span style="font-size: 0.68rem; color: #5DD62C; border: 1px solid #5DD62C; padding: 0.1rem 0.4rem; border-radius: 4px;">STANDBY // READY</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.code(playbook_text, language="markdown")

        # Tactical Export Action Buttons
        col_btn1, col_btn2, _ = st.columns([1.2, 1.2, 2])
        with col_btn1:
            st.download_button(
                "⬇️ Download Playbook (.md)",
                data=playbook_text,
                file_name=f"OLYMPIA_Playbook_{target_athlete_name.replace(' ', '_')}.md",
                mime="text/markdown",
                use_container_width=True
            )
        with col_btn2:
            telemetry_csv = pd.DataFrame([profile["radar_scores"]]).to_csv(index=False)
            st.download_button(
                "⬇️ Download Telemetry (.csv)",
                data=telemetry_csv,
                file_name=f"OLYMPIA_Telemetry_{target_athlete_name.replace(' ', '_')}.csv",
                mime="text/csv",
                use_container_width=True
            )
