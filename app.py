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
from page_components import DashLayout, OffCanvasText, DropdownInterface, SubmeasureInterface
from page_figure_styling import ChoroplethMapInterface, TooltipFigureInterface


# ────────────── #
# Initialization #
# ────────────── #

# Database pool
engine, _ = get_gcp_engine()



# ─── ─── ─── #
#     App     #
# ─── ─── ─── #
app = dash.Dash(
    external_stylesheets = [dbc.themes.CYBORG, "assets/style.css"]
)
server       = app.server
app.title    = 'California Socioeconomic Profile'
app._favicon = 'assets/favicon.ico'
app.layout   = DashLayout.serve_layout



# ─────────────────── #
# Page modal callback #
# ─────────────────── #
@app.callback(
    Output("pageload-modal", "is_open"),
    Input("close-pageload-modal", "n_clicks"),
    State("pageload-modal", "is_open"),
)
def toggle_page_modal(n_clicks, is_open):
    if n_clicks:
        return False
    return is_open


# ────────────────── #
# Dropdown callbacks #
# ────────────────── #
@app.callback(
    [
        Output('place-dropdown', 'options'),
        Output('year-dropdown', 'options'),
        Output('measure-dropdown', 'options'),
    ],
    [
        Input('place-dropdown', 'value'),
        Input('year-dropdown', 'value'),
        Input('measure-dropdown', 'value'),
    ]
)
def update_dropdown_options(place, year, measure):
    ctx      = dash.callback_context
    input_id = ctx.triggered[0]['prop_id'].split('.')[0]

    if input_id == 'place-dropdown':
        # A selected place affects the available years (but not the measures).
        year_options = DropdownInterface.get_year_options(place=place)
        return dash.no_update, year_options, dash.no_update
    
    if input_id == 'year-dropdown':
        # A selected year affects the available places, and the available measures.
        place_options   = DropdownInterface.get_place_options(year)
        measure_options = DropdownInterface.get_measure_options(year)
        return place_options, dash.no_update, measure_options
    
    if input_id == 'measure-dropdown':
        # There is incongruence between the calendar year support for a given place,
        # and the calendar year support for a given measure. As such, by disabling
        # those years for which either the place or measure are unsupported, we are
        # effectively capturing the common calendar year support shared by the given
        # place and the given measure.
        place_options = DropdownInterface.get_place_options(year)
        year_options  = DropdownInterface.get_year_options(place=place, measure=measure)
        return place_options, year_options, dash.no_update

@app.callback(
    Output('submeasure-dropdown', 'options'),
    Input('measure-dropdown', 'value')
)
def update_submeasure_dropdown_options(measure):
    if measure:
        return SubmeasureInterface.get_submeasure_options(measure)
    return dash.no_update


# ──────────────────── #
# Off-canvas callbacks #
# ──────────────────── #
@app.callback(
    Output("offcanvas", "is_open"),
    Input("offcanvas-toggle-button", "n_clicks"),
    State("offcanvas", "is_open")
)
def toggle_offcanvas(n_clicks, is_open):
    return True if n_clicks else is_open

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
    [
        Output('choropleth-map', 'figure'),
        Output('modal-datadownload-table', 'rowData'),
        Output('modal-datadownload-table', 'columnDefs'),
        Output('submeasure-dropdown', 'disabled'), # TODO: Drop
        Output('submeasure-dropdown', 'placeholder'), # TODO: Drop
    ],
    [
        Input('place-dropdown', 'value'),
        Input('year-dropdown', 'value'),
        Input('measure-dropdown', 'value'),
        Input('submeasure-dropdown', 'value')
    ],
    # Disable the dropdowns as the figure is generating (to prevent the user
    # from changing selection amidst an already loading query).
    running = [
        (Output("place-dropdown", "disabled"), True, False),
        (Output("year-dropdown", "disabled"), True, False),
        (Output("measure-dropdown", "disabled"), True, False),
        (Output("submeasure-dropdown", "disabled"), True, False)
    ]
)
def generate_choropleth_figure_and_data_table(place, year, measure, submeasure):
    with engine.connect() as conn:
        gdf = CloudReadTigerData.get_cali_tracts(conn, place, year)
        df  = CloudReadData.get_cali_tracts_data(conn, place, year, measure)

    fig = ChoroplethMapInterface.get_figure(df, gdf, place, year, measure)
    if submeasure is not None:
        fig.update_traces(hoverinfo = 'none', hovertemplate = None)

    # Note that we also outfit our data modal with the data we queried from the
    # database.
    rowData    = df.to_dict("records")
    columnDefs = [{"field": i} for i in df.columns]

    # TODO
    # This is a temporary bandaid for displaying only those submeasures
    # which are currently rigged.
    avail_measures = ['Contract Rent']
    sbm_cond = bool(measure not in avail_measures)
    sbm_text = 'Select a submeasure (optional)' if not sbm_cond else 'Unavailable at this time'

    return fig, rowData, columnDefs, sbm_cond, sbm_text

