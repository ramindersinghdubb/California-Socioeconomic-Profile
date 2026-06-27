"""
Abstract base classes.
"""

import typing as t
from abc import ABC, abstractmethod
from collections import defaultdict

import pandas as pd
import numpy as np



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
        df: pd.DataFrame
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


    @classmethod
    def generate_variables(
        cls,
        base: str,
        first_var: int,
        last_var: int,
        num_zeros: int = 3,
        var_type: t.Literal['E', 'PE'] = 'E'
    ) -> t.List[str]:
        """
        Helper method for generating a list of variables.

        This is particularly useful as the Census purposefully designs the format of
        their variables in such a way as to ensure general categories of information
        are organized and placed close to each other (e.g. estimates decomposed by
        racial status are placed next to one another).

        Parameters
        ----------
        base
            The base string.

        first_var
            The integer specifying the location of the first variable.

        last_var
            The integer specifying the location of the last variable.

        num_zeros
            The number of zeros to pad around variables. Default '3'.

            Note that '3' represents the padding for ACS Detailed or Subject Table info.
            '4' is recommended for ACS Data Profiles.

        var_type
            Indicate whether the variables are of estimate ('E') type or percent estimate
            ('PE') type. Default 'E'.
        """
        vars = [
            f'{base}{str(i).zfill(num_zeros)}{var_type}'
            for i in range(first_var, last_var + 1)
        ]
        return vars
    
    @classmethod
    def generate_binned_qualitative_colors(
        cls,
        bins: t.List[t.Any],
        color_array: t.List[str],
        series: pd.Series,
        default_color: str = '#000000'
    ) -> t.List[str]:
        """
        Generate a color array by binning the `series` in bins according to
        `bins`.

        Note that `color_array` must be of length 1 less than that of `bins`.

        Parameters
        ----------
        bins
            A list of numbers representing the locations of the various bins.

        color_array
            A list of colors.

            Note that the length of this list must be one less than that of
            `bins`.

        series
            The indicated `pandas.Series` object comprising integer or float
            values.

        default_color
            The color to default to for values that may fall outside the
            specified bins.
        """
        binned_series = pd.cut(series.replace({None: np.nan}).astype(float), bins=bins, labels=color_array)
        color_series  = binned_series.astype(object).fillna(default_color)
        color_array   = color_series.tolist()
        return color_array
    
    @classmethod
    def get_long_df_values_populations(
        cls,
        df: pd.DataFrame,
        value_vars: t.List[str],
        population_vars: t.List[str],
        labels: t.List[str],
        total_vars: t.Optional[t.Union[str, t.List[str]]] = None
    ) -> pd.DataFrame:
        """
        Retrive a neatly formatted `pandas.DataFrame` object of 'long' format,
        comprising estimate data on the selected measure of interest and the 
        corresponding population of interest.

        Parameters
        -----------
        df
            A(n) :py:class:`pandas.DataFrame` object.

        value_vars
            The first set of column(s). These correspond to some metric (such as dollar value,
            percentage value, etc.).
        
        population_vars
            The second set column(s). These correspond to the underlying population from which
            `value_vars` were drawn from.
            
            For instance, if `value_vars` represent a metric estimating the percentage of renters
            who are rent-burdened by age, `population_vars` represents the corresponding population,
            i.e. from relative terms (in percentage) to absolute terms.

        labels
            A list of strings renaming the `value_vars` or `population_vars`. This ensures coherence
            when identifying which variable comes with which.

        total_vars
            If a list, this indicates the total population corresponding to each variable (e.g. in
            context of the earlier framed example, the total population of renters by age *regardless*
            of characteristic).

            If a string, this indicates the absolute total population (e.g. the total population of
            renters, without qualification).

            If `None`, this indicates the user does not wish to supply this information.
        """

        id_vars     = ['NAME']
        common_vars = ['NAME', 'VARIABLE']
        if isinstance(total_vars, str):
            id_vars.append(total_vars)
            common_vars.append(total_vars)

        var_df = cls._melt_df(df, id_vars, value_vars, labels, 'VALUE')
        pop_df = cls._melt_df(df, id_vars, population_vars, labels, 'POPULATION')
        
        if isinstance(total_vars, list):
            tot_df = cls._melt_df(df, id_vars, total_vars, labels, 'TOTAL')
            pop_df = pop_df.merge(tot_df, on = common_vars)

        df = var_df.merge(pop_df, on = common_vars)

        del var_df
        del pop_df

        return df
    
    @classmethod
    def _melt_df(
        cls,
        df: pd.DataFrame,
        id_vars: t.List[str],
        value_vars: t.List[str],
        labels: t.List[str],
        value_name: str
    ) -> pd.DataFrame:
        """
        Retrieve a 'long' format `pandas.DataFrame` object.

        Parameters
        ----------
        df
            A(n) :py:class:`pandas.DataFrame` object.

        id_vars
            The column(s) to use as identifier variables.
        
        value_vars
            The column(s) to unpivot.

        labels
            The corresponding label(s) for the column(s) being unpivoted.

        value_name
            The name of the 'value' column.
        """
        ddf = df.copy(deep=True)

        ddf = ddf.rename(columns = dict(zip(value_vars, labels)))
        ddf = ddf.melt(
            id_vars    = id_vars,
            value_vars = labels,
            var_name   = 'VARIABLE',
            value_name = value_name
        )
        return ddf



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