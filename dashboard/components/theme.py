"""
OLYMPIA Brand Identity, Design Tokens & Master Theme Engine.
Implements the Legendary Olympic Intelligence Archive aesthetic:
- Monumental architectural surfaces in Marble White (#FAF8F2) & Sandstone (#EBD9C3)
- Refined Imperial Olympic Gold (#D4AF37) and Victory Red (#C41E3A)
- Authoritative Charcoal (#2E2A25) and Onyx (#1F1F1F) typography & hero surfaces
- Classical Roman Editorial Serif headings (Cinzel, Cormorant Garamond, Playfair Display)
- Precision Data Monospace (JetBrains Mono) for all metrics and counters
- Tactile spring micro-interactions: cubic-bezier(0.22, 1, 0.36, 1)
"""

import re
import streamlit as st

# ============================================================
# 1. OFFICIAL BRAND PALETTE CONSTANTS
# ============================================================
COLOR_MARBLE = "#FAF8F2"       # Main canvas and spacious page backgrounds (65%)
COLOR_SANDSTONE = "#EBD9C3"    # Warm secondary surfaces and heritage accents
COLOR_GOLD = "#D4AF37"         # Primary brand accent, achievement, emphasis (12%)
COLOR_RED = "#C41E3A"          # Rare, high-importance competitive accents (3%)
COLOR_CHARCOAL = "#2E2A25"     # Primary typography and dark cards (20%)
COLOR_ONYX = "#1F1F1F"         # Deep hero panels and high-contrast surfaces
COLOR_WARM_GREY = "#8B857C"    # Secondary text and supporting metadata
COLOR_PALE_GOLD = "#F3E7C5"    # Soft gold-tinted backgrounds & subtle badges
COLOR_BORDER = "#E5DED2"       # Dividers, borders, and component boundaries
COLOR_WHITE = "#FFFFFF"        # Cards, tables, and elevated surfaces

# Semantic Medal Accents
MEDAL_GOLD = "#D4AF37"
MEDAL_SILVER = "#94A3B8"
MEDAL_BRONZE = "#B45309"

