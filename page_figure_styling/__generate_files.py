"""
Script for initializing tooltip files.
"""
from pathlib import Path
import json

import sys
sys.path.insert(0, str(Path.cwd()))

from page_components._submeasures_options import SubmeasureInterface


def generate_files():
    config_folder = Path.cwd() / 'config'
    config_file = config_folder / 'dropdown_config.json'
    with open(config_file, 'r') as file:
        content = json.load(file)
    tables = list(content.keys())

    folder = Path.cwd() / 'page_figure_styling'

    for table in tables:
        module = '_tool_' + table.replace(' ', '') + '.py'
        file = folder / module
        
        options = SubmeasureInterface.get_submeasure_options(table)
        submeasures = [i['value'] for i in options]

        fx_strings = ''
        dict_string = f'lambda_dict = {{\n'
        for sbm in submeasures:
            cleaned_sbm = sbm.replace(' ', '').replace('(', '').replace(')', '').replace('.', '').replace('-', '').replace(',', '').replace('/', '')
            fx_strings += "    @classmethod\n"
            fx_strings += f"    def {cleaned_sbm}(\n"
            fx_strings += "        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame\n"
            fx_strings += "    ):\n"
            fx_strings += "        ...\n"
            fx_strings += "\n\n\n"

            dict_string += f"            '{sbm}': cls.{cleaned_sbm},\n"
        dict_string += f'        }}'




        with open(file, 'w') as file:
            content = f'''"""
    Tooltip metadata interface for the '{table}' category.
    """

    import typing as t

    import pandas as pd

    import sys
    from pathlib import Path
    sys.path.insert(0, str(Path.cwd()))
    from page_figure_styling._abc import TooltipFigureMetaABC



    class {table.replace(' ', '')}Tooltip(TooltipFigureMetaABC, measure = '{table}'):
        """
        Tooltip metadata interface for the '{table}' category.
        """

        @classmethod
        def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
            {dict_string}
            return lambda_dict

            
        
    {fx_strings}
    '''
            file.write(content)


def main(reset_files: bool = False):
    if reset_files:
        generate_files()


if __name__ == '__main__':
    main()