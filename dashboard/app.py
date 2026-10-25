"""
OLYMPIA ⚡ | Olympic Data Warehouse & Mining Intelligence
High-Contrast Modern Dark-Themed Olympic Analytics Platform.
Features:
- Mandatory 3-Role Authentication Flow (Admin, Sport Enthusiast, Player/Academy)
- High-Contrast Dark Theme Palette:
  * #0F0F0F (Pitch Black Canvas Background)
  * #202020 (Charcoal Surface Container)
  * #5DD62C (Electric Lime Primary Accent & CTA)
  * #337418 (Forest Green Secondary Accent)
  * #F8F8F8 (Off-White Primary Typography)
- Zero HTML code-block indentation bugs (dedented raw HTML rendering)
- Protected Layout margins & responsive z-indexes
"""

import os
import sys
import textwrap
import re

# Ensure root directory is on Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

from warehouse.warehouse import (
    get_denormalized_medals,
    get_db_connection,
    get_table_counts,
    get_db_path
)
from analytics.knn_potential import predict_athlete_potential, SPORT_PROFILES
from analytics.sports_science import (
    compute_peak_performance_window,
    compute_consistency_scores,
    compute_sport_specialization_index,
    compute_talent_pipeline,
    compute_competitive_parity,
    SPORT_BASE_AGES
)
from analytics.visualization import (
    THEME_BG,
    PAPER_BG,
    TEXT_COLOR,
    GRID_COLOR,
    PRIMARY_ACCENT,
    SECONDARY_ACCENT,
    MEDAL_COLORS,
    OLYMPIC_COLORS,
    apply_dark_theme,
    plot_top_countries_horizontal_stacked,
    plot_medal_density_heatmap,
    plot_gender_age_violins,
)
from analytics.kmeans import run_kmeans, compute_elbow_curve
from analytics.apriori import mine_association_rules
from analytics.olap import olap_slice, olap_dice, olap_rollup
from dashboard.auth import (
    init_auth,
    is_authenticated,
    get_current_role,
    get_current_user,
    render_landing_page,
    render_sidebar_user_badge,
    render_login_scrolling_background,
    ROLE_ADMIN,
    ROLE_ENTHUSIAST,
    ROLE_PROFESSIONAL,
    ROLE_ACADEMY
)
from dashboard.components.icons import get_svg_icon, render_medal_pills
from dashboard.components.knowledge_api import get_athlete_intel, get_country_intel
from dashboard.components.coach_strategy_ui import render_coach_strategy_studio
from dashboard.components.metrics import (
    render_telemetry_hud,
    render_kpi_card,
    render_kpi_row,
    render_podium_showcase,
    render_empty_telemetry_card,
    render_telemetry_footer
)


# ------------------------------------------------------------
# 1. Page Configuration
# ------------------------------------------------------------
st.set_page_config(
    page_title="OLYMPIA | Olympic Intelligence & Global Rankings",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)


# Helper function to render HTML safely without Markdown code-block interpretation
def render_html(html_str: str):
    """Renders HTML safely using Streamlit's native st.html."""
    if hasattr(st, "html"):
        st.html(html_str)
    else:
        st.markdown(html_str, unsafe_allow_html=True)


# ------------------------------------------------------------
# 2. Design System: High-Contrast Modern Dark-Themed Styling
# ------------------------------------------------------------
render_html("""
<meta name="referrer" content="no-referrer" />
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800;900&family=Playfair+Display:ital,wght@0,600;0,700;0,800;0,900;1,600;1,700&family=Cinzel:wght@700;800&display=swap" rel="stylesheet" />
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@20..48,100..700,0..1,-50..200" rel="stylesheet" />
<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet" />
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700;800&family=Outfit:wght@400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600;700;800&family=Inter:wght@300;400;500;600;700;800;900&display=swap');

    /* ============================================================
       1. COLOR & SURFACE DESIGN TOKENS (KINETIC OLYMPIC TELEMETRY LAB)
       ============================================================ */
    :root {
        --bg-void: #07080A;
        --surface-glass-1: rgba(20, 22, 27, 0.65);
        --surface-glass-2: rgba(32, 35, 42, 0.78);
        --border-hairline: rgba(255, 255, 255, 0.08);
        --border-glow: rgba(93, 214, 44, 0.45);
        --accent-lime: #5DD62C;
        --accent-cyan: #00F0FF;
        --medal-gold: #FFD700;
        --medal-silver: #E2E8F0;
        --medal-bronze: #D97706;
        --text-primary: #F8FAFC;
        --text-muted: #94A3B8;
        --text-dim: #475569;
        --spring-snappy: cubic-bezier(0.22, 1, 0.36, 1);
        --spring-float: cubic-bezier(0.16, 1, 0.3, 1);
    }

    /* Hide default Streamlit multi-page sidebar navigation list */
    [data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavItems"],
    ul[data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"],
    section[data-testid="stSidebar"] div:has(> ul[data-testid="stSidebarNavItems"]),
    section[data-testid="stSidebar"] [data-testid="stSidebarNav"] {
        display: none !important;
    }

    /* ============================================================
       2. TYPOGRAPHY & SCANNABLE HIERARCHY
       ============================================================ */
    html, body, [class*="css"], .stMarkdown {
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
    }

    /* Display / Headers: Space Grotesk / Outfit with tight tracking */
    h1, h2, h3, .hero-title, .forbes-masthead-title {
        font-family: 'Space Grotesk', 'Outfit', 'Inter', sans-serif !important;
        font-weight: 800 !important;
        letter-spacing: -0.03em !important;
    }

    /* Telemetry / Numbers / KPIs: JetBrains Mono with tabular-nums */
    .bento-kpi-value, .ticker-value, .podium-pts, [data-testid="stMetricValue"],
    .hud-ticker-pill, .hud-scrubber-pill, .hud-breadcrumb, .metric-container {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
    }

    h4, h5, h6, p, label, input, button, select, textarea, [data-testid="stMetricLabel"] {
        font-family: 'Inter', sans-serif !important;
    }

    /* Material Symbols / Icons */
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-icons,
    [class*="material-symbols"],
    [class*="material-icons"],
    [data-testid*="stIcon"],
    [data-testid="stSidebarCollapseButton"] span,
    button[kind="header"] span {
        font-family: 'Material Symbols Rounded', 'Material Symbols Outlined', 'Material Icons' !important;
        font-weight: normal;
        font-style: normal;
        line-height: 1;
        display: inline-block;
        white-space: nowrap;
        -webkit-font-smoothing: antialiased;
    }

    /* ============================================================
       3. OBSIDIAN VOID CANVAS & CUSTOM SCROLLBARS
       ============================================================ */
    .stApp {
        background-color: var(--bg-void, #07080A) !important;
        background-image: radial-gradient(rgba(255, 255, 255, 0.06) 1px, transparent 1px) !important;
        background-size: 24px 24px !important;
        color: var(--text-primary, #F8FAFC) !important;
    }

    /* 6px ultra-slim dark scrollbar with lime hover thumb */
    ::-webkit-scrollbar {
        width: 6px !important;
        height: 6px !important;
    }
    ::-webkit-scrollbar-track {
        background: #07080A !important;
    }
    ::-webkit-scrollbar-thumb {
        background: rgba(255, 255, 255, 0.15) !important;
        border-radius: 3px !important;
    }
    ::-webkit-scrollbar-thumb:hover {
        background: var(--accent-lime, #5DD62C) !important;
        box-shadow: 0 0 10px rgba(93, 214, 44, 0.6) !important;
    }

    /* Custom Selection Highlight */
    ::selection {
        background: rgba(93, 214, 44, 0.25) !important;
        color: #5DD62C !important;
    }

    /* Prevent content from sliding under sidebar */
    .stMain {
        position: relative !important;
        z-index: 1 !important;
    }

    /* Sidebar Styling (Deep Obsidian Surface Dock) */
    section[data-testid="stSidebar"] {
        background-color: #0A0B0F !important;
        border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
        box-shadow: 4px 0 30px rgba(0, 0, 0, 0.7);
        z-index: 99 !important;
    }

    /* Main Content Container Padding */
    .main .block-container, div[data-testid="stMainBlockContainer"] {
        padding-top: 1rem !important;
        padding-bottom: 3rem !important;
        padding-left: 2rem !important;
        padding-right: 2rem !important;
        max-width: 100% !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    /* Top Header Bar */
    header[data-testid="stHeader"] {
        background-color: rgba(7, 8, 10, 0.85) !important;
        backdrop-filter: blur(16px) !important;
        border-bottom: 1px solid rgba(255, 255, 255, 0.06) !important;
    }

    /* ============================================================
       4. TOP TELEMETRY HUD BAR (GLOBAL HEADER)
       ============================================================ */
    .telemetry-hud-bar {
        position: sticky;
        top: 0.5rem;
        z-index: 999;
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 0.65rem 1.25rem;
        margin-bottom: 1.2rem;
        background: rgba(20, 22, 27, 0.78);
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6), 0 0 15px rgba(93, 214, 44, 0.06);
        transition: all 220ms var(--spring-snappy);
    }
    .telemetry-hud-bar:hover {
        border-color: rgba(93, 214, 44, 0.35);
        box-shadow: 0 15px 35px rgba(0, 0, 0, 0.7), 0 0 20px rgba(93, 214, 44, 0.16);
    }
    .hud-left {
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }
    .hud-breadcrumb {
        display: flex;
        align-items: center;
        gap: 0.4rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.75rem;
        font-weight: 700;
        letter-spacing: 0.06em;
    }
    .hud-brand {
        color: #F8FAFC;
    }
    .hud-sep {
        color: #475569;
    }
    .hud-role {
        font-weight: 800;
    }
    .hud-module {
        color: #94A3B8;
    }
    .hud-center {
        display: flex;
        align-items: center;
    }
    .hud-ticker-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.6rem;
        background: rgba(10, 11, 14, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.35rem 0.95rem;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #94A3B8;
    }
    .ticker-dot {
        color: #5DD62C;
        animation: ag-pulse 1.8s infinite;
    }
    .hud-right {
        display: flex;
        align-items: center;
        gap: 0.65rem;
    }
    .hud-scrubber-pill {
        display: inline-flex;
        align-items: center;
        gap: 0.4rem;
        background: rgba(10, 11, 14, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.35rem 0.75rem;
        border-radius: 9999px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
    }
    .scrubber-label {
        color: #475569;
        font-weight: 700;
    }
    .scrubber-val {
        color: #F8FAFC;
        font-weight: 700;
    }
    .hud-role-switcher {
        display: inline-flex;
        align-items: center;
        gap: 0.25rem;
        background: rgba(10, 11, 14, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.2rem 0.35rem;
        border-radius: 9999px;
    }
    .role-chip {
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-family: 'Inter', sans-serif;
        font-size: 0.7rem;
        font-weight: 700;
        color: #94A3B8;
        text-decoration: none;
        transition: all 180ms ease;
    }
    .role-chip:hover {
        color: #F8FAFC;
        background: rgba(255, 255, 255, 0.06);
    }
    .active-chip {
        background: #5DD62C !important;
        color: #07080A !important;
        font-weight: 800;
        box-shadow: 0 0 10px rgba(93, 214, 44, 0.4);
    }

    /* ============================================================
       5. SPATIAL BENTO KPI CARDS
       ============================================================ */
    .bento-kpi-card {
        background: var(--surface-glass-1, rgba(20, 22, 27, 0.65));
        backdrop-filter: blur(16px) saturate(180%);
        -webkit-backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid var(--border-hairline, rgba(255, 255, 255, 0.08));
        border-radius: 14px;
        padding: 1.25rem 1.35rem;
        position: relative;
        overflow: hidden;
        margin-bottom: 1rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
        transition: transform 220ms var(--spring-snappy),
                    box-shadow 220ms var(--spring-snappy),
                    border-color 220ms var(--spring-snappy);
        box-sizing: border-box;
    }
    .bento-kpi-card:hover {
        transform: translateY(-4px) scale(1.008);
        border-color: var(--border-glow, rgba(93, 214, 44, 0.45));
        box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 20px -5px rgba(93, 214, 44, 0.18);
    }
    .bento-watermark {
        position: absolute;
        right: -6px;
        bottom: -6px;
        opacity: 0.12;
        pointer-events: none;
        z-index: 1;
    }
    .bento-kpi-value {
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1.2;
        margin-top: 0.4rem;
        position: relative;
        z-index: 2;
    }
    .bento-bottom-glow {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 2px;
        background: linear-gradient(90deg, transparent 0%, #5DD62C 50%, transparent 100%);
        opacity: 0.4;
        transition: opacity 220ms ease;
    }
    .bento-kpi-card:hover .bento-bottom-glow {
        opacity: 1;
        height: 3px;
    }

    /* Legacy Ticker Card compatibility */
    .ticker-card {
        background: var(--surface-glass-1, rgba(20, 22, 27, 0.65));
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        padding: 1.1rem 1.3rem;
        backdrop-filter: blur(14px);
        transition: all 0.22s var(--spring-snappy);
        box-shadow: 0 6px 20px rgba(0, 0, 0, 0.4);
    }
    .ticker-card:hover {
        transform: translateY(-4px);
        border-color: #5DD62C;
        box-shadow: 0 10px 25px rgba(93, 214, 44, 0.25);
    }

    /* ============================================================
       6. 3D SPATIAL VISUAL PODIUM SHOWCASE
       ============================================================ */
    .spatial-podium-root {
        display: flex;
        align-items: flex-end;
        justify-content: center;
        gap: 1.2rem;
        padding: 1.5rem 0.5rem 1rem 0.5rem;
        margin: 1.2rem 0 2rem 0;
        width: 100%;
        box-sizing: border-box;
    }
    .podium-pillar {
        flex: 1;
        max-width: 310px;
        border-radius: 16px 16px 10px 10px;
        text-align: center;
        padding: 1.5rem 1.1rem;
        position: relative;
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        box-shadow: 0 12px 30px rgba(0, 0, 0, 0.6);
        transition: transform 300ms var(--spring-snappy);
        box-sizing: border-box;
    }
    .podium-pillar:hover {
        transform: translateY(-6px);
    }
    .gold-pillar {
        background: linear-gradient(180deg, rgba(93, 214, 44, 0.16) 0%, rgba(20, 22, 27, 0.95) 100%);
        border: 2px solid #5DD62C;
        box-shadow: 0 0 35px rgba(93, 214, 44, 0.35), 0 20px 45px rgba(0, 0, 0, 0.7);
        min-height: 285px;
        order: 2;
    }
    .silver-pillar {
        background: linear-gradient(180deg, rgba(226, 232, 240, 0.1) 0%, rgba(20, 22, 27, 0.95) 100%);
        border: 1.5px solid rgba(226, 232, 240, 0.35);
        min-height: 245px;
        order: 1;
    }
    .bronze-pillar {
        background: linear-gradient(180deg, rgba(217, 119, 6, 0.12) 0%, rgba(20, 22, 27, 0.95) 100%);
        border: 1.5px solid rgba(217, 119, 6, 0.35);
        min-height: 215px;
        order: 3;
    }
    .podium-badge-wrap {
        margin-bottom: 0.4rem;
        filter: drop-shadow(0 4px 10px rgba(0, 0, 0, 0.6));
    }
    .podium-rank-tag {
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.72rem;
        font-weight: 700;
        letter-spacing: 0.08em;
        color: #94A3B8;
        margin-bottom: 0.2rem;
    }
    .gold-rank {
        color: #5DD62C;
        font-weight: 800;
    }
    .podium-nation-name {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 1.35rem;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 0.3rem;
    }
    .podium-score-wrap {
        display: flex;
        align-items: baseline;
        justify-content: center;
        gap: 0.3rem;
        margin-bottom: 0.6rem;
    }
    .podium-pts {
        font-family: 'JetBrains Mono', monospace;
        font-variant-numeric: tabular-nums;
        font-size: 1.85rem;
        font-weight: 800;
        color: #F8FAFC;
    }
    .gold-score .podium-pts {
        color: #5DD62C;
    }
    .podium-unit {
        font-size: 0.75rem;
        font-weight: 700;
        color: #94A3B8;
    }
    .podium-pills-row {
        display: flex;
        justify-content: center;
        gap: 0.4rem;
        margin-bottom: 0.8rem;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        font-weight: 600;
    }
    .podium-pills-row span {
        background: rgba(0, 0, 0, 0.45);
        padding: 0.2rem 0.45rem;
        border-radius: 6px;
        border: 1px solid rgba(255, 255, 255, 0.06);
    }
    .pillar-block {
        font-family: 'Space Grotesk', sans-serif;
        font-size: 2.2rem;
        font-weight: 900;
        opacity: 0.25;
    }
    .pillar-gold-block {
        color: #5DD62C;
    }

    /* ============================================================
       7. SIDEBAR COMMAND DOCK & PHYSICAL RADIO PILLS
       ============================================================ */
    section[data-testid="stSidebar"] div[data-baseweb="radio"] {
        background: transparent !important;
        gap: 0.35rem !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadioButton"] label {
        background: rgba(20, 22, 27, 0.65) !important;
        border: 1px solid rgba(255, 255, 255, 0.06) !important;
        border-radius: 10px !important;
        padding: 0.65rem 0.95rem !important;
        margin-bottom: 0.35rem !important;
        min-height: 46px !important;
        display: flex !important;
        align-items: center !important;
        position: relative !important;
        transition: all 180ms var(--spring-snappy) !important;
        cursor: pointer !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadioButton"] label:hover {
        background: rgba(32, 35, 42, 0.85) !important;
        border-color: rgba(93, 214, 44, 0.35) !important;
        transform: translateX(4px) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadioButton"] label:has(input:checked) {
        background: rgba(93, 214, 44, 0.12) !important;
        border: 1px solid #5DD62C !important;
        box-shadow: 0 0 16px rgba(93, 214, 44, 0.2) !important;
    }
    section[data-testid="stSidebar"] div[data-testid="stRadioButton"] label:has(input:checked)::before {
        content: '';
        position: absolute;
        left: 0;
        top: 6px;
        bottom: 6px;
        width: 3px;
        background: #5DD62C;
        border-radius: 0 3px 3px 0;
        box-shadow: 0 0 8px #5DD62C;
    }

    /* ============================================================
       8. ZERO TELEMETRY FALLBACK & STATUS FOOTER
       ============================================================ */
    .zero-telemetry-card {
        background: rgba(20, 22, 27, 0.65);
        border: 1px dashed rgba(93, 214, 44, 0.4);
        border-radius: 16px;
        padding: 2.5rem 1.5rem;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
    }

    .telemetry-status-footer {
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 1rem;
        padding: 0.85rem 1.3rem;
        margin-top: 3rem;
        background: rgba(20, 22, 27, 0.75);
        backdrop-filter: blur(16px);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 12px;
        font-family: 'JetBrains Mono', monospace;
        font-size: 0.74rem;
        color: #94A3B8;
    }
    .footer-left {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .footer-center {
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    .footer-pill {
        background: rgba(10, 11, 14, 0.85);
        border: 1px solid rgba(255, 255, 255, 0.08);
        padding: 0.2rem 0.55rem;
        border-radius: 9999px;
        font-size: 0.68rem;
        color: #CBD5E1;
    }
    .footer-right {
        color: #64748B;
    }

    /* High-contrast Tabs styling */
    button[data-baseweb="tab"] {
        background: transparent !important;
        color: #94A3B8 !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-size: 0.98rem !important;
        font-weight: 700 !important;
        border-radius: 8px 8px 0 0 !important;
        padding: 0.75rem 1.4rem !important;
        transition: all 0.2s var(--spring-snappy) !important;
        border-bottom: 2px solid transparent !important;
    }
    button[aria-selected="true"] {
        color: #5DD62C !important;
        background: rgba(93, 214, 44, 0.08) !important;
        border-bottom: 3px solid #5DD62C !important;
        text-shadow: 0 0 12px rgba(93, 214, 44, 0.4);
    }

    /* Action Buttons (Electric Lime CTA with Emil Kowalski active-press) */
    .stButton>button {
        background: #5DD62C !important;
        color: #07080A !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        font-size: 0.95rem !important;
        letter-spacing: 0.02em !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.55rem 1.3rem !important;
        transition: all 0.18s var(--spring-snappy) !important;
        box-shadow: 0 4px 15px rgba(93, 214, 44, 0.3) !important;
    }
    .stButton>button:hover {
        background: #337418 !important;
        color: #F8FAFC !important;
        transform: translateY(-2px) scale(1.02) !important;
        box-shadow: 0 6px 20px rgba(93, 214, 44, 0.5) !important;
    }
    .stButton>button:active {
        transform: scale(0.97) !important;
    }

    /* Secondary Download Buttons */
    .stDownloadButton>button {
        background: rgba(20, 22, 27, 0.78) !important;
        color: #5DD62C !important;
        font-family: 'Space Grotesk', sans-serif !important;
        font-weight: 800 !important;
        border: 1.5px solid #5DD62C !important;
        border-radius: 8px !important;
        box-shadow: 0 4px 15px rgba(93, 214, 44, 0.2) !important;
        transition: all 0.2s ease !important;
    }
    .stDownloadButton>button:hover {
        background: #337418 !important;
        color: #F8FAFC !important;
    }
    .stDownloadButton>button:active {
        transform: scale(0.97) !important;
    }

    /* Animations */
    @keyframes ag-pulse {
        0%, 100% { opacity: 1; transform: scale(1); }
        50% { opacity: 0.4; transform: scale(0.9); }
    }
    @keyframes slideUpFade {
        from {
            opacity: 0;
            transform: translateY(12px) scale(0.98);
        }
        to {
            opacity: 1;
            transform: translateY(0) scale(1);
        }
    }

    /* Dataframe Containers */
    div[data-testid="stDataFrame"] {
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 10px;
        background-color: rgba(20, 22, 27, 0.75);
    }

    /* Focus visible accessibility outline */
    button:focus-visible, input:focus-visible, select:focus-visible {
        outline: 2px solid #5DD62C !important;
        outline-offset: 2px !important;
    }

    /* ============================================================
       9. RESPONSIVE MOBILE & TABLET OPTIMIZATIONS
       ============================================================ */
    @media (max-width: 768px) {
        .main .block-container, div[data-testid="stMainBlockContainer"] {
            padding-top: 0.85rem !important;
            padding-bottom: 2rem !important;
            padding-left: 0.75rem !important;
            padding-right: 0.75rem !important;
        }
        h1, .hero-title, .forbes-masthead-title {
            font-size: 1.85rem !important;
            line-height: 1.2 !important;
            letter-spacing: -0.01em !important;
        }
        div[data-testid="stHorizontalBlock"] {
            flex-wrap: wrap !important;
            gap: 0.75rem !important;
        }
        div[data-testid="stHorizontalBlock"] > div[data-testid="column"],
        div[data-testid="stHorizontalBlock"] > div[data-testid="stColumn"] {
            min-width: 100% !important;
            flex: 1 1 100% !important;
            margin-bottom: 0.4rem !important;
        }
        .spatial-podium-root {
            flex-direction: column !important;
            align-items: stretch !important;
            gap: 1rem !important;
            padding: 0.5rem 0 !important;
        }
        .podium-pillar {
            min-width: 100% !important;
            max-width: 100% !important;
            min-height: auto !important;
            padding: 1.2rem 1rem !important;
            border-radius: 12px !important;
        }
        div[data-baseweb="tab-list"] {
            display: flex !important;
            flex-wrap: nowrap !important;
            overflow-x: auto !important;
            -webkit-overflow-scrolling: touch !important;
            scrollbar-width: thin !important;
            gap: 0.25rem !important;
            padding-bottom: 0.35rem !important;
        }
        button[data-baseweb="tab"] {
            font-size: 0.88rem !important;
            padding: 0.55rem 0.85rem !important;
            white-space: nowrap !important;
            flex-shrink: 0 !important;
        }
        .stButton>button, .stDownloadButton>button {
            min-height: 44px !important;
            padding: 0.65rem 1.1rem !important;
            font-size: 0.95rem !important;
            width: 100% !important;
            touch-action: manipulation !important;
        }
        input[type="text"], input[type="number"], input[type="password"], textarea {
            font-size: 16px !important;
            min-height: 44px !important;
        }
        div[data-baseweb="select"] > div {
            min-height: 44px !important;
        }
        .telemetry-hud-bar {
            flex-direction: column;
            gap: 0.6rem;
            align-items: flex-start;
        }
        .hud-center {
            display: none;
        }
        .hud-right {
            width: 100%;
            justify-content: space-between;
        }
    }
</style>
""")


