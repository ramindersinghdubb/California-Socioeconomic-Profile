"""
Tooltip metadata interface for the 'Economic Measures' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class EconomicMeasuresTooltip(TooltipFigureMetaABC, measure = 'Economic Measures'):
    """
    Tooltip metadata interface for the 'Economic Measures' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Civilian Workforce by Industry': cls.CivilianWorkforcebyIndustry,
            'Civilian Workforce by Occupation': cls.CivilianWorkforcebyOccupation,
            'Civilian Workforce by Sector': cls.CivilianWorkforcebySector,
            'Median Earnings, All Workers by Industry': cls.MedianEarningsAllWorkersbyIndustry,
            'Median Earnings, Full-Time Workers by Industry': cls.MedianEarningsFullTimeWorkersbyIndustry,
            'Gender Pay Gap, All Workers': cls.GenderPayGapAllWorkers,
            'Gender Pay Gap, Full-Time Workers': cls.GenderPayGapFullTimeWorkers,
        }
        return lambda_dict

        
    
    @classmethod
    def CivilianWorkforcebyIndustry(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def CivilianWorkforcebyOccupation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def CivilianWorkforcebySector(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def MedianEarningsAllWorkersbyIndustry(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def MedianEarningsFullTimeWorkersbyIndustry(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def GenderPayGapAllWorkers(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def GenderPayGapFullTimeWorkers(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




