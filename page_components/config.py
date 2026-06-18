"""
Configuration settings for the Dash app.
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._config_utils import year_support



CONFIG_SETTINGS = {
    # ───── ───── ───── ───── ───── ───── ─────
    # Calendar years for which the Dash app
    # will support.
    # ───── ───── ───── ───── ───── ───── ─────
    'YEARS': year_support(),
}