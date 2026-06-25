"""
Tooltip metadata interface for the 'Rent Burden' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class RentBurdenTooltip(TooltipFigureMetaABC, measure = 'Rent Burden'):
    """
    Tooltip metadata interface for the 'Rent Burden' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Rent Burden and Severe Rent Burden': cls.RentBurdenandSevereRentBurden,
            'Rent Burden by Age': cls.RentBurdenbyAge,
            'Rent Burden by Income': cls.RentBurdenbyIncome,
        }
        return lambda_dict

        
    
    @classmethod
    def RentBurdenandSevereRentBurden(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def RentBurdenbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def RentBurdenbyIncome(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




