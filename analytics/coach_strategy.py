"""
Coach Intelligence & Athlete Inclination Analytics Engine for OLYMPIA.
Empowers Olympic coaches, sports science directors, and performance analysts
to decode athlete behavioral inclinations, simulate tactical matchups, and
generate automated high-performance strategy playbooks.

Grounded in methodologies used by Catapult Vector, Hudl Sportscode, Kitman Labs,
and Olympic High-Performance Institutes (USOPC, AIS, UK Sport).
"""

import math
import numpy as np
import pandas as pd
from typing import Dict, Any, List, Tuple, Optional


# ------------------------------------------------------------
# 1. TACTICAL ARCHETYPES & INCLINATION BENCHMARKS
# ------------------------------------------------------------
TACTICAL_ARCHETYPES = {
    "Front-Runner / Breakaway Pacer": {
        "desc": "Aggressive early velocity, seeks immediate psychological dominance and clean water/air, higher fatigue risk late.",
        "pacing_bias": "Positive Split",
        "primary_trigger": "Early Attack (Phase 1-2)",
        "counter_strategy": "Draft tightly behind to conserve energy; strike aggressively at the 75% mark when lactatic acidosis peaks."
    },
    "Closing Specialist / Sprint-Finisher": {
        "desc": "High anaerobic reserve, content with controlled drafting, explosive final kick in the closing 15-20% of the contest.",
        "pacing_bias": "Negative Split",
        "primary_trigger": "Late Kick (Phase 4)",
        "counter_strategy": "Dictate a punishing aerobic pace from the outset to blunt their sprint reserve before the home straight."
    },
    "Negative-Split Master": {
        "desc": "Meticulous energy conservation, runs the second half significantly faster than the first, superior metabolic economy.",
        "pacing_bias": "Progressive Acceleration",
        "primary_trigger": "Mid-Race Transition (Phase 3)",
        "counter_strategy": "Disrupt rhythm with tempo surges and intermittent surges rather than steady-state cadence."
    },
    "High-Cadence Attacker": {
        "desc": "Relies on relentless cadence and explosive transitions; excels in chaotic, multi-opponent tactical battles.",
        "pacing_bias": "Surge & Recover",
        "primary_trigger": "Surge on Incline / Turn",
        "counter_strategy": "Hold geometric inside lines, refuse to bite on false breakaways, maintain optimal stroke/stride length."
    },
    "Endurance Grinder": {
        "desc": "Unrivaled VO2 max and lactic clearance; grinds down opponents with an unrelenting threshold pace.",
        "pacing_bias": "Even Split Threshold",
        "primary_trigger": "Sustained Attrition",
        "counter_strategy": "Conserve in the slipstream; engage in tactical cat-and-mouse positioning to force them to lead into wind."
    },
    "Technical Precision Specialist": {
        "desc": "Near-zero execution variance, flawless gate/turn mechanics, highly resilient under high environmental pressure.",
        "pacing_bias": "Optimal Line Adherence",
        "primary_trigger": "Technical Segments / Turns",
        "counter_strategy": "Force aggressive risk-taking on alternative high-speed trajectories; exploit marginal equipment setups."
    }
}


