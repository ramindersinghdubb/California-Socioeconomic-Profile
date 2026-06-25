"""
Tooltip metadata interface for the 'Food Stamps' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class FoodStampsTooltip(TooltipFigureMetaABC, measure = 'Food Stamps'):
    """
    Tooltip metadata interface for the 'Food Stamps' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Food Stamps Recipiency by Racial Status': cls.FoodStampsRecipiencybyRacialStatus,
            'Food Stamps Recipiency by Poverty Status': cls.FoodStampsRecipiencybyPovertyStatus,
            'Food Stamps Recipiency by Disability Status': cls.FoodStampsRecipiencybyDisabilityStatus,
            'Food Stamps Recipiency by Working Status': cls.FoodStampsRecipiencybyWorkingStatus,
        }
        return lambda_dict

        
    
    @classmethod
    def FoodStampsRecipiencybyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def FoodStampsRecipiencybyPovertyStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def FoodStampsRecipiencybyDisabilityStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def FoodStampsRecipiencybyWorkingStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




