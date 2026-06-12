"""
Callables for invoking database connections.

At present, the GCP SQL Connector is employed (as Cloud Run
is where the service is currently hosted).
"""
import os
import sqlite3
from pathlib import Path

import sqlalchemy
from google.cloud.sql.connector import Connector, IPTypes

import sys
sys.path.insert(0, str(Path.cwd()))
from ingestion.config import CONFIG_SETTINGS



def get_gcp_engine() -> tuple[sqlalchemy.Engine, Connector]:
    """
    Retrieve the `sqlalchemy.Engine` instance for the given GCP credentials,
    as well as the `google.cloud.sql.connector.Connector` instance used in
    the connection.
    
    Note that these credentials should be stored in the OS environment.

    Returns
    -------
    A `sqlalchemy.Engine` instance, and the `google.cloud.sql.connector.Connector`
    instance.
    """
    INSTANCE_CONNECTION_STRING = os.environ['INSTANCE_CONNECTION_STRING']
    DB_USER = os.environ['DB_USER']
    DB_PASS = os.environ['DB_PASSWORD']
    DB_NAME = os.environ['DB_NAME']

    IP_TYPE = IPTypes.PRIVATE if os.environ.get("PRIVATE_IP") else IPTypes.PUBLIC

    connector = Connector()

    def getconn():
        conn = connector.connect(
            INSTANCE_CONNECTION_STRING,
            "pg8000",
            user     = DB_USER,
            password = DB_PASS,
            db       = DB_NAME,
            ip_type  = IP_TYPE,
        )
        return conn

    pool = sqlalchemy.create_engine("postgresql+pg8000://", creator = getconn)

    return pool, connector



def get_sqlite_connection() -> sqlite3.Connection:
    """
    Retrieve the `sqlite3.Connection` instance.

    Note that the instance will point to a database location under the name
    'cb_data.db' in the configuration folder.

    Returns
    -------
    A `sqlite3.Connection` instance.
    """
    conn = sqlite3.connect(str(CONFIG_SETTINGS['CONFIGURATION_FOLDER'] / 'cb_data.db'))
    return conn