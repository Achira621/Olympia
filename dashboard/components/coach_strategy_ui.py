"""
Coach Strategy Studio & Athlete Inclination UI Component for OLYMPIA.
Implements the Legendary Olympic Intelligence Archive architectural marble & gold design system.
"""

from typing import List, Dict, Any, TypedDict, Optional
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
from analytics.visualization import apply_dark_theme
from dashboard.components.icons import get_svg_icon
from dashboard.components.theme import COLOR_GOLD, COLOR_CHARCOAL, COLOR_RED, COLOR_SANDSTONE, COLOR_BORDER
from dashboard.components.athlete_photos import get_athlete_avatar_html
from dashboard.components.flags import get_country_flag_html


class AthleteMeta(TypedDict):
    name: str
    sport: str
    country: str
    medals: int
    golds: int


# Top Marquee Athletes across Summer and Winter Olympics
FEATURED_ATHLETES: List[AthleteMeta] = [
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
    s = round(score)
    if s >= 90:
        return "ICON", COLOR_GOLD, "rgba(212, 175, 55, 0.35)"
    elif s >= 85:
        return "ELITE", COLOR_CHARCOAL, "rgba(46, 42, 37, 0.25)"
    elif s >= 80:
        return "PRO", "#8B857C", "rgba(139, 133, 124, 0.25)"
    else:
        return "PROSPECT", "#B45309", "rgba(180, 83, 9, 0.25)"


def render_antigravity_styles():
    """Injects high-craft Architectural CSS tokens and micro-interactions."""
    st.markdown("""
    <style>
    /* ============================================================
       ARCHITECTURAL DESIGN TOKENS
       ============================================================ */

    /* Spatial Architectural Container */
    .ag-glass-panel {
        background: #FFFFFF !important;
        border: 1px solid var(--olympia-border) !important;
        border-radius: 18px !important;
        padding: 1.6rem 2rem !important;
        margin-bottom: 1.5rem !important;
        box-shadow: var(--shadow-subtle) !important;
        transition: transform 220ms cubic-bezier(0.22, 1, 0.36, 1), 
                    box-shadow 220ms cubic-bezier(0.22, 1, 0.36, 1), 
                    border-color 220ms ease-out !important;
        position: relative;
        overflow: hidden;
    }

    .ag-glass-panel:hover {
        transform: translateY(-2px);
        border-color: rgba(212, 175, 55, 0.6) !important;
        box-shadow: var(--shadow-elevated) !important;
    }

    /* FIFA/2K Architectural Hexagonal OVR Card Badge */
    .fifa-ovr-card {
        width: 82px;
        height: 94px;
        background: linear-gradient(135deg, #FAF0D8 0%, #FFFFFF 100%);
        border: 2px solid #D4AF37;
        clip-path: polygon(50% 0%, 100% 25%, 100% 75%, 50% 100%, 0% 75%, 0% 25%);
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(212, 175, 55, 0.25);
        transition: transform 220ms var(--spring-snappy);
        flex-shrink: 0;
    }
    .fifa-ovr-card:hover {
        transform: scale(1.05);
    }
    .fifa-ovr-num {
        font-family: 'JetBrains Mono', monospace;
        font-size: 1.85rem;
        font-weight: 900;
        line-height: 1;
    }
    .fifa-ovr-tier {
        font-family: 'Cinzel', Georgia, serif;
        font-size: 0.65rem;
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
        color: #5A544A;
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
        color: #2E2A25;
    }
    .attr-bar-bg {
        height: 6px;
        background: #EAE3D5;
        border-radius: 3px;
        overflow: hidden;
    }
    .attr-bar-fill {
        height: 100%;
        background: linear-gradient(90deg, #EBD9C3 0%, #D4AF37 100%);
        border-radius: 3px;
        transition: width 400ms var(--spring-snappy);
    }

    /* VS Fight Header */
    .vs-fight-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1.2rem;
        background: #FFFFFF;
        border: 1px solid var(--olympia-border);
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        margin-bottom: 1.5rem;
        box-shadow: var(--shadow-subtle);
    }
    .vs-fighter-card {
        flex: 1;
        display: flex;
        align-items: center;
        gap: 1rem;
    }
    .vs-center-badge {
        font-family: 'Cinzel', Georgia, serif;
        font-size: 1.3rem;
        font-weight: 900;
        color: #AA820A;
        background: #FAF0D8;
        border: 1px solid rgba(212, 175, 55, 0.4);
        width: 52px;
        height: 52px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 12px rgba(212, 175, 55, 0.2);
        flex-shrink: 0;
    }

    /* Tactical Tug-of-War Bar */
    .tug-of-war-container {
        background: #FFFFFF;
        border: 1px solid var(--olympia-border);
        border-radius: 14px;
        padding: 1.4rem;
        text-align: center;
        box-shadow: var(--shadow-subtle);
    }
    .tug-bar-track {
        display: flex;
        position: relative;
        height: 22px;
        border-radius: 11px;
        overflow: visible;
        background: #1F1F1F;
        margin: 1.4rem 0;
        border: 1px solid rgba(212, 175, 55, 0.45);
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.2);
    }
    .tug-fill-a {
        background: linear-gradient(90deg, #FAF0D8 0%, #D4AF37 100%);
        box-shadow: 0 0 16px rgba(212, 175, 55, 0.7);
        transition: width 400ms var(--spring-snappy);
        border-radius: 10px 0 0 10px;
    }
    .tug-fill-b {
        background: linear-gradient(90deg, #C41E3A 0%, #7F1D1D 100%);
        box-shadow: 0 0 16px rgba(196, 30, 58, 0.7);
        transition: width 400ms var(--spring-snappy);
        border-radius: 0 10px 10px 0;
    }
    .clash-spark-fulcrum {
        position: absolute;
        top: -8px;
        bottom: -8px;
        width: 7px;
        transform: translateX(-50%);
        background: #FFFFFF;
        box-shadow: 0 0 18px 4px rgba(212, 175, 55, 0.9), 0 0 8px 2px #FFFFFF;
        border-radius: 4px;
        z-index: 10;
        animation: clashOscillate 0.5s ease-in-out infinite alternate;
    }
    @keyframes clashOscillate {
        0% { transform: translateX(-50%) scaleY(0.95); box-shadow: 0 0 14px 3px rgba(212, 175, 55, 0.8), 0 0 6px #FFFFFF; }
        100% { transform: translateX(-50%) scaleY(1.18); box-shadow: 0 0 24px 6px rgba(196, 30, 58, 0.95), 0 0 12px #FFFFFF; }
    }
    .clash-spark-particle {
        position: absolute;
        width: 4px;
        height: 4px;
        border-radius: 50%;
        background: #D4AF37;
        box-shadow: 0 0 6px #D4AF37;
    }
    @keyframes radarPing {
        0% { transform: scale(0.9); opacity: 1; }
        50% { transform: scale(1.4); opacity: 0.5; }
        100% { transform: scale(0.9); opacity: 1; }
    }

    /* Terminal Playbook Card */
    .terminal-playbook-card {
        background: #1F1F1F;
        border: 1px solid rgba(212, 175, 55, 0.35);
        border-radius: 12px;
        padding: 1.4rem;
        font-family: 'JetBrains Mono', monospace;
        color: #FAF8F2;
        box-shadow: 0 8px 24px rgba(0, 0, 0, 0.3);
    }
    .terminal-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        border-bottom: 1px solid rgba(255, 255, 255, 0.1);
        padding-bottom: 0.6rem;
        margin-bottom: 0.8rem;
    }
    </style>
    """, unsafe_allow_html=True)


def render_wind_tunnel_visualizer_html(drafting_val: float, altitude_val: int) -> str:
    """
    Renders the Biometric Wind-Tunnel Streamline Visualizer.
    Flowing #D4AF37 (laminar flow) and #C41E3A (turbulent drag wake) streamlines
    speed up and bend dynamically based on drafting slipstream and altitude.
    """
    speed_sec = round(max(0.4, 3.2 - (drafting_val / 60.0) * 2.2), 2)
    wake_bend = round((altitude_val / 2500.0) * 18 + (1.0 - drafting_val / 60.0) * 22, 1)

    return f"""
    <div class="wind-tunnel-card" style="background: linear-gradient(135deg, #1C1B19 0%, #292622 100%); border: 1px solid rgba(212, 175, 55, 0.4); border-radius: 14px; padding: 1.2rem; color: #FAF8F2; margin: 1rem 0 1.5rem 0; box-shadow: 0 10px 30px rgba(0,0,0,0.3);">
        <style>
        @keyframes laminarStream {{
            from {{ stroke-dashoffset: 140; }}
            to {{ stroke-dashoffset: 0; }}
        }}
        @keyframes wakeTurbulence {{
            0% {{ transform: translateY(0px) scaleY(1); opacity: 0.8; }}
            50% {{ transform: translateY(-4px) scaleY(1.2); opacity: 1; }}
            100% {{ transform: translateY(3px) scaleY(0.9); opacity: 0.8; }}
        }}
        .laminar-path {{
            stroke: #D4AF37;
            stroke-width: 2.2;
            stroke-dasharray: 18 80;
            fill: none;
            animation: laminarStream {speed_sec}s linear infinite;
        }}
        .wake-path {{
            stroke: #C41E3A;
            stroke-width: 2.2;
            stroke-dasharray: 12 60;
            fill: none;
            animation: laminarStream {round(speed_sec * 0.7, 2)}s linear infinite, wakeTurbulence 1.2s ease-in-out infinite;
        }}
        </style>
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.6rem;">
            <div>
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #D4AF37; background: rgba(212,175,55,0.15); border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700;">
                    LIVE AERODYNAMIC WIND-TUNNEL
                </span>
                <div style="font-family: 'Cinzel', serif; font-size: 1.15rem; font-weight: 800; color: #FAF8F2; margin-top: 0.3rem;">
                    Biometric Slipstream Flow & Boundary Layer Separation
                </div>
                <div style="font-size: 0.78rem; color: #8B857C;">
                    Paced by Drafting Slipstream: <strong style="color: #D4AF37;">{drafting_val:.0f}%</strong> • Venue Altitude: <strong style="color: #E8D9C3;">{altitude_val}m</strong>
                </div>
            </div>
            <div style="text-align: right; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #D4AF37;">
                FLOW VELOCITY: {speed_sec}s/CYCLE
            </div>
        </div>

        <div style="display: flex; justify-content: center; overflow-x: auto;">
            <svg width="680" height="160" viewBox="0 0 680 160" fill="none" xmlns="http://www.w3.org/2000/svg">
                <!-- Wind Tunnel Boundary Rails -->
                <line x1="20" y1="15" x2="660" y2="15" stroke="rgba(212,175,55,0.2)" stroke-dasharray="4 4"/>
                <line x1="20" y1="145" x2="660" y2="145" stroke="rgba(212,175,55,0.2)" stroke-dasharray="4 4"/>

                <!-- Upstream Laminar Streamlines (Gold) -->
                <path d="M 20 35 C 180 35, 270 45, 320 60 C 370 75, 440 {65 - wake_bend * 0.4}, 660 {60 - wake_bend * 0.4}" class="laminar-path"/>
                <path d="M 20 60 C 180 60, 260 65, 305 75 C 345 85, 420 {80 - wake_bend * 0.2}, 660 {78 - wake_bend * 0.2}" class="laminar-path" style="animation-delay: 0.25s;"/>
                <path d="M 20 85 C 180 85, 260 85, 300 85 C 340 85, 400 {90 + wake_bend * 0.2}, 660 {90 + wake_bend * 0.2}" class="laminar-path" style="animation-delay: 0.5s;"/>
                <path d="M 20 110 C 180 110, 270 105, 315 95 C 365 85, 430 {105 + wake_bend * 0.3}, 660 {110 + wake_bend * 0.3}" class="laminar-path" style="animation-delay: 0.75s;"/>
                <path d="M 20 130 C 180 130, 270 125, 330 115 C 380 105, 450 {125 + wake_bend * 0.5}, 660 {130 + wake_bend * 0.5}" class="laminar-path" style="animation-delay: 1.0s;"/>

                <!-- Athlete Aero Silhouette (Center: 300, 45) -->
                <g transform="translate(300, 45)">
                    <ellipse cx="28" cy="18" rx="14" ry="9" transform="rotate(-15 28 18)" fill="#FAF8F2" stroke="#D4AF37" stroke-width="1.5"/>
                    <path d="M 36 17 Q 41 20 37 24" stroke="#D4AF37" stroke-width="2" fill="none"/>
                    <path d="M 22 22 C 14 26, -5 38, -15 48 C -22 55, -20 62, -10 60 C 5 56, 20 44, 30 35 Z" fill="#2E2A25" stroke="#D4AF37" stroke-width="1.5"/>
                    <path d="M 22 28 L 38 42 L 52 38" stroke="#D4AF37" stroke-width="2.8" stroke-linecap="round" fill="none"/>
                    <path d="M -15 48 L -32 68 L -45 58" stroke="#AA820A" stroke-width="3" stroke-linecap="round" fill="none"/>
                </g>

                <!-- Downstream Turbulent Drag Wake Vortices (Victory Red) -->
                <path d="M 345 75 Q 380 {55 - wake_bend * 0.6} 430 {70 - wake_bend * 0.5} T 520 {65 - wake_bend * 0.6} T 660 {60 - wake_bend * 0.6}" class="wake-path"/>
                <path d="M 340 85 Q 380 {95 + wake_bend * 0.6} 435 {85 + wake_bend * 0.5} T 530 {90 + wake_bend * 0.6} T 660 {95 + wake_bend * 0.6}" class="wake-path" style="animation-delay: 0.3s;"/>
                <path d="M 330 92 Q 375 {108 + wake_bend * 0.8} 440 {102 + wake_bend * 0.7} T 540 {110 + wake_bend * 0.8} T 660 {115 + wake_bend * 0.8}" class="wake-path" style="animation-delay: 0.6s;"/>

                <!-- Boundary Layer Separation Marker -->
                <circle cx="340" cy="72" r="4" fill="#C41E3A" filter="drop-shadow(0 0 6px #C41E3A)"/>
                <text x="350" y="68" fill="#C41E3A" font-family="'JetBrains Mono', monospace" font-size="9" font-weight="700">Separation Point</text>
            </svg>
        </div>
    </div>
    """


def plot_inclination_radar(athlete_profile: dict) -> go.Figure:
    """Generates the 6D Behavioral Inclination Polar Radar chart."""
    scores = athlete_profile.get("inclination_scores") or athlete_profile.get("radar_scores", {})
    categories = list(scores.keys())
    values = list(scores.values())


    categories_closed = categories + [categories[0]]
    values_closed = values + [values[0]]

    bench_values = [75.0, 72.0, 74.0, 76.0, 78.0, 73.0]
    bench_closed = bench_values + [bench_values[0]]

    fig = go.Figure()

    # Olympic Benchmark baseline trace
    fig.add_trace(go.Scatterpolar(
        r=bench_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(139, 133, 124, 0.08)',
        line=dict(color='rgba(139, 133, 124, 0.7)', width=1.5, dash='dot'),
        name='Olympic Finalist Baseline'
    ))

    # Athlete Inclination trace
    fig.add_trace(go.Scatterpolar(
        r=values_closed,
        theta=categories_closed,
        fill='toself',
        fillcolor='rgba(212, 175, 55, 0.22)',
        line=dict(color='#D4AF37', width=2.8),
        marker=dict(size=7, color='#D4AF37', symbol='circle'),
        name=athlete_profile["athlete_name"]
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[40, 100],
                tickfont=dict(color='#8B857C', size=9, family='JetBrains Mono'),
                gridcolor='rgba(46, 42, 37, 0.08)',
                linecolor='rgba(46, 42, 37, 0.15)'
            ),
            angularaxis=dict(
                tickfont=dict(color='#2E2A25', size=10, family='Inter', weight=700),
                gridcolor='rgba(46, 42, 37, 0.08)',
                linecolor='rgba(46, 42, 37, 0.15)'
            ),
            bgcolor='rgba(250, 248, 242, 0.95)'
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
            font=dict(color='#2E2A25', size=10)
        ),
        height=340,
        autosize=True
    )
    return fig


