"""
Entry-point for the Plotly-Dash app.
"""
import os

import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, ClientsideFunction
from dash.dependencies import Output, Input, State
from feffery_markdown_components import FefferyMarkdown

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components import *



YEAR_PLACE_OPTIONS, PLACE_YEAR_OPTIONS = get_dependent_year_place_dropdown_options()
YEAR_MEASURE_OPTIONS, MEASURE_YEAR_OPTIONS = get_dependent_year_measure_dropdown_options()

# Necessary as Dash won't natively render JS files unless directly specified
JS_FOLDER  = Path.cwd() / 'assets' / 'js' / 'clientside_callbacks'
JS_SCRIPTS = [f'assets/js/clientside_callbacks/{i}' for i in os.listdir(JS_FOLDER)]



# ─── ─── ─── #
#     App     #
# ─── ─── ─── #
app = Dash(
    __name__,
    external_stylesheets = [dbc.themes.CYBORG, "assets/style.css"],
    external_scripts     = JS_SCRIPTS
)
server = app.server
app.title = 'California Socioeconomic Profile'


app.layout = html.Div([
    html.Div(className = "row", children = [
        # ─── LEFT ─── #
        html.Div(className = "four columns", children = [
            html.H3("California Socioeconomic Profile"),
            html.P("Using the American Community Survey, this website allows you to visualize various socioeconomic measures for cities in California.",
                   className = 'text-p'),
            html.P("Use the dropdowns to navigate your selection process.",
                   className = 'text-p'),
            dcc.Dropdown(
                id          = 'place-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a place',
                options     = YEAR_PLACE_OPTIONS[max(APP_CONFIG_SETTINGS['YEAR'])],
                value       = 'LosAngeles',
                clearable   = False,
                searchable  = True,
            ),
            dcc.Dropdown(
                id          = 'year-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a year',
                options     = PLACE_YEAR_OPTIONS['LosAngeles'],
                value       = max(APP_CONFIG_SETTINGS['YEAR']),
                clearable   = False,
                searchable  = False
            ),
            dcc.Dropdown(
                id          = 'measure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a measure',
                options     = YEAR_MEASURE_OPTIONS[max(APP_CONFIG_SETTINGS['YEAR'])],
                value       = 'ContractRent',
                clearable   = False
            ),
            dcc.Dropdown(
                id          = 'submeasure-dropdown',
                className   = 'fmt-dropdown',
                placeholder = 'Select a submeasure',
                options     = submeasures_dict['ContractRent'],
                clearable   = True,
                searchable  = False
            ),
            dbc.Row(className = 'fmt-button', children = [
                dbc.Col(width = 3, children = [
                    dbc.Button("Help?",
                               id         = "open-offcanvas",
                               outline    = True,
                               color      = 'primary',
                               n_clicks   = 0)],
                         className = 'help-button'
                        )
            ]),
            dbc.Offcanvas(
                FefferyMarkdown(id          = "help-text",
                                renderHtml  = True,
                                className  = 'offcanvas-body'
                               ),
                id      = "offcanvas",
                title   = html.H3("Help"),
                is_open = False,
                class_name = 'four columns'
            )
        ]),
        # ─── RIGHT ─── #
        html.Div(className= "eight columns chart-layout",
                 children = [dcc.Loading(id        = 'loading-sign',
                                         className = 'loading',
                                         color     = '#F8F8FF',
                                         display   = 'show',
                                        ),
                             dcc.Graph(id     = 'map',
                                       config = {'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'], 'displaylogo': False, 'displayModeBar': False},
                                       clear_on_unhover = True
                                      ),
                             dcc.Tooltip(id        = 'tooltip',
                                         children  = [dcc.Graph(id               = "tooltip-graph",
                                                                config           = {'modeBarButtonsToRemove': ['pan2d', 'lasso2d', 'select2d', 'resetview'], 'displaylogo': False},
                                                                clear_on_unhover = True,
                                                               )],
                                         direction = 'bottom',
                                         background_color = '#FEF9F3',
                                        )
                            ]
                )
    ]),
    # ─── DATA ─── #
    dcc.Store(id = "masterfile"),
    dcc.Store(id = "tooltip_file"),
    dcc.Store(id = "mapfile"),
    dcc.Store(id = "discrete_color_dict",   data = get_discrete_color_dict()),
    dcc.Store(id = "continuous_color_dict", data = get_continuous_color_dict()),
    dcc.Store(id = "year-place-options",    data = YEAR_PLACE_OPTIONS),
    dcc.Store(id = "place-year-options",    data = PLACE_YEAR_OPTIONS),
    dcc.Store(id = "year-measure-options",  data = YEAR_MEASURE_OPTIONS),
    dcc.Store(id = "measure-year-options",  data = MEASURE_YEAR_OPTIONS),
    dcc.Store(id = "submeasures-dict",      data = submeasures_dict)
])



