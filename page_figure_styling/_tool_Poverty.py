"""
Tooltip metadata interface for the 'Poverty' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class PovertyTooltip(TooltipFigureMetaABC, measure = 'Poverty'):
    """
    Tooltip metadata interface for the 'Poverty' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Poverty Status by Racial Status': cls.PovertyStatusbyRacialStatus,
            'Poverty Status by Sexual Orientation': cls.PovertyStatusbySexualOrientation,
            'Poverty Status by Age': cls.PovertyStatusbyAge,
            'Poverty Status by Employment Status': cls.PovertyStatusbyEmploymentStatus,
        }
        return lambda_dict

        
    
    @classmethod
    def PovertyStatusbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S1701 (full availability)
        # S1701_C03_009E to S1701_C03_017E for 2012 to 2014 (percent estimates)
        # S1701_C03_013E to S1701_C03_021E for 2015 and later (percent estimates)

        labs = [
            "White alone",
            "Black or African<br>American",
            "American Indian and<br>Alaska Native",
            "Asian",
            "Native Hawaiian and<br>Other Pacific Islander",
            "Some other race",
            "Two or more races",
            "Hispanic or Latino",
            "White (not Hispanic<br>or Latino)"
        ]

        if year <= 2014:
            tot_vars = cls.generate_variables('S1701_C01_', 9, 17)
            pop_vars = cls.generate_variables('S1701_C02_', 9, 17)
            per_vars = cls.generate_variables('S1701_C03_', 9, 17)
        if year > 2014:
            tot_vars = cls.generate_variables('S1701_C01_', 13, 21)
            pop_vars = cls.generate_variables('S1701_C02_', 13, 21)
            per_vars = cls.generate_variables('S1701_C03_', 13, 21)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Poverty by Racial Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Racial Status</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 9
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:10px;'>Percent of Population Below Poverty Level (%)</b>",
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
            "Percent of Households Below the Poverty Level: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Below the Poverty Level: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def PovertyStatusbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S1701 (full availability)
        # S1701_C03_006E to S1701_C03_007E for 2012 to 2014 (percent estimates)
        # S1701_C03_011E to S1701_C03_012E for 2015 and later (percent estimates)

        labs = ["Men", "Women"]

        if year <= 2014:
            tot_vars = cls.generate_variables('S1701_C01_', 6, 7)
            pop_vars = cls.generate_variables('S1701_C02_', 6, 7)
            per_vars = cls.generate_variables('S1701_C03_', 6, 7)
        if year > 2014:
            tot_vars = cls.generate_variables('S1701_C01_', 11, 12)
            pop_vars = cls.generate_variables('S1701_C02_', 11, 12)
            per_vars = cls.generate_variables('S1701_C03_', 11, 12)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Poverty by Sexual Orientation</b>",
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
                    'text': "<b style='font-size:10px;'>Percent of Population Below Poverty Level (%)</b>",
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
            "Percent of Households Below the Poverty Level: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Below the Poverty Level: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def PovertyStatusbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S1701 (full availability)
        # S1701_C02_002E, S1701_C02_004E, S1701_C02_005E for 2012 to 2014
        # (percent estimates; "under 18", "18 to 64", "65 and older")
        # S1701_C02_002E, S1701_C02_006E, S1701_C02_010E for 2015 and later
        # (percent estimates; "under 18", "18 to 64", "65 and older")

        labs = [
            "Under 18", "18 to 64", "65 and Older"
        ]

        if year <= 2014:
            nums = [2, 4, 5]
        if year > 2014:
            nums = [2, 6, 10]
        
        tot_vars = ['S1701_C01_' + str(i).zfill(3) + 'E' for i in nums]
        pop_vars = ['S1701_C02_' + str(i).zfill(3) + 'E' for i in nums]
        per_vars = ['S1701_C03_' + str(i).zfill(3) + 'E' for i in nums]

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Poverty by Age Demographic</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Age Demographic</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 14
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:10px;'>Percent of Population Below Poverty Level (%)</b>",
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
            "Percent of Households Below the Poverty Level: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Below the Poverty Level: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def PovertyStatusbyEmploymentStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S1701 (full availability)
        # S1701_C03_024E, S1701_C03_027E for 2012 to 2014
        # (percent estimates; "employed", "unemployed")
        # S1701_C03_028E, S1701_C03_031E for 2015 and later
        # (percent estimates; "employed", "unemployed")

        labs = ["Employed", "Unemployed"]

        if year <= 2014:
            nums = [24, 27]
        if year > 2014:
            nums = [28, 31]
        
        tot_vars = ['S1701_C01_' + str(i).zfill(3) + 'E' for i in nums]
        pop_vars = ['S1701_C02_' + str(i).zfill(3) + 'E' for i in nums]
        per_vars = ['S1701_C03_' + str(i).zfill(3) + 'E' for i in nums]

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Poverty by Employment Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Employment Status</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 15
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:10px;'>Percent of Population Below Poverty Level (%)</b>",
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
            "Percent of Households Below the Poverty Level: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Below the Poverty Level: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata


    @classmethod
    def __get_color_array(cls, df: pd.DataFrame) -> t.List[str]:
        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#FFA6A6", "#FF9A9A", "#FF8A8A", "#FF7A7A", "#FF6666",
                "#FF5555", "#FF4040", "#FF2E2E", "#E60000", "#B30000",
            ]
        )

        return color_array

