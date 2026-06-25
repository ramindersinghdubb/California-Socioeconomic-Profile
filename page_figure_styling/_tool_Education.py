"""
Tooltip metadata interface for the 'Education' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class EducationTooltip(TooltipFigureMetaABC, measure = 'Education'):
    """
    Tooltip metadata interface for the 'Education' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Educational Attainment by Citizenship Status': cls.EducationalAttainmentbyCitizenshipStatus,
            'Educational Attainment by Racial Status': cls.EducationalAttainmentbyRacialStatus,
            'Educational Attainment by Age': cls.EducationalAttainmentbyAge,
        }
        return lambda_dict

        
    
    @classmethod
    def EducationalAttainmentbyCitizenshipStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # Unavailable for only 2009 (B06009; has partial availability)



    @classmethod
    def EducationalAttainmentbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # Use C15002 tables (full availability)



    @classmethod
    def EducationalAttainmentbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # Use B15001 (full availability)



# TODO
# Consider by Educational Attainment by Sexual Orientation? (B15001, has full availability)



