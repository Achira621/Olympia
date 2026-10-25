"""
Streamlit Community Cloud standard entrypoint for OLYMPIA.
Delegates directly to dashboard/app.py.
"""

import os
import sys
import runpy

ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

dashboard_script = os.path.join(ROOT_DIR, "dashboard", "app.py")
runpy.run_path(dashboard_script, run_name="__main__")
