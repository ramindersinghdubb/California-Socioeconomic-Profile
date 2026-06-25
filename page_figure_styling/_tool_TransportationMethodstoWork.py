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
        ...
        # S0801 (full availability)



    @classmethod
    def DepartureTimes(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S0801 (full availability)



    @classmethod
    def TravelTimes(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S0801 (full availability)



    @classmethod
    def VehiclesAvailable(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        ...
        # S0801 (full availability)




