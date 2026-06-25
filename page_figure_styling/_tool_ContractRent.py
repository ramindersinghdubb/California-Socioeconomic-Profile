"""
Tooltip metadata interface for the 'Contract Rent' category.
"""

import typing as t

import pandas as pd

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import TooltipFigureMetaABC



class ContractRentTooltip(TooltipFigureMetaABC, measure = 'Contract Rent'):
    """
    Tooltip metadata interface for the 'Contract Rent' category.
    """

    @classmethod
    def _dict_lambda(cls) -> t.Dict[str, t.Callable[[], t.Dict[str, t.Any]]]:
        lambda_dict = {
            'Distribution of Contract Rents': cls.DistributionofContractRents,
        }
        return lambda_dict

        
    
    @classmethod
    def DistributionofContractRents(
        cls, place: str, tract: str, year: int, measure: str, df: pd.DataFrame
    ):
        new_cols = {
            '$0 to 249': ['B25056_003E', 'B25056_004E', 'B25056_005E', 'B25056_006E'],
            '$250 to 499': ['B25056_007E', 'B25056_008E', 'B25056_009E', 'B25056_010E', 'B25056_011E'],
            '$500 to 750': ['B25056_012E', 'B25056_013E', 'B25056_014E', 'B25056_015E', 'B25056_016E'],
            '$750 to 999': ['B25056_017E', 'B25056_018E', 'B25056_019E'],
            '$1.0k to 1.25k': ['B25056_020E'],
            '$1.25k to 1.5k': ['B25056_021E'],
            '$1.5k to 2.0k': ['B25056_022E']
        }
        if year < 2015:
            new_cols.update({"$2.0k or more": ["B25056_023E"]})
            color_array = [
                "#FFD400", "#FFC300", "#FFB200",
                "#FF9F00", "#FF8C00", "#FF7300",
                "#FF4D00", "#FF0000"
            ]
        if year >= 2015:
            new_cols.update({
                "$2.0k to 2.5k": ["B25056_023E"],
                "$2.5k to 3.0k": ["B25056_024E"],
                "$3.0k to $3.5k": ["B25056_025E"],
                "$3.5k or more": ["B25056_026E"]
            })
            color_array = [
                "#FFFF00", "#FFEB00", "#FFE100",
                "#FFD700", "#FFCC00", "#FFBF00",
                "#FFB300", "#FF9900", "#FF7A00",
                "#FF4D00", "#FF0000"
            ]

        for col_name, cols in new_cols.items():
            df[col_name] = df[cols].sum(axis = 1)
        
        df = df.melt(
            id_vars    = ['NAME'],
            value_vars = list(new_cols),
            var_name   = 'VARIABLE',
            value_name = 'VALUE'
        )

        metadata = {
            'dataframe': df,
            'x': 'VARIABLE',
            'y': 'VALUE',
            'title': {
                'text': "<b style='font-size:20px;'>Distribution of Contract Rents</b>",
                'x': 0.05
            },
            'xaxis': {
                'title': {
                    'text': '<b>Contract Rent (USD)</b>',
                    'standoff': 15
                },
                'tickfont': {
                    'size': 10
                },
                
            },
            'yaxis': {
                'title': {
                    'text': '<b>Number of Units</b>',
                    'standoff': 15
                },
                'ticklabelstandoff': 5,
            },
            'marker': {
                'color': color_array,
                'line': {
                    'color': '#111111', 'width': 1.5
                }
            }
        }

        return metadata





# Distribution of Contract Rents
# column_dict = {
#     "B25056_003E": "Less than $100",
#     "B25056_004E": "$100 to $149",
#     "B25056_005E": "$150 to $199",
#     "B25056_006E": "$200 to $249",
#     "B25056_007E": "$250 to $299",
#     "B25056_008E": "$300 to $349",
#     "B25056_009E": "$350 to $399",
#     "B25056_010E": "$400 to $449",
#     "B25056_011E": "$450 to $499",
#     "B25056_012E": "$500 to $549",
#     "B25056_013E": "$550 to $599",
#     "B25056_014E": "$600 to $649",
#     "B25056_015E": "$650 to $699",
#     "B25056_016E": "$700 to $749",
#     "B25056_017E": "$750 to $799",
#     "B25056_018E": "$800 to $899",
#     "B25056_019E": "$900 to $999",
#     "B25056_020E": "$1.0k to 1.25k",
#     "B25056_021E": "$1.25k to 1.5k",
#     "B25056_022E": "$1.5k to 2.0k"
# }