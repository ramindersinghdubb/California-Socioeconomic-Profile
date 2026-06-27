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
        # B25070 (full availability)

        labs = ["Rent Burdened", "Severely Rent Burdened"]
        pop_vars = [f'{i} Population' for i in labs]
        per_vars = [f'{i} Percentage' for i in labs]
        
        Total    = 'B25070_001E'
        RB_cols  = cls.generate_variables('B25070_', 2, 10)
        SRB_cols = cls.generate_variables('B25070_', 10, 10)
        col_grps = [RB_cols, SRB_cols]

        for pop_col, per_col, cols in zip(pop_vars, per_vars, col_grps):
            df[per_col] = df[cols].sum(axis = 1).mul(100).div(df[Total]).round(2)
            df[pop_col] = df[cols].sum(axis = 1)
    
        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, Total)

        color_array = ['#FF160C', '#8B0000']

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Rent Burden and Severe Rent Burden</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Type of Rent Burden</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percentage of Renters (%)</b>",
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
            'custom_data': ['POPULATION', Total],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Of <b>%{customdata[1]} renters</b>, approximately <b>%{customdata[0]} renters</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "(or <b>%{y}</b> of renters) are <b style='color:#660000'>%{x}</b>."
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata


    @classmethod
    def RentBurdenbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # B25072 (full availability)

        labs = ['15 to 24', '25 to 34', '35 to 64', '65 and older']
        pop_vars = [f'{i} Population' for i in labs]
        per_vars = [f'{i} Percentage' for i in labs]
        tot_vars = []

        for percent_col, population_col, j in zip(per_vars, pop_vars, [2, 9, 16, 23]):
            RB_totl = 'B25072_' + str(j).zfill(3) + 'E'
            RB_cols = cls.generate_variables('B25072_', j + 4, j + 5)

            df[percent_col]    = df[RB_cols].sum(axis = 1).mul(100).div(df[RB_totl]).round(2)
            df[population_col] = df[RB_cols].sum(axis = 1)
            tot_vars.append(RB_totl)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#FFA6A6", "#FF9A9A", "#FF8A8A", "#FF7A7A", "#FF6666",
                "#FF5555", "#FF4040", "#FF2E2E", "#E60000", "#B30000",
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Rent Burden by Age</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Age Demographic</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percentage of Renters (%)</b>",
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
            'custom_data': ['POPULATION', 'TOTAL'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Of the <b>%{customdata[1]} renters</b> who are in this demographic,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "approximately <b>%{customdata[0]} renters</b> (or <b>%{y}</b> of renters)&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "are <b style='color:#660000'>rent burdened</b>."
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def RentBurdenbyIncome(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # B25074 (full availability)

        labs = [
            'Less than $10k', '$10k to 20.0k', '$20k to 35.0k',
            '$35k to 50.0k', '$50k to 75.0k', '$75k to 100.0k',
            'More than $100k'
        ]
        pop_vars = [f'{i} Population' for i in labs]
        per_vars = [f'{i} Percentage' for i in labs]
        tot_vars = []

        if year < 2014:
            for per_col, pop_col, j in zip(per_vars, pop_vars, range(2, 45, 7)):
                RB_totl = 'B25074_' + str(j).zfill(3) + 'E'
                RB_cols = cls.generate_variables('B25074_', j + 4, j + 5)

                df[per_col] = df[RB_cols].sum(axis = 1).mul(100).div(df[RB_totl]).round(2)
                df[pop_col] = df[RB_cols].sum(axis = 1)
                tot_vars.append(RB_totl)
        
        if year >= 2014:
            for per_col, pop_col, j in zip(per_vars, pop_vars, range(2, 57, 9)):
                RB_totl = 'B25074_' + str(j).zfill(3) + 'E'
                RB_cols = cls.generate_variables('B25074_', j + 4, j + 7)

                df[per_col] = df[RB_cols].sum(axis = 1).mul(100).div(df[RB_totl]).round(2)
                df[pop_col] = df[RB_cols].sum(axis = 1)
                tot_vars.append(RB_totl)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#FFA6A6", "#FF9A9A", "#FF8A8A", "#FF7A7A", "#FF6666",
                "#FF5555", "#FF4040", "#FF2E2E", "#E60000", "#B30000",
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Rent Burden by Income</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Income Bracket</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percentage of Renters (%)</b>",
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
            'custom_data': ['POPULATION', 'TOTAL'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Of the <b>%{customdata[1]} renters</b> in this income bracket,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "approximately <b>%{customdata[0]} renters</b> (or <b>%{y}</b> of&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "renters) are <b style='color:#660000'>rent burdened</b>."
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata




