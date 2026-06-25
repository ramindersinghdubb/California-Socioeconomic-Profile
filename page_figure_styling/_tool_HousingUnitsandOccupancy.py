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
            'Occupancy by Householder Racial Status': cls.OccupancybyHouseholderRacialStatus,
            'Occupancy by Householder Age': cls.OccupancybyHouseholderAge,
            'Housing Units by Year Built': cls.HousingUnitsbyYearBuilt,
            'Rooms in Housing Units': cls.RoomsinHousingUnits,
            'Bedrooms in Housing Units': cls.BedroomsinHousingUnits,
            'House Heating Fuel': cls.HouseHeatingFuel,
            'Select Units Lacking Facilities': cls.SelectUnitsLackingFacilities,
            'Occupants Per Room': cls.OccupantsPerRoom,
            'Monthly Owner Costs for Units w/ Mortgage': cls.MonthlyOwnerCostsforUnitswMortgage,
            'Year Householder Moved In': cls.YearHouseholderMovedIn,
        }
        return lambda_dict

        
    
    @classmethod
    def PropertyValuesforOwnerOccupiedUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def OccupancybyHouseholderRacialStatus(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def OccupancybyHouseholderAge(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def HousingUnitsbyYearBuilt(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def RoomsinHousingUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def BedroomsinHousingUnits(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def HouseHeatingFuel(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def SelectUnitsLackingFacilities(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def OccupantsPerRoom(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def MonthlyOwnerCostsforUnitswMortgage(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...



    @classmethod
    def YearHouseholderMovedIn(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...




