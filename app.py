"""
Entry-point for the Plotly-Dash app.
"""
import os, sys
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

sys.path.insert(0, str(Path.cwd()))
from db_retrieval import CloudReadData, CloudReadTigerData, get_gcp_engine
from page_components import (
    DashLayout, OffCanvasText,
    get_dependent_year_place_dropdown_options,
    get_dependent_year_measure_dropdown_options,
    # submeasures_dict
)
from page_figure_styling import ChoroplethMapInterface


# ────────────── #
# Initialization #
# ────────────── #

# Database pool
engine, _ = get_gcp_engine()

# Necessary as Dash won't natively render JS files unless directly specified
JS_FOLDER  = Path.cwd() / 'assets' / 'js' / 'clientside_callbacks'
JS_SCRIPTS = [f'assets/js/clientside_callbacks/{i}' for i in os.listdir(JS_FOLDER)]



# ─── ─── ─── #
#     App     #
# ─── ─── ─── #
app = dash.Dash(
    external_stylesheets = [dbc.themes.CYBORG, "assets/style.css"],
    external_scripts     = JS_SCRIPTS,
)
server       = app.server
app.title    = 'California Socioeconomic Profile'
app._favicon = 'assets/favicon.ico'
app.layout   = DashLayout.serve_layout



# ────────────── #
# Modal callback #
# ────────────── #
@app.callback(
    Output("pageload-modal", "is_open"),
    Input("close-modal", "n_clicks"),
    State("pageload-modal", "is_open"),
)
def toggle_modal(n_clicks, is_open):
    if n_clicks:
        return False
    return is_open

# ────────────────── #
# Dropdown callbacks #
# ────────────────── #
@app.callback(
    Output('place-dropdown', 'options'),
    Output('year-dropdown', 'options'),
    Output('measure-dropdown', 'options'),
    Input('place-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('measure-dropdown', 'value'),
)
def update_dropdown_options(place, year, measure):
    ctx      = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    YEAR_PLACE_OPTIONS, PLACE_YEAR_OPTIONS     = get_dependent_year_place_dropdown_options()
    YEAR_MEASURE_OPTIONS, MEASURE_YEAR_OPTIONS = get_dependent_year_measure_dropdown_options()

    if input_id == 'place-dropdown':
        # A selected place affects the available years (but not the measures).
        return dash.no_update, PLACE_YEAR_OPTIONS[place], dash.no_update
    if input_id == 'year-dropdown':
        # A selected year affects the available places, and the available measures.
        return YEAR_PLACE_OPTIONS[year], dash.no_update, YEAR_MEASURE_OPTIONS[year]
    if input_id == 'measure-dropdown':
        # There is incongruence between the calendar year support for a given place,
        # and the calendar year support for a given measure. As such, by disabling
        # those years for which either the place or measure are unsupported, we are
        # effectively capturing the common calendar year support shared by the given
        # place and the given measure.
        p_yr_options = PLACE_YEAR_OPTIONS[place]
        m_yrs = {i['value']: i['disabled'] for i in MEASURE_YEAR_OPTIONS[measure]}
        p_yrs = {i['value']: i['disabled'] for i in p_yr_options}
        modified_yr_options = [
            {
                **i,
                'disabled': True if any(j[i['value']] for j in [m_yrs,p_yrs]) else False
            }
            for i in p_yr_options
        ]
        return YEAR_PLACE_OPTIONS[year], modified_yr_options, dash.no_update

# @app.callback(
#     Output('submeasure-dropdown', 'options'),
#     Input('measure-dropdown', 'value')
# )
# def update_submeasure_dropdown_options(measure):
#     if measure:
#         return submeasures_dict[measure]
#     return dash.no_update


# ──────────────────── #
# Off-canvas callbacks #
# ──────────────────── #
@app.callback(
    Output("offcanvas", "is_open"),
    Input("offcanvas-toggle-button", "n_clicks"),
    State("offcanvas", "is_open")
)
def toggle_offcanvas(n_clicks, is_open):
    state = True if n_clicks else is_open
    return state

@app.callback(
    Output('offcanvas', 'children'),
    Input('measure-dropdown', 'value'),
)
def update_offcanvas_text(measure):
    return OffCanvasText.get_help_text(measure)

# ──────────────── #
# Figure callbacks #
# ──────────────── #
@app.callback(
    Output('map', 'figure'),
    Input('place-dropdown', 'value'),
    Input('year-dropdown', 'value'),
    Input('measure-dropdown', 'value')
)
def update_figure(place, year, measure):
    with engine.connect() as conn:
        gdf = CloudReadTigerData.get_cali_tracts(conn, place, year)
        df  = CloudReadData.get_cali_tracts_data(conn, place, year, measure)

    fig = ChoroplethMapInterface.get_figure(df, gdf, place, year, measure)

    return fig


# Tooltip figure
# app.clientside_callback(
#     dash.ClientsideFunction('clientside_figure_callbacks', 'tooltip_figure_function'),
#     [Output('tooltip', 'show'),
#      Output('tooltip-graph', 'figure'),
#      Output('tooltip', 'bbox')],
#     [Input('year-dropdown', 'value'),
#      Input('submeasure-dropdown', 'value'),
#      Input('map', 'hoverData'),
#      Input('tooltip_file', 'data'),
#      Input('discrete-color-dict', 'data'),
#      Input('place-dropdown', 'value'),]
# )



# ────────────── #
# Deploy the app #
# ────────────── #
if __name__ == '__main__':
    app.run(debug = False, host = "0.0.0.0", port = int(os.environ.get("PORT", 8080)))