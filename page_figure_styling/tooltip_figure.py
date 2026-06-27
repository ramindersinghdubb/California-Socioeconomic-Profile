"""
Interface for creating the tooltip figure (enabled when a submeasure
is selected).
"""

import typing as t

import pandas as pd
import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_figure_styling._abc import retrieve_measure_tooltip_interface





class TooltipFigureInterface:
    """
    Interface for generating the `plotly.graph_object.Figure` instance
    displayed in the `dcc.Tooltip` component.
    """

    @classmethod
    def get_figure(cls, rowData, tract, place, year, measure, submeasure):
        """
        Generate the tooltip figure from the supplied dropdown selection
        values, and the hover data (accessed via `tract`).
        """
        df = cls.__get_tract_df(rowData, tract)

        interface = retrieve_measure_tooltip_interface(measure)
        metadata  = interface.get_metadata(
            place      = place,
            tract      = tract,
            year       = year,
            measure    = measure,
            submeasure = submeasure,
            df = df
        )

        fig = cls.__generate_bar_trace(metadata, place, tract, year)
        
        return fig
    

    
    @classmethod
    def __generate_bar_trace(cls, metadata, place, tract, year):
        """
        Generate a :py:class:`plotly.graph_objects.Figure` with a bar trace.
        """
        fig = px.bar(
            data_frame  = metadata['dataframe'],
            x           = metadata['x'],
            y           = metadata['y'],
            custom_data = metadata.get('custom_data', None),
        )

        fig = fig.update_traces(
            marker        = {**metadata.get('marker', {})},
            hovertemplate = metadata.get('hovertemplate', ''),
            hoverlabel    = {
                'bgcolor': '#FAFAFA',
                'bordercolor': '#111810',
                'font': {
                    'color': '#020403'
                }
            },
        )

        yaxis = metadata.get('yaxis', {})
        yaxis['title'] = {**yaxis.get('title', {}), 'font': {'family': 'Trebuchet MS'}}
        xaxis = metadata.get('xaxis', {})
        xaxis['title'] = {**xaxis.get('title', {}), 'font': {'family': 'Trebuchet MS'}}
        
        fig = fig.update_layout(
            margin        = {'b': 100, 't': 100, 'r': 100},
            paper_bgcolor = '#FEF9F3',
            plot_bgcolor  = '#FEF9F3',
            showlegend    = metadata.get('showlegend', False),
            xaxis = {
                **xaxis,
                'linecolor': '#000000',
            },
            yaxis = {
                **yaxis,
                'gridcolor': '#C0C0C0',
            },
            title = {
                **metadata.get('title', {}),
                'font': {
                    'family': "Trebuchet MS",
                },
                'subtitle': {
                    'text': f'{tract}, {place} ({year})'
                }
            },
        )

        return fig
    
    @classmethod
    def __get_tract_df(cls, rowData: t.List[t.Dict[str, t.Any]], tract: str) -> pd.DataFrame:
        """
        Get the `pandas.DataFrame` object for the specified census tract.
        """
        data = [next((i for i in rowData if i.get('NAME', '') == tract))]
        df   = pd.DataFrame(data)
        return df