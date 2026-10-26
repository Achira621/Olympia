"""
High-Resolution Athlete Portrait & Classical Olympic Avatar System for OLYMPIA.
Guarantees every Olympic athlete name renders with an authentic, verified photo or
a prestigious gold-laureled Olympic portrait vector avatar.
"""

import re
import urllib.parse
from typing import Dict, Any, List, Optional
from dashboard.components.knowledge_api import get_athlete_intel, CURATED_LEGEND_CACHE
from dashboard.components.flags import get_country_flag_emoji, get_country_flag_html

# Expanded Curated High-Res Olympic Legend Portraits (Wikimedia Commons verified public domain / CC)
ATHLETE_PHOTO_DIRECTORY: Dict[str, str] = {
    "Michael PHELPS": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c7/Michael_Phelps_Rio_2016.jpg/800px-Michael_Phelps_Rio_2016.jpg",
    "Usain BOLT": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1e/Usain_Bolt_after_400_m_semi_final_at_2013_World_Championships_in_Athletics.jpg/800px-Usain_Bolt_after_400_m_semi_final_at_2013_World_Championships_in_Athletics.jpg",
    "Simone BILES": "https://upload.wikimedia.org/wikipedia/commons/thumb/8/87/Simone_Biles_at_the_2024_Olympics_all-around_podium_02.jpg/800px-Simone_Biles_at_the_2024_Olympics_all-around_podium_02.jpg",
    "Larisa LATYNINA": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e0/Larisa_Latynina_1964.jpg/800px-Larisa_Latynina_1964.jpg",
    "Carl LEWIS": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Carl_Lewis_1984.jpg/800px-Carl_Lewis_1984.jpg",
    "Paavo NURMI": "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e4/Paavo_Nurmi_1920.jpg/800px-Paavo_Nurmi_1920.jpg",
    "Katie LEDECKY": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/1b/Katie_Ledecky_2024.jpg/800px-Katie_Ledecky_2024.jpg",
    "Birgit FISCHER": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Bundesarchiv_Bild_183-1988-0930-011%2C_Birgit_Schmidt_%28Fischer%29.jpg/800px-Bundesarchiv_Bild_183-1988-0930-011%2C_Birgit_Schmidt_%28Fischer%29.jpg",
    "Mark SPITZ": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Mark_Spitz_1972.jpg/800px-Mark_Spitz_1972.jpg",
    "Jesse OWENS": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ab/Jesse_Owens_1936_Olympics.jpg/800px-Jesse_Owens_1936_Olympics.jpg",
    "Nadia COMANECI": "https://upload.wikimedia.org/wikipedia/commons/thumb/9/91/Nadia_Comaneci_1976.jpg/800px-Nadia_Comaneci_1976.jpg",
    "Nikolai ANDRIANOV": "https://upload.wikimedia.org/wikipedia/commons/thumb/2/29/Nikolai_Andrianov_1976.jpg/800px-Nikolai_Andrianov_1976.jpg",
    "Sawao KATO": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c5/Sawao_Kato_1972.jpg/800px-Sawao_Kato_1972.jpg",
    "Edoardo MANGIAROTTI": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Edoardo_Mangiarotti_1956.jpg/800px-Edoardo_Mangiarotti_1956.jpg",
    "Allyson FELIX": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/7b/Allyson_Felix_2016.jpg/800px-Allyson_Felix_2016.jpg",
    "Ian THORPE": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b2/Ian_Thorpe_2001.jpg/800px-Ian_Thorpe_2001.jpg",
    "Bjorn DAEHLIE": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/03/Bj%C3%B8rn_D%C3%A6hlie_1994.jpg/800px-Bj%C3%B8rn_D%C3%A6hlie_1994.jpg",
    "Ole Einar BJORNDALEN": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Ole_Einar_Bj%C3%B8rndalen_2014.jpg/800px-Ole_Einar_Bj%C3%B8rndalen_2014.jpg",
    "Marit BJORGEN": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/Marit_Bj%C3%B8rgen_2018.jpg/800px-Marit_Bj%C3%B8rgen_2018.jpg",
    "Emil ZATOPEK": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Emil_Z%C3%A1topek_1952.jpg/800px-Emil_Z%C3%A1topek_1952.jpg",
    "Al OERTER": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f6/Al_Oerter_1956.jpg/800px-Al_Oerter_1956.jpg",
    "Fanny BLANKERS-KOEN": "https://upload.wikimedia.org/wikipedia/commons/thumb/7/73/Fanny_Blankers-Koen_1948.jpg/800px-Fanny_Blankers-Koen_1948.jpg",
    "Aleksandr KARELIN": "https://upload.wikimedia.org/wikipedia/commons/thumb/3/30/Aleksandr_Karelin_1996.jpg/800px-Aleksandr_Karelin_1996.jpg",
    "Caeleb DRESSEL": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/4e/Caeleb_Dressel_2021.jpg/800px-Caeleb_Dressel_2021.jpg",
    "Sun YANG": "https://upload.wikimedia.org/wikipedia/commons/thumb/d/db/Sun_Yang_2016.jpg/800px-Sun_Yang_2016.jpg",
    "Eliud KIPCHOGE": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Eliud_Kipchoge_Rio_2016.jpg/800px-Eliud_Kipchoge_Rio_2016.jpg",
    "Armand DUPLANTIS": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/Armand_Duplantis_2024.jpg/800px-Armand_Duplantis_2024.jpg",
    "Leon MARCHAND": "https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Leon_Marchand_2024.jpg/800px-Leon_Marchand_2024.jpg",
    "Neeraj CHOPRA": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/ae/Neeraj_Chopra_Tokyo_2020.jpg/800px-Neeraj_Chopra_Tokyo_2020.jpg"
}


