"""Module for the analyze screen component."""

import dash_bootstrap_components as dbc
import pandas as pd
from components.base_components import BaseComponent
from dash import Input, Output, State, dash, dcc, html
from utils.backend_api_client import BackendApiClient

BACKEND_API_CLIENT = BackendApiClient()


class AnalyzeScreen(BaseComponent):
    """Analyze screen component."""

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
                                    "Analyze CV",
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
                # Main Analyze content and analysis results
                dbc.Row(
                    [
                        # Left side of the screen
                        dbc.Col(
                            children=[
                                dbc.Tabs(
                                    [
                                        dbc.Tab(
                                            label="Analyze New Application",
                                            tab_id="tab-3",
                                            active_label_style={
                                                "color": "white",
                                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                            },
                                        ),
                                        dbc.Tab(
                                            label="View Applications",
                                            tab_id="tab-1",
                                            active_label_style={
                                                "color": "white",
                                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                            },
                                        ),
                                        dbc.Tab(
                                            label="Use Existing Knowledge Base",
                                            tab_id="tab-2",
                                            active_label_style={
                                                "color": "white",
                                                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                                            },
                                        ),
                                    ],
                                    id="analyze-tabs",
                                    active_tab="tab-3",
                                    style={
                                        "border": "1px solid rgba(255,255,255,0.2)",
                                        "borderRadius": "15px",
                                        "justifyContent": "center",
                                        "alignItems": "center",
                                    },
                                ),
                                html.Hr(),
                                html.Div(id="analyze-left-side-content"),
                                html.Br(),
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
                                                            "Analyze CV",
                                                            id="analyze-card-header",
                                                            className="mb-0",
                                                        )
                                                    ]
                                                ),
                                                dbc.CardBody(
                                                    [
                                                        html.Div(
                                                            id="analyze-card-table"
                                                        )
                                                    ]
                                                ),
                                            ],
                                            className="shadow-sm",
                                            style={"borderRadius": "15px"},
                                        )
                                    ],
                                ),
                            ],
                            width=10,
                        ),
                    ]
                ),
            ],
            id="analyze-screen",
            className="p-4",
        )

    @staticmethod
    def create_bullet_list(text_list: list):
        if not text_list:
            return ""

        return html.Ul([html.Li(line) for line in text_list])

    @staticmethod
    def create_analyze_table(analyze_data):
        """Create the analyze table."""

        if not analyze_data:
            return html.P(
                "No analyze data found", className="text-muted text-center"
            )

        general_recommendations = analyze_data.get(
            "general_recommendations", "N/A"
        )

        job_description_ats_skills_extracted_must_have = (
            AnalyzeScreen.create_bullet_list(
                analyze_data.get(
                    "job_description_ats_skills_extracted", {}
                ).get("must_have", [])
            )
        )

        job_description_ats_skills_extracted_nice_to_have = (
            AnalyzeScreen.create_bullet_list(
                analyze_data.get(
                    "job_description_ats_skills_extracted", {}
                ).get("nice_to_have", [])
            )
        )

        match_score = analyze_data.get("match_score", "N/A")
        missing_skills = AnalyzeScreen.create_bullet_list(
            analyze_data.get("missing_skills", [])
        )
        matched_skills = AnalyzeScreen.create_bullet_list(
            analyze_data.get("matched_skills", [])
        )
        new_cv_bullet_points = AnalyzeScreen.create_bullet_list(
            analyze_data.get("new_cv_bullet_points", [])
        )

        ats_keywords_included = AnalyzeScreen.create_bullet_list(
            analyze_data.get("ats_keywords_included", [])
        )

        return dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("General Recommendation"),
                            html.Th("ATS Skills Extrated (Must Have)"),
                            html.Th("ATS Skills Extrated (Nice to Have)"),
                            html.Th("Match Score"),
                            html.Th("Missing Skills"),
                            html.Th("Matched Skills"),
                            html.Th("New CV Bullet Points"),
                            html.Th("ATS Keywords Included"),
                        ]
                    )
                ),
                html.Tbody(
                    html.Tr(
                        [
                            html.Td(general_recommendations),
                            html.Td(
                                job_description_ats_skills_extracted_must_have,
                            ),
                            html.Td(
                                job_description_ats_skills_extracted_nice_to_have
                            ),
                            html.Td(
                                f"{float(match_score)*100}%"
                                if match_score != "N/A"
                                else "N/A"
                            ),
                            html.Td(missing_skills),
                            html.Td(matched_skills),
                            html.Td(new_cv_bullet_points),
                            html.Td(ats_keywords_included),
                        ]
                    )
                ),
            ],
            striped=True,
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the analyze screen component."""

        @app.callback(
            [
                Output("analyze-left-side-content", "children"),
                Output("analyze-card-table", "children", allow_duplicate=True),
            ],
            [Input("analyze-tabs", "active_tab")],
            [State("session-store", "data")],
            prevent_initial_call=True,
        )
        def update_analyze_left_side_content(active_tab, session_store):
            if active_tab == "tab-1":
                cv_analysis_jobs_response = (
                    BACKEND_API_CLIENT.get_cv_analysis_jobs(
                        session_store["username"]
                    )
                )

                cv_analysis_jobs = (
                    cv_analysis_jobs_response.get("data", {})
                    if cv_analysis_jobs_response
                    and cv_analysis_jobs_response.get("success")
                    else {}
                )

                cv_analysis_jobs_dropdown_options = [
                    {
                        "label": cv_analysis_job.get("id", "N/A"),
                        "value": cv_analysis_job.get("id", "N/A"),
                    }
                    for cv_analysis_job in cv_analysis_jobs
                ]

                return (
                    dbc.Row(
                        [
                            # CV dropdown
                            html.H6(
                                "Analysis Job",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                id="analyze-analysis-jobs-dropdown",
                                options=cv_analysis_jobs_dropdown_options,
                                value=0,
                                placeholder="Select an existing Analysis Job",
                                style={
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "color": "black",
                                    "padding": "2%",
                                },
                            ),
                            html.Hr(),
                            # CV section
                            html.H6(
                                "CV",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                                id="analyze-tab-1-cv-section-header",
                            ),
                            html.Div(
                                id="upload-tab-1-status-1",
                                className="mb-3",
                            ),
                            html.Hr(),
                            # Company section
                            html.H6(
                                "Company",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                                id="analyze-tab-1-company-section-header",
                            ),
                            html.Div(
                                id="upload-tab-1-status-2",
                                className="mb-3",
                            ),
                            html.Hr(),
                            # Job title section
                            html.H6(
                                "Job Title",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                                id="analyze-tab-1-job-title-section-header",
                            ),
                            html.Div(
                                id="upload-tab-1-status-3",
                                className="mb-3",
                            ),
                            html.Div(
                                dbc.Button(
                                    "Load",
                                    id="analyze-btn-1",
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
                    ),
                    None,
                )

            elif active_tab == "tab-2":
                # CV dropdown
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
                    if job_titles_response
                    and job_titles_response.get("success")
                    else {}
                ).get("job_titles", [])

                job_titles_dropdown_options = [
                    {
                        "label": job_title,
                        "value": job_title,
                    }
                    for job_title in job_titles
                ]

                return (
                    dbc.Row(
                        [
                            # CV dropdown
                            html.H6(
                                "CV",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                id="analyze-cv-dropdown-2",
                                options=cv_dropdown_options,
                                value=0,
                                placeholder="Select a CV",
                                style={
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "color": "black",
                                    "padding": "2%",
                                },
                            ),
                            html.Div(
                                id="upload-tab-2-status-1",
                                className="mb-3",
                            ),
                            html.Hr(),
                            # Company dropdown
                            html.H6(
                                "Company",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                id="analyze-company-dropdown",
                                options=company_names_dropdown_options,
                                value=0,
                                placeholder="Select a Company",
                                style={
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "color": "black",
                                    "padding": "2%",
                                },
                            ),
                            html.Div(
                                id="upload-tab-2-status-2",
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
                                id="analyze-job-title-dropdown",
                                options=job_titles_dropdown_options,
                                value=0,
                                placeholder="Select a Job Title",
                                style={
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "color": "black",
                                    "padding": "2%",
                                },
                            ),
                            html.Div(
                                id="upload-tab-2-status-3",
                                className="mb-3",
                            ),
                            html.Div(
                                dbc.Button(
                                    "Analyze",
                                    id="analyze-btn-2",
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
                    ),
                    None,
                )

            elif active_tab == "tab-3":

                # CV dropdown
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

                return (
                    dbc.Row(
                        [
                            # CV dropdown
                            html.H6(
                                "CV",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            dcc.Dropdown(
                                id="analyze-cv-dropdown-3",
                                options=cv_dropdown_options,
                                value=0,
                                placeholder="Select a CV",
                                style={
                                    "border": "none",
                                    "borderRadius": "8px",
                                    "color": "black",
                                    "padding": "2%",
                                },
                            ),
                            html.Div(
                                id="upload-tab-3-status-1",
                                className="mb-3",
                            ),
                            html.Hr(),
                            # Company dropdown
                            html.H6(
                                "Company URLs",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Textarea(
                                        id="analyze-company-urls-input-3",
                                        placeholder="Enter company URLs, one per line:\nhttps://company1.com\nhttps://company2.com/about\nhttps://company3.com/careers",
                                        style={
                                            "width": "100%",
                                            "height": "120px",
                                            "padding": "10px",
                                            "borderRadius": "8px",
                                            "border": "1px solid #ddd",
                                            "fontSize": "14px",
                                            "fontFamily": "monospace",
                                            "resize": "vertical",
                                        },
                                        value="",
                                    ),
                                ],
                                style={"marginBottom": "25px"},
                            ),
                            html.Div(
                                id="upload-tab-3-status-2",
                                className="mb-3",
                            ),
                            html.Hr(),
                            # Job title dropdown
                            html.H6(
                                "Job Description URLs",
                                style={
                                    "fontSize": "1.2rem",
                                    "marginTop": "10px",
                                },
                            ),
                            html.Div(
                                [
                                    dcc.Textarea(
                                        id="analyze-job-description-urls-input-3",
                                        placeholder="Enter job description URLs, one per line:\nhttps://company1.com\nhttps://company2.com/about\nhttps://company3.com/careers",
                                        style={
                                            "width": "100%",
                                            "height": "120px",
                                            "padding": "10px",
                                            "borderRadius": "8px",
                                            "border": "1px solid #ddd",
                                            "fontSize": "14px",
                                            "fontFamily": "monospace",
                                            "resize": "vertical",
                                        },
                                        value="",
                                    ),
                                ],
                                style={"marginBottom": "25px"},
                            ),
                            html.Div(
                                id="upload-tab-3-status-3",
                                className="mb-3",
                            ),
                            html.Div(
                                dbc.Button(
                                    "Analyze",
                                    id="analyze-btn-3",
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
                    ),
                    None,
                )

        @app.callback(
            [
                Output("upload-tab-1-status-1", "children"),
                Output("upload-tab-1-status-2", "children"),
                Output("upload-tab-1-status-3", "children"),
                Output("analyze-tab-1-cv-section-header", "children"),
                Output("analyze-tab-1-company-section-header", "children"),
                Output("analyze-tab-1-job-title-section-header", "children"),
            ],
            [Input("analyze-analysis-jobs-dropdown", "value")],
            prevent_initial_call=False,
        )
        def update_tab_1_status(job_id):
            if job_id:
                job_response = BACKEND_API_CLIENT.get_cv_analysis_job_by_id(
                    int(job_id)
                )

                job_data = (
                    job_response.get("data", {})
                    if job_response and job_response.get("success")
                    else {}
                )

                file_name = job_data.get("file_name", "N/A")
                company_name = job_data.get("company_name", "N/A")
                job_title = job_data.get("job_title", "N/A")

                cv_status_alert = dbc.Alert(
                    [
                        f"File {file_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                company_status_alert = dbc.Alert(
                    [
                        f"Company {company_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                job_status_alert = dbc.Alert(
                    [
                        f"Job {job_title} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return (
                    cv_status_alert,
                    company_status_alert,
                    job_status_alert,
                    f"CV {file_name}",
                    f"Company {company_name}",
                    f"Job {job_title}",
                )

            else:
                return [dash.no_update] * 6

        @app.callback(
            Output("upload-tab-2-status-1", "children"),
            [Input("analyze-cv-dropdown-2", "value")],
            [State("analyze-cv-dropdown-2", "options")],
            prevent_initial_call=False,
        )
        def update_tab_2_status_1(file_hash, options):
            if file_hash:
                file_name = [
                    option["label"]
                    for option in options
                    if option["value"] == file_hash
                ][0]

                status_alert = dbc.Alert(
                    [
                        f"File {file_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        @app.callback(
            Output("upload-tab-2-status-2", "children"),
            [Input("analyze-company-dropdown", "value")],
            prevent_initial_call=False,
        )
        def update_tab_2_status_2(company_name):
            if company_name:

                status_alert = dbc.Alert(
                    [
                        f"Company info for {company_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        @app.callback(
            Output("upload-tab-2-status-3", "children"),
            [Input("analyze-job-title-dropdown", "value")],
            prevent_initial_call=False,
        )
        def update_tab_2_status_3(job_title):
            if job_title:

                status_alert = dbc.Alert(
                    [
                        f"Job info for {job_title} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        @app.callback(
            Output("upload-tab-3-status-1", "children"),
            [Input("analyze-cv-dropdown-3", "value")],
            [State("analyze-cv-dropdown-3", "options")],
            prevent_initial_call=False,
        )
        def update_tab_3_status_1(file_hash, options):
            if file_hash:
                file_name = [
                    option["label"]
                    for option in options
                    if option["value"] == file_hash
                ][0]

                status_alert = dbc.Alert(
                    [
                        f"File {file_name} loaded successfully!",
                    ],
                    color="success",
                    className="mb-3",
                )

                return status_alert

            else:
                return dash.no_update

        # Tab 1 callbacks
        @app.callback(
            [
                Output("analyze-card-table", "children", allow_duplicate=True),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
            ],
            [Input("analyze-btn-1", "n_clicks")],
            [State("analyze-analysis-jobs-dropdown", "value")],
            prevent_initial_call=True,
        )
        def update_tab_1_analyze_card_table(n_clicks, job_id):
            if job_id:
                job_response = BACKEND_API_CLIENT.get_cv_analysis_job_by_id(
                    int(job_id)
                )

                job_data = (
                    job_response.get("data", {})
                    if job_response and job_response.get("success")
                    else {}
                )

                analyze_table = AnalyzeScreen.create_analyze_table(
                    job_data.get("raw_analysis_result", {})
                )

                return (
                    analyze_table,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            else:
                status_message = f"Please select a Job ID to load!"

                return (
                    dash.no_update,
                    status_message,
                    True,
                    "danger",
                )

        # Tab 2 callbacks
        @app.callback(
            [
                Output("analyze-card-table", "children", allow_duplicate=True),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
            ],
            [Input("analyze-btn-2", "n_clicks")],
            [
                State("analyze-cv-dropdown-2", "value"),
                State("analyze-cv-dropdown-2", "options"),
                State("analyze-company-dropdown", "value"),
                State("analyze-job-title-dropdown", "value"),
                State("session-store", "data"),
            ],
            prevent_initial_call=True,
        )
        def update_analyze_card_header(
            n_clicks,
            file_hash,
            options,
            company_name,
            job_title,
            session_store,
        ):
            if not n_clicks:
                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            if file_hash and company_name and job_title:
                file_name = [
                    option["label"]
                    for option in options
                    if option["value"] == file_hash
                ][0]

                object_key = f"{file_hash}/{file_name}"

                # Analyze the CV based on the company name and job title
                analyze_response = BACKEND_API_CLIENT.analyze_cv(
                    session_store["username"],
                    object_key,
                    company_name,
                    job_title,
                )

                analyze_data = (
                    analyze_response.get("data", {})
                    if analyze_response and analyze_response.get("success")
                    else {}
                )

                try:
                    job_response = (
                        BACKEND_API_CLIENT.get_cv_analysis_job_by_id(
                            int(analyze_data["job_id"])
                        )
                    )
                except Exception as e:
                    return [dash.no_update] * 4

                job_data = (
                    job_response.get("data", {})
                    if job_response and job_response.get("success")
                    else {}
                )

                analyze_table = AnalyzeScreen.create_analyze_table(
                    job_data.get("raw_analysis_result", {})
                )

                return (
                    analyze_table,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            else:
                status_message = (
                    f"Please select a CV, company, and job title to analyze!"
                )

                return (
                    dash.no_update,
                    status_message,
                    True,
                    "danger",
                )

        # Tab 3 callbacks
        @app.callback(
            [
                Output("analyze-card-table", "children", allow_duplicate=True),
                Output(
                    "upload-tab-3-status-2", "children", allow_duplicate=True
                ),
                Output(
                    "upload-tab-3-status-3", "children", allow_duplicate=True
                ),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
            ],
            [Input("analyze-btn-3", "n_clicks")],
            [
                State("analyze-cv-dropdown-3", "value"),
                State("analyze-cv-dropdown-3", "options"),
                State("analyze-company-urls-input-3", "value"),
                State("analyze-job-description-urls-input-3", "value"),
                State("session-store", "data"),
            ],
            prevent_initial_call=True,
        )
        def update_tab_3_analyze_card_table(
            n_clicks,
            file_hash,
            options,
            company_urls,
            job_description_urls,
            session_store,
        ):
            if not n_clicks:
                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                )

            if file_hash and company_urls and job_description_urls:
                file_name = [
                    option["label"]
                    for option in options
                    if option["value"] == file_hash
                ][0]

                object_key = f"{file_hash}/{file_name}"

                # URL cleanup -> extract URL info
                company_urls = [
                    url.strip() for url in company_urls.split("\n")
                ]

                job_description_urls = [
                    url.strip() for url in job_description_urls.split("\n")
                ]

                company_urls_response = (
                    BACKEND_API_CLIENT.extract_company_urls(company_urls)
                )

                job_description_urls_response = (
                    BACKEND_API_CLIENT.extract_jd_urls(job_description_urls)
                )

                # Check if there are existing Company URLs data
                if "existing_urls_data" in company_urls_response.get(
                    "data", {}
                ):
                    accessible_company_urls = (
                        company_urls_response.get("data", {})
                        .get("existing_urls_data", {})
                        .keys()
                    )

                    non_accessible_company_urls = []
                else:
                    accessible_company_urls = company_urls_response.get(
                        "data", {}
                    ).get("accessible_urls", [])

                    non_accessible_company_urls = company_urls_response.get(
                        "data", {}
                    ).get("non_accessible_urls", [])

                # Check if there are existing Job Description URLs data
                if "existing_urls_data" in job_description_urls_response.get(
                    "data", {}
                ):
                    accessible_job_description_urls = (
                        job_description_urls_response.get("data", {})
                        .get("existing_urls_data", {})
                        .keys()
                    )

                    non_accessible_job_description_urls = []

                    # Get the first non-null company name and job title
                    df = pd.DataFrame(
                        job_description_urls_response.get("data", {}).get(
                            "existing_urls_data", {}
                        )
                    ).T

                    first_non_null_per_col = df.apply(
                        lambda col: col.dropna().iloc[0]
                    )
                    company_name = first_non_null_per_col["company_name"]
                    job_title = first_non_null_per_col["job_title"]

                else:
                    accessible_job_description_urls = (
                        job_description_urls_response.get("data", {}).get(
                            "accessible_urls", []
                        )
                    )

                    non_accessible_job_description_urls = (
                        job_description_urls_response.get("data", {}).get(
                            "non_accessible_urls", []
                        )
                    )

                    company_name = job_description_urls_response.get(
                        "data", {}
                    ).get("company_name", "N/A")

                    job_title = job_description_urls_response.get(
                        "data", {}
                    ).get("job_title", "N/A")

                # Analyze the CV based on the company URLs and job description URLs
                if accessible_company_urls and accessible_job_description_urls:
                    analyze_response = BACKEND_API_CLIENT.analyze_cv(
                        session_store["username"],
                        object_key,
                        company_name,
                        job_title,
                    )
                else:
                    status_message = f"All the URLs are not accessible!"

                    status_alert = dbc.Alert(
                        [status_message],
                        color="danger",
                        className="mb-3",
                    )

                    return (
                        dash.no_update,
                        status_alert,
                        status_alert,
                        status_message,
                        True,
                        "danger",
                    )

                analyze_data = (
                    analyze_response.get("data", {})
                    if analyze_response and analyze_response.get("success")
                    else {}
                )

                try:
                    job_response = (
                        BACKEND_API_CLIENT.get_cv_analysis_job_by_id(
                            int(analyze_data["job_id"])
                        )
                    )
                except Exception as e:
                    return [dash.no_update] * 6

                job_data = (
                    job_response.get("data", {})
                    if job_response and job_response.get("success")
                    else {}
                )

                analyze_table = AnalyzeScreen.create_analyze_table(
                    job_data.get("raw_analysis_result", {})
                )

                # If there are some non-accessible URLs, show a warning
                if (
                    non_accessible_company_urls
                    or non_accessible_job_description_urls
                ):
                    status_message = f"Some of the URLs are not accessible: {non_accessible_company_urls} {non_accessible_job_description_urls}!"
                    status_color = "danger"

                    status_alert = dbc.Alert(
                        [status_message],
                        color=status_color,
                        className="mb-3",
                    )

                else:
                    status_message = f"All the URLs are accessible!"
                    status_color = "success"

                    status_alert = dbc.Alert(
                        [status_message],
                        color=status_color,
                        className="mb-3",
                    )

                return (
                    analyze_table,
                    status_alert,
                    status_alert,
                    status_message,
                    True,
                    status_color,
                )

            else:
                status_message = f"Please select a CV, and inserts company URLs, job description URLs to analyze!"

                return (
                    dash.no_update,
                    dash.no_update,
                    dash.no_update,
                    status_message,
                    True,
                    "danger",
                )

        @app.callback(
            Output("analyze-tabs", "active_tab"),
            [Input("url", "pathname")],
            prevent_initial_call=False,
        )
        def update_analyze_tabs(pathname):
            if pathname == "/analyze":
                return "tab-3"
            else:
                return dash.no_update
