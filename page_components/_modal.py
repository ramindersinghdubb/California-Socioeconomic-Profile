"""
Styling for the modal pop-up.
"""
import typing as t
from datetime import datetime
from pathlib import Path

import pandas as pd
import dash_bootstrap_components as dbc
import dash_ag_grid as dag
from dash import html



class ModalInterface:
    """
    Interface for formatting the necessary `dash_bootstrap_components.Modal`
    components.
    """

    @classmethod
    def get_pageload_modal(cls) -> dbc.Modal:
        """
        Retrieve the `dash_bootstrap_components.Modal` component for when the page loads.

        This component consists of a(n) :py:class:`dash_bootstrap_components.ModalBody`
        component and a(n) :py:class:`dash_bootstrap_components.ModalFooter` component.
        """
        modal_body = cls.__pageload_modal_body_content()
        modal_foot = cls.__pageload_modal_footer_content()
        
        modal = dbc.Modal(
            id       = "pageload-modal",
            is_open  = True,
            size     = "l",
            children = [modal_body, modal_foot]
        )

        return modal
    
    @classmethod
    def get_datadownload_modal(cls) -> dbc.Modal:
        """
        Retrieve the `dash_bootstrap_components.Modal` component for data downloads.

        This component consists of a(n) :py:class:`dash_bootstrap_components.ModalBody`
        component and a(n) :py:class:`dash_bootstrap_components.ModalFooter` component.
        """
        modal_body = cls.__datadownload_modal_body()
        modal_foot = cls.__datadownload_modal_footer_content()

        modal = dbc.Modal(
            id       = "datadownload-modal",
            is_open  = False,
            size     = "lg",
            children = [modal_body, modal_foot]
        )

        return modal


    @classmethod
    def __pageload_modal_body_content(cls) -> dbc.ModalBody:
        """
        :py:class:`dash_bootstrap_components.ModalBody` component for the body
        content of the modal pop-up. Note that this component will contain an
        image.
        """
        title = html.H4(
            className = "modal-title text-center my-4",
            children  = ["California Socioeconomic Profile"],
        )

        image = cls.__pageload_modal_image_comp()

        info_text = """
        The California Socioeconomic Profile makes use of the United States Census Bureau's
        American Community Survey to visualize key social, demographic, and economic information
        across census tracts for major cities in California.
        """
        author_text = html.P(
            className = "modal-comp",
            children  = f"Raminder Singh Dubb, {datetime.now().year}"
        )

        note_text = html.P(
            className = "modal-comp",
            style     = {'font-style': 'italic'},
            children = "This app is best viewed on a tablet or computer."
        )
        
        info_text  = html.P(
            className = "modal-body",
            children  = [info_text, note_text, author_text]
        )

        modal_body = dbc.ModalBody(
            children = [
                dbc.Row(
                    children = [
                        dbc.Col(
                            width    = 12,
                            children = [title, image, info_text]
                        )
                    ]
                )
            ]
        )

        return modal_body

    @classmethod
    def __pageload_modal_footer_content(cls) -> dbc.ModalFooter:
        """
        :py:class:`dash_bootstrap_components.ModalFooter` component for the footer
        content of the modal pop-up.
        """
        modal_footer = dbc.ModalFooter(
            dbc.Button(
                id        = "close-pageload-modal",
                className = "ml-auto",
                color     = "secondary",
                children  = ["Close"],
            )
        )

        return modal_footer

    @classmethod
    def __pageload_modal_image_comp(cls) -> html.Div:
        """
        :py:class:`html.Div` component containing the image and the image caption.
        """
        photographer, year, source_link, img_link = cls.__get_random_modal_image().values()

        image_comp = html.Img(
                className = "modal-image modal-comp", src = img_link
            )

        image_caption_comp = html.Div(
            className = "modal-comp",
            children  = [
                html.Figcaption(
                    className = "modal-image-caption",
                    children  = [
                        html.A(
                            children = [f"{photographer}, {year}"],
                            href     = source_link
                        )
                    ]
                )
            ]
        )

        modal_image_component = html.Div(
            className = "modal-div", 
            children  = [image_comp, image_caption_comp],
        )

        return modal_image_component
    
    @classmethod
    def __get_random_modal_image(cls) -> t.Dict[str, t.Any]:
        """
        Sample the `pandas.DataFrame` object containing information on the
        modal pop-up images and return a formatted dictionary corresponding
        to the sample.
        """
        file = Path.cwd() / 'assets' / 'modal_images' / 'metadata.csv'
        df = pd.read_csv(file, sep='|', skiprows=[7,28,29,30,36]) # <- Vertical-oriented images
        modal_dict = dict( zip(df.columns, df.sample().values[0]) )
        return modal_dict
    

    @classmethod
    def __datadownload_modal_body(cls) -> dbc.ModalBody:
        """
        :py:class:`dash_bootstrap_components.ModalBody` component for the body
        content of the data pop-up.
        """
        title = html.H4(
            className = "modal-title my-4",
            children  = ["Data"],
        )

        grid = dag.AgGrid(
            id              = "modal-datadownload-table",
            className       = "data-table",
            dashGridOptions = {
                "pagination": True,
                "paginationPageSizeSelector": False,
                "paginationPageSize": 10,
                "animateRows": False,
                "theme": "themeAlpine"
            },
        )

        # modal_body = dbc.ModalBody(
        #     children = [
        #         dbc.Row(
        #             children = [
        #                 dbc.Col(
        #                     width    = 12,
        #                     children = [title, grid]
        #                 )
        #             ]
        #         )
        #     ]
        # )

        modal_body = dbc.ModalBody(
            children = [title, grid]
        )

        return modal_body
    
    @classmethod
    def __datadownload_modal_footer_content(cls) -> dbc.ModalFooter:
        """
        :py:class:`dash_bootstrap_components.ModalFooter` component for the footer
        content of the modal pop-up.
        """

        modal_footer = dbc.ModalFooter(
            className = "custom-modal-footer",
            children  = [
                dbc.Button(
                    id        = "download-data-button",
                    color     = "info",
                    children  = ["Download CSV"],
                ),
                dbc.Button(
                    id        = "close-datadownload-modal",
                    className = "ml-auto",
                    color     = "secondary",
                    children  = ["Close"]
                )
            ]
        )

        return modal_footer