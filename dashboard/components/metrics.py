"""
UI Metrics and KPI Cards component for OLYMPIA.
Renders dark analytics KPI cards with Forbes-inspired editorial accents and custom SVG icons.
"""

import re
import streamlit as st
from typing import List, Dict, Any, Optional
from dashboard.components.icons import get_svg_icon


def render_forbes_masthead(tag: str, title: str, subtitle: str, badge_text: str = "", badge_status: str = "Active"):
    """Renders a Forbes-inspired minimalist serif masthead with status badge without any Markdown indentation issues."""
    badge_html = f"""
    <div style="display: inline-flex; align-items: center; gap: 0.5rem; background: #141414; border: 1px solid #262626; padding: 0.35rem 1rem; border-radius: 20px; font-size: 0.78rem; color: #94A3B8;">
        <span style="color: #5DD62C; font-weight: 700;">{badge_status}</span> {badge_text}
    </div>
    """ if badge_text else ""
    
    masthead_html = f"""
    <div style="text-align: center; padding: 2.4rem 1.2rem 1.8rem 1.2rem; border-bottom: 1px solid #222222; margin-bottom: 1.5rem; background: #0A0A0A; border-radius: 12px; box-shadow: 0 4px 24px rgba(0,0,0,0.6);">
        <div style="font-size: 0.85rem; color: #94A3B8; text-transform: uppercase; letter-spacing: 0.16em; font-weight: 700; margin-bottom: 0.35rem;">
            {tag}
        </div>
        <h1 style="font-family: 'Playfair Display', Georgia, serif !important; font-size: 3rem; font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.15; letter-spacing: -0.01em;">
            {title}
        </h1>
        <div style="color: #94A3B8; font-size: 1.05rem; max-width: 780px; margin: 0.65rem auto 1.1rem auto; line-height: 1.5; font-family: 'Segoe UI', sans-serif;">
            {subtitle}
        </div>
        {badge_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', masthead_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)



def render_kpi_card(title: str, value: Any, subtitle: Optional[str] = None, icon: Optional[str] = None):
    """Renders a single styled KPI card with Forbes-inspired editorial minimalism."""
    icon_svg = get_svg_icon(icon, size=20, color="#5DD62C") if icon and not icon.startswith("<") else (icon or "")
    icon_html = f"<span style='display: inline-flex; align-items: center; margin-right: 0.6rem;'>{icon_svg}</span>" if icon_svg else ""
    sub_html = f"<div style='font-size: 0.78rem; color: #94A3B8; margin-top: 0.35rem; font-weight: 500;'>{subtitle}</div>" if subtitle else ""

    card_html = f"""
    <div style="
        background: #141414;
        border: 1px solid #262626;
        border-radius: 8px;
        padding: 1.25rem 1.4rem;
        margin-bottom: 0.75rem;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.4);
        transition: border-color 0.2s ease;
    ">
        <div style="font-size: 0.75rem; color: #737373; text-transform: uppercase; letter-spacing: 0.08em; font-weight: 700;">
            {title}
        </div>
        <div style="font-size: 1.85rem; font-weight: 800; color: #F8FAFC; margin-top: 0.4rem; display: flex; align-items: center; letter-spacing: -0.02em;">
            {icon_html}{value}
        </div>
        {sub_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', card_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def render_kpi_row(kpis: List[Dict[str, Any]]):
    """Renders a responsive horizontal row of KPI cards."""
    cols = st.columns(len(kpis))
    for col, kpi in zip(cols, kpis):
        with col:
            render_kpi_card(
                title=kpi.get("title", ""),
                value=kpi.get("value", 0),
                subtitle=kpi.get("subtitle"),
                icon=kpi.get("icon")
            )


def render_viva_note(title: str, description: str, theory: Optional[str] = None):
    """Renders a conceptual explanation callout with custom SVG icon."""
    info_icon = get_svg_icon("search", size=18, color="#38BDF8")
    theory_html = f"<div style='margin-top: 0.5rem; font-size: 0.82rem; color: #94A3B8;'><strong>Analytical Insight:</strong> {theory}</div>" if theory else ""
    note_html = f"""
    <div style="
        background: #12161A;
        border-left: 3px solid #38BDF8;
        border-radius: 0 6px 6px 0;
        padding: 1rem 1.3rem;
        margin: 1.2rem 0;
        font-size: 0.9rem;
        color: #E2E8F0;
    ">
        <div style="font-weight: 700; color: #38BDF8; margin-bottom: 0.3rem; display: flex; align-items: center; gap: 0.5rem; text-transform: uppercase; font-size: 0.78rem; letter-spacing: 0.06em;">
            {info_icon} System Method: {title}
        </div>
        <div style="line-height: 1.5;">{description}</div>
        {theory_html}
    </div>
    """
    cleaned = re.sub(r'\s+', ' ', note_html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