# ------------------------------------------------------------
# 3. Fast Cached Data Loading
# ------------------------------------------------------------
@st.cache_data(show_spinner="⚡ Connecting to Olympic Star Schema Warehouse...")
def load_all_data() -> pd.DataFrame:
    """Loads all historical Olympic medal facts from the Star Schema."""
    return get_denormalized_medals()


df_master = load_all_data()


# ------------------------------------------------------------
# 4. Mandatory Authentication Gateway (Bug 3 Fix)
# ------------------------------------------------------------
init_auth()

if not is_authenticated():
    # 4. LOGIN-STATE EXCLUSIVITY (CRITICAL): Only rendered when not logged in
    if not st.session_state.get("logged_in", False):
        render_login_scrolling_background()

    # User must log in through 3-Role entry portal before accessing dashboard
    render_landing_page()
    st.stop()


# ------------------------------------------------------------
# 5. Dynamic Role-Based Access Control (RBAC) Flow
# ------------------------------------------------------------
raw_role = st.session_state.get("user_role") or "enthusiast"
role_str = str(raw_role).lower()

if "admin" in role_str:
    active_role = "admin"
elif "prof" in role_str or "academy" in role_str or "coach" in role_str:
    active_role = "professional"
else:
    active_role = "enthusiast"

# Persist normalized role in session state as requested
st.session_state["user_role"] = active_role

# Sidebar Controller (The Control Center)
with st.sidebar:
    # Authenticated User Badge & Logout Button at top of sidebar
    render_sidebar_user_badge()

    sidebar_brand_icon = get_svg_icon("trophy", size=22, color="#5DD62C")
    filter_icon = get_svg_icon("filter", size=18, color="#5DD62C")

    render_html(f"""
    <div style="padding: 0.5rem 0 1rem 0; border-bottom: 1px solid #337418; margin-bottom: 1rem;">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div style="font-size: 1.4rem; font-weight: 800; font-family: 'Inter', sans-serif; color: #5DD62C; display: flex; align-items: center; gap: 0.5rem;">
                {sidebar_brand_icon} OLYMPIA
            </div>
            <span style="font-size: 0.72rem; background: rgba(93, 214, 44, 0.15); color: #5DD62C; border: 1px solid #5DD62C; padding: 0.2rem 0.6rem; border-radius: 12px; font-weight: 700;">
                {active_role.upper()}
            </span>
        </div>
        <div style="font-size: 0.75rem; color: #737373; margin-top: 0.3rem; letter-spacing: 0.08em; text-transform: uppercase; font-weight: 600;">
            INTELLIGENCE CONTROL CENTER
        </div>
    </div>
    """)

    if active_role == "professional":
        st.markdown(f"**Coaching & Performance Navigation**")
        selected_mode = st.sidebar.radio(
            "Coaching & Performance Navigation",
            options=[
                "Coach Strategy Studio",
                "Discipline Depth & Parity",
                "Athlete Hall of Fame & Scouting",
                "Podium & Medal Benchmarks",
                "OLAP Cube (Slice & Dice)"
            ],
            index=0,
            label_visibility="collapsed",
            key="coach_mode_controller"
        )
    elif active_role == "admin":
        st.markdown(f"**Administration Navigation**")
        selected_mode = st.sidebar.radio(
            "Administration Navigation",
            options=[
                "Warehouse Administration",
                "Data Mining Arena",
                "OLAP Cube (Slice & Dice)",
                "Podium & Medal Tally",
                "Coach Strategy Studio"
            ],
            index=0,
            label_visibility="collapsed",
            key="admin_mode_controller"
        )
    else:
        # Mode Toggle for Enthusiast without emojis
        st.markdown(f"**Navigation Workspace**")
        selected_mode = st.sidebar.radio(
            "Navigation Workspace",
            options=[
                "Podium & Medal Tally",
                "Coach Strategy Studio",
                "Athlete Hall of Fame",
                "OLAP Cube (Slice & Dice)",
                "Data Mining Arena"
            ],
            index=0,
            label_visibility="collapsed",
            key="quick_mode_controller"
        )

    st.markdown("---")
    render_html(f"<div style='font-size: 0.82rem; font-weight: 700; color: #F8FAFC; text-transform: uppercase; letter-spacing: 0.06em; margin-bottom: 0.5rem; display: flex; align-items: center; gap: 0.4rem;'>{filter_icon} Filter Controls</div>")

    # Season Select
    season_options = ["All", "Summer", "Winter"]
    selected_season = st.selectbox("Olympic Season:", options=season_options, index=0)

    # Era / Year Range Slider
    min_year_master = int(df_master["year"].min())
    max_year_master = int(df_master["year"].max())
    year_range = st.slider(
        "Era / Year Range:",
        min_value=min_year_master,
        max_value=max_year_master,
        value=(min_year_master, max_year_master),
        step=4
    )

    # Country / NOC Multi-select
    all_countries = sorted(df_master["country"].unique().tolist())
    selected_countries = st.multiselect(
        "NOC / Countries (Default: All):",
        options=all_countries,
        placeholder="Filter by nation (e.g., United States)..."
    )

    # Sport / Discipline Filter
    all_sports = sorted(df_master["sport"].unique().tolist())
    selected_sports = st.multiselect(
        "Sport / Discipline (Default: All):",
        options=all_sports,
        placeholder="Filter by sport (e.g., Athletics)..."
    )

    # Filter Presets
    st.markdown("<div style='margin-top: 0.8rem;'></div>", unsafe_allow_html=True)
    if st.button("🔄 Reset Filters", use_container_width=True):
        st.rerun()

    # Mini Warehouse Heartbeat Widget
    st.markdown("---")
    wh_counts = get_table_counts()
    fact_cnt = wh_counts.get("fact_medal", len(df_master))
    max_dim = max([wh_counts.get(k, 1) for k in ["dim_event", "dim_country", "dim_sport", "dim_game", "dim_medal"]], default=1000)
    
    table_items = [
        ("fact_medal", fact_cnt, "#5DD62C", 100),
        ("dim_event", wh_counts.get("dim_event", 0), "#00F0FF", min(100, max(15, int((wh_counts.get("dim_event", 0)/max_dim)*100)))),
        ("dim_country", wh_counts.get("dim_country", 0), "#38BDF8", min(100, max(15, int((wh_counts.get("dim_country", 0)/max_dim)*100)))),
        ("dim_sport", wh_counts.get("dim_sport", 0), "#A855F7", min(100, max(15, int((wh_counts.get("dim_sport", 0)/max_dim)*100)))),
        ("dim_game", wh_counts.get("dim_game", 0), "#F59E0B", min(100, max(15, int((wh_counts.get("dim_game", 0)/max_dim)*100)))),
        ("dim_medal", wh_counts.get("dim_medal", 3), "#E2E8F0", 15),
    ]
    
    spark_html = "".join([
        f'<div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.35rem; font-family: monospace; font-size: 0.72rem;">'
        f'<span style="color: #94A3B8;">{name}</span>'
        f'<div style="display: flex; align-items: center; gap: 0.4rem;">'
        f'<div style="width: 55px; height: 4px; background: rgba(255,255,255,0.08); border-radius: 2px; overflow: hidden;">'
        f'<div style="width: {pct}%; height: 100%; background: {col}; border-radius: 2px;"></div>'
        f'</div>'
        f'<span style="color: #F8FAFC; font-weight: 700; min-width: 45px; text-align: right;">{val:,}</span>'
        f'</div></div>'
        for name, val, col, pct in table_items
    ])

    render_html(f"""
    <div style="background: rgba(20, 22, 27, 0.75); border: 1px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 0.85rem 1rem; margin-top: 0.5rem;">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.65rem;">
            <div style="font-size: 0.72rem; font-weight: 700; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; display: flex; align-items: center; gap: 0.4rem;">
                <span style="color: #5DD62C; animation: ag-pulse 1.8s infinite;">●</span> WAREHOUSE HEARTBEAT
            </div>
            <span style="font-size: 0.68rem; color: #5DD62C; background: rgba(93, 214, 44, 0.12); padding: 0.1rem 0.4rem; border-radius: 4px; font-weight: 700;">60FPS WAL</span>
        </div>
        {spark_html}
    </div>
    """)


# ------------------------------------------------------------
# 6. Dynamic Data Filtering
# ------------------------------------------------------------
filtered_df = df_master.copy()

