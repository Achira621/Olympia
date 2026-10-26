"""
Authentication and Role-Based Access Control for OLYMPIA.
Implements the Legendary Olympic Intelligence Archive architectural marble & gold design system.
"""

import os
import re
import base64
import textwrap
import streamlit as st
from typing import Optional, Tuple
from dashboard.components.icons import get_svg_icon, get_olympic_rings_svg
from dashboard.components.theme import get_olympia_logo, COLOR_GOLD, COLOR_CHARCOAL, COLOR_RED, COLOR_SANDSTONE

# Role Constants (Normalized: admin, enthusiast, professional)
ROLE_ADMIN = "admin"
ROLE_ENTHUSIAST = "enthusiast"
ROLE_PROFESSIONAL = "professional"
ROLE_ACADEMY = ROLE_PROFESSIONAL  # Alias for backwards compatibility

ROLE_DISPLAY = {
    ROLE_ADMIN: {
        "title": "Data Architect",
        "icon": get_svg_icon("database", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "Full access to Star Schema Warehouse, ETL pipeline telemetry, and administrative controls."
    },
    ROLE_ENTHUSIAST: {
        "title": "Sport Enthusiast",
        "icon": get_svg_icon("trophy", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "The Olympic Podium, global dominance maps, nation dynasties, and legend profiles."
    },
    ROLE_PROFESSIONAL: {
        "title": "Performance Coach",
        "icon": get_svg_icon("lightning", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "6D Athlete inclination radar, opponent scouting, pacing analysis, and aerodynamic simulation."
    },
    # Backwards compatibility keys
    "ADMIN": {
        "title": "Data Architect",
        "icon": get_svg_icon("database", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "Full access to Star Schema Warehouse, ETL pipeline telemetry, and administrative controls."
    },
    "SPORT_ENTHUSIAST": {
        "title": "Sport Enthusiast",
        "icon": get_svg_icon("trophy", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "The Olympic Podium, global dominance maps, nation dynasties, and legend profiles."
    },
    "PLAYER_ACADEMY": {
        "title": "Performance Coach",
        "icon": get_svg_icon("lightning", size=16, color=COLOR_GOLD),
        "badge_color": COLOR_GOLD,
        "badge_bg": "rgba(212, 175, 55, 0.15)",
        "description": "6D Athlete inclination radar, opponent scouting, pacing analysis, and aerodynamic simulation."
    }
}

DEMO_ACCOUNTS = {
    "admin": {"password": "olympia2024", "role": ROLE_ADMIN, "name": "System Administrator"},
    "fan": {"password": "olympia", "role": ROLE_ENTHUSIAST, "name": "Olympic Fan"},
    "coach": {"password": "olympia", "role": ROLE_PROFESSIONAL, "name": "Elite Sports Academy"},
    "professional": {"password": "olympia", "role": ROLE_PROFESSIONAL, "name": "Performance Analyst"},
    "enthusiast": {"password": "olympia", "role": ROLE_ENTHUSIAST, "name": "Olympic Enthusiast"}
}


def _safe_html(html: str):
    """Renders HTML safely without markdown code-block indentation interpretation."""
    cleaned = re.sub(r'\n\s*', ' ', html).strip()
    st.markdown(cleaned, unsafe_allow_html=True)


def init_auth():
    """Initializes session state keys for authentication."""
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False
    if "user_role" not in st.session_state:
        st.session_state["user_role"] = None
    if "username" not in st.session_state:
        st.session_state["username"] = None
    if "user_fullname" not in st.session_state:
        st.session_state["user_fullname"] = None
    if "selected_role_intent" not in st.session_state:
        st.session_state["selected_role_intent"] = None


def is_authenticated() -> bool:
    """Checks if the current session has an authenticated user."""
    init_auth()
    role_param = st.query_params.get("role")
    if role_param:
        role_map = {
            "admin": ("admin", ROLE_ADMIN, "System Administrator"),
            "fan": ("fan", ROLE_ENTHUSIAST, "Olympic Fan"),
            "enthusiast": ("enthusiast", ROLE_ENTHUSIAST, "Olympic Enthusiast"),
            "coach": ("coach", ROLE_PROFESSIONAL, "Elite Sports Academy"),
            "professional": ("professional", ROLE_PROFESSIONAL, "Performance Analyst"),
            "academy": ("coach", ROLE_PROFESSIONAL, "Elite Sports Academy"),
        }
        if role_param.lower() in role_map:
            u, r, f = role_map[role_param.lower()]
            if not st.session_state.get("authenticated", False) or st.session_state.get("user_role") != r:
                st.session_state["authenticated"] = True
                st.session_state["logged_in"] = True
                st.session_state["user_role"] = r
                st.session_state["username"] = u
                st.session_state["user_fullname"] = f

    return st.session_state.get("authenticated", False)


def get_current_role() -> Optional[str]:
    """Returns the normalized role of the current user, or None."""
    init_auth()
    return st.session_state.get("user_role")


def get_current_user() -> dict:
    """Returns a dictionary of current user info."""
    init_auth()
    return {
        "username": st.session_state.get("username", "guest"),
        "role": st.session_state.get("user_role", ROLE_ENTHUSIAST),
        "fullname": st.session_state.get("user_fullname", "Guest User")
    }


def login(username: str, role: str, fullname: str):
    """Logs the user into session state and updates query params."""
    st.session_state["authenticated"] = True
    st.session_state["logged_in"] = True
    st.session_state["user_role"] = role
    st.session_state["username"] = username
    st.session_state["user_fullname"] = fullname
    # Set query param for reload stability
    param_val = "admin" if role == ROLE_ADMIN else ("coach" if role == ROLE_PROFESSIONAL else "fan")
    st.query_params["role"] = param_val
    st.rerun()


def logout():
    """Logs the user out and clears session state."""
    st.session_state["authenticated"] = False
    st.session_state["logged_in"] = False
    st.session_state["user_role"] = None
    st.session_state["username"] = None
    st.session_state["user_fullname"] = None
    st.session_state["selected_role_intent"] = None
    if "role" in st.query_params:
        del st.query_params["role"]
    st.rerun()


def render_landing_page():
    """
    Renders the monumental OLYMPIA entrance experience.
    Classical marble and gold hero with the vector flame emblem,
    editorial serif typography, and 3 tactile Persona Accreditation Cards.
    """
    init_auth()

    emblem_svg = get_olympia_logo("mark", width=80, height=80)
    rings_svg = get_olympic_rings_svg(width=58, height=26)

    _safe_html(f"""
    <div style="text-align: center; padding: 2.5rem 1.5rem 2rem 1.5rem; background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 22px; margin-bottom: 2rem; box-shadow: 0 10px 32px rgba(46,42,37,0.06);">
        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 0.8rem;">
            {emblem_svg}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.78rem; color: #D4AF37; letter-spacing: 0.25em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem;">
            ENTER THE OLYMPIC INTELLIGENCE VAULT
        </div>
        <h1 style="font-family: 'Cinzel', 'Playfair Display', Georgia, serif !important; font-size: clamp(2.4rem, 6vw, 3.8rem); font-weight: 800; color: #2E2A25; margin: 0; line-height: 1.05; letter-spacing: -0.01em;">
            OLYMPI<span style="color: #D4AF37;">A</span>
        </h1>
        <div style="font-size: clamp(0.85rem, 2vw, 1.05rem); color: #8B857C; font-weight: 600; letter-spacing: 0.12em; text-transform: uppercase; margin-top: 0.5rem; font-family: 'Inter', sans-serif;">
            The Legacy of Human Greatness, Decoded Through Data
        </div>
        <p style="max-width: 680px; margin: 0.85rem auto 0 auto; color: #5A544A; font-size: clamp(0.9rem, 2vw, 1rem); line-height: 1.6; font-family: 'Inter', sans-serif;">
            Explore 131 years of Olympic history (1896 – 2026) through an offline-first Star Schema warehouse,
            sports science tactical coach telemetry, and multidimensional analytical modeling.
        </p>
        <div style="margin-top: 1rem;">
            {rings_svg}
        </div>
    </div>
    """)

    st.markdown("<div style='text-align: center; color: #8B857C; font-family: Cinzel, serif; font-size: 0.88rem; letter-spacing: 0.16em; text-transform: uppercase; font-weight: 700; margin-bottom: 1.2rem;'>Select Identity to Enter Archive</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    icon_db = get_svg_icon("database", size=24, color=COLOR_GOLD)
    icon_tr = get_svg_icon("trophy", size=24, color=COLOR_GOLD)
    icon_lt = get_svg_icon("lightning", size=24, color=COLOR_GOLD)

    # 1. SPORT ENTHUSIAST ROLE CARD
    with col1:
        _safe_html(f"""
        <div class="bento-marble-card" style="height: 330px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); display: flex; align-items: center; justify-content: center;">
                        {icon_tr}
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #AA820A; font-weight: 800; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.3); padding: 0.2rem 0.6rem; border-radius: 9999px;">
                        TIER 1 ARCHIVE
                    </span>
                </div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.25rem; font-weight: 800; color: #2E2A25;">Sport Enthusiast</div>
                <div style="color: #8B857C; font-size: 0.82rem; font-weight: 500; margin-bottom: 0.75rem;">Global Visual Storyboards & Dynasties</div>
                <ul style="padding-left: 1.1rem; color: #5A544A; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    <li>🏆 3D Visual Olympic Podium & all-time leaderboards</li>
                    <li>🌍 Interactive nation dominance maps & records</li>
                    <li>⚡ Historical athlete profiles & edition trajectories</li>
                </ul>
            </div>
            <div style="border-top: 1px solid #E5DED2; padding-top: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #8B857C;">
                Instant Demo Profile: <strong style="color: #AA820A;">fan</strong>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Enter as Enthusiast →", key="btn_quick_fan", use_container_width=True):
            login("fan", ROLE_ENTHUSIAST, "Olympic Fan")

    # 2. PRO COACH / ACADEMY ROLE CARD
    with col2:
        _safe_html(f"""
        <div class="bento-marble-card" style="height: 330px; display: flex; flex-direction: column; justify-content: space-between; border-color: rgba(212,175,55,0.6); box-shadow: 0 8px 24px rgba(212,175,55,0.12);">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.6); display: flex; align-items: center; justify-content: center;">
                        {icon_lt}
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #AA820A; font-weight: 800; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); padding: 0.2rem 0.6rem; border-radius: 9999px;">
                        PRO TACTICAL LAB
                    </span>
                </div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.25rem; font-weight: 800; color: #2E2A25;">Performance Coach</div>
                <div style="color: #8B857C; font-size: 0.82rem; font-weight: 500; margin-bottom: 0.75rem;">Biometrics & Head-to-Head Scouting</div>
                <ul style="padding-left: 1.1rem; color: #5A544A; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    <li>🎯 6D Athlete inclination radar & tactical archetypes</li>
                    <li>⚔️ Head-to-head opponent scouting & win probability</li>
                    <li>🏁 Race-quarter pacing & drafting simulator</li>
                </ul>
            </div>
            <div style="border-top: 1px solid #E5DED2; padding-top: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #8B857C;">
                Instant Demo Profile: <strong style="color: #AA820A;">coach</strong>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Enter as Pro Coach →", key="btn_quick_coach", use_container_width=True):
            login("coach", ROLE_ACADEMY, "Elite Sports Academy")

    # 3. ADMIN ROLE CARD
    with col3:
        _safe_html(f"""
        <div class="bento-marble-card" style="height: 330px; display: flex; flex-direction: column; justify-content: space-between;">
            <div>
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.8rem;">
                    <div style="width: 44px; height: 44px; border-radius: 12px; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); display: flex; align-items: center; justify-content: center;">
                        {icon_db}
                    </div>
                    <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #AA820A; font-weight: 800; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.3); padding: 0.2rem 0.6rem; border-radius: 9999px;">
                        ROOT ARCHITECT
                    </span>
                </div>
                <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.25rem; font-weight: 800; color: #2E2A25;">Data Architect</div>
                <div style="color: #8B857C; font-size: 0.82rem; font-weight: 500; margin-bottom: 0.75rem;">Warehouse & Machine Learning</div>
                <ul style="padding-left: 1.1rem; color: #5A544A; font-size: 0.85rem; line-height: 1.6; margin: 0;">
                    <li>🏛️ SQLite Star Schema & live table telemetry</li>
                    <li>🤖 5-Stage Data Mining & Predictive models</li>
                    <li>🎲 5D Multidimensional OLAP Cube operations</li>
                </ul>
            </div>
            <div style="border-top: 1px solid #E5DED2; padding-top: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.74rem; color: #8B857C;">
                Instant Demo Profile: <strong style="color: #AA820A;">admin</strong>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("Enter as Data Architect →", key="btn_quick_admin", use_container_width=True):
            login("admin", ROLE_ADMIN, "System Administrator")

    # Custom Credential Login Option
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    with st.expander("🔑 Secure Credential Authentication (Advanced)"):
        c1, c2, c3 = st.columns([2, 2, 1])
        with c1:
            uname = st.text_input("Username", placeholder="e.g. admin, fan, coach", key="login_uname")
        with c2:
            pword = st.text_input("Password", type="password", placeholder="Enter password", key="login_pword")
        with c3:
            st.markdown("<div style='height: 28px;'></div>", unsafe_allow_html=True)
            if st.button("Sign In", key="btn_submit_login", use_container_width=True):
                uname_clean = uname.strip().lower()
                if uname_clean in DEMO_ACCOUNTS and DEMO_ACCOUNTS[uname_clean]["password"] == pword:
                    acc = DEMO_ACCOUNTS[uname_clean]
                    login(uname_clean, acc["role"], acc["name"])
                else:
                    st.error("Invalid credentials. Demo accounts: admin / olympia2024, fan / olympia, coach / olympia")

    # Footer Metadata
    st.markdown("<div style='height: 24px;'></div>", unsafe_allow_html=True)
    _safe_html("""
    <div style="text-align: center; font-size: 0.75rem; color: #8B857C; font-family: 'JetBrains Mono', monospace; border-top: 1px solid #E5DED2; padding-top: 1.2rem;">
        OLYMPIA // THE LEGACY OF HUMAN GREATNESS, DECODED THROUGH DATA • 20,582 VERIFIED MEDAL RECORDS (1896 – 2026)
    </div>
    """)


def render_sidebar_user_badge():
    """
    Renders the official Olympic VIP Accreditation Pass
    featuring warm gold status dot (ONLINE // SQLITE WAL), role clearance badge,
    and Switch Persona / Logout buttons.
    """
    if not is_authenticated():
        return

    user = get_current_user()
    role = user["role"]
    role_meta = ROLE_DISPLAY.get(role, ROLE_DISPLAY[ROLE_ENTHUSIAST])

    _safe_html(f"""
    <div style="background: #FFFFFF; border: 1px solid #E5DED2; border-radius: 14px; padding: 1rem; margin-bottom: 1.2rem; box-shadow: 0 2px 8px rgba(46,42,37,0.04);">
        <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.5rem;">
            <div style="display: flex; align-items: center; gap: 0.4rem; font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #5A544A;">
                <span style="color: #D4AF37; font-size: 0.65rem;">●</span> ONLINE // SQLITE WAL
            </div>
            <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; color: #7A5C05; background: #FAF0D8; border: 1px solid rgba(212,175,55,0.4); padding: 0.15rem 0.5rem; border-radius: 6px; font-weight: 700;">
                {role_meta['title']}
            </span>
        </div>
        <div style="font-family: 'Cinzel', Georgia, serif; font-size: 1.05rem; font-weight: 800; color: #2E2A25;">
            {user['fullname']}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.72rem; color: #8B857C; margin-top: 0.25rem;">
            ID: <code style="color: #AA820A; background: #F8F5EE; padding: 0.1rem 0.3rem; border-radius: 4px;">{user['username']}</code> • CLEARANCE: <strong style="color: #D4AF37;">ACTIVE</strong>
        </div>
        <div style="border-top: 1px solid #E5DED2; margin-top: 0.65rem; padding-top: 0.45rem; font-family: 'JetBrains Mono', monospace; font-size: 0.68rem; color: #8B857C; display: flex; justify-content: space-between;">
            <span>SESSION // SECURE</span>
            <span>OFFLINE ENGINE</span>
        </div>
    </div>
    """)

    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if col_btn1.button("🔄 Switch", key="sidebar_switch_persona_btn", use_container_width=True):
            logout()
    with col_btn2:
        if col_btn2.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True):
            logout()



def render_login_scrolling_background():
    """Subtle architectural warm atmosphere background helper for authentication entry."""
    pass

