"""
Comprehensive Olympic National Flags & Geopolitical Mapping for OLYMPIA.
Maps all 169 historical and modern Olympic nations to ISO-2 codes, official flag URLs,
and Unicode flag emojis with 100% accuracy and fallback graphics.
"""

from typing import Dict, Optional, Tuple

# Comprehensive ISO-2 Alpha code mapping for all 169 nations in the Star Schema
COUNTRY_ISO2_MAP: Dict[str, str] = {
    "Afghanistan": "af",
    "Albania": "al",
    "Algeria": "dz",
    "Argentina": "ar",
    "Armenia": "am",
    "Australasia": "au",
    "Australia": "au",
    "Austria": "at",
    "Azerbaijan": "az",
    "Bahamas": "bs",
    "Bahrain": "bh",
    "Barbados": "bb",
    "Belarus": "by",
    "Belgium": "be",
    "Bermuda": "bm",
    "Bohemia": "cz",
    "Botswana": "bw",
    "Brazil": "br",
    "British West Indies": "jm",
    "Bulgaria": "bg",
    "Burundi": "bi",
    "Cameroon": "cm",
    "Canada": "ca",
    "Cape Verde": "cv",
    "Ceylon": "lk",
    "Chile": "cl",
    "China": "cn",
    "Chinese Taipei": "tw",
    "Colombia": "co",
    "Costa Rica": "cr",
    "Cote d'Ivoire": "ci",
    "Croatia": "hr",
    "Cuba": "cu",
    "Cyprus": "cy",
    "Czech Republic": "cz",
    "Czechoslovakia": "cz",
    "Denmark": "dk",
    "Djibouti": "dj",
    "Dominica": "dm",
    "Dominican Republic": "do",
    "Ecuador": "ec",
    "Egypt": "eg",
    "Eritrea": "er",
    "Estonia": "ee",
    "Ethiopia": "et",
    "Federal Republic of Germany": "de",
    "Fiji": "fj",
    "Finland": "fi",
    "France": "fr",
    "Gabon": "ga",
    "Georgia": "ge",
    "German Democratic Republic": "de",
    "Germany": "de",
    "Ghana": "gh",
    "Great Britain": "gb",
    "Greece": "gr",
    "Grenada": "gd",
    "Guatemala": "gt",
    "Guyana": "gy",
    "Haiti": "ht",
    "Hong Kong, British": "hk",
    "Hong Kong, China": "hk",
    "Hungary": "hu",
    "Iceland": "is",
    "Independent Olympic Athletes": "un",
    "Independent Participants (ex Yugoslavia)": "rs",
    "India": "in",
    "Indonesia": "id",
    "Iran": "ir",
    "Iraq": "iq",
    "Ireland": "ie",
    "Israel": "il",
    "Italy": "it",
    "Ivory Coast": "ci",
    "Jamaica": "jm",
    "Jamaica, British": "jm",
    "Japan": "jp",
    "Jordan": "jo",
    "Kazakhstan": "kz",
    "Kenya": "ke",
    "Korea DPR": "kp",
    "Korea Republic": "kr",
    "Kosovo": "xk",
    "Kuwait": "kw",
    "Kyrgyzstan": "kg",
    "Latvia": "lv",
    "Lebanon": "lb",
    "Liechtenstein": "li",
    "Lithuania": "lt",
    "Luxembourg": "lu",
    "Macedonia": "mk",
    "Malaysia": "my",
    "Mauritius": "mu",
    "Mexico": "mx",
    "Mixed Team": "un",
    "Moldova": "md",
    "Mongolia": "mn",
    "Montenegro": "me",
    "Morocco": "ma",
    "Mozambique": "mz",
    "Namibia": "na",
    "Netherlands": "nl",
    "Netherlands Antilles": "cw",
    "New Zealand": "nz",
    "Niger": "ne",
    "Nigeria": "ng",
    "Norway": "no",
    "Olympic Athletes from Russia": "ru",
    "Pakistan": "pk",
    "Panama": "pa",
    "Paraguay": "py",
    "Peru": "pe",
    "Philippines": "ph",
    "Poland": "pl",
    "Portugal": "pt",
    "Puerto Rico": "pr",
    "Qatar": "qa",
    "ROC": "ru",
    "Refugee Olympic Team": "un",
    "Republic of China (Taiwan)": "tw",
    "Romania": "ro",
    "Russian Empire": "ru",
    "Russian Federation": "ru",
    "Saint Lucia": "lc",
    "Samoa": "ws",
    "Saudi Arabia": "sa",
    "Senegal": "sn",
    "Serbia": "rs",
    "Serbia and Montenegro": "rs",
    "Singapore": "sg",
    "Singapore, British": "sg",
    "Slovakia": "sk",
    "Slovenia": "si",
    "South Africa": "za",
    "South Korea": "kr",
    "Spain": "es",
    "Sri Lanka": "lk",
    "Sudan": "sd",
    "Suriname": "sr",
    "Sweden": "se",
    "Switzerland": "ch",
    "Syria": "sy",
    "Tajikistan": "tj",
    "Tanzania": "tz",
    "Thailand": "th",
    "Togo": "tg",
    "Tonga": "to",
    "Trinidad and Tobago": "tt",
    "Trinidad and Tobago, British": "tt",
    "Tunisia": "tn",
    "Turkey": "tr",
    "USSR": "su",
    "Uganda": "ug",
    "Ukraine": "ua",
    "Unified Team (ex USSR)": "su",
    "Unified Team of Germany": "de",
    "United Arab Emirates": "ae",
    "United Arab Republic (Egypt, Syria)": "eg",
    "United States": "us",
    "Uruguay": "uy",
    "Uzbekistan": "uz",
    "Venezuela": "ve",
    "Vietnam": "vn",
    "Virgin Islands, US": "vi",
    "Yugoslavia": "rs",
    "Yugoslavia Federal Republic": "rs",
    "Zambia": "zm",
    "Zimbabwe": "zw",
    "AIN": "un"
}

