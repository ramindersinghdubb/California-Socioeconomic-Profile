"""
Utility functions for the configuration settings.
"""
import json
import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from ingestion.config import CONFIG_SETTINGS


def year_support(
    years: t.Optional[t.List[int]] = None
) -> t.List[int]:
    """
    Retrieve the calendar year support for places in California.

    Note that if `years` is specified, it will return itself back as it will
    implicitly assumes the user wishes only for these years. Otherwise, it
    will look in the configuration settings and return all supported years.
    """
    if years is not None:
        return years
    
    else:
        dropdown_config_file = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'place_metadata.csv'
        df = pd.read_csv(dropdown_config_file)
        years = df['YEAR'].unique().tolist()
        return years



def get_topic_dict() -> dict[str, list[int]]:
    """
    Get the look-up table/dictionary such that keys represent the user-defined
    topics/categories, and the values represent a list of calendar years over
    which each topic/category is supported.
    """
    config_folder = CONFIG_SETTINGS.get('CONFIGURATION_FOLDER')
    tpc_file      = Path(config_folder) / 'dropdown_config.json'
    with open(tpc_file, 'r') as file:
        TOPIC_DICT = json.load(file)

    return TOPIC_DICT