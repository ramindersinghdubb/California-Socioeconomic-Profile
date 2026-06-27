"""
Tooltip metadata interface for the 'Population' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class PopulationTooltip(TooltipFigureMetaABC, measure = 'Population'):
    """
    Tooltip metadata interface for the 'Population' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Population by Age': cls.PopulationbyAge,
            'Population by Racial Status': cls.PopulationbyRacialStatus,
            'Population by Sexual Orientation': cls.PopulationbySexualOrientation,
        }
        return lambda_dict

        
    
    @classmethod
    def PopulationbyAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP05 (full availability)
        # DP05_0004E to DP05_0016E for 2009 to 2016 (estimates)
        # DP05_0005E to DP05_0017E for 2017 to (estimates)
        # Percent estimate are also of the same position (except letter switch to PE)

        labs = [
            "5 to 9",
            "10 to 14",
            "15 to 19",
            "20 to 24",
            "25 to 34",
            "35 to 44",
            "45 to 54",
            "55 to 59",
            "60 to 64",
            "65 to 74",
            "75 to 84",
            "85 and Older",
        ]

        if year < 2017:
            pop_vars = cls.generate_variables('DP05_', 4, 16, num_zeros = 4, var_type='E')
            per_vars = cls.generate_variables('DP05_', 4, 16, num_zeros = 4, var_type='PE')
        if year >= 2017:
            pop_vars = cls.generate_variables('DP05_', 5, 17, num_zeros = 4, var_type='E')
            per_vars = cls.generate_variables('DP05_', 5, 17, num_zeros = 4, var_type='PE')

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, 'DP05_0001E')

        color_array = [
            "#E6F7FF", "#CDEFFF", "#B4E7FF", "#9ADFFF", "#81D7FF",
            "#68CFFF", "#4FC6FF", "#39BEFF", "#23B3F0", "#1199D9",
            "#0A4F86"
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Population by Age Demographic</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Age Demographic</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 11
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Population (%)</b>",
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
            'custom_data': ['POPULATION', 'DP05_0001E'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "There were approximately <b style='font-size:15px; color:#0A4F86;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "individuals (or <b style='color:#0A4F86;'>%{y}</b> of the entire&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "population of %{customdata[1]} individuals)&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "who were in the <b>%{x}</b> age&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "demographic.</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def PopulationbyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP05 (full availability)
        # DP05_0032E, DP05_0033E, DP05_0034E, DP05_0039E, DP05_0047E,
        # DP05_0052E, DP05_0053E, DP05_0066E, DP05_0072E
        # 2009 to 2017 (estimates)
        #
        # DP05_0037E, DP05_0038E, DP05_0039E, DP05_0044E, DP05_0052E,
        # DP05_0057E, DP05_0058E, DP05_0071E, DP05_0077E
        # 2017 to 2022 (estimates)
        #
        # DP05_0037E, DP05_0038E, DP05_0039E, DP05_0047E, DP05_0055E,
        # DP05_0060E, DP05_0061E, DP05_0076E, DP05_0082E
        # 2023 (estimates)
        #
        # DP05_0037E, DP05_0045E, DP05_0053E, DP05_0061E, DP05_0069E,
        # DP05_0074E, DP05_0075E, DP05_0090E, DP05_0096E
        # 2024 (estimates)

        # All are arranged in the same order (from "White alone" to "White alone, not Hispanic/Latino")
        # Note that each racial status comes with specific racial denominations (e.g. "Asian Indian")
        # alongside the fact that Hispanic/Latino is its own category.
        # Percent estimate are also of the same position (except letter switch to PE)

        # Also, as a side, in 2024, "Egyptian" or "Lebanese" is classified under the "One race, White"
        # racial status. White. WHITE.

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

        if 2009 <= year <= 2016:
            nums = [32, 33, 34, 39, 47, 52, 53, 66, 72]
        elif 2017 <= year <= 2022:
            nums = [37, 38, 39, 44, 52, 57, 58, 71, 77]
        elif year == 2023:
            nums = [37, 38, 39, 47, 55, 60, 61, 76, 82]
        elif year == 2024:
            nums = [37, 45, 53, 61, 69, 74, 75, 90, 96]

        pop_vars = ['DP05_' + str(i).zfill(4) + 'E'  for i in nums]
        per_vars = ['DP05_' + str(i).zfill(4) + 'PE' for i in nums]

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, 'DP05_0001E')
        color_array = ["#39BEFF"] * len(labs)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Population by Racial Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Racial Status</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 9
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Population (%)</b>",
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
            'custom_data': ['POPULATION', 'DP05_0001E'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "There were approximately <b style='font-size:15px; color:#0A4F86;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "individuals (or <b style='color:#0A4F86;'>%{y}</b> of the entire&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "population of %{customdata[1]} individuals)&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "who self-reported as belonging to&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "this demographic.</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def PopulationbySexualOrientation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP05 (full availability)
        # DP05_0002E, DP05_0003E for 2009 and later (estimates)
        # Percent estimate are also of the same position (except letter switch to PE)

        labs = ["Men", "Women"]

        pop_vars = cls.generate_variables('DP05_', 2, 3, num_zeros = 4, var_type='E')
        per_vars = cls.generate_variables('DP05_', 2, 3, num_zeros = 4, var_type='PE')

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, 'DP05_0001E')
        color_array = ["#39BEFF"] * len(labs)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Population by Sexual Orientation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Sexual Orientation</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 15
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:14px;'>Percent of Population (%)</b>",
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
            'custom_data': ['POPULATION', 'DP05_0001E'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "There were approximately <b style='font-size:15px; color:#0A4F86;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "individuals (or <b style='color:#0A4F86;'>%{y}</b> of the entire&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "population of %{customdata[1]} individuals)&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "who self-reported as belonging to&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "this demographic.</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata