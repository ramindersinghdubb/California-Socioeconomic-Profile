"""
Objects and functions for handling database queries/reads.
"""
import json
import sys
from pathlib import Path
from functools import reduce

import yaml
import sqlalchemy
import pandas as pd
import geopandas as gpd
from sqlalchemy.sql.elements import quoted_name

sys.path.insert(0, str(Path.cwd()))
from ingestion.config import CONFIG_SETTINGS as INGESTION_CONFIG_SETTINGS


class CloudReadData:
    """
    Interface for handling the reading of data files from the cloud/GCP-hosted
    relational database.
    """

    @classmethod
    def get_cali_tracts_data(
        cls, conn: sqlalchemy.Connection, place: str, year: int, measure: str
    ) -> pd.DataFrame:
        """
        Retrieve the :py:class:`pandas.DataFrame` instance corresponding
        to the selected place, calendar year, and measure/topic.

        Parameters
        ----------
        conn
            A(n) :py:class:`sqlalchemy.Connection` to the PostGIS database.

        place
            The indicated Californian place/city.

        year
            The indicated calendar year.

        measure
            The indicated measure/topic of interest.

        Returns
        -------
        A(n) :py:class:`pandas.DataFrame` containing information for the
        selected place, year, and measure.
        """
        sql_statement = cls._cali_tract_sql_statement(measure, place, year)
        results = conn.execute(sql_statement)
        df = pd.DataFrame(
            data    = list(results.fetchall()),
            columns = list(results.keys()),
        )
        df = df.loc[:, ~df.columns.duplicated()].copy()
        df = cls.__name_coerce(df)
        return df
    
    @classmethod
    def __name_coerce(
        cls, df: pd.DataFrame
    ) -> pd.DataFrame:
        df['NAME'] = 'Census Tract ' + df['TRACT'].str.slice(0, 4) + '.' + df['TRACT'].str.slice(4)
        col_order = ['NAME'] + [col for col in df.columns if col != 'NAME']
        df = df[col_order]
        return df

    @classmethod
    def _cali_tract_sql_statement(
        cls, topic: str, place: str, year: int
    ) -> sqlalchemy.TextClause:
        geog_scopes = {'state': '06', 'tract': '*'}
        where_condition = _sql_cali_tract_where_clause(place, year)
        sql_tbls = [quoted_name(tbl, quote=True) for tbl in cls.__list_sql_tables(geog_scopes, topic, year)]

        select_clause = "SELECT *\n"
        from_clause = f'FROM "{sql_tbls[0]}"\n'
        join_clause = ''
        for idx in range(0, len(sql_tbls) - 1):
            join_clause += f'JOIN "{sql_tbls[idx+1]}" ON "{sql_tbls[idx]}"."GEO_ID"="{sql_tbls[idx+1]}"."GEO_ID"'
            join_clause += '\n'
        where_clause = f'WHERE "{sql_tbls[0]}"."GEO_ID" in :geo_ids;'
        
        sql_statement = ''.join([select_clause, from_clause, join_clause, where_clause])
        sql_statement = sqlalchemy.text(sql_statement).bindparams(
            sqlalchemy.bindparam(key="geo_ids", value=where_condition, expanding=True)
        )

        return sql_statement

    @classmethod
    def __list_sql_tables(
        cls, geog_scopes: dict, topic: str, year: int
    ) -> list[str]:
        """
        Return the list of SQL table names.
        """
        topics_dict = cls.__get_table_support(geog_scopes)
        if topic not in topics_dict:
            raise KeyError(
                f"'{topic}' was not recognized from the configuration file. "
                f"Supported topics include one of: {list(topics_dict)}"
            )
        if (tbls:=topics_dict[topic].get(year, None)) is None:
            years = list(sorted(topics_dict[topic]))
            raise KeyError(
                f"The '{topic}' topic does not support the {year} calendar year. "
                f"Supported years in the database include one of: {years}"
            )
        gs_name  = cls.__geographic_path_tbl_component(geog_scopes)
        id_sql_tbl = f'{gs_name}_{year}'
        sql_tbls   = [f'{gs_name}_{tbl}_{year}' for tbl in tbls]
        return [id_sql_tbl, *sql_tbls]
    
    @classmethod
    def __get_table_support(cls, geog_scopes: dict) -> dict[int, dict[str, list[str]]]:
        """
        Using the configuration files, return a dictionary such that:
            { topic: {year: tables} }
        """
        config   = _read_config()
        metadata = _read_metadata()
        try:
            inner = list(geog_scopes)[-1]
            apis = metadata['API_SEARCH'][inner]
        except:
            raise KeyError(
                f"The entered geographic pathway, {geog_scopes}, was not qualified "
                f"in the configuration search setting. Supported inner scopes from "
                f"the search setting include one of: {list(metadata['API_SEARCH'])}."
            ) from None
        support = [i for i in config['TABLE_SUPPORT'] if (list(geog_scopes) in i['compatible_scopes'])
                   and any(i['dataset'] == j for j in apis)]
        
        years = list(set(sorted([i['year'] for i in support])))
        year_tbl_dict = {}
        for year in years:
            tbls = [i['tables'] for i in support if i['year'] == year]
            year_tbl_dict[year] = reduce(lambda x, y: x + y, tbls)

        topic_dict = metadata['CENSUS_BUREAU_TABLES_BY_TOPIC']
        
        topic_support_dict = {}
        for topic, tbls in topic_dict.items():
            dummy_dict = {}
            for year, tables in sorted(year_tbl_dict.items()):
                if len(support:=[i for i in tables if i in tbls]) > 0:
                    dummy_dict[year] = support
            topic_support_dict[topic] = dummy_dict

        return topic_support_dict
    
    @classmethod
    def __geographic_path_tbl_component(
        cls, geog_scopes: dict,
    ) -> str:
        """Formatting for the TIGER shapefile table name."""
        geo_spec= {k: 'ALL' if v == '*' else v for k, v in geog_scopes.items()}
        gs_name = '_'.join([f'{k}{v}' for k, v in geo_spec.items()])
        return gs_name