# ============================================================
# 2. VECTOR LOGO GENERATORS (INLINE SVG)
# ============================================================
def get_olympia_logo(variant: str = "horizontal", width: int = 220, height: int = 44) -> str:
    """
    Generates inline resolution-independent vector SVG for OLYMPIA brand identity.
    Variants: 'horizontal', 'primary' (vertical), 'mark' (emblem only), 'light' (on dark surfaces), 'favicon'.
    """
    if variant == "mark":
        return f"""<svg width="{width}" height="{height}" viewBox="0 0 200 200" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <defs>
                <linearGradient id="g_mark" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#AA820A"/><stop offset="40%" stop-color="#D4AF37"/><stop offset="80%" stop-color="#F3E7C5"/><stop offset="100%" stop-color="#D4AF37"/>
                </linearGradient>
            </defs>
            <circle cx="100" cy="104" r="76" fill="none" stroke="url(#g_mark)" stroke-width="2.5" stroke-dasharray="380 90" stroke-dashoffset="40" opacity="0.85"/>
            <path d="M78 108 L78 160 C78 161.5 79.2 162 81 162 L87 162 C88.8 162 90 161.5 90 160 L90 114 C90 112 88.5 110 86 109 Z" fill="#2E2A25"/>
            <path d="M95 96 L95 160 C95 161.5 96.2 162 98 162 L105 162 C106.8 162 108 161.5 108 160 L108 84 C108 81.5 106 79.5 103 80 C98.5 81 95 87 95 96 Z" fill="#2E2A25"/>
            <path d="M113 104 L113 160 C113 161.5 114.2 162 116 162 L122 162 C123.8 162 125 161.5 125 160 L125 116 C125 113.5 123 111 120 110 Z" fill="#2E2A25"/>
            <rect x="74" y="164" width="55" height="3.5" rx="1.7" fill="url(#g_mark)"/>
            <path d="M102 78 C99 68 102 52 112 36 C116 30 122 24 126 18 C126.5 17.5 127.5 18 127 19 C124 28 122 36 124 44 C126 52 133 60 134 70 C135 80 128 88 118 90 C125 80 124 66 118 56 C114 50 110 46 109 40 C108.5 39 107.5 39.5 107.8 40.5 C109 48 108 58 104 66 C102.5 69 101.5 73 102 78 Z" fill="url(#g_mark)"/>
        </svg>"""

    elif variant == "light":
        return f"""<svg width="{width}" height="{height}" viewBox="0 0 380 70" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <defs>
                <linearGradient id="g_light" x1="0%" y1="100%" x2="100%" y2="0%">
                    <stop offset="0%" stop-color="#D4AF37"/><stop offset="50%" stop-color="#F3E7C5"/><stop offset="100%" stop-color="#D4AF37"/>
                </linearGradient>
            </defs>
            <g transform="translate(4, 2) scale(0.33)">
                <circle cx="100" cy="104" r="76" fill="none" stroke="url(#g_light)" stroke-width="3" stroke-dasharray="380 90" opacity="0.95"/>
                <path d="M78 108 L78 160 C78 161.5 79.2 162 81 162 L87 162 C88.8 162 90 161.5 90 160 L90 114 Z" fill="#FFFFFF"/>
                <path d="M95 96 L95 160 C95 161.5 96.2 162 98 162 L105 162 C106.8 162 108 161.5 108 160 L108 84 Z" fill="#FFFFFF"/>
                <path d="M113 104 L113 160 C113 161.5 114.2 162 116 162 L122 162 C123.8 162 125 161.5 125 160 L125 116 Z" fill="#FFFFFF"/>
                <rect x="74" y="164" width="55" height="4" rx="2" fill="url(#g_light)"/>
                <path d="M102 78 C99 68 102 52 112 36 C116 30 122 24 126 18 C126.5 17.5 127.5 18 127 19 C124 28 122 36 124 44 C126 52 133 60 134 70 C135 80 128 88 118 90 C125 80 124 66 118 56 C114 50 110 46 109 40 C108.5 39 107.5 39.5 107.8 40.5 C109 48 108 58 104 66 C102.5 69 101.5 73 102 78 Z" fill="url(#g_light)"/>
            </g>
            <text x="82" y="44" font-family="'Cinzel', 'Playfair Display', Georgia, serif" font-size="34" font-weight="800" letter-spacing="4" fill="#FFFFFF">
                OLYMPI<tspan fill="url(#g_light)">A</tspan>
            </text>
            <text x="85" y="58" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600" letter-spacing="3.2" fill="#E5DED2">
                ANALYSE · DISCOVER · EMPOWER
            </text>
        </svg>"""

    # Default: Horizontal lockup for light backgrounds (Top Nav & Header)
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 380 70" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
        <defs>
            <linearGradient id="g_horiz" x1="0%" y1="100%" x2="100%" y2="0%">
                <stop offset="0%" stop-color="#AA820A"/><stop offset="35%" stop-color="#D4AF37"/><stop offset="70%" stop-color="#F3E7C5"/><stop offset="100%" stop-color="#D4AF37"/>
            </linearGradient>
            <linearGradient id="g_char" x1="0%" y1="0%" x2="0%" y2="100%">
                <stop offset="0%" stop-color="#1F1F1F"/><stop offset="100%" stop-color="#2E2A25"/>
            </linearGradient>
        </defs>
        <g transform="translate(4, 2) scale(0.33)">
            <circle cx="100" cy="104" r="76" fill="none" stroke="url(#g_horiz)" stroke-width="3" stroke-dasharray="380 90" stroke-dashoffset="40" opacity="0.9"/>
            <path d="M78 108 L78 160 C78 161.5 79.2 162 81 162 L87 162 C88.8 162 90 161.5 90 160 L90 114 Z" fill="url(#g_char)"/>
            <path d="M95 96 L95 160 C95 161.5 96.2 162 98 162 L105 162 C106.8 162 108 161.5 108 160 L108 84 Z" fill="url(#g_char)"/>
            <path d="M113 104 L113 160 C113 161.5 114.2 162 116 162 L122 162 C123.8 162 125 161.5 125 160 L125 116 Z" fill="url(#g_char)"/>
            <rect x="74" y="164" width="55" height="4" rx="2" fill="url(#g_horiz)"/>
            <path d="M102 78 C99 68 102 52 112 36 C116 30 122 24 126 18 C126.5 17.5 127.5 18 127 19 C124 28 122 36 124 44 C126 52 133 60 134 70 C135 80 128 88 118 90 C125 80 124 66 118 56 C114 50 110 46 109 40 C108.5 39 107.5 39.5 107.8 40.5 C109 48 108 58 104 66 C102.5 69 101.5 73 102 78 Z" fill="url(#g_horiz)"/>
            <path d="M112 68 C110 60 113 50 118 42 C118.5 41 119.5 41.5 119.2 42.5 C117.5 48 118 54 122 60 C124 63 125 67 124 72 C122 76 117 78 113 77 Z" fill="#FFF9E6" opacity="0.95"/>
        </g>
        <text x="82" y="44" font-family="'Cinzel', 'Playfair Display', Georgia, serif" font-size="34" font-weight="800" letter-spacing="4" fill="#2E2A25">
            OLYMPI<tspan fill="url(#g_horiz)">A</tspan>
        </text>
        <text x="85" y="58" font-family="'Inter', sans-serif" font-size="7.5" font-weight="600" letter-spacing="3.2" fill="#8B857C">
            ANALYSE · DISCOVER · EMPOWER
        </text>
    </svg>"""

# ============================================================
# 3. GLOBAL MASTER CSS STYLESHEET
# ============================================================
def get_olympia_theme_css() -> str:
    """Returns the complete, authoritative CSS styling for OLYMPIA's Marble & Gold identity."""
    return f"""
    <meta name="referrer" content="no-referrer" />
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cinzel:wght@600;700;800;900&family=Cormorant+Garamond:ital,wght@0,500;0,600;0,700;1,500;1,600;1,700&family=Playfair+Display:ital,wght@0,600;0,700;0,800;1,600;1,700&family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600;700;800&display=swap" rel="stylesheet" />

    <style>
    /* ============================================================
       A. MASTER DESIGN TOKENS
       ============================================================ */
    :root {{
        --olympia-marble: #FAF8F2;
        --olympia-sandstone: #EBD9C3;
        --olympia-gold: #D4AF37;
        --olympia-gold-hover: #AA820A;
        --olympia-red: #C41E3A;
        --olympia-charcoal: #2E2A25;
        --olympia-onyx: #1F1F1F;
        --olympia-warm-grey: #8B857C;
        --olympia-pale-gold: #F3E7C5;
        --olympia-border: #E5DED2;
        --olympia-white: #FFFFFF;

        --page-background: var(--olympia-marble);
        --surface-primary: var(--olympia-white);
        --surface-secondary: #F4F0E8;
        --surface-hover: #EFE9DE;
        --text-primary: var(--olympia-charcoal);
        --text-secondary: var(--olympia-warm-grey);

        --radius-card: 16px;
        --radius-panel: 22px;
        --radius-control: 10px;

        --shadow-subtle: 0 4px 20px -2px rgba(46, 42, 37, 0.05), 0 2px 6px -1px rgba(46, 42, 37, 0.03);
        --shadow-elevated: 0 12px 32px -4px rgba(46, 42, 37, 0.08), 0 4px 12px -2px rgba(212, 175, 55, 0.12);
        --shadow-hero: 0 20px 48px -8px rgba(0, 0, 0, 0.35);

        --spring-snappy: cubic-bezier(0.22, 1, 0.36, 1);
        --spring-float: cubic-bezier(0.16, 1, 0.3, 1);
        --motion-fast: 180ms;
        --motion-medium: 320ms;
        --motion-slow: 650ms;
    }}

    /* Global Base Reset */
    html, body, .stApp {{
        background-color: var(--olympia-marble) !important;
        color: var(--olympia-charcoal) !important;
        font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
        -webkit-font-smoothing: antialiased;
        text-rendering: optimizeLegibility;
    }}

    /* Architectural Subtle Marble Canvas Texture */
    .stApp {{
        background-image: radial-gradient(rgba(212, 175, 55, 0.04) 1px, transparent 1px), radial-gradient(rgba(46, 42, 37, 0.02) 1px, transparent 1px) !important;
        background-size: 32px 32px, 16px 16px !important;
        background-position: 0 0, 16px 16px !important;
    }}

    /* Custom Selection */
    ::selection {{
        background: rgba(212, 175, 55, 0.28) !important;
        color: #2E2A25 !important;
    }}

    /* Refined Architectural Scrollbar */
    ::-webkit-scrollbar {{
        width: 7px;
        height: 7px;
    }}
    ::-webkit-scrollbar-track {{
        background: #F4F0E8;
    }}
    ::-webkit-scrollbar-thumb {{
        background: #D5CBBB;
        border-radius: 9999px;
    }}
    ::-webkit-scrollbar-thumb:hover {{
        background: var(--olympia-gold);
    }}

    /* ============================================================
       B. EDITORIAL TYPOGRAPHY
       ============================================================ */
    h1, h2, h3, .editorial-heading {{
        font-family: 'Cinzel', 'Cormorant Garamond', 'Playfair Display', Georgia, serif !important;
        color: var(--olympia-charcoal) !important;
        letter-spacing: -0.01em;
        font-weight: 700;
    }}

    .hero-serif-title {{
        font-family: 'Cinzel', 'Playfair Display', Georgia, serif !important;
        letter-spacing: -0.02em;
        line-height: 1.1;
    }}

    /* Tabular Numerals & Telemetry Monospace */
    .telemetry-num, [data-testid="stMetricValue"], .tabular-data {{
        font-family: 'JetBrains Mono', monospace !important;
        font-variant-numeric: tabular-nums !important;
    }}

    /* ============================================================
       C. STREAMLIT CHROME & SIDEBAR CUSTOMIZATION
       ============================================================ */
    /* Hide default Streamlit multi-page list */
    [data-testid="stSidebarNav"],
    div[data-testid="stSidebarNavItems"],
    ul[data-testid="stSidebarNavItems"],
    [data-testid="stSidebarNavSeparator"] {{
        display: none !important;
    }}

    /* Sidebar Background & Borders */
    section[data-testid="stSidebar"] {{
        background-color: #F8F5EE !important;
        border-right: 1px solid var(--olympia-border) !important;
        box-shadow: 2px 0 16px rgba(46, 42, 37, 0.03) !important;
    }}

    section[data-testid="stSidebar"] div[data-testid="stSidebarContent"] {{
        padding-top: 1.2rem !important;
        padding-left: 1.1rem !important;
        padding-right: 1.1rem !important;
    }}

    /* Navigation Radio Pills matching Reference Mockup */
    div[data-testid="stRadio"] > div[role="radiogroup"] > label {{
        background: #FFFFFF !important;
        border: 1px solid var(--olympia-border) !important;
        border-radius: var(--radius-control) !important;
        padding: 0.65rem 1rem !important;
        margin-bottom: 0.45rem !important;
        color: var(--olympia-charcoal) !important;
        font-weight: 500 !important;
        font-size: 0.88rem !important;
        transition: all var(--motion-fast) var(--spring-snappy) !important;
        box-shadow: 0 1px 3px rgba(46, 42, 37, 0.03) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label:hover {{
        background: #F4EFE6 !important;
        border-color: var(--olympia-gold) !important;
        transform: translateX(3px) !important;
    }}

    div[data-testid="stRadio"] > div[role="radiogroup"] > label[data-checked="true"],
    div[data-testid="stRadio"] > div[role="radiogroup"] > label:has(input:checked) {{
        background: linear-gradient(135deg, #FAF3E3 0%, #F5E5BE 100%) !important;
        border-color: var(--olympia-gold) !important;
        color: #1F1F1F !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(212, 175, 55, 0.22) !important;
    }}

    /* Buttons: Tactile Gold & Architectural Finishes */
    div.stButton > button {{
        background: linear-gradient(135deg, #F3E7C5 0%, #D4AF37 100%) !important;
        color: #1F1F1F !important;
        font-family: 'Inter', sans-serif !important;
        font-weight: 700 !important;
        font-size: 0.88rem !important;
        border: 1px solid rgba(170, 130, 10, 0.3) !important;
        border-radius: var(--radius-control) !important;
        padding: 0.55rem 1.25rem !important;
        min-height: 44px !important;
        letter-spacing: 0.02em !important;
        transition: all var(--motion-fast) var(--spring-snappy) !important;
        box-shadow: 0 2px 8px rgba(212, 175, 55, 0.22) !important;
    }}

    div.stButton > button:hover {{
        background: linear-gradient(135deg, #FAF0D8 0%, #DFBA45 100%) !important;
        box-shadow: 0 6px 18px rgba(212, 175, 55, 0.35) !important;
        transform: translateY(-2px) !important;
    }}

    div.stButton > button:active {{
        transform: scale(0.98) !important;
    }}

    /* Secondary / Ghost Buttons */
    div.stButton > button[kind="secondary"] {{
        background: #FFFFFF !important;
        color: var(--olympia-charcoal) !important;
        border: 1px solid var(--olympia-border) !important;
        box-shadow: 0 1px 4px rgba(46, 42, 37, 0.04) !important;
    }}
    div.stButton > button[kind="secondary"]:hover {{
        background: #FAF8F2 !important;
        border-color: var(--olympia-gold) !important;
        color: #AA820A !important;
    }}

    /* Selectboxes, Multi-selects & Inputs */
    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div,
    div[data-testid="stTextInput"] input {{
        background-color: #FFFFFF !important;
        border-color: var(--olympia-border) !important;
        color: var(--olympia-charcoal) !important;
        border-radius: var(--radius-control) !important;
        font-size: 0.88rem !important;
    }}

    div[data-baseweb="select"] > div:hover,
    div[data-baseweb="input"] > div:hover,
    div[data-testid="stTextInput"] input:focus {{
        border-color: var(--olympia-gold) !important;
        box-shadow: 0 0 0 1px var(--olympia-gold) !important;
    }}

    /* Segmented Controls / Tabs */
    .stTabs [data-baseweb="tab-list"] {{
        background: #F4F0E8 !important;
        border: 1px solid var(--olympia-border) !important;
        border-radius: var(--radius-control) !important;
        padding: 4px !important;
        gap: 4px !important;
    }}

    .stTabs [data-baseweb="tab"] {{
        background: transparent !important;
        border-radius: 8px !important;
        color: var(--olympia-warm-grey) !important;
        font-weight: 600 !important;
        font-size: 0.85rem !important;
        padding: 0.45rem 1rem !important;
        border: none !important;
        transition: all var(--motion-fast) var(--spring-snappy) !important;
    }}

    .stTabs [aria-selected="true"] {{
        background: #FFFFFF !important;
        color: var(--olympia-charcoal) !important;
        box-shadow: 0 2px 8px rgba(46, 42, 37, 0.08) !important;
    }}

    /* Metric Container Overrides */
    div[data-testid="stMetric"] {{
        background: var(--olympia-white) !important;
        border: 1px solid var(--olympia-border) !important;
        border-radius: var(--radius-card) !important;
        padding: 1.1rem 1.25rem !important;
        box-shadow: var(--shadow-subtle) !important;
        transition: all var(--motion-fast) var(--spring-snappy) !important;
    }}

    div[data-testid="stMetric"]:hover {{
        border-color: var(--olympia-gold) !important;
        box-shadow: var(--shadow-elevated) !important;
        transform: translateY(-2px) !important;
    }}

    div[data-testid="stMetricLabel"] {{
        font-family: 'Inter', sans-serif !important;
        font-size: 0.78rem !important;
        text-transform: uppercase !important;
        letter-spacing: 0.08em !important;
        color: var(--olympia-warm-grey) !important;
        font-weight: 600 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: var(--olympia-charcoal) !important;
        font-weight: 700 !important;
    }}

    /* ============================================================
       D. CUSTOM BENTO ARCHITECTURAL SURFACES
       ============================================================ */
    .bento-marble-card {{
        background: #FFFFFF;
        border: 1px solid var(--olympia-border);
        border-radius: var(--radius-card);
        padding: 1.4rem;
        box-shadow: var(--shadow-subtle);
        transition: all var(--motion-fast) var(--spring-snappy);
        position: relative;
        overflow: hidden;
    }}

    .bento-marble-card:hover {{
        border-color: rgba(212, 175, 55, 0.6);
        box-shadow: var(--shadow-elevated);
        transform: translateY(-3px);
    }}

    /* Split Hero Left Card: Dark Onyx Architectural Panel */
    .hero-onyx-card {{
        background: linear-gradient(135deg, #1C1B19 0%, #292622 100%);
        border: 1px solid rgba(212, 175, 55, 0.28);
        border-radius: var(--radius-panel);
        padding: 2.2rem 2.4rem;
        box-shadow: var(--shadow-hero);
        color: #FAF8F2;
        position: relative;
        overflow: hidden;
    }}

    .hero-onyx-card::before {{
        content: '';
        position: absolute;
        top: 0;
        right: 0;
        width: 45%;
        height: 100%;
        background: radial-gradient(circle at 80% 40%, rgba(212, 175, 55, 0.15) 0%, transparent 70%);
        pointer-events: none;
    }}

    /* Split Hero Right Card: Olympic Legacy in Numbers */
    .hero-legacy-card {{
        background: #FFFFFF;
        border: 1px solid var(--olympia-border);
        border-radius: var(--radius-panel);
        padding: 1.8rem 2rem;
        box-shadow: var(--shadow-subtle);
        height: 100%;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }}

    /* Top Telemetry Floating Command Header */
    .telemetry-hud-bar {{
        position: sticky;
        top: 0.5rem;
        z-index: 998;
        background: rgba(250, 248, 242, 0.94);
        backdrop-filter: blur(16px) saturate(180%);
        border: 1px solid var(--olympia-border);
        border-radius: 14px;
        padding: 0.55rem 1.25rem;
        margin-bottom: 1.2rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 4px 20px rgba(46, 42, 37, 0.05);
        font-family: 'Inter', sans-serif;
    }}

    .hud-left {{
        display: flex;
        align-items: center;
        gap: 0.9rem;
    }}

    .hud-breadcrumb {{
        display: flex;
        align-items: center;
        gap: 0.45rem;
        font-size: 0.8rem;
        font-weight: 600;
        font-family: 'JetBrains Mono', monospace;
    }}

    .hud-brand {{
        font-family: 'Cinzel', Georgia, serif;
        font-weight: 800;
        letter-spacing: 0.12em;
        color: #2E2A25;
    }}

    .hud-sep {{
        color: #D5CBBB;
    }}

    .hud-role {{
        color: #AA820A;
        font-weight: 700;
    }}

    .hud-module {{
        color: #5A544A;
    }}

    .hud-center {{
        display: flex;
        align-items: center;
    }}

    .hud-ticker-pill {{
        background: #F4EFE6;
        border: 1px solid var(--olympia-border);
        padding: 0.28rem 0.95rem;
        border-radius: 9999px;
        font-size: 0.74rem;
        color: #5A544A;
        display: flex;
        align-items: center;
        gap: 0.55rem;
        font-family: 'JetBrains Mono', monospace;
    }}

    .ticker-dot {{
        color: var(--olympia-gold);
        font-size: 0.65rem;
        animation: pulseGold 2s infinite ease-in-out;
    }}

    @keyframes pulseGold {{
        0%, 100% {{ opacity: 1; transform: scale(1); }}
        50% {{ opacity: 0.4; transform: scale(0.85); }}
    }}

    .hud-right {{
        display: flex;
        align-items: center;
        gap: 0.75rem;
    }}

    .hud-scrubber-pill {{
        background: #FFFFFF;
        border: 1px solid var(--olympia-border);
        padding: 0.25rem 0.75rem;
        border-radius: 9999px;
        font-size: 0.72rem;
        font-family: 'JetBrains Mono', monospace;
        color: #5A544A;
    }}

    .role-chip {{
        display: inline-block;
        padding: 0.22rem 0.6rem;
        border-radius: 6px;
        font-size: 0.72rem;
        font-weight: 700;
        color: #5A544A;
        border: 1px solid var(--olympia-border);
        text-decoration: none !important;
        transition: all 0.15s ease;
    }}

    .role-chip:hover {{
        border-color: var(--olympia-gold);
        color: #AA820A;
    }}

    .active-chip {{
        background: #FAF0D8;
        border-color: var(--olympia-gold);
        color: #7A5C05 !important;
    }}

    /* Global Telemetry Status Footer */
    .telemetry-footer-bar {{
        margin-top: 3.5rem;
        padding: 1.1rem 1.6rem;
        background: #F8F5EE;
        border-top: 1px solid var(--olympia-border);
        border-radius: 14px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        font-size: 0.76rem;
        color: var(--olympia-warm-grey);
        font-family: 'Inter', sans-serif;
    }}

    /* Accessibility: prefers-reduced-motion */
    @media (prefers-reduced-motion: reduce) {{
        * {{
            animation-duration: 0.01ms !important;
            animation-iteration-count: 1 !important;
            transition-duration: 0.01ms !important;
            scroll-behavior: auto !important;
        }}
    }}
    </style>
    """

def inject_olympia_theme():
    """Injects the global OLYMPIA theme stylesheet."""
    css = get_olympia_theme_css()
    if hasattr(st, "html"):
        st.html(css)
    else:
        st.markdown(css, unsafe_allow_html=True)
