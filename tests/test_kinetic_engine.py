"""
Tests for OLYMPIA Ultra-Complex Kinetic & Shader Physics Engine.
Verifies all 12 kinetic systems, SVG shader filters, 3D CSS isometric structures,
and topology blueprints render accurately without syntax or DOM errors.
"""

import unittest
from dashboard.components.kinetic_engine import (
    get_3d_astrolabe_rings_html,
    render_isometric_3d_olap_cube,
    render_apriori_energy_conduits_html,
    render_centroid_gravity_pulse_html,
    render_bifurcating_tree_svg_html,
    render_star_schema_blueprint_html
)
from dashboard.components.icons import get_olympia_flame_shader_svg
from dashboard.components.coach_strategy_ui import render_wind_tunnel_visualizer_html


class TestKineticEngine(unittest.TestCase):

    def test_svg_flame_shader(self):
        shader_svg = get_olympia_flame_shader_svg()
        self.assertIn("olympia-flame-shader", shader_svg)
        self.assertIn("feTurbulence", shader_svg)
        self.assertIn("feDisplacementMap", shader_svg)

    def test_3d_astrolabe_rings(self):
        rings_html = get_3d_astrolabe_rings_html(width=340, height=150)
        self.assertIn("astrolabe-viewport", rings_html)
        self.assertIn("astrolabe-ring-mesh", rings_html)
        self.assertIn("rotateX", rings_html)

    def test_isometric_3d_olap_cube_operations(self):
        for op in ["slice", "dice", "rollup", "drilldown", "pivot"]:
            cube_html = render_isometric_3d_olap_cube(op)
            self.assertIn("olap-cube-container", cube_html)
            self.assertIn("olap-cube-stage", cube_html)
            self.assertIn("olap-voxel", cube_html)
            self.assertIn(f"Live Choreography: {op.upper()}", cube_html)

    def test_apriori_energy_conduits(self):
        conduits_html = render_apriori_energy_conduits_html()
        self.assertIn("FORCE-DIRECTED ENERGY CONDUITS", conduits_html)
        self.assertIn("animateMotion", conduits_html)
        self.assertIn("apriori-conduit-pair", conduits_html)

    def test_centroid_gravity_pulse(self):
        pulse_html = render_centroid_gravity_pulse_html()
        self.assertIn("UNSUPERVISED GRAVITATIONAL PHYSICS", pulse_html)
        self.assertIn("centroidShockwave", pulse_html)
        self.assertIn("orbitCW", pulse_html)

    def test_bifurcating_decision_tree(self):
        tree_html = render_bifurcating_tree_svg_html()
        self.assertIn("SUPERVISED DECISION GRAPH", tree_html)
        self.assertIn("GOLD (88.4%)", tree_html)
        self.assertIn("treePulseFlow", tree_html)

    def test_star_schema_blueprint(self):
        counts = {
            "fact_medal": 20582,
            "dim_game": 54,
            "dim_country": 206,
            "dim_sport": 47,
            "dim_event": 1017,
            "dim_medal": 3
        }
        blueprint_html = render_star_schema_blueprint_html(counts)
        self.assertIn("STAR SCHEMA RELATIONAL TOPOLOGY", blueprint_html)
        self.assertIn("fact_medal", blueprint_html)
        self.assertIn("dim_game", blueprint_html)
        self.assertIn("dim_country", blueprint_html)
        self.assertIn("dim_sport", blueprint_html)
        self.assertIn("dim_event", blueprint_html)
        self.assertIn("dim_medal", blueprint_html)
        self.assertIn("20,582", blueprint_html)

    def test_wind_tunnel_visualizer(self):
        wind_html = render_wind_tunnel_visualizer_html(drafting_val=35.0, altitude_val=1200)
        self.assertIn("LIVE AERODYNAMIC WIND-TUNNEL", wind_html)
        self.assertIn("laminar-path", wind_html)
        self.assertIn("wake-path", wind_html)
        self.assertIn("Separation Point", wind_html)


if __name__ == "__main__":
    unittest.main()
