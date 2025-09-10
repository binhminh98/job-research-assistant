"""Upload screen component."""

import dash_bootstrap_components as dbc
from components.base_components import BaseComponent
from dash import Input, Output, State, dash, dcc, html
from utils.backend_api_client import BackendApiClient

BACKEND_API_CLIENT = BackendApiClient()


class UploadScreen(BaseComponent):
    """Upload screen for CV file uploads with drag-and-drop functionality."""

    @staticmethod
    def render():
        """
        Create the upload screen layout.

        Components/Ids:
            - cv-dropdown: cv-dropdown
            - cv-upload: cv-upload
            - upload-status: upload-status
            - cv-preview-table: cv-preview-table
            - upload-screen: upload-screen
        """

        return html.Div(
            [
                # Title
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "CV upload & preview",
                                    className="text-center mb-4",
                                    style={
                                        "fontWeight": "600",
                                        "fontSize": "2rem",
                                        "color": "#4c4baa",
                                    },
                                )
                            ],
                            width=12,
                        )
                    ],
                    className="mb-4",
                ),
                # Main Upload Card and preview
                dbc.Row(
                    [
                        # Upload Section
                        dbc.Col(
                            [
                                dcc.Upload(
                                    id="cv-upload",
                                    children=html.Div(
                                        [
                                            html.Div(
                                                [
                                                    html.Img(
                                                        src="/assets/upload.svg",
                                                        style={
                                                            "height": "80px",
                                                            "width": "80px",
                                                            "marginBottom": "20px",
                                                        },
                                                    ),
                                                    html.H4(
                                                        "Select a file or drag here",
                                                        className="mb-3",
                                                        style={
                                                            "fontWeight": "400",
                                                            "color": "#4c4baa",
                                                        },
                                                    ),
                                                    dbc.Button(
                                                        "Upload new CV",
                                                        id="upload-select-file-btn",
                                                        color="primary",
                                                        className="me-2",
                                                        style={
                                                            "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                            "border": "none",
                                                            "borderRadius": "8px",
                                                        },
                                                    ),
                                                ],
                                                className="text-center",
                                            )
                                        ],
                                        style={
                                            "height": "300px",
                                            "display": "flex",
                                            "alignItems": "center",
                                            "justifyContent": "center",
                                            "border": "2px dashed rgba(0,0,0,0.3)",
                                            "borderRadius": "15px",
                                            "backgroundColor": "rgba(0,34,255,0.05)",
                                            "transition": "all 0.3s ease",
                                        },
                                    ),
                                    style={
                                        "width": "100%",
                                        "borderRadius": "15px",
                                    },
                                    multiple=False,
                                    accept=".pdf,.doc,.docx,.txt",
                                ),
                                html.Br(),
                                # CV dropdown
                                dcc.Dropdown(
                                    id="cv-dropdown",
                                    options=[],
                                    value=0,
                                    placeholder="Select an existing CV",
                                    style={
                                        "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                        "border": "none",
                                        "borderRadius": "8px",
                                        "color": "black",
                                    },
                                    className="custom-dropdown",
                                ),
                                # Upload Status and Actions
                                dbc.Row(
                                    [
                                        dbc.Col(
                                            [
                                                html.Div(
                                                    id="upload-status",
                                                    className="mb-3",
                                                ),
                                            ],
                                            width=12,
                                        )
                                    ]
                                ),
                            ],
                            width=2,
                        ),
                        # CV Data Parser Preview Section
                        dbc.Col(
                            [
                                dcc.Loading(
                                    type="cube",
                                    overlay_style={
                                        "visibility": "visible",
                                        "filter": "blur(5px)",
                                    },
                                    custom_spinner=html.H2(
                                        [
                                            "Loading... ",
                                            dbc.Spinner(
                                                color="primary", type="border"
                                            ),
                                        ],
                                        className="text-center",
                                    ),
                                    children=dbc.Card(
                                        [
                                            dbc.CardHeader(
                                                [
                                                    html.H5(
                                                        "CV parser preview",
                                                        className="mb-0",
                                                        style={
                                                            "fontWeight": "500",
                                                            "color": "#4c4baa",
                                                        },
                                                    )
                                                ],
                                                style={
                                                    "backgroundColor": "rgba(255,255,255,0.1)",
                                                    "border": "none",
                                                    "borderRadius": "15px 15px 0 0",
                                                },
                                            ),
                                            dbc.CardBody(
                                                [
                                                    # Preview Table
                                                    html.Div(
                                                        id="cv-preview-table",
                                                    )
                                                ],
                                                style={
                                                    "backgroundColor": "rgba(255,255,255,0.05)",
                                                    "border": "none",
                                                },
                                            ),
                                        ],
                                        style={
                                            "backgroundColor": "transparent",
                                            "border": "1px solid rgba(255,255,255,0.2)",
                                            "borderRadius": "15px",
                                        },
                                    ),
                                )
                            ],
                            width=10,
                        ),
                    ],
                    className="mb-4",
                ),
            ],
            id="upload-screen",
            className="p-4",
        )

    @staticmethod
    def create_cv_preview_table(cv_data):
        """Create the CV preview table."""
        if not cv_data:
            return html.P(
                "No cv data found", className="text-muted text-center"
            )

        return dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("File Name"),
                            html.Th("Name"),
                            html.Th("Contact"),
                            html.Th("Skills"),
                            html.Th("Summary"),
                            html.Th("Experience"),
                            html.Th("Education"),
                            html.Th("Certifications"),
                            html.Th("Languages"),
                        ]
                    )
                ),
                html.Tbody(
                    html.Tr(
                        [
                            html.Td(cv_data.get("file_name", "N/A")),
                            html.Td(
                                cv_data.get("extracted_text", {}).get(
                                    "name", "N/A"
                                )
                            ),
                            html.Td(
                                [
                                    dbc.Badge(
                                        f"{cv_data.get('contact', 'N/A')}",
                                        color="secondary",
                                    ),
                                ],
                                className="text-center",
                            ),
                            html.Td(cv_data.get("skills", "N/A")),
                            html.Td(cv_data.get("summary", "N/A")),
                            html.Td(cv_data.get("experience", "N/A")),
                            html.Td(cv_data.get("education", "N/A")),
                            html.Td(cv_data.get("certifications", "N/A")),
                            html.Td(cv_data.get("languages", "N/A")),
                        ]
                    )
                ),
            ],
            striped=True,
        )

    @staticmethod
    def register_callbacks(app):
        """Register callbacks for the upload screen."""

        @app.callback(
            [
                Output("upload-status", "children"),
                Output("cv-preview-table", "children"),
            ],
            [Input("cv-upload", "contents")],
            [State("cv-upload", "filename"), State("session-store", "data")],
            prevent_initial_call=True,
        )
        def handle_file_upload(contents, filename, session_store):
            """Handle file upload and preview."""
            # Upload file to MinIO
            if contents is None:
                return "", ""
            else:
                try:
                    response = BACKEND_API_CLIENT.upload_file(
                        session_store["username"], contents, filename
                    )

                    file_hash = (
                        response.get("data").get("object_key").split("/")[0]
                        if response
                        else ""
                    )

                except Exception as e:
                    error_alert = dbc.Alert(
                        [
                            f"Error uploading file: {str(e)}",
                        ],
                        color="danger",
                        className="mb-3",
                    )
                    return error_alert, ""

            try:
                # Show upload status
                status_alert = dbc.Alert(
                    [
                        f"File '{filename}' uploaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                cv_response = BACKEND_API_CLIENT.get_cv_data_by_file_hash(
                    file_hash
                )

                cv_data = (
                    cv_response.get("data", {})
                    if cv_response and cv_response.get("success")
                    else {}
                )

                preview_table = UploadScreen.create_cv_preview_table(cv_data)

                return status_alert, preview_table

            except Exception as e:
                error_alert = dbc.Alert(
                    [
                        f"Error processing file: {str(e)}",
                    ],
                    color="danger",
                    className="mb-3",
                )
                return error_alert, ""

        @app.callback(
            [
                Output("cv-dropdown", "options"),
                Output("cv-preview-table", "children", allow_duplicate=True),
            ],
            [Input("cv-dropdown", "value")],
            [State("session-store", "data")],
            prevent_initial_call=True,
        )
        def update_cv_preview_table_from_dropdown(value, session_store):
            """Update the CV preview table from dropdown."""
            cv_response = BACKEND_API_CLIENT.get_cv_data_by_username(
                session_store["username"]
            )

            cv_data = (
                cv_response.get("data", {})
                if cv_response and cv_response.get("success")
                else {}
            )

            cv_dropdown_options = [
                {
                    "label": cv.get("file_name", "N/A"),
                    "value": cv.get("file_hash", "N/A"),
                }
                for cv in cv_data
            ]

            cv_response = BACKEND_API_CLIENT.get_cv_data_by_file_hash(value)

            cv_data = (
                cv_response.get("data", {})
                if cv_response and cv_response.get("success")
                else {}
            )

            preview_table = UploadScreen.create_cv_preview_table(cv_data)

            return cv_dropdown_options, preview_table
