"""
Custom SVG Icon Library for OLYMPIA.
Replaces all emojis with crisp, lightweight, resolution-independent SVG vector icons
modeled after Forbes' minimalist editorial design system.
"""

import re

# Palette Constants - OLYMPIA Architectural Brand Identity
COLOR_GOLD = "#D4AF37"
COLOR_SILVER = "#94A3B8"
COLOR_BRONZE = "#B45309"
COLOR_GREEN = "#16A34A"
COLOR_RED = "#C41E3A"
COLOR_BLUE = "#2E2A25"
COLOR_MUTED = "#8B857C"
COLOR_WHITE = "#FAF8F2"
COLOR_ACCENT = "#D4AF37"


# Emoji to Icon Name Alias Dictionary for 100% Emoji Replacement
EMOJI_ALIASES = {
    "🥇": "gold_medal",
    "🥈": "silver_medal",
    "🥉": "bronze_medal",
    "🏅": "gold_medal",
    "🏆": "trophy",
    "⚡": "lightning",
    "🌐": "globe",
    "🌍": "globe",
    "📅": "calendar",
    "🔍": "search",
    "🔎": "search",
    "📊": "chart",
    "📈": "trend_up",
    "📉": "trend_down",
    "🏛️": "database",
    "🗄️": "database",
    "💾": "database",
    "👥": "user",
    "👤": "user",
    "⭐": "star",
    "🎯": "star",
    "🔥": "lightning",
    "🕒": "calendar",
    "🛡️": "trophy",
    "🏃": "lightning",
    "📜": "chart",
    "🧊": "database",
    "🤖": "chart",
    "✏️": "chart",
    "➕": "trend_up",
    "🗑️": "trend_down",
    "💡": "lightning",
    "📌": "star",
    "⚠️": "trend_down"
}


def get_svg_icon(name: str, size: int = 18, color: str = "currentColor", stroke_width: float = 1.8) -> str:
    """
    Returns an inline SVG string for the requested icon name or emoji alias.
    """
    if not name:
        return ""
    
    # Check if name is an emoji alias
    resolved_name = EMOJI_ALIASES.get(name.strip(), name.strip())

    svg_map = {
        "gold_medal": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="12" cy="14" r="7" fill="{COLOR_GOLD}" fill-opacity="0.25" stroke="{COLOR_GOLD}" stroke-width="{stroke_width}"/>
            <path d="M12 11V17M10 13H14" stroke="{COLOR_GOLD}" stroke-width="{stroke_width}" stroke-linecap="round"/>
            <path d="M8 7L6 3H9L12 7M16 7L18 3H15L12 7" stroke="{COLOR_GOLD}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "silver_medal": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="12" cy="14" r="7" fill="{COLOR_SILVER}" fill-opacity="0.2" stroke="{COLOR_SILVER}" stroke-width="{stroke_width}"/>
            <path d="M12 11V17M10 13H14" stroke="{COLOR_SILVER}" stroke-width="{stroke_width}" stroke-linecap="round"/>
            <path d="M8 7L6 3H9L12 7M16 7L18 3H15L12 7" stroke="{COLOR_SILVER}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "bronze_medal": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="12" cy="14" r="7" fill="{COLOR_BRONZE}" fill-opacity="0.25" stroke="{COLOR_BRONZE}" stroke-width="{stroke_width}"/>
            <path d="M12 11V17M10 13H14" stroke="{COLOR_BRONZE}" stroke-width="{stroke_width}" stroke-linecap="round"/>
            <path d="M8 7L6 3H9L12 7M16 7L18 3H15L12 7" stroke="{COLOR_BRONZE}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "trophy": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M8 21H16M12 17V21M6 4H18V9C18 12.3137 15.3137 15 12 15C8.68629 15 6 12.3137 6 9V4ZM6 6H3V8C3 9.65685 4.34315 11 6 11V6ZM18 6H21V8C21 9.65685 19.6569 11 18 11V6Z" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "podium": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M3 20H21M4 20V12H9V20M9 20V8H15V20M15 20V14H20V20" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "search": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="11" cy="11" r="7" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M20 20L16 16" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        </svg>
        """,
        "trend_up": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M7 17L17 7M17 7H9M17 7V15" stroke="{COLOR_GREEN}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "trend_down": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M7 7L17 17M17 17H9M17 17V9" stroke="{COLOR_RED}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "chevron_down": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M6 9L12 15L18 9" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "filter": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M3 4H21V6.5L14 13.5V19L10 21V13.5L3 6.5V4Z" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "globe": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="12" cy="12" r="9" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M3 12H21M12 3C14.5 5.5 16 8.5 16 12C16 15.5 14.5 18.5 12 21C9.5 18.5 8 15.5 8 12C8 8.5 9.5 5.5 12 3Z" stroke="{color}" stroke-width="{stroke_width}"/>
        </svg>
        """,
        "calendar": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <rect x="3" y="5" width="18" height="16" rx="2" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M3 10H21M8 3V7M16 3V7" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        </svg>
        """,
        "lightning": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M13 2L3 14H12L11 22L21 10H12L13 2Z" stroke="{COLOR_ACCENT}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "chart": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <path d="M4 20H20M6 16V14M11 16V9M16 16V5" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/>
        </svg>
        """,
        "database": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <ellipse cx="12" cy="5" rx="8" ry="3" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M4 5V12C4 13.6569 7.58172 15 12 15C16.4183 15 20 13.6569 20 12V5M4 12V19C4 20.6569 7.58172 22 12 22C16.4183 22 20 20.6569 20 19V12" stroke="{color}" stroke-width="{stroke_width}"/>
        </svg>
        """,
        "user": f"""
        <svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
            <circle cx="12" cy="8" r="4" stroke="{color}" stroke-width="{stroke_width}"/>
            <path d="M5 20C5 16.5 8 14 12 14C16 14 19 16.5 19 20" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round"/>
        </svg>
        """,
        "star": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2" stroke="{COLOR_GOLD}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round" fill="{COLOR_GOLD}" fill-opacity="0.2"/></svg>""",
        "arrow_right": f"""<svg width="{size}" height="{size}" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;"><path d="M5 12H19M19 12L13 6M19 12L13 18" stroke="{color}" stroke-width="{stroke_width}" stroke-linecap="round" stroke-linejoin="round"/></svg>"""
    }
    raw_svg = svg_map.get(resolved_name, f"""<span style="font-size: {size}px; color: {color};">•</span>""")
    return re.sub(r'\s+', ' ', raw_svg).strip()


