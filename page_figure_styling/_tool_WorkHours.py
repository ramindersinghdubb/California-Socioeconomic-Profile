"""
Tooltip metadata interface for the 'Work Hours' category.
"""

import typing as t

import pandas as pd
import numpy as np

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
        # S2303 (full availability)
        # S2303_C01_008E, S2303_C01_011E, S2303_C01_014E, S2303_C01_017E (Total: S2303_C01_001E)
        # Percent estimates, for 2010 to 2014
        # C02 (Men) and C03 (Women); also percent estimates and same order
        #
        # S2303_C01_009E, S2303_C01_016E, S2303_C01_023E, S2303_C01_030E (Total: S2303_C01_001E)
        # Absolute estimates, for 2014 and later
        # C03 (Men) and C05 (Women); also absolute estimates and same order
        # C04 and C06 are percent estimates

        # Order: "35 or more hrs per week", "15 to 34 hrs per week", "1 to 14 hrs per week", "Did not work"

        labs = [
            "35 or more hrs",
            "15 to 34 hrs",
            "1 to 14 hrs",
            "Did not work"
        ]

        TOTAL_VAR = 'S2303_C01_001E'

        if year <= 2014:
            nums = range(8, 18, 3)
            MEN_per_vars = cls.generate_particular_variables('S2303_C02_', nums)
            WOM_per_vars = cls.generate_particular_variables('S2303_C03_', nums)
            for M_per_var, W_per_var in zip(MEN_per_vars, WOM_per_vars):
                df[f'POPULAT_{M_per_var}'] = df[M_per_var].mul(df['S2303_C02_001E'], fill_value=np.nan).div(100).round(0)
                df[M_per_var] = df[f'POPULAT_{M_per_var}'].div(df[TOTAL_VAR], fill_value=np.nan).mul(100).round(1)
                df[f'POPULAT_{W_per_var}'] = df[W_per_var].mul(df['S2303_C03_001E'], fill_value=np.nan).div(100).round(0)
                df[W_per_var] = df[f'POPULAT_{W_per_var}'].div(df[TOTAL_VAR], fill_value=np.nan).mul(100).round(1)
            MEN_pop_vars = cls.generate_particular_variables('POPULAT_S2303_C02_', nums)
            WOM_pop_vars = cls.generate_particular_variables('POPULAT_S2303_C03_', nums)
        if year > 2014:
            nums = range(9, 31, 7)
            MEN_pop_vars = cls.generate_particular_variables('S2303_C03_', nums)
            MEN_per_vars = cls.generate_particular_variables('S2303_C04_', nums)
            WOM_pop_vars = cls.generate_particular_variables('S2303_C05_', nums)
            WOM_per_vars = cls.generate_particular_variables('S2303_C06_', nums)
            for M_per_var, M_pop_var, W_per_var, W_pop_var in zip(MEN_per_vars, MEN_pop_vars, WOM_per_vars, WOM_pop_vars):
                df[M_per_var] = df[M_pop_var].div(df[TOTAL_VAR], fill_value=np.nan).mul(100).round(1)
                df[W_per_var] = df[W_pop_var].div(df[TOTAL_VAR], fill_value=np.nan).mul(100).round(1)

        SEX_ORI_VAR = "<span style='font-family: Trebuchet MS, sans-serif; font-weight: 700;'>Sexual<br>Orientation</span>"
        
        MEN_df = cls.get_long_df_values_populations(df.copy(), MEN_per_vars, MEN_pop_vars, labs, TOTAL_VAR)
        MEN_df[SEX_ORI_VAR] = 'Men'
        WOM_df = cls.get_long_df_values_populations(df.copy(), WOM_per_vars, WOM_pop_vars, labs, TOTAL_VAR)
        WOM_df[SEX_ORI_VAR] = 'Women'

        color_discrete_map = {
            'Men': "#2C8FDA",
            'Women': "#E3912E",
        }

        df = pd.concat([WOM_df, MEN_df])
        df['COLOR'] = df[SEX_ORI_VAR].map(color_discrete_map)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'color': SEX_ORI_VAR,
            'barmode': 'group',
            'color_discrete_map': color_discrete_map,
            'showlegend': True,
            'title': {
                'text': "<b style='font-size:20px;'>Usual Hours Worked Weekly</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Hours Worked Weekly</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 13
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Percent of Population (%)</b>",
                    'standoff': 25
                },
                'ticklabelstandoff': 5,
                'ticksuffix': '%'
            },
            'marker': {
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', TOTAL_VAR, SEX_ORI_VAR, 'COLOR'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'><span style='color: %{customdata[3]};'>%{customdata[2]}</span>, %{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Individuals: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Individuals: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Individuals (16 to 64): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def AverageHoursWorkedWeekly(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2303 (full availability)
        # S2303_C01_018E, for 2010 to 2014
        # C02 (Men) and C03 (Women)
        #
        # S2303_C01_031E, for 2014 and later
        # C03 (Men) and C05 (Women)

        labs = ["Men", "Women"]
        TOTAL_VAR = 'S2303_C01_001E'

        if year <= 2014:
            val_vars = ['S2303_C02_018E', 'S2303_C03_018E']
            pop_vars = ['S2303_C02_001E', 'S2303_C03_001E']
        if year > 2014:
            val_vars = ['S2303_C03_031E', 'S2303_C05_031E']
            pop_vars = ['S2303_C03_001E', 'S2303_C05_001E']

        color_array = ["#2C8FDA", "#E3912E"]

        df = cls.get_long_df_values_populations(df, val_vars, pop_vars, labs, TOTAL_VAR)        
        df['COLOR'] = df['VARIABLE'].map(dict(zip(labs, color_array)))

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Average Hours Worked Weekly</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sexual Orientation</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 15
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Hours Worked</b>",
                    'standoff': 25
                },
                'ticklabelstandoff': 5,
                'ticksuffix': ' hrs'
            },
            'marker': {
                'color': color_array,
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['POPULATION', 'COLOR', TOTAL_VAR],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'><span style='color: %{customdata[1]};'>%{x}</span></b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Average Hours Worked Weekly: <b>%{y}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Individuals: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Individuals (16 to 64): %{customdata[2]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata




