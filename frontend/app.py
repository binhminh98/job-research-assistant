"""
Main Plotly Dash frontend application for Job Research Assistant.
Multi-tab interface with user authentication.
"""

import dash
import dash_bootstrap_components as dbc
from components.analyze_screen import AnalyzeScreen
from components.authentication_screen import LogInScreen, SignUpScreen
from components.base_components import PageTitle
from components.dashboard_screen import DashboardScreen
from components.interview_screen import InterviewScreen
from components.upload_screen import UploadScreen
from dash import dcc, html
from dash.dependencies import Input, Output, State
from utils.auth_utils import JWTTokenAuthUtils
from utils.backend_api_client import BackendApiClient

# Initialize auth utils
JWT_AUTH_UTILS = JWTTokenAuthUtils()
BACKEND_API_CLIENT = BackendApiClient()

# App compnents
LOG_IN_SCREEN = LogInScreen()
SIGN_UP_SCREEN = SignUpScreen()
DASHBOARD_SCREEN = DashboardScreen()
PAGE_TITLE = PageTitle()
UPLOAD_SCREEN = UploadScreen()
ANALYZE_SCREEN = AnalyzeScreen()
INTERVIEW_SCREEN = InterviewScreen()

# Initialize Dash app
app = dash.Dash(
    __name__,
    title="Job Interview Preparation Assistant",
    external_stylesheets=[dbc.themes.BOOTSTRAP],
)

app.layout = dbc.Container(
    [
        # Session store and URL
        dcc.Store(id="session-store", storage_type="session"),
        dcc.Location(id="url", refresh=False),
        # Main app - Only visible when authenticated
        dbc.Navbar(
            [
                # Left side - App title with icon
                dbc.NavbarBrand(
                    id="page-title-container",
                ),
                # Top bar left - User info and settings
                dbc.Nav(
                    [
                        # User avatar and welcome
                        dbc.DropdownMenu(
                            id="settings-dropdown",
                            children=[
                                # Username
                                dbc.DropdownMenuItem(
                                    id="settings-username", disabled=True
                                ),
                                # Dropdown menu items
                                dbc.DropdownMenuItem(divider=True),
                                # dbc.DropdownMenuItem(
                                #     "Profile Settings", href="/profile"
                                # ),
                                dbc.DropdownMenuItem(
                                    "Logout", id="logout-btn", href="/login"
                                ),
                            ],
                            toggle_style={
                                "backgroundColor": "transparent",
                                "border": "none",
                                "color": "white",
                                "padding": "0px",
                            },
                            label=html.Div(
                                id="settings-dropdown-label",
                                children=[
                                    html.Img(
                                        src="assets/user.png",
                                        style={
                                            "height": "50px",
                                            "borderRadius": "50%",  # Circular image
                                            "border": "1px solid rgba(255,255,255,0.5)",
                                        },
                                    ),
                                ],
                                style={
                                    "display": "flex",
                                    "alignItems": "center",
                                },
                            ),
                            direction="down",
                            align_end=True,
                            style={"display": "none"},
                        ),
                    ],
                    className="ms-auto align-items-center mt-1 me-3",
                    id="top-bar-navbar-dropdown",
                ),
            ],
            style={
                "height": "70px",
                "zIndex": 1000,
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "borderBottom": "1px solid rgba(255,255,255,0.1)",
                "boxShadow": "0 2px 10px rgba(0,0,0,0.1)",
            },
            id="top-bar-navbar",
        ),
        # Main content area
        html.Div(
            id="main-content",
        ),
        # Global alert
        dbc.Alert(
            id="global-alert-tab",
            is_open=False,
            dismissable=True,
            color="danger",
            style={
                "position": "fixed",
                "top": "20px",
                "right": "20px",
                "width": "300px",
                "zIndex": 1050,
                "boxShadow": "0 4px 12px rgba(0,0,0,0.15)",
            },
        ),
    ],
    fluid=True,
    style={"padding": "0", "margin": "0"},
)


