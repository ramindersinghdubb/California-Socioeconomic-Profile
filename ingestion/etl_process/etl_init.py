"""
ETL interface.
"""
from __future__ import annotations
import asyncio
import sqlite3
import logging
import typing as t
from functools import reduce
from re import sub
from pathlib import Path

import aiohttp
import acspsuedo.query as apq
import pandas as pd
import sqlalchemy

import sys
sys.path.insert(0, str(Path.cwd()))
from ingestion.etl_process.exceptions import (
    UnsupportedPathException,
    MissingDataException
)
from ingestion.etl_process.metadata import (
    _metadata_config_init,
    _metadata_config_update,
    _read_metadata,
    _read_config,
    ConfigException
)
from ingestion.etl_process._tiger_init import _TigerHandlerInterface
from ingestion.config import CONFIG_SETTINGS

logging.basicConfig(
    filename = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'log.log',
    filemode = 'a',
    format   = "%(asctime)s - %(filename)s, Line %(lineno)s - %(levelname)s: %(message)s",
    datefmt  = "%m-%d-%Y, %I:%M:%S %p",
    level    = logging.INFO
)
etl_logger = logging.getLogger(__name__)



    
class EtlProcess():
    def __init__(
        self,
        connection: t.Union[sqlite3.Connection, sqlalchemy.Connection],
        table_dict: t.Optional[dict[str, t.Union[list[str], str]]] = None,
        selection_dict: t.Optional[dict[str, t.Union[list[str], str]]] = None,
        folder: t.Union[Path, str] = Path.cwd(),
        **yaml_kwargs
    ):
        """
        Initialization for the :py:class:`EtlProcess` interface.

        Parameters
        ----------
        connection
            A :py:class:`sqlite3.Connection` or `sqlalchemy.Connection`. Represents the
            SQL database for the ingested data.

        folder
            The folder location containing the YAML metadata and JSON configuration
            files. Defaults to the current working directory.

        table_dict
            A look-up table such that keys represent a user-defined topic/category and
            values represent those tables (provided by any number of the Census Bureau's
            American Community Survey dataset APIs).

        selection_dict
            A look-up table such that keys identify each inner-layer set of geometries
            against which data will be collected (cf. the `acspsuedo.query` interface)
            and values identify a subset of Census Bureau APIs to comb through. This is
            particularly advantageous if users know precisely which APIs contain their
            listed tables, and controls what happens if any two APIs share a common
            geometry space (e.g. ACS 1-Year Detailed Tables and ACS 5-Year Detailed
            Tables).
        
        yaml_kwargs
            Any customization when writing the YAML metadata file. Argument space
            is that of `yaml.dump()`.
        """
        self._connection = connection
        self._table_dict = table_dict
        self._selection_dict = selection_dict
        self._folder = folder
        self._yaml_kwargs = yaml_kwargs

        self._tiger_init = _TigerHandlerInterface(self._connection)


    def initialize_configuration(self) -> None:
        """
        Initialize the YAML metadata and JSON configuration files (both written to
        the same folder).

        This initialization process is crucial for configuring the ingestion process
        to concentrate on the argument space as stipulated here.

        **Note**: If any one of the initialization components are changed *after*
        these files are written, be sure to execute this method once more to track
        those updates.
        """
        apis = [v if isinstance(v, list) else [v] for v in self._selection_dict.values()]
        apis = list(dict.fromkeys(reduce(lambda x, y: x + y, apis)))
        _metadata_config_init(
            table_dict        = self._table_dict,
            cb_datasets       = apis,
            geographic_scopes = list(self._selection_dict),
            selection_dict    = self._selection_dict,
            folder            = self._folder,
            **self._yaml_kwargs
        )
        etl_logger.info("Initialized configuration files to '%s'", self._folder)

    def update_configuration(self) -> None:
        """
        Update the (initialized) YAML metadata file and JSON configuration files
        by tracking Census Bureau releases.

        **Note**: This update is **strictly** for tracking/checking any new API
        releases published by the Census Bureau. **If you are changing any one
        of the initialization components** (such as which APIs to comb through or
        the folder location for the configuration files), **be sure to use the**
        `initialize_configuration` **method**.
        """
        _metadata_config_update(self._folder)

    def ingest(
        self, *paths: t.Dict[str, t.Any]
    ) -> None:
        """
        Ingest data for the specified set of geographic pathways.

        Note: Be sure the necessary configuration files are initialized prior
        to running this. This is accomplished via the `initialize_configuration`
        method.

        Parameters
        ----------
        paths
            One, or multiple, fully-specified geographic paths. Each pathway should be
            *completely* specified, and passed as a dictionary (keys represent the
            geographic scope, values represent a specific identifier or a wildcard
            operator, `*`). See `acspsuedo.query.view_geographic_paths()`.

            Each one of these fully-specified geographic paths will be validated against
            the configuration settings and, upon sucession, will ingest data where
            available.
        """
        self._batch_extract_paths(paths)


    async def async_ingest(
        self, *paths: t.Dict[str, t.Any], batch_size: int = 5,
    ) -> None:
        """
        **EXPERIMENTAL**

        Ingest data for the specified set of geographic pathways.

        Note: Be sure the necessary configuration files are initialized prior
        to running this. This is accomplished via the `initialize_configuration`
        method.

        Parameters
        ----------
        paths
            One, or multiple, fully-specified geographic paths. Each pathway should be
            *completely* specified, and passed as a dictionary (keys represent the
            geographic scope, values represent a specific identifier or a wildcard
            operator, `*`). See `acspsuedo.query.view_geographic_paths()`.

            Each one of these fully-specified geographic paths will be validated against
            the configuration settings and, upon sucession, will ingest data where
            available.

        batch_size
            The number of concurrent requests to be made to the Census Bureau
            for data extraction. Default 5.

            Note that this number should be intentionally kept low (<10),
            especially for large data queries. Be polite, don't get blocked.
        """
        await self._async_batch_extract_paths(*paths, batch_size = batch_size)


    def get_topic_df(
        self, path: t.Dict[str, t.Any], topic: str, year: int
    ) -> pd.DataFrame:
        """
        Retrieve the `pandas.DataFrame` instance corresponding to the specified
        topic (as stipulated in the initialized configuration settings) for the
        calendar year of interest *and* the geographic path.

        Note: Be sure the data for the specified path is ingested prior to
        using this function.

        Parameters
        ----------
        path
            A fully-specified geographic path.

        topic
            One of the user-defined topics/categories used when initializing the
            configuration settings for this interface.

        year
            A supported calendar year for the topic.

        Returns
        -------
        A `pandas.DataFrame` object corresponding to the topic of interest for the
        (available) calendar year and the (previously ingested) geographic pathway.
        """
        return self.__create_topic_table(self._connection, path, topic, year)
    
    def get_topic_tables_support(
        self, path: t.Dict[str, t.Any]
    ) -> t.Dict[str, t.Dict[int, t.List[str]]]:
        """
        Get a nested dictionary such that

            User-defined topic -> {Year: Tables}

        In other words, given the configuration files, return a nested dictionary
        where the outer key specifies your defined topics, the inner key specifies
        the calendar year support for that topic, and the values specify the list of
        tables for a given calendar year.

        Parameters
        ----------
        path
            A fully-specified geographic path.

        Returns
        -------
        A nested dictionary such that

            User-defined topic -> {Year: Tables}
        """
        return self.__get_table_support(path)

    @property
    def connection(self):
        """
        A :py:class:`sqlite3.Connection` or `sqlalchemy.Connection`. Represents the
        SQL database for the ingested data.
        """
        return self._connection
    
    @connection.setter
    def connection(self, new_connection: t.Union[sqlite3.Connection, sqlalchemy.Connection]):
        self._folder = new_connection

    @connection.deleter
    def connection(self):
        raise AttributeError("Cannot have an uninitialized connection.")

    @property
    def folder(self):
        """
        The location of the YAML metadata and JSON configuration files.
        """
        return self._folder
    
    @folder.setter
    def folder(self, new_folder: t.Union[Path, str]):
        self._folder = new_folder

    @folder.deleter
    def folder(self):
        raise AttributeError("Cannot have an uninitialized folder.")
    
    @property
    def table_dict(self):
        """
        A look-up table such that keys represent a user-defined topic/category and
        values represent those tables (provided by any number of the Census Bureau's
        American Community Survey dataset APIs).
        """
        return self._table_dict
    
    @table_dict.setter
    def table_dict(self, new_table_dict: dict[str, t.Union[list[str], str]]) -> None:
        self._table_dict = new_table_dict

    @property
    def selection_dict(self):
        """
        A look-up table such that keys identify each inner-layer set of geometries
        against which data will be collected (cf. the `acspsuedo.query` interface)
        and values identify a subset of Census Bureau APIs to comb through. This is
        particularly advantageous if users know precisely which APIs contain their
        listed tables, and controls what happens if any two APIs share a common
        geometry space (e.g. ACS 1-Year Detailed Tables and ACS 5-Year Detailed
        Tables).
        """
        return self._selection_dict
    
    @selection_dict.setter
    def selection_dict(self, new_selection_dict: dict[str, t.Union[list[str], str]]) -> None:
        self._selection_dict = new_selection_dict

    @property
    def yaml_kwargs(self):
        """
        Any customization when writing the YAML metadata file. Argument space
        is that of `yaml.dump()`.
        """
        return self._selection_dict
    
    @yaml_kwargs.setter
    def yaml_kwargs(self, new_yaml_kwargs: dict[str, t.Any]) -> None:
        self._yaml_kwargs = new_yaml_kwargs


    def __create_topic_table(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], geog_scopes: t.Dict[str, t.Any], topic: str, year: int
    ) -> pd.DataFrame:
        dfs = self.__read_tables(conn, geog_scopes, topic, year)
        df = reduce(
            lambda left, right: pd.merge(left, right, how = "inner", on = 'GEO_ID'), dfs
        )
        return df


    def __read_tables(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], geog_scopes: t.Dict[str, t.Any], topic: str, year: int
    ) -> t.List[pd.DataFrame]:
        sql_tbls = self.__list_tables(geog_scopes, topic, year)
        dfs = []
        for sql_tbl in sql_tbls:
            read_tbl = 'SELECT * from "%s"' % sql_tbl
            try:
                if isinstance(conn, sqlite3.Connection):
                    dfs.append(pd.read_sql(read_tbl, conn))
                else:
                    dfs.append(pd.read_sql_table(sql_tbl, conn))
            except:
                raise MissingDataException(
                    f"Missing table: '{sql_tbl}'. Is the connection correct and/or "
                    f"have you ingested data for the path: {geog_scopes}?"
                ) from None
        return dfs


    def __list_tables(
        self, geog_scopes: t.Dict[str, t.Any], topic: str, year: int
    ) -> t.List[str]:
        """
        Return the list of SQL table names.
        """
        topics_dict = self.__get_table_support(geog_scopes)
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
        gs_name  = self.__geographic_path_tbl_component(geog_scopes)
        id_sql_tbl = f'{gs_name}_{year}'
        sql_tbls   = [f'{gs_name}_{tbl}_{year}' for tbl in tbls]
        return [id_sql_tbl, *sql_tbls]
    
    def __get_table_support(self, geog_scopes: t.Dict[str, t.Any]) -> t.Dict[int, t.Dict[str, t.List[str]]]:
        """
        Using the configuration files, return a dictionary such that:
            { topic: {year: tables} }
        """
        config  = _read_config(self._folder)
        metadata = _read_metadata(self._folder)
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

        topic_dict = self.__list_yaml_topics()
        
        topic_support_dict = {}
        for topic, tbls in topic_dict.items():
            dummy_dict = {}
            for year, tables in sorted(year_tbl_dict.items()):
                if len(support:=[i for i in tables if i in tbls]) > 0:
                    dummy_dict[year] = support
            topic_support_dict[topic] = dummy_dict
        
        
        return topic_support_dict

    def __list_yaml_topics(self) -> t.Dict[str, t.List[str]]:
        metadata = _read_metadata(self._folder)
        return metadata['CENSUS_BUREAU_TABLES_BY_TOPIC']



    def _batch_extract_paths(
        self, *paths: t.Dict[str, t.Any]
    ) -> None:
        for path in paths:
            self._batch_extract(self._connection, path)
        etl_logger.info('Data ingestion complete.')
    
    async def _async_batch_extract_paths(
        self, *paths: t.Dict[str, t.Any], batch_size: int = 5
    ) -> None:
        for path in paths:
            await self._batch_async_extract(self._connection, path, batch_size)
        etl_logger.info('Data ingestion complete.')

    
    def _batch_extract(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], path: t.Dict[str, t.Any],
    ) -> None:
        geog_scopes, tasks_dict = self.__ingestion_init(conn, path)
        if len(tasks) == 0:
            etl_logger.info("No updates to be made for the path: %s. Skipping...", path)
            return
        
        for year, tasks in tasks_dict.items():
            for task in tasks:
                self._extract(task, geog_scopes)
            self.__segmentation_by_table_and_year(conn, tasks, year, geog_scopes)
            del tasks
        etl_logger.info("Successfully ingested data for the path: %s", geog_scopes)
    
    async def _batch_async_extract(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], path: t.Dict[str, t.Any], batch_size: int
    ) -> None:
        geog_scopes, tasks_dict = self.__ingestion_init(conn, path)
        if len(tasks_dict) == 0:
            etl_logger.info("No updates to be made for the path: %s. Skipping...", path)
            return
        
        for year, tasks in tasks_dict.items():
            for idx in range(0, len(tasks), batch_size):
                await asyncio.gather(
                    *[self._async_extract(task, geog_scopes) for task in tasks[idx:idx+batch_size]]
                )
            await asyncio.sleep(0)
            self.__segmentation_by_table_and_year(conn, tasks, year, geog_scopes)
            del tasks
        etl_logger.info("Successfully ingested data for the path: %s", geog_scopes)

    
    def __ingestion_init(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], path: t.Dict[str, t.Any],
    ) -> t.Tuple[t.Dict[str, t.Any], t.Dict[int, t.List[t.Dict[str, t.Any]]]]:
        geog_scopes, tasks = self.__specs(path)
        etl_logger.info("Beginning data ingestion for the path: %s", geog_scopes)
        tasks = self.__must_download_tasks(conn, tasks, geog_scopes)
        return geog_scopes, tasks
    
    def __segmentation_by_table_and_year(
        self, conn: t.Union[sqlite3.Connection, sqlalchemy.Connection], tasks: t.List[t.Dict[str, t.Any]], year: int, geog_scopes: t.Dict[str, t.Any]
    ) -> None:
        """
        Once all 'download tasks' are fulfilled, we segment by year and table.
        We also provide star tables for each year, where these tables contain
        geographic identifying information. Each segmented table, thus, has a
        primary key column ('GEO_ID') shared by this auxiliary identifier table.
        """
        etl_logger.info("Beginning segmentation for the %s calendar year...", year)
        gs_name = self.__geographic_path_tbl_component(geog_scopes)

        dfs      = [i['content'] for i in tasks]
        id_cols  = tasks[0]['id_cols']
        tbl_dict = {k: v for i in tasks for k,v in i['tbl_dict'].items()}
        
        if len(dfs) > 1 and all(isinstance(x, pd.DataFrame) for x in dfs):
            df = reduce(lambda left, right: pd.merge(left, right, on = id_cols), dfs)
        else:
            df = dfs[0]
        
        if 'GEO_ID' not in id_cols:
            df['GEO_ID'] = pd.Series(list(range(0, df.shape[1])), dtype=object)
            id_cols.append('GEO_ID')

        cols = apq.GEO_SPEC_METADATA[list(geog_scopes)[-1]][1]

        for col in [*cols, 'NAME']:
            if col in df.columns and col != 'YEAR':
                df[col] = [str(i).replace("'", '').replace('"', '') for i in df[col]]
        
        STAR_COL = ['GEO_ID']
        TBL_TUPLES = [
            (f'{gs_name}_{tbl}_{year}', df[STAR_COL + tbl_cols].copy())
            for tbl, tbl_cols in tbl_dict.items()
        ] + [(f'{gs_name}_{year}', df[id_cols].copy())]
        
        if isinstance(conn, sqlalchemy.Connection):
            self.__sql_insert_sqlalchemy(conn, TBL_TUPLES)
        else:
            self.__sql_insert_sqlite(conn, TBL_TUPLES)
            
        etl_logger.info("Successfully segmented and cached data for the %s calendar year.", year)

    def __sql_insert_sqlite(
        self, conn: sqlite3.Connection, TBL_TUPLES: t.List[t.Tuple[str, pd.DataFrame]]
    ) -> None:
        for (tbl_name, tbl_df) in TBL_TUPLES:
            tbl_df.to_sql(tbl_name, conn, index=False)

    def __sql_insert_sqlalchemy(
        self, conn: sqlalchemy.Connection, TBL_TUPLES: t.List[t.Tuple[str, pd.DataFrame]]
    ) -> None:
        statements = [self.__sql_tbl_statements(tbl_df, tbl_name) for tbl_name, tbl_df in TBL_TUPLES]
        CREATE, INSERT = map(list, zip(*statements))
    
        for idx in range(0, len(statements), 5):
            conn.execute(sqlalchemy.text('\n'.join(CREATE[idx:idx+5])))
            conn.commit()
            conn.execute(sqlalchemy.text('\n'.join(INSERT[idx:idx+5])))
            conn.commit()


    def __sql_tbl_statements(self, df: pd.DataFrame, tbl_name: str) -> t.Tuple[str, str]:
        """
        Return SQL formatted statements for DROP TABLE, CREATE TABLE, and INSERT VALUES
        statements.

        For shared core CloudSQL services, GCP takes an unusually long time (perhaps some
        throughput issues with `pandas.DataFrame.to_sql()`?) and thus it is much more
        preferential to use the DataFrame contents in order to format SQL statements.

        Many thanks to StackOverflow user absoup for this!
        https://stackoverflow.com/a/70585493
        """
        columns = ", ".join([f'"{i}"' for i in df.columns])
        tuples = map(str, df.itertuples(index = False, name = None))
        values = sub(r"(?<=\W)(nan|None)(?=\W)", "NULL", (",\n" + " " * 7).join(tuples))

        create_tbl = pd.io.sql.get_schema(df, tbl_name)
        CREATE_TABLE_SQL = create_tbl.replace('CREATE TABLE', 'CREATE TABLE IF NOT EXISTS') + ';\n'
        insert_fmt_string = 'INSERT INTO "{table}" ({columns})\nVALUES {values};'
        INSERT_VALUES_SQL = insert_fmt_string.format(
            table   = tbl_name,
            columns = columns,
            values  = values
        )
        
        return CREATE_TABLE_SQL, INSERT_VALUES_SQL

        
        

    async def _async_extract(
        self, task: t.Dict[str, t.Any], geog_scopes: t.Dict[str, t.Any]
    ) -> None:
        args, dataset, year, _ = self.__get_task_meta(task)

        etl_logger.info("Beginning query for the '%s' API, calendar year %s...", dataset, year)
        async with aiohttp.ClientSession(trust_env=True) as session:
            await asyncio.sleep(0)
            df = await apq.async_download(session, **args, **geog_scopes)
        etl_logger.info("Completed query for the '%s' API, calendar year %s.", dataset, year)
        self.__meta_organize(task, df, geog_scopes)

    def _extract(
        self, task: t.Dict[str, t.Any], geog_scopes: t.Dict[str, t.Any]
    ) -> None:
        args, dataset, year, _ = self.__get_task_meta(task)

        etl_logger.info("Beginning query for the '%s' API, calendar year %s...", dataset, year)
        df = apq.download(**args, **geog_scopes)
        etl_logger.info("Completed query for the '%s' API, calendar year %s.", dataset, year)
        self.__meta_organize(task, df, geog_scopes)

    
    def __meta_organize(
        self, task: t.Dict[str, t.Any], df: pd.DataFrame, geog_scopes: t.Dict[str, t.Any],
    ) -> pd.DataFrame:
        """
        Organize the database by each of the user-specified tables.
        """
        geo_col_labs = apq.GeoSpecFmtter.get_geo_cols(**geog_scopes)
        id_cols = [col for col in ['NAME', 'GEO_ID', 'UCGID', *geo_col_labs, 'YEAR']
                   if col in list(df.columns)]
        data_cols = sorted([col for col in list(df.columns) if col not in id_cols])

        df.reset_index(drop = True, inplace = True)
        task['content'] = df
        task['id_cols'] = id_cols
        tbls = task['arg']['tables']
        var_df = apq.variable_cache.var_metadata_df(task['arg']['dataset'], task['arg']['year'])
        
        task['tbl_dict'] = {
            tbl: [i for i in data_cols if i in var_df['VARIABLE'][var_df['TABLE'] == tbl].to_list()]
            for tbl in tbls
        }
        task.pop('arg')


    def __must_download_tasks(
        self, conn, tasks: t.List[t.Dict[str, t.Any]], geog_scopes: t.Dict[str, t.Any]
    ) -> t.Dict[int, t.List[t.Dict[str, t.Any]]]:
        """
        This step is initiated prior to running data queries. This helps isolate
        tasks for which we must download data from the Bureau from those that have
        have been previously downloaded.
        """
        years = list(sorted(set([i['year'] for i in tasks])))
        task_by_yr_dict = {yr: [i for i in tasks if i['year'] == yr] for yr in years}
        gs_name = self.__geographic_path_tbl_component(geog_scopes)
        
        not_cached_tasks = {}
        for year, yr_tasks in task_by_yr_dict.items():
            id_tbl_name = f'{gs_name}_{year}'
            if not self.__cache_check(conn, id_tbl_name):
                not_cached_tasks[year] = (yr_tasks)
        
        return not_cached_tasks
    
    def __cache_check(self, conn, tbl_name: str):
        if isinstance(conn, sqlite3.Connection):
            return self.__cache_check_sqlite(conn, tbl_name)
        else:
            return self.__cache_check_postgres(conn, tbl_name)

    def __cache_check_postgres(
        self, conn: sqlalchemy.Connection, tbl_name: str
    ) -> bool:
        cond = sqlalchemy.inspect(conn).has_table(tbl_name)
        return cond

    def __cache_check_sqlite(
        self, conn: sqlite3.Connection, tbl_name: str
    ) -> bool:
        cursor = conn.cursor()
        check_tbl = "PRAGMA table_info(%s)" % tbl_name
        cursor.execute(check_tbl)
        check = cursor.fetchall()
        cursor.close()

        if len(check) > 0:
            return True
        
        return False


    def __get_task_meta(
        self, task: t.Dict[str, t.Any]
    ) -> t.Tuple[dict, str, int, str]:
        """
        Extract metadata and generate the standardized SQL table name.
        """
        args    = task['arg']
        dataset = args['dataset']
        year    = args['year']

        gs_name = self.__geographic_path_tbl_component(task['geographic_scopes'])
        
        tbl_name = f'{gs_name}_{year}'
        
        return args, dataset, year, tbl_name
    
    def __geographic_path_tbl_component(
        self, path: t.Dict[str, t.Any],
    ) -> str:
        geo_spec= {k: 'ALL' if v == '*' else v for k, v in path.items()}
        gs_name = '_'.join([f'{k}{v}' for k, v in geo_spec.items()])
        return gs_name

    def __specs(
        self, path: t.Dict[str, t.Any]
    ) -> tuple[t.Dict[str, t.Any], t.List[t.Dict[str, t.Any]]]:
        """
        Given a path, return a neatly formatted array of look-up tables to use
        in the ingestion process. Raises an `UnsupportedPathException` for empty
        arrays, or a `ConfigException` for missing search specifications.
        """
        metadata = _read_metadata(self._folder)
        search   = metadata['API_SEARCH']

        config        = _read_config(self._folder)
        config_tables = config['TABLE_SUPPORT']

        geo_specs = list(path)
        support = [
            {
                "dataset": i["dataset"],
                "year": i["year"],
                "tables": i["tables"],
                "specifiers": {x: path.get(x) for x in j}
            } for i in config_tables for j in i['compatible_scopes'] if set(geo_specs) == set(j)
        ]

        if len(support) > 1:
            inner = list(fmtted_path:=support[0]['specifiers'])[-1]
            apis  = [i for i in search.get(inner)]
            if len(apis) == 0:
                msg = f"Missing a search specification for the '{inner}' scope for the path {path}."
                etl_logger.warning(msg)
                raise ConfigException(msg)
            
            search_support = [
                {k:v for k,v in i.items() if k!='specifiers'}
                for i in support if any(i['dataset'] == j for j in apis)
            ]
            
            if len(search_support) > 1:
                tasks = [
                    {
                        'geographic_scopes': fmtted_path,
                        'arg': arg,
                        'year': arg['year'],
                        'content': None,
                        'id_cols': None,
                        'tbl_dict': None,
                    }
                    for arg in search_support if len(arg["tables"]) > 0
                ]
                return fmtted_path, tasks
            else:
                f_api = list(dict.fromkeys(i['dataset'] for i in support))
                msg = f"Missing relevant search specifications for '{inner}' for the " \
                    f"path: {path}. Listed support for this path include: {f_api}."
                etl_logger.warning(msg)
                raise ConfigException(
                    f"Missing relevant search specifications for '{inner}' for the "
                    f"path: {path}. Listed support for this path include: {f_api}."
                )
        
        msg = f"{geo_specs} is not supported in any Census Bureau dataset of interest." \
        " Consider dropping?"
        etl_logger.warning(msg)
        raise UnsupportedPathException(msg)