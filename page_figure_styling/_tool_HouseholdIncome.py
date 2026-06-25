"""
Tooltip metadata interface for the 'Household Income' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class HouseholdIncomeTooltip(TooltipFigureMetaABC, measure = 'Household Income'):
    """
    Tooltip metadata interface for the 'Household Income' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Income Distribution (Households)': cls.IncomeDistributionHouseholds,
            'Income Distribution (Families)': cls.IncomeDistributionFamilies,
            'Income Distribution (Married Couples)': cls.IncomeDistributionMarriedCouples,
            'Income Distribution (Nonfamily Households)': cls.IncomeDistributionNonfamilyHouseholds,
        }
        return lambda_dict

        
    
    @classmethod
    def IncomeDistributionHouseholds(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1901 (full availability)



    @classmethod
    def IncomeDistributionFamilies(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1901 (full availability)



    @classmethod
    def IncomeDistributionMarriedCouples(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1901 (full availability)



    @classmethod
    def IncomeDistributionNonfamilyHouseholds(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S1901 (full availability)




