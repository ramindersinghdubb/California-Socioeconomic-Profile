"""
Metadata interfaces for priming the Census Bureau data
extraction pipeline.
"""
from __future__ import annotations

import logging
import warnings
import json
import typing as t
from itertools import chain
from collections import OrderedDict
from pathlib import Path

import yaml
import pandas as pd
import acspsuedo.query as apq

import sys
sys.path.insert(0, str(Path.cwd()))
from ingestion.etl_process.protocols import fetch_content
from ingestion.etl_process.exceptions import ConfigException
from ingestion.config import CONFIG_SETTINGS


logging.basicConfig(
    filename = Path(CONFIG_SETTINGS['CONFIGURATION_FOLDER']) / 'log.log',
    filemode = 'w',
    format   = "%(asctime)s - %(filename)s, Line %(lineno)s - %(levelname)s: %(message)s",
    datefmt  = "%m-%d-%Y, %I:%M:%S %p",
    level    = logging.INFO
)
metadata_logger = logging.getLogger(__name__)



def _metadata_config_init(
    table_dict: dict[str, t.Union[list[str], str]],
    cb_datasets: t.Union[list[str], str],
    geographic_scopes: t.Union[list[str], str],
    selection_dict: dict[str, t.Union[list[str], str]],
    folder: t.Union[Path, str] = Path.cwd(),
    **yaml_kwargs
):
    """
    Initialize the YAML metadata file and JSON configuration file (both written in
    the same folder).

    This initialization process is crucial for configuring the ingestion process
    to concentrate on the argument space as stipulated here.

    Parameters
    ----------
    table_dict
        A look-up table such that keys represent a user-defined topic/category and
        values represent those tables (provided by any number of the Census Bureau's
        American Community Survey dataset APIs).
    
    cb_datasets
        The collection of dataset APIs from which tables will be extracted.

    geographic_scopes
        The set of inner-layer geometries against which data will be collected (cf.
        the `acspsuedo.query` interface).

    selection_dict
        A look-up table such that keys identify one (or all) of the listed
        `geographic_scopes` and values identify a subset of `cb_dataset` APIs to comb
        through. This is particularly advantageous if users know precisely which APIs
        contain their listed tables, and controls what happens if any two APIs share
        a common variable space (e.g. ACS 1-Year Detailed Tables and ACS 5-Year
        Detailed Tables).

    folder
        The folder that will contain the YAML metadata file and JSON config file.
    
    yaml_kwargs
        Any customization when writing the metadata YAML file. Argument space
        is that of `yaml.dump()`.
    """
    feeder = MetadataYamlParser(file = Path(folder) / 'metadata.yaml', **yaml_kwargs)
    feeder.write_file(
        table_dict  = table_dict,
        api         = cb_datasets,
        geog_scopes = geographic_scopes,
        search_dict = selection_dict
    )

    tmc = TableMetadataConfigParser(file = Path(folder) / 'config.json', indent = 2)
    tmc.write_file(metadata_file = feeder.file)

def _metadata_config_update(
    folder: t.Union[Path, str] = Path.cwd(),
):
    """
    Update the JSON configuration file. **Only works after the YAML metadata file has
    been written.**

    This update process is useful for tracking new Census Bureau API releases, and
    implicitly configures the ingestion pipeline to only download these new releases
    (as opposed to, presumably, previously downloaded data in conjunction with these
    new releases).

    Parameters
    ----------
    folder
        The folder that contains the YAML metadata and JSON config files.
    """
    tmc = TableMetadataConfigParser(file = Path(folder) / 'config.json', indent = 2)
    tmc.update_file(Path(folder) / 'metadata.yaml')

def _read_metadata(
    folder: t.Union[Path, str] = Path.cwd(),
) -> t.Dict[str, t.Union[t.Dict[str, t.List[str]], t.List[str]]]:
    """
    Read the YAML metadata file.

    Parameters
    ----------
    folder
        The folder that contains the YAML metadata and JSON config files.
    """
    with open(Path(folder) / 'metadata.yaml', 'r', encoding='utf-8') as f:
        content = yaml.safe_load(f)
    return content