@app.callback(
    [
        Output('tooltip', 'show'),
        Output('tooltip-graph', 'figure'),
        Output('tooltip', 'bbox')
    ],
    [
        Input('choropleth-map', 'hoverData'),
        Input('submeasure-dropdown', 'value'),
        State('place-dropdown', 'value'),
        State('year-dropdown', 'value'),
        State('measure-dropdown', 'value'),
        State('modal-datadownload-table', 'rowData')
    ],
)
def generate_tooltip_figure(hoverData, submeasure, place, year, measure, rowData):
    if (submeasure is None) or (hoverData is None):
        return False, dash.no_update, dash.no_update

    point = hoverData['points'][0]
    bbox  = point['bbox']
    tract = point['customdata'][0]
    fig   = TooltipFigureInterface.get_figure(rowData, tract, place, year, measure, submeasure)
    return True, fig, bbox

# TODO: A bug appears wherein the hoverinfo displays if people change any
# of the other dropdowns beside the submeasure dropdown. For the time being,
# we supply the submeasure value as its own input in the choropleth figure
# callback.
# @app.callback(
#     Output('choropleth-map', 'figure', allow_duplicate=True),
#     [
#         Input('submeasure-dropdown', 'value'),
#         Input('place-dropdown', 'value'),
#         Input('year-dropdown', 'value'),
#         Input('measure-dropdown', 'value'),
#     ],
#     prevent_initial_call = True
# )
# def hide_choropleth_map_hoverinfo(submeasure, place, year, measure):
#     patched_figure = dash.Patch()

#     if submeasure is None:
#         patched_figure['data'][0]['hoverinfo']     = "all"
#         patched_figure['data'][0]['hovertemplate'] = ChoroplethMapInterface._get_hovertemplate(place, year, measure)
#     else:
#         patched_figure['data'][0]['hoverinfo']     = "none"
#         patched_figure['data'][0]['hovertemplate'] = None
    
#     return patched_figures


# ──────────────────── #
# Data modal callbacks #
# ──────────────────── #
@app.callback(
    [
        Output("datadownload-modal", "is_open"),
        Output('download-data-button', 'n_clicks'),
    ],
    [
        Input("close-datadownload-modal", "n_clicks"),
        Input("open-datadownload-modal", "n_clicks"),
        State("datadownload-modal", "is_open"),
    ]
)
def toggle_data_modal(n1, n2, is_open):
    # Note: By resetting 'download-data-button' to 0, we are preventing a bug wherein
    # modal displays may accidentally force the user into the download dialogue if
    # they have engaged it previously.
    if n1 or n2:
        return not is_open, 0
    return is_open, 0

@app.callback(
    [
        Output('modal-datadownload-table', 'exportDataAsCsv'),
        Output('modal-datadownload-table', 'csvExportParams'),
    ],
    [
        Input('download-data-button', 'n_clicks'),
        Input('place-dropdown', 'value'),
        Input('year-dropdown', 'value'),
        Input('measure-dropdown', 'value'),
    ]
)
def export_csv_file(n_clicks, place, year, measure):
    if n_clicks > 0:
        file_name = f"{place.replace(' ', '')}_{year}_{measure.replace(' ', '')}.csv"
        csvExportParams = {'fileName': file_name}
        return True, csvExportParams
    else:
        return False, {}



# ────────────── #
# Deploy the app #
# ────────────── #
if __name__ == '__main__':
    app.run(debug = False, host = "0.0.0.0", port = int(os.environ.get("PORT", 8080)))