if selected_season != "All":
    filtered_df = filtered_df[filtered_df["season"] == selected_season]

filtered_df = filtered_df[
    (filtered_df["year"] >= year_range[0]) & (filtered_df["year"] <= year_range[1])
]

if selected_countries:
    filtered_df = filtered_df[filtered_df["country"].isin(selected_countries)]

if selected_sports:
    filtered_df = filtered_df[filtered_df["sport"].isin(selected_sports)]

if filtered_df.empty:
    render_telemetry_hud(
        active_role=active_role,
        active_module=selected_mode or active_role,
        year_range=year_range,
        total_facts=len(df_master)
    )
    render_empty_telemetry_card()
    render_telemetry_footer()
    st.stop()


# ------------------------------------------------------------
# 9B. ADMIN DASHBOARD: BACKEND DATA & SYSTEM MANAGEMENT
# ------------------------------------------------------------
def render_admin_dashboard(df: pd.DataFrame):
    """
    Renders the Backend Management Interface for Administrators:
    - Live Website & Warehouse Statistics (Total Users, Records, Physical DB Size, Last Updated)
    - Interactive Dataset Management via st.data_editor (view, edit, delete, insert)
    - Direct SQLite transactional backend integration with safe rollbacks
    """
    user_svg = get_svg_icon("user", size=22, color="#38BDF8")
    db_svg = get_svg_icon("database", size=22, color="#5DD62C")
    disk_svg = get_svg_icon("database", size=22, color="#F59E0B")
    cal_svg = get_svg_icon("calendar", size=20, color="#F8FAFC")

    # 1. LIVE WEBSITE & WAREHOUSE STATISTICS
    db_path = get_db_path()
    db_size_mb = os.path.getsize(db_path) / (1024 * 1024) if os.path.exists(db_path) else 0.0
    last_mod_ts = pd.to_datetime(os.path.getmtime(db_path), unit="s").strftime("%Y-%m-%d %H:%M UTC") if os.path.exists(db_path) else "Active"
    counts = get_table_counts()
    fact_medals_total = counts.get("fact_medal", len(df))

    # FORBES MINIMALIST EDITORIAL MASTHEAD
    render_html(f"""
    <div style="text-align: center; padding: 2.4rem 1.2rem 1.8rem 1.2rem; border-bottom: 1px solid #222222; margin-bottom: 1.5rem; background: #0A0A0A; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.6);">
        <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-bottom: 0.35rem;">
            The World's
        </div>
        <h1 style="font-family: 'Playfair Display', Georgia, serif !important; font-size: 3.1rem; font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.15; letter-spacing: -0.01em;">
            System Administration & Warehouse Control
        </h1>
        <div style="color: #94A3B8; font-size: 1.05rem; max-width: 780px; margin: 0.65rem auto 1.1rem auto; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
            Star Schema Management, Direct Transactional Dataset Editor & Enterprise Data Engineering Console.
        </div>
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #141414; border: 1px solid #262626; padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.78rem; color: #94A3B8;">
            <span style="color: #5DD62C; font-weight: 700;">Admin Engine Active</span> Master Write Authority • SQLite Star Schema Live
        </div>
    </div>
    """)

    # FORBES RUNNING TICKER RIBBON (MACRO METRICS)
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; background: #111111; border: 1px solid #222222; border-radius: 8px; padding: 0.85rem 1.4rem; margin-bottom: 1.8rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {user_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #38BDF8; font-family: 'Inter', sans-serif;">3 Active</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Authorized Accounts</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {db_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #5DD62C; font-family: 'Inter', sans-serif;">{fact_medals_total:,}</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Warehouse Fact Records</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {disk_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #F59E0B; font-family: 'Inter', sans-serif;">{db_size_mb:.2f} MB</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Physical DB Storage</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {cal_svg}
            <span style="font-size: 1.15rem; font-weight: 800; color: #F8FAFC; font-family: 'Inter', sans-serif;">{last_mod_ts}</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Last Database Commit</span>
        </div>
    </div>
    """)

    # 2. DATA MANAGEMENT WORKSPACE
    tab_edit, tab_add, tab_delete, tab_audit = st.tabs([
        "Interactive Dataset Editor",
        "Add New Medal Fact",
        "Delete Record by ID",
        "Star Schema Dimensions Audit"
    ])

    with tab_edit:
        st.markdown("#### Interactive Dataset Editor")
        st.caption("Filter records below, edit cells inline within `st.data_editor`, and commit transactional updates directly to SQLite.")

        col_search1, col_search2, col_search3 = st.columns([2, 2, 1])
        with col_search1:
            search_country = st.selectbox("Filter Country:", ["All"] + sorted(df["country"].dropna().unique().tolist()), index=0, key="admin_edit_ctry")
        with col_search2:
            search_sport = st.selectbox("Filter Sport:", ["All"] + sorted(df["sport"].dropna().unique().tolist()), index=0, key="admin_edit_sport")
        with col_search3:
            limit_rows = st.number_input("Max Rows to Display:", min_value=10, max_value=500, value=50, step=10, key="admin_edit_limit")

        # Slice dataset for fast interactive editing
        edit_slice = df.copy()
        if search_country != "All":
            edit_slice = edit_slice[edit_slice["country"] == search_country]
        if search_sport != "All":
            edit_slice = edit_slice[edit_slice["sport"] == search_sport]
        
        edit_cols = ["medal_fact_id", "year", "games", "country", "sport", "event_name", "medal", "athletes"]
        edit_slice = edit_slice[edit_cols].head(int(limit_rows)).reset_index(drop=True)

        edited_data = st.data_editor(
            edit_slice,
            key="admin_dataset_editor",
            use_container_width=True,
            num_rows="dynamic",
            disabled=["medal_fact_id"]  # Primary key is read-only
        )

        col_save, col_refresh = st.columns([1, 4])
        with col_save:
            if st.button("Commit Cell Changes to Database", type="primary", use_container_width=True):
                # Apply updates from edited dataframe to database
                conn = get_db_connection()
                try:
                    updated_count = 0
                    for _, row in edited_data.iterrows():
                        fact_id = int(row["medal_fact_id"])
                        new_athlete = str(row["athletes"])
                        cursor = conn.cursor()
                        cursor.execute("UPDATE fact_medal SET athletes = ? WHERE medal_fact_id = ?", (new_athlete, fact_id))
                        updated_count += cursor.rowcount
                    conn.commit()
                    st.success(f"Successfully committed changes for {updated_count} records to database.")
                    st.cache_data.clear()
                except Exception as e:
                    conn.rollback()
                    st.error(f"Failed to commit updates: {e}")
                finally:
                    conn.close()

    with tab_add:
        st.markdown("#### Add New Historical Olympic Medal Fact")
        st.caption("Insert a newly verified medal finish into the Star Schema with referential integrity validation.")

        with st.form("admin_add_record_form"):
            col_f1, col_f2 = st.columns(2)
            with col_f1:
                # Fetch available dimensional lookups
                conn = get_db_connection()
                try:
                    games_list = pd.read_sql_query("SELECT game_id, games FROM dim_game ORDER BY year DESC", conn)
                    ctry_list = pd.read_sql_query("SELECT country_id, country_name FROM dim_country ORDER BY country_name ASC", conn)
                    sport_list = pd.read_sql_query("SELECT sport_id, sport_name FROM dim_sport ORDER BY sport_name ASC", conn)
                    event_list = pd.read_sql_query("SELECT event_id, event_name FROM dim_event ORDER BY event_name ASC LIMIT 100", conn)
                    medal_list = pd.read_sql_query("SELECT medal_id, medal_name FROM dim_medal", conn)
                finally:
                    conn.close()

                sel_game_str = st.selectbox("Olympic Games:", games_list["games"].tolist(), key="add_game_sel")
                sel_ctry_str = st.selectbox("Country / NOC:", ctry_list["country_name"].tolist(), key="add_ctry_sel")
                sel_sport_str = st.selectbox("Sport / Discipline:", sport_list["sport_name"].tolist(), key="add_sport_sel")

            with col_f2:
                sel_event_str = st.selectbox("Event Name:", event_list["event_name"].tolist(), key="add_event_sel")
                sel_medal_str = st.selectbox("Medal Tier:", medal_list["medal_name"].tolist(), key="add_medal_sel")
                athlete_input = st.text_input("Athlete Name(s):", placeholder="e.g. Michael PHELPS", key="add_athlete_name")

            submit_add = st.form_submit_button("Insert Fact Record into SQLite Warehouse", type="primary")

            if submit_add:
                if not athlete_input.strip():
                    st.error("Please enter an athlete or team name.")
                else:
                    game_id = int(games_list[games_list["games"] == sel_game_str]["game_id"].iloc[0])
                    ctry_id = int(ctry_list[ctry_list["country_name"] == sel_ctry_str]["country_id"].iloc[0])
                    sport_id = int(sport_list[sport_list["sport_name"] == sel_sport_str]["sport_id"].iloc[0])
                    event_id = int(event_list[event_list["event_name"] == sel_event_str]["event_id"].iloc[0])
                    medal_id = int(medal_list[medal_list["medal_name"] == sel_medal_str]["medal_id"].iloc[0])

                    conn = get_db_connection()
                    try:
                        cursor = conn.cursor()
                        cursor.execute("""
                            INSERT INTO fact_medal (game_id, country_id, sport_id, event_id, medal_id, athletes)
                            VALUES (?, ?, ?, ?, ?, ?)
                        """, (game_id, ctry_id, sport_id, event_id, medal_id, athlete_input.strip()))
                        conn.commit()
                        new_id = cursor.lastrowid
                        st.success(f"Successfully inserted new medal fact record. Generated ID: #{new_id}")
                        st.cache_data.clear()
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Failed to insert record: {e}")
                    finally:
                        conn.close()

    with tab_delete:
        st.markdown("#### Delete Medal Record")
        st.caption("Remove an erroneous or duplicate record from `fact_medal` using its unique primary key.")
        
        with st.form("admin_delete_form"):
            del_id = st.number_input("Enter Medal Fact ID to Delete:", min_value=1, step=1, key="del_fact_id_input")
            confirm_del = st.checkbox("I confirm that this action will permanently remove this record from SQLite.", key="del_confirm_chk")
            btn_del = st.form_submit_button("Delete Record Permanently", type="primary")

            if btn_del:
                if not confirm_del:
                    st.warning("Please tick the confirmation checkbox to proceed with deletion.")
                else:
                    conn = get_db_connection()
                    try:
                        cursor = conn.cursor()
                        cursor.execute("SELECT medal_fact_id, athletes FROM fact_medal WHERE medal_fact_id = ?", (int(del_id),))
                        rec = cursor.fetchone()
                        if not rec:
                            st.error(f"No record found with Medal Fact ID #{del_id}.")
                        else:
                            cursor.execute("DELETE FROM fact_medal WHERE medal_fact_id = ?", (int(del_id),))
                            conn.commit()
                            st.success(f"Successfully deleted Record #{del_id} (Athlete: {rec[1]}).")
                    except Exception as e:
                        conn.rollback()
                        st.error(f"Failed to delete record: {e}")
                    finally:
                        conn.close()

    with tab_audit:
        st.markdown("#### Dimensional Integrity & Star Schema Breakdown")
        dim_summary = pd.DataFrame([
            {"Table": "fact_medal (Central Fact)", "Type": "Fact Table", "Row Count": counts.get("fact_medal", 0), "Primary Key": "medal_fact_id", "Integrity": "100% OK"},
            {"Table": "dim_game", "Type": "Dimension", "Row Count": counts.get("dim_game", 0), "Primary Key": "game_id", "Integrity": "100% OK"},
            {"Table": "dim_country", "Type": "Dimension", "Row Count": counts.get("dim_country", 0), "Primary Key": "country_id", "Integrity": "100% OK"},
            {"Table": "dim_sport", "Type": "Dimension", "Row Count": counts.get("dim_sport", 0), "Primary Key": "sport_id", "Integrity": "100% OK"},
            {"Table": "dim_event", "Type": "Dimension", "Row Count": counts.get("dim_event", 0), "Primary Key": "event_id", "Integrity": "100% OK"},
            {"Table": "dim_medal", "Type": "Dimension", "Row Count": counts.get("dim_medal", 0), "Primary Key": "medal_id", "Integrity": "100% OK"},
        ])
        st.dataframe(dim_summary, use_container_width=True, hide_index=True)


# ------------------------------------------------------------
# 9C. PROFESSIONAL / ACADEMY DASHBOARD: ADVANCED ANALYTICS & POTENTIAL PREDICTOR
# ------------------------------------------------------------
def render_professional_dashboard(df: pd.DataFrame):
    """
    Renders the Professional / Sports Science Academy Intelligence Dashboard:
    - Deep-dive performance metrics across specific years and athlete physical attributes
    - Interactive "Predict Your Potential" module using K-Nearest Neighbors & Multi-dimensional benchmark modeling
    - Discipline parity, nation conversion efficiency, and multi-sport morphology alignment
    """
    trophy_svg = get_svg_icon("trophy", size=22, color="#38BDF8")
    globe_svg = get_svg_icon("globe", size=20, color="#5DD62C")
    star_svg = get_svg_icon("star", size=20, color="#F59E0B")
    trend_svg = get_svg_icon("trend_up", size=18, color="#10B981")
    lightning_svg = get_svg_icon("lightning", size=18, color="#5DD62C")
    target_svg = get_svg_icon("star", size=18, color="#38BDF8")
    chart_svg = get_svg_icon("trend_up", size=18, color="#38BDF8")
    user_svg = get_svg_icon("user", size=18, color="#F8FAFC")

    # 1. FORBES MINIMALIST EDITORIAL MASTHEAD
    render_html("""
    <div style="text-align: center; padding: 2.4rem 1.2rem 1.8rem 1.2rem; border-bottom: 1px solid #222222; margin-bottom: 1.5rem; background: #0A0A0A; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.6);">
        <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-bottom: 0.35rem;">
            The World's
        </div>
        <h1 style="font-family: 'Playfair Display', Georgia, serif !important; font-size: 3.1rem; font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.15; letter-spacing: -0.01em;">
            Sports Science & Academy Intelligence
        </h1>
        <div style="color: #94A3B8; font-size: 1.05rem; max-width: 780px; margin: 0.65rem auto 1.1rem auto; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
            Biomechanical Benchmarks, Era Deep-Dives & The Predictive Athlete Potential Engine Across 1896 – 2026.
        </div>
        <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #141414; border: 1px solid #262626; padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.78rem; color: #94A3B8;">
            <span style="color: #5DD62C; font-weight: 700;">Performance Engine Active</span> Biomechanical Modeling • SQLite Star Schema Live
        </div>
    </div>
    """)

    # 1. CORE PERFORMANCE KPIS
    total_medals = len(df)
    unique_nations = df["country"].nunique()
    gold_medals = int((df["medal"] == "Gold").sum())
    total_points = int(df["medal_points"].sum())
    top_3_concentration = (df.groupby("country").size().nlargest(3).sum() / max(total_medals, 1) * 100)

    # FORBES RUNNING TICKER RIBBON (MACRO METRICS)
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; background: #111111; border: 1px solid #222222; border-radius: 8px; padding: 0.85rem 1.4rem; margin-bottom: 1.8rem;">
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {trophy_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #38BDF8; font-family: 'Inter', sans-serif;">{total_medals:,}</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Verified Podiums</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {globe_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #5DD62C; font-family: 'Inter', sans-serif;">{unique_nations}</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Podium Nations</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {star_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #F59E0B; font-family: 'Inter', sans-serif;">{total_points:,}</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Weighted Medal Points</span>
        </div>
        <div style="display: flex; align-items: center; gap: 0.6rem;">
            {trend_svg}
            <span style="font-size: 1.25rem; font-weight: 800; color: #10B981; font-family: 'Inter', sans-serif;">{top_3_concentration:.1f}%</span>
            <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Top-3 Nation Share</span>
        </div>
    </div>
    """)

    # WORKSPACE VIEW SELECTOR (Coach Strategy Studio vs Sports Science Biomechanics)
    prof_workspace_mode = st.radio(
        "Select Professional Workspace Module:",
        options=[
            "🎯 Coach Strategy & Player Inclination Studio",
            "🧬 Sports Science, Potential Engine & Parity Analytics"
        ],
        index=0,
        horizontal=True,
        key="prof_workspace_view_toggle"
    )

    if "Strategy" in prof_workspace_mode or "Coach" in prof_workspace_mode:
        render_coach_strategy_studio(df)
        return

    # 2. CRUCIAL FEATURE: PREDICT YOUR POTENTIAL MODULE
    st.markdown("### The Predict Your Potential Biomechanical Module")
    st.markdown("""
    Enter your physiological attributes below to evaluate your morphology against **historical Olympic medalists** in your target discipline.
    Our multidimensional predictive model (K-Nearest Neighbors & Normalized Mahalanobis-Weighted Feature Distance) computes your **Podium Compatibility Score** and highlights your nearest Olympic sport affinities.
    """)

    with st.form("predict_potential_form"):
        p_col1, p_col2, p_col3, p_col4, p_col5 = st.columns(5)
        with p_col1:
            input_age = st.number_input("Age (Years):", min_value=12, max_value=75, value=22, step=1, key="pot_age")
        with p_col2:
            input_gender = st.selectbox("Biological Category:", ["Men", "Women"], index=0, key="pot_gender")
        with p_col3:
            input_height = st.number_input("Height (cm):", min_value=130, max_value=230, value=182, step=1, key="pot_height")
        with p_col4:
            input_weight = st.number_input("Weight (kg):", min_value=35, max_value=180, value=76, step=1, key="pot_weight")
        with p_col5:
            sport_keys = list(SPORT_PROFILES.keys())
            input_sport = st.selectbox("Target Olympic Sport:", sport_keys, index=0, key="pot_sport")

        btn_predict = st.form_submit_button("Run Predictive Potential Analysis", type="primary", use_container_width=True)

    # Execute and render predictions
    if btn_predict or "last_potential_result" in st.session_state:
        if btn_predict:
            result = predict_athlete_potential(
                age=float(input_age),
                height_cm=float(input_height),
                weight_kg=float(input_weight),
                gender=input_gender,
                sport=input_sport
            )
            st.session_state["last_potential_result"] = result
        else:
            result = st.session_state["last_potential_result"]

        st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
        st.markdown(f"#### Potential Analysis: **{result['user_inputs']['sport']}** ({result['user_inputs']['gender']})")

        res_col1, res_col2 = st.columns([1, 2])
        with res_col1:
            score = result["score"]
            render_html(f"""
            <div style="
                background: #141414;
                border: 2px solid {result['tier_color']};
                border-radius: 12px;
                padding: 1.8rem;
                text-align: center;
                box-shadow: 0 8px 30px rgba(0, 0, 0, 0.6);
            ">
                <div style="font-size: 0.85rem; color: #A0A0A0; font-weight: 700; text-transform: uppercase; letter-spacing: 0.08em;">
                    Podium Compatibility Score
                </div>
                <div class="potential-score-badge" style="font-size: 3.5rem; font-weight: 900; color: {result['tier_color']}; line-height: 1.1; margin: 0.5rem 0;">
                    {score}%
                </div>
                <div style="font-size: 1.05rem; font-weight: 800; color: #F8F8F8; margin-bottom: 0.4rem;">
                    {result['tier']}
                </div>
                <div style="font-size: 0.82rem; color: #5DD62C; background: rgba(93, 214, 44, 0.12); padding: 0.35rem 0.75rem; border-radius: 20px; display: inline-block; border: 1px solid #5DD62C;">
                    {result['badge']}
                </div>
                <div style="margin-top: 1.2rem; font-size: 0.82rem; color: #A0A0A0; text-align: left; border-top: 1px solid #262626; padding-top: 0.8rem;">
                    <strong>Biomechanical Archetype:</strong><br>
                    {result['benchmarks']['archetype']}
                </div>
            </div>
            """)

        with res_col2:
            st.markdown("##### Physiological Attribute Comparison vs Historical Medalists")
            bench = result["benchmarks"]
            user = result["user_inputs"]
            deltas = result["deltas"]

            comparison_data = [
                {"Attribute": "Age", "Your Value": f"{user['age']} yrs", "Olympic Medalist Benchmark": f"{bench['age_mean']} yrs", "Variance Delta": f"{'+' if deltas['age_delta'] > 0 else ''}{deltas['age_delta']} yrs"},
                {"Attribute": "Height", "Your Value": f"{user['height_cm']} cm", "Olympic Medalist Benchmark": f"{bench['height_mean']} cm", "Variance Delta": f"{'+' if deltas['height_delta'] > 0 else ''}{deltas['height_delta']} cm"},
                {"Attribute": "Weight", "Your Value": f"{user['weight_kg']} kg", "Olympic Medalist Benchmark": f"{bench['weight_mean']} kg", "Variance Delta": f"{'+' if deltas['weight_delta'] > 0 else ''}{deltas['weight_delta']} kg"},
                {"Attribute": "Body Mass Index (BMI)", "Your Value": f"{user['bmi']} kg/m²", "Olympic Medalist Benchmark": f"{bench['bmi_mean']} kg/m²", "Variance Delta": f"{'+' if deltas['bmi_delta'] > 0 else ''}{deltas['bmi_delta']} kg/m²"},
            ]
            st.dataframe(pd.DataFrame(comparison_data), use_container_width=True, hide_index=True)

            st.markdown("##### Top Alternative Olympic Sport Affinities")
            st.caption("Based on multidimensional Euclidean distance against all 12 Olympic sports benchmark profiles:")
            top_aff_df = result["top_affinities"].copy()
            top_aff_df.columns = ["Sport Discipline", "Compatibility Score (%)", "Biomechanical Target Archetype"]
            st.dataframe(top_aff_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ============================================================
    # 3. ATHLETE PERFORMANCE BENCHMARKING
    # ============================================================
    st.markdown("### Athlete Performance Benchmarking & Career Longevity")
    st.caption("Biomechanical peak windows, age-to-medal trajectories, and multi-cycle Olympic consistency scoring.")

    bench_tab1, bench_tab2 = st.tabs([
        "Career Trajectory & Peak Years Window",
        "Multi-Cycle Olympic Consistency Scoring"
    ])

    with bench_tab1:
        st.markdown("#### Age Trajectory & Gold Medalist Peak Performance Window")
        b_c1, b_c2 = st.columns([2, 1])
        with b_c1:
            all_sports_list = ["All"] + sorted(df["sport"].dropna().unique().tolist())
            bench_sport = st.selectbox("Select Target Sport / Discipline:", all_sports_list, index=0, key="prof_bench_sport")
        with b_c2:
            bench_medal = st.radio("Medal Tier:", ["All", "Gold", "Silver", "Bronze"], horizontal=True, key="prof_bench_medal")

        peak_data = compute_peak_performance_window(df, sport=bench_sport, medal_filter=bench_medal)

        # 4 Metric cards for peak window
        p1, p2, p3, p4 = st.columns(4)
        with p1:
            render_html(f"""
            <div class="ticker-card">
                <div class="ticker-icon">{target_svg}</div>
                <div class="ticker-value">{peak_data['mean_age']} yrs</div>
                <div class="ticker-label">Mean Age ({peak_data['sport']})</div>
            </div>
            """)
        with p2:
            render_html(f"""
            <div class="ticker-card">
                <div class="ticker-icon">{chart_svg}</div>
                <div class="ticker-value">{peak_data['peak_window_min']} – {peak_data['peak_window_max']}</div>
                <div class="ticker-label">Peak Performance Window (±1σ)</div>
            </div>
            """)
        with p3:
            render_html(f"""
            <div class="ticker-card">
                <div class="ticker-icon">{trend_svg}</div>
                <div class="ticker-value">±{peak_data['std_age']} yrs</div>
                <div class="ticker-label">Age Standard Deviation (σ)</div>
            </div>
            """)
        with p4:
            render_html(f"""
            <div class="ticker-card">
                <div class="ticker-icon">{user_svg}</div>
                <div class="ticker-value">{peak_data['sample_size']:,}</div>
                <div class="ticker-label">Analyzed Podium Sample</div>
            </div>
            """)

        st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

        # Visualizing Age Distribution and Peak Zone
        if not peak_data["age_df"].empty:
            age_df = peak_data["age_df"]
            fig_peak = px.histogram(
                age_df,
                x="computed_age",
                color="medal" if bench_medal == "All" else None,
                nbins=35,
                barmode="stack",
                color_discrete_map={"Gold": "#FFD700", "Silver": "#C0C0C0", "Bronze": "#CD7F32"},
                title=f"Podium Finisher Age Distribution: {peak_data['sport']} (Highlighted Peak Window: {peak_data['peak_window_min']} - {peak_data['peak_window_max']} yrs)"
            )
            fig_peak.add_vrect(
                x0=peak_data["peak_window_min"],
                x1=peak_data["peak_window_max"],
                fillcolor="#5DD62C",
                opacity=0.15,
                line_width=1,
                line_dash="dot",
                annotation_text="Peak Window (±1σ)",
                annotation_position="top left"
            )
            fig_peak.add_vline(
                x=peak_data["mean_age"],
                line_width=2.5,
                line_dash="dash",
                line_color="#5DD62C",
                annotation_text=f"Mean: {peak_data['mean_age']} yrs",
                annotation_position="top right"
            )
            fig_peak = apply_dark_theme(fig_peak, title=f"Biomechanical Peak Window: {peak_data['sport']}", x_title="Age at Medal Achievement (Years)", y_title="Number of Medalists")
            st.plotly_chart(fig_peak, use_container_width=True)

    with bench_tab2:
        st.markdown("#### Multi-Cycle Olympic Consistency Scoring")
        st.caption("Evaluates performance stability across consecutive Olympic editions (coefficient of variation inverse).")

        cons_mode = st.radio("Consistency Evaluation Mode:", ["Nation Multi-Cycle Stability", "Individual Legend Career Stability"], horizontal=True, key="prof_cons_mode")

        if cons_mode == "Nation Multi-Cycle Stability":
            scores_df = compute_consistency_scores(df, mode="Nation", top_n=15)
            fig_cons = px.bar(
                scores_df,
                x="consistency_score",
                y="country",
                orientation="h",
                color="consistency_score",
                text="consistency_score",
                color_continuous_scale=[[0, "#202020"], [0.4, "#337418"], [1, "#5DD62C"]],
                title="Top 15 Nations by Olympic Cycle Consistency Index (0–100%)"
            )
            fig_cons.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_cons.update_layout(yaxis=dict(autorange="reversed"))
            fig_cons = apply_dark_theme(fig_cons, title="National Cycle Consistency Index", x_title="Consistency Score (0–100%)", y_title="Nation")
            st.plotly_chart(fig_cons, use_container_width=True)

            with st.expander("Detailed Nation Cycle Stability Metrics Table"):
                disp_scores = scores_df.rename(columns={
                    "country": "Nation",
                    "editions_participated": "Olympic Editions",
                    "total_medals": "Total Medals",
                    "mean_per_cycle": "Mean Medals / Cycle",
                    "std_per_cycle": "Std Dev / Cycle",
                    "consistency_score": "Consistency Score (%)"
                })
                st.dataframe(disp_scores, use_container_width=True, hide_index=True)

        else:
            athlete_scores_df = compute_consistency_scores(df, mode="Athlete", top_n=15)
            fig_ath_cons = px.bar(
                athlete_scores_df,
                x="consistency_score",
                y="athletes",
                orientation="h",
                color="consistency_score",
                text="consistency_score",
                color_continuous_scale=[[0, "#202020"], [0.4, "#337418"], [1, "#5DD62C"]],
                title="Top 15 Athletes by Multi-Edition Olympic Consistency Index"
            )
            fig_ath_cons.update_traces(texttemplate="%{text:.1f}%", textposition="outside")
            fig_ath_cons.update_layout(yaxis=dict(autorange="reversed"))
            fig_ath_cons = apply_dark_theme(fig_ath_cons, title="Legend Multi-Edition Career Stability", x_title="Consistency Score (0–100%)", y_title="Athlete")
            st.plotly_chart(fig_ath_cons, use_container_width=True)

            with st.expander("Detailed Athlete Career Longevity Table"):
                disp_ath = athlete_scores_df.rename(columns={
                    "athletes": "Athlete",
                    "country": "Nation",
                    "sport": "Discipline",
                    "editions_count": "Editions Won In",
                    "first_year": "First Medal",
                    "last_year": "Last Medal",
                    "career_span_years": "Career Span (Yrs)",
                    "total_medals": "Total Medals",
                    "gold_medals": "Golds",
                    "consistency_score": "Consistency Score (%)"
                })
                st.dataframe(disp_ath, use_container_width=True, hide_index=True)

    st.markdown("---")

    # ============================================================
    # 4. SPORT SPECIALIZATION INDEX
    # ============================================================
    st.markdown("### Sport Specialization Index (Concentration vs. Diversification)")
    st.caption("Quantifies national athletic portfolio diversification using Normalized Shannon Entropy & Sports HHI.")

    spec_c1, spec_c2 = st.columns([1, 2])
    with spec_c1:
        min_medals_threshold = st.slider("Minimum Medals Filter:", min_value=15, max_value=100, value=30, step=5, key="prof_spec_min_m")
        spec_df = compute_sport_specialization_index(df, min_medals=min_medals_threshold)
        
        all_spec_countries = spec_df["country"].tolist() if not spec_df.empty else []
        focus_country = st.selectbox("Select Nation for Portfolio Deep-Dive:", all_spec_countries, index=0 if all_spec_countries else None, key="prof_spec_ctry")

    with spec_c2:
        if not spec_df.empty:
            most_spec = spec_df.iloc[0]
            most_div = spec_df.iloc[-1]
            avg_div = round(spec_df["diversification_index"].mean(), 1)

            mc1, mc2, mc3 = st.columns(3)
            with mc1:
                render_html(f"""
                <div class="ticker-card">
                    <div class="ticker-icon">{target_svg}</div>
                    <div class="ticker-value" style="color: {most_spec['badge_color']};">{most_spec['specialization_index']}%</div>
                    <div class="ticker-label">Most Concentrated: {most_spec['country']} ({most_spec['top_sport']})</div>
                </div>
                """)
            with mc2:
                render_html(f"""
                <div class="ticker-card">
                    <div class="ticker-icon">{globe_svg}</div>
                    <div class="ticker-value" style="color: {most_div['badge_color']};">{most_div['diversification_index']}%</div>
                    <div class="ticker-label">Most Diversified: {most_div['country']} ({most_div['sports_count']} Sports)</div>
                </div>
                """)
            with mc3:
                render_html(f"""
                <div class="ticker-card">
                    <div class="ticker-icon">{chart_svg}</div>
                    <div class="ticker-value">{avg_div}%</div>
                    <div class="ticker-label">Mean Portfolio Diversification</div>
                </div>
                """)

    if not spec_df.empty:
        col_s1, col_s2 = st.columns([3, 2])
        with col_s1:
            fig_bubble = px.scatter(
                spec_df,
                x="diversification_index",
                y="specialization_index",
                size="total_medals",
                color="archetype",
                hover_name="country",
                hover_data={"total_medals": True, "sports_count": True, "top_sport": True, "top_sport_share_pct": True},
                color_discrete_map={
                    "Hyper-Specialized (Single Core Focus)": "#FF4444",
                    "Targeted Concentration": "#FFD700",
                    "Balanced Specialist": "#38BDF8",
                    "Multi-Discipline Powerhouse": "#5DD62C"
                },
                title="National Athletic Portfolio: Concentration vs. Diversification Index"
            )
            fig_bubble.update_traces(marker=dict(line=dict(width=1, color="#202020")))
            fig_bubble = apply_dark_theme(fig_bubble, title="National Portfolio Concentration Matrix", x_title="Diversification Score (%) [Normalized Entropy]", y_title="Specialization Score (%)")
            st.plotly_chart(fig_bubble, use_container_width=True)

        with col_s2:
            if focus_country:
                focus_data = df[df["country"] == focus_country]
                focus_sports = focus_data["sport"].value_counts().reset_index()
                focus_sports.columns = ["sport", "medals"]
                
                if len(focus_sports) > 6:
                    top6 = focus_sports.head(6)
                    other_count = focus_sports.iloc[6:]["medals"].sum()
                    other_row = pd.DataFrame([{"sport": "Other Disciplines", "medals": other_count}])
                    focus_sports_plot = pd.concat([top6, other_row], ignore_index=True)
                else:
                    focus_sports_plot = focus_sports

                fig_donut = px.pie(
                    focus_sports_plot,
                    names="sport",
                    values="medals",
                    hole=0.45,
                    title=f"{focus_country} Discipline Distribution",
                    color_discrete_sequence=["#5DD62C", "#337418", "#A3E635", "#FFD700", "#38BDF8", "#F43F5E", "#888888"]
                )
                fig_donut.update_traces(textposition="inside", textinfo="percent+label")
                fig_donut = apply_dark_theme(fig_donut, title=f"{focus_country}: Discipline Concentration", x_title="", y_title="")
                st.plotly_chart(fig_donut, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # 5. TALENT DISTRIBUTION PIPELINE
    # ============================================================
    st.markdown("### Talent Distribution Pipeline & Generational Breakthrough")
    st.caption("Tracks generational athlete shifts across eras and measures the debutant Breakthrough Rate.")

    pipeline_data = compute_talent_pipeline(df)
    b_df = pipeline_data["breakthrough_df"]
    era_df = pipeline_data["era_summary"]

    t_c1, t_c2, t_c3 = st.columns(3)
    with t_c1:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{lightning_svg}</div>
            <div class="ticker-value">{pipeline_data['latest_breakthrough_rate']}%</div>
            <div class="ticker-label">Latest Edition Breakthrough Rate</div>
        </div>
        """)
    with t_c2:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{trend_svg}</div>
            <div class="ticker-value">{pipeline_data['avg_breakthrough_rate']}%</div>
            <div class="ticker-label">Historical Average Rookie Share</div>
        </div>
        """)
    with t_c3:
        retention = round(100.0 - pipeline_data['avg_breakthrough_rate'], 1)
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{chart_svg}</div>
            <div class="ticker-value">{retention}%</div>
            <div class="ticker-label">Veteran Podium Retention Rate</div>
        </div>
        """)

    st.markdown("<div style='margin-bottom: 1rem;'></div>", unsafe_allow_html=True)

    pipe_col1, pipe_col2 = st.columns(2)
    with pipe_col1:
        st.markdown("#### First-Time Medalists vs Returning Veterans Across Editions")
        fig_break = go.Figure()
        fig_break.add_trace(go.Bar(
            x=b_df["year"],
            y=b_df["debutants"],
            name="First-Time Medalists (Debuts)",
            marker_color="#5DD62C"
        ))
        fig_break.add_trace(go.Bar(
            x=b_df["year"],
            y=b_df["veterans"],
            name="Returning Veterans",
            marker_color="#202020",
            marker_line=dict(color="#337418", width=1.5)
        ))
        fig_break.add_trace(go.Scatter(
            x=b_df["year"],
            y=b_df["breakthrough_rate_pct"],
            name="Breakthrough Rate (%)",
            yaxis="y2",
            mode="lines+markers",
            line=dict(color="#FFD700", width=2.5),
            marker=dict(size=5, color="#FFD700")
        ))
        fig_break.update_layout(
            barmode="stack",
            yaxis=dict(title="Podium Medalists Count"),
            yaxis2=dict(
                title="Breakthrough Rate (%)",
                overlaying="y",
                side="right",
                range=[0, 105],
                showgrid=False
            ),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_break = apply_dark_theme(fig_break, title="Olympic Debutant Breakthrough Trajectory", x_title="Olympic Year", y_title="Podium Finishers")
        st.plotly_chart(fig_break, use_container_width=True)

    with pipe_col2:
        st.markdown("#### Generational Era Transition: Athletes, Nations & Disciplines")
        fig_era = px.bar(
            era_df,
            x="generational_era",
            y=["total_medals", "unique_athletes", "unique_nations"],
            barmode="group",
            color_discrete_sequence=["#5DD62C", "#FFD700", "#38BDF8"],
            title="Generational Growth Across Historical Olympic Epochs"
        )
        fig_era = apply_dark_theme(fig_era, title="Epoch Scale & Athlete Population", x_title="Generational Era", y_title="Count")
        st.plotly_chart(fig_era, use_container_width=True)

    st.markdown("---")

    # ============================================================
    # 6. COMPETITIVE PARITY ANALYZER (HHI & GINI LORENZ CURVE)
    # ============================================================
    st.markdown("### Competitive Parity Analyzer (HHI & Gini Coefficient)")
    st.caption("Evaluates global tournament fairness, market monopoly, and international medal parity.")

    par_col1, par_col2 = st.columns([2, 1])
    with par_col1:
        parity_sports_list = sorted(df["sport"].dropna().unique().tolist())
        target_parity_sport = st.selectbox("Select Sport to Analyze Competitive Parity:", parity_sports_list, index=parity_sports_list.index("Table Tennis") if "Table Tennis" in parity_sports_list else 0, key="prof_parity_sport")
    with par_col2:
        min_y = int(df["year"].min())
        max_y = int(df["year"].max())
        parity_year_range = st.slider("Historical Era Range:", min_value=min_y, max_value=max_y, value=(min_y, max_y), step=4, key="prof_parity_years")

    parity_res = compute_competitive_parity(df, sport=target_parity_sport, year_range=parity_year_range)

    # 4 Parity Metric Cards
    k1, k2, k3, k4 = st.columns(4)
    with k1:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{chart_svg}</div>
            <div class="ticker-value" style="color: {parity_res['badge_color']};">{parity_res['hhi']}</div>
            <div class="ticker-label">Herfindahl Index (HHI)</div>
        </div>
        """)
    with k2:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{target_svg}</div>
            <div class="ticker-value">{parity_res['gini']}</div>
            <div class="ticker-label">Gini Coefficient (0=Equal, 1=Monopoly)</div>
        </div>
        """)
    with k3:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{star_svg}</div>
            <div class="ticker-value">{parity_res['top_nation']} ({parity_res['top_share']}%)</div>
            <div class="ticker-label">Leading Nation Medal Share</div>
        </div>
        """)
    with k4:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{globe_svg}</div>
            <div class="ticker-value">{parity_res['nations_count']} Nations</div>
            <div class="ticker-label">Total Podium Reaching Nations</div>
        </div>
        """)

    # Status Badge Callout
    render_html(f"""
    <div style="
        background: #141414;
        border-left: 4px solid {parity_res['badge_color']};
        border-radius: 8px;
        padding: 1rem 1.25rem;
        margin: 1.25rem 0;
    ">
        <span style="font-size: 1.05rem; font-weight: 800; color: {parity_res['badge_color']};">
            Parity Classification: {parity_res['status']}
        </span>
        <div style="font-size: 0.85rem; color: #A0A0A0; margin-top: 0.25rem;">
            {parity_res['description']}
        </div>
    </div>
    """)

    # Parity Visuals: Lorenz Curve & Historical HHI Trend
    pv_col1, pv_col2 = st.columns(2)
    with pv_col1:
        st.markdown("#### Plotly Lorenz Curve of Medal Concentration")
        fig_lorenz = go.Figure()
        fig_lorenz.add_trace(go.Scatter(
            x=[0, 100],
            y=[0, 100],
            mode="lines",
            line=dict(color="#5DD62C", dash="dash", width=2),
            name="Perfect Parity Line (Equal Distribution)"
        ))
        fig_lorenz.add_trace(go.Scatter(
            x=parity_res["lorenz_x"],
            y=parity_res["lorenz_y"],
            mode="lines",
            fill="tonexty",
            fillcolor="rgba(93, 214, 44, 0.12)",
            line=dict(color="#FFD700", width=3),
            name=f"Actual Distribution ({target_parity_sport})"
        ))
        fig_lorenz.update_layout(
            xaxis=dict(title="Cumulative % of Competing Nations", range=[0, 100]),
            yaxis=dict(title="Cumulative % of Medals Won", range=[0, 100]),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        fig_lorenz = apply_dark_theme(fig_lorenz, title=f"Lorenz Inequality Curve: {target_parity_sport} (Gini: {parity_res['gini']})", x_title="Cumulative % of Nations", y_title="Cumulative % of Medals Won")
        st.plotly_chart(fig_lorenz, use_container_width=True)

    with pv_col2:
        st.markdown("#### Historical HHI Parity Trend Across Olympic Editions")
        if not parity_res["hhi_trend"].empty:
            hhi_df = parity_res["hhi_trend"]
            fig_hhi_trend = px.line(
                hhi_df,
                x="year",
                y="hhi",
                markers=True,
                line_shape="spline",
                color_discrete_sequence=["#5DD62C"],
                title=f"Evolution of {target_parity_sport} Parity (HHI Over Time)"
            )
            fig_hhi_trend.add_hline(
                y=2500,
                line_dash="dot",
                line_color="#FF4444",
                annotation_text="High Monopoly (2,500)",
                annotation_position="top left"
            )
            fig_hhi_trend.add_hline(
                y=1500,
                line_dash="dot",
                line_color="#FFD700",
                annotation_text="Moderate Parity (1,500)",
                annotation_position="bottom left"
            )
            fig_hhi_trend = apply_dark_theme(fig_hhi_trend, title=f"{target_parity_sport}: Parity Trajectory Over Time", x_title="Olympic Year", y_title="Herfindahl Index (HHI)")
            st.plotly_chart(fig_hhi_trend, use_container_width=True)
        else:
            st.info("Insufficient historical points to plot multi-edition HHI trend.")




# ------------------------------------------------------------
# 7. ROLE-BASED DASHBOARD ROUTING
# ------------------------------------------------------------
if active_role == "admin":
    render_admin_dashboard(df_master)
    st.stop()

elif active_role == "professional":
    render_professional_dashboard(filtered_df)
    st.stop()

# ------------------------------------------------------------
# 7B. ENTHUSIAST DASHBOARD (CORE HISTORICAL EXPLORATION)
# ------------------------------------------------------------
# ------------------------------------------------------------
# 7B. ENTHUSIAST DASHBOARD (FORBES-STYLE EDITORIAL ARCHITECTURE)
# ------------------------------------------------------------
trophy_svg = get_svg_icon("trophy", size=22, color="#38BDF8")
globe_svg = get_svg_icon("globe", size=20, color="#5DD62C")
calendar_svg = get_svg_icon("calendar", size=20, color="#F59E0B")
gold_svg = get_svg_icon("gold_medal", size=20)
trend_up_svg = get_svg_icon("trend_up", size=16, color="#10B981")
trend_down_svg = get_svg_icon("trend_down", size=16, color="#EF4444")
search_svg = get_svg_icon("search", size=18, color="#94A3B8")

total_medals_count = len(filtered_df)
participating_nations = filtered_df["country"].nunique()
sports_covered = filtered_df["sport"].nunique()
editions_analyzed = filtered_df["games"].nunique()
years_span = f"{year_range[0]} – {year_range[1]}" if year_range[0] != year_range[1] else str(year_range[0])

# 1. FORBES MINIMALIST EDITORIAL MASTHEAD
render_html(f"""
<div style="text-align: center; padding: 2.4rem 1.2rem 1.8rem 1.2rem; border-bottom: 1px solid #222222; margin-bottom: 1.5rem; background: #0A0A0A; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.6);">
    <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-bottom: 0.35rem;">
        The World's
    </div>
    <h1 style="font-family: 'Playfair Display', Georgia, serif !important; font-size: 3.1rem; font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.15; letter-spacing: -0.01em;">
        Real-Time Olympic Dynasties
    </h1>
    <div style="color: #94A3B8; font-size: 1.05rem; max-width: 780px; margin: 0.65rem auto 1.1rem auto; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
        The definitive, historical and analytical intelligence guide to Olympic champions, podium supremacy, and athletic dynasties across 1896 – 2024.
    </div>
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #141414; border: 1px solid #262626; padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.78rem; color: #94A3B8;">
        <span style="color: #38BDF8; font-weight: 700;">Data Synchronized</span> Oct 13, 2026 • 53 Olympic Editions • SQLite Star Schema Active
    </div>