def _read_config(
    folder: t.Union[Path, str] = Path.cwd(),
) -> t.Dict[str, t.Union[t.Union[t.List[int], t.Dict[str, t.List[str]]], bool]]:
    """
    Read the JSON config file.

    Parameters
    ----------
    folder
        The folder that contains the YAML metadata and JSON config files.
    """
    with open(Path(folder) / 'config.json', 'r', encoding='utf-8') as f:
        content = json.load(f)
    return content


class MetadataYamlParser:
    """
    YAML configuration parser for writing/reading the metadata file.
    """

    def __init__(
        self,
        file: t.Union[str, Path] = Path.cwd() / 'metadata.yaml',
        **kwargs: t.Any
    ):
        """
        Parameters
        ----------
        file
            The location of the yaml file for the metadata .yaml file
            file. This will be used for writing to, and reading from.
        
        kwargs
            Any customization when writing to the metadata .yaml file.
            Argument space is that of `yaml.dump()`.
        """
        self._file = file
        self._kwargs = kwargs

        self._parser = Parser(Parser._init_obj)

    def __repr__(self):
        return 'MetadataYamlParser(file={})'.format(self._file)

    @property
    def file(self):
        """The location of the metadata .yaml file path."""
        return self._file
    
    @file.setter
    def file(self, new_file: t.Union[str, Path]):
        self._file = new_file

    @file.deleter
    def file(self):
        raise AttributeError("Cannot have a non-existent file location.")
    
    def read_file(self):
        """
        Read the YAML metadata file.

        See the `file` property attribute.
        """
        if Path(self._file).exists():
            with open(self._file, mode = 'r', encoding = 'utf-8') as file:
                file_content = yaml.safe_load(file)
            return file_content
        
        raise AttributeError(
            "Metadata file has not been written yet. Please initialize "
            "the file object with the `_metadata_config_init` function."
        )
    
    def write_file(
        self,
        table_dict: dict[str, t.Union[list[str], str]],
        api: t.Union[list[str], str],
        geog_scopes: t.Union[list[str], str],
        search_dict: t.Optional[dict[str, t.Union[list[str], str]]] = None
    ) -> None:
        """
        Write the .yaml file containing metadata and look-up tables
        containing:
            - Census Bureau tables of interest (organized by topic),
            - Census Bureau APIs to reference,
            - Geographic scopes of interest 

        Parameters
        ----------
        table_dict
            A lookup table/dictionary whose format is such that the keys
            represent the topics of interest, while the values provie the
            table(s) organized under each topic, e.g.

            {'Rents': ['B25056', 'B25057', 'B25058'], 'Marital Status': 'S1201'}

        api
            The Census Bureau dataset API(s) to be fed into the parser.

            The API(s) must contain those tables which are specified for
            extraction.

        geog_scopes
            The reference(s) to the inner-layer set of geographic components to be
            fed into the parser.

            Note that these must made available in at least one of the specified
            Census Bureau dataset APIs.

        search_dict
            A search-based selection for narrowing API searches on specified
            geographic scopes in order to prioritize quicker metadata searches.
            
            Accepts a lookup-table/dictionary whose keys represent the scope (must
            be listed in `geog_scopes`) and whose values represent the selection
            of APIs (must be a strict subset of those listed in `api`).

            This is particularly advantageous if users know which Census Bureau
            APIs contain the tables of interest and/or if common tables are
            found for multiple Census Bureau APIs (e.g. the ACS 1-Year and ACS
            5-Year APIs share table metadata, but differ in which and how many
            scopes they respectively support).
        """
        self._parser.reset_feed()
        self._set_file_content(table_dict, api, geog_scopes, search_dict)
        with open(self._file, 'wt', encoding = 'utf-8') as file:
            file.write(self._parser.yaml_str)
        metadata_logger.info("Successfully written metadata YAML file: %s", self._file)

    def list_topics(self) -> list[str]:
        """
        Retrieve the list of user-specified topics from the
        (written) YAML metadata file.
        """
        file = self.read_file()
        return list(file['CENSUS_BUREAU_TABLES_BY_TOPIC'].keys())
    
    def list_tables(self) -> list[str]:
        """
        Retrieve the list of user-specified Census Bureau tables
        from the (written) YAML metadata file.
        """
        file = self.read_file()
        return list(OrderedDict.fromkeys(chain.from_iterable(file['CENSUS_BUREAU_TABLES_BY_TOPIC'].values())))
    
    def list_dataset_api(self) -> list[str]:
        """
        Retrieve the list of user-specified Census Bureau APIs
        from the (written) YAML metadata file.
        """
        file = self.read_file()
        return file['CENSUS_BUREAU_DATASET_APIs']
    
    def list_geog_scopes(self) -> list[str]:
        """
        Retrieve the list of user-specified geographic scopes
        from the (written) YAML metadata file.
        """
        file = self.read_file()
        return file['GEOGRAPHIC_SCOPES']
    
    def list_dataset_api_by_scope(self, scope: str) -> t.Optional[list[str]]:
        """
        If the optional user-specified API selection search is
        provided, retrieve the API selection indicating which
        APIs to comb through for the specified geographic scope.
        """
        file = self.read_file()
        if (api_search := file['API_SEARCH']) is None:
            warnings.warn("No selection search option was provided.", UserWarning)
            return None
        
        if (api := api_search.get(scope)) is None:
            msg = "No such scope '{}' was found.".format(scope)
            warnings.warn(msg, UserWarning)
            return
        
        return api
    
    def _set_file_content(
        self,
        table_dict: dict[str, t.Union[list[str], str]],
        api: t.Union[list[str], str],
        geog_scopes: t.Union[list[str], str],
        search_dict: t.Optional[dict[str, t.Union[list[str], str]]] = None
    ) -> None:
        """
        Set the text into the parser.
        """
        self._parser_set_leading_message()
        self._parser_set_cb_tables_by_topic(table_dict)
        self._parser_set_cb_dataset_api(api)
        self._parser_set_cb_geog_scopes(geog_scopes)
        self._parser_set_search_specs_message()
        self._parser_set_cb_api_search(api, geog_scopes, search_dict)
        
    
    def _parser_set_leading_message(self) -> None:
        """The leading (commented) message in the metadata file."""
        text = """# ─────────────────────────────────────────────────────────── #
#                 METADATA CONFIGURATION FILE                 #
# Use this yaml file to set up any metadata and look-up       #
# tables for:                                                 #
#   - Census Bureau tables of interest (organized by topic),  #
#   - Census Bureau APIs to reference,                        #
#   - Geographic scopes of interest                           #
# ─────────────────────────────────────────────────────────── #\n
"""
        self._parser.feed(text)

    def _parser_set_search_specs_message(self) -> None:
        """
        Search specifications.
        
        Here, these are indicated with a gesture towards priming the
        pipeline to search through a selection of the overall set of
        specified APIs. In doing so, we hasten our search process
        (when looking for tables in each API)
        """
        text = """\n\n\n# ─────────────────────────────────────────────────────────── #
#                  API SEARCH SPECIFICATIONS                  #
# Here, these are indicated with a gesture towards priming    #
# the pipeline to search through a selection of the overall   #
# set of specified APIs. In doing so, we narrow our search    #
# process (when looking for tables in each API) and           #
# prioritize select APIs when tables are found in multiple    #
# APIs (i.e. in the case of ACS 1-Year vs. ACS 5-Year data,   #
# given their proximate overlap in table metadata).           #
#                                                             #
# The format is API_SEARCH, followed by one of the listed     #
# geographic scopes and the accompanying APIs to prioritize   #
# in the search.                                              #
# ─────────────────────────────────────────────────────────── #\n
"""
        self._parser.feed(text)
    
    def _parser_set_cb_tables_by_topic(
        self,
        table_dict: dict[str, t.Union[list[str], str]]
    ) -> None:
        """
        The Census Bureau tables, segmented by user-specific topic, to
        be fed into the parser.

        Parameters
        ----------
         table_dict
            A lookup table/dictionary whose format is such that the keys
            represent the topics of interest, while the values provie the
            table(s) organized under each topic, e.g.

            {'Rents': ['B25056', 'B25057', 'B25058'], 'Marital Status': 'S1201'}
        """
        table_dict = {
            'CENSUS_BUREAU_TABLES_BY_TOPIC': self._set_cb_tables_by_topic(table_dict)
        }

        self._parser.feed_yaml(table_dict, **self._kwargs)

    def _parser_set_cb_dataset_api(
        self,
        api: t.Union[list[str], str]
    ) -> None:
        """
        The Census Bureau dataset API(s) to be fed into the parser.

        The API(s) must contain those tables which are specified for
        extraction.

        Parameters
        ----------
        api
            The Census Bureau dataset API(s).
        """
        self._parser.feed('\n\n')
        api_dict = {'CENSUS_BUREAU_DATASET_APIs': self._set_cb_dataset_api(api)}
        self._parser.feed_yaml(api_dict, **self._kwargs)

    def _parser_set_cb_geog_scopes(
        self,
        geog_scopes: t.Union[list[str], str]
    ) -> None:
        """
        The reference(s) to the inner-layer set of geographic components to be
        fed into the parser.

        Note that these must made available in at least one of the specified
        Census Bureau dataset APIs.

        Parameters
        ----------
        geog_scopes
            The reference(s) to the inner-layer set of geographic components.
        """
        self._parser.feed('\n\n')
        gs_dict = {'GEOGRAPHIC_SCOPES': self._set_cb_geog_scopes(geog_scopes)}
        self._parser.feed_yaml(gs_dict, **self._kwargs)

    def _parser_set_cb_api_search(
        self,
        api: t.Union[list[str], str],
        geog_scopes: t.Union[list[str], str],
        search_dict: t.Optional[dict[str, t.Union[list[str], str]]] = None
    ) -> None:
        """
        A search-based selection for narrowing API searches on specified
        geographic scopes in order to prioritize quicker metadata searches.
        This is particularly advantageous if users know which Census Bureau
        APIs contain the tables of interest and/or if common tables are
        found for multiple Census Bureau APIs (e.g. the ACS 1-Year and ACS
        5-Year APIs share table metadata, but differ in which and how many
        scopes they respectively support).

        Parameters
        ----------
        api
            The Census Bureau dataset API(s).

        geog_scopes
            The reference(s) to the inner-layer set of geographic components.

        search_dict
            A lookup-table whose keys represent the scope (must be listed
            in `geog_scopes`) and whose values represent the selection of
            APIs (must be a strict subset of those listed in `api`).
        """
        
        if search_dict is not None:
            search_dict = {'API_SEARCH': self._set_cb_api_search(api, geog_scopes, search_dict)}
            self._parser.feed_yaml(search_dict, **self._kwargs)
        

    def _set_cb_tables_by_topic(
        self,
        table_dict: dict[str, t.Union[list[str], str]]
    ) -> dict[str, list[str]]:
        """
        Set the Census Bureau tables of interest, which are organized by topic.

        Note that the keys represent the topics of interest, while the values
        provide the table(s) organized under each topic, e.g.

        {'Rents': ['B25056', 'B25057', 'B25058'], 'Marital Status': 'S1201'}

        Parameters
        ----------
        table_dict
            A lookup table/dictionary whose format is as described earlier.
        """
        return {k: v if isinstance(v, list) else [v] for k, v in table_dict.items()}
    
    def _set_cb_dataset_api(self, api: t.Union[list[str], str]) -> list[str]:
        """
        Set the Census Bureau dataset API(s).

        The API(s) must contain those tables which are specified
        for extraction.
        """
        return api if isinstance(api, list) else [api]
    
    def _set_cb_geog_scopes(self, geog_scopes: t.Union[list[str], str]) -> list[str]:
        """
        Set the reference(s) to the inner-layer of geographic components.
        Note that these must made available in at least one of the specified
        Census Bureau dataset APIs.
        """
        return geog_scopes if isinstance(geog_scopes, list) else [geog_scopes]
    
    def _set_cb_api_search(
        self,
        api: t.Union[list[str], str],
        geog_scopes: t.Union[list[str], str],
        search_dict: dict[str, t.Union[list[str], str]]
    ) -> dict[str, list[str]]:
        geog_scopes = self._set_cb_geog_scopes(geog_scopes)
        api = self._set_cb_dataset_api(api)

        for scope, dataset in search_dict.items():
            if scope in geog_scopes:
                dataset = dataset if isinstance(dataset, list) else [dataset]
                if all(d in api for d in dataset):
                    continue
                raise ValueError(
                    f"Encountered non-specified APIs: {[d for d in dataset if d not in api]}. "
                    "Search criteria is incompatible with a non-disjoint set."
                )
            else:
                raise ValueError(
                    f"Encountered unrecognizable geographic scope: '{scope}'."
                )
            
        return {k: v if isinstance(v, list) else [v] for k,v in search_dict.items()}
    