class CloudReadTigerData:
    """
    Interface for handling the reading of TIGER shapefiles from the
    cloud/GCP-hosted relational database.
    """

    @classmethod
    def get_cali_tracts(
        cls, conn: sqlalchemy.Connection, place: str, year: int
    ) -> gpd.GeoDataFrame:
        """
        Retrieve the :py:class:`geopandas.GeoDataFrame` instance corresponding
        to the selected place and calendar year.

        Parameters
        ----------
        conn
            A(n) :py:class:`sqlalchemy.Connection` to the PostGIS database.

        place
            The indicated Californian place/city.

        year
            The indicated calendar year.

        Returns
        -------
        A(n) :py:class:`geopandas.GeoDataFrame` containing information for
        the selected place and year.
        """
        crs_df = cls._get_crs_df(conn)
        tract_tbl, sql_statement = cls._cali_tract_sql_statement(place, year)
        gdf = cls._read_gdf(conn, crs_df, tract_tbl, sql_statement)
        return gdf
        
    @classmethod
    def _get_crs_df(cls, conn: sqlalchemy.Connection) -> pd.DataFrame:
        """
        A(n) :py:class:`pandas.DataFrame` object containing information
        on the Coordinate Referencing System of all TIGER shapefile data
        tables in the database.
        """
        query = conn.execute(sqlalchemy.text("SELECT * FROM tiger_srid_info;"))
        df    = pd.DataFrame(data = list(query.fetchall()), columns=['TABLE', 'SRID'])
        return df
    
    @classmethod
    def _cali_tract_sql_statement(
        cls, place: str, year: int,
    ) -> tuple[str, sqlalchemy.TextClause]:
        """
        Generate the SQL statement for reading geometric information for
        the selected Californian city and the selected year, and the indicated
        table name.
        """
        tract_tbl = quoted_name(f'tiger_state06_tractALL_{year}', quote=True)
        condition = _sql_cali_tract_where_clause(place, year)
        
        sql_statement = f"""
        SELECT CONCAT("STATEFP", "COUNTYFP", "TRACTCE") AS "GEO_ID", "geom"
        FROM "{tract_tbl}"
        WHERE CONCAT("STATEFP", "COUNTYFP", "TRACTCE") in :geo_ids;
        """
        stmt = sqlalchemy.text(sql_statement).bindparams(
            sqlalchemy.bindparam(key="geo_ids", value=tuple(condition), expanding=True)
        )
        return tract_tbl, stmt

    @classmethod
    def _read_gdf(
        cls,
        conn: sqlalchemy.Connection,
        crs_df: pd.DataFrame,
        tbl_name: str,
        sql_statement: sqlalchemy.TextClause
    ) -> gpd.GeoDataFrame:
        """
        Retrive the `geopandas.GeoDataFrame` for the corresponding `tbl_name`.
        """
        crs = cls._get_crs(crs_df, tbl_name)
        gdf = gpd.read_postgis(
            sql_statement, con = conn, crs = crs
        )
        gdf.rename(columns={'geom': 'geometry'}, inplace=True)
        gdf.set_geometry(col = "geometry", inplace=True)
        return gdf

    @classmethod
    def _get_crs(cls, crs_df: pd.DataFrame, tbl_name: str) -> str:
        """
        Get the SRID/CRS for the stipulated table.
        """
        crs = crs_df['SRID'][crs_df['TABLE'] == tbl_name].iloc[0]
        return crs
    



def _sql_cali_tract_where_clause(place: str, year: int) -> list[str]:
    """
    Generate the WHERE clause condition for SQL statements. Specifically,
    list the values of the 'GEO_ID' column (found in all tables, whether
    that be the TIGER shapefile tables or the data tables) for which to
    select.
    
    Parameters
    ----------
    place
        The selected Californian city/place.

    year
        The selected calendar year.
    """
    metadata_df = _read_cali_tract_metadata_df()
    
    if place not in metadata_df['PLACENAME'].unique().tolist():
        raise KeyError(f"The indicated city, '{place}', does not exist.")
    if year not in metadata_df['YEAR'].unique().tolist():
        raise KeyError(f"The indicated calendar year, {year}, does not exist.")
    
    mask = (metadata_df['YEAR'] == year) & (metadata_df['PLACENAME'] == place)
    in_clause = metadata_df[mask]['GEO_ID'].unique().tolist()

    return in_clause


def _read_cali_tract_metadata_df() -> pd.DataFrame:
    """
    Retrieve the `pandas.DataFrame` object consisting of metadata on
    Californian census tracts.
    """
    config_folder = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER'])
    file = config_folder / 'tract_metadata.csv'
    df = pd.read_csv(file, dtype={'GEO_ID': object})
    df = df[['YEAR', 'PLACENAME', 'GEO_ID']].copy()
    return df


def _read_config() -> dict:
    """
    Read the ingestion configuration JSON file.
    """
    file_path = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'config.json'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content

def _read_metadata() -> dict:
    """
    Read the ingestion configuration YAML file.
    """
    file_path = Path(INGESTION_CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'metadata.yaml'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
    return content