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

    years = APP_CONFIG_SETTINGS['YEAR']

    dropdown_config_file = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'place_metadata.csv'
    df = pd.read_csv(dropdown_config_file)
    df['PLACEVALUE'] = df['PLACENAME'].str.replace(' ', '')

    YEAR_PLACE_OPTIONS = {
        year: [
            {'label': html.Span([i], style = {'color': '#151E3D'}), 'value': j}
            for i, j in zip(list(df['PLACENAME'][df['YEAR'] == year]), list(df['PLACEVALUE'][df['YEAR'] == year]))
        ] for year in years
    }

    PLACE_YEAR_OPTIONS = dict()
    """
    Place -> Year dropdown options
    """
    for place in list(set(df['PLACEVALUE'])):
        yrs = [i for i in df['YEAR'][df['PLACEVALUE'] == place] if i in years]
        PLACE_YEAR_OPTIONS[place] = [
            {'label': html.Span([i], style = {'color': '#000000'}), 'value': i}
            for i in yrs
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

    years = APP_CONFIG_SETTINGS['YEAR']

    topic_dict = get_topic_dict()

    MEASURE_YEAR_OPTIONS = dict()
    for topic, yrs in topic_dict.items():
        MEASURE_YEAR_OPTIONS[topic.replace(' ', '')] = [
            {'label': html.Span([i], style = {'color': '#000000'}), 'value': i}
            for i in yrs if i in years
        ]

    YEAR_MEASURE_OPTIONS = dict()
    for yr in years:
        YEAR_MEASURE_OPTIONS[yr] = [
            {'label': html.Span([i], style = {'color': '#000000'}), 'value': i.replace(' ', '')}
            for i, j in topic_dict.items() if yr in j
        ]

    return YEAR_MEASURE_OPTIONS, MEASURE_YEAR_OPTIONS