class TableMetadataConfigParser:
    """
    JSON configuration parser for writing/reading the configuration file.
    This will contain the year support for each specified table in the
    metadata file.

    The generated JSON file contains four items.

    - 'CENSUS_BUREAU_DATASET_API_SUPPORT'
    A record such that each key is a dataset API, accompanied by a value
    that is an array indicating available years (henceforth support) for
    that dataset API.

    - 'TABLE_SUPPORT'
    Similar to the format above, except the record now indicates tables,
    their respective support, and the list of compatible geographic scopes.
    """
    
    def __init__(
        self,
        file: t.Union[str, Path] = Path.cwd() / 'config.json',
        **kwargs: t.Any
    ):
        """
        Parameters
        ----------
        file
            The location of the JSON file for the metadata .json file
            file. This will be used for writing to, and reading from.
        
        kwargs
            Any customization when writing to the config .json file.
            Argument space is that of `json.dump()`.
        """
        self._file = file
        self.kwargs = kwargs

        self._API_DF = self._create_acs_api_dataset()

    def __repr__(self):
        return 'TableMetadataConfigParser(file={})'.format(self._file)

    @property
    def file(self):
        """The location of the config .json file path."""
        return self._file
    
    @file.setter
    def file(self, new_file: t.Union[str, Path]):
        self._file = new_file

    @file.deleter
    def file(self):
        raise AttributeError("Cannot have a non-existent file location.")
    
    def update_file(
        self,
        metadata_file: t.Union[Path, str] = Path.cwd() / 'metadata.yaml'
    ):
        """
        Update the config JSON file.

        This allows for updating by comparing the remote (the server) to the
        local (in-file). If updates are warranted, this will read the new API
        releases and update each table's support accordingly.

        Parameters
        ----------
        metadata_file
            The metadata YAML file.
        """
        metadata_logger.info("Updating config file...")
        content = self.read_file()
        infile_support = content.get('CENSUS_BUREAU_DATASET_API_SUPPORT', None)
        cb_support = self._config_set_cb_dataset_api_support(metadata_file)
        
        if infile_support == cb_support:
            metadata_logger.info("No new Census Bureau API releases. Skipping config file update.")
            return None
        
        metadata_logger.info("Found new Census Bureau API releases. Updating...")
        self._update_file(infile_support, cb_support, metadata_file)
        metadata_logger.info("Successfully updated config file.")
        

    def _update_file(
        self,
        infile_support: dict,
        cb_support: dict,
        metadata_file: t.Union[Path, str]
    ):
        """
        Internal for if/when updates need to be made.
        """
        new_support = {api: [yr for yr in yrs if yr not in infile_support[api]] for api, yrs in cb_support.items()}
        new_support = {k:v for k,v in new_support.items() if len(v) > 0}

        content = self.read_file()

        infile_tbl_support = content.get('TABLE_SUPPORT')

        new_tbl_support = self._config_set_cb_table_support(metadata_file, new_support)

        def update_support(updated_support: list[dict], infile_support: list[dict]):
            updated_support = [i for i in updated_support if i not in infile_support]
            infile_support.extend(updated_support)
            infile_support.sort(key=lambda d: (d['dataset'], d['year']))

            return infile_support

        infile_tbl_support = update_support(new_tbl_support, infile_tbl_support)
        
        updated_content = {
            'CENSUS_BUREAU_DATASET_API_SUPPORT': cb_support,
            'TABLE_SUPPORT': infile_tbl_support,
        }
        with open(self._file, 'w', encoding = 'utf-8') as file:
            json.dump(updated_content, file, **self.kwargs)

    
    def read_file(self):
        """
        Read the config file.

        See the `file` property attribute.
        """
        if Path(self._file).exists():
            with open(self._file, mode = 'r', encoding = 'utf-8') as file:
                file_content = json.load(file)
            return file_content
        
        raise AttributeError(
            "Metadata file has not been written yet. Please initialize "
            "the file object with the `_metadata_config_init` function."
        )
    
    def write_file(
        self,
        metadata_file: t.Union[Path, str]
    ) -> None:
        """
        Write the JSON configuration file containing the support
        for the user-specified Census Bureau APIs and tables, as
        provided in the `metadata_file`.

        Parameters
        ----------
        metadata_file
            The metadata YAML file location.
        """
        content = self._set_file_content(metadata_file)
        with open(self._file, 'w', encoding = 'utf-8') as file:
            json.dump(content, file, **self.kwargs)
        metadata_logger.info("Successfully written config JSON file: %s", self._file)

    def _set_file_content(
        self,
        metadata_file: t.Union[Path, str]
    ) -> dict[str, dict]:
        """
        Set the contents of the JSON configuration file.
        """
        api_support = self._config_set_cb_dataset_api_support(metadata_file)
        tbl_support = self._config_set_cb_table_support(metadata_file, api_support)

        return {
            'CENSUS_BUREAU_DATASET_API_SUPPORT': api_support,
            'TABLE_SUPPORT': tbl_support,
        }
    
    def _config_set_cb_table_support(
        self,
        metadata_file: t.Union[Path, str],
        support_dict: dict[str, list[str]]
    ) -> list[dict[str, t.Union[str, t.Union[int, list[str]]]]]:
        """
        Parameters
        ----------
        metadata_file
            The location of the metadata file.

        support_dict
            The lookup-table/dictionary such that keys represent the
            dataset APIs and the values represent the support (an
            array/list of years).

        Returns
        -------
        An array of lookup-tables/dictionaries whose format is a subset of
        the parameter space in the `acspsuedo.query` download interface.
        """
        content = self.__read_metadata_file(metadata_file)
        tbls = list(OrderedDict.fromkeys(chain.from_iterable(content['CENSUS_BUREAU_TABLES_BY_TOPIC'].values())))
        scopes = content['GEOGRAPHIC_SCOPES']
        
        cb_table_support = []
        for api, years in support_dict.items():
            for year in years:
                api_df   = apq.variable_cache.var_metadata_df(api, int(year))
                api_tbls = list(sorted([tbl for tbl in tbls if tbl in api_df['TABLE'].unique().tolist()]))

                tmp_scopes = apq.view_geographic_paths(api, int(year))
                tgt_scopes = [i for i in tmp_scopes if i[-1] in scopes]
                cb_table_support.append({'dataset': api, 'year': year, 'tables': api_tbls, 'compatible_scopes': tgt_scopes})
                if len(api_tbls) > 0:
                    metadata_logger.info("Extracted metadata for the '%s' API during calendar year %s", api, year)
                else:
                    metadata_logger.warning(
                        "Found no tables of interest for the '%s' API during %s. Consider dropping the API for this year?",
                        api, year
                    )
            metadata_logger.info("Set table and geographic support given by the '%s' API. Continuing...", api)
        cb_table_support.sort(key=lambda d: (d['dataset'], d['year']))
        metadata_logger.info("Successfully set support for all specified tables!")
        
        return cb_table_support
    
    def _config_set_cb_dataset_api_support(self, metadata_file: t.Union[Path, str]) -> dict[str, list[str]]:
        """
        Read the dataset support as given by the Census Bureau server.
        """
        content = self.__read_metadata_file(metadata_file)
        if (apis := content.get('CENSUS_BUREAU_DATASET_APIs')) is None:
            raise ConfigException("File has no known Census Bureau APIs to reference (`CENSUS_BUREAU_DATASET_APIs`).")
        return self._supported_dataset_api_years(apis)


    def _supported_dataset_api_years(
        self,
        datasets: t.Union[str, list[str]]
    ) -> dict[str, list[str]]:
        """
        Generate the support (available years) for the specified
        dataset API(s).
        """
        datasets = datasets if isinstance(datasets, list) else [datasets]
        api_df = self._API_DF.copy()
        return {dataset: list(api_df[api_df['BASE'] == dataset]['YEAR']) for dataset in datasets}

    def _create_acs_api_dataset(self) -> pd.DataFrame:
        """
        Download the Census Bureau's American Community Survey APIs into
        a formatted dataset.
        """
        URL = f'https://api.census.gov/data/?{apq.api_key_config._get_api_key()}'
        metadata_logger.info("Running request to available Census Bureau APIs...")
        CENSUS_DATA_DICT = fetch_content(URL)
        metadata_logger.info("Success! Cleaning API information...")

        LIST_ACS_API = [i for i in CENSUS_DATA_DICT['dataset'] if
                        '/'.join(i.get('c_dataset')).startswith(('acs/acs'))]

        DF = self._api_df_fmt(LIST_ACS_API)

        metadata_logger.info("Successfully formatted API metadata reference dataframe.")
        
        return DF

    def _api_df_fmt(self, list_api: list[dict]) -> pd.DataFrame:
        ACS_API_df = pd.DataFrame(
            [{'YEAR': ACS_API.get('c_vintage'),
            'BASE': '/'.join( [i for i in ACS_API.get('c_dataset', '')] ),
            'BASE_URL': ACS_API.get('distribution', '')[0].get('accessURL'),
            'GEOGRAPHIES_URL': ACS_API.get('c_geographyLink'),
            'GROUPS_URL': ACS_API.get('c_groupsLink'),
            'VARIABLES_URL': ACS_API.get('c_variablesLink'),
            } for ACS_API in list_api ])

        ACS_API_df['REF'] = [BASE.upper().replace('/', '_').replace('ACS_', '') for BASE
                             in ACS_API_df['BASE']]

        DF = ACS_API_df.sort_values(by = ['YEAR', 'BASE'], ignore_index = True)

        return DF
    
    def __read_metadata_file(self, metadata_file: t.Union[Path, str]) -> t.Any:
        with open(metadata_file, mode='r', encoding='utf-8') as f:
            data = yaml.safe_load(f)
        return data



class Parser:
    """
    The internal feeder, used by the :py:class:`MetadataYamlParser`
    class.
    """

    _init_obj = object()

    def __init__(self, init_obj):
        if init_obj != Parser._init_obj:
            raise ValueError("Cannot initialize a `Parser` object.")
        
        # Underlying, to exploit string joining
        self.yaml_str = ''

    def feed(self, text: str) -> None:
        """
        Feed a normal string to the internal parser.

        Parameters
        ----------
        text
            A string to be fed into the internal parser.
        """
        self.yaml_str += text
        
    def feed_yaml(self, text: t.Any, **kwargs: t.Any) -> None:
        """
        Feed a YAML string/object to the internal parser.

        Parameters
        ----------
        text
            An object to be fed into the internal parser.
            This may be a string, or a dictionary, or a list.

        **kwargs
            Any keyword arguments passed to `yaml.dump`.
        """
        self.yaml_str += yaml.dump(data = text, **kwargs)

    def reset_feed(self) -> None:
        """
        Reset the internal parser.
        """
        self.yaml_str = ''