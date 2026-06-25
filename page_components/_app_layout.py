"""
Layout for the Dash app.
"""
import typing as t

import dash_bootstrap_components as dbc
from dash import dcc, html

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._modal import ModalInterface
from page_components._off_canvas import OffCanvasText
from page_components._dropdowns import DropdownInterface
from page_components._submeasures_options import SubmeasureInterface
from page_components.config import CONFIG_SETTINGS as APP_CONFIG_SETTINGS



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
            children = [cls.app_display(),]
        )
        return layout

    @classmethod
    def app_display(cls) -> html.Div:
        """
        Retrieve the py:class:`dash.html.Div` component for the
        app component
        """
        app_div = html.Div(
            className = "row",
            children  = [
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
                ModalInterface.get_pageload_modal(),
                ModalInterface.get_datadownload_modal(),
                *cls._toggle_schema(),
            ]
        )
        
        return left_col
    
    @classmethod
    def right_column(cls) -> dcc.Loading:
        """
        Retrieve the py:class:`dash.dcc.Loading` component corresponding
        to the right column of the Dash app.

        This column contains the choropleth map and the tooltip (active
        when a sub-measure is selected). Note that the
        py:class:`dash.dcc.Loading` component is only active when changes
        are made to the choropleth map figure.
        """

        right_col = dcc.Loading(
            parent_className = "eight columns chart-layout",
            id        = 'loading-sign',
            className = 'loading',
            color     = '#F8F8FF',
            children  = [
                cls._choropleth_map(),
                cls._choropleth_map_tooltip()
            ],
            target_components = {"choropleth-map": "figure"}
        )
        
        return right_col
    
    @classmethod
    def _header(cls) -> t.List[t.Union[html.H3, html.P]]:
        """
        Retrieve the set of :py:class:`dash.html` components used in
        the Dash app heading info.
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
            dcc.Dropdown(
                id          = 'submeasure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a submeasure (optional)',
                options     = SubmeasureInterface.get_submeasure_options('Contract Rent'),
                clearable   = True,
                searchable  = True
            )
        ]

        return dropdowns
    
    @classmethod
    def _toggle_schema(cls) -> t.List[t.Union[dbc.Row, dbc.Offcanvas]]:
        """
        Retrieve the set of :py:class:`dash_bootstrap_components` components
        necessary for displaying the off-canvas element, the button for
        interacting with the off-canvas element, and the button for displaying
        the data-download pop-up.
        """
        off_canvas_components = [
            dbc.Row(
                className = 'fmt-button',
                children  = [
                    dbc.Col(
                        width     = 4,
                        children  = [
                            dbc.Button(
                                id       = "offcanvas-toggle-button",
                                outline  = True,
                                color    = 'primary',
                                n_clicks = 0,
                                children = "Help?"
                            )
                        ]
                    ),
                    dbc.Col(
                        width     = 4,
                        children  = [
                            dbc.Button(
                                id       = "open-datadownload-modal",
                                outline  = True,
                                color    = 'info',
                                n_clicks = 0,
                                children = "Data"
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
    def _choropleth_map(cls) -> dcc.Graph:
        """
        Retrieve the :py:class:`dash.dcc.Graph` component corresponding
        to the choropleth map.
        """

        map = dcc.Graph(
            id               = 'choropleth-map',
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
            children         = [tooltip_figure]
        )

        return tooltip