"""
Abstract base classes.
"""

import typing as t
from abc import ABC, abstractmethod

from pandas import DataFrame



class TooltipFigureMetaABC(ABC):
    """
    Abstract base class for retrieving the metadata for the tooltip figure.
    """

    @classmethod
    def get_metadata(
        cls,
        *,
        place: str,
        tract: str,
        year: int,
        measure: str,
        submeasure: str,
        df: DataFrame
    ) -> t.Dict[str, t.Any]:
        """
        Retrieve the metadata for the indicate dropdown and hoverdata selection.

        Parameters
        ----------
        place
            The indicated place.

        tract
            The indicated census tract.

        year
            The indicated calendar year.
        
        measure
            The indicated measure.

        submeasure
            The indicated submeasure.

        df
            A(n) :py:class:`pandas.DataFrame` instance.
        """
        metadata = cls._dict_lambda()[submeasure](place, tract, year, measure, df)
        return metadata
    
    @classmethod
    @abstractmethod
    def _dict_lambda(cls) -> t.Dict[
        str, t.Callable[[str, str, int, str, t.Any], t.Dict[str, t.Any]]
    ]:
        raise NotImplementedError
    
    CLS_REGISTRY = {}
    def __init_subclass__(cls, measure):
        TooltipFigureMetaABC.CLS_REGISTRY[measure] = cls




def retrieve_measure_tooltip_interface(measure: str) -> TooltipFigureMetaABC:
    """
    Retrieve the tooltip metadata interface for the indicated `measure`.

    Parameters
    ----------
    measure
        The indicated measure of interest.

    Returns
    -------
    A subclass of :py:class:`TooltipFigureMetaABC`, which supports the
    `get_metadata` class method.
    """
    meta_interface = TooltipFigureMetaABC.CLS_REGISTRY.get(measure)
    return meta_interface