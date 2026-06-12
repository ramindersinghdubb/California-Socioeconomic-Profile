"""
Functions for the data ingestion process for CI/CD.

Triggered by GitHub Actions.
"""
import sys
import traceback
import asyncio
import json
from pathlib import Path

import sqlalchemy
import pandas as pd

sys.path.insert(0, str(Path.cwd()))
from ingestion.etl_process import EtlProcess, _TigerHandlerInterface, etl_logger
from ingestion.config import CONFIG_SETTINGS
from db_retrieval.db_connection import get_gcp_engine
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

    _log_cleaner()