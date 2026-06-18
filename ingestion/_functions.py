"""
Functions for the data ingestion process for CI/CD.

Triggered by GitHub Actions.
"""
import os
import sys
import traceback
import asyncio
import json
from pathlib import Path

import sqlalchemy
import pandas as pd
import requests as req

sys.path.insert(0, str(Path.cwd()))
from ingestion.etl_process import EtlProcess, _TigerHandlerInterface, etl_logger
from ingestion.config import CONFIG_SETTINGS
from db_retrieval import get_gcp_engine
from ingestion._tiger_confine import _write_tract_metadata


def _make_config_folder() -> None:
    """
    Make the folder holding the configuration files, if it
    doesn't already exist.
    """
    folder = CONFIG_SETTINGS['CONFIGURATION_FOLDER']
    if not Path(folder).exists():
        Path(folder).mkdir(parents = True, exist_ok = True)


def _init_ingestion_interface(connection: sqlalchemy.Connection) -> EtlProcess:
    """
    Initialize the ingestion interface instance.
    """
    etl_interface = EtlProcess(
        connection     = connection,
        table_dict     = CONFIG_SETTINGS['CENSUS_TABLES_BY_TOPIC'],
        selection_dict = CONFIG_SETTINGS['API_SEARCH_DICT'],
        folder         = CONFIG_SETTINGS['CONFIGURATION_FOLDER'],
        # Miscellaneous keyword arguments
        indent = 2
    )
    return etl_interface


def _init_configuration_files(etl_interface: EtlProcess) -> None:
    """
    Write/Update the configuration files.
    """
    metadata_file = Path(etl_interface.folder) / 'metadata.yaml'
    config_file   = Path(etl_interface.folder) / 'config.json'
    if not (metadata_file.exists() and config_file.exists()):
        etl_interface.initialize_configuration()
    else:
        etl_interface.update_configuration()

def _data_ingest(etl_interface: EtlProcess) -> None:
    """Data ingestion."""
    try:
        asyncio.run(etl_interface.async_ingest(*CONFIG_SETTINGS['PATHS'], batch_size = 3))
    except Exception as e:
        err_msg = ''.join(traceback.format_exception(*sys.exc_info()))
        etl_logger.exception(
            'Concurrent ingestion failed. Try later? Exception Type: %s. Traceback: %s',
            type(e), err_msg, exc_info = False
        )

def _tiger_ingest(connection: sqlalchemy.Connection) -> None:
    """TIGER shapefile ingestion."""
    if CONFIG_SETTINGS['INCLUDE_TIGER_SHAPEFILES']:
        tiger_interface = _TigerHandlerInterface(connection)
        tiger_interface._tiger_query(*CONFIG_SETTINGS['PATHS'])


def _get_topic_dict(etl_interface: EtlProcess) -> dict[str, list[int]]:
    """
    Get the look-up table/dictionary such that keys represent the
    user-defined topics/categories, and the values represent a list
    of calendar years over which each topic/category is supported.
    """
    CA_tracts = CONFIG_SETTINGS.get('PATHS')[-1]
    TOPIC_DICT = etl_interface.get_topic_tables_support(CA_tracts)
    TOPIC_DICT = {k: list(v) for k, v in TOPIC_DICT.items()}

    return TOPIC_DICT

def _write_place_df(etl_interface) -> None:
    """
    Write the CSV file containing holistic information on each Cali city/place.
    """
    tract_file = Path(etl_interface.folder) / 'tract_metadata.csv'
    tract_df = pd.read_csv(tract_file, dtype={'PLACE_FIPS': object})
    tract_df.drop(columns=['GEO_ID'], inplace=True)

    place_df = tract_df.drop_duplicates().copy()
    place_df.sort_values(by=['YEAR', 'PLACE_FIPS'], inplace=True)
    place_file = Path(etl_interface.folder) / 'place_metadata.csv'
    place_df.to_csv(place_file, index=False)


def _write_dashboard_config(etl_interface: EtlProcess) -> None:
    """
    Write a JSON file in the specified configuration settings folder
    containing the configurations for the Dash app dropdowns.
    """
    tpc_support = _get_topic_dict(etl_interface)
    tpc_file = Path(etl_interface.folder) / 'dropdown_config.json'
    with open(tpc_file, 'w') as file:
        json.dump(tpc_support, file, indent = 2)
    etl_logger.info("Successfully wrote the topic dropdown configuration settings: %s", str(tpc_file))

    tract_file = Path(etl_interface.folder) / 'tract_metadata.csv'
    _write_tract_metadata(etl_interface.connection)
    etl_logger.info("Successfully wrote tract metadata: %s", str(tract_file))

    place_file = Path(etl_interface.folder) / 'place_metadata.csv'
    _write_place_df(etl_interface)
    etl_logger.info("Successfully wrote the place metadata: %s", str(place_file))

