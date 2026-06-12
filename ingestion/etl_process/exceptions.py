"""
General exceptions pertaining to ingestion and metadata issues.
"""


class ConfigException(Exception):
    """General exception class for any configuration-related issues."""
    pass

class UnsupportedPathException(Exception):
    """General exception class for any unsupported path."""
    pass


class MissingDataException(Exception):
    """General exception class for any missing data, usually from lack of ingestion."""
    pass