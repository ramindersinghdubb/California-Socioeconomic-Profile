"""
Utility functions for the Plotly-Dash app UI.
"""
import typing as t



def add_color(
    color_dict: dict, color_name: str, color_list: list[str], num_colors: t.Optional[int] = None
) -> None:
    """
    Parameters
    ----------
    color_dict
        A color dictionary, which will store tuples of colors and fractions.

    color_name
        The name of the key in the color dictionary.

    color_list
        The list of colors.

    num_colors
        The number of colors, used to specify the tranches/fractions.

        Specify this *only* for continuous colors, as `plotly.express` figures
        using a color bar need tranches to reference color scaling.
    """
    if num_colors is not None:
        color_dict[color_name] = sorted(
            [ [1 - i/num_colors, color_list[i]] for i in list(range(0, num_colors + 1)) ]
        )
        return
    color_dict[color_name] = color_list