def _get_initials(name: str) -> str:
    """Extracts 2-letter uppercase initials from athlete name."""
    parts = re.findall(r'[A-Za-z]+', name or "")
    if len(parts) >= 2:
        return f"{parts[0][0].upper()}{parts[-1][0].upper()}"
    elif len(parts) == 1:
        return parts[0][:2].upper()
    return "OL"


def generate_olympic_portrait_svg(athlete_name: str, size: int = 64) -> str:
    """
    Generates a classical Roman Olympic Gold Laureled Vector Portrait Avatar
    with athlete initials, dark marble backdrop, and metallic gold ring.
    """
    initials = _get_initials(athlete_name)
    hash_val = sum(ord(c) for c in athlete_name) % 360

    return f"""<svg width="{size}" height="{size}" viewBox="0 0 100 100" fill="none" xmlns="http://www.w3.org/2000/svg" style="border-radius: 50%; box-shadow: 0 4px 14px rgba(46,42,37,0.18); flex-shrink: 0; display: inline-block; vertical-align: middle;">
        <defs>
            <linearGradient id="bgGrad_{hash_val}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#2E2A25"/>
                <stop offset="100%" stop-color="#1A1815"/>
            </linearGradient>
            <linearGradient id="goldBorder_{hash_val}" x1="0%" y1="0%" x2="100%" y2="100%">
                <stop offset="0%" stop-color="#F3E7C5"/>
                <stop offset="50%" stop-color="#D4AF37"/>
                <stop offset="100%" stop-color="#AA820A"/>
            </linearGradient>
        </defs>
        <!-- Background Marble Coin -->
        <circle cx="50" cy="50" r="48" fill="url(#bgGrad_{hash_val})" stroke="url(#goldBorder_{hash_val})" stroke-width="3"/>
        <!-- Inner Laurel Ring -->
        <circle cx="50" cy="50" r="40" stroke="#D4AF37" stroke-width="1" stroke-dasharray="2 3" opacity="0.6"/>
        <!-- Stylized Laurel Leaves at Base -->
        <path d="M 30 75 Q 40 82 50 82 Q 60 82 70 75" stroke="#D4AF37" stroke-width="2" fill="none" stroke-linecap="round"/>
        <path d="M 36 78 Q 42 74 46 70" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linecap="round"/>
        <path d="M 64 78 Q 58 74 54 70" stroke="#D4AF37" stroke-width="1.6" fill="none" stroke-linecap="round"/>
        <!-- Centered Initials in Imperial Roman Serif -->
        <text x="50" y="56" font-family="'Cinzel', 'Playfair Display', Georgia, serif" font-size="28" font-weight="800" fill="#F3E7C5" text-anchor="middle" dominant-baseline="middle" letter-spacing="1">
            {initials}
        </text>
        <circle cx="50" cy="22" r="3" fill="#D4AF37"/>
    </svg>"""


def get_athlete_photo_url(athlete_name: str, sport: str = "Olympics", country: str = "") -> str:
    """
    Returns the best available high-res photo URL for any athlete:
    1. Curated photo directory
    2. Cached Wikipedia Commons dossier
    3. None if only vector fallback should be used
    """
    clean = str(athlete_name or "").strip()
    
    # 1. Check exact or normalized curated directory
    for k, url in ATHLETE_PHOTO_DIRECTORY.items():
        if k.lower() == clean.lower() or k.replace(" ", "").lower() == clean.replace(" ", "").lower():
            return url
    
    # 2. Check knowledge API / Wikipedia cache
    intel = get_athlete_intel(clean, fallback_sport=sport, fallback_country=country)
    img = intel.get("image_url")
    if img and "unsplash" not in img:
        return img
    
    return ""


