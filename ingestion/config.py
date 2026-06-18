"""
Configuration settings for the ingestion process.
"""
import sys
from pathlib import Path

from acspsuedo.datasets import ACS5, ACS5_PROFILE, ACS5_SUBJECT
from acspsuedo.fips.states import CALIFORNIA

sys.path.insert(0, str(Path.cwd()))
from ingestion.utils import lettered_table



API_LIST = [ACS5, ACS5_PROFILE, ACS5_SUBJECT]


CONFIG_SETTINGS = {
    # ───── ───── ───── ───── ───── ───── ─────
    # Census Bureau tables specified by your
    # defined topics.
    # ───── ───── ───── ───── ───── ───── ─────
    'CENSUS_TABLES_BY_TOPIC': {
        'Contract Rent': ['B25056', 'B25057', 'B25058', 'B25059'],
        'Rent Burden': ['B25070', 'B25072', 'B25074'],
        'Employment Statistics': ['S2301'],
        'Food Stamps': lettered_table('B22005') + ['S2201'],
        'Health Insurance Coverage': ['S2701'],
        'Household Income': ['S1901'],
        'Housing Units and Occupancy': ['B25002', 'B25016', 'B25053', 'DP04', 'S2502'],
        'Poverty': ['S1701'],
        'Transportation Methods to Work': ['S0801'],
        'Work Hours': ['S2303'],
        'Economic Measures': ['DP03', 'S2403', 'S2413', 'S2404', 'S2414'],
        'Population': ['S0101', 'DP05'],
        'Education': ['B06009', 'B15001'] + lettered_table('C15002'),
    },
    
    # ───── ───── ───── ───── ───── ───── ─────
    # Paths for which the tables specified
    # above should be downloaded for
    # ───── ───── ───── ───── ───── ───── ─────
    'PATHS': [
        {'state': CALIFORNIA, inner: '*'} for inner in ['place', 'tract']
    ],

    # ───── ───── ───── ───── ───── ───── ─────
    # Search specifications for the previosly
    # listed Census Bureau tables.
    # ───── ───── ───── ───── ───── ───── ─────
    'API_SEARCH_DICT': {
        'place': API_LIST,
        'tract': API_LIST.copy()
    },

    # ───── ───── ───── ───── ───── ───── ─────
    # The folder location that will contain the
    # configuration files for the ingestion.
    # ───── ───── ───── ───── ───── ───── ─────
    'CONFIGURATION_FOLDER': Path.cwd() / 'config',

    # ───── ───── ───── ───── ───── ───── ─────
    # Boolean indicating whether or not to
    # ingest TIGER shapefile data.
    # ───── ───── ───── ───── ───── ───── ─────
    'INCLUDE_TIGER_SHAPEFILES': True,

    # ───── ───── ───── ───── ───── ───── ─────
    # Boolean indicating whether or not to
    # include inflation adjustment file.
    # ───── ───── ───── ───── ───── ───── ─────
    'NEED_INFLATION_SERIES': True,
}


# ───── ───── ───── ───── ───── ───── ───── ───── ───── ───── #
# NOTE
# CloudSQL's Python connector interface is used to connect to
# the SQL database (PostgreSQL driver). Credentials should be
# stored in the OS environment and not hard-coded into any
# script.
#
# LOCATIONS:
#  - INSTANCE_CONNECTION_STRING (instance connection string)
#  - DB_USER (database username)
#  - DB_PASSWORD (database password)
#  - DB_NAME (database name)
# ───── ───── ───── ───── ───── ───── ───── ───── ───── ───── #