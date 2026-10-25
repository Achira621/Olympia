"""
Root entrypoint for OLYMPIA Olympic Analytics & Intelligence Platform.
Delegates to dashboard/app.py for 1-click cloud deployments on
Streamlit Community Cloud, Hugging Face Spaces, Render, and Railway.
"""

import os
import sys
import runpy

# Ensure root directory is on Python path
ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

dashboard_script = os.path.join(ROOT_DIR, "dashboard", "app.py")
runpy.run_path(dashboard_script, run_name="__main__")