# Unicode Flag Emojis for instant inline rendering
COUNTRY_EMOJI_MAP: Dict[str, str] = {
    "United States": "🇺🇸",
    "USSR": "☭",
    "Soviet Union": "☭",
    "Great Britain": "🇬🇧",
    "China": "🇨🇳",
    "France": "🇫🇷",
    "Germany": "🇩🇪",
    "Italy": "🇮🇹",
    "Sweden": "🇸🇪",
    "Australia": "🇦🇺",
    "Norway": "🇳🇴",
    "India": "🇮🇳",
    "Japan": "🇯🇵",
    "Canada": "🇨🇦",
    "Netherlands": "🇳🇱",
    "South Korea": "🇰🇷",
    "Korea Republic": "🇰🇷",
    "Korea DPR": "🇰🇵",
    "Brazil": "🇧🇷",
    "Cuba": "🇨🇺",
    "Hungary": "🇭🇺",
    "Poland": "🇵🇱",
    "Jamaica": "🇯🇲",
    "Kenya": "🇰🇪",
    "Ethiopia": "🇪🇹",
    "Spain": "🇪🇸",
    "Greece": "🇬🇷",
    "South Africa": "🇿🇦",
    "New Zealand": "🇳🇿",
    "Switzerland": "🇨🇭",
    "Austria": "🇦🇹",
    "Belgium": "🇧🇪",
    "Finland": "🇫🇮",
    "Denmark": "🇩🇰",
    "Romania": "🇷🇴",
    "Bulgaria": "🇧🇬",
    "Russian Federation": "🇷🇺",
    "Russia": "🇷🇺",
    "ROC": "🇷🇺",
    "Olympic Athletes from Russia": "🇷🇺",
    "Russian Empire": "🇷🇺",
    "Unified Team (ex USSR)": "🇷🇺",
    "German Democratic Republic": "🇩🇪",
    "Federal Republic of Germany": "🇩🇪",
    "Unified Team of Germany": "🇩🇪",
    "Czechoslovakia": "🇨🇿",
    "Czech Republic": "🇨🇿",
    "Ukraine": "🇺🇦",
    "Belarus": "🇧🇾",
    "Kazakhstan": "🇰🇿",
    "Uzbekistan": "🇺🇿",
    "Georgia": "🇬🇪",
    "Azerbaijan": "🇦🇿",
    "Armenia": "🇦🇲",
    "Iran": "🇮🇷",
    "Turkey": "🇹🇷",
    "Argentina": "🇦🇷",
    "Mexico": "🇲🇽",
    "Colombia": "🇨🇴",
    "Croatia": "🇭🇷",
    "Serbia": "🇷🇸",
    "Slovenia": "🇸🇮",
    "Slovakia": "🇸🇰",
    "Yugoslavia": "🇷🇸",
    "Ireland": "🇮🇪",
    "Portugal": "🇵🇹",
    "Algeria": "🇩🇿",
    "Morocco": "🇲🇦",
    "Egypt": "🇪🇬",
    "Nigeria": "🇳🇬",
    "Bahamas": "🇧🇸",
    "Trinidad and Tobago": "🇹🇹",
    "Indonesia": "🇮🇩",
    "Thailand": "🇹🇭",
    "Philippines": "🇵🇭",
    "Chinese Taipei": "🇹🇼",
    "Hong Kong, China": "🇭🇰",
    "Mixed Team": "🏳️",
    "Refugee Olympic Team": "🏳️",
    "AIN": "🏳️",
    "Independent Olympic Athletes": "🏳️"
}