def render_main_app(pathname="/dashboard"):
    """Render the main multi-tab application interface."""
    url_to_tab = {
        "/dashboard": DASHBOARD_SCREEN.render(),
        "/upload": UPLOAD_SCREEN.render(),
        "/analyze": ANALYZE_SCREEN.render(),
        "/interview": INTERVIEW_SCREEN.render(),
    }

    tab_content = url_to_tab.get(pathname, DASHBOARD_SCREEN.render())

    return dbc.Container(
        [
            dbc.Row(
                [
                    # Left Sidebar Navigation - Modern Design
                    dbc.Col(
                        [
                            html.Div(
                                [
                                    dbc.Nav(
                                        [
                                            dbc.NavLink(
                                                [
                                                    html.Img(
                                                        src="assets/dashboard.svg",
                                                        style={
                                                            "height": "50px",
                                                        },
                                                    ),
                                                    html.Span("Home"),
                                                ],
                                                href="/dashboard",
                                                id="nav-dashboard",
                                                className="nav-item-custom",
                                                active="exact",
                                            ),
                                            dbc.NavLink(
                                                [
                                                    html.Img(
                                                        src="assets/upload.svg",
                                                        style={
                                                            "height": "50px",
                                                        },
                                                    ),
                                                    html.Span("Your CVs"),
                                                ],
                                                href="/upload",
                                                id="nav-upload",
                                                className="nav-item-custom",
                                                active="exact",
                                            ),
                                            dbc.NavLink(
                                                [
                                                    html.Img(
                                                        src="assets/analyze.svg",
                                                        style={
                                                            "height": "50px",
                                                        },
                                                    ),
                                                    html.Span("CV Analysis"),
                                                ],
                                                href="/analyze",
                                                id="nav-analyze",
                                                className="nav-item-custom",
                                                active="exact",
                                            ),
                                            dbc.NavLink(
                                                [
                                                    html.Img(
                                                        src="assets/interview.svg",
                                                        style={
                                                            "height": "50px",
                                                        },
                                                    ),
                                                    html.Span(
                                                        "Interview Preparation"
                                                    ),
                                                ],
                                                href="/interview",
                                                id="nav-interview",
                                                className="nav-item-custom",
                                                active="exact",
                                            ),
                                        ],
                                        vertical=True,
                                        className="nav-sidebar",
                                    ),
                                ],
                                className="sidebar-container",
                            ),
                        ],
                        width=1,
                        className="sidebar-col",
                    ),
                    # Main Content Area
                    dbc.Col(
                        [
                            html.Div(id="tab-content", children=tab_content),
                        ],
                        width=11,
                        className="main-content-col",
                    ),
                ],
                className="main-row",
            ),
        ],
        fluid=True,
        className="main-container",
    )


# Main content update callback
@app.callback(
    [
        Output("main-content", "children"),
        Output("settings-dropdown", "style"),
        Output("settings-username", "children"),
        Output("session-store", "data", allow_duplicate=True),
        Output("url", "pathname", allow_duplicate=True),
    ],
    [
        Input("url", "pathname"),
    ],
    [
        State("session-store", "data"),
    ],
    prevent_initial_call=True,
)
def display_components(pathname, session_data):
    if pathname in ["/login", "/"]:
        return (
            LOG_IN_SCREEN.render(),
            {"display": "none"},
            None,
            {},
            dash.no_update,
        )
    elif pathname in ["/sign_up", "/"]:
        return (
            SIGN_UP_SCREEN.render(),
            {"display": "none"},
            None,
            {},
            dash.no_update,
        )
    else:
        if not session_data or not JWT_AUTH_UTILS.verify_jwt_token(
            session_data.get("token")
        ):
            return (
                LOG_IN_SCREEN.render(),
                {"display": "none"},
                None,
                {},
                "/login",
            )

        # Verify user still exists in database
        username = session_data.get("username")
        user_data = BACKEND_API_CLIENT.get_user_by_username(username)

        if not user_data:
            # User no longer exists, logout
            return (
                LOG_IN_SCREEN.render(),
                {"display": "none"},
                None,
                {},
                "/login",
            )

        # Main application
        return (
            render_main_app(pathname),
            {"display": "block"},
            username,
            session_data,
            pathname,
        )


# Logout callback
@app.callback(
    Output("session-store", "data", allow_duplicate=True),
    Output("url", "pathname", allow_duplicate=True),
    [Input("logout-btn", "n_clicks")],
    prevent_initial_call=True,
)
def handle_logout(n_clicks):
    if n_clicks:
        return {}, "/login"
    return dash.no_update, dash.no_update


# Main tabs update callbacks
@app.callback(
    Output("main-tabs", "active_tab"),
    [Input("url", "pathname")],
    prevent_initial_call=True,
)
def update_main_tabs(pathname):
    return pathname.split("/")[-1]


@app.callback(
    Output("url", "pathname", allow_duplicate=True),
    [Input("main-tabs", "active_tab")],
    prevent_initial_call=True,
)
def update_url(active_tab):
    return "/" + active_tab


# Register callbacks for the screens
PAGE_TITLE.register_callbacks(app)
LOG_IN_SCREEN.register_callbacks(app)
SIGN_UP_SCREEN.register_callbacks(app)
DASHBOARD_SCREEN.register_callbacks(app)
UPLOAD_SCREEN.register_callbacks(app)
ANALYZE_SCREEN.register_callbacks(app)
INTERVIEW_SCREEN.register_callbacks(app)

# Expose the Flask server for Gunicorn
server = app.server

if __name__ == "__main__":
    app.run(debug=False, host="0.0.0.0", port=8050)