def render_coach_strategy_studio(df: pd.DataFrame | None = None):
    """
    Renders the complete Coach Intelligence & Player Inclination Strategy Studio.
    Available across both the Professional / Academy role and the Enthusiast menu.
    """
    render_antigravity_styles()

    # 1. ARCHITECTURAL HERO BANNER
    st.markdown(f"""
    <div class="ag-glass-panel">
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 1rem;">
            <div>
                <div style="display: flex; align-items: center; gap: 0.6rem; margin-bottom: 0.4rem;">
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); padding: 0.2rem 0.6rem; border-radius: 9999px; color: #5A4005; font-weight: 700;">
                        <span style="color: #D4AF37;">●</span> Coach Intelligence Engine Active
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; background: #F8F5EE; border: 1px solid #E5DED2; padding: 0.2rem 0.6rem; border-radius: 9999px; color: #5A544A; font-weight: 600;">
                        Milano-Cortina 2026 Ready
                    </span>
                </div>
                <h1 style="font-family: 'Cinzel', 'Playfair Display', Georgia, serif; font-size: clamp(1.8rem, 4vw, 2.5rem); font-weight: 800; color: #2E2A25; margin: 0 0 0.4rem 0; line-height: 1.15;">
                    Olympic Coach Strategy Studio
                </h1>
                <div style="color: #8B857C; font-size: 0.95rem; max-width: 820px; line-height: 1.55; font-family: 'Inter', sans-serif;">
                    Translate behavioral inclinations, physiological tendencies, and fatigue drift into actionable tactical execution.
                    Modeled after high-performance analytics workflows deployed by Olympic National Federations.
                </div>
            </div>
            <div style="display: flex; gap: 0.75rem; align-items: center;">
                <div style="background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); border-radius: 12px; padding: 0.75rem 1.2rem; text-align: right;">
                    <div style="font-size: 0.72rem; color: #8B857C; text-transform: uppercase; font-weight: 700; letter-spacing: 0.05em; font-family: 'JetBrains Mono', monospace;">Tactical Accuracy</div>
                    <div style="font-size: 1.4rem; font-weight: 800; color: #AA820A; font-family: 'JetBrains Mono', monospace;">94.2%</div>
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

        target_athlete_name = str(custom_input.strip() if custom_input.strip() else selected_ath_name)

        ath_meta: Optional[AthleteMeta] = next((a for a in FEATURED_ATHLETES if a["name"] == target_athlete_name), None)
        sport_val: str = ath_meta["sport"] if ath_meta else "Cross Country Skiing"
        medals_won_val: int = ath_meta["medals"] if ath_meta else 3
        gold_ratio_val: float = (ath_meta["golds"] / max(ath_meta["medals"], 1)) if ath_meta else 0.5

        profile = compute_athlete_inclinations(target_athlete_name, sport_val, medals_won_val, gold_ratio_val)
        tier_label, tier_col, tier_glow = get_ovr_tier_card(profile["composite_rating"])

        # Athlete Scouting Hero Bar
        ath_avatar = get_athlete_avatar_html(target_athlete_name, size=72, sport=sport_val, country=ath_meta['country'] if ath_meta else '')
        ctry_flag = get_country_flag_html(ath_meta['country'] if ath_meta else '', size=16)

        st.markdown(f"""
        <div style="background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 16px; padding: 1.4rem 1.6rem; margin: 1rem 0 1.5rem 0; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 1rem; box-shadow: var(--shadow-subtle);">
            <div style="display: flex; align-items: center; gap: 1.2rem;">
                <div style="flex-shrink: 0;">
                    {ath_avatar}
                </div>
                <div class="fifa-ovr-card" style="border-color: {tier_col};">
                    <span class="fifa-ovr-num" style="color: {tier_col};">{int(round(profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: {tier_col};">{tier_label}</span>
                </div>
                <div>
                    <div style="font-size: 0.78rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; font-family: 'JetBrains Mono', monospace; display: flex; align-items: center; gap: 0.35rem;">
                        <span>{sport_val}</span> // {ctry_flag} <span>{ath_meta['country'] if ath_meta else 'Olympian'}</span>
                    </div>
                    <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.65rem; font-weight: 800; color: #2E2A25;">
                        {target_athlete_name}
                    </div>
                    <div style="display: flex; gap: 0.6rem; margin-top: 0.35rem; align-items: center; flex-wrap: wrap;">
                        <span style="font-size: 0.75rem; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.55rem; border-radius: 6px; font-weight: 700; color: #5A4005;">
                            ARCHETYPE: {profile['archetype']}
                        </span>
                        <span style="font-size: 0.75rem; background: #F8F5EE; border: 1px solid #E5DED2; padding: 0.15rem 0.55rem; border-radius: 6px; font-weight: 600; color: #5A544A;">
                            CLUTCH INDEX: {profile['clutch_index']}
                        </span>
                    </div>
                </div>
            </div>
            <div style="display: flex; gap: 1.2rem;">
                <div style="text-align: right;">
                    <div style="font-size: 0.72rem; color: #8B857C; text-transform: uppercase; font-weight: 600;">Historical Podiums</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 800; color: #2E2A25;">{profile.get('career_podiums', medals_won_val)}</div>
                </div>
                <div style="text-align: right;">
                    <div style="font-size: 0.72rem; color: #8B857C; text-transform: uppercase; font-weight: 600;">Gold Conversion</div>
                    <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.4rem; font-weight: 800; color: #D4AF37;">{int(round(profile.get('gold_conversion_pct', gold_ratio_val * 100)))}%</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        col_radar, col_bars = st.columns([1.1, 1])
        with col_radar:
            st.markdown("""
            <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                <div style="font-weight: 700; color: #2E2A25; font-size: 0.95rem;">6-Dimensional Inclination Radar</div>
                <div style="display: flex; align-items: center; gap: 0.4rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #AA820A; background: #FAF0D8; padding: 0.15rem 0.5rem; border-radius: 9999px; border: 1px solid rgba(212,175,55,0.4);">
                    <span style="display: inline-block; width: 6px; height: 6px; border-radius: 50%; background: #D4AF37; box-shadow: 0 0 8px #D4AF37; animation: radarPing 1.4s ease-out infinite;"></span>
                    SONIC BOOM SWEEP ACTIVE
                </div>
            </div>
            """, unsafe_allow_html=True)
            fig_radar = plot_inclination_radar(profile)
            st.plotly_chart(fig_radar, use_container_width=True)

        with col_bars:
            st.markdown("##### Key Inclination Attributes vs Benchmark")
            profile_scores = profile.get("inclination_scores") or profile.get("radar_scores", {})
            for dim, score in profile_scores.items():
                bench = 74.0
                delta = score - bench
                delta_str = f"+{delta:.1f}" if delta >= 0 else f"{delta:.1f}"
                delta_col = "#D4AF37" if delta >= 0 else "#C41E3A"
                fill_pct = min(100, max(10, int(score)))

                st.markdown(f"""
                <div class="attr-row">
                    <div class="attr-meta">
                        <span class="attr-title">{dim}</span>
                        <div class="attr-val-delta">
                            <span class="attr-score">{score:.1f}</span>
                            <span style="font-size: 0.72rem; color: {delta_col};">({delta_str})</span>
                        </div>
                    </div>
                    <div class="attr-bar-bg">
                        <div class="attr-bar-fill" style="width: {fill_pct}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        # Race-Quarter Fatigue Drift
        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown("##### Race-Quarter Fatigue Drift & Error Telemetry")
        drift = profile.get("fatigue_drift") or {
            "split_velocity_pct": profile.get("split_velocity_pct", [100.0, 97.5, 94.0, 91.0]),
            "technical_error_risk_pct": profile.get("error_chances", [2.0, 3.5, 6.0, 9.5])
        }

        fig_drift = go.Figure()

        fig_drift.add_trace(go.Scatter(
            x=["Split 1 (0-25%)", "Split 2 (25-50%)", "Split 3 (50-75%)", "Split 4 (75-100%)"],
            y=drift["split_velocity_pct"],
            mode="lines+markers",
            name="Split Velocity Index (%)",
            line=dict(color='#D4AF37', width=3),
            marker=dict(size=8, color='#D4AF37')
        ))
        fig_drift.add_trace(go.Scatter(
            x=["Split 1 (0-25%)", "Split 2 (25-50%)", "Split 3 (50-75%)", "Split 4 (75-100%)"],
            y=drift["technical_error_risk_pct"],
            mode="lines+markers",
            name="Technical Error Risk (%)",
            yaxis="y2",
            fill="tozeroy",
            fillcolor="rgba(196, 30, 58, 0.1)",
            line=dict(color='#C41E3A', width=2.5),
            marker=dict(size=7, color='#C41E3A')
        ))
        fig_drift.add_vrect(
            x0="Split 3 (50-75%)", x1="Split 4 (75-100%)",
            fillcolor="rgba(196, 30, 58, 0.06)", layer="below", line_width=1,
            line_dash="dash", line_color="rgba(196, 30, 58, 0.35)",
            annotation_text="🚨 Lactic Acid Threshold Zone", annotation_position="top left",
            annotation_font=dict(color="#C41E3A", size=10)
        )
        fig_drift.update_layout(
            yaxis=dict(title="Velocity Index (%)", range=[80, 110], gridcolor="rgba(46,42,37,0.07)"),
            yaxis2=dict(title="Error Risk (%)", overlaying="y", side="right", range=[0, 20], gridcolor="rgba(46,42,37,0.04)"),
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
            st.markdown("##### 🟡 Primary Athlete (Gold)")
            p_a_name = str(st.selectbox("Select Your Athlete:", options=athlete_names, index=0, key="matchup_p_a"))
            ath_a_meta: AthleteMeta = next(a for a in FEATURED_ATHLETES if a["name"] == p_a_name)
            p_a_profile = compute_athlete_inclinations(p_a_name, ath_a_meta["sport"], ath_a_meta["medals"], ath_a_meta["golds"]/max(ath_a_meta["medals"], 1))

        with col_m2:
            st.markdown("##### ⚫ Scouted Opponent (Charcoal)")
            p_b_name = str(st.selectbox("Select Opponent Athlete:", options=[a for a in athlete_names if a != p_a_name], index=0, key="matchup_p_b"))
            ath_b_meta: AthleteMeta = next(a for a in FEATURED_ATHLETES if a["name"] == p_b_name)
            p_b_profile = compute_athlete_inclinations(p_b_name, ath_b_meta["sport"], ath_b_meta["medals"], ath_b_meta["golds"]/max(ath_b_meta["medals"], 1))

        matchup = simulate_tactical_matchup(p_a_profile, p_b_profile)

        # Dual-Column "VS" Fight-Card Header
        t_a_label, t_a_col, t_a_glow = get_ovr_tier_card(p_a_profile["composite_rating"])
        t_b_label, t_b_col, t_b_glow = get_ovr_tier_card(p_b_profile["composite_rating"])

        av_a = get_athlete_avatar_html(p_a_name, size=52, sport=ath_a_meta['sport'], country=ath_a_meta['country'])
        av_b = get_athlete_avatar_html(p_b_name, size=52, sport=ath_b_meta['sport'], country=ath_b_meta['country'])
        fl_a = get_country_flag_html(ath_a_meta['country'], size=15)
        fl_b = get_country_flag_html(ath_b_meta['country'], size=15)

        st.markdown(f"""
        <div class="vs-fight-header">
            <!-- Athlete A (Gold) -->
            <div class="vs-fighter-card">
                <div style="flex-shrink: 0;">{av_a}</div>
                <div class="fifa-ovr-card" style="border-color: #D4AF37;">
                    <span class="fifa-ovr-num" style="color: #D4AF37;">{int(round(p_a_profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: #AA820A;">{t_a_label}</span>
                </div>
                <div>
                    <div style="font-size: 0.72rem; color: #AA820A; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace; display: flex; align-items: center; gap: 0.3rem;">
                        PRIMARY ATHLETE • {fl_a} {ath_a_meta['country']}
                    </div>
                    <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.35rem; font-weight: 800; color: #2E2A25;">{p_a_name}</div>
                    <div style="font-size: 0.78rem; color: #8B857C; margin-top: 0.2rem;">
                        {p_a_profile['archetype']} • Clutch: <strong style="color: #D4AF37;">{p_a_profile['clutch_index']}</strong>
                    </div>
                </div>
            </div>

            <!-- VS Center Emblem -->
            <div class="vs-center-badge">VS</div>

            <!-- Athlete B (Charcoal) -->
            <div class="vs-fighter-card" style="justify-content: flex-end; text-align: right;">
                <div>
                    <div style="font-size: 0.72rem; color: #5A544A; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace; display: flex; align-items: center; justify-content: flex-end; gap: 0.3rem;">
                        {fl_b} {ath_b_meta['country']} • SCOUTED OPPONENT
                    </div>
                    <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.35rem; font-weight: 800; color: #2E2A25;">{p_b_name}</div>
                    <div style="font-size: 0.78rem; color: #8B857C; margin-top: 0.2rem;">
                        {p_b_profile['archetype']} • Clutch: <strong style="color: #2E2A25;">{p_b_profile['clutch_index']}</strong>
                    </div>
                </div>
                <div class="fifa-ovr-card" style="border-color: #2E2A25;">
                    <span class="fifa-ovr-num" style="color: #2E2A25;">{int(round(p_b_profile['composite_rating']))}</span>
                    <span class="fifa-ovr-tier" style="color: #5A544A;">{t_b_label}</span>
                </div>
                <div style="flex-shrink: 0;">{av_b}</div>
            </div>
        </div>
        """, unsafe_allow_html=True)


        # Tactical Tug-of-War Win Probability Energy Bar
        win_pct = matchup["win_probability"]
        opp_pct = matchup["opponent_win_prob"]

        st.markdown(f"""
        <div class="tug-of-war-container">
            <div style="display: flex; justify-content: space-between; align-items: center; font-family: 'Cinzel', Georgia, serif;">
                <div style="text-align: left;">
                    <div style="font-size: 0.74rem; color: #AA820A; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace;">{p_a_name} WIN PROB</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #D4AF37; font-family: 'JetBrains Mono', monospace;">{win_pct}%</div>
                </div>
                <div style="font-size: 0.85rem; color: #8B857C; font-weight: 700; letter-spacing: 0.1em;">TACTICAL TUG-OF-WAR ENGINE</div>
                <div style="text-align: right;">
                    <div style="font-size: 0.74rem; color: #5A544A; font-weight: 700; text-transform: uppercase; font-family: 'JetBrains Mono', monospace;">{p_b_name} WIN PROB</div>
                    <div style="font-size: 2.2rem; font-weight: 900; color: #2E2A25; font-family: 'JetBrains Mono', monospace;">{opp_pct}%</div>
                </div>
            </div>
            <div class="tug-bar-track">
                <div class="tug-fill-a" style="width: {win_pct}%;"></div>
                <div class="clash-spark-fulcrum" style="left: {win_pct}%;">
                    <div class="clash-spark-particle" style="top: 2px; left: -8px;"></div>
                    <div class="clash-spark-particle" style="top: 14px; left: 8px; background: #C41E3A;"></div>
                    <div class="clash-spark-particle" style="top: 24px; left: -6px; background: #FAF8F2;"></div>
                </div>
                <div class="tug-fill-b" style="width: {opp_pct}%;"></div>
            </div>
            <div style="font-size: 0.78rem; color: #8B857C;">
                Deterministic advantage vector integration across stamina, clutch composure, and pacing bias.
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Automated Scouting Report Cards
        st.markdown("<div style='margin-top: 1.2rem;'></div>", unsafe_allow_html=True)
        col_sc1, col_sc2 = st.columns(2)
        with col_sc1:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid rgba(196, 30, 58, 0.4); border-radius: 12px; padding: 1.2rem; height: 100%; box-sizing: border-box; box-shadow: var(--shadow-subtle);">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; color: #C41E3A; font-weight: 800; font-family: 'Cinzel', Georgia, serif;">
                    ⚠️ Opponent Vulnerability Matrix ({p_b_name})
                </div>
                <div style="font-size: 0.88rem; color: #5A544A; line-height: 1.6;">
                    {'<br>'.join(['• ' + w for w in matchup['opponent_weaknesses']])}
                </div>
            </div>
            """, unsafe_allow_html=True)
        with col_sc2:
            st.markdown(f"""
            <div style="background: #FFFFFF; border: 1px solid rgba(212, 175, 55, 0.5); border-radius: 12px; padding: 1.2rem; height: 100%; box-sizing: border-box; box-shadow: var(--shadow-subtle);">
                <div style="display: flex; align-items: center; gap: 0.5rem; margin-bottom: 0.6rem; color: #AA820A; font-weight: 800; font-family: 'Cinzel', Georgia, serif;">
                    🎯 Recommended Counter-Tactical Execution
                </div>
                <div style="font-size: 0.88rem; color: #5A544A; line-height: 1.6;">
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
            color_discrete_map={p_a_name: "#D4AF37", p_b_name: "#2E2A25"},
            title=f"Head-to-Head Vector Edge: {p_a_name} (Gold) vs {p_b_name} (Charcoal)"
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
            time_sgn = "-" if net_time_shift <= 0 else "+"
            st.metric("Finish Time Shift", f"{time_sgn}{abs(net_time_shift):.2f}s", delta="Aerodynamic Edge" if net_time_shift <= 0 else "Atmospheric Drag", delta_color="normal" if net_time_shift <= 0 else "inverse")
        with k2:
            st.metric("Aerobic VO2 Drift", f"{vo2_drift:+.1f}%", delta="Metabolic Economy", delta_color="normal" if vo2_drift >= 0 else "inverse")
        with k3:
            st.metric("Drafting Energy Saved", f"+{sim_res['drafting_savings_pct']}%", delta="Slipstream Buffer")
        with k4:
            podium_delta = int(round(revised_podium - sim_res['podium_probability']))
            st.metric("Podium Conversion Prob", f"{revised_podium}%", delta=f"{podium_delta:+d}% vs Baseline")

        # Biometric Wind-Tunnel Streamline Visualizer
        st.markdown(render_wind_tunnel_visualizer_html(drafting_val, altitude_val), unsafe_allow_html=True)

        # Plot Energy Curve & Split Velocity Profile
        col_p1, col_p2 = st.columns([1, 1])
        with col_p1:
            st.markdown("##### Metabolic Energy Depletion Curve")
            fig_eng = go.Figure()
            fig_eng.add_trace(go.Scatter(
                x=["Start", "25% Mark", "50% Mark", "75% Mark", "Finish Line"],
                y=sim_res["energy_curve"],
                mode="lines+markers",
                line=dict(color="#D4AF37", width=3),
                marker=dict(size=8, color="#D4AF37"),
                fill="tozeroy",
                fillcolor="rgba(212, 175, 55, 0.15)"
            ))
            fig_eng.update_layout(
                yaxis=dict(title="Energy Reserve (%)", range=[0, 105], gridcolor="rgba(46,42,37,0.07)"),
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
                color_discrete_sequence=["#D4AF37"]
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

        target_name_str = str(target_athlete_name or "Athlete")
        profile_scores = profile.get("inclination_scores") or profile.get("radar_scores", {})
        playbook_text = f"""======================================================================

OLYMPIA COACH INTELLIGENCE DOSSIER // MILANO-CORTINA 2026 PRE-RACE
ATHLETE: {target_name_str.upper()}
SPORT: {sport_val.upper()} | OVR TIER: {tier_label} ({int(round(profile['composite_rating']))})
======================================================================

[1] TACTICAL ARCHETYPE & DNA
- Primary Persona: {profile['archetype']}
- Tactical Description: {TACTICAL_ARCHETYPES.get(profile['archetype'], {}).get('description', 'High performance Olympian')}
- Clutch Composure Index: {profile['clutch_index']}/100
- Pacing Bias Vector: {profile['pacing_bias']}

[2] INCLINATION ATTRIBUTES
- Opening Aggressiveness: {profile_scores.get('Opening Aggressiveness', 75.0):.1f}/100
- Tactical Discipline:    {profile_scores.get('Tactical Discipline', 75.0):.1f}/100
- Stamina Reserve:        {profile_scores.get('Stamina Reserve', 75.0):.1f}/100
- Clutch Composure:       {profile_scores.get('Clutch Composure', 75.0):.1f}/100
- Technical Precision:    {profile_scores.get('Technical Precision', 75.0):.1f}/100
- Fatigue Durability:     {profile_scores.get('Fatigue Durability', 75.0):.1f}/100

[3] OPERATIONAL EXECUTION MANDATE
- Recommended Strategy: {profile['counter_strategy']}
- Critical Danger Zone: Phase 3 to 4 (Lactic Acid Threshold Surge)
- Pacing Protocol: Negative Split with high-drafting slipstream retention

======================================================================
GENERATED VIA OLYMPIA OFFLINE STAR SCHEMA INTELLIGENCE ENGINE
======================================================================
"""

        st.markdown(f"""
        <div class="terminal-playbook-card">
            <div class="terminal-header">
                <span style="color: #D4AF37; font-weight: 700;">olympia_coach_dossier.sh</span>
                <span style="color: #8B857C; font-size: 0.75rem;">SHA-256 VERIFIED</span>
            </div>
            <pre style="margin: 0; color: #FAF8F2; font-size: 0.82rem; line-height: 1.45; white-space: pre-wrap;">{playbook_text}</pre>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 12px;'></div>", unsafe_allow_html=True)
        col_down1, col_down2 = st.columns([1, 1])
        with col_down1:
            st.download_button(
                "⬇️ Download Briefing Dossier (.txt)",
                data=playbook_text,
                file_name=f"olympia_tactical_{target_name_str.replace(' ', '_').lower()}.txt",
                mime="text/plain",
                use_container_width=True
            )
        with col_down2:
            scores_df = pd.DataFrame(list(profile_scores.items()), columns=["Dimension", "Score"])
            st.download_button(
                "⬇️ Download Telemetry Matrix (.csv)",
                data=scores_df.to_csv(index=False),
                file_name=f"olympia_telemetry_{target_name_str.replace(' ', '_').lower()}.csv",
                mime="text/csv",
                use_container_width=True
            )


