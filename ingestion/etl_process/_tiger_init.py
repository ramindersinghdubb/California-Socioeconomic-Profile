"""
Interface for handling TIGER Shapefile ingestion.
"""
from __future__ import annotations
import logging
import traceback
import warnings
import typing as t
from re import sub

import sqlalchemy
import pandas as pd
import geopandas as gpd
from acspsuedo.source.shpfile import shapefile_handler

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from ingestion.etl_process.custom_warnings import TigerShapefileNotFoundWarning
from ingestion.etl_process.metadata import (
    _read_config,
    _read_metadata
)
from ingestion.config import CONFIG_SETTINGS

shapefile_handler.auto_cache = True


logging.basicConfig(
    filename = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'log.log',
    filemode = 'a',
    format   = "%(asctime)s - %(filename)s, Line %(lineno)s - %(levelname)s: %(message)s",
    datefmt  = "%m-%d-%Y, %I:%M:%S %p",
    level    = logging.INFO
)
tiger_logger = logging.getLogger(__name__)



class _TigerHandlerInterface:
    def __init__(
        self,
        connection: sqlalchemy.Connection,
    ):
        """
        Initialization for the :py:class:`EtlProcess` TigerHandlerInterface.

        Parameters
        ----------
        connection
            A `sqlalchemy.Connection`. Represents the Postgres database for the ingested data.
        """
        self._connection = connection

        # Internal for caching CRS info lost when writing to the database.
        self._crs_points: t.List[t.Dict[str, t.Any]] = []


    @property
    def connection(self):
        """
        A `sqlalchemy.Connection`. Represents the Postgres database for the ingested data.
        """
        return self._connection
    
    @connection.setter
    def connection(self, new_connection: sqlalchemy.Connection):
        self._folder = new_connection

    @connection.deleter
    def connection(self):
        raise AttributeError("Cannot have an uninitialized connection.")
    

    def _tiger_query(
        self, *paths: t.Dict[str, t.Any]
    ) -> None:
        """
        **For PostgreSQL databases only**. Indicate whether or not to *attempt* to
        ingest TIGER shapefiles for the indicated paths.

        Note that TIGER shapefiles may not be uniformly available for all paths for
        some reasons (inconsistent naming convention, generally unavailability).
        Nonetheless, we make every effort to query and ingest these shapefiles, for
        potential developer use thereafter.
        """
        self.__check_postgis_installation()
        tables = self.__database_tables()
        for path in paths:
            self.__tiger_query(path, tables)
        if len(self._crs_points) > 0:
            self.__crs_metadata_table()
    
    def __tiger_query(
        self, path: t.Dict[str, t.Any], tables: t.List[str]
    ) -> None:
        """
        Conduct queries to the TIGER shapefile database for the given path.
        """
        path, years   = self.__get_path_support_years(path)
        tbl_name_comp = self.__geographic_path_tbl_component(path)

        p_years = [int(i.removeprefix(f'{tbl_name_comp}_')) for i in tables if i.startswith(tbl_name_comp)]
        d_years = [yr for yr in years if yr not in p_years]

        tiger_logger.info(
            'Beginning query attempts to TIGER database for the path: %s. Indicated download '
            'years for this path from the configuration settings: %s.',
            path, d_years
        )
        
        failed_years = []
        for year in d_years:
            gdf = self.__attempt_tiger_fetch(path, year)
            if isinstance(gdf, gpd.GeoDataFrame):
                tbl_name = tbl_name_comp + f'_{year}'
                self.__append_shpfile_crs(gdf, tbl_name)
                CREATE_TABLE_SQL, INSERT_VALUES_SQL = self.__sql_statements(gdf, tbl_name)
                self._connection.execute(sqlalchemy.text(CREATE_TABLE_SQL))
                self._connection.commit()
                self._connection.execute(sqlalchemy.text(INSERT_VALUES_SQL))
                self._connection.commit()
                tiger_logger.info(
                    "Successfully queried and cached the shapefile for the %s calendar year", year
                )
            else:
                failed_years.append(year)
            del gdf

        msg = f'Failed attempts for the following years: {failed_years}' if len(failed_years) > 0 else ''

        tiger_logger.info(
            'Fulfilled attempts for querying TIGER shapefiles for the path: %s.%s',
            path, msg
        )


    def __crs_metadata_table(self) -> None:
        """
        Store the CRS/SRID info into the PostGIS database.

        Note that the table name is 'tiger_srid_info'.
        """
        tiger_logger.info("Caching SRID/CRS info...")
        crs_df = pd.DataFrame(self._crs_points)
        
        columns = ", ".join([f'"{i}"' for i in crs_df.columns])
        tuples  = map(str, crs_df.itertuples(index = False, name = None))
        values  = sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))
        
        create_tbl = pd.io.sql.get_schema(crs_df, 'tiger_srid_info')
        CREATE_TABLE_SQL = create_tbl.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS') + ';\n'

        insert_fmt_string = """
        INSERT INTO "{table}" ({columns})
        VALUES {values};
        """
        INSERT_VALUES_SQL = insert_fmt_string.format(
            table   = 'tiger_srid_info',
            columns = columns,
            values  = values
        )

        self._connection.execute(sqlalchemy.text(CREATE_TABLE_SQL))
        self._connection.commit()
        self._connection.execute(sqlalchemy.text(INSERT_VALUES_SQL))
        self._connection.commit()
        tiger_logger.info("Successfully cached SRID/CRS info: %s", 'tiger_srid_info')

        self._crs_points.clear()

    def __database_tables(self) -> t.List[str]:
        """
        Fetch the list of tables present in the database.
        """
        fetch = self._connection.execute(
            sqlalchemy.text(
                """
                SELECT table_name FROM information_schema.tables
                WHERE table_type='BASE TABLE' AND table_schema='public';
                """
            )
        )
        tables = [i[0] for i in fetch.fetchall()]
        return tables
    
    def __attempt_tiger_fetch(
        self, path: t.Dict[str, t.Any], year: int
    ) -> t.Optional[gpd.GeoDataFrame]:
        """
        Attempt to query the TIGER shapefile. Sometimes, this may not be successful
        for a host of reasons (cf. `acspsuedo.source.shpfile`) and, if so, raise a
        warning.
        """
        try:
            with warnings.catch_warnings():
                warnings.filterwarnings('ignore')
                gdf = shapefile_handler.fetch_tiger_shpfile(year, **path)
                if gdf is not None:
                    return gdf
                
                msg = f"The TIGER shapefile for the path {path} for the {year} calendar "
                "year could not be located. The Census Bureau may not maintain the "
                "relevant file for this year. See https://www2.census.gov/geo/tiger."
                warnings.warn(msg, TigerShapefileNotFoundWarning)
                tiger_logger.warning(msg)
                
                return None
        except Exception as e:
            err_msg = ''.join(traceback.format_exception(*sys.exc_info()))
            tiger_logger.exception(
                'TIGER shapefile fetch failed. Try later? Exception Type: %s. Traceback: %s',
                type(e), err_msg, exc_info = False
            )
            return None

    def __sql_statements(
        self, gdf: gpd.GeoDataFrame, tbl_name: str
    ) -> t.Tuple[str, str]:
        """
        Return CREATE TABLE and INSERT VALUES statements for the fetched TIGER
        shapefile.

        GeoPandas is built upon Pandas so any throughput issues w/r/t sanitizing
        in Pandas will likely be mirrored by that of GeoPandas. Thus, this step
        is taken to overcome that hassle.
        """
        gdf['geom'] = [str(i) for i in gdf['geometry']]
        gdf.drop(columns=['geometry'], inplace=True)

        columns = ", ".join([f'"{i}"' for i in gdf.columns])
        tuples = map(str, gdf.itertuples(index = False, name = None))
        values = sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))
        
        create_tbl = pd.io.sql.get_schema(gdf, tbl_name)
        CREATE_TABLE_SQL = create_tbl.replace('"geom" TEXT', '"geom" geometry') + ';\n'

        insert_fmt_string = """
        INSERT INTO "{table}" ({columns})
        VALUES {values};
        """
        INSERT_VALUES_SQL = insert_fmt_string.format(
            table   = tbl_name,
            columns = columns,
            values  = values
        )

        return CREATE_TABLE_SQL, INSERT_VALUES_SQL
    
    def __check_postgis_installation(self) -> None:
        """
        Check if the postgis extension is installed, otherwise create it.
        """
        result = self._connection.execute(
            sqlalchemy.text(
                "SELECT * FROM pg_extension WHERE extname = 'postgis';"
            )
        )
        if len(result.fetchall()) > 0:
            return None
        
        self._connection.execute(
            sqlalchemy.text(
                "CREATE EXTENSION postgis;"
            )
        )
        self._connection.commit()
    

    def __geographic_path_tbl_component(
        self, path: t.Dict[str, t.Any],
    ) -> str:
        """
        Formatting for the TIGER shapefile table name.
        """
        geo_spec= {k: 'ALL' if v == '*' else v for k, v in path.items()}
        gs_name = 'tiger_' + '_'.join([f'{k}{v}' for k, v in geo_spec.items()])
        return gs_name
    
    def __get_path_support_years(
        self, path: t.Dict[str, t.Any]
    ) -> t.Tuple[t.Dict[str, t.Any], t.List[int]]:
        """
        Return the list of supported calendar years and path itself.
        """
        config = _read_config(CONFIG_SETTINGS['CONFIGURATION_FOLDER'])
        metadata = _read_metadata(CONFIG_SETTINGS['CONFIGURATION_FOLDER'])

        # Only check in APIs for which the user has specified
        scopes = list(path)
        inner_scope = scopes[-1]
        apis = metadata['API_SEARCH'][inner_scope]

        config_tbls = config['TABLE_SUPPORT']

        support = [
            {"year": i["year"], "specifiers": {x: path.get(x) for x in j}}
            for i in config_tbls for j in i['compatible_scopes'] if
            ( set(scopes) == set(j) ) and ( i['dataset'] in apis )
        ]
        years = list(dict.fromkeys([i['year'] for i in support]))
        path  = support[0]['specifiers'] 

        return path, years

    def __append_shpfile_crs(
        self, gdf: gpd.GeoDataFrame, tbl_name: str
    ) -> None:
        """
        Store the CRS/SRID information for the fetched TIGER shapefile.

        This step is necessary as reading from the PostGIS database will cause
        the `geopandas.GeoDataFrame` to have a `None` value for the CRS.
        """
        self._crs_points.append({'TABLE': tbl_name, 'SRID': str(gdf.crs)})