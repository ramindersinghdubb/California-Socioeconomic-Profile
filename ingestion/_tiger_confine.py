"""
Functions for extracting only those California census tracts
that intersect with the geographical regions implied by
the TIGER shapefiles for California cities.
"""
import typing as t

import sqlalchemy
import pandas as pd
import geopandas as gpd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from ingestion.config import CONFIG_SETTINGS
from ingestion.utils import get_california_fips_df


def _get_crs_df(conn: sqlalchemy.Connection) -> pd.DataFrame:
    """
    Retrieve the SRID/CRS metadata for each of the cached TIGER shapefiles.

    Parameters
    ----------
    conn
        A(n) `sqlalchemy.Connection` to a PostGIS database.

    Returns
    -------
    A `pandas.DataFrame` instance whose columns are:
    - 'TABLE', indicating the table name
    - 'SRID', indicating the SRID/CRS
    """
    query = conn.execute(sqlalchemy.text("SELECT * FROM tiger_srid_info;"))
    df    = pd.DataFrame(data = list(query.fetchall()), columns=['TABLE', 'SRID'])
    
    return df


def _table_years(conn: sqlalchemy.Connection) -> t.List[int]:
    """
    List the calendar years for which TIGER shapefiles are available for both census
    tracts and cities.

    Without this, a situation may arise when one of the inner (census tract-level maps)
    or the outer (city-level maps) are unavailable. This is to ensure cohesion.

    Parameters
    ----------
    conn
        A(n) `sqlalchemy.Connection` to a PostGIS database.

    Returns
    -------
    A list of calendar years for which both sets of map data are available.
    """
    fetch = conn.execute(
        sqlalchemy.text(
            """
            SELECT table_name FROM information_schema.tables
            WHERE table_type='BASE TABLE' AND table_schema='public';
            """
        )
    )
    tbls = [i[0] for i in fetch.fetchall()]
    tract_yrs = [int(i.split('_')[-1]) for i in tbls if i.startswith('tiger_state06_tractALL')]
    place_yrs = [int(i.split('_')[-1]) for i in tbls if i.startswith('tiger_state06_placeALL')]
    years     = [yr for yr in place_yrs if yr in tract_yrs]

    return years


def _confine(
    outer_gdf: gpd.GeoDataFrame,
    inner_gdf: gpd.GeoDataFrame,
    inner_gdf_crs: str,
    threshold: t.Union[int, float] = 0.8
) -> gpd.GeoDataFrame:
    """
    Confine the `inner_gdf` to the boundaries implied by the `outer_gdf`.

    Parameters
    ----------
    outer_gdf
        The outer `geopandas.GeoDataFrame` to which to reference to.

    inner_gdf
        The inner `geopandas.GeoDataFrame` which must be confined.

    inner_gdf_crs
        The CRS/SRID of the inner `geopandas.GeoDataFrame`.

    threshold
        The percentage of intersecting areas that overlap with the original
        areas. Greater values indicate strict adherence (i.e. intersecting
        areas must have a greater proportion in common with their original
        areas). Default 0.8.

    Returns
    -------
    A `geopandas.GeoDataFrame` instance comprising the confined data.
    """
    if (threshold > 1) or (threshold < 0):
        raise ValueError("Threshold value can only be between 0 and 1.")
    
    # Preserve the originals
    c_outer_gdf = outer_gdf.copy()
    c_inner_gdf = inner_gdf.copy()
    
    # Project to Web-Mercator
    c_outer_gdf.to_crs(3857, inplace=True)
    c_inner_gdf.to_crs(3857, inplace=True)

    # Keep the geometries
    c_inner_gdf['inner_geometry'] = c_inner_gdf.geometry
    c_outer_gdf['outer_geometry'] = c_outer_gdf.geometry

    # Confining
    confined_data = c_inner_gdf.sjoin(
        c_outer_gdf,
        how = 'inner',
        predicate = 'intersects',
        lsuffix = 'inner',
        rsuffix = 'outer'
    )

    # Thresholding
    thresholded_data: gpd.GeoDataFrame = confined_data[
        confined_data['inner_geometry'].intersection(confined_data['outer_geometry']).area >=
        0.6 * confined_data['inner_geometry'].area
    ]

    # Cleaning
    thresholded_data.drop(columns = ['inner_geometry', 'outer_geometry',
                                     *[col for col in thresholded_data if col.endswith('_outer')]],
                                     inplace = True)
    thresholded_data.columns = [col.rstrip('_inner') for col in thresholded_data.columns]
    thresholded_data.reset_index(drop = True, inplace=True)

    # Restore to the original/inner CRS
    thresholded_data.to_crs(inner_gdf_crs, inplace=True)

    return thresholded_data

def _get_crs(crs_df: pd.DataFrame, tbl_name: str) -> str:
    """
    Get the SRID/CRS for the stipulated table.
    """
    crs = crs_df['SRID'][crs_df['TABLE'] == tbl_name].iloc[0]
    return crs

def _read_gdf(conn: sqlalchemy.Connection, crs_df: pd.DataFrame, tbl_name: str) -> gpd.GeoDataFrame:
    """
    Retrive the `geopandas.GeoDataFrame` for the corresponding `tbl_name`.
    """
    crs = _get_crs(crs_df, tbl_name)
    gdf = gpd.read_postgis(
        'SELECT * FROM "{}";'.format(tbl_name),
        con = conn,
        crs = crs
    )
    gdf.set_geometry("geom", inplace=True)
    return gdf


def _write_tract_metadata(conn: sqlalchemy.Connection) -> None:
    """
    Write metadata on census tracts located within cities.
    """
    crs_df  = _get_crs_df(conn)
    d_years = _table_years(conn)
    file = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'tract_metadata.csv'
    if file.exists():
        df = pd.read_csv(file)
        p_years = df['YEAR'].unique().tolist()
        d_years = [yr for yr in d_years if yr not in p_years]

    dfs = []
    for year in sorted(d_years):
        tract_tbl = f'tiger_state06_tractALL_{year}'
        place_tbl = f'tiger_state06_placeALL_{year}'

        tract_gdf = _read_gdf(conn, crs_df, tract_tbl)
        place_gdf = _read_gdf(conn, crs_df, place_tbl)

        confined_gdf = _confine(place_gdf, tract_gdf, str(tract_gdf.crs))
        confined_gdf.drop(columns=['geom'], inplace=True)
        confined_gdf['GEO_ID'] = confined_gdf['STATEFP'] + confined_gdf['COUNTYFP'] + confined_gdf['TRACTCE']
        confined_gdf['PLACE_FIPS'] = confined_gdf['STATEFP'] + confined_gdf['PLACEFP']
        meta_df = confined_gdf[['YEAR', 'PLACE_FIPS', 'GEO_ID']].copy()
        dfs.append(meta_df)
    
    if len(dfs) > 0:
        df = pd.concat(dfs, axis=0)
        CA_DF = get_california_fips_df()
        CA_DF.rename(columns = {'GEO_ID': 'PLACE_FIPS', 'COUNTIES': 'COUNTY'}, inplace=True)
        df = df.merge(CA_DF, on='PLACE_FIPS')
        df.sort_values(by=['YEAR', 'PLACE_FIPS'], inplace=True)


        df.to_csv(file, mode = 'a' if file.exists() else 'w', index=False)