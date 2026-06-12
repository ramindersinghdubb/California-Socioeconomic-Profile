"""
Supporting data ingestion processes.

**Purposes**:
    - Fetch data from the United States Census Bureau's American
    Community Survey

    - Curate a lookup table summarizing potential variable label
    changes for a given dataset across many years

    - Curate a lookup table summarizing years of when a dataset
    is available, alongside the range of years for which a given
    region is able to provide data

**Modules**:

    - `etl_process.etl_init`
    Main data ingestion pipeline, accessed via the `EtlProcess`
    interface

    - `etl_process._tiger_init`
    Interface for handling TIGER shapefiles, accessed via the
    `_TigerHandlerInterface` interface
"""

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))

from ingestion.etl_process.etl_init import EtlProcess, etl_logger
from ingestion.etl_process._tiger_init import _TigerHandlerInterface, tiger_logger
from ingestion.etl_process.metadata import metadata_logger


__all__ = [
    'EtlProcess',
    '_TigerHandlerInterface',
    'etl_logger',
    'tiger_logger',
    'metadata_logger'
]