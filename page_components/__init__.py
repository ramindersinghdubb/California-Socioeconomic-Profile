"""
`dash` HTML/styling components for the app.
"""


import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._app_layout import DashLayout
from page_components._off_canvas import OffCanvasText
from page_components._submeasures_options import submeasures_dict
from page_components._dropdowns import (
    get_dependent_year_measure_dropdown_options,
    get_dependent_year_place_dropdown_options
)
from page_components._colors import (
    get_continuous_color_dict,
    get_discrete_color_dict
)


__all__ = [
    'DashLayout',
    'OffCanvasText',
    'get_continuous_color_dict',
    'get_discrete_color_dict',
    'get_dependent_year_measure_dropdown_options',
    'get_dependent_year_place_dropdown_options',
    'submeasures_dict',
]