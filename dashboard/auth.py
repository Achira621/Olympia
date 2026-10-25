"""
Authentication and Role-Based Access Control for OLYMPIA.
High-Contrast Modern Dark-Themed Authentication Portal.
Palette:
- #0F0F0F (Pitch Black Canvas)
- #202020 (Charcoal Surface Container)
- #5DD62C (Electric Lime Accent & CTA)
- #337418 (Forest Green Secondary Accent)
- #F8F8F8 (Off-White Primary Typography)
"""

import os
import re
import base64
import textwrap
import streamlit as st
from typing import Optional, Tuple
from dashboard.components.icons import get_svg_icon

# Role Constants (Normalized: admin, enthusiast, professional)
ROLE_ADMIN = "admin"
ROLE_ENTHUSIAST = "enthusiast"
ROLE_PROFESSIONAL = "professional"
ROLE_ACADEMY = ROLE_PROFESSIONAL  # Alias for backwards compatibility

ROLE_DISPLAY = {
    ROLE_ADMIN: {
        "title": "Administrator",
        "icon": get_svg_icon("database", size=16, color="#5DD62C"),
        "badge_color": "#5DD62C",
        "badge_bg": "rgba(93, 214, 44, 0.15)",
        "description": "Full access to Data Warehouse, dataset editor, system stats, and administrative controls."
    },
    ROLE_ENTHUSIAST: {
        "title": "Sport Enthusiast",
        "icon": get_svg_icon("trophy", size=16, color="#A3E635"),
        "badge_color": "#A3E635",
        "badge_bg": "rgba(163, 230, 53, 0.15)",
        "description": "The Podium, OLAP Cube, Data Mining Arena, and Athlete Hall of Fame."
    },
    ROLE_PROFESSIONAL: {
        "title": "Professional / Academy",
        "icon": get_svg_icon("lightning", size=16, color="#5DD62C"),
        "badge_color": "#5DD62C",
        "badge_bg": "rgba(93, 214, 44, 0.15)",
        "description": "Advanced physical telemetry, sports science deep dives, and Predict Your Potential."
    },
    # Backwards compatibility keys
    "ADMIN": {
        "title": "Administrator",
        "icon": get_svg_icon("database", size=16, color="#5DD62C"),
        "badge_color": "#5DD62C",
        "badge_bg": "rgba(93, 214, 44, 0.15)",
        "description": "Full access to Data Warehouse, dataset editor, system stats, and administrative controls."
    },
    "SPORT_ENTHUSIAST": {
        "title": "Sport Enthusiast",
        "icon": get_svg_icon("trophy", size=16, color="#A3E635"),
        "badge_color": "#A3E635",
        "badge_bg": "rgba(163, 230, 53, 0.15)",
        "description": "The Podium, OLAP Cube, Data Mining Arena, and Athlete Hall of Fame."
    },
    "PLAYER_ACADEMY": {
        "title": "Professional / Academy",
        "icon": get_svg_icon("lightning", size=16, color="#5DD62C"),
        "badge_color": "#5DD62C",
        "badge_bg": "rgba(93, 214, 44, 0.15)",
        "description": "Advanced physical telemetry, sports science deep dives, and Predict Your Potential."
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
    # Support query parameter login convenience (e.g., ?role=admin, ?role=fan, ?role=coach)
    role_param = st.query_params.get("role")
    if role_param and not st.session_state.get("authenticated", False):
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
            st.session_state["authenticated"] = True
            st.session_state["logged_in"] = True
            st.session_state["username"] = u
            st.session_state["user_role"] = r
            st.session_state["user_fullname"] = f
            return True

    is_auth = st.session_state.get("authenticated", False)
    st.session_state["logged_in"] = is_auth
    return is_auth


def get_current_role() -> Optional[str]:
    """Returns the active user role."""
    init_auth()
    return st.session_state.get("user_role")


def get_current_user() -> Optional[dict]:
    """Returns user profile metadata."""
    init_auth()
    if not is_authenticated():
        return None
    return {
        "username": st.session_state.get("username"),
        "role": st.session_state.get("user_role"),
        "fullname": st.session_state.get("user_fullname", "User"),
    }


def login(username: str, role: str, fullname: Optional[str] = None):
    """Sets session state on successful authentication."""
    init_auth()
    st.session_state["authenticated"] = True
    st.session_state["logged_in"] = True
    st.session_state["username"] = username
    st.session_state["user_role"] = role
    st.session_state["user_fullname"] = fullname or DEMO_ACCOUNTS.get(username, {}).get("name", username)
    st.session_state["selected_role_intent"] = None
    if "role" in st.query_params:
        del st.query_params["role"]
    st.rerun()


def logout():
    """Clears authentication session state."""
    init_auth()
    st.session_state["authenticated"] = False
    st.session_state["logged_in"] = False
    st.session_state["username"] = None
    st.session_state["user_role"] = None
    st.session_state["user_fullname"] = None
    st.session_state["selected_role_intent"] = None
    if "role" in st.query_params:
        del st.query_params["role"]
    st.rerun()


@st.cache_data
def get_login_background_images_b64() -> list:
    """Reads Olympic background images and returns them as Base64 data URIs."""
    assets_dir = os.path.join(os.path.dirname(__file__), "assets", "backgrounds")
    filenames = [
        "olympic_stadium.png",
        "usain_bolt.png",
        "olympic_flags.png",
        "ancient_olympics.png",
        "olympic_rings.png"
    ]
    b64_list = []
    for fn in filenames:
        p = os.path.join(assets_dir, fn)
        if os.path.exists(p):
            with open(p, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                b64_list.append(f"data:image/png;base64,{b64}")
    return b64_list


def render_login_scrolling_background():
    """
    Renders an infinite 3-column continuous scrolling image background
    with heavy blur and opacity, positioned strictly behind the login page.
    Exclusively rendered when the user is unauthenticated.
    """
    if st.session_state.get("logged_in", False):
        return

    images = get_login_background_images_b64()
    if not images:
        return

    # Create 3 staggered lists (duplicated to create a seamless infinite loop at -50% translateY)
    col1_imgs = (images + images)
    col2_imgs = (images[1:] + images[:1]) + (images[1:] + images[:1])
    col3_imgs = (images[2:] + images[:2]) + (images[2:] + images[:2])

    col1_html = "".join([f'<img src="{src}" alt="Olympic Asset">' for src in col1_imgs])
    col2_html = "".join([f'<img src="{src}" alt="Olympic Asset">' for src in col2_imgs])
    col3_html = "".join([f'<img src="{src}" alt="Olympic Asset">' for src in col3_imgs])

    bg_html = f"""
    <style>
        /* 1. 3-COLUMN VERTICAL SCROLL: z-index: -1, position: fixed */
        .login-bg-container {{
            position: fixed;
            top: -5%;
            left: -5%;
            width: 110vw;
            height: 110vh;
            z-index: -1;
            overflow: hidden;
            pointer-events: none;
            display: flex;
            justify-content: space-between;
            gap: 1.8rem;
            /* 3. HEAVY BLUR & OPACITY */
            filter: blur(10px) brightness(0.4);
            opacity: 0.9;
            box-sizing: border-box;
        }}

        .login-bg-col {{
            flex: 1;
            height: 100%;
            overflow: hidden;
            position: relative;
        }}

        .login-scroll-track {{
            display: flex;
            flex-direction: column;
            gap: 1.8rem;
            width: 100%;
            will-change: transform;
        }}

        .login-scroll-track img {{
            width: 100%;
            height: 380px;
            object-fit: cover;
            border-radius: 14px;
            display: block;
            box-shadow: 0 8px 30px rgba(0, 0, 0, 0.7);
        }}

        /* 2. INFINITE CSS ANIMATION (Staggered 20s, 25s, 30s & Directions Up, Down, Up) */
        .col-scroll-up-1 {{
            animation: scrollInfiniteUp 20s linear infinite;
        }}

        .col-scroll-down {{
            animation: scrollInfiniteDown 25s linear infinite;
        }}

        .col-scroll-up-2 {{
            animation: scrollInfiniteUp 30s linear infinite;
        }}

        @keyframes scrollInfiniteUp {{
            0% {{
                transform: translateY(0);
            }}
            100% {{
                transform: translateY(-50%);
            }}
        }}

        @keyframes scrollInfiniteDown {{
            0% {{
                transform: translateY(-50%);
            }}
            100% {{
                transform: translateY(0%);
            }}
        }}

        /* Ensure .stApp background transparency ONLY during login state so z-index: -1 is visible */
        .stApp {{
            background-color: transparent !important;
        }}
        html, body {{
            background-color: #0F0F0F !important;
        }}
        /* Ensure login cards stay firmly interactive and prominent */
        .main .block-container, div[data-testid="stMainBlockContainer"] {{
            position: relative !important;
            z-index: 10 !important;
        }}

        /* Hide default Streamlit multi-page sidebar navigation list */
        [data-testid="stSidebarNav"],
        div[data-testid="stSidebarNavItems"],
        ul[data-testid="stSidebarNavItems"],
        [data-testid="stSidebarNavSeparator"] {{
            display: none !important;
        }}

        /* Mobile optimizations for auth background */
        @media (max-width: 768px) {{
            .login-bg-container {{
                gap: 0.8rem;
                filter: blur(6px) brightness(0.35);
            }}
            .login-bg-col:nth-child(2),
            .login-bg-col:nth-child(3) {{
                display: none !important;
            }}
            .login-bg-col:nth-child(1) {{
                width: 100% !important;
            }}
        }}
    </style>

    <div class="login-bg-container">
        <div class="login-bg-col">
            <div class="login-scroll-track col-scroll-up-1">
                {col1_html}
            </div>
        </div>
        <div class="login-bg-col">
            <div class="login-scroll-track col-scroll-down">
                {col2_html}
            </div>
        </div>
        <div class="login-bg-col">
            <div class="login-scroll-track col-scroll-up-2">
                {col3_html}
            </div>
        </div>
    </div>
    """

    if hasattr(st, "html"):
        st.html(bg_html)
    else:
        st.markdown(bg_html, unsafe_allow_html=True)


def render_landing_page():
    """
    Renders the futuristic, 3-role spatial authentication portal.
    Weightless 3D floating glass hero card over animated aurora backdrop
    with 3 isometric persona accreditation cards and instant 1-click initialization.
    """
    init_auth()

    # Dynamic blurred continuous scrolling background (exclusively for login)
    if not st.session_state.get("logged_in", False):
        render_login_scrolling_background()

    # Hero Section: Weightless 3D Floating Glass Hero
    rings_svg = get_olympic_rings_svg(width=64, height=30)
    brand_trophy = get_svg_icon("trophy", size=32, color="#5DD62C")

    _safe_html(f"""
    <div class="auth-aurora-hero">
        <div style="display: flex; justify-content: center; align-items: center; gap: 1rem; margin-bottom: 0.8rem;">
            {rings_svg}
        </div>
        <div style="font-family: 'JetBrains Mono', monospace; font-size: 0.82rem; color: #5DD62C; letter-spacing: 0.2em; text-transform: uppercase; font-weight: 700; margin-bottom: 0.4rem;">
            ENTER THE OLYMPIC INTELLIGENCE VAULT
        </div>
        <h1 class="auth-hero-title" style="font-family: 'Space Grotesk', 'Playfair Display', sans-serif !important; font-size: clamp(2.4rem, 6.5vw, 3.8rem); font-weight: 900; color: #F8FAFC; margin: 0; line-height: 1.05; letter-spacing: -0.03em;">
            OLYMPIA <span style="color: #5DD62C; font-weight: 400;">OS</span>
        </h1>
        <div style="font-size: clamp(0.85rem, 2.5vw, 1.05rem); color: #94A3B8; font-weight: 600; letter-spacing: 0.06em; text-transform: uppercase; margin-top: 0.5rem; font-family: 'Inter', sans-serif;">
            F1-Style Olympic Telemetry • Star Schema Warehouse • Predictive Modeling
        </div>
        <p style="max-width: 720px; margin: 0.9rem auto 0 auto; color: #CBD5E1; font-size: clamp(0.88rem, 2vw, 0.98rem); line-height: 1.6; font-family: 'Inter', sans-serif;">
            Explore 130 years of Olympic history (1896 – 2026) through an offline-first Star Schema warehouse,
            real-time tactical coach intelligence, and multi-dimensional OLAP cubes.
        </p>
    </div>
    """)

    st.markdown("<div style='text-align: center; color: #94A3B8; font-family: Space Grotesk, sans-serif; font-size: 0.85rem; letter-spacing: 0.14em; text-transform: uppercase; font-weight: 700; margin-bottom: 1.2rem;'>Select Identity to Initialize Session</div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3, gap="medium")

    icon_db = get_svg_icon("database", size=26, color="#38BDF8")
    icon_tr = get_svg_icon("trophy", size=26, color="#F59E0B")
    icon_lt = get_svg_icon("lightning", size=26, color="#5DD62C")

    # 1. SPORT ENTHUSIAST ROLE CARD
    with col1:
        _safe_html(f"""
        <div class="persona-isometric-card enthusiast-card">
            <div class="persona-card-header">
                <div class="persona-icon-circle" style="background: rgba(245, 158, 11, 0.12); border-color: #F59E0B;">
                    {icon_tr}
                </div>
                <span class="persona-clearance-badge" style="color: #F59E0B; border-color: rgba(245, 158, 11, 0.4); background: rgba(245, 158, 11, 0.1);">
                    CLEARANCE: TIER 1
                </span>
            </div>
            <div class="persona-title">Sport Enthusiast</div>
            <div class="persona-tagline">Visual Storyboards & Dynasties</div>
            <ul class="persona-feature-list">
                <li>🏆 3D Visual Olympic Podium & medal tallies</li>
                <li>🌍 Interactive nation dominance maps & milestones</li>
                <li>⚡ Legend profiles & multi-edition trajectories</li>
            </ul>
            <div class="persona-card-footer">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">Auto-Profile: <code style="color: #F59E0B;">fan</code></span>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Initialize as Enthusiast →", key="btn_quick_fan", use_container_width=True):
            login("fan", ROLE_ENTHUSIAST, "Olympic Fan")

    # 2. PRO COACH / ACADEMY ROLE CARD
    with col2:
        _safe_html(f"""
        <div class="persona-isometric-card coach-card">
            <div class="persona-card-header">
                <div class="persona-icon-circle" style="background: rgba(93, 214, 44, 0.14); border-color: #5DD62C;">
                    {icon_lt}
                </div>
                <span class="persona-clearance-badge" style="color: #5DD62C; border-color: rgba(93, 214, 44, 0.4); background: rgba(93, 214, 44, 0.1);">
                    CLEARANCE: PRO TACTICAL
                </span>
            </div>
            <div class="persona-title" style="color: #5DD62C;">Performance Coach</div>
            <div class="persona-tagline">Kinetic Telemetry & Matchups</div>
            <ul class="persona-feature-list">
                <li>🎯 6D Athlete inclination radar & archetypes</li>
                <li>⚔️ Head-to-head opponent scouting & win prob</li>
                <li>🏁 Race pacing & aerodynamic drafting simulator</li>
            </ul>
            <div class="persona-card-footer">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">Auto-Profile: <code style="color: #5DD62C;">coach</code></span>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Initialize as Pro Coach →", key="btn_quick_coach", use_container_width=True):
            login("coach", ROLE_ACADEMY, "Elite Sports Academy")

    # 3. ADMIN ROLE CARD
    with col3:
        _safe_html(f"""
        <div class="persona-isometric-card admin-card">
            <div class="persona-card-header">
                <div class="persona-icon-circle" style="background: rgba(56, 189, 248, 0.12); border-color: #38BDF8;">
                    {icon_db}
                </div>
                <span class="persona-clearance-badge" style="color: #38BDF8; border-color: rgba(56, 189, 248, 0.4); background: rgba(56, 189, 248, 0.1);">
                    CLEARANCE: ROOT ADMIN
                </span>
            </div>
            <div class="persona-title">Data Architect</div>
            <div class="persona-tagline">Warehouse & Machine Learning</div>
            <ul class="persona-feature-list">
                <li>🏛️ SQLite Star Schema & live table telemetry</li>
                <li>🤖 5-Stage Data Mining & Predictive models</li>
                <li>🎲 5D Multidimensional OLAP Cube operations</li>
            </ul>
            <div class="persona-card-footer">
                <span style="font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #94A3B8;">Auto-Profile: <code style="color: #38BDF8;">admin</code></span>
            </div>
        </div>
        """)
        st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
        if st.button("⚡ Initialize as Admin →", key="btn_quick_admin", use_container_width=True):
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
    <div style="text-align: center; font-size: 0.75rem; color: #64748B; font-family: 'JetBrains Mono', monospace; border-top: 1px solid rgba(255,255,255,0.06); padding-top: 1.2rem;">
        OLYMPIA OS // KINETIC TELEMETRY LAB • 20,582 VERIFIED MEDAL FACTS (1896 – 2026)
    </div>
    """)


def render_sidebar_user_badge():
    """
    Renders the official Olympic VIP Accreditation Hologram Pass
    featuring glowing status dot (ONLINE // SQLITE WAL), role clearance badge,
    session uptime counter, and tactile Switch Persona / Logout micro-button.
    """
    if not is_authenticated():
        return

    user = get_current_user()
    role = user["role"]
    role_meta = ROLE_DISPLAY.get(role, ROLE_DISPLAY[ROLE_ENTHUSIAST])
    role_color = role_meta["badge_color"]

    _safe_html(f"""
    <div class="vip-accreditation-pass">
        <div class="pass-hologram-strip"></div>
        <div class="pass-header">
            <div class="pass-status-dot-wrap">
                <span class="pass-pulse-dot"></span>
                <span class="pass-status-text">ONLINE // SQLITE WAL</span>
            </div>
            <span class="pass-clearance-chip" style="color: {role_color}; border-color: {role_color};">
                {role_meta['title']}
            </span>
        </div>
        <div class="pass-body">
            <div class="pass-user-name">{user['fullname']}</div>
            <div class="pass-details-row">
                <span>ID: <code style="color: #5DD62C;">{user['username']}</code></span>
                <span>CLEARANCE: <strong style="color: {role_color};">ACTIVE</strong></span>
            </div>
        </div>
        <div class="pass-footer">
            <span class="pass-session-clock">SESSION // ACTIVE</span>
            <span style="color: #64748B;">•</span>
            <span style="color: #94A3B8; font-size: 0.7rem;">OFFLINE ENGINE</span>
        </div>
    </div>
    """)

    col_btn1, col_btn2 = st.sidebar.columns(2)
    with col_btn1:
        if st.sidebar.button("🔄 Switch Persona", key="sidebar_switch_persona_btn", use_container_width=True):
            logout()
    with col_btn2:
        if st.sidebar.button("🚪 Log Out", key="sidebar_logout_btn", use_container_width=True):
            logout()

