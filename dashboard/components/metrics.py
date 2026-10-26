"""
UI Metrics, KPI Cards & Telemetry HUD component for OLYMPIA.
Implements the Legendary Olympic Intelligence Archive architectural marble & gold design system.
"""

import re
from typing import Any, Optional, List, Dict
import streamlit as st
from dashboard.components.icons import get_svg_icon, get_olympic_rings_svg, get_olympic_sculpted_rings_svg
from dashboard.components.theme import get_olympia_logo, COLOR_GOLD, COLOR_CHARCOAL, COLOR_RED
from dashboard.components.flags import get_country_flag_html



def render_telemetry_hud(active_role: str, active_module: str, year_range: tuple = (1896, 2026), total_facts: int = 20582):
    """
    Renders the Floating Architectural Command Header (Top Telemetry HUD Bar).
    Sticky, light marble backdrop with subtle blur, dataset fact ticker, and role switcher quick-chips.
    """
    role_normalized = str(active_role).upper()
    role_display = "COACH" if ("PROF" in role_normalized or "COACH" in role_normalized) else ("ADMIN" if "ADMIN" in role_normalized else "FAN")
    role_param = "coach" if role_display == "COACH" else ("admin" if role_display == "ADMIN" else "fan")
    logo_svg = get_olympia_logo(variant="horizontal", width=165, height=32)
    mod_lower = str(active_module).lower()

    hud_html = f"""
    <div class="telemetry-hud-bar">
        <div class="hud-left">
            <a href="?role={role_param}&nav=home" target="_self" style="text-decoration: none; display: flex; align-items: center;">{logo_svg}</a>
        </div>
        <div class="hud-nav-links" style="display: flex; align-items: center; gap: 0.35rem; flex-wrap: wrap;">
            <a href="?role={role_param}&nav=home" target="_self" class="hud-nav-item {'active-nav' if 'home' in mod_lower or 'overview' in mod_lower else ''}">🏠 Home</a>
            <a href="?role={role_param}&nav=medals" target="_self" class="hud-nav-item {'active-nav' if 'medal' in mod_lower or 'podium' in mod_lower else ''}">🏆 Medal Analysis</a>
            <a href="?role={role_param}&nav=country" target="_self" class="hud-nav-item {'active-nav' if 'countr' in mod_lower else ''}">🌐 Countries</a>
            <a href="?role={role_param}&nav=sports" target="_self" class="hud-nav-item {'active-nav' if 'sport' in mod_lower else ''}">🏃 Sports</a>
            <a href="?role={role_param}&nav=athletes" target="_self" class="hud-nav-item {'active-nav' if 'athlet' in mod_lower else ''}">👤 Athletes</a>
            <a href="?role={role_param}&nav=predictions" target="_self" class="hud-nav-item {'active-nav' if 'predict' in mod_lower or 'regr' in mod_lower else ''}">📈 Predictions</a>
            <a href="?role={role_param}&nav=coach" target="_self" class="hud-nav-item {'active-nav' if 'coach' in mod_lower or 'strat' in mod_lower else ''}">⚡ Coach Strategy</a>
            <a href="?role={role_param}&nav=olap" target="_self" class="hud-nav-item {'active-nav' if 'olap' in mod_lower or 'cube' in mod_lower else ''}">🧊 OLAP Cubes</a>
            <a href="?role={role_param}&nav=mining" target="_self" class="hud-nav-item {'active-nav' if 'mining' in mod_lower or 'cluster' in mod_lower else ''}">⛏️ Data Mining</a>
            <a href="?role={role_param}&nav=warehouse" target="_self" class="hud-nav-item {'active-nav' if 'wareh' in mod_lower or 'admin' in mod_lower else ''}">🗄️ Warehouse</a>
        </div>
        <div class="hud-right" style="display: flex; align-items: center; gap: 0.75rem;">
            <div class="hud-scrubber-pill">
                <span style="color: #8B857C; font-weight: 600;">ERA:</span>
                <span style="font-weight: 700; color: #2E2A25;">{year_range[0]} — {year_range[1]}</span>
            </div>
            <div class="hud-role-switcher" style="display: flex; gap: 4px;">
                <a href="?role=fan" target="_self" class="role-chip {'active-chip' if role_display == 'FAN' else ''}">FAN</a>
                <a href="?role=coach" target="_self" class="role-chip {'active-chip' if role_display == 'COACH' else ''}">COACH</a>
                <a href="?role=admin" target="_self" class="role-chip {'active-chip' if role_display == 'ADMIN' else ''}">ADMIN</a>
            </div>
        </div>
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', hud_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)



def render_hero_split_banner():
    """
    Renders the iconic Split Hero Section exactly matching the reference design:
    - Left Panel: Deep Onyx architectural card with torch runner and gold typography:
      'Turn Olympic Data into Real Impact'
    - Right Panel: 'OLYMPIC LEGACY IN NUMBERS 1896-2026' with sculpted Olympic rings
      and 5-column metric strip (20,582 Medal Records, 131 Years, 206 Countries, 47 Sports, 1,017 Events).
    """
    from dashboard.components.kinetic_engine import get_3d_astrolabe_rings_html
    astrolabe_rings = get_3d_astrolabe_rings_html(width=280, height=120)

    hero_html = f"""
    <div style="display: grid; grid-template-columns: 1.55fr 1fr; gap: 1.25rem; margin-bottom: 1.5rem;">
        <!-- LEFT PANEL: DEEP ONYX HERO -->
        <div class="hero-onyx-card" style="display: flex; flex-direction: column; justify-content: space-between; min-height: 270px; background: linear-gradient(135deg, #1C1B19 0%, #2A2520 100%);">
            <div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.76rem; color: #D4AF37; letter-spacing: 0.22em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.6rem;">
                    OLYMPIC INTELLIGENCE LAB
                </div>
                <h1 style="font-family: 'Cinzel', 'Playfair Display', Georgia, serif; font-size: clamp(2rem, 3.8vw, 3rem); font-weight: 800; color: #FFFFFF; line-height: 1.1; margin: 0; letter-spacing: -0.02em;">
                    Turn Olympic Data<br>into <span style="font-family: 'Cormorant Garamond', Georgia, serif; font-style: italic; color: #D4AF37; font-weight: 600;">Real Impact</span>
                </h1>
                <p style="color: #C5BEB3; font-size: 0.95rem; max-width: 500px; margin: 0.8rem 0 1.2rem 0; line-height: 1.5; font-family: 'Inter', sans-serif;">
                    Explore 131 years of human greatness. Discover patterns across 20,582 medal facts. Predict the future of sport.
                </p>
            </div>
            <div style="display: flex; align-items: center; justify-content: space-between; border-top: 1px solid rgba(255,255,255,0.1); padding-top: 1rem;">
                <div style="display: flex; align-items: center; gap: 0.75rem;">
                    <a href="?role=fan&nav=medals" target="_self" class="magnetic-btn" style="background: linear-gradient(135deg, #F3E7C5 0%, #D4AF37 100%); color: #1F1F1F; padding: 0.55rem 1.25rem; border-radius: 10px; font-weight: 700; font-size: 0.86rem; text-decoration: none; display: inline-flex; align-items: center; gap: 0.4rem; box-shadow: 0 4px 14px rgba(212,175,55,0.3);">
                        Explore Analytics →
                    </a>
                    <span style="color: #94A3B8; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace;">
                        Offline Star Schema Active
                    </span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #8B857C; letter-spacing: 0.15em; text-transform: uppercase;">
                    ATHLETES • NATIONS • SPORTS • HISTORY
                </div>

            </div>
        </div>

        <!-- RIGHT PANEL: OLYMPIC LEGACY IN NUMBERS -->
        <div class="hero-legacy-card">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="font-family: 'Cinzel', Georgia, serif; font-weight: 800; font-size: 1rem; color: #2E2A25; letter-spacing: 0.06em;">
                        OLYMPIC LEGACY IN NUMBERS
                    </span>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #8B857C; font-weight: 600;">
                        1896 — 2026
                    </span>
                </div>
                <div style="padding: 0.2rem 0;">
                    {astrolabe_rings}
                </div>
            </div>
            
            <!-- 5-COLUMN METRIC STRIP WITH MECHANICAL CIPHER SCRAMBLE -->
            <div style="display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.5rem; border-top: 1px solid #E5DED2; padding-top: 0.85rem; text-align: center;">
                <div>
                    <div class="kinetic-odometer" data-odometer="true" data-target-value="20,582" style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #2E2A25;">20,582</div>
                    <div style="font-size: 0.68rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Medal Records</div>
                </div>
                <div>
                    <div class="kinetic-odometer" data-odometer="true" data-target-value="131" style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #2E2A25;">131</div>
                    <div style="font-size: 0.68rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Years</div>
                </div>
                <div>
                    <div class="kinetic-odometer" data-odometer="true" data-target-value="206" style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #2E2A25;">206</div>
                    <div style="font-size: 0.68rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Countries</div>
                </div>
                <div>
                    <div class="kinetic-odometer" data-odometer="true" data-target-value="47" style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #2E2A25;">47</div>
                    <div style="font-size: 0.68rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Sports</div>
                </div>
                <div>
                    <div class="kinetic-odometer" data-odometer="true" data-target-value="1,017" style="font-family: 'JetBrains Mono', monospace; font-size: 1.15rem; font-weight: 800; color: #2E2A25;">1,017</div>
                    <div style="font-size: 0.68rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.05em; font-weight: 600;">Events</div>
                </div>
            </div>
        </div>
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', hero_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_forbes_masthead(tag: str, title: str, subtitle: str, badge_text: str = "", badge_status: str = "Active"):
    """Renders a monumental Roman editorial masthead with warm architectural styling."""
    badge_html = f"""
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #FAF0D8; border: 1px solid rgba(212, 175, 55, 0.4); padding: 0.3rem 0.95rem; border-radius: 20px; font-size: 0.78rem; color: #5A4005; margin-top: 0.6rem;">
        <span style="color: #AA820A; font-weight: 800;">● {badge_status}</span> {badge_text}
    </div>
    """ if badge_text else ""

    masthead_html = f"""
    <div class="forbes-masthead" style="text-align: center; padding: 2rem 1.4rem 1.6rem 1.4rem; border: 1px solid var(--olympia-border); margin-bottom: 1.5rem; background: #FFFFFF; border-radius: 16px; box-shadow: var(--shadow-subtle);">
        <div style="font-size: 0.78rem; color: #D4AF37; text-transform: uppercase; letter-spacing: 0.22em; font-weight: 700; margin-bottom: 0.4rem; font-family: 'JetBrains Mono', monospace;">
            {tag}
        </div>
        <h1 class="forbes-masthead-title" style="font-family: 'Cinzel', 'Playfair Display', Georgia, serif !important; font-size: clamp(1.8rem, 4.5vw, 2.8rem); font-weight: 800; color: #2E2A25; margin: 0; line-height: 1.15; letter-spacing: -0.01em;">
            {title}
        </h1>
        <div class="forbes-masthead-subtitle" style="color: #8B857C; font-size: clamp(0.9rem, 2vw, 1.05rem); max-width: 760px; margin: 0.65rem auto 0.8rem auto; line-height: 1.5; font-family: 'Inter', sans-serif;">
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
    Renders a spatial architectural Bento KPI card with background watermark SVG,
    tabular numbers in JetBrains Mono, dual-layer ambient shadows, and bottom gold accent line.
    """
    icon_svg = get_svg_icon(icon, size=18, color=COLOR_GOLD) if icon and not icon.startswith("<") else (icon or "")
    watermark_svg = get_svg_icon(icon, size=46, color="rgba(212, 175, 55, 0.08)") if icon and not icon.startswith("<") else ""

    delta_html = ""
    if delta:
        delta_color = COLOR_GOLD if delta_positive else COLOR_RED
        delta_bg = "rgba(212, 175, 55, 0.12)" if delta_positive else "rgba(196, 30, 58, 0.1)"
        delta_html = f"""
        <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: {delta_color}; background: {delta_bg}; padding: 0.15rem 0.5rem; border-radius: 9999px; font-weight: 700; border: 1px solid rgba(212, 175, 55, 0.25);">
            {delta}
        </span>
        """

    sub_html = f"<div style='font-size: 0.78rem; color: #8B857C; margin-top: 0.35rem; font-weight: 500; font-family: Inter, sans-serif;'>{subtitle}</div>" if subtitle else ""

    card_html = f"""
    <div class="bento-marble-card" style="padding: 1.25rem 1.35rem; position: relative;">
        <div style="position: absolute; right: 12px; bottom: 8px; opacity: 0.8; pointer-events: none;">{watermark_svg}</div>
        <div style="display: flex; justify-content: space-between; align-items: center; position: relative; z-index: 2;">
            <div style="font-size: 0.72rem; color: #8B857C; text-transform: uppercase; letter-spacing: 0.1em; font-weight: 700; font-family: 'Inter', sans-serif;">
                {title}
            </div>
            {delta_html}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: clamp(1.6rem, 3.2vw, 2.1rem); font-weight: 800; color: #2E2A25; margin-top: 0.4rem; position: relative; z-index: 2; display: flex; align-items: center;">
            <span style="margin-right: 0.45rem; display: inline-flex; align-items: center;">{icon_svg}</span>{value}
        </div>
        <div style="position: relative; z-index: 2;">
            {sub_html}
        </div>
        <div style="position: absolute; bottom: 0; left: 0; right: 0; height: 3px; background: linear-gradient(90deg, #D4AF37 0%, transparent 80%);"></div>
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
    Renders an Interactive Sculptural Olympic Podium in classical marble and gold.
    #1 Center (tallest, Gold glow), #2 Left (Silver), #3 Right (Bronze).
    """
    gold_icon = get_svg_icon("gold_medal", size=24)
    silver_icon = get_svg_icon("silver_medal", size=24)
    bronze_icon = get_svg_icon("bronze_medal", size=24)

    podium_html = f"""
    <div style="display: grid; grid-template-columns: 1fr 1.15fr 1fr; gap: 1rem; align-items: end; margin: 1.5rem 0 2rem 0; padding: 1.5rem; background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 18px; box-shadow: var(--shadow-subtle);">
        <!-- 2ND PLACE (SILVER - LEFT) -->
        <div style="background: #F8F5EE; border: 1px solid #E5DED2; border-radius: 14px 14px 4px 4px; padding: 1.2rem; text-align: center; height: 210px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="margin-bottom: 0.2rem;">{silver_icon}</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #8B857C; font-weight: 700;">#2 RANK</div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.15rem; font-weight: 800; color: #2E2A25; margin: 0.2rem 0; display: flex; align-items: center; justify-content: center; gap: 0.35rem;">
                    {get_country_flag_html(second.get('country', ''), size=18)}
                    <span>{second.get('country', 'Silver Nation')}</span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: #5A544A;">{second.get('points', 0):,} <span style="font-size: 0.75rem; color: #8B857C;">PTS</span></div>
            </div>
            <div style="background: #EAE3D5; border-radius: 6px; padding: 0.4rem; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; color: #2E2A25; font-weight: 600;">
                G: {second.get('gold', 0)} • S: {second.get('silver', 0)} • B: {second.get('bronze', 0)}
            </div>
        </div>

        <!-- 1ST PLACE (GOLD - CENTER / TALLEST) -->
        <div style="background: linear-gradient(180deg, #FAF0D8 0%, #FFFFFF 100%); border: 2px solid #D4AF37; border-radius: 16px 16px 4px 4px; padding: 1.4rem; text-align: center; height: 260px; display: flex; flex-direction: column; justify-content: space-between; box-shadow: 0 8px 24px rgba(212,175,55,0.22);">
            <div>
                <div style="margin-bottom: 0.2rem;">{gold_icon}</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #AA820A; font-weight: 800; letter-spacing: 0.08em;">🏆 1ST CHAMPION</div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.45rem; font-weight: 900; color: #2E2A25; margin: 0.2rem 0; display: flex; align-items: center; justify-content: center; gap: 0.4rem;">
                    {get_country_flag_html(first.get('country', ''), size=22)}
                    <span>{first.get('country', 'Gold Champion')}</span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.6rem; font-weight: 900; color: #D4AF37;">{first.get('points', 0):,} <span style="font-size: 0.85rem; color: #AA820A;">PTS</span></div>
            </div>
            <div style="background: #F3E7C5; border: 1px solid rgba(212,175,55,0.4); border-radius: 8px; padding: 0.5rem; font-size: 0.82rem; font-family: 'JetBrains Mono', monospace; color: #5A4005; font-weight: 700;">
                G: {first.get('gold', 0)} • S: {first.get('silver', 0)} • B: {first.get('bronze', 0)}
            </div>
        </div>

        <!-- 3RD PLACE (BRONZE - RIGHT) -->
        <div style="background: #F8F5EE; border: 1px solid #E5DED2; border-radius: 14px 14px 4px 4px; padding: 1.2rem; text-align: center; height: 180px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="margin-bottom: 0.2rem;">{bronze_icon}</div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #8B857C; font-weight: 700;">#3 RANK</div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.15rem; font-weight: 800; color: #2E2A25; margin: 0.2rem 0; display: flex; align-items: center; justify-content: center; gap: 0.35rem;">
                    {get_country_flag_html(third.get('country', ''), size=18)}
                    <span>{third.get('country', 'Bronze Nation')}</span>
                </div>
                <div style="font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; font-weight: 800; color: #B45309;">{third.get('points', 0):,} <span style="font-size: 0.75rem; color: #8B857C;">PTS</span></div>
            </div>
            <div style="background: #EAE3D5; border-radius: 6px; padding: 0.4rem; font-size: 0.78rem; font-family: 'JetBrains Mono', monospace; color: #2E2A25; font-weight: 600;">
                G: {third.get('gold', 0)} • S: {third.get('silver', 0)} • B: {third.get('bronze', 0)}
            </div>
        </div>
    </div>

    """
    cleaned = re.sub(r'\s+', ' ', podium_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_empty_telemetry_card(on_reset_key: Optional[str] = None):
    """Renders a custom 'Zero-Telemetry' fallback card when user filters yield 0 rows."""
    search_icon = get_svg_icon("search", size=36, color=COLOR_GOLD)
    empty_html = f"""
    <div style="text-align: center; padding: 3rem 1.5rem; background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 16px; margin: 1.5rem 0; box-shadow: var(--shadow-subtle);">
        <div style="margin-bottom: 0.8rem;">{search_icon}</div>
        <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.35rem; font-weight: 800; color: #2E2A25;">
            No Active Olympic Records Found
        </div>
        <div style="color: #8B857C; font-size: 0.92rem; max-width: 480px; margin: 0.5rem auto 1.4rem auto; line-height: 1.5; font-family: 'Inter', sans-serif;">
            The currently selected filter combination returned 0 records from the Olympic archive. Reset filters to explore all 20,582 medal records.
        </div>
    </div>
    """
    st.markdown(re.sub(r'\s+', ' ', empty_html).strip(), unsafe_allow_html=True)
    if st.button("🔄 Reset Filter Parameters to Global Default", key=on_reset_key or "btn_reset_zero_telemetry", use_container_width=True):
        st.rerun()


def render_telemetry_footer():
    """Renders the global architectural archive footer."""
    footer_html = """
    <div class="telemetry-footer-bar">
        <div>
            <span style="color: #D4AF37; font-weight: 800;">●</span> <strong>OLYMPIA</strong> // THE LEGACY OF HUMAN GREATNESS, DECODED THROUGH DATA
        </div>
        <div style="display: flex; gap: 0.6rem;">
            <span style="background: #FFFFFF; border: 1px solid #E5DED2; padding: 0.2rem 0.6rem; border-radius: 9999px;">OFFLINE-FIRST STAR SCHEMA</span>
            <span style="background: #FFFFFF; border: 1px solid #E5DED2; padding: 0.2rem 0.6rem; border-radius: 9999px;">ZERO DATA LEAKAGE</span>
        </div>
        <div>
            1896 – 2026 ARCHIVE • 20,582 VERIFIED MEDAL RECORDS
        </div>
    </div>
    """
    st.markdown(re.sub(r'\s+', ' ', footer_html).strip(), unsafe_allow_html=True)


def render_viva_note(title: str, description: str, theory: Optional[str] = None):
    """Renders an architectural conceptual explanation callout."""
    info_icon = get_svg_icon("search", size=18, color=COLOR_GOLD)
    theory_html = f"<div style='margin-top: 0.4rem; font-size: 0.82rem; color: #5A544A;'><strong>Analytical Insight:</strong> {theory}</div>" if theory else ""
    note_html = f"""
    <div style="
        background: #FFFFFF;
        border-left: 4px solid #D4AF37;
        border: 1px solid #E5DED2;
        border-left-width: 4px;
        border-radius: 0 12px 12px 0;
        padding: 1.1rem 1.4rem;
        margin: 1.2rem 0;
        font-size: 0.9rem;
        color: #2E2A25;
        box-shadow: var(--shadow-subtle);
    ">
        <div style="font-weight: 700; color: #AA820A; margin-bottom: 0.35rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.08em; font-family: 'JetBrains Mono', monospace;">
            {info_icon} System Method: {title}
        </div>
        <div style="line-height: 1.5; font-family: 'Inter', sans-serif;">{description}</div>
        {theory_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', note_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)
