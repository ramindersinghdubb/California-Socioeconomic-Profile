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



class DropdownInterface:
    """
    Interface for handling the formatting and retrieving of dropdown options.
    """

    @classmethod
    def get_place_options(
        cls,
        year: t.Optional[int] = None
    ) -> t.List[t.Dict[str, t.Any]]:
        """
        Get the options for the place dropdown.

        Note that these options are directly enforced by the calendar year.

        Parameters
        ----------
        year
            The selected calendar year.
        """
        place_df = cls.__get_place_metadata_df()

        all_plcs = place_df['PLACENAME'].unique().tolist()
        support_plcs = place_df[place_df['YEAR'] == year]['PLACENAME'].unique().tolist()

        options = [
            {
                'label': html.Span(
                    children = [plc if plc in support_plcs else f'{plc} (UNAVAILABLE)'],
                    style    = {'color': '#000000' if plc in support_plcs else '#C5C6C7'}
                ),
                'value': plc,
                'disabled': False if plc in support_plcs else True
            } for plc in all_plcs
        ]

        return options


    @classmethod
    def get_year_options(
        cls,
        place: t.Optional[str] = None,
        measure: t.Optional[str] = None
    ) -> t.List[t.Dict[str, t.Any]]:
        """
        Get the options for the year dropdown.

        Note that these options are jointly enforced by the selected place *and* the
        selected measure.

        Parameters
        ----------
        place
            The selected place/city.

        measure
            The selected measure
        """
        config_years = APP_CONFIG_SETTINGS['YEARS']

        inputed_place   = bool(place is not None)
        inputed_measure = bool(measure is not None)

        if inputed_place and not inputed_measure:
            options = cls.__get_year_options_from_place(place, config_years)
        
        if inputed_measure and not inputed_place:
            options = cls.__get_year_options_from_measure(measure, config_years)

        if inputed_measure and inputed_place:
            p_options = cls.__get_year_options_from_place(place, config_years)
            m_options = cls.__get_year_options_from_measure(measure, config_years)

            m_yrs = {i['value']: i['disabled'] for i in m_options}
            p_yrs = {i['value']: i['disabled'] for i in p_options}

            options = [
                {
                    **i,
                    'disabled': True if any(j[i['value']] for j in [m_yrs,p_yrs]) else False
                }
                for i in p_options
            ]

            options = [
                {
                    **i,
                    'label': html.Span(
                        children = [str(i['value']) if not i['disabled'] else f'{i['value']} (UNAVAILABLE)'],
                        style    = {'color': '#000000' if not i['disabled'] else '#C5C6C7'}
                    ),
                } for i in options
            ]

        return options


    @classmethod
    def get_measure_options(
        cls,
        year: t.Optional[int] = None
    ) -> t.List[t.Dict[str, t.Any]]:
        """
        Get the options for the measure dropdown.

        Note that these options are directly enforced by the calendar year.

        Parameters
        ----------
        year
            The selected calendar year.
        """
        topic_dict = get_topic_dict()
        options    = [
            {
                'label': html.Span(
                    children = [tpc if year in support_yrs else f'{tpc} (UNAVAILABLE)'],
                    style    = {'color': '#000000' if year in support_yrs else '#C5C6C7'}
                ),
                'value': tpc,
                'disabled': False if year in support_yrs else True
            }
            for tpc, support_yrs in topic_dict.items()
        ]

        return options

    
    @classmethod
    def __get_year_options_from_measure(
        cls, measure: str, config_years: t.List[int]
    ) -> t.List[t.Dict[str, t.Any]]:
        """
        From the indicated measure, retrieve the set of available years from the list
        of configuration years in-file for that specific measure.
        """
        topic_dict = get_topic_dict()
        years = topic_dict.get(measure)
        options = [
            {
                'label': html.Span(
                    children = [str(yr) if yr in years else f'{yr} (UNAVAILABLE)'],
                    style    = {'color': '#000000' if yr in years else '#C5C6C7'}
                ),
                'value': yr,
                'disabled': False if yr in years else True
            }
            for yr in config_years
        ]
        return options



    @classmethod
    def __get_year_options_from_place(
        cls, place: str, config_years: t.List[int]
    ) -> t.List[t.Dict[str, t.Any]]:
        """
        From the indicated place, retrieve the set of available years from the list
        of configuration years in-file for that specific place.
        """
        place_df = cls.__get_place_metadata_df()
        years = place_df[place_df['PLACENAME'] == place]['YEAR'].unique().tolist()
        options = [
            {
                'label': html.Span(
                    children = [str(yr) if yr in years else f'{yr} (UNAVAILABLE)'],
                    style    = {'color': '#000000' if yr in years else '#C5C6C7'}
                ),
                'value': yr,
                'disabled': False if yr in years else True
            }
            for yr in config_years
        ]
        return options



    @classmethod
    def __get_place_metadata_df(cls) -> pd.DataFrame:
        plc_file = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'place_metadata.csv'
        df = pd.read_csv(plc_file)
        return df