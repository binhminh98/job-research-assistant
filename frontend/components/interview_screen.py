"""Interview screen component."""

import dash_bootstrap_components as dbc
from components.base_components import BaseComponent
from dash import Input, Output, State, dash, dcc, html
from utils.backend_api_client import BackendApiClient

BACKEND_API_CLIENT = BackendApiClient()


class InterviewScreen(BaseComponent):
    """Interview screen component."""

    @staticmethod
    def render():
        return html.Div(
            children=[
                # Title
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H2(
                                    "Interview Preparation",
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
                # Main interview screen content
                dbc.Row(
                    [
                        # Left side of the screen
                        dbc.Col(
                            children=[
                                dbc.Row(
                                    [
                                        # Company dropdown
                                        html.H6(
                                            "Company",
                                            style={
                                                "fontSize": "1.2rem",
                                                "marginTop": "10px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="interview-company-dropdown",
                                            options=[],
                                            value=None,
                                            placeholder="Select a Company",
                                            style={
                                                "border": "none",
                                                "borderRadius": "8px",
                                                "color": "black",
                                                "padding": "2%",
                                            },
                                        ),
                                        html.Div(
                                            id="interview-upload-status-1",
                                            className="mb-3",
                                        ),
                                        html.Hr(),
                                        # Job title dropdown
                                        html.H6(
                                            "Job Title",
                                            style={
                                                "fontSize": "1.2rem",
                                                "marginTop": "10px",
                                            },
                                        ),
                                        dcc.Dropdown(
                                            id="interview-job-title-dropdown",
                                            options=[],
                                            value=None,
                                            placeholder="Select a Job Title",
                                            style={
                                                "border": "none",
                                                "borderRadius": "8px",
                                                "color": "black",
                                                "padding": "2%",
                                            },
                                        ),
                                        html.Div(
                                            id="interview-upload-status-2",
                                            className="mb-3",
                                        ),
                                        html.Div(
                                            dbc.Button(
                                                "Generate",
                                                id="interview-btn",
                                                color="primary",
                                                className="me-2",
                                                style={
                                                    "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                                    "border": "none",
                                                    "borderRadius": "8px",
                                                },
                                            ),
                                            style={
                                                "textAlign": "center",
                                            },
                                        ),
                                    ],
                                )
                            ],
                            width=2,
                        ),
                        # Right side of the screen
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
                                            "Loading...",
                                            dbc.Spinner(
                                                color="primary", type="border"
                                            ),
                                        ],
                                        className="text-center",
                                    ),
                                    children=[
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    [
                                                        html.H4(
                                                            "Interview Questions and Answers",
                                                            id="interview-card-header-1",
                                                            className="mb-0",
                                                        )
                                                    ]
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            id="interview-card-table-1"
                                                        )
                                                    ]
                                                ),
                                            ],
                                            className="shadow-sm",
                                            style={"borderRadius": "15px"},
                                        ),
                                        dbc.Card(
                                            [
                                                dbc.CardHeader(
                                                    [
                                                        html.H4(
                                                            "Additional Resources",
                                                            id="interview-card-header-2",
                                                            className="mb-0",
                                                        )
                                                    ]
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            id="interview-card-table-2"
                                                        )
                                                    ]
                                                ),
                                            ],
                                            className="shadow-sm",
                                            style={"borderRadius": "15px"},
                                        ),
                                    ],
                                ),
                            ],
                            width=10,
                        ),
                    ]
                ),
            ],
            id="interview-screen",
            className="p-4",
        )

    @staticmethod
    def create_interview_card_table_questions_and_answers_table(
        interview_data,
    ):
        """Create the interview card table questions and answers table."""

        if not interview_data:
            return html.P(
                "No analyze data found", className="text-muted text-center"
            )

        interview_questions = interview_data.get(
            "generated_interview_questions", {}
        )
        interview_answers = interview_data.get(
            "generated_interview_answers", {}
        )

        categories = [
            (
                "General Questions",
                "general_questions",
                "answers_general_questions",
            ),
            (
                "Behavioral Questions",
                "behavioral_questions",
                "answers_behavioral_questions",
            ),
            (
                "Technical Questions",
                "technical_questions",
                "answers_technical_questions",
            ),
        ]

        all_tables = []

        for category_name, q_key, a_key in categories:
            questions = interview_questions.get(q_key, [])
            answers = interview_answers.get(a_key, [])

            # Create table rows
            rows = []
            max_items = max(len(questions), len(answers))

            for i in range(max_items):
                question = questions[i] if i < len(questions) else ""
                answer = answers[i] if i < len(answers) else ""

                rows.append(
                    html.Tr(
                        [
                            html.Td(
                                f"Q{i+1}: {question}",
                                style={
                                    "padding": "12px",
                                    "backgroundColor": "#e3f2fd",
                                    "borderBottom": "1px solid #ddd",
                                    "width": "45%",
                                    "verticalAlign": "top",
                                },
                            ),
                            html.Td(
                                f"A{i+1}: {answer}",
                                style={
                                    "padding": "12px",
                                    "backgroundColor": "#f3e5f5",
                                    "borderBottom": "1px solid #ddd",
                                    "width": "55%",
                                    "verticalAlign": "top",
                                },
                            ),
                        ]
                    )
                )

            table = html.Div(
                [
                    html.H5(
                        f"{category_name} ({len(questions)} items)",
                        style={"color": "#495057", "marginBottom": "15px"},
                    ),
                    html.Table(
                        [
                            html.Thead(
                                [
                                    html.Tr(
                                        [
                                            html.Th(
                                                "Questions",
                                                style={
                                                    "backgroundColor": "#6c757d",
                                                    "color": "white",
                                                    "padding": "12px",
                                                    "textAlign": "center",
                                                },
                                            ),
                                            html.Th(
                                                "Suggested Answers",
                                                style={
                                                    "backgroundColor": "#6c757d",
                                                    "color": "white",
                                                    "padding": "12px",
                                                    "textAlign": "center",
                                                },
                                            ),
                                        ]
                                    )
                                ]
                            ),
                            html.Tbody(rows),
                        ],
                        style={
                            "width": "100%",
                            "borderCollapse": "collapse",
                            "marginBottom": "30px",
                            "border": "1px solid #ddd",
                        },
                    ),
                ]
            )

            all_tables.append(table)

        return html.Div(
            [
                *all_tables,
            ],
            style={"padding": "20px"},
        )

    @staticmethod
    def create_interview_card_table_additional_resources_table(interview_data):
        """Create the interview card table additional resources table."""

        if not interview_data:
            return html.P(
                "No interview data found", className="text-muted text-center"
            )

        additional_resources = interview_data.get(
            "generated_additional_resources", {}
        )
        additional_resources = additional_resources.get(
            "additional_resources", []
        )

        return dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("Additional Resources"),
                        ]
                    )
                ),
                html.Tbody(
                    html.Tr(
                        [
                            html.Td(
                                [
                                    html.Li(resource)  # Make it a bullet list
                                    for resource in additional_resources
                                ]
                            ),
                        ]
                    )
                ),
            ],
            striped=True,
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the interview screen component."""

        @app.callback(
            Output("interview-upload-status-1", "children"),
            [Input("interview-company-dropdown", "value")],
            prevent_initial_call=False,
        )
        def update_interview_upload_status_1(company_name):
            if company_name:
                status_alert = dbc.Alert(
                    [
                        f"Company {company_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        @app.callback(
            Output("interview-upload-status-2", "children"),
            [Input("interview-job-title-dropdown", "value")],
            prevent_initial_call=False,
        )
        def update_interview_upload_status_2(job_title):
            if job_title:

                status_alert = dbc.Alert(
                    [
                        f"Job title info for {job_title} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        @app.callback(
            [
                Output(
                    "interview-card-table-1", "children", allow_duplicate=True
                ),
                Output(
                    "interview-card-table-2", "children", allow_duplicate=True
                ),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
            ],
            [Input("interview-btn", "n_clicks")],
            [
                State("interview-company-dropdown", "value"),
                State("interview-job-title-dropdown", "value"),
            ],
            prevent_initial_call=True,
        )
        def update_interview_card_table(n_clicks, company_name, job_title):
            if company_name and job_title:

                interview_response = BACKEND_API_CLIENT.interview_prep(
                    company_name,
                    job_title,
                )

                interview_data = (
                    interview_response.get("data", {})
                    if interview_response and interview_response.get("success")
                    else {}
                )

                interview_card_table_questions_and_answers = InterviewScreen.create_interview_card_table_questions_and_answers_table(
                    interview_data.get("result", {})
                )

                interview_card_table_additional_resources = InterviewScreen.create_interview_card_table_additional_resources_table(
                    interview_data.get("result", {})
                )

                status_message = interview_data.get("message", "N/A")

                return (
                    interview_card_table_questions_and_answers,
                    interview_card_table_additional_resources,
                    status_message,
                    True,
                    "success",
                )

            else:
                status_message = (
                    f"Please select a company and job title to generate!"
                )

                return (
                    dash.no_update,
                    dash.no_update,
                    status_message,
                    True,
                    "danger",
                )

        @app.callback(
            Output("interview-company-dropdown", "options"),
            Output("interview-job-title-dropdown", "options"),
            [
                Input("url", "pathname"),
            ],
            State("session-store", "data"),
            prevent_initial_call=True,
        )
        def populate_dropdown_options(pathname, session_store):
            if pathname != "/interview" or not session_store:
                return [], []

            # Company dropdown
            company_names_response = BACKEND_API_CLIENT.get_company_names(
                session_store["username"]
            )

            company_names = (
                company_names_response.get("data", {})
                if company_names_response
                and company_names_response.get("success")
                else {}
            ).get("company_names", [])

            company_names_dropdown_options = [
                {
                    "label": company_name,
                    "value": company_name,
                }
                for company_name in company_names
            ]

            # Job title dropdown
            job_titles_response = BACKEND_API_CLIENT.get_job_titles(
                session_store["username"]
            )

            job_titles = (
                job_titles_response.get("data", {})
                if job_titles_response and job_titles_response.get("success")
                else {}
            ).get("job_titles", [])

            job_titles_dropdown_options = [
                {
                    "label": job_title,
                    "value": job_title,
                }
                for job_title in job_titles
            ]

            return company_names_dropdown_options, job_titles_dropdown_options