# ───────── #
# Dropdowns #
# ───────── #

# Place options (given the selected year)
app.clientside_callback(
    ClientsideFunction('clientside_dropdowns', 'place_options_function'),
    Output('place-dropdown', 'options'),
    [Input('year-dropdown', 'value'),
     Input('year-place-options', 'data')]
)


# Year options (given the selected city and measure)
app.clientside_callback(
    ClientsideFunction('clientside_dropdowns', 'year_options_function'),
    Output('year-dropdown', 'options'),
    [Input('place-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('place-year-options', 'data'),
     Input('measure-year-options', 'data')]
)


# Measure options (given the selected year)
app.clientside_callback(
    ClientsideFunction('clientside_dropdowns', 'measure_options_functions'),
    Output('measure-dropdown', 'options'),
    [Input('year-dropdown', 'value'),
     Input('year-measure-options', 'data')]
)


# Submeasure options (given the selected measure)
app.clientside_callback(
    ClientsideFunction('clientside_dropdowns', 'submeasure_options_function'),
    Output('submeasure-dropdown', 'options'),
    [Input('measure-dropdown', 'value'),
     Input('submeasures-dict', 'data')]
)



# ────────── #
# Off-canvas #
# ────────── #

# Display the off-canvas
app.clientside_callback(
    ClientsideFunction('clientside_off_canvas_callbacks', 'display_canvas_function'),
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    State("offcanvas", "is_open")
)


# Control the off-canvas help text
app.clientside_callback(
    ClientsideFunction('clientside_off_canvas_callbacks', 'display_canvas_help_function'),
    Output("help-text", "markdownStr"),
    Input('measure-dropdown', 'value')
)



# ────────────── #
# Data callbacks #
# ────────────── #

# Masterfile data
app.clientside_callback(
    ClientsideFunction('clientside_data_callbacks', 'masterfile_data'),
    Output('masterfile', 'data'),
    [Input('year-dropdown', 'value'),
     Input('place-dropdown', 'value'),
     Input('measure-dropdown', 'value')]
)


# Tooltip data
app.clientside_callback(
    ClientsideFunction('clientside_data_callbacks', 'tooltip_data'),
    Output('tooltip_file', 'data'),
    [Input('year-dropdown', 'value'),
     Input('place-dropdown', 'value'),
     Input('submeasure-dropdown', 'value')]
)


# Center-point data
app.clientside_callback(
    ClientsideFunction('clientside_data_callbacks', 'mapfile_center_points_data'),
    Output('mapfile', 'data'),
    [Input('year-dropdown', 'value')]
)


# Redundancy for disabling tooltip data
app.clientside_callback(
    ClientsideFunction('clientside_data_callbacks', 'tooltip_redundancy'),
    Output('tooltip', 'className'),
    Input('submeasure-dropdown', 'value')
)



# ────────────── #
# Plotly figures #
# ────────────── #

# Choropleth map
app.clientside_callback(
    ClientsideFunction('clientside_figure_callbacks', 'choropleth_map_function'),
    Output('map', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('place-dropdown', 'value'),
     Input('measure-dropdown', 'value'),
     Input('submeasure-dropdown', 'value'),
     Input('masterfile', 'data'),
     Input('mapfile', 'data'),
     Input('continuous_color_dict', 'data')]
)


# Tooltip figure
app.clientside_callback(
    ClientsideFunction('clientside_figure_callbacks', 'tooltip_figure_function'),
    [Output('tooltip', 'show'),
     Output('tooltip-graph', 'figure'),
     Output('tooltip', 'bbox')],
    [Input('year-dropdown', 'value'),
     Input('submeasure-dropdown', 'value'),
     Input('map', 'hoverData'),
     Input('tooltip_file', 'data'),
     Input('discrete_color_dict', 'data'),
     Input('place-dropdown', 'value'),
     Input('year-place-options', 'data')]
)



# ─────────── #
# Run the app #
# ─────────── #
if __name__ == '__main__':
    app.run(debug = False, host="0.0.0.0", port = int(os.environ.get("PORT", 8080)))