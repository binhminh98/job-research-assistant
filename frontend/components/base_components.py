"""
Base frontend component for the Job Research Assistant app.
"""

from abc import ABC, abstractmethod
from typing import Any

from dash import Input, Output, dash, html


class BaseComponent(ABC):
    @staticmethod
    @abstractmethod
    def render(*args, **kwargs) -> Any:
        pass

    @staticmethod
    @abstractmethod
    def register_callbacks(app: dash.Dash) -> None:
        pass


class PageTitle(BaseComponent):
    """
    Page title component.

    Components/Ids:
        - page-title-container: page-title-container
    """

    @staticmethod
    def render(title: str, tagline: str):
        """
        Render the Job Research Assistant title for any page.
        """
        return html.Div(
            [
                html.Span(
                    [
                        title,
                        " - ",
                        html.I(tagline),
                    ]
                ),
            ],
            style={
                "fontSize": "2rem",
                "fontWeight": "600",
                "color": "white",
                "marginLeft": "15px",
            },
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the page title component."""

        @app.callback(
            Output("page-title-container", "children"),
            [Input("url", "pathname")],
            prevent_initial_call=True,
        )
        def update_page_title(pathname):
            """Update page title based on current page/tab"""

            title = "🤖 AI-Powered CV Tailoring"
            tagline = "Land more interviews with a CV that fits"

            return PageTitle.render(title, tagline)