def _write_retroactive_cpi_series():
    """
    Write the Bureau of Labor Statistics' Retroactive CPI for all Urban Customers (R-CPI-U-RS)
    series into a CSV file.

    This will be used to adjust income/earnings estimates for cross-year comparisons in constant
    dollars.

    See 
    https://www.census.gov/topics/income-poverty/income/guidance/current-vs-constant-dollars.html
    """
    etl_logger.info('Making request attempt to the Bureau of Labor Statistics...')
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Accept-Encoding': 'gzip, deflate',
        'Connection': 'keep-alive',
    }
    
    try:
        r = req.get("https://www.bls.gov/cpi/research-series/r-cpi-u-rs-allitems.xlsx",
                    headers = headers)
        etl_logger.info('Request attempt success.')
    except Exception as e:
        err_msg = ''.join(traceback.format_exception(*sys.exc_info()))
        etl_logger.exception(
            'Request attempt failed. Exception Type: %s. Traceback: %s',
            type(e), err_msg, exc_info = False
        )
        return 
    
    folder = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER'])
    
    EXCEL_file = folder / 'r-cpi-u-rs.xlsx'
    CSV_file = folder / 'r-cpi-u-rs.csv'
    
    with open(EXCEL_file, 'wb') as file:
        file.write(r.content)
    
    df = pd.read_excel(EXCEL_file, header = 5, engine = 'openpyxl')
    df = df[['YEAR', 'AVG']].dropna()

    for YEAR in df['YEAR']:
        ind_val = df.loc[df['YEAR'] == YEAR, 'AVG'].iat[0]
        df[f'{YEAR}_ADJ_FACTOR'] = round(ind_val / df['AVG'], 5)
    
    df.to_csv(CSV_file, index = False)
    etl_logger.info(
        'Created CSV file for the Bureau of Labor Statistics Retroactive CPI Series: %s',
        str(CSV_file)
    )

    os.remove(EXCEL_file)


def _log_cleaner() -> None:
    """Just to be cautious."""
    import os

    log_file = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'log.log'
    with open(log_file, 'r') as file:
        content = ''.join(file.readlines())
    
    rewritten_content = content.replace(
        os.environ['INSTANCE_CONNECTION_STRING'], '*****'
    ).replace(
        os.environ['DB_USER'], '*****'
    ).replace(
        os.environ['DB_PASSWORD'], '*****'
    ).replace(
        os.environ['DB_NAME'], '*****'
    ).replace(
        os.environ['CENSUS_BUREAU_API_KEY'], '*****'
    )

    with open(log_file, 'w') as file:
        file.writelines(rewritten_content.splitlines(keepends=True))



def ingestion() -> None:
    """
    Ingestion process.
     
    This process makes use of the specifications listed under `ingestion.config.CONFIG_SETTINGS`
    to accomplish six tasks.

    - Initialize the ETL interface,
    - Write/update the configuration files for the listed specifications,
    - Ingest data into the GCP database,
    - (Optional) Ingest TIGER shapefile data into the GCP database,
    - Write the configuration settings for the Dash app dropdowns,
    - Write a log file (for debugging purposes)

    CloudSQL's Python connector interface is used to connect to the SQL database (PostgreSQL driver).
    Credentials should be stored in the OS environment and not hard-coded into any script.

    OS environment locations:
        - `INSTANCE_CONNECTION_STRING` (instance connection string)
        - `DB_USER` (database username)
        - `DB_PASSWORD` (database password)
        - `DB_NAME` (database name)
        - `CENSUS_BUREAU_API_KEY` (API key for quering Census Bureau data)
    """
    engine, connector = get_gcp_engine()
    conn = engine.connect()
    
    # For the ingestion (backend)
    _make_config_folder()
    etl_interface = _init_ingestion_interface(conn)
    _init_configuration_files(etl_interface)
    _data_ingest(etl_interface)
    _tiger_ingest(conn)

    # For the Dash app (frontend)
    _write_dashboard_config(etl_interface)

    conn.close()
    connector.close()

    # Optional inflation series
    if CONFIG_SETTINGS['NEED_INFLATION_SERIES']:
        _write_retroactive_cpi_series()

    _log_cleaner()