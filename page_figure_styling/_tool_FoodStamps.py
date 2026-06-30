"""
Tooltip metadata interface for the 'Food Stamps' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class FoodStampsTooltip(TooltipFigureMetaABC, measure = 'Food Stamps'):
    """
    Tooltip metadata interface for the 'Food Stamps' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Food Stamps Recipiency by Racial Status': cls.FoodStampsRecipiencybyRacialStatus,
            'Food Stamps Recipiency by Poverty Status': cls.FoodStampsRecipiencybyPovertyStatus,
            'Food Stamps Recipiency by Disability Status': cls.FoodStampsRecipiencybyDisabilityStatus,
            'Food Stamps Recipiency by Working Status': cls.FoodStampsRecipiencybyWorkingStatus,
        }
        return lambda_dict

        
    
    @classmethod
    def FoodStampsRecipiencybyRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2201 (full availability)
        # Also, any of the B22005 variant tables work (but S2201 is broader)
        # S2201_C02_007E to S2201_C02_015E for 2012 to 2014 (these are percent estimates)
        # S2201_C03_025E to S2201_C03_033E for 2015 and later (these are absolute estimates)
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
            tot_vars = cls.generate_variables('S2201_C01_', 7, 15)
            per_vars = cls.generate_variables('S2201_C02_', 7, 15)
            for tot, per in zip(tot_vars, per_vars):
                df[f'POPULAT_{per}'] = df[per].mul(df['S2201_C02_001E']).div(100).round(0)
                df[f'TOTAL_{per}']   = df[f'POPULAT_{per}'].mul(100).div(df[per]).round(0)
            pop_vars = cls.generate_variables('POPULAT_S2201_C02_', 7, 15)
            tot_vars = cls.generate_variables('TOTAL_S2201_C02_', 7, 15)
        if year >= 2015:
            tot_vars = cls.generate_variables('S2201_C01_', 25, 33)
            pop_vars = cls.generate_variables('S2201_C03_', 25, 33)
            for pop, tot in zip(pop_vars, tot_vars):
                df[f'PERCENT_{tot}'] = df[pop].div(df[tot]).mul(100).round(1)
            per_vars = cls.generate_variables('PERCENT_S2201_C01_', 25, 33)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Food Stamps Recipiency by Racial Status</b>",
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
                    'text': "<b style='font-size:12px;'>Percent of Food Stamps Recipients (%)</b>",
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
            "Percent of Food Stamps Recipients: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Receiving Food Stamps: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def FoodStampsRecipiencybyPovertyStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2201 (full availability)
        # S2201_C02_004E for 2012 to 2014 (these are percent estimates; only "below poverty status")
        # S2201_C03_021E to S2201_C03_022E for 2015 and later (these are absolute estimates; "below" and "at or above")

        labs = [
            "Below poverty line",
            "At or above poverty line"
        ]

        if year < 2015:
            tot_below = 'S2201_C01_004E'
            per_below = 'S2201_C02_004E'
            df[f'POPULAT_{per_below}'] = df[per_below].mul(df['S2201_C02_001E']).div(100).round(0)
            df['POPULAT_S2201_C02_005E'] = df['S2201_C02_001E'] - df[f'POPULAT_{per_below}']
            
            df[f'TOTAL_{tot_below}'] = df[tot_below].mul(df['S2201_C01_001E']).div(100).round(0)
            df['TOTAL_S2201_C01_005E'] = df['S2201_C01_001E'].sub(df[f'TOTAL_{tot_below}'])

            df['S2201_C02_005E'] = df['POPULAT_S2201_C02_005E'].div(df['TOTAL_S2201_C01_005E']).mul(100).round(1)

            per_vars = cls.generate_variables('S2201_C02_', 4, 5)
            pop_vars = cls.generate_variables('POPULAT_S2201_C02_', 4, 5)
            tot_vars = cls.generate_variables('TOTAL_S2201_C01_', 4, 5)
        
        if year >= 2015:
            tot_vars = cls.generate_variables('S2201_C01_', 21, 22)
            pop_vars = cls.generate_variables('S2201_C03_', 21, 22)
            for pop, tot in zip(pop_vars, tot_vars):
                df[f'PERCENT_{tot}'] = df[pop].div(df[tot]).mul(100).round(1)
            per_vars = cls.generate_variables('PERCENT_S2201_C01_', 21, 22)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Food Stamps Recipiency by Poverty Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Poverty Status</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Food Stamps Recipients (%)</b>",
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
            "Percent of Food Stamps Recipients: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Receiving Food Stamps: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def FoodStampsRecipiencybyDisabilityStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2201 (full availability)
        # S2201_C02_005E for 2012 to 2014 (these are percent estimates; only "at least one w/ disabilities")
        # S2201_C03_023E to S2201_C03_024E for 2015 and later (these are absolute estimates; "at least one" and "none")

        labs = [
            "At least one person with disabilities",
            "No person with disabilities"
        ]

        if year < 2015:
            tot_below = 'S2201_C01_005E'
            per_below = 'S2201_C02_005E'
            df[f'POPULAT_{per_below}'] = df[per_below].mul(df['S2201_C02_001E']).div(100).round(0)
            df['POPULAT_S2201_C02_006E'] = df['S2201_C02_001E'] - df[f'POPULAT_{per_below}']
            
            df[f'TOTAL_{tot_below}'] = df[tot_below].mul(df['S2201_C01_001E']).div(100).round(0)
            df['TOTAL_S2201_C01_006E'] = df['S2201_C01_001E'].sub(df[f'TOTAL_{tot_below}'])

            df['S2201_C02_006E'] = df['POPULAT_S2201_C02_006E'].div(df['TOTAL_S2201_C01_006E']).mul(100).round(1)

            per_vars = cls.generate_variables('S2201_C02_', 5, 6)
            pop_vars = cls.generate_variables('POPULAT_S2201_C02_', 5, 6)
            tot_vars = cls.generate_variables('TOTAL_S2201_C01_', 5, 6)
        
        if year >= 2015:
            tot_vars = cls.generate_variables('S2201_C01_', 23, 24)
            pop_vars = cls.generate_variables('S2201_C03_', 23, 24)
            for pop, tot in zip(pop_vars, tot_vars):
                df[f'PERCENT_{tot}'] = df[pop].div(df[tot]).mul(100).round(1)
            per_vars = cls.generate_variables('PERCENT_S2201_C01_', 23, 24)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Food Stamps Recipiency by Disability Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Disability Status</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Food Stamps Recipients (%)</b>",
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
            "Percent of Food Stamps Recipients: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Receiving Food Stamps: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def FoodStampsRecipiencybyWorkingStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # S2201 (full availability)
        # S2201_C02_018E to S2201_C02_020E for 2012 to 2014 (these are percent estimates)
        # S2201_C03_036E to S2201_C03_038E for 2015 and later (these are absolute estimates)
        # All are arranged in the same order (from "No workers" to "2 or more workers")

        labs = [
            "No workers",
            "1 worker",
            "2 or more workers",
        ]

        if year < 2015:
            tot_vars = cls.generate_variables('S2201_C01_', 18, 20)
            per_vars = cls.generate_variables('S2201_C02_', 18, 20)
            for tot, per in zip(tot_vars, per_vars):
                df[f'POPULAT_{per}'] = df[per].mul(df['S2201_C02_001E']).div(100).round(0)
                df[f'TOTAL_{per}']   = df[f'POPULAT_{per}'].mul(100).div(df[per]).round(0)
            pop_vars = cls.generate_variables('POPULAT_S2201_C02_', 18, 20)
            tot_vars = cls.generate_variables('TOTAL_S2201_C02_', 18, 20)
        if year >= 2015:
            tot_vars = cls.generate_variables('S2201_C01_', 36, 38)
            pop_vars = cls.generate_variables('S2201_C03_', 36, 38)
            for pop, tot in zip(pop_vars, tot_vars):
                df[f'PERCENT_{tot}'] = df[pop].div(df[tot]).mul(100).round(1)
            per_vars = cls.generate_variables('PERCENT_S2201_C01_', 36, 38)

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, tot_vars)

        color_array = cls.__get_color_array(df)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Food Stamps Recipiency by Working Status</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Number of Workers in Household</b>',
                    'standoff': 20
                },
                'tickfont': {
                    'size': 12
                },
                # 'tickangle': 'auto'
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Food Stamps Recipients (%)</b>",
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
            "Percent of Food Stamps Recipients: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Number of Households Receiving Food Stamps: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Households: %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata
    

    @classmethod
    def __get_color_array(cls, df: pd.DataFrame) -> t.List[str]:
        color_array = cls.generate_binned_qualitative_colors(
            series      = df['VALUE'],
            bins        = list(range(0, 101, 10)),
            color_array = list(reversed((
                "#8B0000", "#8E2006", "#8F3E0C",
                "#8E5B12", "#8A7418", "#7F8A1D",
                "#6E9A18", "#569C16", "#2F8C14",
                "#228B22"
            )))
        )

        return color_array




