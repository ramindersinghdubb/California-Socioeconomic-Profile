"""
Metadata for formatting the `plotly.graph_object.Figure`
instance used in the `dcc.Graph(id='map', ...)` component.
"""

import typing as t
from warnings import catch_warnings

import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
from plotly.graph_objects import Figure

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from ingestion.config import CONFIG_SETTINGS as INGESTION_CONFIG_SETTINGS
from page_components.config import CONFIG_SETTINGS as APP_CONFIG_SETTINGS


class ChoroplethMapInterface:
    """
    Interface for collecting critical styling information to be
    passed to the `plotly.graph_object.Figure`.
    """

    @classmethod
    def get_figure(
        cls, df: pd.DataFrame, gdf: gpd.GeoDataFrame, place: str, year: int, measure: str
    ) -> Figure:
        """
        Retrieve the `plotly.graph_objects.Figure` for the indicated place, calendar year,
        and measure of interest.

        Parameters
        ----------
        df
            The `pandas.DataFrame` instance retrieved from the SQL query.

        gdf
            The `geopandas.GeoDataFrame` instance retrieved from the SQL query.

        place
            The indicated city/place from the dropdown selection.

        year
            The indicated calendar year from the dropdown selection.

        measure
            The indicated measure of interest from the dropdown selection.
        """
        metadata = cls._format_metadata(df, gdf, year, measure)

        fig = px.choropleth_map(
            metadata['dataframe'],
            geojson     = gdf.__geo_interface__,
            locations   = 'GEO_ID',
            featureidkey= 'properties.GEO_ID',
            color       = metadata['color'],
            custom_data = ['NAME', 'YEAR'],
            color_continuous_scale = metadata['color_scale'],
            map_style   = 'streets',
            opacity     = 0.6,
            zoom        = 10,
            center      = {
                'lat': round(metadata['center_point'].y, 8),
                'lon': round(metadata['center_point'].x, 8)
            },
        )

        fig = fig.update_layout(
            autosize    = True,
            margin      = {"r": 0, "t": 0, "l": 0, "b": 0},
            hoverlabel  = {
                'align': 'left'
            },
            coloraxis   = dict(
                colorbar = {
                    'outlinewidth': 2,
                    'outlinecolor': '#020403',
                    'ticklabelposition': 'outside bottom',
                    'tickprefix': metadata['tick_prefix'],
                    'ticksuffix': metadata['tick_suffix'],
                    'title': {
                        'font': {'color': '#020403', 'weight': 500},
                        'text': metadata['colorbar_title']
                    },
                    'tickfont': {
                        'weight': 500
                    }
                }
            ) 
        )

        fig = fig.update_traces(
            hovertemplate = "<b style='font-size:16px;'>%{customdata[0]}</b>&nbsp;&nbsp;&nbsp;&nbsp;<br>" +
                "<span style='font-family: Trebuchet MS, sans-serif;'>" + place + ", " + str(year) +
                "</span><br><br>" + "<span style='font-family: Trebuchet MS, sans-serif;>" +
                metadata['colorbar_title'].replace('<br>', ' ') + "</span>: <b>" + metadata['tick_prefix']
                + "%{z:,.0f}" + metadata['tick_suffix'] + "</b>&nbsp;&nbsp;&nbsp;&nbsp;<extra></extra>",
            hoverlabel = {
                'bgcolor': '#FAFAFA',
                'bordercolor': '#111810',
                'font': {
                    'color': '#020403'
                }
            },
            marker = {
                'line': {'color': '#020403', 'width': 1.25},
                'opacity': 0.6,
            }
        )

        return fig

    @classmethod
    def _format_metadata(
        cls, df: pd.DataFrame, gdf: gpd.GeoDataFrame, year: int, measure: str
    ) -> dict[str, t.Any]:
        """
        Return a neatly formated look-up table consisting of critical information
        to pass to the `plotly.graph_object.Figure` instantiated when using the
        `plotly.express.choropleth_map` function.

        Parameters
        ----------
        df
            The `pandas.DataFrame` instance retrieved from the SQL query.

        gdf
            The `geopandas.GeoDataFrame` instance retrieved from the SQL query.

        year
            The indicated calendar year from the dropdown selection.

        measure
            The indicated measure of interest from the dropdown selection.

        Returns
        -------
        A `dict` instance. The key-value pairs of this instance will ultimately be
        used in the downstream/higher-level instantiation of the figure.
        """
        metadata = cls._dict_lambda()[measure]()

        # Due to variable label changes over the years, and specific formulas for
        # otherwise desired information, there may be such cases whereby different
        # variables must be specified according to a callable. This step handles
        # that.
        if metadata.get('new_var', False):
            def apply_func(row, year):
                try:
                    result = metadata['new_var'](row, year)
                    return result if result > 0 else np.nan
                except:
                    return np.nan
            df[metadata['color']] = df.apply(apply_func, axis=1, args=(year,))
            metadata.pop('new_var')

        # Inflation-adjust columns
        if metadata.get('inflation_adjust', False):
            current_year = max(APP_CONFIG_SETTINGS['YEARS'])
            df = cls.__inflation_adjust_cols(df, current_year, metadata['color'])
            metadata.pop('inflation_adjust')

        # Create a name column (to display in the hover text)
        df['NAME'] = 'Census Tract ' + df['TRACT'].str.slice(0, 4) + '.' + df['TRACT'].str.slice(4)
        col_order = ['NAME'] + [col for col in df.columns if col != 'NAME']
        df = df[col_order].copy()

        metadata['dataframe'] = df
        
        # Retrieve the center-point of all geometries
        with catch_warnings(action = 'ignore'):
            display = df[(df[metadata['color']] != 0)]
            display = display[~display[metadata['color']].isna()][['GEO_ID']]
            gdf = gdf.merge(display, on='GEO_ID')
            metadata['center_point'] = gdf.dissolve().centroid[0]

        metadata['colorbar_title'] = metadata.get('colorbar_title', "")
        metadata['tick_prefix']    = metadata.get('tick_prefix', "")
        metadata['tick_suffix']    = metadata.get('tick_suffix', "")
        
        return metadata
    
    @classmethod
    def __inflation_adjust_cols(
        cls, df: pd.DataFrame, current_year: int, cols: t.Union[str, list[str]]
    ) -> pd.DataFrame:
        """
        Inflation-adjust the indicated columns (`cols`) in the dataframe (`df`)
        to the specified calendar year.

        Note: `current_year` *must* be present in the R-CPI-U-RS CSV file. It is
        ultimately determined by the most recent year in the configuration file
        for the app.
        """
        cols = cols if isinstance(cols, list) else [cols]
        current_year_adj = f'{current_year}_ADJ_FACTOR'

        cpi_df = cls.__cpi_df()[['YEAR', current_year_adj]]

        df = pd.merge(df, cpi_df, on = ['YEAR'], how = 'left')
        for col in cols:
            df[col] = round(df[col] * df[current_year_adj])

        df = df.drop(columns = [current_year_adj])

        return df
    
    @classmethod
    def __cpi_df(cls) -> pd.DataFrame:
        file = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'r-cpi-u-rs.csv'
        df   = pd.read_csv(file)
        return df

    @classmethod
    def _dict_lambda(cls) -> dict[str, t.Callable[[], dict[str, t.Any]]]:
        return {
            'Contract Rent': cls._fig_metadata_ContractRent,
            'Economic Measures': cls._fig_metadata_EconomicMeasures,
            'Education': cls._fig_metadata_Education,
            'Employment Statistics': cls._fig_metadata_EmploymentStatistics,
            'Food Stamps': cls._fig_metadata_FoodStamps,
            'Health Insurance Coverage': cls._fig_metadata_HealthInsuranceCoverage,
            'Household Income': cls._fig_metadata_HouseholdIncome,
            'Housing Units and Occupancy': cls._fig_metadata_HousingUnitsandOccupancy,
            'Population': cls._fig_metadata_Population,
            'Poverty': cls._fig_metadata_Poverty,
            'Rent Burden': cls._fig_metadata_RentBurden,
            'Transportation Methods to Work': cls._fig_metadata_TransportationMethodstoWork,
            'Work Hours': cls._fig_metadata_WorkHours
        }

    @classmethod
    def _fig_metadata_ContractRent(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['B25058_001E'],
            'color': 'MedianContractRent', # Median contract rent
            'color_scale': px.colors.sequential.YlOrRd,
            'tick_prefix': '$',
            'colorbar_title': 'Median<br>Contract<br>Rent (USD)'
        }

        return metadata


    @classmethod
    def _fig_metadata_EconomicMeasures(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['DP03_0009PE'],
            'color': 'UnempRate', # Unemployment rate percent estimate
            'color_scale': px.colors.sequential.Hot_r,
            'tick_suffix': '%',
            'colorbar_title': 'Unemploy.<br>Rate'
        }

        return metadata


    @classmethod
    def _fig_metadata_Education(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['B15001_001E'],
            'color': 'Total18andOverPop', # Total 18 and older population
            'color_scale': px.colors.sequential.Blues,
            'colorbar_title': '18+<br>Population'
        }

        return metadata


    @classmethod
    def _fig_metadata_EmploymentStatistics(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S2301_C02_001E'] / row['S2301_C02_001E'] if year < 2015 else row['S2301_C02_001E'],
            'color': 'LaborForcePartRate', # LFPR, for civilian 16 and older population
            'color_scale': px.colors.sequential.Viridis,
            'tick_suffix': '%',
            'colorbar_title': 'Labor<br>Force<br>Particip.<br>Rate'
        }

        return metadata


    @classmethod
    def _fig_metadata_FoodStamps(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: (row['S2301_C02_001E'] / row['S2301_C02_001E']) if year < 2015 else row['S2201_C04_001E'],
            'color': 'HouseholdFoodStampRecpPerc', # Percentage of households who self-report as food stamps recipients
            'color_scale': px.colors.sequential.Magma_r,
            'tick_suffix': '%',
            'colorbar_title': 'Percent of<br>Households<br>Receiving<br>Food Stamps'
        }

        return metadata


    @classmethod
    def _fig_metadata_HealthInsuranceCoverage(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S2701_C03_001E'] if year < 2015 else row['S2701_C05_001E'],
            'color': 'UninsuredPercent', # Percentage of uninsured for the civilian noninstitutionalized population
            'color_scale': px.colors.sequential.Oranges,
            'tick_suffix': '%',
            'colorbar_title': 'Uninsured<br>Percent of<br>Civilians<br>'
        }

        return metadata


    @classmethod
    def _fig_metadata_HouseholdIncome(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S1901_C01_012E'],
            'color': 'MedianIncome', # Median income
            'inflation_adjust': True,
            'color_scale': px.colors.sequential.Emrld,
            'tick_prefix': '$',
            'colorbar_title': f'Real Median<br>Income ({max(APP_CONFIG_SETTINGS['YEARS'])} USD)'
        }

        return metadata


    @classmethod
    def _fig_metadata_HousingUnitsandOccupancy(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['DP04_0002PE'],
            'color': 'OccPerc', # Percentage of housing units that are occupied
            'color_scale': px.colors.sequential.Mint,
            'tick_suffix': '%',
            'colorbar_title': 'Occupancy<br>Rate'
        }

        return metadata


    @classmethod
    def _fig_metadata_Population(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['DP05_0001E'],
            'color': 'TotalPop', # Total poulation
            'color_scale': px.colors.sequential.Blues,
            'colorbar_title': 'Total<br>Population'
        }

        return metadata


    @classmethod
    def _fig_metadata_Poverty(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S1701_C03_001E'],
            'color': 'PovertyPerc', # Percentage of population below poverty level
            'color_scale': px.colors.sequential.Hot_r,
            'tick_suffix': '%',
            'colorbar_title': 'Poverty<br>Rate'
        }

        return metadata


    @classmethod
    def _fig_metadata_RentBurden(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: ((row['B25070_007E'] + row['B25070_008E'] + row['B25070_009E'] + row['B25070_010E']) / (row['B25070_001E'])) * 100, 
            'color': 'RentBurden', # Percentage of rent burdened renters (30% or more income to rent)
            'color_scale': px.colors.sequential.YlOrRd,
            'tick_suffix': '%',
            'colorbar_title': 'Percent of<br>Rent-Burdened<br>Renters'
        }

        return metadata


    @classmethod
    def _fig_metadata_TransportationMethodstoWork(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S0801_C01_046E'],
            'color': 'MeanTravelTimeMins', # Mean travel time (in minutes)
            'color_scale': px.colors.sequential.Oranges,
            'tick_suffix': 'mins.',
            'colorbar_title': 'Average Travel<br>Times (mins.)'
        }

        return metadata


    @classmethod
    def _fig_metadata_WorkHours(cls) -> dict:
        metadata = {
            'new_var': lambda row, year: row['S2303_C01_018E'] if year < 2015 else row['S2303_C01_031E'],
            'color': 'MeanWeeklyHours', # Mean weekly hours worked for 16-to-64 workers
            'color_scale': px.colors.sequential.Purples,
            'tick_suffix': 'hrs.',
            'colorbar_title': 'Average Hours<br>Worked Weekly'
        }

        return metadata