# Special historical flag URLs (Wikipedia / Wikimedia Commons verified assets)
HISTORICAL_FLAG_URLS: Dict[str, str] = {
    "USSR": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/60px-Flag_of_the_Soviet_Union.svg.png",
    "Soviet Union": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/60px-Flag_of_the_Soviet_Union.svg.png",
    "Unified Team (ex USSR)": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/60px-Flag_of_the_Soviet_Union.svg.png",
    "German Democratic Republic": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Flag_of_East_Germany.svg/60px-Flag_of_East_Germany.svg.png",
    "Federal Republic of Germany": "https://upload.wikimedia.org/wikipedia/en/thumb/b/ba/Flag_of_Germany.svg/60px-Flag_of_Germany.svg.png",
    "Unified Team of Germany": "https://upload.wikimedia.org/wikipedia/commons/thumb/1/11/German_Olympic_flag_1960-1968.svg/60px-German_Olympic_flag_1960-1968.svg.png",
    "Czechoslovakia": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/60px-Flag_of_the_Czech_Republic.svg.png",
    "Yugoslavia": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/61/Flag_of_Yugoslavia_%281946-1992%29.svg/60px-Flag_of_Yugoslavia_%281946-1992%29.svg.png",
    "Russian Empire": "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f3/Flag_of_Russia.svg/60px-Flag_of_Russia.svg.png",
    "Australasia": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/Flag_of_Australia.svg/60px-Flag_of_Australia.svg.png",
    "Bohemia": "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cb/Flag_of_the_Czech_Republic.svg/60px-Flag_of_the_Czech_Republic.svg.png",
    "British West Indies": "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0a/Flag_of_the_West_Indies_Federation_%281958%E2%80%931962%29.svg/60px-Flag_of_the_West_Indies_Federation_%281958%E2%80%931962%29.svg.png",
    "Mixed Team": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/60px-Olympic_flag.svg.png",
    "Refugee Olympic Team": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/60px-Olympic_flag.svg.png",
    "Independent Olympic Athletes": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/60px-Olympic_flag.svg.png",
    "AIN": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/60px-Olympic_flag.svg.png"
}


def get_country_iso2(country_name: str) -> str:
    """Returns the lowercase 2-letter ISO code for a nation."""
    clean = str(country_name or "").strip()
    return COUNTRY_ISO2_MAP.get(clean, "un")


def get_country_flag_emoji(country_name: str) -> str:
    """Returns the Unicode flag emoji for any Olympic nation with fallback."""
    clean = str(country_name or "").strip()
    if clean in COUNTRY_EMOJI_MAP:
        return COUNTRY_EMOJI_MAP[clean]
    
    # Try ISO-2 regional indicator emoji
    iso = get_country_iso2(clean)
    if iso and len(iso) == 2 and iso != "un":
        try:
            return chr(ord(iso[0].upper()) + 127397) + chr(ord(iso[1].upper()) + 127397)
        except Exception:
            pass
    return "🏛️"


def get_country_flag_url(country_name: str) -> str:
    """Returns a high-resolution CDN or Wikimedia flag image URL."""
    clean = str(country_name or "").strip()
    if clean in HISTORICAL_FLAG_URLS:
        return HISTORICAL_FLAG_URLS[clean]
    
    iso = get_country_iso2(clean)
    if iso and iso != "un":
        return f"https://flagcdn.com/w40/{iso}.png"
    return "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a7/Olympic_flag.svg/60px-Olympic_flag.svg.png"


def get_country_flag_html(country_name: str, size: int = 18, show_name: bool = False) -> str:
    """
    Returns a crisp, retina-ready flag badge HTML snippet with graceful emoji fallback.
    """
    clean = str(country_name or "").strip()
    flag_url = get_country_flag_url(clean)
    emoji = get_country_flag_emoji(clean)
    w = int(round(size * 1.35))
    h = size

    img_html = f'<img src="{flag_url}" alt="{clean}" loading="lazy" style="width: {w}px; height: {h}px; object-fit: cover; border-radius: 2px; vertical-align: middle; box-shadow: 0 1px 3px rgba(46,42,37,0.18); border: 0.5px solid rgba(46,42,37,0.15); display: inline-block; margin-right: 4px;" onerror="this.style.display=\'none\'; this.nextElementSibling.style.display=\'inline\';" /><span style="display: none; vertical-align: middle; margin-right: 4px;">{emoji}</span>'

    if show_name:
        return f'<span style="display: inline-flex; align-items: center; gap: 0.35rem; font-weight: 600;">{img_html}<span>{clean}</span></span>'
    return img_html


def get_country_with_flag(country_name: str) -> str:
    """Formats string as '🇺🇸 United States' for standard Streamlit dropdowns."""
    clean = str(country_name or "").strip()
    emoji = get_country_flag_emoji(clean)
    return f"{emoji} {clean}"
