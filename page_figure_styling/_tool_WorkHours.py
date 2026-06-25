"""
Tooltip metadata interface for the 'Work Hours' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class WorkHoursTooltip(TooltipFigureMetaABC, measure = 'Work Hours'):
    """
    Tooltip metadata interface for the 'Work Hours' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Usual Hours Worked Weekly': cls.UsualHoursWorkedWeekly,
            'Average Hours Worked Weekly': cls.AverageHoursWorkedWeekly,
        }
        return lambda_dict

        
    
    @classmethod
    def UsualHoursWorkedWeekly(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2303 (full availability)



    @classmethod
    def AverageHoursWorkedWeekly(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S2303 (full availability)