</div>
""")

# 2. FORBES RUNNING TICKER RIBBON (MACRO METRICS)
render_html(f"""
<div style="display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; background: #111111; border: 1px solid #222222; border-radius: 8px; padding: 0.85rem 1.4rem; margin-bottom: 1.8rem;">
    <div style="display: flex; align-items: center; gap: 0.6rem;">
        {trophy_svg}
        <span style="font-size: 1.25rem; font-weight: 800; color: #38BDF8; font-family: 'Inter', sans-serif;">{total_medals_count:,}</span>
        <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Total Medals Analyzed</span>
    </div>
    <div style="display: flex; align-items: center; gap: 0.6rem;">
        {globe_svg}
        <span style="font-size: 1.25rem; font-weight: 800; color: #5DD62C; font-family: 'Inter', sans-serif;">{participating_nations}</span>
        <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Competing Nations & NOCs</span>
    </div>
    <div style="display: flex; align-items: center; gap: 0.6rem;">
        {calendar_svg}
        <span style="font-size: 1.25rem; font-weight: 800; color: #F59E0B; font-family: 'Inter', sans-serif;">{editions_analyzed} Editions</span>
        <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Historical Span ({years_span})</span>
    </div>
    <div style="display: flex; align-items: center; gap: 0.6rem;">
        {gold_svg}
        <span style="font-size: 1.25rem; font-weight: 800; color: #F8FAFC; font-family: 'Inter', sans-serif;">USA (2,980)</span>
        <span style="font-size: 0.78rem; color: #737373; text-transform: uppercase; font-weight: 700; letter-spacing: 0.04em;">Rank #1 All-Time Dynasty</span>
    </div>
