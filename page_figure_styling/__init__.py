"""
HTML/styling components for the `dash.dcc.Graph` figure.
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling.choropleth_metadata import ChoroplethMapInterface
from page_figure_styling.tooltip_figure import TooltipFigureInterface

__all__ = [
    'ChoroplethMapInterface',
    'TooltipFigureInterface',
]