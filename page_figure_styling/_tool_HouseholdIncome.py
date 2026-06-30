"""
Tooltip metadata interface for the 'Household Income' category.
"""

import typing as t

import pandas as pd
import numpy as np

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
            'Income Distribution': cls.IncomeDistribution,
            # 'Income Distribution (Families)': cls.IncomeDistributionFamilies,
            # 'Income Distribution (Married Couples)': cls.IncomeDistributionMarriedCouples,
            # 'Income Distribution (Nonfamily Households)': cls.IncomeDistributionNonfamilyHouseholds,
        }
        return lambda_dict

        
    
    @classmethod
    def IncomeDistribution(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S1901 (full availability)
        # S1901_C01_002E to S1901_C01_011E (percent estimates; total is S1901_C01_001E)

        labs = cls.__get_labs()
        TOTAL_VAR = 'S1901_C01_001E'

        per_vars = cls.generate_variables('S1901_C01_', 2, 11)
        pop_vars = cls.generate_variables('POPULAT_S1901_C01_', 2, 11)

        for pop_var, per_var in zip(pop_vars, per_vars):
            df[pop_var] = df[per_var].mul(df[TOTAL_VAR], fill_value=np.nan).div(100, fill_value=np.nan).round(0)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)

        color_array = cls.__get_color_array()

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Income Distribution for Households</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': f"<b style='font-size:15px;'>Income ({year} Inflation-Adjusted USD)</b>",
                    'standoff': 15
                },
                'tickfont': {
                    'size': 9
                },
                
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Percentage of Households</b>",
                    'standoff': 15
                },
                'ticklabelstandoff': 5,
                'ticksuffix': '%'
            },
            'marker': {
                'color': color_array,
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', TOTAL_VAR],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Of <b>%{customdata[1]} households</b>, approximately <b style='color:#396F39;'>%{customdata[0]} households</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "(or <b style='color:#396F39;'>%{y}</b> of households) self-reported to belonging&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "in this income bracket."
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    # @classmethod
    # def IncomeDistributionFamilies(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S1901 (full availability)



    # @classmethod
    # def IncomeDistributionMarriedCouples(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S1901 (full availability)



    # @classmethod
    # def IncomeDistributionNonfamilyHouseholds(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S1901 (full availability)




    @classmethod
    def __get_labs(cls) -> t.List[str]:
        labs = [
            "Less than $10k",
            "$10k to 15.0k",
            "$15k to 25.0k",
            "$25k to 35.0k",
            "$35k to 50.0k",
            "$50k to 75.0k",
            "$75k to 100.0k",
            "$100k to 150.0k",
            "$150k to 200.0k",
            "$200k or more"
        ]

        return labs
    
    @classmethod
    def __get_color_array(cls) -> t.List[str]:
        color_array = [
            "#8BEF8B",
            "#7FDF7F",
            "#75CF75",
            "#6BC06B",
            "#61B061",
            "#57A257",
            "#4D944D",
            "#438243",
            "#396F39",
            "#2E4D2E",
        ]

        return color_array
