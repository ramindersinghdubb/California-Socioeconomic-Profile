"""
Tooltip metadata interface for the 'Employment Statistics' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class EmploymentStatisticsTooltip(TooltipFigureMetaABC, measure = 'Employment Statistics'):
    """
    Tooltip metadata interface for the 'Employment Statistics' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Unemploy. Rate by Racial Status': cls.UnemployRatebyRacialStatus,
            'LFPR by Racial Status': cls.LFPRbyRacialStatus,
            'EPOP Ratio by Racial Status': cls.EPOPRatiobyRacialStatus,
            'Unemploy. Rate by Sexual Orientation': cls.UnemployRatebySexualOrientation,
            'LFPR by Sexual Orientation': cls.LFPRbySexualOrientation,
            'EPOP Ratio by Sexual Orientation': cls.EPOPRatiobySexualOrientation,
            'Unemploy. Rate by Educational Attainment': cls.UnemployRatebyEducationalAttainment,
            'LFPR by Educational Attainment': cls.LFPRbyEducationalAttainment,
            'EPOP Ratio by Educational Attainment': cls.EPOPRatiobyEducationalAttainment,
        }
        return lambda_dict

        
    
    @classmethod
    def UnemployRatebyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def LFPRbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def EPOPRatiobyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def UnemployRatebySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def LFPRbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def EPOPRatiobySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def UnemployRatebyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def LFPRbyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)



    @classmethod
    def EPOPRatiobyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2301 (full availability)







# NOTE:
# All years for the LFPR, EPOP, and UR are percentages.
# This includes years prior to 2015. Thus, just hunt for
# these variables and make the appropriate long-format df.