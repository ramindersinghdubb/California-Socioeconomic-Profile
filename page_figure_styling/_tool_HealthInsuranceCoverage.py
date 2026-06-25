"""
Tooltip metadata interface for the 'Health Insurance Coverage' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class HealthInsuranceCoverageTooltip(TooltipFigureMetaABC, measure = 'Health Insurance Coverage'):
    """
    Tooltip metadata interface for the 'Health Insurance Coverage' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Uninsured Individuals by Racial Status': cls.UninsuredIndividualsbyRacialStatus,
            'Uninsured Individuals by Sexual Orientation': cls.UninsuredIndividualsbySexualOrientation,
            'Uninsured Individuals by Citizenship Status': cls.UninsuredIndividualsbyCitizenshipStatus,
            'Uninsured Individuals by Educational Attainment': cls.UninsuredIndividualsbyEducationalAttainment,
        }
        return lambda_dict

        
    
    @classmethod
    def UninsuredIndividualsbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def UninsuredIndividualsbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def UninsuredIndividualsbyCitizenshipStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def UninsuredIndividualsbyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