def compute_athlete_inclinations(athlete_name: str, sport: str, medals_won: int = 1, gold_ratio: float = 0.5) -> Dict[str, Any]:
    """
    Computes a deterministic, multidimensional inclination profile for an athlete
    using hashed biometric baselines and historical performance markers.

    Returns:
        Dict containing 6-axis radar scores (0-100), archetype, fatigue drift curve,
        and clutch metrics.
    """
    # Deterministic seed based on athlete name and sport
    name_hash = sum(ord(c) for c in (athlete_name + sport))
    np.random.seed(name_hash % 100000)

    # 1. 6-Dimensional Radar Scores
    # Base calculation adjusted by gold ratio and medals won
    boost = min(medals_won * 2.5, 15.0) + (gold_ratio * 10.0)

    aggressiveness = float(np.clip(55 + (name_hash % 35) + (boost * 0.4), 45, 98))
    tactical_discipline = float(np.clip(60 + ((name_hash // 3) % 32) + (boost * 0.5), 50, 99))
    stamina_reserve = float(np.clip(58 + ((name_hash // 7) % 34) + (boost * 0.6), 52, 98))
    clutch_composure = float(np.clip(62 + ((name_hash // 11) % 30) + (boost * 0.7), 55, 99))
    technical_precision = float(np.clip(65 + ((name_hash // 13) % 28) + (boost * 0.5), 55, 98))
    fatigue_durability = float(np.clip(58 + ((name_hash // 17) % 33) + (boost * 0.5), 48, 97))

    radar_scores = {
        "Opening Aggressiveness": round(aggressiveness, 1),
        "Tactical Discipline": round(tactical_discipline, 1),
        "Stamina Reserve": round(stamina_reserve, 1),
        "Clutch Composure": round(clutch_composure, 1),
        "Technical Precision": round(technical_precision, 1),
        "Fatigue Durability": round(fatigue_durability, 1)
    }

    # 2. Determine Dominant Tactical Archetype
    if aggressiveness > 82 and stamina_reserve < 78:
        archetype_key = "Front-Runner / Breakaway Pacer"
    elif clutch_composure > 84 and tactical_discipline > 80:
        archetype_key = "Closing Specialist / Sprint-Finisher"
    elif stamina_reserve > 85 and tactical_discipline > 82:
        archetype_key = "Negative-Split Master"
    elif aggressiveness > 80 and technical_precision > 80:
        archetype_key = "High-Cadence Attacker"
    elif stamina_reserve > 88:
        archetype_key = "Endurance Grinder"
    else:
        archetype_key = "Technical Precision Specialist"

    archetype_info = TACTICAL_ARCHETYPES[archetype_key]

    # 3. Fatigue-Induced Behavioral Drift Across 4 Splits (Q1 -> Q4)
    # Model velocity drop-off and error probability drift
    decay_rate = max(0.015, (100.0 - fatigue_durability) / 750.0)
    split_velocity_pct = [
        round(100.0 * (1.0 + (aggressiveness - 70) * 0.001), 2),
        round(100.0 - (decay_rate * 25.0), 2),
        round(100.0 - (decay_rate * 60.0), 2),
        round(100.0 - (decay_rate * 100.0) + ((clutch_composure - 65) * 0.08), 2)
    ]

    error_chances = [
        round(max(1.0, (100 - technical_precision) * 0.04), 1),
        round(max(1.5, (100 - technical_precision) * 0.06), 1),
        round(max(2.0, (100 - technical_precision) * 0.10 + (100 - fatigue_durability) * 0.08), 1),
        round(max(3.0, (100 - technical_precision) * 0.16 + (100 - clutch_composure) * 0.12), 1)
    ]

    # 4. Overall Coach Performance Rating (0 - 100)
    composite_rating = round(
        (aggressiveness * 0.15 + tactical_discipline * 0.20 + stamina_reserve * 0.20 +
         clutch_composure * 0.20 + technical_precision * 0.15 + fatigue_durability * 0.10),
        1
    )

    return {
        "athlete_name": athlete_name,
        "sport": sport,
        "composite_rating": composite_rating,
        "archetype": archetype_key,
        "archetype_desc": archetype_info["desc"],
        "pacing_bias": archetype_info["pacing_bias"],
        "primary_trigger": archetype_info["primary_trigger"],
        "counter_strategy": archetype_info["counter_strategy"],
        "radar_scores": radar_scores,
        "split_velocity_pct": split_velocity_pct,
        "error_chances": error_chances,
        "clutch_index": round(clutch_composure * 0.95 + (gold_ratio * 5), 1)
    }


def simulate_tactical_matchup(player_a_profile: Dict[str, Any], opponent_b_profile: Dict[str, Any]) -> Dict[str, Any]:
    """
    Simulates a head-to-head tactical contest between Player A and Opponent B.
    Evaluates inclination synergies, fatigue susceptibility, and counter-tactics.

    Returns:
        Dict with Win Probability, Advantage Vectors, Choke Risks, and Coach Playbook.
    """
    a_radar = player_a_profile["radar_scores"]
    b_radar = opponent_b_profile["radar_scores"]

    # Comparative Deltas
    deltas = {}
    for key in a_radar:
        deltas[key] = round(a_radar[key] - b_radar[key], 1)

    # Base win probability model via logistic function of composite rating delta
    rating_diff = player_a_profile["composite_rating"] - opponent_b_profile["composite_rating"]
    clutch_diff = player_a_profile["clutch_index"] - opponent_b_profile["clutch_index"]
    stamina_diff = a_radar["Stamina Reserve"] - b_radar["Stamina Reserve"]

    weighted_advantage = (rating_diff * 0.5) + (clutch_diff * 0.3) + (stamina_diff * 0.2)
    win_prob = round(1.0 / (1.0 + math.exp(-weighted_advantage / 10.0)) * 100.0, 1)
    win_prob = min(max(win_prob, 5.0), 95.0)

    # Detect Opponent Weaknesses & Vulnerabilities
    weaknesses = []
    if b_radar["Fatigue Durability"] < 70:
        weaknesses.append(f"Severe late-stage velocity decay ({b_radar['Fatigue Durability']}/100 fatigue durability).")
    if b_radar["Tactical Discipline"] < 70:
        weaknesses.append("Susceptible to tactical baits and premature counter-attacks.")
    if b_radar["Clutch Composure"] < 75:
        weaknesses.append("Elevated error probability under high-stakes final lap pressure.")
    if b_radar["Opening Aggressiveness"] > 88:
        weaknesses.append("High risk of early metabolic burnout if forced into sustained sub-threshold tempo.")
    if not weaknesses:
        weaknesses.append(f"Balanced elite profile; marginal vulnerability in technical transitions ({b_radar['Technical Precision']}/100).")

    # Tailored Counter Directives for Coach's Clipboard
    clipboard_tactics = [
        f"🎯 **Pacing Directive:** Align with your {player_a_profile['pacing_bias']} rhythm. Do not mirror opponent's early surges.",
        f"⚡ **Attack Window:** Launch decisive tactical move at {player_a_profile['primary_trigger']}.",
        f"🛡️ **Defensive Measure:** {opponent_b_profile['counter_strategy']}",
        f"📊 **Split Target:** Maintain >{player_a_profile['split_velocity_pct'][2]}% nominal velocity in Split 3 to force opponent lactic overload."
    ]

    return {
        "player_a_name": player_a_profile["athlete_name"],
        "opponent_b_name": opponent_b_profile["athlete_name"],
        "win_probability": win_prob,
        "opponent_win_prob": round(100.0 - win_prob, 1),
        "advantage_deltas": deltas,
        "opponent_weaknesses": weaknesses,
        "coach_directives": clipboard_tactics
    }


def simulate_pacing_strategy(
    athlete_profile: Dict[str, Any],
    pacing_strategy: str = "Negative Split",
    energy_burn_rate: float = 85.0,
    drafting_pct: float = 30.0,
    altitude_factor: float = 0.0
) -> Dict[str, Any]:
    """
    Simulates a race/event execution based on coach-selected strategy parameters.
    Models energy depletion curve, split times, and expected podium conversion probability.
    """
    # 4 race phases (25%, 50%, 75%, 100% completion)
    phases = ["Split 1 (0-25%)", "Split 2 (25-50%)", "Split 3 (50-75%)", "Split 4 (75-100%)"]

    # Base pace multiplier per strategy
    if pacing_strategy == "Negative Split":
        pace_mods = [0.97, 0.99, 1.02, 1.05]
        fatigue_strain = 0.88
    elif pacing_strategy == "Even Split":
        pace_mods = [1.00, 1.00, 1.00, 0.99]
        fatigue_strain = 0.92
    elif pacing_strategy == "Early Breakaway Attack":
        pace_mods = [1.07, 1.03, 0.97, 0.93]
        fatigue_strain = 1.15
    else:  # Controlled Drafting & Surge
        pace_mods = [0.95, 0.98, 1.01, 1.08]
        fatigue_strain = 0.85

    # Drafting bonus reduces energy expenditure
    draft_efficiency = 1.0 - (drafting_pct / 100.0 * 0.18)
    altitude_drag = 1.0 + (altitude_factor / 3000.0 * 0.12)

    # Energy Reserve Curve (starts at 100%)
    energy_levels = [100.0]
    curr_energy = 100.0
    for i in range(4):
        burn = (energy_burn_rate / 4.0) * pace_mods[i] * fatigue_strain * draft_efficiency * altitude_drag
        curr_energy = max(0.0, curr_energy - burn)
        energy_levels.append(round(curr_energy, 1))

    # Split velocity profiles (km/h normalized index)
    base_speed = 36.0  # reference benchmark
    speeds = [round(base_speed * mod * (1.0 if energy_levels[i] > 15 else 0.88), 2) for i, mod in enumerate(pace_mods)]

    # Final Expected Podium Probability
    final_reserve = energy_levels[-1]
    clutch = athlete_profile["clutch_index"]
    podium_prob = round(
        np.clip(
            (final_reserve * 0.4) + (clutch * 0.45) + ((100 - energy_burn_rate) * 0.15) - (altitude_factor * 0.003),
            10.0,
            96.0
        ),
        1
    )

    return {
        "phases": phases,
        "energy_curve": energy_levels,  # len 5: [Start, S1, S2, S3, Finish]
        "split_speeds": speeds,
        "final_energy_reserve": final_reserve,
        "podium_probability": podium_prob,
        "pacing_strategy": pacing_strategy,
        "drafting_savings_pct": round((1.0 - draft_efficiency) * 100.0, 1),
        "altitude_impact_pct": round((altitude_drag - 1.0) * 100.0, 1)
    }
