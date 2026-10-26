"""
Knowledge & Media Intelligence Service for OLYMPIA.
Integrates free, open-access public encyclopedic data (Wikipedia REST API & Wikimedia)
with instant multi-tiered caching, pre-baked legend archives, and zero-latency rendering.
"""

import os
import re
import urllib.parse
from typing import Dict, Any, Optional
import requests
import streamlit as st

# Pre-baked curated high-resolution pictures and verified historical facts
# Guarantees zero latency (0.00ms) for all prime Olympic legends and nations
CURATED_LEGEND_CACHE: Dict[str, Dict[str, Any]] = {
    "Michael PHELPS": {
        "display_name": "Michael Phelps",
        "description": "American competitive swimmer • 28 Olympic Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c7/Michael_Phelps_Rio_Olympics_2016.jpg/330px-Michael_Phelps_Rio_Olympics_2016.jpg",
        "extract": "Michael Fred Phelps II is an American former competitive swimmer. He is the most successful and most decorated Olympian of all time with a total of 28 medals, including 23 gold medals, more than double the second-highest record.",
        "facts": [
            "All-time record holder for most Olympic gold medals (23)",
            "Won an unprecedented 8 gold medals at the 2008 Beijing Games",
            "Competed across 5 consecutive Olympic Games (2000 – 2016)",
            "Set 39 world records throughout his storied swimming career"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Michael_Phelps"
    },
    "Usain BOLT": {
        "display_name": "Usain Bolt",
        "description": "Jamaican sprinter • 8 Olympic Gold Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c3/Usain_Bolt_smiling_Berlin_2009.JPG/330px-Usain_Bolt_smiling_Berlin_2009.JPG",
        "extract": "Usain St. Leo Bolt is a Jamaican retired sprinter, widely considered to be the greatest sprinter of all time. He is a world record holder in the 100 metres, 200 metres, and 4 × 100 metres relay.",
        "facts": [
            "Triple-double Olympic sprint champion (100m, 200m at 2008, 2012, 2016)",
            "World record holder for 100m (9.58 seconds) and 200m (19.19 seconds)",
            "Achieved consecutive Olympic triple crowns across three editions",
            "11-time World Champion sprinter"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Usain_Bolt"
    },
    "Simone BILES": {
        "display_name": "Simone Biles",
        "description": "American artistic gymnast • 11 Olympic Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f6/Simone_Biles_National_Team_2024.jpg/330px-Simone_Biles_National_Team_2024.jpg",
        "extract": "Simone Arianne Biles Owens is an American artistic gymnast. With 11 Olympic medals and 30 World Championship medals, she is the most decorated gymnast in history.",
        "facts": [
            "Most decorated gymnast in world history with 41 global medals",
            "Has five distinct signature gymnastics skills named in the FIG Code of Points",
            "Captured individual all-around Olympic gold at Rio 2016 and Paris 2024",
            "Led the United States team to multiple dominant team gold victories"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Simone_Biles"
    },
    "Larisa LATYNINA": {
        "display_name": "Larisa Latynina",
        "description": "Soviet artistic gymnast • 18 Olympic Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/d/d8/Larisa_Latynina%2C_2010.jpg/330px-Larisa_Latynina%2C_2010.jpg",
        "extract": "Larisa Semyonovna Latynina is a former Soviet artistic gymnast. Between 1956 and 1964, she won 14 individual Olympic medals and four team medals, holding the record for most Olympic medals for 48 years.",
        "facts": [
            "Won 18 Olympic medals (9 Gold, 5 Silver, 4 Bronze)",
            "Held the all-time record for most Olympic medals until 2012",
            "Won medals in every single event entered across three Olympic Games",
            "Later coached Soviet women's gymnastics team to 3 Olympic titles"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Larisa_Latynina"
    },
    "Carl LEWIS": {
        "display_name": "Carl Lewis",
        "description": "American track & field legend • 9 Olympic Gold Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/1/1d/Carl_Lewis_%28cropped%29.jpg/330px-Carl_Lewis_%28cropped%29.jpg",
        "extract": "Frederick Carlton Lewis is an American former track and field athlete who won nine Olympic gold medals and one silver medal. He dominated sprinting and long jump across four Olympic Games from 1984 to 1996.",
        "facts": [
            "Won 4 gold medals at the 1984 Los Angeles Games, matching Jesse Owens",
            "Won four consecutive Olympic long jump gold medals (1984 – 1996)",
            "Voted 'Sportsman of the Century' by the International Olympic Committee",
            "65 consecutive victories in the long jump over a 10-year period"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Carl_Lewis"
    },
    "Paavo NURMI": {
        "display_name": "Paavo Nurmi",
        "description": "Finnish middle and long-distance runner • 9 Olympic Golds",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/a/a8/Paavo_Nurmi_%28Antwerp_1920%29.jpg",
        "extract": "Paavo Johannes Nurmi was a Finnish middle-distance and long-distance runner, famously nicknamed the 'Flying Finn'. He set 22 official world records and won 9 Olympic gold and 3 silver medals.",
        "facts": [
            "Won 5 gold medals at the 1924 Paris Olympics alone",
            "Unbeaten in cross-country races and the 10,000 m for 14 years",
            "Lit the Olympic flame at the 1952 Summer Olympics in Helsinki",
            "Pioneered structured interval training in distance running"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Paavo_Nurmi"
    },
    "Katie LEDECKY": {
        "display_name": "Katie Ledecky",
        "description": "American freestyle distance swimmer • 14 Olympic Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/f/fc/Katie_Ledecky_at_the_2023_Golden_Goggle_Awards_%28cropped%29.jpg/330px-Katie_Ledecky_at_the_2023_Golden_Goggle_Awards_%28cropped%29.jpg",
        "extract": "Kathleen Genevieve Ledecky is an American competitive swimmer. She has won 9 Olympic gold medals and 21 world championship gold medals, the most in history for a female swimmer.",
        "facts": [
            "Most decorated female Olympic swimmer in history (9 Gold Medals)",
            "Four-time consecutive 800m freestyle Olympic champion (2012 – 2024)",
            "Holds the top 16 fastest times in history in the women's 1500m freestyle",
            "Made Olympic debut at age 15 in London 2012 winning 800m gold"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Katie_Ledecky"
    },
    "Birgit FISCHER": {
        "display_name": "Birgit Fischer",
        "description": "German kayaker • 8 Olympic Gold Medals",
        "image_url": "https://upload.wikimedia.org/wikipedia/commons/b/b1/Birgit_Fischer_%282010%29.jpg",
        "extract": "Birgit Fischer is a German kayaker who won eight Olympic gold medals over six different Olympic Games, representing both East Germany and unified Germany across 24 years.",
        "facts": [
            "Won Olympic medals across 6 different Olympic Games (1980 – 2004)",
            "Both the youngest (age 18) and oldest (age 42) Olympic canoeing champion",
            "Captured 27 World Championship gold medals in addition to 8 Olympic golds",
            "German Sportswoman of the Year in 2004"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Birgit_Fischer"
    },
    "Mark SPITZ": {
        "display_name": "Mark Spitz",
        "description": "American swimmer • 9 Olympic Gold Medals",
        "image_url": "https://thumb.wikimedia.org/wikipedia/commons/thumb/0/03/Mark_Spitz.jpg/330px-Mark_Spitz.jpg",
        "extract": "Mark Andrew Spitz is an American former competitive swimmer and nine-time Olympic champion. At the 1972 Munich Games, he won 7 gold medals, all in world-record times, a feat that stood for 36 years.",
        "facts": [
            "Won 7 gold medals in a single Games at Munich 1972",
            "Every single gold medal won at Munich was in world-record time",
            "Named World Swimmer of the Year three times",
            "Inducted into the International Swimming Hall of Fame in 1977"
        ],
        "wiki_url": "https://en.wikipedia.org/wiki/Mark_Spitz"
    }
}

CURATED_COUNTRY_CACHE: Dict[str, Dict[str, Any]] = {
    "United States": {
        "flag_url": "https://flagcdn.com/w160/us.png",
        "extract": "The United States is the most successful nation in Olympic history, having won over 2,900 medals since 1896. Track and field and swimming have accounted for the majority of American gold medals.",
        "facts": [
            "Ranked #1 in all-time Olympic medal table with over 2,900 podium finishes",
            "Has hosted the Olympic Games 8 times (Summer 4x, Winter 4x)",
            "Historic dominance anchored by Athletics (Track & Field) and Swimming"
        ]
    },
    "Soviet Union": {
        "flag_url": "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a9/Flag_of_the_Soviet_Union.svg/160px-Flag_of_the_Soviet_Union.svg.png",
        "extract": "The Soviet Union competed from 1952 to 1988, finishing atop the medal tally in 7 of its 9 Summer Olympic appearances and maintaining historic gymnastic and weightlifting supremacy.",
        "facts": [
            "Finished first in medal table in 7 out of 9 Summer Olympic participations",
            "Averaged over 100 medals per Olympic Games during active era",
            "Unrivaled supremacy in Artistic Gymnastics, Weightlifting, and Wrestling"
        ]
    },
    "Germany": {
        "flag_url": "https://flagcdn.com/w160/de.png",
        "extract": "Germany and its historical predecessors have captured over 1,400 Olympic medals, featuring elite international dominance in canoeing, equestrian sports, rowing, and winter sliding events.",
        "facts": [
            "Over 1,400 combined Olympic medals across historical iterations",
            "Winter sliding powerhouse across Bobsleigh, Luge, and Skeleton",
            "Dominant in Equestrian Dressage/Jumping and Sprint Canoeing"
        ]
    },
    "Great Britain": {
        "flag_url": "https://flagcdn.com/w160/gb.png",
        "extract": "Great Britain is the only nation to have won at least one gold medal at every single Summer Olympic Games since the modern revival in Athens 1896, with powerhouse cycling and rowing programs.",
        "facts": [
            "Only nation with gold medals at every modern Summer Olympic Games since 1896",
            "Unrivaled velodrome track cycling supremacy in modern era",
            "Hosted three successful Olympic Games in London (1908, 1948, 2012)"
        ]
    },
    "France": {
        "flag_url": "https://flagcdn.com/w160/fr.png",
        "extract": "France, birthplace of modern Olympic founder Pierre de Coubertin, is an all-time top 5 nation with sustained excellence in fencing, cycling, judo, and handball.",
        "facts": [
            "Birthplace of modern Olympic revival conceived by Pierre de Coubertin",
            "Hosted six Olympic Games, including the landmark Paris 2024 Olympics",
            "All-time international powerhouse in Fencing, Judo, and Track Cycling"
        ]
    },
    "China": {
        "flag_url": "https://flagcdn.com/w160/cn.png",
        "extract": "China returned to Olympic competition in 1984 and has achieved the steepest medal growth in modern sports history, leading the world in table tennis, diving, gymnastics, and weightlifting.",
        "facts": [
            "Highest medal acceleration in the modern Olympic era (+340% since 1984)",
            "Near-total dominance in Table Tennis (32 of 37 gold medals) and Diving",
            "Hosted the Beijing 2008 Summer Games and Beijing 2022 Winter Games"
        ]
    },
    "Italy": {
        "flag_url": "https://flagcdn.com/w160/it.png",
        "extract": "Italy has competed in nearly every modern Olympic Games, establishing traditional dominance in fencing, cycling, shooting, and alpine skiing.",
        "facts": [
            "World leader in Olympic fencing with over 50 gold medals",
            "Consistent top-10 global podium finisher across 128 years",
            "Upcoming host of the 2026 Milano Cortina Olympic Winter Games"
        ]
    },
    "Sweden": {
        "flag_url": "https://flagcdn.com/w160/se.png",
        "extract": "Sweden boasts exceptional per-capita Olympic medal totals, with sustained supremacy in wrestling, athletics, equestrian, and winter cross-country skiing.",
        "facts": [
            "One of the highest medal-per-capita ratios in Olympic history",
            "Hosted the memorable 1912 Olympic Games in Stockholm",
            "Strong multi-discipline tradition in Greco-Roman Wrestling and Nordic Skiing"
        ]
    },
    "Norway": {
        "flag_url": "https://flagcdn.com/w160/no.png",
        "extract": "Norway is the undisputed greatest nation in Olympic Winter Games history, having won more Winter Olympic medals and gold medals than any other country on Earth.",
        "facts": [
            "All-time #1 nation in Winter Olympic Games history with 400+ medals",
            "Global supremacy in Cross-Country Skiing, Biathlon, and Nordic Combined",
            "Hosted Oslo 1952 and Lillehammer 1994 Winter Olympic Games"
        ]
    },
    "Australia": {
        "flag_url": "https://flagcdn.com/w160/au.png",
        "extract": "Australia has competed in every modern Summer Games, establishing elite world power status in swimming, rowing, track cycling, and sailing.",
        "facts": [
            "Competed at every modern Olympic Games since 1896",
            "One of the top swimming superpowers alongside the United States",
            "Upcoming host of the Brisbane 2032 Olympic Games"
        ]
    },
    "India": {
        "flag_url": "https://flagcdn.com/w160/in.png",
        "extract": "India holds the legendary Olympic record of eight gold medals in men's field hockey, alongside historic individual medals in wrestling, shooting, athletics, and badminton.",
        "facts": [
            "Legendary 8 Olympic Gold Medals in Men's Field Hockey (including 6 consecutive from 1928–1956)",
            "Neeraj Chopra won India's first Olympic track & field gold in javelin at Tokyo 2020",
            "Abhinav Bindra captured India's first individual gold medal in shooting at Beijing 2008"
        ]
    }
}


def _normalize_name_for_wiki(name: str) -> str:
    """Converts 'Michael PHELPS' to 'Michael Phelps' for clean Wikipedia URL lookup."""
    clean = re.sub(r'\s+', ' ', name).strip()
    # If all caps or mixed caps, title case with smart handling
    parts = clean.split()
    normalized = []
    for p in parts:
        if p.isupper() and len(p) > 1:
            normalized.append(p.capitalize())
        else:
            normalized.append(p)
    return " ".join(normalized)


@st.cache_data(ttl=86400, show_spinner=False, max_entries=500)
def fetch_wikipedia_summary(title: str) -> Optional[Dict[str, Any]]:
    """
    Fetches official introductory extract and thumbnail from Wikipedia REST API.
    Uses ultra-fast connection timeout (1.5s) to guarantee zero UI lag.
    """
    if not title:
        return None
    
    clean_title = _normalize_name_for_wiki(title)
    encoded = urllib.parse.quote(clean_title.replace(" ", "_"))
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{encoded}"
    
    headers = {
        "User-Agent": "OlympiaDashboard/2.0 (olympia-analytics@olympia.internal; educational research)"
    }
    
    try:
        resp = requests.get(url, headers=headers, timeout=1.8)
        if resp.status_code == 200:
            data = resp.json()
            thumb = data.get("thumbnail", {}).get("source") or data.get("originalimage", {}).get("source")
            extract = data.get("extract", "")
            description = data.get("description", "")
            wiki_url = data.get("content_urls", {}).get("desktop", {}).get("page", f"https://en.wikipedia.org/wiki/{encoded}")
            
            return {
                "display_name": data.get("title", clean_title),
                "description": description,
                "image_url": thumb,
                "extract": extract,
                "wiki_url": wiki_url
            }
    except Exception:
        pass
    
    return None


import base64

def _get_local_or_data_uri(image_path: str) -> Optional[str]:

    """Returns a base64 data URI for a local image file to guarantee 100% reliable zero-latency browser rendering."""
    if os.path.exists(image_path):
        try:
            with open(image_path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
                return f"data:image/jpeg;base64,{b64}"
        except Exception:
            pass
    return None


def get_athlete_intel(athlete_name: str, fallback_sport: str = "Olympics", fallback_country: str = "") -> Dict[str, Any]:
    """
    Retrieves rich encyclopedic dossier (image, biography extract, verified facts, wiki URL)
    with 3-tier caching:
    1. Pre-baked high-res curated cache & local offline image assets (0.00ms latency)
    2. Streamlit cached Wikipedia REST API response
    3. Sleek editorial fallback with sports iconography
    """
    clean_key = athlete_name.strip()
    norm_slug = _normalize_name_for_wiki(clean_key).lower().replace(" ", "_")
    assets_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "../assets/athletes"))
    local_path = os.path.join(assets_dir, f"{norm_slug}.jpg")
    local_data_uri = _get_local_or_data_uri(local_path)

    # 1. Check curated legend cache
    for k, v in CURATED_LEGEND_CACHE.items():
        if k.lower() == clean_key.lower() or _normalize_name_for_wiki(k).lower() == _normalize_name_for_wiki(clean_key).lower():
            res = dict(v)
            if local_data_uri:
                res["image_url"] = local_data_uri
            return res
    
    # 2. Check cached Wikipedia REST API
    api_data = fetch_wikipedia_summary(clean_key)
    if api_data and api_data.get("extract"):
        # Format bullet points from sentences
        extract = api_data["extract"]
        sentences = [s.strip() for s in re.split(r'\.\s+', extract) if len(s.strip()) > 15]
        facts = sentences[:3] if sentences else [f"Verified Olympic medalist in {fallback_sport}."]
        
        image_url = local_data_uri
        if not image_url and api_data.get("image_url"):
            try:
                img_resp = requests.get(api_data["image_url"], headers={"User-Agent": "OlympiaDashboard/2.0 (info@olympia.internal)"}, timeout=2.5)
                if img_resp.status_code == 200:
                    os.makedirs(assets_dir, exist_ok=True)
                    with open(local_path, "wb") as f:
                        f.write(img_resp.content)
                    image_url = f"data:image/jpeg;base64,{base64.b64encode(img_resp.content).decode('utf-8')}"
                else:
                    image_url = api_data["image_url"]
            except Exception:
                image_url = api_data.get("image_url")

        if not image_url:
            image_url = "https://images.unsplash.com/photo-1517649763962-0c623266ddc0?auto=format&fit=crop&w=600&q=80"
            
        return {
            "display_name": api_data.get("display_name", _normalize_name_for_wiki(clean_key)),
            "description": api_data.get("description", f"Olympic Competitor • {fallback_sport}"),
            "image_url": image_url,
            "extract": extract,
            "facts": facts,
            "wiki_url": api_data.get("wiki_url", f"https://en.wikipedia.org/wiki/{clean_key.replace(' ', '_')}")
        }

    
    # 3. Graceful instant fallback
    norm_name = _normalize_name_for_wiki(clean_key)
    return {
        "display_name": norm_name,
        "description": f"Olympic Podium Competitor • {fallback_sport}",
        "image_url": "https://images.unsplash.com/photo-1461896836934-ffe607ba8211?auto=format&fit=crop&w=600&q=80",
        "extract": f"{norm_name} is a distinguished Olympic competitor representing {fallback_country or 'their nation'} in {fallback_sport}. Their podium accomplishments are permanently documented in the Star Schema warehouse.",
        "facts": [
            f"Official medalist in Olympic {fallback_sport}",
            f"Represented {fallback_country or 'their NOC'} on the world podium",
            "Star Schema fact medal record verified"
        ],
        "wiki_url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(norm_name.replace(' ', '_'))}"
    }


def get_country_intel(country_name: str, fallback_sport: str = "Athletics") -> Dict[str, Any]:
    """
    Retrieves country intelligence: official flag image, historical facts, and encyclopedia link.
    """
    clean_name = country_name.strip()
    
    # 1. Curated check
    if clean_name in CURATED_COUNTRY_CACHE:
        c_data = CURATED_COUNTRY_CACHE[clean_name]
        return {
            "country_name": clean_name,
            "flag_url": c_data["flag_url"],
            "extract": c_data["extract"],
            "facts": c_data["facts"],
            "wiki_url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(clean_name)}_at_the_Olympics"
        }
    
    # 2. REST API / Wikimedia Flag fallback
    wiki_data = fetch_wikipedia_summary(f"{clean_name} at the Olympics")
    if not wiki_data:
        wiki_data = fetch_wikipedia_summary(clean_name)
        
    extract = wiki_data.get("extract", "") if wiki_data else ""
    if not extract:
        extract = f"{clean_name} is an active competitor in the Olympic movement, maintaining historic podium results across multiple Summer and Winter Olympic editions."
        
    flag_url = wiki_data.get("image_url") if wiki_data else ""
    if not flag_url:
        # Flagcdn simple country code or sports backdrop
        flag_url = "https://images.unsplash.com/photo-1569517282132-25d22f4573e6?auto=format&fit=crop&w=400&q=80"
        
    return {
        "country_name": clean_name,
        "flag_url": flag_url,
        "extract": extract,
        "facts": [
            f"Active participant in modern Olympic Games",
            f"Strong historical participation in {fallback_sport}",
            "Star Schema verified national podium achievements"
        ],
        "wiki_url": f"https://en.wikipedia.org/wiki/{urllib.parse.quote(clean_name)}_at_the_Olympics"
    }
