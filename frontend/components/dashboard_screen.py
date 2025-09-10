"""Module for the dashboard screen component."""

import json
from datetime import datetime

import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from components.base_components import BaseComponent
from dash import Input, Output, State, ctx, dash, dcc, html
from utils.backend_api_client import BackendApiClient

BACKEND_API_CLIENT = BackendApiClient()


class DashboardScreen(BaseComponent):
    """
    Dashboard screen component with user analytics and statistics.

    Components/Ids:
        - active-card-store: active-card-store
        - dashboard-user-stats-cards: dashboard-user-stats-cards
        - dashboard-overview-card-1-header: dashboard-overview-card-1-header
        - dashboard-overview-card-1-chart: dashboard-overview-card-1-chart
        - dashboard-overview-card-2-header: dashboard-overview-card-2-header
        - dashboard-overview-card-2-chart: dashboard-overview-card-2-chart
        - dashboard-overview-card-3-header: dashboard-overview-card-3-header
        - dashboard-overview-card-3-table: dashboard-overview-card-3-table
        - dashboard-overview-card-4-header: dashboard-overview-card-4-header
        - dashboard-overview-card-4-table: dashboard-overview-card-4-table
        - dashboard-overview-card-5-header: dashboard-overview-card-5-header
        - dashboard-overview-card-5-table: dashboard-overview-card-5-table
        - dashboard-screen: dashboard-screen
    """

    @staticmethod
    def render():
        return html.Div(
            [
                dcc.Store(
                    id="active-card-store",
                    data="dashboard-total-cvs-uploaded-card",
                ),
                # Statistics Cards
                html.Div(id="dashboard-user-stats-cards", className="mb-4"),
                # Charts Section
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H4(
                                                    id="dashboard-overview-card-1-header",
                                                    className="mb-0",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="dashboard-overview-card-1-chart",
                                                )
                                            ]
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={"borderRadius": "15px"},
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H4(
                                                    id="dashboard-overview-card-2-header",
                                                    className="mb-0",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                dcc.Graph(
                                                    id="dashboard-overview-card-2-chart"
                                                )
                                            ]
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={"borderRadius": "15px"},
                                )
                            ],
                            width=6,
                        ),
                    ],
                    className="mb-4",
                ),
                # Recent Users Table
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H4(
                                                    id="dashboard-overview-card-3-header",
                                                    className="mb-0",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="dashboard-overview-card-3-table"
                                                )
                                            ]
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={"borderRadius": "15px"},
                                )
                            ],
                            width=6,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H4(
                                                    id="dashboard-overview-card-4-header",
                                                    className="mb-0",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="dashboard-overview-card-4-table"
                                                )
                                            ]
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={"borderRadius": "15px"},
                                )
                            ],
                            width=3,
                        ),
                        dbc.Col(
                            [
                                dbc.Card(
                                    [
                                        dbc.CardHeader(
                                            [
                                                html.H4(
                                                    id="dashboard-overview-card-5-header",
                                                    className="mb-0",
                                                )
                                            ]
                                        ),
                                        dbc.CardBody(
                                            [
                                                html.Div(
                                                    id="dashboard-overview-card-5-table"
                                                )
                                            ]
                                        ),
                                    ],
                                    className="shadow-sm",
                                    style={"borderRadius": "15px"},
                                )
                            ],
                            width=3,
                        ),
                    ]
                ),
            ],
            id="dashboard-screen",
            className="p-4",
        )

    @staticmethod
    def create_stats_cards(
        cv_data, company_names, job_titles, ai_analysis_jobs
    ):
        """Create statistics cards for the dashboard."""
        total_cvs_uploaded = len(cv_data) if cv_data else 0
        total_companies = len(company_names) if company_names else 0
        total_job_titles = len(job_titles) if job_titles else 0
        total_ai_analysis_jobs = (
            len(ai_analysis_jobs) if ai_analysis_jobs else 0
        )

        return dbc.Row(
            [
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                [
                                                    html.H2(
                                                        str(
                                                            total_cvs_uploaded
                                                        ),
                                                        className="text-info mb-0",
                                                        style={
                                                            "fontSize": "2.5rem",
                                                            "fontWeight": "bold",
                                                        },
                                                        id="dashboard-total-cvs-uploaded-card-number",
                                                    ),
                                                    html.P(
                                                        "Total CVs Uploaded",
                                                        className="text-muted mb-0",
                                                    ),
                                                ],
                                                className="position-relative",
                                            )
                                        ]
                                    )
                                ],
                                id="dashboard-total-cvs-uploaded-card",
                                className="text-center shadow-sm dashboard-card",
                                style={
                                    "borderRadius": "15px",
                                    "border": "none",
                                    "background": "linear-gradient(135deg, #17a2b820 0%, #1e88e520 100%)",
                                    "cursor": "pointer",
                                },
                            ),
                            id="dashboard-total-cvs-uploaded-card-button",
                            n_clicks=0,
                        )
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                [
                                                    html.H2(
                                                        str(total_companies),
                                                        className="text-info mb-0",
                                                        style={
                                                            "fontSize": "2.5rem",
                                                            "fontWeight": "bold",
                                                        },
                                                        id="dashboard-total-companies-card-number",
                                                    ),
                                                    html.P(
                                                        "Companies",
                                                        className="text-muted mb-0",
                                                    ),
                                                ],
                                                className="position-relative",
                                            )
                                        ]
                                    )
                                ],
                                id="dashboard-total-companies-card",
                                className="text-center shadow-sm dashboard-card",
                                style={
                                    "borderRadius": "15px",
                                    "border": "none",
                                    "background": "linear-gradient(135deg, #17a2b820 0%, #1e88e520 100%)",
                                    "cursor": "pointer",
                                },
                            ),
                            id="dashboard-total-companies-card-button",
                            n_clicks=0,
                        )
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                [
                                                    html.H2(
                                                        str(total_job_titles),
                                                        className="text-info mb-0",
                                                        style={
                                                            "fontSize": "2.5rem",
                                                            "fontWeight": "bold",
                                                        },
                                                        id="dashboard-total-job-descriptions-card-number",
                                                    ),
                                                    html.P(
                                                        "Job Descriptions",
                                                        className="text-muted mb-0",
                                                    ),
                                                ],
                                                className="position-relative",
                                            )
                                        ]
                                    )
                                ],
                                id="dashboard-total-job-descriptions-card",
                                className="text-center shadow-sm dashboard-card",
                                style={
                                    "borderRadius": "15px",
                                    "border": "none",
                                    "background": "linear-gradient(135deg, #17a2b820 0%, #1e88e520 100%)",
                                    "cursor": "pointer",
                                },
                            ),
                            id="dashboard-total-job-descriptions-card-button",
                            n_clicks=0,
                        ),
                    ],
                    width=3,
                ),
                dbc.Col(
                    [
                        html.Div(
                            dbc.Card(
                                [
                                    dbc.CardBody(
                                        [
                                            html.Div(
                                                [
                                                    html.H2(
                                                        str(
                                                            total_ai_analysis_jobs
                                                        ),
                                                        className="text-info mb-0",
                                                        style={
                                                            "fontSize": "2.5rem",
                                                            "fontWeight": "bold",
                                                        },
                                                        id="dashboard-total-ai-analysis-jobs-card-number",
                                                    ),
                                                    html.P(
                                                        "AI Analysis Jobs",
                                                        className="text-muted mb-0",
                                                    ),
                                                ],
                                                className="position-relative",
                                            )
                                        ]
                                    )
                                ],
                                id="dashboard-total-ai-analysis-jobs-card",
                                className="text-center shadow-sm dashboard-card",
                                style={
                                    "borderRadius": "15px",
                                    "border": "none",
                                    "background": "linear-gradient(135deg, #17a2b820 0%, #1e88e520 100%)",
                                    "cursor": "pointer",
                                },
                            ),
                            id="dashboard-total-ai-analysis-jobs-card-button",
                            n_clicks=0,
                        ),
                    ],
                    width=3,
                ),
            ]
        )

    @staticmethod
    def create_cv_data_table(cv_data):
        """Create a table of recent 5 cv data."""
        if not cv_data:
            return html.P(
                "No cv data found", className="text-muted text-center"
            )

        # Sort by ID (most recent first) and take top 10
        sorted_cv = sorted(cv_data, key=lambda x: x.get("id", 0))[:5]

        table_rows = []
        for cv in sorted_cv:
            table_rows.append(
                html.Tr(
                    [
                        html.Td(
                            [
                                dbc.Badge(
                                    f"{cv.get('id', 'N/A')}",
                                    color="secondary",
                                ),
                            ],
                            className="text-center",
                        ),
                        html.Td(cv.get("file_name", "N/A")),
                        html.Td(cv.get("summary", "N/A")),
                        html.Td(
                            datetime.fromisoformat(
                                cv.get("inserted_at", "N/A")
                            ).strftime("%d %b, %Y")
                        ),
                        html.Td(
                            datetime.fromisoformat(
                                cv.get("updated_at", "N/A")
                            ).strftime("%d %b, %Y")
                        ),
                    ]
                )
            )

        return dbc.Table(
            [
                html.Thead(
                    html.Tr(
                        [
                            html.Th("ID", className="text-center"),
                            html.Th("File Name"),
                            html.Th("Summary"),
                            html.Th("Inserted At"),
                            html.Th("Updated At"),
                        ]
                    )
                ),
                html.Tbody(table_rows),
            ],
            striped=True,
            hover=True,
            responsive=True,
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the dashboard screen component."""

        @app.callback(
            Output("dashboard-user-stats-cards", "children"),
            [Input("url", "pathname")],
            [State("session-store", "data")],
            prevent_initial_call=False,
        )
        def populate_user_stats_cards(pathname, session_store):
            if pathname == "/dashboard":
                # Fetch cv data
                cv_response = BACKEND_API_CLIENT.get_cv_data_by_username(
                    session_store["username"]
                )

                cv_data = (
                    cv_response.get("data", [])
                    if cv_response and cv_response.get("success")
                    else []
                )

                # Fetch company names
                company_names_response = BACKEND_API_CLIENT.get_company_names(
                    session_store["username"]
                )

                company_names = (
                    company_names_response.get("data", {})
                    if company_names_response
                    and company_names_response.get("success")
                    else {}
                ).get("company_names", [])

                # Fetch job titles from company names
                job_titles_response = BACKEND_API_CLIENT.get_job_titles()

                job_titles = (
                    job_titles_response.get("data", {})
                    if job_titles_response
                    and job_titles_response.get("success")
                    else {}
                ).get("job_titles", [])

                # Fetch ai analysis jobs
                ai_analysis_jobs_response = (
                    BACKEND_API_CLIENT.get_cv_analysis_jobs(
                        session_store["username"]
                    )
                )

                ai_analysis_jobs = (
                    ai_analysis_jobs_response.get("data", {})
                    if ai_analysis_jobs_response
                    and ai_analysis_jobs_response.get("success")
                    else {}
                )

                # Create stats cards
                stats_cards = DashboardScreen.create_stats_cards(
                    cv_data, company_names, job_titles, ai_analysis_jobs
                )

                return stats_cards

            else:
                return dash.no_update

        @app.callback(
            Output("active-card-store", "data"),
            [
                Input("dashboard-total-cvs-uploaded-card-button", "n_clicks"),
                Input("dashboard-total-companies-card-button", "n_clicks"),
                Input(
                    "dashboard-total-job-descriptions-card-button", "n_clicks"
                ),
                Input(
                    "dashboard-total-ai-analysis-jobs-card-button", "n_clicks"
                ),
            ],
            prevent_initial_call=False,
        )
        def update_active_card_store(
            n_clicks, n_clicks_2, n_clicks_3, n_clicks_4
        ):
            button_id = ctx.triggered[0]["prop_id"].split(".")[0]
            return button_id

        @app.callback(
            [
                Output(
                    "dashboard-total-cvs-uploaded-card-number", "className"
                ),
                Output("dashboard-total-cvs-uploaded-card", "style"),
                Output("dashboard-total-companies-card-number", "className"),
                Output("dashboard-total-companies-card", "style"),
                Output(
                    "dashboard-total-job-descriptions-card-number", "className"
                ),
                Output("dashboard-total-job-descriptions-card", "style"),
                Output(
                    "dashboard-total-ai-analysis-jobs-card-number", "className"
                ),
                Output("dashboard-total-ai-analysis-jobs-card", "style"),
            ],
            [
                Input("active-card-store", "data"),
            ],
            prevent_initial_call=False,
        )
        def update_active_card_styles(active_card_store):
            # Inactive card number text color and style
            inactive_card_number_class = "text-info mb-0"
            inactive_card_style = {
                "borderRadius": "15px",
                "border": "none",
                "background": "linear-gradient(135deg, #17a2b820 0%, #1e88e520 100%)",
                "cursor": "pointer",
            }

            # Make the card number text color and style active
            active_card_number_class = "text-primary"
            active_card_style = {
                "borderRadius": "15px",
                "border": "none",
                "background": "linear-gradient(135deg, #667eea20 0%, #764ba220 100%)",
                "cursor": "pointer",
            }

            if active_card_store == "dashboard-total-cvs-uploaded-card-button":
                return (
                    active_card_number_class,
                    active_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                )
            elif active_card_store == "dashboard-total-companies-card-button":
                return (
                    inactive_card_number_class,
                    inactive_card_style,
                    active_card_number_class,
                    active_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                )
            elif (
                active_card_store
                == "dashboard-total-job-descriptions-card-button"
            ):
                return (
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    active_card_number_class,
                    active_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                )
            elif (
                active_card_store
                == "dashboard-total-ai-analysis-jobs-card-button"
            ):
                return (
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    inactive_card_number_class,
                    inactive_card_style,
                    active_card_number_class,
                    active_card_style,
                )
            else:
                return (
                    inactive_card_number_class,
                    inactive_card_style,
                ) * 4

        @app.callback(
            [
                Output(
                    "dashboard-overview-card-1-header",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-1-chart",
                    "figure",
                ),
                Output(
                    "dashboard-overview-card-2-header",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-2-chart",
                    "figure",
                ),
                Output(
                    "dashboard-overview-card-3-header",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-3-table",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-4-header",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-4-table",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-5-header",
                    "children",
                ),
                Output(
                    "dashboard-overview-card-5-table",
                    "children",
                ),
            ],
            [Input("url", "pathname")],
            [State("session-store", "data")],
            prevent_initial_call=False,
        )
        def update_dashboard(pathname, session_store):
            # Fetch cv data
            cv_response = BACKEND_API_CLIENT.get_cv_data_by_username(
                session_store["username"]
            )

            cv_data = (
                cv_response.get("data", [])
                if cv_response and cv_response.get("success")
                else []
            )

            if cv_data:
                df_users = pd.DataFrame(cv_data)
                df_users["inserted_at"] = pd.to_datetime(
                    df_users["inserted_at"]
                )
                df_users["extension"] = df_users["file_name"].apply(
                    lambda x: x.split(".")[-1]
                )

                # Group by day
                daily_cvs = (
                    df_users.groupby(df_users["inserted_at"].dt.to_period("D"))
                    .size()
                    .reset_index()
                )

                daily_cvs.columns = ["inserted_at", "count"]
                daily_cvs["inserted_at"] = daily_cvs["inserted_at"].astype(str)

                # Create CV uploaded over time chart
                cv_uploaded_chart = px.line(
                    daily_cvs,
                    x="inserted_at",
                    y="count",
                    title="CVs Uploaded Over Time",
                    labels={"count": "New CVs", "inserted_at": "Day"},
                    markers=True,
                )

                cv_uploaded_chart.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#2c3e50"),
                    showlegend=False,
                    yaxis=dict(rangemode="tozero"),
                )

                cv_uploaded_chart.update_traces(
                    line_color="#667eea", line_width=3
                )

                # Create CV extensions pie chart
                cv_extensions_chart = go.Figure(
                    data=[
                        go.Pie(
                            labels=df_users["extension"].value_counts().index,
                            values=df_users["extension"].value_counts().values,
                            hole=0.3,
                            marker=dict(
                                colors=px.colors.sequential.Viridis,
                                line=dict(color="#FFFFFF", width=2),
                            ),
                            textinfo="label+percent",
                            textposition="auto",
                            hovertemplate="<b>%{label}</b><br>Count: %{value}<br>Percentage: %{percent}<extra></extra>",
                        )
                    ]
                )

                cv_extensions_chart.update_layout(
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="#2c3e50"),
                    showlegend=True,
                )

                # Create CV data table
                cv_table = DashboardScreen.create_cv_data_table(cv_data)

                # Create company names table
                company_names = (
                    BACKEND_API_CLIENT.get_company_names()
                    .get("data", [])
                    .get("company_names", [])
                )

                company_names_table = dbc.Table(
                    [
                        html.Thead(
                            [
                                html.Tr(
                                    [
                                        html.Th("Company Name"),
                                    ]
                                )
                            ]
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(company_name),
                                    ]
                                )
                                for company_name in company_names
                            ]
                        ),
                    ],
                    striped=True,
                    hover=True,
                    responsive=True,
                )

                # Create job titles table
                job_titles = (
                    BACKEND_API_CLIENT.get_job_titles()
                    .get("data", [])
                    .get("job_titles", [])
                )

                job_titles_table = dbc.Table(
                    [
                        html.Thead(
                            [
                                html.Tr(
                                    [
                                        html.Th("Job Title"),
                                    ]
                                )
                            ]
                        ),
                        html.Tbody(
                            [
                                html.Tr(
                                    [
                                        html.Td(job_title),
                                    ]
                                )
                                for job_title in job_titles
                            ]
                        ),
                    ],
                    striped=True,
                    hover=True,
                    responsive=True,
                )

            else:
                empty_chart = go.Figure()
                empty_chart.add_annotation(
                    text="No user data available",
                    x=0.5,
                    y=0.5,
                    showarrow=False,
                )

                cv_uploaded_chart = empty_chart
                cv_extensions_chart = empty_chart
                cv_table = empty_chart
                company_names_table = empty_chart
                job_titles_table = empty_chart

            return (
                "CVs uploaded over time",
                cv_uploaded_chart,
                "CV extensions",
                cv_extensions_chart,
                "CV data table",
                cv_table,
                "Company names table",
                company_names_table,
                "Job titles table",
                job_titles_table,
            )
