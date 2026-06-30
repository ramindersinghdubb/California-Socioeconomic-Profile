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
        # S2701 (full availability)
        # S2701_C03_009E to S2701_C03_017E for 2010 to 2014 (percent estimates)
        # S2701_C05_017E to S2701_C05_025E for 2015 and 2016 (percent estimates)
        # S2701_C05_016E to S2701_C05_024E for 2017 and later (percent estimates)
        # All are arranged in the same order (from "White alone" to "White alone, not Hispanic/Latino")

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
            tot_vars = cls.generate_variables('S2701_C01_', 9, 17)
            pop_vars = cls.generate_variables('S2701_C02_', 9, 17)
            per_vars = cls.generate_variables('S2701_C03_', 9, 17)
        if 2015 <= year <= 2016:
            tot_vars = cls.generate_variables('S2701_C01_', 17, 25)
            pop_vars = cls.generate_variables('S2701_C04_', 17, 25)
            per_vars = cls.generate_variables('S2701_C05_', 17, 25)
        if year >= 2017:
            tot_vars = cls.generate_variables('S2701_C01_', 16, 24)
            pop_vars = cls.generate_variables('S2701_C04_', 16, 24)
            per_vars = cls.generate_variables('S2701_C05_', 16, 24)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Uninsured Population by Racial Status</b>",
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
                    'text': "<b style='font-size:12px;'>Percent of Uninsured Population (%)</b>",
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
            "Percent of Uninsured Households: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Uninsured Households: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def UninsuredIndividualsbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2701 (full availability)
        # S2701_C03_006E to S2701_C03_007E for 2010 to 2014 (percent estimates)
        # S2701_C05_015E to S2701_C05_016E for 2015 and 2016 (percent estimates)
        # S2701_C05_014E to S2701_C05_015E for 2017 and later (percent estimates)

        labs = ["Men", "Women"]

        if year <= 2014:
            tot_vars = cls.generate_variables('S2701_C01_', 6, 7)
            pop_vars = cls.generate_variables('S2701_C02_', 6, 7)
            per_vars = cls.generate_variables('S2701_C03_', 6, 7)
        if 2015 <= year <= 2016:
            tot_vars = cls.generate_variables('S2701_C01_', 15, 16)
            pop_vars = cls.generate_variables('S2701_C04_', 15, 16)
            per_vars = cls.generate_variables('S2701_C05_', 15, 16)
        if year >= 2017:
            tot_vars = cls.generate_variables('S2701_C01_', 14, 15)
            pop_vars = cls.generate_variables('S2701_C04_', 14, 15)
            per_vars = cls.generate_variables('S2701_C05_', 14, 15)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:16px;'>Uninsured Population by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sexual Orientation</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 14
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Uninsured Population (%)</b>",
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
            "Percent of Uninsured Households: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Uninsured Households: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def UninsuredIndividualsbyCitizenshipStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2701 (full availability)
        # S2701_C03_018E to S2701_C03_021E for 2010 to 2014 (percent estimates)
        # S2701_C05_032E to S2701_C05_035E for 2015 and 2016 (percent estimates)
        # S2701_C05_031E to S2701_C05_034E for 2017 and later (percent estimates)

        labs = [
            "Native",
            "Foreign",
            "Foreign, naturalized",
            "Foreign, not a citizen"
        ]

        if year <= 2014:
            tot_vars = cls.generate_variables('S2701_C01_', 18, 21)
            pop_vars = cls.generate_variables('S2701_C02_', 18, 21)
            per_vars = cls.generate_variables('S2701_C03_', 18, 21)
        if 2015 <= year <= 2016:
            tot_vars = cls.generate_variables('S2701_C01_', 32, 35)
            pop_vars = cls.generate_variables('S2701_C04_', 32, 35)
            per_vars = cls.generate_variables('S2701_C05_', 32, 35)
        if year >= 2017:
            tot_vars = cls.generate_variables('S2701_C01_', 31, 34)
            pop_vars = cls.generate_variables('S2701_C04_', 31, 34)
            per_vars = cls.generate_variables('S2701_C05_', 31, 34)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:16px;'>Uninsured Population by Citizenship Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Citizenship Status</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 11
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Uninsured Population (%)</b>",
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
            "Percent of Uninsured Households: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Uninsured Households: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def UninsuredIndividualsbyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2701 (full availability)
        # S2701_C03_023E to S2701_C03_026E for 2010 to 2014 (percent estimates)
        # S2701_C05_039E to S2701_C05_042E for 2015 and 2016 (percent estimates)
        # S2701_C05_038E to S2701_C05_041E for 2017 and later (percent estimates)

        labs = [
            "Less than HS<br>graduate",
            "HS graduate<br>or equivalent",
            "Some college<br>or associate's",
            "Bachelor's or<br>higher",
        ]

        if year <= 2014:
            tot_vars = cls.generate_variables('S2701_C01_', 23, 26)
            pop_vars = cls.generate_variables('S2701_C02_', 23, 26)
            per_vars = cls.generate_variables('S2701_C03_', 23, 26)
        if 2015 <= year <= 2016:
            tot_vars = cls.generate_variables('S2701_C01_', 39, 42)
            pop_vars = cls.generate_variables('S2701_C04_', 39, 42)
            per_vars = cls.generate_variables('S2701_C05_', 39, 42)
        if year >= 2017:
            tot_vars = cls.generate_variables('S2701_C01_', 38, 41)
            pop_vars = cls.generate_variables('S2701_C04_', 38, 41)
            per_vars = cls.generate_variables('S2701_C05_', 38, 41)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:16px;'>Uninsured Population by Educational Attainment</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Educational Attainment</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 11
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Uninsured Population (%)</b>",
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
            "Percent of Uninsured Households: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Uninsured Households: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households (25 and older): %{customdata[1]}</span>"
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

