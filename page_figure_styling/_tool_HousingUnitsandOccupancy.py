"""
Tooltip metadata interface for the 'Housing Units and Occupancy' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class HousingUnitsandOccupancyTooltip(TooltipFigureMetaABC, measure = 'Housing Units and Occupancy'):
    """
    Tooltip metadata interface for the 'Housing Units and Occupancy' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Property Values for Owner-Occupied Units': cls.PropertyValuesforOwnerOccupiedUnits,
            # 'Occupancy by Householder Racial Status': cls.OccupancybyHouseholderRacialStatus,
            # 'Occupancy by Householder Age': cls.OccupancybyHouseholderAge,
            # 'Housing Units by Year Built': cls.HousingUnitsbyYearBuilt,
            'Rooms in Housing Units': cls.RoomsinHousingUnits,
            'Bedrooms in Housing Units': cls.BedroomsinHousingUnits,
            'House Heating Fuel': cls.HouseHeatingFuel,
            'Select Units Lacking Facilities': cls.SelectUnitsLackingFacilities,
            'Occupants Per Room': cls.OccupantsPerRoom,
            'Monthly Owner Costs for Units w/ Mortgage': cls.MonthlyOwnerCostsforUnitswMortgage,
            # 'Year Householder Moved In': cls.YearHouseholderMovedIn,
        }
        return lambda_dict

        
    
    @classmethod
    def PropertyValuesforOwnerOccupiedUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0080E to DP04_0087E for 2009 to 2014 (DP04_0079E total)
        # DP04_0081E to DP04_0088E for 2015 and later (DP04_0080E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = {
            "Less than $50k": "less than $50K",
            "$50k to 100.0k": "$50K to $100.0K",
            "$100k to 150.0k": "$100K to $150.0K",
            "$150k to 200.0k": "$150K to $200.0K",
            "$200k to 300.0k": "$200K to $300.0K",
            "$300k to 500.0k": "$300K to $500.0K",
            "$500k to 1 mil.": "$500k to $1 million",
            "$1 million or more": "$1 million or more"
        }

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 80, 87, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 80, 87, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0079E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 81, 88, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 81, 88, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0080E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        color_array = [
            "#FFBA08", "#FAA307", "#F48C06", "#E85D04",
            "#DC2F02", "#D00000", "#9D0208", "#6A040F"
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:17px;'>Property Values for Owner-Occupied Units</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Property Values</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} owner-occupied units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) had a property value&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "of <b>%{customdata[2]}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    # @classmethod
    # def OccupancybyHouseholderRacialStatus(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2502 (unavailable for 2009)



    # @classmethod
    # def OccupancybyHouseholderAge(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # S2502 (unavailable for 2009)



    # @classmethod
    # def HousingUnitsbyYearBuilt(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # DP04 (full availability)



    @classmethod
    def RoomsinHousingUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0027E to DP04_0035E for 2009 to 2014 (DP04_0026E total)
        # DP04_0028E to DP04_0036E for 2015 and later (DP04_0027E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = [
            "1 room",
            *[f"{i} rooms" for i in range(2, 9)],
            "9 rooms or more"
        ]

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 27, 35, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 27, 35, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0026E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 28, 36, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 28, 36, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0027E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)

        color_array = [
            "#ADE8F4", "#90E0EF", "#48CAE4", "#00B4D8",
            "#0096C7", "#0077B6", "#023E8A", "#03045E"
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Housing Units by Number of Rooms</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Number of Rooms</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} housing units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) had <b>%{x}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    @classmethod
    def BedroomsinHousingUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0038E to DP04_0043E for 2009 to 2014 (DP04_0037E total)
        # DP04_0039E to DP04_0044E for 2015 and later (DP04_0038E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = [
            "No bedroom",
            "1 bedroom",
            *[f"{i} bedrooms" for i in range(2, 5)],
            "5 bedrooms or more"
        ]

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 38, 43, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 38, 43, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0037E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 39, 44, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 39, 44, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0038E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].str.lower()

        color_array = ["#E9F5DB", "#CFE1B9", "#B5C99A", "#97A97C", "#87986A", "#718355"]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Housing Units by Number of Bedooms</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Number of Bedrooms</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} housing units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) had <b>%{customdata[2]}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    @classmethod
    def HouseHeatingFuel(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0062E to DP04_0070E for 2009 to 2014 (DP04_0061E total)
        # DP04_0063E to DP04_0071E for 2015 and later (DP04_0062E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = [
            "Utility gas",
            "Bottled or tank gas",
            "Electricity",
            "Fuel oil, kerosene, etc.",
            "Coal or coke",
            "Wood",
            "Solar",
            "Other",
            "No fuel"
        ]

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 62, 70, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 62, 70, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0061E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 63, 71, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 63, 71, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0062E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].str.lower()

        color_array = [
            "#E76F51", "#EE8959", "#F4A261", "#E9C46A",
            "#8AB17D", "#2A9D8F", "#287271", "#264653"
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Housing Units by Heating Fuel</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Type of Heating Fuel</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} housing units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) used <b>%{customdata[2]}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata





    @classmethod
    def SelectUnitsLackingFacilities(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # Two options:
        # - B25016 (plumbing facilities) and B25053 (kitchen facilities) (both full availability)
        # - DP04 (plumbing, kitchen, and telephone facilities; full availability) <- preferred
        #
        # DP04_0072E to DP04_0074E for 2009 to 2014 (DP04_0071E total)
        # DP04_0073E to DP04_0075E for 2015 and later (DP04_0072E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = {
            "Lacking complete<br>plumbing facilities": "lacked complete<br>plumbing facilities",
            "Lacking complete<br>kitchen facilities": "lacked complete<br>kitchen facilities",
            "No telephone service": "had no telephone<br>service available"
        }

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 72, 74, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 72, 74, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0071E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 73, 75, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 73, 75, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0072E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        color_array = ["#26547C", "#EF476F", "#FFD166"]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Housing Units by Lacking Facilities</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Type of Lacking Facility</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 12
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} housing units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) <b>%{customdata[2]}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    @classmethod
    def OccupantsPerRoom(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0076E to DP04_0078E for 2009 to 2014 (DP04_0075E total)
        # DP04_0077E to DP04_0079E for 2015 and later (DP04_0076E total)
        # Absolute estimates (percent estimates, 'PE')

        labs = [
            "1.00 or less",
            "1.01 to 1.50",
            "1.51 or more"
        ]

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 76, 78, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 76, 78, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0075E'
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 77, 79, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 77, 79, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0076E'

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)

        color_array = ["#A7C957", "#6A994E", "#386641",]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:18px;'>Housing Units by Average Occupants per Room</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Average Occupants per Room</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 12
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Percent of Units (%)</b>",
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
            "Of the estimated <b>%{customdata[1]} housing units</b>,&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b>%{customdata[0]}</b> units (or <b>%{y}</b>) had an average&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "occupancy rate of <b>%{x}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "occupants per room."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    @classmethod
    def MonthlyOwnerCostsforUnitswMortgage(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        # DP04 (full availability)
        # DP04_0093E to DP04_0099E for 2009 to 2014 (DP04_0092E total)
        # DP04_0094E to DP04_0100E for 2015 and later (DP04_0093E total)
        # Absolute estimates (percent estimates, 'PE')

        if year <= 2014:
            pop_vars = cls.generate_variables('DP04_', 93, 99, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 93, 99, num_zeros=4, var_type='PE')
            TOTAL_VAR= 'DP04_0092E'
            labs = {
                "Less than<br>$300": "Less than $300",
                "$300 to<br>$499": "$300 to $499",
                "$500 to<br>$699": "$500 to $699",
                "$700 to<br>$999": "$700 to $999",
                "$1,000 to<br>$1,499": "$1,000 to $1,499",
                "$1,500 to<br>$1,999": "$1,500 to $1,999",
                "$2,000 or<br>more": "$2,000 or more"
            }
        if year > 2014:
            pop_vars = cls.generate_variables('DP04_', 94, 100, num_zeros=4, var_type='E')
            per_vars = cls.generate_variables('DP04_', 94, 100, num_zeros=4, var_type='PE')
            TOTAL_VAR='DP04_0093E'
            labs = {
                "Less than<br>$500": "Less than $500",
                "$500 to<br>$1.0K": "$500 to $999",
                "$1K to<br>$1.5K": "$1,000 to $1,499",
                "$1.5K to<br>$2.0K": "$1,500 to $1,999",
                "$2.0K to<br>$2.5K": "$2,000 to $2,499",
                "$2.5K to<br>$3.0K": "$2,500 to $2,999",
                "$3.0K or<br>more": "$3,000 or more"
            }

        df = cls.get_long_df_values_populations(df, per_vars, pop_vars, list(labs), TOTAL_VAR)
        df['TEXT'] = df['VARIABLE'].map(labs)

        color_array = [
            "#F19E18", "#EF8A17", "#ED7517", "#EC6116",
            "#EA4C15", "#E83715", "#E62314"
        ]

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'POPULATION',
            'title': {
                'text': "<b style='font-size:18px;'>Monthly Owner Costs for Units with Mortgages</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': "<b style='font-size:18px;'>Monthly Owner Costs</b>",
                    'standoff': 25
                },
                'tickfont': {
                    'size': 11
                },
            },
            'yaxis': {
                'title': {
                    'text': "<b style='font-size:15px;'>Number of Units</b>",
                    'standoff': 15
                },
                'ticklabelstandoff': 5,
            },
            'marker': {
                'color': color_array,
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            },
            'custom_data': ['VALUE', TOTAL_VAR, 'TEXT'],
            'hovertemplate': 
            "<span style='font-family: Trebuchet MS, sans-serif;'>"
            "An estimated <b style='font-size:14px'>%{y} households</b> (or <b>%{customdata[0]}%</b> of&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "%{customdata[1]} households) indicated monthly costs of&nbsp;&nbsp;&nbsp;&nbsp;<br>"
            "<b style='font-size:14px'>%{customdata[2]}</b>."
            "</span>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>"
        }

        return metadata



    # @classmethod
    # def YearHouseholderMovedIn(
    #     cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    # ):
    #     ...
    #     # DP04 (full availability)




