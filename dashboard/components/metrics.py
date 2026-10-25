"""
UI Metrics, KPI Cards & Telemetry HUD component for OLYMPIA.
Implements the Kinetic Olympic Telemetry Lab spatial design system.
"""

import re
import streamlit as st
from typing import List, Dict, Any, Optional
from dashboard.components.icons import get_svg_icon, get_olympic_rings_svg


def render_telemetry_hud(active_role: str, active_module: str, year_range: tuple = (1896, 2026), total_facts: int = 20582):
    """
    Renders the Floating Glass Command Header (Top Telemetry HUD Bar).
    Sticky, translucent, with live dataset ticker and quick role-switch chips.
    """
    rings_svg = get_olympic_rings_svg(width=44, height=20)
    role_normalized = str(active_role).upper()
    role_color = "#5DD62C" if "PROF" in role_normalized or "COACH" in role_normalized else ("#38BDF8" if "ADMIN" in role_normalized else "#F59E0B")
    
    hud_html = f"""
    <div class="telemetry-hud-bar">
        <div class="hud-left">
            <span class="hud-rings">{rings_svg}</span>
            <div class="hud-breadcrumb">
                <span class="hud-brand">OLYMPIA OS</span>
                <span class="hud-sep">//</span>
                <span class="hud-role" style="color: {role_color};">{role_normalized}</span>
                <span class="hud-sep">//</span>
                <span class="hud-module">{active_module.upper()}</span>
            </div>
        </div>
        <div class="hud-center">
            <div class="hud-ticker-pill">
                <span class="ticker-dot">●</span>
                <span class="ticker-text">⚡ <strong>{total_facts:,}</strong> FACTS LOADED</span>
                <span class="ticker-divider">•</span>
                <span class="ticker-text">🏛️ STAR SCHEMA: <strong>100% HEALTHY</strong></span>
                <span class="ticker-divider">•</span>
                <span class="ticker-text">🔥 TOP NATION: <strong>USA</strong></span>
            </div>
        </div>
        <div class="hud-right">
            <div class="hud-scrubber-pill">
                <span class="scrubber-label">ERA:</span>
                <span class="scrubber-val">{year_range[0]} — {year_range[1]}</span>
            </div>
            <div class="hud-role-switcher">
                <a href="?role=fan" target="_self" class="role-chip {'active-chip' if 'ENTH' in role_normalized or 'FAN' in role_normalized else ''}">FAN</a>
                <a href="?role=coach" target="_self" class="role-chip {'active-chip' if 'PROF' in role_normalized or 'COACH' in role_normalized else ''}">COACH</a>
                <a href="?role=admin" target="_self" class="role-chip {'active-chip' if 'ADMIN' in role_normalized else ''}">ADMIN</a>
            </div>
        </div>
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', hud_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_forbes_masthead(tag: str, title: str, subtitle: str, badge_text: str = "", badge_status: str = "Active"):
    """Renders a Forbes-inspired minimalist serif masthead with status badge without any Markdown indentation issues."""
    badge_html = f"""
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: var(--surface-glass-2, #141414); border: 1px solid var(--border-hairline, #262626); padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.78rem; color: #94A3B8; margin-top: 0.5rem;">
        <span style="color: #5DD62C; font-weight: 700;">{badge_status}</span> {badge_text}
    </div>
    """ if badge_text else ""
    
    masthead_html = f"""
    <div class="forbes-masthead" style="text-align: center; padding: 2rem 1.1rem 1.6rem 1.1rem; border-bottom: 1px solid rgba(255,255,255,0.08); margin-bottom: 1.5rem; background: var(--surface-glass-1, #0A0A0A); border-radius: 14px; box-shadow: 0 10px 30px rgba(0,0,0,0.6);">
        <div style="font-size: 0.82rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-bottom: 0.35rem; font-family: 'JetBrains Mono', monospace;">
            {tag}
        </div>
        <h1 class="forbes-masthead-title" style="font-family: 'Space Grotesk', 'Playfair Display', Georgia, serif !important; font-size: clamp(1.75rem, 5vw, 3rem); font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.15; letter-spacing: -0.02em;">
            {title}
        </h1>
        <div class="forbes-masthead-subtitle" style="color: #94A3B8; font-size: clamp(0.88rem, 2.5vw, 1.05rem); max-width: 780px; margin: 0.65rem auto 1.1rem auto; line-height: 1.5; font-family: 'Inter', sans-serif;">
            {subtitle}
        </div>
        {badge_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', masthead_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_kpi_card(
    title: str,
    value: Any,
    subtitle: Optional[str] = None,
    icon: Optional[str] = None,
    delta: Optional[str] = None,
    delta_positive: bool = True
):
    """
    Renders a spatial Bento KPI card with background watermark SVG,
    tabular numbers in JetBrains Mono, dual-layer ambient shadows, and bottom progress glow.
    """
    icon_svg = get_svg_icon(icon, size=20, color="#5DD62C") if icon and not icon.startswith("<") else (icon or "")
    watermark_svg = get_svg_icon(icon, size=46, color="rgba(93, 214, 44, 0.08)") if icon and not icon.startswith("<") else ""
    
    delta_html = ""
    if delta:
        delta_color = "#5DD62C" if delta_positive else "#EF4444"
        delta_html = f"""
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: {delta_color}; background: rgba(93, 214, 44, 0.12); padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700; border: 1px solid rgba(93, 214, 44, 0.2);">
            {delta}
        </span>
        """

    sub_html = f"<div style='font-size: 0.78rem; color: #94A3B8; margin-top: 0.4rem; font-weight: 500; font-family: Inter, sans-serif;'>{subtitle}</div>" if subtitle else ""

    card_html = f"""
    <div class="bento-kpi-card">
        <div class="bento-watermark">{watermark_svg}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 2;">
            <div style="font-size: 0.72rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700; font-family: 'Inter', sans-serif;">
                {title}
            </div>
            {delta_html}
        </div>
        <div class="bento-kpi-value">
            <span style="display: inline-flex; align-items: center; margin-right: 0.5rem;">{icon_svg}</span>{value}
        </div>
        <div style="position: relative; z-index: 2;">
            {sub_html}
        </div>
        <div class="bento-bottom-glow"></div>
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', card_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_kpi_row(kpis: List[Dict[str, Any]]):
    """Renders a responsive horizontal row of Bento KPI cards."""
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            render_kpi_card(
                title=kpi.get("title", ""),
                value=kpi.get("value", 0),
                subtitle=kpi.get("subtitle"),
                icon=kpi.get("icon"),
                delta=kpi.get("delta"),
                delta_positive=kpi.get("delta_positive", True)
            )


def render_podium_showcase(first: dict, second: dict, third: dict):
    """
    Renders an Interactive 3D Visual Olympic Podium in HTML/CSS
    #1 Center (tallest, Gold glow), #2 Left (Silver glow), #3 Right (Bronze glow).
    """
    gold_icon = get_svg_icon("gold_medal", size=24)
    silver_icon = get_svg_icon("silver_medal", size=24)
    bronze_icon = get_svg_icon("bronze_medal", size=24)

    podium_html = f"""
    <div class="spatial-podium-root">
        <!-- 2ND PLACE (SILVER - LEFT) -->
        <div class="podium-pillar silver-pillar">
            <div class="podium-badge-wrap silver-badge">{silver_icon}</div>
            <div class="podium-rank-tag">#2 RANK</div>
            <div class="podium-nation-name">{second.get('country', 'Silver Nation')}</div>
            <div class="podium-score-wrap">
                <span class="podium-pts">{second.get('points', 0):,}</span>
                <span class="podium-unit">PTS</span>
            </div>
            <div class="podium-pills-row">
                <span class="pill-g">🥇 {second.get('gold', 0)}</span>
                <span class="pill-s">🥈 {second.get('silver', 0)}</span>
                <span class="pill-b">🥉 {second.get('bronze', 0)}</span>
            </div>
            <div class="pillar-block pillar-silver-block">2</div>
        </div>

        <!-- 1ST PLACE (GOLD - CENTER / TALLEST) -->
        <div class="podium-pillar gold-pillar">
            <div class="podium-badge-wrap gold-badge">{gold_icon}</div>
            <div class="podium-rank-tag gold-rank">🏆 1ST CHAMPION</div>
            <div class="podium-nation-name gold-nation">{first.get('country', 'Gold Champion')}</div>
            <div class="podium-score-wrap gold-score">
                <span class="podium-pts">{first.get('points', 0):,}</span>
                <span class="podium-unit">PTS</span>
            </div>
            <div class="podium-pills-row">
                <span class="pill-g">🥇 {first.get('gold', 0)}</span>
                <span class="pill-s">🥈 {first.get('silver', 0)}</span>
                <span class="pill-b">🥉 {first.get('bronze', 0)}</span>
            </div>
            <div class="pillar-block pillar-gold-block">1</div>
        </div>

        <!-- 3RD PLACE (BRONZE - RIGHT) -->
        <div class="podium-pillar bronze-pillar">
            <div class="podium-badge-wrap bronze-badge">{bronze_icon}</div>
            <div class="podium-rank-tag">#3 RANK</div>
            <div class="podium-nation-name">{third.get('country', 'Bronze Nation')}</div>
            <div class="podium-score-wrap">
                <span class="podium-pts">{third.get('points', 0):,}</span>
                <span class="podium-unit">PTS</span>
            </div>
            <div class="podium-pills-row">
                <span class="pill-g">🥇 {third.get('gold', 0)}</span>
                <span class="pill-s">🥈 {third.get('silver', 0)}</span>
                <span class="pill-b">🥉 {third.get('bronze', 0)}</span>
            </div>
            <div class="pillar-block pillar-bronze-block">3</div>
        </div>
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', podium_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_empty_telemetry_card(on_reset_key: Optional[str] = None):
    """Renders a custom SVG 'Zero-Telemetry' fallback card when user filters yield 0 rows."""
    search_icon = get_svg_icon("search", size=36, color="#5DD62C")
    empty_html = f"""
    <div class="zero-telemetry-card">
        <div style="margin-bottom: 0.8rem;">{search_icon}</div>
        <div style="font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 800; color: #F8FAFC;">
            No Active Telemetry Facts Found
        </div>
        <div style="color: #94A3B8; font-size: 0.92rem; max-width: 480px; margin: 0.4rem auto 1.2rem auto; line-height: 1.5;">
            The currently selected filter combination (Season, Era Range, Country, Sport) returned 0 records from the Star Schema.
        </div>
    </div>
    """
    st.markdown(re.sub(r'\s+', ' ', empty_html).strip(), unsafe_allow_html=True)
    if st.button("🔄 Reset Filter Parameters to Global Default", key=on_reset_key or "btn_reset_zero_telemetry", use_container_width=True):
        st.rerun()


def render_telemetry_footer():
    """Renders the global 3-column telemetry status footer bar."""
    footer_html = """
    <div class="telemetry-status-footer">
        <div class="footer-left">
            <span style="color: #5DD62C; font-weight: 800;">●</span> OLYMPIA v2.6 // OFFLINE-FIRST STAR SCHEMA ENGINE
        </div>
        <div class="footer-center">
            <span class="footer-pill">SQLite WAL 60FPS</span>
            <span class="footer-pill">ZERO DATA LEAKAGE</span>
            <span class="footer-pill">ANTIGRAVITY MOTION</span>
        </div>
        <div class="footer-right">
            1896 – 2026 ARCHIVE • 20,582 CLEAN FACT MEDALS
        </div>
    </div>
    """
    st.markdown(re.sub(r'\s+', ' ', footer_html).strip(), unsafe_allow_html=True)


def render_viva_note(title: str, description: str, theory: Optional[str] = None):
    """Renders a conceptual explanation callout with custom SVG icon."""
    info_icon = get_svg_icon("search", size=18, color="#38BDF8")
    theory_html = f"<div style='margin-top: 0.5rem; font-size: 0.82rem; color: #94A3B8;'><strong>Analytical Insight:</strong> {theory}</div>" if theory else ""
    note_html = f"""
    <div style="
        background: rgba(18, 22, 26, 0.7);
        border-left: 3px solid #38BDF8;
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-left-width: 3px;
        border-radius: 0 10px 10px 0;
        padding: 1rem 1.3rem;
        margin: 1.2rem 0;
        font-size: 0.9rem;
        color: #E2E8F0;
        backdrop-filter: blur(12px);
    ">
        <div style="font-weight: 700; color: #38BDF8; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em; font-family: 'Space Grotesk', sans-serif;">
            {info_icon} System Method: {title}
        </div>
        <div style="line-height: 1.5; font-family: 'Inter', sans-serif;">{description}</div>
        {theory_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', note_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)