def render_medal_pills(gold: int, silver: int, bronze: int) -> str:
    """Returns compact HTML badges with custom SVG icons for gold, silver, bronze."""
    g_svg = get_svg_icon("gold_medal", size=15)
    s_svg = get_svg_icon("silver_medal", size=15)
    b_svg = get_svg_icon("bronze_medal", size=15)
    pills = f"""<div style="display: inline-flex; align-items: center; gap: 0.5rem; font-size: 0.8rem; font-weight: 600;"><span style="display: inline-flex; align-items: center; gap: 0.25rem; color: {COLOR_GOLD};">{g_svg} {gold:,}</span><span style="display: inline-flex; align-items: center; gap: 0.25rem; color: {COLOR_SILVER};">{s_svg} {silver:,}</span><span style="display: inline-flex; align-items: center; gap: 0.25rem; color: {COLOR_BRONZE};">{b_svg} {bronze:,}</span></div>"""
    return re.sub(r'\s+', ' ', pills).strip()


def get_olympic_rings_svg(width: int = 48, height: int = 24) -> str:
    """Returns a refined, elegant metallic Olympic rings SVG motif."""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 100 48" fill="none" xmlns="http://www.w3.org/2000/svg" style="vertical-align: middle; display: inline-block;">
        <circle cx="20" cy="18" r="14" stroke="#2563EB" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
        <circle cx="50" cy="18" r="14" stroke="#2E2A25" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
        <circle cx="80" cy="18" r="14" stroke="#C41E3A" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
        <circle cx="35" cy="30" r="14" stroke="#D4AF37" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
        <circle cx="65" cy="30" r="14" stroke="#16A34A" stroke-width="2.6" stroke-linecap="round" opacity="0.9"/>
    </svg>"""


def get_olympic_sculpted_rings_svg(width: int = 340, height: int = 150) -> str:
    """Returns the large sculpted metallic Olympic rings illustration seen in the hero panel."""
    return f"""<svg width="{width}" height="{height}" viewBox="0 0 340 150" fill="none" xmlns="http://www.w3.org/2000/svg" style="display: block; margin: 0 auto; filter: drop-shadow(0 8px 24px rgba(46,42,37,0.12));">
        <defs>
            <linearGradient id="ringGoldGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#E5DED2"/>
                <stop offset="30%" stop-color="#D4AF37"/>
                <stop offset="70%" stop-color="#F3E7C5"/>
                <stop offset="100%" stop-color="#AA820A"/>
            </linearGradient>
            <linearGradient id="ringBronzeGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#D4AF37"/>
                <stop offset="50%" stop-color="#AA820A"/>
                <stop offset="100%" stop-color="#5A4005"/>
            </linearGradient>
            <linearGradient id="ringSilverGrad" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#FFFFFF"/>
                <stop offset="50%" stop-color="#C5BEB3"/>
                <stop offset="100%" stop-color="#8B857C"/>
            </linearGradient>
        </defs>
        <!-- Top Three Interlocking Sculpted Rings -->
        <circle cx="80" cy="55" r="46" stroke="url(#ringGoldGrad)" stroke-width="8" stroke-linecap="round"/>
        <circle cx="170" cy="55" r="46" stroke="url(#ringBronzeGrad)" stroke-width="8.5" stroke-linecap="round"/>
        <circle cx="260" cy="55" r="46" stroke="url(#ringSilverGrad)" stroke-width="8" stroke-linecap="round"/>
        <!-- Bottom Two Interlocking Sculpted Rings -->
        <circle cx="125" cy="95" r="46" stroke="url(#ringBronzeGrad)" stroke-width="8.2" stroke-linecap="round"/>
        <circle cx="215" cy="95" r="46" stroke="url(#ringGoldGrad)" stroke-width="8.2" stroke-linecap="round"/>
    </svg>"""


def get_olympia_flame_shader_svg() -> str:
    """Returns the SVG filter definition for procedural fluid heat-haze distortion."""
    return """
    <svg style="position: absolute; width: 0; height: 0;" aria-hidden="true">
        <filter id="olympia-flame-shader" x="-20%" y="-20%" width="140%" height="140%">
            <feTurbulence type="fractalNoise" baseFrequency="0.02 0.09" numOctaves="3" seed="2" result="noise">
                <animate attributeName="baseFrequency" values="0.02 0.09; 0.03 0.14; 0.02 0.09" dur="3.5s" repeatCount="indefinite" />
            </feTurbulence>
            <feDisplacementMap in="SourceGraphic" in2="noise" scale="8" xChannelSelector="R" yChannelSelector="G" />
        </filter>
    </svg>
    """


def get_olympia_modular_logo(variant: str = "horizontal", width: int = 220, height: int = 50) -> str:
    """
    Returns the 4-element modular OLYMPIA logo lockup with procedural fluid flame shader:
    1. Procedural flame with feTurbulence filter
    2. Sculpted Olympic rings
    3. Classical serif wordmark
    4. Subtitle metadata
    """
    from dashboard.components.theme import get_olympia_logo
    return get_olympia_logo(variant=variant, width=width, height=height)


def get_3d_astrolabe_rings_svg(width: int = 340, height: int = 150) -> str:
    """Returns the 3D Gyroscopic Astrolabe Olympic Rings."""
    from dashboard.components.kinetic_engine import get_3d_astrolabe_rings_html
    return get_3d_astrolabe_rings_html(width=width, height=height)


def get_isometric_olap_cube_widget(active_op: str = "slice") -> str:
    """Returns the Interactive 3D CSS Isometric Data Cube widget."""
    from dashboard.components.kinetic_engine import render_isometric_3d_olap_cube
    return render_isometric_3d_olap_cube(active_op=active_op)


def get_star_schema_blueprint_widget(counts: dict | None = None) -> str:
    """Returns the Interactive SVG Star Schema Blueprint widget."""
    from dashboard.components.kinetic_engine import render_star_schema_blueprint_html
    return render_star_schema_blueprint_html(counts=counts)




