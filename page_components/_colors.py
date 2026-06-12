"""
Discrete and continuous color scales.

Used primarily for plotting and the tooltip.
"""

import plotly.express as px

import sys
from pathlib import Path
sys.path.insert(0, str(Path.cwd()))
from page_components._utils import add_color



# ─────────────── #
# Discrete colors #
# ─────────────── #
def get_discrete_color_dict():
    """
    Get the dictionary containing discrete color scales.
    """
    DISC_COLOR_DICT = dict()

    DISC_COLOR_PARAMETERS = [
        ('G10', px.colors.qualitative.G10),
        ('Viridis', px.colors.sequential.Viridis),
        ('Magma', px.colors.sequential.Magma),
        ('GnBu', px.colors.sequential.GnBu),
        ('D3_5', px.colors.qualitative.D3[0:5]),
        ('D3_7', px.colors.qualitative.D3[0:7]),
        ('Reds_2', ['#F69697', '#FF0500']),
        ('Same_Reds_5', ['#F69697'] * 5),
        ('Same_Reds_8', ['#F69697'] * 8),
        ('Greens_10', px.colors.sequential.Greens + ['rgb(0,65,26)']),
        ('Oranges', px.colors.sequential.Oranges[0:7] + ['rgb(149, 49, 3)', 'rgb(133, 43, 2)']),
        ('Pastel2', px.colors.qualitative.Pastel2 + ['rgb(179,205,227)']),
        ('Set3', px.colors.qualitative.Set3 + ['rgb(251,180,174)']),
        (
            'Okabe_8',
            ['#000000', '#CC79A7', '#D55E00', '#0072B2',
            '#F0E442', '#009E73', '#56B4E9', '#E69F00']
        ),
        (
            'YlOrRd_9',
            ['rgb(255, 255, 204)', 'rgb(255, 237, 160)', 'rgb(254, 217, 118)', 'rgb(254, 178, 76)',
            'rgb(253, 141, 60)', 'rgb(252, 78, 42)', 'rgb(227, 26, 28)', 'rgb(189, 0, 38)',
            'rgb(128, 0, 38)']
        ),
        (
            'YlOrRd_12',
            ['rgb(255, 255, 204)', 'rgb(255, 242, 172)', 'rgb(255, 228, 141)', 'rgb(254, 210, 110)',
            'rgb(254, 182, 80)', 'rgb(253, 154, 66)', 'rgb(253, 118, 53)', 'rgb(250, 73, 41)',
            'rgb(232, 35, 31)', 'rgb(206, 12, 33)', 'rgb(172, 0, 38)', 'rgb(128, 0, 38)']
        ),
        (
            'Blues',
            ['rgb(247,251,255)', 'rgb(222, 238, 255)', 'rgb(197, 226, 255)', 'rgb(172, 213, 255)',
            'rgb(147, 201, 255)', 'rgb(121, 188, 255)', 'rgb(96, 176, 255)', 'rgb(71, 163, 255)',
            'rgb(46, 151, 255)', 'rgb(21, 138, 255)', 'rgb(0, 125, 251)', 'rgb(0, 113, 226)',
            'rgb(0, 100, 201)']
        )
    ]

    for (color_key, color_list) in DISC_COLOR_PARAMETERS:
        add_color(DISC_COLOR_DICT, color_key, color_list)

    return DISC_COLOR_DICT


# ───────────────── #
# Continuous colors #
# ───────────────── #
def get_continuous_color_dict():
    """
    Get the dictionary containing continuous color scales.
    """
    CONT_COLOR_DICT = dict()

    CONT_COLOR_PARAMETERS = [
        ('YlGnBu', px.colors.sequential.YlGnBu, 8),
        ('YlGn', px.colors.sequential.YlGn, 8),
        ('deep', px.colors.sequential.deep, 11),
        ('Emrld', px.colors.sequential.Emrld, 6),
        ('Mint', px.colors.sequential.Mint, 6),
        ('PuBuGn', px.colors.sequential.PuBuGn, 8),
        ('DarkMint', px.colors.sequential.Darkmint, 6),
        ('Magma', px.colors.sequential.Magma, 9),
        ('Hot', px.colors.sequential.Hot, 3),
        ('OrRd', px.colors.sequential.OrRd, 8),
        ('matter', px.colors.sequential.matter, 11),
    ]

    for (color_key, color_list, tranche_count) in CONT_COLOR_PARAMETERS:
        add_color(CONT_COLOR_DICT, color_key, color_list, tranche_count)

    return CONT_COLOR_DICT