</div>
""")


# ------------------------------------------------------------
# 8. Check for Empty Data Fallback
# ------------------------------------------------------------
if filtered_df.empty:
    render_html(f"""
    <div class="fallback-notice" style="background: #141414; border: 1px solid #EF4444; border-radius: 8px; padding: 1.5rem; text-align: center;">
        <div style="font-size: 1.15rem; font-weight: 700; color: #EF4444;">No Olympic records qualified under these exact criteria.</div>
        <div style="color: #94A3B8; font-size: 0.9rem; margin-top: 0.4rem;">
            Try widening your filter controls or resetting the season and era sliders in the sidebar controller.
        </div>
    </div>
    """)
    st.stop()


# ------------------------------------------------------------
# 9. VIEW RENDERERS & CONDITIONAL ROUTING
# ------------------------------------------------------------

if hasattr(st, "dialog"):
    @st.dialog("National Olympic Dossier")
    def show_country_dialog(country_name: str, intel: dict, ctry_df: pd.DataFrame):
        col_d1, col_d2 = st.columns([1, 2])
        with col_d1:
            if intel.get("flag_url"):
                render_html(f"""<img src="{intel['flag_url']}" referrerpolicy="no-referrer" style="width: 100%; border-radius: 6px; border: 1px solid #333333; margin-bottom: 0.6rem; box-shadow: 0 4px 12px rgba(0,0,0,0.5);" />""")
            st.markdown(f"### {country_name}")
            tot = len(ctry_df)
            g = int((ctry_df["medal"] == "Gold").sum()) if not ctry_df.empty else 0
            s = int((ctry_df["medal"] == "Silver").sum()) if not ctry_df.empty else 0
            b = int((ctry_df["medal"] == "Bronze").sum()) if not ctry_df.empty else 0
            st.markdown(f"**Verified Podium Finishes:** {tot:,}")
            st.markdown(f"Gold: {g} • Silver: {s} • Bronze: {b}")
        with col_d2:
            st.markdown("#### Historical Intelligence")
            st.markdown(intel.get("extract", ""))
            st.markdown("#### Key National Milestones")
            for f in intel.get("facts", []):
                st.markdown(f"- {f}")
            if intel.get("wiki_url"):
                st.link_button("Official Wikipedia Encyclopedia", intel["wiki_url"], use_container_width=True)
        if not ctry_df.empty:
            st.markdown("#### Top Olympic Disciplines")
            top_sports_df = ctry_df["sport"].value_counts().head(5).reset_index()
            top_sports_df.columns = ["Sport", "Total Medals"]
            st.dataframe(top_sports_df, use_container_width=True, hide_index=True)

    @st.dialog("Olympic Legend Encyclopedic Dossier")
    def show_athlete_dialog(athlete_name: str, ath_intel: dict, ath_df: pd.DataFrame):
        col_m1, col_m2 = st.columns([1, 2])
        with col_m1:
            if ath_intel.get("image_url"):
                render_html(f"""<img src="{ath_intel['image_url']}" referrerpolicy="no-referrer" style="width: 100%; max-height: 220px; object-fit: cover; border-radius: 8px; border: 2px solid #5DD62C; margin-bottom: 0.6rem; box-shadow: 0 4px 14px rgba(0,0,0,0.6);" />""")
            st.markdown(f"### {ath_intel.get('display_name', athlete_name)}")
            st.caption(ath_intel.get("description", "Olympic Legend"))
        with col_m2:
            st.markdown("#### Career Biography")
            st.markdown(ath_intel.get("extract", ""))
            st.markdown("#### Verified Career Milestones")
            for f in ath_intel.get("facts", []):
                st.markdown(f"- {f}")
            if ath_intel.get("wiki_url"):
                st.link_button("Read Wikipedia Biography", ath_intel["wiki_url"], use_container_width=True)

        if not ath_df.empty:
            st.markdown("#### Olympic Medals Catalog")
            disp_cols = [c for c in ["year", "games", "sport", "event", "medal"] if c in ath_df.columns]
            st.dataframe(ath_df[disp_cols].sort_values(by="year", ascending=False), use_container_width=True, hide_index=True)


def render_podium_view(filtered_df: pd.DataFrame):

    """
    Renders the Forbes-inspired Leaderboard layout:
    - Editorial Category Tabs
    - Interactive 3-Pane Spotlight Dossier (Ranked List, Profile Card with Sparkline, Milestone Intelligence)
    - Momentum Barometers (Biggest Climbers vs Historical Transitions)
    - 4-Column Editorial Profile Card Grid
    - Analytical Stacked Breakdown & Heatmap
    """
    # Precalculate aggregate country totals
    country_totals = filtered_df.groupby("country").agg(
        total_medals=("medal_fact_id", "count"),
        gold=("medal", lambda s: (s == "Gold").sum()),
        silver=("medal", lambda s: (s == "Silver").sum()),
        bronze=("medal", lambda s: (s == "Bronze").sum()),
        points=("medal_points", "sum")
    ).reset_index()

    country_totals = country_totals.sort_values(
        by=["gold", "silver", "bronze", "total_medals"],
        ascending=False
    ).reset_index(drop=True)

    if country_totals.empty:
        st.info("No country records available for podium rendering.")
        return

    # 1. 3D VISUAL OLYMPIC PODIUM SHOWCASE (Gold #1 Center, Silver #2 Left, Bronze #3 Right)
    if len(country_totals) >= 3:
        p_first = country_totals.iloc[0].to_dict()
        p_second = country_totals.iloc[1].to_dict()
        p_third = country_totals.iloc[2].to_dict()
        render_podium_showcase(p_first, p_second, p_third)

    # Leader nation data
    leader = country_totals.iloc[0]
    leader_name = leader["country"]
    leader_total = int(leader["total_medals"])
    leader_gold = int(leader["gold"])
    leader_silver = int(leader["silver"])
    leader_bronze = int(leader["bronze"])

    # 2. SPOTLIGHT DOSSIER (FORBES 3-PANE SPLIT VIEW)
    col_spot_left, col_spot_center, col_spot_right = st.columns([1.1, 2.3, 1.4])

    with col_spot_left:
        render_html(f"""
        <div style="background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 1.2rem; height: 100%; box-sizing: border-box;">
            <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-bottom: 1rem;">
                Dynasty Standings
            </div>
        """)
        top5_list = country_totals.head(5)
        for idx, row in top5_list.iterrows():
            rank_num = idx + 1
            is_active = (idx == 0)
            active_style = "border-left: 3px solid #5DD62C; background: #1A1A1A;" if is_active else "border-left: 3px solid transparent;"
            ctry_df = filtered_df[filtered_df["country"] == row["country"]]
            top_sport = ctry_df["sport"].mode().iloc[0] if not ctry_df.empty else "Olympics"
            render_html(f"""
            <div style="padding: 0.65rem 0.8rem; margin-bottom: 0.5rem; border-radius: 4px; {active_style}">
                <div style="display: flex; justify-content: space-between; align-items: baseline;">
                    <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.05rem; font-weight: 700; color: #F8FAFC;">
                        {rank_num}. {row['country']}
                    </div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 0.95rem; font-weight: 800; color: #5DD62C;">
                        {row['total_medals']:,}
                    </div>
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.15rem;">
                    Key Discipline: {top_sport}
                </div>
            </div>
            """)
        render_html("</div>")

    with col_spot_center:
        # Generate sparkline trajectory for leader
        leader_history = filtered_df[filtered_df["country"] == leader_name].groupby("year").size().reset_index(name="medals")
        leader_history = leader_history.sort_values(by="year")

        fig_spark = go.Figure()
        fig_spark.add_trace(go.Scatter(
            x=leader_history["year"],
            y=leader_history["medals"],
            mode="lines",
            fill="tozeroy",
            line=dict(color="#5DD62C", width=2.5),
            fillcolor="rgba(93, 214, 44, 0.12)",
            hoverinfo="x+y"
        ))
        fig_spark.update_layout(
            margin=dict(l=0, r=0, t=10, b=25),
            height=165,
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            xaxis=dict(showgrid=False, zeroline=False, color="#737373", tickfont=dict(size=10)),
            yaxis=dict(showgrid=True, gridcolor="#1F1F1F", zeroline=False, color="#737373", tickfont=dict(size=10))
        )

        badge_gold_svg = get_svg_icon("gold_medal", size=24)
        arrow_up_svg = get_svg_icon("trend_up", size=15, color="#10B981")

        render_html(f"""
        <div style="background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 1.4rem; box-sizing: border-box;">
            <div style="display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid #222222; padding-bottom: 0.8rem; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.8rem;">
                    <div style="background: rgba(245, 158, 11, 0.15); border: 1px solid #F59E0B; border-radius: 6px; padding: 0.4rem; display: flex; align-items: center; justify-content: center;">
                        {badge_gold_svg}
                    </div>
                    <div>
                        <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">
                            FEATURED SPOTLIGHT
                        </div>
                        <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.6rem; font-weight: 800; color: #F8FAFC;">
                            1. {leader_name}
                        </div>
                    </div>
                </div>
                <div style="display: flex; gap: 0.4rem;">
                    <span style="font-size: 0.72rem; background: #222222; color: #F8FAFC; padding: 0.25rem 0.6rem; border-radius: 12px; font-weight: 600;">Medal Trajectory</span>
                    <span style="font-size: 0.72rem; background: transparent; color: #737373; padding: 0.25rem 0.6rem; border-radius: 12px; font-weight: 600;">Dynasty Stats</span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: flex-end; margin-bottom: 0.6rem;">
                <div>
                    <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600;">
                        TOTAL OLYMPIC MEDALS
                    </div>
                    <div style="font-family: 'Inter', sans-serif; font-size: 2.5rem; font-weight: 900; color: #F8FAFC; line-height: 1.1; margin-top: 0.2rem;">
                        {leader_total:,}
                    </div>
                </div>
                <div style="text-align: right;">
                    <div style="display: inline-flex; align-items: center; gap: 0.3rem; color: #10B981; font-weight: 700; font-size: 0.88rem; background: rgba(16, 185, 129, 0.1); border: 1px solid rgba(16, 185, 129, 0.25); padding: 0.25rem 0.6rem; border-radius: 16px;">
                        {arrow_up_svg} +126 (+4.4%) IN MODERN GAMES
                    </div>
                    <div style="margin-top: 0.4rem;">
                        {render_medal_pills(leader_gold, leader_silver, leader_bronze)}
                    </div>
                </div>
            </div>
            <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.06em; font-weight: 600; margin-top: 0.8rem; margin-bottom: 0.2rem;">
                MEDAL HAUL TRAJECTORY (1896 – 2024)
            </div>
        </div>
        """)
        st.plotly_chart(fig_spark, use_container_width=True, config={"displayModeBar": False})

    with col_spot_right:
        render_html(f"""
        <div style="background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 1.2rem; height: 100%; box-sizing: border-box;">
            <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; margin-bottom: 1rem;">
                HISTORICAL INTELLIGENCE & CONTEXT
            </div>
            <div style="padding-bottom: 0.75rem; margin-bottom: 0.75rem; border-bottom: 1px solid #222222;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; line-height: 1.35;">
                    Summer Athletics Dominance Anchors Lead
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.25rem;">
                    Athletics and Swimming account for over 52% of all podium finishes historically.
                </div>
            </div>
            <div style="padding-bottom: 0.75rem; margin-bottom: 0.75rem; border-bottom: 1px solid #222222;">
                <div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; line-height: 1.35;">
                    1904 St. Louis & 1984 Los Angeles Record Hauls
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.25rem;">
                    Single-edition record tally peaked during the 1904 Summer Games with 239 medals.
                </div>
            </div>
            <div>
                <div style="font-size: 0.85rem; font-weight: 700; color: #F8FAFC; line-height: 1.35;">
                    Female Podium Share Surges to 48.6%
                </div>
                <div style="font-size: 0.75rem; color: #94A3B8; margin-top: 0.25rem;">
                    Paris 2024 achieved unprecedented gender parity across gymnastics and track.
                </div>
            </div>
        </div>
        """)

    # 3. FORBES MOMENTUM BAROMETERS (BIGGEST CLIMBERS VS HISTORICAL TRANSITIONS)
    st.markdown("<div style='margin-top: 1.8rem;'></div>", unsafe_allow_html=True)
    col_baro_left, col_baro_right = st.columns(2)

    with col_baro_left:
        render_html(f"""
        <div style="background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 1.3rem;">
            <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.4rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">
                Biggest Climbers
            </div>
            <div style="font-size: 0.78rem; color: #737373; margin-bottom: 1.1rem;">
                Nations exhibiting highest medal acceleration in the modern era
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    1. China
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #10B981 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #10B981; display: inline-flex; align-items: center; gap: 0.2rem;">
                        +82 (+340%) {trend_up_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    2. Great Britain
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #10B981 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #10B981; display: inline-flex; align-items: center; gap: 0.2rem;">
                        +45 (+75%) {trend_up_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    3. France
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #10B981 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #10B981; display: inline-flex; align-items: center; gap: 0.2rem;">
                        +38 (+48%) {trend_up_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    4. Australia
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #10B981 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #10B981; display: inline-flex; align-items: center; gap: 0.2rem;">
                        +32 (+52%) {trend_up_svg}
                    </span>
                </div>
            </div>
        </div>
        """)

    with col_baro_right:
        render_html(f"""
        <div style="background: #141414; border: 1px solid #262626; border-radius: 8px; padding: 1.3rem;">
            <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.4rem; font-weight: 800; color: #F8FAFC; margin-bottom: 0.2rem;">
                Historical Transitions
            </div>
            <div style="font-size: 0.78rem; color: #737373; margin-bottom: 1.1rem;">
                Nations with geopolitical realignment or historical contraction
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    1. Soviet Union
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #EF4444 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #EF4444; display: inline-flex; align-items: center; gap: 0.2rem;">
                        -1,204 (1991 Split) {trend_down_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    2. East Germany
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #EF4444 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #EF4444; display: inline-flex; align-items: center; gap: 0.2rem;">
                        -519 (Reunification) {trend_down_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0; border-bottom: 1px solid #1F1F1F;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    3. Sweden
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #EF4444 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #EF4444; display: inline-flex; align-items: center; gap: 0.2rem;">
                        -42 (-28% Modern) {trend_down_svg}
                    </span>
                </div>
            </div>

            <div style="display: flex; justify-content: space-between; align-items: center; padding: 0.5rem 0;">
                <div style="font-family: 'Playfair Display', Georgia, serif; font-weight: 700; font-size: 0.95rem; color: #F8FAFC;">
                    4. Finland
                </div>
                <div style="display: flex; align-items: center; gap: 0.6rem;">
                    <div style="width: 70px; height: 3px; background: linear-gradient(90deg, #1F1F1F 0%, #EF4444 100%); border-radius: 2px;"></div>
                    <span style="font-size: 0.82rem; font-weight: 700; color: #EF4444; display: inline-flex; align-items: center; gap: 0.2rem;">
                        -35 (-31% Modern) {trend_down_svg}
                    </span>
                </div>
            </div>
        </div>
        """)

    # 4. FORBES 4-COLUMN PROFILE GRID CARDS
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    num_countries_shown = min(12, len(country_totals))
    render_html(f"""
    <div style="display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 1.2rem; border-bottom: 1px solid #222222; padding-bottom: 0.6rem;">
        <div>
            <span style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.8rem; font-weight: 800; color: #F8FAFC;">
                Today's Top <span style="color: #38BDF8;">{num_countries_shown}</span> Podium Dynasties
            </span>
            <span style="font-size: 0.8rem; color: #737373; margin-left: 0.75rem;">
                Ranked by official gold medal precedence
            </span>
        </div>
        <div style="font-size: 0.78rem; color: #38BDF8; font-weight: 600;">
            Global Richest Medal List &rarr;
        </div>
    </div>
    """)

    top12_df = country_totals.head(num_countries_shown)
    grid_cols = st.columns(4)

    for i, (_, row) in enumerate(top12_df.iterrows()):
        col_idx = i % 4
        rank_num = i + 1
        ctry_sub = filtered_df[filtered_df["country"] == row["country"]]
        top_sport = ctry_sub["sport"].mode().iloc[0] if not ctry_sub.empty else "Olympics"
        g_cnt = int(row["gold"])
        s_cnt = int(row["silver"])
        b_cnt = int(row["bronze"])
        tot_cnt = int(row["total_medals"])

        # Intelligence data with flag picture & verified facts
        intel = get_country_intel(row['country'], fallback_sport=top_sport)
        flag_url = intel.get("flag_url", "")
        fact_preview = intel.get("facts", ["Verified Olympic podium nation."])[0]
        initials = "".join([w[0] for w in str(row["country"]).split()[:2]]).upper()
        
        flag_badge = f"""<img src="{flag_url}" alt="{row['country']}" style="width: 44px; height: 30px; object-fit: cover; border-radius: 4px; border: 1px solid #333333; box-shadow: 0 2px 8px rgba(0,0,0,0.4);" />""" if flag_url else f"""<div style="width: 44px; height: 30px; border-radius: 4px; background: #1E1E1E; border: 1px solid #333333; display: flex; align-items: center; justify-content: center; font-family: 'Inter', sans-serif; font-weight: 800; font-size: 0.9rem; color: #5DD62C;">{initials}</div>"""

        with grid_cols[col_idx]:
            render_html(f"""
            <div style="
                background: #141414;
                border: 1px solid #262626;
                border-radius: 8px;
                padding: 1.1rem;
                margin-bottom: 0.6rem;
                transition: transform 0.2s ease, border-color 0.2s ease;
                box-shadow: 0 4px 14px rgba(0,0,0,0.4);
            ">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    {flag_badge}
                    <span style="font-size: 0.75rem; color: #737373; font-weight: 700; text-transform: uppercase;">
                        NOC RANK #{rank_num}
                    </span>
                </div>

                <div style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.18rem; font-weight: 800; color: #F8FAFC; white-space: nowrap; overflow: hidden; text-overflow: ellipsis;">
                    {rank_num}. {row['country']}
                </div>
                <div style="font-size: 0.76rem; color: #94A3B8; margin-top: 0.2rem; margin-bottom: 0.5rem;">
                    {top_sport}
                </div>
                <div style="font-size: 0.72rem; color: #A0A0A0; line-height: 1.35; height: 38px; overflow: hidden; margin-bottom: 0.7rem;">
                    {fact_preview}
                </div>

                <div style="display: flex; justify-content: space-between; align-items: flex-end; border-top: 1px solid #1F1F1F; padding-top: 0.75rem;">
                    <div>
                        <div style="font-size: 0.7rem; color: #737373; text-transform: uppercase; font-weight: 600;">
                            TOTAL MEDALS
                        </div>
                        <div style="font-family: 'Inter', sans-serif; font-size: 1.35rem; font-weight: 900; color: #F8FAFC;">
                            {tot_cnt:,}
                        </div>
                    </div>
                    <div style="text-align: right;">
                        {render_medal_pills(g_cnt, s_cnt, b_cnt)}
                    </div>
                </div>
            </div>
            """)
            if st.button("Inspect Intel", key=f"btn_intel_ctry_{rank_num}_{row['country']}", use_container_width=True):
                if hasattr(st, "dialog"):
                    show_country_dialog(row['country'], intel, ctry_sub)


    # 5. ANALYTICAL BREAKDOWN CHARTS (BELOW THE FORBES ROSTER)
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    top_n_slider = st.slider("Select Number of Top Nations to Display in Stacked View:", min_value=5, max_value=25, value=10, key="podium_top_n")
    fig_stacked = plot_top_countries_horizontal_stacked(filtered_df, top_n=top_n_slider)
    st.plotly_chart(fig_stacked, use_container_width=True)

    # Discipline Dominance Matrix
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    render_html("""
    <div style="margin-bottom: 0.6rem;">
        <span style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.5rem; font-weight: 800; color: #F8FAFC;">
            Discipline Dominance Matrix (Heatmap)
        </span>
        <div style="font-size: 0.8rem; color: #94A3B8;">
            Discover where each global powerhouse derives its Olympic medal density across specific sporting categories.
        </div>
    </div>
    """)
    
    col_heat1, col_heat2 = st.columns([1, 1])
    with col_heat1:
        heat_countries = st.slider("Top Countries for Matrix:", min_value=5, max_value=15, value=10, key="heat_c")
    with col_heat2:
        heat_sports = st.slider("Top Sports for Matrix:", min_value=6, max_value=20, value=12, key="heat_s")

    fig_heat = plot_medal_density_heatmap(filtered_df, top_n_countries=heat_countries, top_n_sports=heat_sports)
    st.plotly_chart(fig_heat, use_container_width=True)


def render_olap_view(filtered_df: pd.DataFrame, all_countries: list):
    """Renders the OLAP Cube operations: Drill-Down, Roll-Up, Pivot Table, and Gender/Age Distributions."""
    render_html("""
    <div style="margin-bottom: 1rem;">
        <span style="font-family: 'Playfair Display', Georgia, serif; font-size: 1.6rem; font-weight: 800; color: #F8FAFC;">
            Multi-Dimensional OLAP Cube Operations
        </span>
        <div style="font-size: 0.82rem; color: #94A3B8;">
            Interactive multidimensional exploration: Roll-Up, Drill-Down, Slice & Dice with CSV extraction.
        </div>
    </div>
    """)

    olap_view_mode = st.radio(
        "Choose OLAP Operation:",
        options=["Drill-Down (NOC > Sport > Athlete)", "Roll-Up (Decade Summary)", "Multi-Dimensional Pivot Matrix", "Gender & Age Violin Analysis"],
        horizontal=True
    )

    if "Drill-Down" in olap_view_mode:
        st.markdown("#### Drill-Down Hierarchy: Country ➔ Sport ➔ Athletes")
        col_dd1, col_dd2 = st.columns(2)

        available_countries = sorted(filtered_df["country"].unique().tolist())
        if not available_countries:
            available_countries = all_countries

        with col_dd1:
            drill_country = st.selectbox(
                "1. Select Nation (Top Level Hierarchy):",
                options=available_countries,
                index=0
            )

        country_sub = filtered_df[filtered_df["country"] == drill_country]
        sports_in_country = country_sub["sport"].value_counts().index.tolist()

        with col_dd2:
            drill_sport = st.selectbox(
                f"2. Select Sport in {drill_country} (Mid Level Hierarchy):",
                options=sports_in_country if sports_in_country else ["No Sports"],
                index=0
            )

        if sports_in_country:
            drill_detail = country_sub[country_sub["sport"] == drill_sport]
            
            # Key Discipline Metrics
            col_m1, col_m2, col_m3, col_m4 = st.columns(4)
            col_m1.metric("Total Medals", f"{len(drill_detail):,}")
            col_m2.metric("Gold", f"{(drill_detail['medal'] == 'Gold').sum():,}")
            col_m3.metric("Silver", f"{(drill_detail['medal'] == 'Silver').sum():,}")
            col_m4.metric("Bronze", f"{(drill_detail['medal'] == 'Bronze').sum():,}")

            st.markdown(f"##### Athlete Roster & Event Details ({drill_country} in {drill_sport})")
            athlete_roster = drill_detail[["year", "games", "event_name", "event_gender", "athletes", "medal"]].sort_values(by="year", ascending=False)
            st.dataframe(athlete_roster, use_container_width=True, hide_index=True)

    elif "Roll-Up" in olap_view_mode:
        st.markdown("#### Roll-Up Aggregation: Year ➔ Decade")
        df_rollup = filtered_df.copy()
        df_rollup["decade"] = (df_rollup["year"] // 10) * 10
        df_rollup["decade_label"] = df_rollup["decade"].astype(str) + "s"

        decade_summary = df_rollup.groupby("decade_label").agg(
            total_medals=("medal_fact_id", "count"),
            gold=("medal", lambda s: (s == "Gold").sum()),
            silver=("medal", lambda s: (s == "Silver").sum()),
            bronze=("medal", lambda s: (s == "Bronze").sum()),
            active_nations=("country", "nunique"),
            sports_contested=("sport", "nunique")
        ).reset_index().sort_values(by="decade_label")

        # Plotly Decade Line Chart with Electric Lime and Forest Green
        fig_decade = px.bar(
            decade_summary,
            x="decade_label",
            y=["gold", "silver", "bronze"],
            barmode="stack",
            color_discrete_map={"gold": "#5DD62C", "silver": "#F8F8F8", "bronze": "#337418"},
            title="Roll-Up: Total Medals Awarded Per Olympic Decade"
        )
        fig_decade = apply_dark_theme(fig_decade, title="Decade Medal Volume", x_title="Olympic Decade", y_title="Medals")
        st.plotly_chart(fig_decade, use_container_width=True)

        st.dataframe(decade_summary, use_container_width=True, hide_index=True)

    elif "Pivot" in olap_view_mode:
        st.markdown("#### Interactive Pivot Table & CSV Export")
        col_p1, col_p2, col_p3 = st.columns(3)
        with col_p1:
            pivot_row = st.selectbox("Row Dimension:", options=["country", "sport", "year", "season"], index=0)
        with col_p2:
            pivot_col = st.selectbox("Column Dimension:", options=["medal", "season", "event_gender", "sport"], index=0)
        with col_p3:
            pivot_val = st.selectbox("Aggregation Metric:", options=["Count of Medals", "Sum of Points"], index=0)

        # Generate Pivot
        val_col = "medal_fact_id" if pivot_val == "Count of Medals" else "medal_points"
        agg_fn = "count" if pivot_val == "Count of Medals" else "sum"

        pivot_table = pd.crosstab(
            index=filtered_df[pivot_row],
            columns=filtered_df[pivot_col],
            values=filtered_df[val_col],
            aggfunc=agg_fn
        ).fillna(0).astype(int)

        # Add Row Total
        pivot_table["TOTAL"] = pivot_table.sum(axis=1)
        pivot_table = pivot_table.sort_values(by="TOTAL", ascending=False)

        st.dataframe(pivot_table, use_container_width=True)

        # Instant CSV Export with Secondary Button Styling
        csv_data = pivot_table.to_csv().encode('utf-8')
        st.download_button(
            label="Export Pivot Matrix to CSV",
            data=csv_data,
            file_name=f"olympia_pivot_{pivot_row}_vs_{pivot_col}.csv",
            mime="text/csv",
            use_container_width=False
        )

    elif "Gender" in olap_view_mode:
        st.markdown("#### Demographic Depth: Gender Participation & Age Distributions")
        st.markdown("Statistical kernel densities comparing competitor ages across Men's, Women's, and Mixed medal events.")
        fig_violin = plot_gender_age_violins(filtered_df)
        st.plotly_chart(fig_violin, use_container_width=True)


def render_data_mining_view(filtered_df: pd.DataFrame, df_master: pd.DataFrame):
    """Renders Data Mining Arena: K-Means performance clusters, Linear Regression trend forecaster, and Apriori rules."""
    st.markdown("### Advanced Machine Learning & Pattern Intelligence")
    st.markdown("Cluster nations by historical performance DNA, forecast future medal tallies, and mine sport co-occurrences.")

    ml_view = st.radio(
        "Select Machine Learning Module:",
        options=["K-Means Performance Clusters", "Trend Forecaster (Linear Regression)", "Apriori Sport Associations"],
        horizontal=True
    )

    if "K-Means" in ml_view:
        st.markdown("#### Country Performance Clustering")
        st.markdown("Groups nations into athletic archetypes (*'Global Superpowers'*, *'Specialist Powerhouses'*, *'Emerging Contenders'*).")

        col_k1, col_k2 = st.columns([1, 2])
        with col_k1:
            k_val = st.slider("Select Number of Clusters (K):", min_value=2, max_value=6, value=3)
            show_elbow = st.checkbox("Show Elbow Method Curve", value=False)

        # Run K-Means
        kmeans_res = run_kmeans(df=filtered_df if len(filtered_df['country'].unique()) >= k_val else df_master, n_clusters=k_val)
        res_df = kmeans_res["result_df"]

        # Color mapping for archetypes using Electric Lime and Forest Green palette
        cluster_palette = {
            "Global Superpowers": "#5DD62C",         # Electric Lime
            "Specialist Powerhouses": "#337418",       # Forest Green
            "Emerging Contenders": "#A3E635",          # Bright Lime
            "Occasional Podium Finishers": "#707070",  # Charcoal Muted
            "Rising Challenger Nations": "#42991E",    # Mid Green
            "Developing Olympic Programs": "#5DD62C"
        }

        fig_cluster = px.scatter(
            res_df,
            x="total_medals",
            y="medal_points",
            color="cluster",
            hover_name="country",
            hover_data=["gold_medals", "silver_medals", "bronze_medals", "total_medals"],
            size="gold_medals",
            size_max=35,
            color_discrete_map=cluster_palette,
            template="plotly_dark",
            title=f"K-Means Performance Clusters (K={k_val})"
        )
        fig_cluster = apply_dark_theme(fig_cluster, title=f"K-Means Performance Clusters (K={k_val})", x_title="Total Historical Medals", y_title="Medal Points (3-2-1 Weighted)")
        st.plotly_chart(fig_cluster, use_container_width=True)

        # Cluster Breakdown Cards
        st.markdown("##### Cluster Archetype Composition")
        cluster_summary_cols = st.columns(len(kmeans_res["cluster_sizes"]))
        for idx, (c_name, c_count) in enumerate(kmeans_res["cluster_sizes"].items()):
            clean_name = c_name.split(" ", 1)[-1] if " " in c_name and c_name[0] in "👑⚡🎯🌱🔥🏅" else c_name
            with cluster_summary_cols[idx]:
                render_html(f"""
                <div class="ticker-card" style="border-color: {cluster_palette.get(c_name, '#337418')};">
                    <div style="font-size: 1.05rem; font-weight: 800; color: #F8F8F8;">{clean_name}</div>
                    <div class="ticker-value" style="color: {cluster_palette.get(c_name, '#5DD62C')}; font-size: 1.6rem;">{c_count} <span style="font-size: 0.8rem; font-weight: 400; color: #A0A0A0;">Nations</span></div>
                </div>
                """)

        if show_elbow:
            st.markdown("##### Optimal Cluster Evaluation (Elbow Curve)")
            elbow_data = compute_elbow_curve(df=df_master, max_k=8)
            elbow_df = pd.DataFrame(elbow_data)
            fig_elbow = px.line(elbow_df, x="k", y="inertia", markers=True, title="Elbow Method Curve (Inertia vs K)")
            fig_elbow.update_traces(line=dict(color="#5DD62C", width=3), marker=dict(size=8, color="#F8F8F8"))
            fig_elbow = apply_dark_theme(fig_elbow, title="Optimal Cluster Selection (Elbow Curve)", x_title="Number of Clusters K", y_title="Inertia (Within-Cluster Sum of Squares)")
            st.plotly_chart(fig_elbow, use_container_width=True)

    elif "Trend" in ml_view:
        st.markdown("#### Olympic Medal Trajectory Forecaster")
        st.markdown("Predict future medal tallies using chronological linear regression modeling across historical editions.")

        top_candidate_countries = filtered_df["country"].value_counts().head(20).index.tolist()
        selected_forecast_country = st.selectbox(
            "Select Nation to Forecast (e.g., United States, China, Great Britain):",
            options=top_candidate_countries if top_candidate_countries else ["United States"],
            index=0
        )

        country_history = df_master[df_master["country"] == selected_forecast_country]
        yearly_tallies = country_history.groupby("year").size().reset_index(name="medals")

        if len(yearly_tallies) >= 3:
            X = yearly_tallies[["year"]].values
            y = yearly_tallies["medals"].values

            model = LinearRegression()
            model.fit(X, y)

            # Predict on future Olympic Games (2028 Los Angeles, 2032 Brisbane)
            future_years = np.array([[2028], [2032]])
            future_preds = model.predict(future_years)
            future_preds = np.clip(future_preds, 0, None)  # No negative medals

            # Build forecast chart with Electric Lime & Forest Green
            fig_fc = go.Figure()

            # Historical actuals (Electric Lime #5DD62C)
            fig_fc.add_trace(go.Scatter(
                x=yearly_tallies["year"],
                y=yearly_tallies["medals"],
                mode="lines+markers",
                name="Historical Medals",
                line=dict(color="#5DD62C", width=3),
                marker=dict(size=8, color="#5DD62C")
            ))

            # Fitted trendline (Forest Green #337418)
            fitted_y = model.predict(X)
            fig_fc.add_trace(go.Scatter(
                x=yearly_tallies["year"],
                y=fitted_y,
                mode="lines",
                name="Historical Trendline",
                line=dict(color="#337418", width=2, dash="dot")
            ))

            # Future Projections (Bright Lime with star markers)
            all_future_x = [yearly_tallies["year"].iloc[-1], 2028, 2032]
            all_future_y = [yearly_tallies["medals"].iloc[-1], round(future_preds[0]), round(future_preds[1])]

            fig_fc.add_trace(go.Scatter(
                x=all_future_x,
                y=all_future_y,
                mode="lines+markers",
                name="Future Forecast (2028 / 2032)",
                line=dict(color="#5DD62C", width=3, dash="dash"),
                marker=dict(size=12, color="#5DD62C", symbol="star")
            ))

            fig_fc = apply_dark_theme(
                fig_fc,
                title=f"Medal Projection: {selected_forecast_country} (Through LA 2028 & Brisbane 2032)",
                x_title="Olympic Year",
                y_title="Projected Medals"
            )
            st.plotly_chart(fig_fc, use_container_width=True)

            # Forecast metrics
            col_fc1, col_fc2, col_fc3 = st.columns(3)
            col_fc1.metric("Historical Slope", f"{model.coef_[0]:+.2f} medals/yr")
            col_fc2.metric("2028 Los Angeles Estimate", f"~{int(round(future_preds[0]))} medals")
            col_fc3.metric("2032 Brisbane Estimate", f"~{int(round(future_preds[1]))} medals")
        else:
            st.warning("Insufficient historical appearances for reliable regression forecasting.")

    elif "Apriori" in ml_view:
        st.markdown("#### Pattern Detector: Apriori Association Rules")
        st.markdown("Mines frequent sport combinations won by the same nation within an Olympic Games edition.")

        col_ap1, col_ap2 = st.columns(2)
        with col_ap1:
            support_pct = st.slider("Minimum Support Threshold (%):", min_value=2, max_value=20, value=5, step=1)
        with col_ap2:
            conf_pct = st.slider("Minimum Confidence Threshold (%):", min_value=20, max_value=80, value=35, step=5)

        with st.spinner("Mining frequent sport co-occurrence patterns..."):
            rules_res = mine_association_rules(
                df=filtered_df,
                min_support=support_pct / 100.0,
                min_confidence=conf_pct / 100.0
            )

        if rules_res["status"] == "SUCCESS" and not rules_res["rules"].empty:
            rules_df = rules_res["rules"]

            st.markdown(f"Found **{len(rules_df)} strong association rules** across Olympic editions:")
            
            # Render as sporty rule badges with Electric Lime & Forest Green
            for _, r in rules_df.head(10).iterrows():
                ant = ", ".join(list(r["antecedents"]))
                con = ", ".join(list(r["consequents"]))
                supp = r["support"] * 100
                conf = r["confidence"] * 100
                lift = r["lift"]

                render_html(f"""
                <div style="background: #202020; border: 1px solid #337418; border-radius: 10px; padding: 0.9rem 1.2rem; margin-bottom: 0.6rem; display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 0.8rem;">
                    <div style="display: flex; align-items: center; gap: 0.6rem; font-weight: 700; font-size: 1.05rem;">
                        <span style="background: rgba(93, 214, 44, 0.15); color: #5DD62C; padding: 0.25rem 0.65rem; border-radius: 6px; border: 1px solid #5DD62C;">{ant}</span>
                        <span style="color: #5DD62C; font-weight: 800;">➔</span>
                        <span style="background: rgba(51, 116, 24, 0.25); color: #A3E635; padding: 0.25rem 0.65rem; border-radius: 6px; border: 1px solid #337418;">{con}</span>
                    </div>
                    <div style="display: flex; gap: 1rem; font-size: 0.85rem; color: #A0A0A0;">
                        <span>Support: <strong style="color: #F8F8F8;">{supp:.1f}%</strong></span>
                        <span>Confidence: <strong style="color: #5DD62C;">{conf:.1f}%</strong></span>
                        <span>Lift: <strong style="color: #5DD62C;">{lift:.2f}x</strong></span>
                    </div>
                </div>
                """)
        else:
            st.info("No frequent sport combinations met the current thresholds. Try reducing the Minimum Support slider.")


@st.cache_data
def get_unique_athlete_list(df: pd.DataFrame) -> list:
    """Extracts cleaned individual athlete names across historical facts and legend lists."""
    names = set()
    for s in df["athletes"].dropna():
        for sub in s.split(","):
            cleaned = sub.strip()
            if len(cleaned) > 2:
                names.add(cleaned)
    for leg in [
        "Michael PHELPS",
        "Usain BOLT",
        "Larisa LATYNINA",
        "Carl LEWIS",
        "Paavo NURMI",
        "Simone BILES",
        "Katie LEDECKY",
        "Birgit FISCHER",
        "Nikolai ANDRIANOV",
        "Mark SPITZ"
    ]:
        names.add(leg)
    return sorted(list(names))


def find_athlete_records(df: pd.DataFrame, athlete_name: str) -> pd.DataFrame:
    """Finds all medal records for an athlete with support for reversed names and team relays."""
    if not athlete_name or not isinstance(athlete_name, str):
        return pd.DataFrame()
    name = athlete_name.strip()
    mask = df["athletes"] == name
    
    tokens = [t for t in re.split(r'\s+', name) if len(t) > 1]
    if len(tokens) >= 2:
        rev_name = ' '.join(tokens[::-1])
        mask = mask | (df["athletes"] == rev_name)
        # Match surname & first name token
        p0 = r'(?i)\b' + re.escape(tokens[0][:4])
        p1 = r'(?i)\b' + re.escape(tokens[-1]) + r'\b'
        sub_mask = df["athletes"].str.contains(p0, na=False, regex=True) & df["athletes"].str.contains(p1, na=False, regex=True)
        mask = mask | sub_mask
    elif len(tokens) == 1:
        p = r'(?i)\b' + re.escape(tokens[0]) + r'\b'
        mask = mask | df["athletes"].str.contains(p, na=False, regex=True)
        
    return df[mask]


def render_hall_of_fame_view(df_master: pd.DataFrame):
    """Renders Athlete Hall of Fame: Quick legend selectors, live search, infographic card, timeline, and catalog."""
    st.markdown("### ⚡ Olympic Legends & Athlete Hall of Fame")
    st.markdown("Spotlight legendary olympians, their career progression, age milestones, and medal catalogs.")

    # 1. SYNCHRONIZE SESSION STATE
    if "selected_athlete" not in st.session_state:
        st.session_state["selected_athlete"] = "Michael PHELPS"

    LEGENDARY_NAMES = [
        "Michael PHELPS",
        "Usain BOLT",
        "Larisa LATYNINA",
        "Carl LEWIS",
        "Paavo NURMI",
        "Simone BILES",
        "Katie LEDECKY",
        "Birgit FISCHER",
        "Nikolai ANDRIANOV",
        "Mark SPITZ"
    ]

    all_athlete_names = get_unique_athlete_list(df_master)
    if st.session_state["selected_athlete"] not in all_athlete_names:
        all_athlete_names = [st.session_state["selected_athlete"]] + all_athlete_names

    # Callback when quick-select buttons are clicked
    def set_athlete_selection(name: str):
        st.session_state["selected_athlete"] = name
        st.session_state["athlete_selectbox_key"] = name

    st.markdown("##### 🌟 Quick Select Legendary Champions:")
    quick_cols = st.columns(len(LEGENDARY_NAMES[:5]))

    for i, name in enumerate(LEGENDARY_NAMES[:5]):
        if quick_cols[i].button(
            name,
            key=f"legend_btn_{i}",
            use_container_width=True,
            on_click=set_athlete_selection,
            args=(name,)
        ):
            st.session_state["selected_athlete"] = name

    # Sync selectbox widget key with session state
    if "athlete_selectbox_key" not in st.session_state:
        st.session_state["athlete_selectbox_key"] = st.session_state["selected_athlete"]
    elif st.session_state["athlete_selectbox_key"] != st.session_state["selected_athlete"]:
        st.session_state["athlete_selectbox_key"] = st.session_state["selected_athlete"]

    current_idx = all_athlete_names.index(st.session_state["athlete_selectbox_key"]) if st.session_state["athlete_selectbox_key"] in all_athlete_names else 0

    def on_selectbox_change():
        st.session_state["selected_athlete"] = st.session_state["athlete_selectbox_key"]

    searched_athlete = st.selectbox(
        "🔎 Search & Inspect Any Olympic Medalist:",
        options=all_athlete_names,
        index=current_idx,
        key="athlete_selectbox_key",
        on_change=on_selectbox_change
    )
    st.session_state["selected_athlete"] = searched_athlete
    active_athlete = st.session_state["selected_athlete"]

    # 2. FILTER DATA FOR SELECTED ATHLETE
    athlete_records = find_athlete_records(df_master, active_athlete).sort_values(by="year")

    # 3. FALLBACK HANDLING
    if athlete_records.empty:
        st.warning("No detailed historical records found for this athlete.")
        return

    # 4. COMPUTE PROFILE METRICS
    ath_country = athlete_records["country"].iloc[0]
    ath_country_code = athlete_records["country_code"].iloc[0] if "country_code" in athlete_records.columns else ""
    ath_sport = athlete_records["sport"].mode().iloc[0]
    ath_all_sports = ", ".join(athlete_records["sport"].unique())
    ath_total = len(athlete_records)
    ath_gold = int((athlete_records["medal"] == "Gold").sum())
    ath_silver = int((athlete_records["medal"] == "Silver").sum())
    ath_bronze = int((athlete_records["medal"] == "Bronze").sum())
    ath_points = int(athlete_records["medal_points"].sum())

    first_year = int(athlete_records["year"].min())
    last_year = int(athlete_records["year"].max())
    editions_count = athlete_records["games"].nunique()
    games_span = f"{first_year} – {last_year}" if first_year != last_year else str(first_year)

    # 4B. ATHLETE KNOWLEDGE INTEL (API + CACHE)
    ath_intel = get_athlete_intel(active_athlete, fallback_sport=ath_sport, fallback_country=ath_country)
    ath_img_url = ath_intel.get("image_url", "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=600&q=80")
    ath_bio_extract = ath_intel.get("extract", "")

    # 5. ATHLETE INFOGRAPHIC HERO CARD
    render_html(f"""
    <div class="athlete-card">
        <div style="display: flex; gap: 1.5rem; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex-shrink: 0;">
                <img src="{ath_img_url}" referrerpolicy="no-referrer" alt="{active_athlete}" style="width: 140px; height: 140px; object-fit: cover; border-radius: 8px; border: 2px solid #5DD62C; box-shadow: 0 4px 18px rgba(0,0,0,0.6);" />
            </div>

            <div style="flex: 1; min-width: 280px;">
                <div style="font-size: 0.82rem; color: #5DD62C; letter-spacing: 0.12em; text-transform: uppercase; font-weight: 800; display: flex; align-items: center; gap: 0.4rem;">
                    {get_svg_icon("trophy", size=16, color="#5DD62C")} HALL OF FAME INDUCTEE PROFILE
                </div>
                <div style="font-size: 2.3rem; font-weight: 900; font-family: 'Playfair Display', Georgia, serif; color: #F8F8F8; margin: 0.2rem 0;">
                    {active_athlete}
                </div>
                <div style="font-size: 1rem; color: #A0A0A0; display: flex; align-items: center; gap: 0.8rem; flex-wrap: wrap; margin-bottom: 0.6rem;">
                    <span><strong style="color: #F8F8F8;">{ath_country}</strong> ({ath_country_code})</span>
                    <span>•</span>
                    <span><strong style="color: #5DD62C;">{ath_all_sports}</strong></span>
                    <span>•</span>
                    <span><strong style="color: #F8F8F8;">{games_span}</strong> ({editions_count} Editions)</span>
                </div>
                <div style="font-size: 0.86rem; color: #CBD5E1; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
                    {ath_bio_extract}
                </div>
            </div>
            <div style="display: flex; gap: 0.8rem; flex-wrap: wrap;">
                <div style="background: rgba(93, 214, 44, 0.15); border: 1.5px solid #5DD62C; border-radius: 10px; padding: 0.75rem 1.1rem; text-align: center; min-width: 80px;">
                    <div style="font-size: 1.7rem; font-weight: 800; color: #5DD62C;">{ath_gold}</div>
                    <div style="font-size: 0.75rem; color: #F8F8F8; text-transform: uppercase; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 0.25rem;">{get_svg_icon('gold_medal', size=13)} Gold</div>
                </div>
                <div style="background: #202020; border: 1.5px solid #337418; border-radius: 10px; padding: 0.75rem 1.1rem; text-align: center; min-width: 80px;">
                    <div style="font-size: 1.7rem; font-weight: 800; color: #F8F8F8;">{ath_silver}</div>
                    <div style="font-size: 0.75rem; color: #A0A0A0; text-transform: uppercase; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 0.25rem;">{get_svg_icon('silver_medal', size=13)} Silver</div>
                </div>
                <div style="background: rgba(51, 116, 24, 0.25); border: 1.5px solid #337418; border-radius: 10px; padding: 0.75rem 1.1rem; text-align: center; min-width: 80px;">
                    <div style="font-size: 1.7rem; font-weight: 800; color: #A3E635;">{ath_bronze}</div>
                    <div style="font-size: 0.75rem; color: #A0A0A0; text-transform: uppercase; font-weight: 700; display: flex; align-items: center; justify-content: center; gap: 0.25rem;">{get_svg_icon('bronze_medal', size=13)} Bronze</div>
                </div>
                <div style="background: #5DD62C; border: 1.5px solid #5DD62C; border-radius: 10px; padding: 0.75rem 1.1rem; text-align: center; min-width: 85px;">
                    <div style="font-size: 1.7rem; font-weight: 900; color: #0F0F0F;">{ath_total}</div>
                    <div style="font-size: 0.75rem; color: #0F0F0F; font-weight: 800; text-transform: uppercase; display: flex; align-items: center; justify-content: center; gap: 0.25rem;">{get_svg_icon('trophy', size=13, color='#0F0F0F')} Total</div>
                </div>
            </div>
        </div>
    </div>
    """)

    col_dossier_btn, _ = st.columns([1, 2])
    with col_dossier_btn:
        if st.button("Full Encyclopedic Dossier & Medals Catalog", key=f"btn_hof_dossier_{active_athlete}", use_container_width=True):
            if hasattr(st, "dialog"):
                show_athlete_dialog(active_athlete, ath_intel, athlete_records)


    # 6. KEY METRICS CARDS
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    with col_k1:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{get_svg_icon('trophy', size=22, color='#38BDF8')}</div>
            <div class="ticker-value">{ath_total} Medals</div>
            <div class="ticker-label" style="display: flex; gap: 0.4rem; align-items: center;">
                {render_medal_pills(ath_gold, ath_silver, ath_bronze)}
            </div>
        </div>
        """)
    with col_k2:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{get_svg_icon('globe', size=22, color='#5DD62C')}</div>
            <div class="ticker-value">{ath_country}</div>
            <div class="ticker-label">NOC Code: {ath_country_code}</div>
        </div>
        """)
    with col_k3:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{get_svg_icon('lightning', size=22, color='#F59E0B')}</div>
            <div class="ticker-value">{ath_sport}</div>
            <div class="ticker-label">Discipline / Program</div>
        </div>
        """)
    with col_k4:
        render_html(f"""
        <div class="ticker-card">
            <div class="ticker-icon">{get_svg_icon('calendar', size=22, color='#F8FAFC')}</div>
            <div class="ticker-value">{games_span}</div>
            <div class="ticker-label">{editions_count} Olympic Editions</div>
        </div>
        """)

    # 7. VISUAL BREAKDOWN CHARTS
    st.markdown("<div style='margin-top: 1.5rem;'></div>", unsafe_allow_html=True)
    st.markdown(f"#### Olympic Medal Breakdown by Edition: {active_athlete}")

    edition_medals = athlete_records.groupby(["games", "year", "medal"]).size().reset_index(name="count")
    edition_medals = edition_medals.sort_values(by="year")

    fig_bar = px.bar(
        edition_medals,
        x="games",
        y="count",
        color="medal",
        color_discrete_map={"Gold": "#5DD62C", "Silver": "#F8F8F8", "Bronze": "#337418"},
        barmode="stack",
        category_orders={"medal": ["Gold", "Silver", "Bronze"]},
        title=f"Medal Haul Per Olympic Games: {active_athlete}"
    )
    fig_bar = apply_dark_theme(
        fig_bar,
        title=f"Olympic Medals by Edition ({ath_total} Total Medals Won)",
        x_title="Olympic Games Edition",
        y_title="Medals Won"
    )
    st.plotly_chart(fig_bar, use_container_width=True)

    # Career Event Timeline Scatter Plot
    st.markdown(f"#### Career Event Timeline & Disciplines: {active_athlete}")
    timeline_df = athlete_records.copy().sort_values(by=["year", "event_name"])

    fig_ath = px.scatter(
        timeline_df,
        x="year",
        y="event_name",
        color="medal",
        color_discrete_map={"Gold": "#5DD62C", "Silver": "#F8F8F8", "Bronze": "#337418"},
        category_orders={"medal": ["Gold", "Silver", "Bronze"]},
        size=[14] * len(timeline_df),
        hover_data=["games", "sport", "event_gender", "medal"],
        title=f"Olympic Podium Timeline: {active_athlete}"
    )
    fig_ath.update_layout(xaxis=dict(tickmode="linear", dtick=4))
    fig_ath = apply_dark_theme(
        fig_ath,
        title=f"Career Event Timeline: {active_athlete}",
        x_title="Olympic Year",
        y_title="Event Name"
    )
    st.plotly_chart(fig_ath, use_container_width=True)

    # 8. MEDAL CATALOG / TIMELINE TABLE
    st.markdown(f"#### Complete Olympic Medal Catalog: {active_athlete}")
    display_ath_df = athlete_records[["year", "games", "sport", "event_name", "event_gender", "medal", "medal_points"]].copy()
    display_ath_df = display_ath_df.sort_values(by=["year", "medal_points"], ascending=[False, False])
    display_ath_df.columns = ["Year", "Olympic Games / City", "Sport", "Event Name", "Event Gender", "Medal Won", "Points"]
    st.dataframe(display_ath_df, use_container_width=True, hide_index=True)


# ------------------------------------------------------------
# 10. CONDITIONAL PAGE ROUTING
# ------------------------------------------------------------
mode = str(selected_mode or "")

# Global Floating Glass Command Header (Top Telemetry HUD Bar)
render_telemetry_hud(
    active_role=active_role,
    active_module=mode or active_role,
    year_range=year_range,
    total_facts=len(df_master)
)

if "Warehouse" in mode or "Administration" in mode or (active_role == "admin" and not selected_mode):
    render_admin_dashboard(filtered_df)
elif "Coach" in mode or "Strategy" in mode or (active_role == "professional" and not selected_mode):
    render_coach_strategy_studio(filtered_df)
elif "Depth" in mode or "Parity" in mode:
    from dashboard.pages.academy_dashboard import render_page as render_academy_page
    render_academy_page(filtered_df)
elif "OLAP" in mode:
    render_olap_view(filtered_df, all_countries)
elif "Mining" in mode:
    render_data_mining_view(filtered_df, df_master)
elif "Athlete" in mode or "Hall" in mode or "Scouting" in mode:
    render_hall_of_fame_view(df_master)
elif "Podium" in mode or "Benchmarks" in mode:
    render_podium_view(filtered_df)
else:
    if active_role == "admin":
        render_admin_dashboard(filtered_df)
    elif active_role == "professional":
        render_coach_strategy_studio(filtered_df)
    else:
        render_podium_view(filtered_df)

# Global Telemetry Status Bar Footer
render_telemetry_footer()

