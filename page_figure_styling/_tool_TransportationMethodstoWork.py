"""
Tooltip metadata interface for the 'Transportation Methods to Work' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class TransportationMethodstoWorkTooltip(TooltipFigureMetaABC, measure = 'Transportation Methods to Work'):
    """
    Tooltip metadata interface for the 'Transportation Methods to Work' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Commute Methods to Work': cls.CommuteMethodstoWork,
            'Departure Times': cls.DepartureTimes,
            'Travel Times': cls.TravelTimes,
            'Vehicles Available': cls.VehiclesAvailable,
        }
        return lambda_dict

        
    
    @classmethod
    def CommuteMethodstoWork(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S0801 (full availability)
        # S0801_C01_003E, S0801_C01_004E, S0801_C01_009E to S0801_C01_013E for 2009 and later
        # Note that S0801_C01_005E to S0801_C01_007E are sub-variants of "Carpooling",
        # where S0801_C01_004E is "Carpooling" proper and S0801_C01_003E is "Drove alone".
        # Note that S0801_C01_008E represents "Workers per car, truck, or van".
        # These are percent estimates.

        labs = [
            "Drove alone",
            "Carpooled",
            "Public transport",
            "Walked",
            "Biked",
            "Taxicab, motorcycle,<br>or other",
            "Worked from home"
        ]

        TOTAL_VAR = 'S0801_C01_001E'
        per_vars  = cls.generate_variables('S0801_C01_', 3, 4) + cls.generate_variables('S0801_C01_', 9, 13)
        pop_vars  = [f'POPULAT_{i}' for i in per_vars]
        for pop_var, per_var in zip(pop_vars, per_vars):
            df[pop_var] = df[per_var].mul(df[TOTAL_VAR]).div(100).round(0)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Commute Methods to Work</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Commute Method</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 11
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Workers (%)</b>",
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
            "Percent of Workers Traveling by this Method: <b style='color:#CC5200;'>%{y}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Workers Traveling by this Method: <b style='color:#CC5200;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Workers (16 and older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def DepartureTimes(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S0801 (full availability)
        # S0801_C01_027E to S0801_C01_036E for 2009 and later (percent estimates)

        labs = [
            "12 AM to 5 AM",
            "5 AM to 5:30 AM",
            "5:30 AM to 6 AM",
            "6 AM to 6:30 AM",
            "6:30 AM to 7 AM",
            "7 AM to 7:30 AM",
            "7:30 AM to 8 AM",
            "8 AM to 8:30 AM",
            "8:30 AM to 9 AM",
            "9 AM to 12 AM"
        ]

        TOTAL_VAR = 'S0801_C01_026E'
        per_vars  = cls.generate_variables('S0801_C01_', 27, 36)
        pop_vars  = [f'POPULAT_{i}' for i in per_vars]
        for pop_var, per_var in zip(pop_vars, per_vars):
            df[pop_var] = df[per_var].mul(df[TOTAL_VAR]).div(100).round(0)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Departure Times to Work</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Departure Times</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 9
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Workers (%)</b>",
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
            "Percent of Workers Departing: <b style='color:#CC5200;'>%{y}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Workers Departing: <b style='color:#CC5200;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Workers Traveling to Work (16 and older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata




    @classmethod
    def TravelTimes(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S0801 (full availability)
        # S0801_C01_037E to S0801_C01_045E for 2009 and later (percent estimates)

        labs = [
            "Less than 10 mins.",
            "10 to 14 mins.",
            "15 to 19 mins.",
            "20 to 24 mins.",
            "25 to 29 mins.",
            "30 to 34 mins.",
            "35 to 44 mins.",
            "45 to 59 mins.",
            "1 hr. or more"
        ]

        TOTAL_VAR = 'S0801_C01_026E'
        per_vars  = cls.generate_variables('S0801_C01_', 37, 45)
        pop_vars  = [f'POPULAT_{i}' for i in per_vars]
        for pop_var, per_var in zip(pop_vars, per_vars):
            df[pop_var] = df[per_var].mul(df[TOTAL_VAR]).div(100).round(0)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        color_array = [
            "#FFD9A0", "#FFCC7A", "#FFC165", "#FFB14D", "#FFA33D",
            "#FF9500", "#F47C00", "#E66500", "#CC5200",
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Travel Times to Work</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Travel Time</b>",
                    'standoff': 20
                },
                'tickfont': {
                    'size': 9
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Workers (%)</b>",
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
            "Percent of Workers Traveling: <b style='color:#CC5200;'>%{y}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Workers Traveling: <b style='color:#CC5200;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Workers Traveling to Work (16 and older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def VehiclesAvailable(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S0801 (full availability)
        # S0801_C01_048E to S0801_C01_051E for 2009 and later (percent estimates)

        labs = [
            "No vehicle",
            "1 vehicle",
            "2 vehicles",
            "3 or more vehicles",
        ]

        TOTAL_VAR = 'S0801_C01_047E'
        per_vars  = cls.generate_variables('S0801_C01_', 48, 51)
        pop_vars  = [f'POPULAT_{i}' for i in per_vars]
        for pop_var, per_var in zip(pop_vars, per_vars):
            df[pop_var] = df[per_var].mul(df[TOTAL_VAR]).div(100).round(0)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Vehicles Available</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:16px;'>Number of Vehicles Available</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Workers (%)</b>",
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
            "Percent of Workers: <b style='color:#CC5200;'>%{y}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Workers: <b style='color:#CC5200;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Workers (16 and older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def __get_color_array(cls, df: pd.DataFrame) -> t.List[str]:
        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = [
                "#FFE5B4", "#FFD9A0", "#FFCC7A", "#FFC165", "#FFB14D",
                "#FFA33D", "#FF9500", "#F47C00", "#E66500", "#CC5200",
            ]
        )


        return color_array

