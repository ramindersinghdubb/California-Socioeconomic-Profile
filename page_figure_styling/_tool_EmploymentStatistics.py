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
        # S2301 (full availability)
        # S2301_C04_009E to S2301_C04_018E for 2010 to 2014
        # S2301_C04_012E to S2301_C04_020E for 2015 and later
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

        if year < 2015:
            vars = cls.generate_variables('S2301_C04_', 10, 18)
            pops = cls.generate_variables('S2301_C01_', 10, 18)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C04_', 12, 20)
            pops = cls.generate_variables('S2301_C01_', 12, 20)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = [0, 2.5, 5, 10, 15, 20, 50, 100],
            color_array = [
                "#2E7D32", "#43A047", "#D4E157",
                "#FFEB3B", "#FFB347", "#FF6A00",
                "#7A0016"
            ],
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Unemployment Rates by Racial Status</b>",
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
                    'text': '<b>Unemployment Rate (%)</b>',
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Unemployment Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (16+): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def LFPRbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C02_010E to S2301_C02_018E for 2010 to 2014
        # S2301_C02_012E to S2301_C02_020E for 2015 and later
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

        if year < 2015:
            vars = cls.generate_variables('S2301_C02_', 10, 18)
            pops = cls.generate_variables('S2301_C01_', 10, 18)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C02_', 12, 20)
            pops = cls.generate_variables('S2301_C01_', 12, 20)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Labor Force Participation Rates by Racial Status</b>",
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
                    'text': "<b style='font-size:14px;'>Labor Force Particip. Rate (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Labor Force Participation Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (16+): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def EPOPRatiobyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C03_010E to S2301_C03_018E for 2010 to 2014
        # S2301_C03_012E to S2301_C03_020E for 2015 and later
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

        if year < 2015:
            vars = cls.generate_variables('S2301_C03_', 10, 18)
            pops = cls.generate_variables('S2301_C01_', 10, 18)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C03_', 12, 20)
            pops = cls.generate_variables('S2301_C01_', 12, 20)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)
        

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Employment-to-Population Ratios by Racial Status</b>",
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
                    'text': "<b style='font-size:14px;'>Employment-to-Pop. Ratio (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Employment-to-Population Ratio: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (16+): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def UnemployRatebySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C04_020E to S2301_C04_021E for 2010 to 2014
        # S2301_C04_022E to S2301_C04_022E for 2015 and later
        # All are arranged in the same order ("Male", "Female")
        labs = ["Men", "Women"]
        if year < 2015:
            vars = cls.generate_variables('S2301_C04_', 20, 21)
            pops = cls.generate_variables('S2301_C01_', 20, 21)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C04_', 22, 23)
            pops = cls.generate_variables('S2301_C01_', 22, 23)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = [0, 2.5, 5, 10, 15, 20, 50, 100],
            color_array = [
                "#2E7D32", "#43A047", "#D4E157",
                "#FFEB3B", "#FFB347", "#FF6A00",
                "#7A0016"
            ],
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Unemployment Rates by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sexual Orientation</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 15
                },
            },
            'yaxis': {
                'title': {
                    'text': '<b>Unemployment Rate (%)</b>',
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Unemployment Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (20 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def LFPRbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C02_020E to S2301_C02_021E for 2010 to 2014
        # S2301_C02_022E to S2301_C02_023E for 2015 and later
        # All are arranged in the same order ("Male", "Female")
        labs = ["Men", "Women"]
        if year < 2015:
            vars = cls.generate_variables('S2301_C02_', 20, 21)
            pops = cls.generate_variables('S2301_C01_', 20, 21)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C02_', 22, 23)
            pops = cls.generate_variables('S2301_C01_', 22, 23)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:17px;'>Labor Force Participation Rates by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sexual Orientation</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 15
                },                
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Labor Force Particip. Rate (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Labor Force Participation Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (20 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def EPOPRatiobySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C03_020E to S2301_C03_021E for 2010 to 2014
        # S2301_C03_022E to S2301_C03_023E for 2015 and later
        # All are arranged in the same order ("Male", "Female")

        labs = ["Men", "Women"]
        if year < 2015:
            vars = cls.generate_variables('S2301_C03_', 20, 21)
            pops = cls.generate_variables('S2301_C01_', 20, 21)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C03_', 22, 23)
            pops = cls.generate_variables('S2301_C01_', 22, 23)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:17px;'>Employment-to-Population Ratios by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sexual Orientation</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 15
                },                
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Employment-to-Pop. Ratio (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Employment-to-Population Ratio: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (20 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def UnemployRatebyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C04_026E to S2301_C04_029E for 2010 to 2014
        # S2301_C04_032E to S2301_C04_035E for 2015 and later
        # All are arranged in the same order (from "Less than HS grad" to "Bachelor's or higher")

        labs = [
            "Less than HS<br>graduate",
            "HS graduate<br>or equivalent",
            "Some college<br>or associate's",
            "Bachelor's or<br>higher",
        ]

        if year < 2015:
            vars = cls.generate_variables('S2301_C04_', 26, 29)
            pops = cls.generate_variables('S2301_C01_', 26, 29)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C04_', 32, 35)
            pops = cls.generate_variables('S2301_C01_', 32, 35)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = [0, 2.5, 5, 10, 15, 20, 50, 100],
            color_array = [
                "#2E7D32", "#43A047", "#D4E157",
                "#FFEB3B", "#FFB347", "#FF6A00",
                "#7A0016"
            ],
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Unemployment Rates by Educational Attainment</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Educational Attainment</b>',
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': '<b>Unemployment Rate (%)</b>',
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Unemployment Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (25 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def LFPRbyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C02_026E to S2301_C02_029E for 2010 to 2014
        # S2301_C02_032E to S2301_C02_035E for 2015 and later
        # All are arranged in the same order (from "Less than HS grad" to "Bachelor's or higher")
        labs = [
            "Less than HS<br>graduate",
            "HS graduate<br>or equivalent",
            "Some college<br>or associate's",
            "Bachelor's or<br>higher",
        ]

        if year < 2015:
            vars = cls.generate_variables('S2301_C02_', 26, 29)
            pops = cls.generate_variables('S2301_C01_', 26, 29)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C02_', 32, 35)
            pops = cls.generate_variables('S2301_C01_', 32, 35)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:17px;'>Labor Force Participation Rates by Educational Attainment</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Educational Attainment</b>',
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },                
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Labor Force Particip. Rate (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Labor Force Participation Rate: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (25 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def EPOPRatiobyEducationalAttainment(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2301 (full availability)
        # S2301_C03_026E to S2301_C03_029E for 2010 to 2014
        # S2301_C03_032E to S2301_C03_035E for 2015 and later
        # All are arranged in the same order (from "Less than HS grad" to "Bachelor's or higher")
        labs = [
            "Less than HS<br>graduate",
            "HS graduate<br>or equivalent",
            "Some college<br>or associate's",
            "Bachelor's or<br>higher",
        ]

        if year < 2015:
            vars = cls.generate_variables('S2301_C03_', 26, 29)
            pops = cls.generate_variables('S2301_C01_', 26, 29)
        if year >= 2015:
            vars = cls.generate_variables('S2301_C03_', 32, 35)
            pops = cls.generate_variables('S2301_C01_', 32, 35)

        df = cls.get_long_df_values_populations(df, vars, pops, labs)

        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            ]
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:17px;'>Employment-to-Population Ratios by Educational Attainment</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Educational Attainment</b>',
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },                
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Employment-to-Pop. Ratio (%)</b>",
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
            'custom_data': ['POPULATION'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Employment-to-Population Ratio: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Population (25 to 64): %{customdata[0]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata