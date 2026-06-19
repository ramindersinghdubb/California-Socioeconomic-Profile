"""
Layout for the Dash app.
"""
import typing as t

import dash_bootstrap_components as dbc
from dash import dcc, html

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._modal import get_modal
from page_components._off_canvas import OffCanvasText
from page_components.config import CONFIG_SETTINGS as APP_CONFIG_SETTINGS
from page_components._dropdowns import DropdownInterface
# from page_components._submeasures_options import submeasures_dict



class DashLayout:
    """
    Interface for formatting the Dash app layout.
    """

    @classmethod
    def serve_layout(cls) -> html.Div:
        """
        The Dash app layout.
        """
        layout = html.Div(
            children = [
                cls.app_display(),
                *cls.data_components()
            ]
        )
        return layout

    @classmethod
    def app_display(cls) -> html.Div:
        """
        Retrieve the py:class:`dash.html.Div` component for the
        app component
        """
        app_div = html.Div(
            className="row",
            children = [
                cls.left_column(),
                cls.right_column()
            ]
        )

        return app_div


    @classmethod
    def left_column(cls) -> html.Div:
        """
        Retrieve the py:class:`dash.html.Div` component corresponding
        to the left column of the Dash app.

        This column contains the title text, the dropdowns, and the
        off-canvas component.
        """
        left_col = html.Div(
            className = "four columns",
            children  = [
                *cls._header(),
                *cls._dropdowns(),
                get_modal(),
                *cls._offcanvas()
            ]
        )
        
        return left_col
    
    @classmethod
    def right_column(cls) -> dcc.Loading:
        """
        Retrieve the py:class:`dash.dcc.Loading` component corresponding
        to the right column of the Dash app.

        This column contains the choropleth map and the tooltip (active
        when a sub-measure is selected).
        """

        right_col = dcc.Loading(
            parent_className = "eight columns chart-layout",
            id        = 'loading-sign',
            className = 'loading',
            color     = '#F8F8FF',
            children  = [
                cls._choropleth_map(),
                cls._choropleth_map_tooltip()
            ]
        )
        
        return right_col
    
    @classmethod
    def data_components(cls) -> t.List[dcc.Store]:
        """
        Retrieve the list of py:class:`dash.dcc.Store` components.

        These components are used for locally caching data on the
        client-side.
        """
        data_components = [
            dcc.Store(id = "masterfile"),
            dcc.Store(id = "tooltip_file"),
            dcc.Store(id = "mapfile")
        ]

        return data_components
    
    @classmethod
    def _header(cls) -> t.List[t.Union[html.H3, html.P]]:
        """
        Retrieve the set of :py:class:`dash.html` components used in
        the Dash app.
        """
        header = [
            html.H3(
                "California Socioeconomic Profile"
            ),
            html.P(
                className = 'text-p',
                children  = """
                This website allows you to visualize various socioeconomic measures 
                for cities in California.
                """
            ),
            html.P(
                className = 'text-p',
                children  = 'Use the dropdowns to navigate your selection process.'
            )
        ]
        return header
    
    @classmethod
    def _dropdowns(cls) -> t.List[dcc.Dropdown]:
        """
        Retrieve the set of :py:class:`dash.dcc.Dropdown` components
        used in the Dash app.
        """

        dropdowns = [
            dcc.Dropdown(
                id          = 'place-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a place',
                options     = DropdownInterface.get_place_options(max(APP_CONFIG_SETTINGS['YEARS'])),
                value       = 'Los Angeles',
                clearable   = False,
                searchable  = True,
            ),
            dcc.Dropdown(
                id          = 'year-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a year',
                options     = DropdownInterface.get_year_options(place='Los Angeles'),
                value       = max(APP_CONFIG_SETTINGS['YEARS']),
                clearable   = False,
                searchable  = True
            ),
            dcc.Dropdown(
                id          = 'measure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a measure',
                options     = DropdownInterface.get_measure_options(max(APP_CONFIG_SETTINGS['YEARS'])),
                value       = 'Contract Rent',
                clearable   = False,
                searchable  = True,
            ),
            # dcc.Dropdown(
            #     id          = 'submeasure-dropdown',
            #     className   = 'fmt-dropdown',
            #     placeholder = 'Select a submeasure',
            #     options     = submeasures_dict['Contract Rent'],
            #     clearable   = True,
            #     searchable  = False
            # )
        ]

        return dropdowns
    
    @classmethod
    def _offcanvas(cls) -> t.List[t.Union[dbc.Row, dbc.Offcanvas]]:
        """
        Retrieve the set of :py:class:`dash_bootstrap_components` components
        necessary for displaying the off-canvas element, and the button for
        interacting with the off-canvas element.
        """
        off_canvas_components = [
            dbc.Row(
                className = 'fmt-button',
                children  = [
                    dbc.Col(
                        className = 'help-button',
                        width     = 3,
                        children  = [
                            dbc.Button(
                                id       = "offcanvas-toggle-button",
                                outline  = True,
                                color    = 'primary',
                                n_clicks = 0,
                                children = "Help?"
                            )
                        ]
                    )
                ]
            ),
            dbc.Offcanvas(
                children = OffCanvasText.get_help_text('Contract Rent'),
                id      = "offcanvas",
                title   = html.H3("Help"),
                is_open = False,
                class_name = 'four columns'
            )
        ]

        return off_canvas_components
    
    @classmethod
    def _choropleth_map(cls) -> dcc.Loading:
        """
        Retrieve the :py:class:`dash.dcc.Graph` component corresponding
        to the choropleth map.
        
        Note that the :py:class:`dash.dcc.Graph` component is encased with
        a :py:class:`dash.dcc.Loading` component.
        """

        map = dcc.Graph(
            id               = 'map',
            className        = 'choropleth-map',
            responsive       = True,
            clear_on_unhover = True,
            config = {
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'],
                'displaylogo': False,
                'displayModeBar': False
            }
        )

        return map
    
    @classmethod
    def _choropleth_map_tooltip(cls) -> dcc.Tooltip:
        """
        Retrieve the :py:class:`dash.dcc.Tooltip` component corresponding
        to the choropleth map tooltip (active when a submeasure is selected).
        
        Note that the :py:class:`dash.dcc.Tooltip` component contains a
        a :py:class:`dash.dcc.Graph` component.
        """

        tooltip_figure = dcc.Graph(
            id               = "tooltip-graph",
            clear_on_unhover = True,
            config = {
                'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'],
                'displaylogo': False
            },
        )
        
        tooltip = dcc.Tooltip(
            id               = 'tooltip',
            direction        = 'bottom',
            background_color = '#FEF9F3',
            children  = tooltip_figure
        )

        return tooltip