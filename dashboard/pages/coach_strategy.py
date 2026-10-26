"""
Coach Intelligence & Player Inclination Strategy Studio Page for OLYMPIA.
High-Performance Olympic Tactics, Opponent Scouting & Pacing Simulator.
"""

import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import streamlit as st
import pandas as pd
from warehouse.warehouse import get_denormalized_medals
from dashboard.components.coach_strategy_ui import render_coach_strategy_studio


def render_page(df: pd.DataFrame | None = None):
    if df is None:
        df = get_denormalized_medals()
    render_coach_strategy_studio(df)


if __name__ == "__main__":
    render_page()
