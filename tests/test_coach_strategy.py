"""
Unit tests for Coach Strategy and Athlete Inclination Analytics Engine.
"""

import unittest
from analytics.coach_strategy import (
    compute_athlete_inclinations,
    simulate_tactical_matchup,
    simulate_pacing_strategy,
    TACTICAL_ARCHETYPES
)


class TestCoachStrategy(unittest.TestCase):

    def test_compute_athlete_inclinations(self):
        """Verify inclination scoring, archetypes, and fatigue drift."""
        profile = compute_athlete_inclinations("Johannes Høsflot Klæbo", "Cross Country Skiing", medals_won=10, gold_ratio=0.8)
        self.assertIn("radar_scores", profile)
        self.assertEqual(len(profile["radar_scores"]), 6)
        for val in profile["radar_scores"].values():
            self.assertTrue(0 <= val <= 100)

        self.assertIn(profile["archetype"], TACTICAL_ARCHETYPES)
        self.assertEqual(len(profile["split_velocity_pct"]), 4)
        self.assertEqual(len(profile["error_chances"]), 4)
        self.assertGreater(profile["composite_rating"], 50)
        self.assertGreater(profile["clutch_index"], 50)

    def test_simulate_tactical_matchup(self):
        """Verify head-to-head tactical matchup modeling."""
        p_a = compute_athlete_inclinations("Johannes Høsflot Klæbo", "Cross Country Skiing", medals_won=10, gold_ratio=0.8)
        p_b = compute_athlete_inclinations("Federico Pellegrino", "Cross Country Skiing", medals_won=3, gold_ratio=0.2)

        matchup = simulate_tactical_matchup(p_a, p_b)
        self.assertIn("win_probability", matchup)
        self.assertTrue(0 <= matchup["win_probability"] <= 100)
        self.assertAlmostEqual(matchup["win_probability"] + matchup["opponent_win_prob"], 100.0, places=1)
        self.assertGreater(len(matchup["coach_directives"]), 0)
        self.assertGreater(len(matchup["opponent_weaknesses"]), 0)

    def test_simulate_pacing_strategy(self):
        """Verify race execution pacing simulation and energy depletion curve."""
        profile = compute_athlete_inclinations("Jordan Stolz", "Speed skating", medals_won=4, gold_ratio=0.75)
        sim = simulate_pacing_strategy(
            profile,
            pacing_strategy="Negative Split",
            energy_burn_rate=80.0,
            drafting_pct=35.0,
            altitude_factor=1000.0
        )
        self.assertIn("energy_curve", sim)
        self.assertEqual(len(sim["energy_curve"]), 5)  # Start + 4 splits
        # Energy should deplete monotonically
        for i in range(len(sim["energy_curve"]) - 1):
            self.assertGreaterEqual(sim["energy_curve"][i], sim["energy_curve"][i+1])

        self.assertTrue(0 <= sim["podium_probability"] <= 100)
        self.assertEqual(len(sim["split_speeds"]), 4)
        self.assertGreater(sim["drafting_savings_pct"], 0)


if __name__ == "__main__":
    unittest.main()
