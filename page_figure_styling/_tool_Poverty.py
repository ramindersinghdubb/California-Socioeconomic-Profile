"""
Tooltip metadata interface for the 'Poverty' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class PovertyTooltip(TooltipFigureMetaABC, measure = 'Poverty'):
    """
    Tooltip metadata interface for the 'Poverty' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Poverty Status by Racial Status': cls.PovertyStatusbyRacialStatus,
            'Poverty Status by Sexual Orientation': cls.PovertyStatusbySexualOrientation,
            'Poverty Status by Age': cls.PovertyStatusbyAge,
            'Poverty Status by Employment Status': cls.PovertyStatusbyEmploymentStatus,
        }
        return lambda_dict

        
    
    @classmethod
    def PovertyStatusbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1701 (full availability)



    @classmethod
    def PovertyStatusbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1701 (full availability)



    @classmethod
    def PovertyStatusbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1701 (full availability)



    @classmethod
    def PovertyStatusbyEmploymentStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1701 (full availability)




