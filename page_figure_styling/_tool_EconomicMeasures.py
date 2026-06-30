"""
Tooltip metadata interface for the 'Economic Measures' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class EconomicMeasuresTooltip(TooltipFigureMetaABC, measure = 'Economic Measures'):
    """
    Tooltip metadata interface for the 'Economic Measures' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Civilian Workforce by Industry': cls.CivilianWorkforcebyIndustry,
            'Civilian Workforce by Occupation': cls.CivilianWorkforcebyOccupation,
            'Civilian Workforce by Sector': cls.CivilianWorkforcebySector,
            # 'Median Earnings, All Workers by Industry': cls.MedianEarningsAllWorkersbyIndustry,
            # 'Median Earnings, Full-Time Workers by Industry': cls.MedianEarningsFullTimeWorkersbyIndustry,
            # 'Gender Pay Gap, All Workers': cls.GenderPayGapAllWorkers,
            # 'Gender Pay Gap, Full-Time Workers': cls.GenderPayGapFullTimeWorkers,
        }
        return lambda_dict

        
    
    @classmethod
    def CivilianWorkforcebyIndustry(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # Two options:
        # - S2403 (unavailable for 2009)
        # - DP03 (full availability) <- preferred

        # DP03_0033E (total), DP03_0034E to DP03_0046E (industries) - 2009
        # DP03_0032E (total), DP03_0033E to DP03_0045E (industries) - 2010 and later
        # Absolute estimates (percent estimates, 'PE')

        labs = cls.__get_industries()

        if year == 2009:
            per_vars = cls.generate_variables('DP03_', 34, 46, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 34, 46, num_zeros = 4, var_type = 'E')
            TOTAL_VAR = 'DP03_0033E'
        else:
            per_vars = cls.generate_variables('DP03_', 33, 45, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 33, 45, num_zeros = 4, var_type = 'E')
            TOTAL_VAR = 'DP03_0032E'
        
        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        color_array = cls.__get_13_color_array()

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Civilian Workforce by Industry of Employment</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Industry</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 7
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Civilian Workforce (%)</b>",
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
            'custom_data': ['POPULATION', TOTAL_VAR, 'TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Employed Civilian Workforce: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workers Employed in Industry: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workforce (16 and Older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def CivilianWorkforcebyOccupation(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP03 (full availability)
        # DP03_0026E (total), DP03_0027E to DP03_0032E (occupations) - 2009
        # DP03_0026E (total), DP03_0027E to DP03_0031E (occupations) - 2010 and later
        # Absolute estimates (percent estimates, 'PE')

        labs = cls.__get_occupations(year)

        TOTAL_VAR = 'DP03_0026E'
        if year == 2009:
            per_vars = cls.generate_variables('DP03_', 27, 32, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 27, 32, num_zeros = 4, var_type = 'E')
            color_array = cls.__get_6_color_array()
        else:
            per_vars = cls.generate_variables('DP03_', 27, 31, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 27, 31, num_zeros = 4, var_type = 'E')
            color_array = cls.__get_5_color_array()
        
        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Civilian Workforce by Occupation</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Occupation</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 9
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Civilian Workforce (%)</b>",
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
            'custom_data': ['POPULATION', TOTAL_VAR, 'TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Employed Civilian Workforce: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workers in Occupation: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workforce (16 and Older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    @classmethod
    def CivilianWorkforcebySector(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP03 (full availability)
        # DP03_0047E (total), DP03_0048E to DP03_0051E (sectors) - 2009
        # DP03_0046E (total), DP03_0047E to DP03_0050E (sectors) - 2010 and later
        # Absolute estimates (percent estimates, 'PE')

        labs = cls.__get_sectors()

        if year == 2009:
            per_vars = cls.generate_variables('DP03_', 48, 51, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 48, 51, num_zeros = 4, var_type = 'E')
            TOTAL_VAR = 'DP03_0047E'
        else:
            per_vars = cls.generate_variables('DP03_', 47, 50, num_zeros = 4, var_type = 'PE')
            pop_vars = cls.generate_variables('DP03_', 47, 50, num_zeros = 4, var_type = 'E')
            TOTAL_VAR = 'DP03_0046E'
        
        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, labs, TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        color_array = cls.__get_4_color_array()

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Civilian Workforce by Sector</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Sector</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:12px;'>Percent of Civilian Workforce (%)</b>",
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
            'custom_data': ['POPULATION', TOTAL_VAR, 'TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "<b style='font-size:15px'>%{customdata[2]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br><br>"
            "Percent of Employed Civilian Workforce: %{y}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workers Employed in Sector: %{customdata[0]}&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "Total Civilian Workforce (16 and Older): %{customdata[1]}</span>"
            "&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
        }

        return metadata



    # @classmethod
    # def MedianEarningsAllWorkersbyIndustry(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2413 (unavailable for years earlier than 2015)



    # @classmethod
    # def MedianEarningsFullTimeWorkersbyIndustry(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2414 (unavailable for years earlier than 2015)



    # @classmethod
    # def GenderPayGapAllWorkers(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2413 (unavailable for years earlier than 2015)



    # @classmethod
    # def GenderPayGapFullTimeWorkers(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2414 (unavailable for years earlier than 2015)


    
    @classmethod
    def __get_industries(cls) -> t.Dict[str, str]:
        html_ind_labs = [
            "Agriculture, forestry,<br>fishing and hunting,<br>and mining",
            "Construction",
            "Manufacturing",
            "Wholesale trade",
            "Retail trade",
            "Transportation and<br>warehousing,<br>and utilities",
            "Information",
            "Finance and insurance,<br>and real estate and<br>rental and leasing",
            "Professional, scientific, and<br>management, and<br>administrative and<br>waste management services",
            "Educational services, and<br>health care and social<br>assistance",
            "Arts, entertainment, and<br>recreation, and<br>accommodation and food<br>services",
            "Other services, except<br>public administration",
            "Public administration"
        ]

        text_ind_labs = [
            "Agriculture, forestry, fishing and<br>hunting, and mining",
            "Construction",
            "Manufacturing",
            "Wholesale trade",
            "Retail trade",
            "Transportation and warehousing, and<br>utilities",
            "Information",
            "Finance and insurance, and real estate<br>and rental and leasing",
            "Professional, scientific, and management,<br>and administrative and waste management<br>services",
            "Educational services, and health care<br>and social assistance",
            "Arts, entertainment, and recreation, and<br>accommodation and food services",
            "Other services, except public<br>administration",
            "Public administration"
        ]
        ind_labs = dict(zip(html_ind_labs, text_ind_labs))

        return ind_labs
    
    @classmethod
    def __get_occupations(cls, year: int) -> t.Dict[str, str]:
        if year == 2009:
            html_labs = [
                "Management, professional,<br>and related occupations",
                "Service",
                "Sales and office",
                "Farming, fishing, and<br>forestry",
                "Construction, extraction,<br>maintenance, and repair",
                "Production, transportation,<br>and material moving"
            ]
            text_labs = [
                "Management, professional, and related occupations",
                "Service",
                "Sales and office",
                "Farming, fishing, and forestry",
                "Construction, extraction,<br>maintenance, and repair",
                "Production, transportation, and material moving"
            ]
        else:
            html_labs = [
                "Management, business,<br>science, and arts",
                "Service",
                "Sales and office",
                "Natural resources,<br>construction,<br>and maintenance",
                "Production, transportation,<br>and material moving",
            ]
            text_labs = [
                "Management, business, science, and arts",
                "Service",
                "Sales and office",
                "Natural resources, construction, and maintenance",
                "Production, transportation, and material moving",
            ]
        labs = dict(zip(html_labs, text_labs))
        return labs
    
    @classmethod
    def __get_sectors(cls) -> t.Dict[str, str]:
        html_labs = [
            "Private wage<br>and salary",
            "Government",
            "Self-employed in own<br>not incorporated<br>business",
            "Unpaid family"
        ]

        text_labs = [
            "Private wage and salary",
            "Government",
            "Self-employed in own not incorporated business",
            "Unpaid family"
        ]
        labs = dict(zip(html_labs, text_labs))
        return labs
    
    @classmethod
    def __get_4_color_array(cls) -> t.List[str]:
        color_array = ["#219EBC", "#023047", "#FFB703", "#FB8500"]
        return color_array
    
    @classmethod
    def __get_5_color_array(cls) -> t.List[str]:
        color_array = [
            "#FF595E", "#FFCA3A", "#8AC926", "#1982C4", "#6A4C93"
        ]
        return color_array
    
    @classmethod
    def __get_6_color_array(cls) -> t.List[str]:
        color_array = [
            "#FD5901", "#F78104", "#FAAB36", "#249EA0", "#008083",
            "#005F60"
        ]
        return color_array
    
    @classmethod
    def __get_13_color_array(cls) -> t.List[str]:
        color_array = [
            "#DB2777", "#EF4444", "#F97316", "#F59E0B", "#84CC16",
            "#10B981", "#059669", "#14B8A6", "#0891B2", "#0284C7",
            "#2563EB", "#7C3AED", "#4F46E5"
        ]
        return color_array

