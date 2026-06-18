"""
Place and year dropdowns.
"""
import typing as t

import pandas as pd
from dash import html

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._config_utils import get_topic_dict
from ingestion.config import CONFIG_SETTINGS as INGESTION_CONFIG_SETTINGS
from page_components.config import CONFIG_SETTINGS as APP_CONFIG_SETTINGS



def get_dependent_year_place_dropdown_options() -> t.Tuple[t.Dict, t.Dict]:
    """
    Get the dropdown options corresponding to:
        - The place dropdown options,
        - The year dropdown options

    Note that this set of dropdown options are mutually interdependent
    (i.e. a given year has a corresponding list of place options, and
    vice versa).
    """

    CONFIG_YEARS = APP_CONFIG_SETTINGS['YEARS']

    plc_file = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'place_metadata.csv'
    df = pd.read_csv(plc_file)
    all_plcs = df['PLACENAME'].unique().tolist()

    YEAR_PLACE_OPTIONS = dict()
    for year in CONFIG_YEARS:
        support_plcs = df[df['YEAR'] == year]['PLACENAME'].unique().tolist()
        YEAR_PLACE_OPTIONS[year] = [
            {
                'label': html.Span(
                    children = [plc],
                    style    = {'color': '#000000' if plc in support_plcs else '#C5C6C7'}
                ),
                'value': plc,
                'disabled': False if plc in support_plcs else True
            }
            for plc in all_plcs
        ]

    PLACE_YEAR_OPTIONS = dict()
    for place in all_plcs:
        support_yrs = df[df['PLACENAME'] == place]['YEAR'].unique().tolist()
        PLACE_YEAR_OPTIONS[place] = [
            {
                'label': html.Span(
                    children = [i],
                    style    = {'color': '#000000' if i in support_yrs else '#C5C6C7'}
                ),
                'value': i,
                'disabled': False if i in support_yrs else True
            }
            for i in CONFIG_YEARS
        ]

    return YEAR_PLACE_OPTIONS, PLACE_YEAR_OPTIONS



def get_dependent_year_measure_dropdown_options() -> t.Tuple[t.Dict, t.Dict]:
    """
    Get the dropdown options corresponding to:
        - The measure dropdown options,
        - The year dropdown options

    Note that this set of dropdown options are mutually interdependent
    (i.e. a given year has a corresponding list of measure options, and
    vice versa).
    """

    CONFIG_YEARS = APP_CONFIG_SETTINGS['YEARS']

    topic_dict = get_topic_dict()

    MEASURE_YEAR_OPTIONS = dict()
    for topic, support_yrs in topic_dict.items():
        MEASURE_YEAR_OPTIONS[topic] = [
            {
                'label': html.Span(
                    children = [yr],
                    style    = {'color': '#000000' if yr in support_yrs else '#C5C6C7'}
                ),
                'value': yr,
                'disabled': False if yr in support_yrs else True
            }
            for yr in CONFIG_YEARS
        ]

    YEAR_MEASURE_OPTIONS = dict()
    for yr in CONFIG_YEARS:
        YEAR_MEASURE_OPTIONS[yr] = [
            {
                'label': html.Span(
                    children = [tpc],
                    style    = {'color': '#000000' if yr in support_yrs else '#C5C6C7'}
                ),
                'value': tpc,
                'disabled': False if yr in support_yrs else True
            }
            for tpc, support_yrs in topic_dict.items()
        ]

    return YEAR_MEASURE_OPTIONS, MEASURE_YEAR_OPTIONS