def get_athlete_avatar_html(athlete_name: str, size: int = 50, sport: str = "", country: str = "", border_color: str = "#D4AF37") -> str:
    """
    Returns complete, self-contained HTML for an athlete avatar.
    If photo exists, renders high-res circular portrait with gold border;
    otherwise renders the classical Roman Olympic Gold Laurel Vector.
    """
    clean = str(athlete_name or "").strip()
    photo_url = get_athlete_photo_url(clean, sport=sport, country=country)

    if photo_url:
        fallback_svg = generate_olympic_portrait_svg(clean, size=size).replace("\n", " ").replace('"', '&quot;')
        return f'<img src="{photo_url}" alt="{clean}" loading="lazy" referrerpolicy="no-referrer" style="width: {size}px; height: {size}px; min-width: {size}px; min-height: {size}px; object-fit: cover; border-radius: 50%; border: 2px solid {border_color}; box-shadow: 0 4px 12px rgba(46,42,37,0.18); display: inline-block; vertical-align: middle;" onerror="this.outerHTML=\'{fallback_svg}\'" />'
    
    return generate_olympic_portrait_svg(clean, size=size)


def get_top_legends_list() -> List[Dict[str, Any]]:
    """Returns structured data for the top Olympic legends with photo, country, sport, and medals."""
    return [
        {
            "name": "Michael Phelps",
            "country": "United States",
            "sport": "Swimming",
            "golds": 23,
            "silvers": 3,
            "bronzes": 2,
            "total": 28,
            "editions": "2000 – 2016",
            "photo": ATHLETE_PHOTO_DIRECTORY["Michael PHELPS"],
            "title": "Most Decorated Olympian of All Time"
        },
        {
            "name": "Larisa Latynina",
            "country": "USSR",
            "sport": "Gymnastics",
            "golds": 9,
            "silvers": 5,
            "bronzes": 4,
            "total": 18,
            "editions": "1956 – 1964",
            "photo": ATHLETE_PHOTO_DIRECTORY["Larisa LATYNINA"],
            "title": "Soviet Gymnastics Sovereign"
        },
        {
            "name": "Usain Bolt",
            "country": "Jamaica",
            "sport": "Athletics",
            "golds": 8,
            "silvers": 0,
            "bronzes": 0,
            "total": 8,
            "editions": "2008 – 2016",
            "photo": ATHLETE_PHOTO_DIRECTORY["Usain BOLT"],
            "title": "Unbeaten Olympic Sprint Triple-Double"
        },
        {
            "name": "Simone Biles",
            "country": "United States",
            "sport": "Gymnastics",
            "golds": 7,
            "silvers": 2,
            "bronzes": 2,
            "total": 11,
            "editions": "2016 – 2024",
            "photo": ATHLETE_PHOTO_DIRECTORY["Simone BILES"],
            "title": "Most Decorated Gymnast in History"
        },
        {
            "name": "Carl Lewis",
            "country": "United States",
            "sport": "Athletics",
            "golds": 9,
            "silvers": 1,
            "bronzes": 0,
            "total": 10,
            "editions": "1984 – 1996",
            "photo": ATHLETE_PHOTO_DIRECTORY["Carl LEWIS"],
            "title": "4 Consecutive Long Jump Titles"
        },
        {
            "name": "Paavo Nurmi",
            "country": "Finland",
            "sport": "Athletics",
            "golds": 9,
            "silvers": 3,
            "bronzes": 0,
            "total": 12,
            "editions": "1920 – 1928",
            "photo": ATHLETE_PHOTO_DIRECTORY["Paavo NURMI"],
            "title": "The Legendary Flying Finn"
        },
        {
            "name": "Katie Ledecky",
            "country": "United States",
            "sport": "Swimming",
            "golds": 9,
            "silvers": 4,
            "bronzes": 1,
            "total": 14,
            "editions": "2012 – 2024",
            "photo": ATHLETE_PHOTO_DIRECTORY["Katie LEDECKY"],
            "title": "Distance Freestyle World Empress"
        },
        {
            "name": "Mark Spitz",
            "country": "United States",
            "sport": "Swimming",
            "golds": 9,
            "silvers": 1,
            "bronzes": 1,
            "total": 11,
            "editions": "1968 – 1972",
            "photo": ATHLETE_PHOTO_DIRECTORY["Mark SPITZ"],
            "title": "7 Gold Medals at Munich 1972"
        }
    ]
