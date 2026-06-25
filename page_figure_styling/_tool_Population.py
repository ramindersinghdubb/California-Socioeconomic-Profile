"""
Tooltip metadata interface for the 'Population' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class PopulationTooltip(TooltipFigureMetaABC, measure = 'Population'):
    """
    Tooltip metadata interface for the 'Population' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Population by Age': cls.PopulationbyAge,
            'Population by Racial Status': cls.PopulationbyRacialStatus,
        }
        return lambda_dict

        
    
    @classmethod
    def PopulationbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def PopulationbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




