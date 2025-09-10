"""
Authentication screen components for the Job Research Assistant frontend.
Modern, clean design matching the provided mockup.
"""

from datetime import datetime
from pathlib import Path

import dash
import dash_bootstrap_components as dbc
from components.base_components import BaseComponent
from dash import html
from dash.dependencies import Input, Output, State
from utils.auth_utils import JWTTokenAuthUtils
from utils.backend_api_client import BackendApiClient
from utils.logging import get_logger

# Initialize auth utils and postgres client
JWT_AUTH_UTILS = JWTTokenAuthUtils()
BACKEND_API_CLIENT = BackendApiClient()

file_logger = get_logger(
    "file_" + __name__,
    write_to_file=True,
    log_filepath=Path(r"logs/frontend/authentication_screen.log"),
)

stream_logger = get_logger(
    "stream_" + __name__,
)


class LogInScreen(BaseComponent):
    """
    Login screen component.

    Components/Ids:
        - login-input: login-input
        - password-input: password-input
        - login-btn: login-btn
        - show-register-btn: show-register-btn
    """

    @staticmethod
    def render():
        return html.Div(
            style={
                "minHeight": "100vh",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "20px",
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "width": "100%",
                "height": "100%",
                "position": "absolute",
            },
            children=[
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                # Title
                                html.H2(
                                    "Log in",
                                    className="text-center",
                                    style={
                                        "fontWeight": "600",
                                        "color": "#2c3e50",
                                        "marginBottom": "2.5rem",
                                        "textAlign": "center",
                                        "fontSize": "50px",
                                    },
                                ),
                                # Login Form
                                dbc.Form(
                                    [
                                        # Username Input
                                        dbc.Input(
                                            id="login-input",
                                            type="text",
                                            placeholder="Username or Email",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Password Input
                                        dbc.Input(
                                            id="password-input",
                                            type="password",
                                            placeholder="Password",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "25px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Login Button (centered)
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Log in",
                                                    id="login-btn",
                                                    style={
                                                        "backgroundColor": "#4db6ac",
                                                        "borderColor": "#4db6ac",
                                                        "borderRadius": "8px",
                                                        "padding": "12px 24px",
                                                        "fontSize": "14px",
                                                        "fontWeight": "500",
                                                        "border": "none",
                                                        "minWidth": "100px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "textAlign": "center",
                                                "marginBottom": "30px",
                                            },
                                        ),
                                    ]
                                ),
                                # Divider and Sign Up Link
                                html.Div(
                                    [
                                        html.Hr(
                                            style={
                                                "borderColor": "#e1e8ed",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                            }
                                        ),
                                        html.P(
                                            [
                                                "or, ",
                                                html.A(
                                                    "sign up",
                                                    id="show-register-btn",
                                                    href="#",
                                                    style={
                                                        "color": "#4db6ac",
                                                        "textDecoration": "none",
                                                        "fontWeight": "500",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "color": "#6c757d",
                                                "fontSize": "14px",
                                                "textAlign": "center",
                                                "margin": "0",
                                            },
                                        ),
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={"padding": "40px 35px 35px 35px"},
                        ),
                    ],
                    style={
                        "maxWidth": "700px",
                        "width": "100%",
                        "borderRadius": "12px",
                        "boxShadow": "0 10px 25px rgba(0,0,0,0.1)",
                        "border": "none",
                        "backgroundColor": "white",
                        "margin": "0 auto",
                    },
                ),
            ],
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the login screen."""

        @app.callback(
            [
                Output("session-store", "data", allow_duplicate=True),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
                Output("url", "pathname", allow_duplicate=True),
            ],
            [Input("login-btn", "n_clicks")],
            [
                State("login-input", "value"),
                State("password-input", "value"),
            ],
            prevent_initial_call=True,
        )
        def handle_login(n_clicks, login_input, password):
            if n_clicks and login_input and password:
                # Authenticate against database
                user_data = JWT_AUTH_UTILS.authenticate_user(
                    login_input, password
                )

                if user_data:
                    token = JWT_AUTH_UTILS.generate_jwt_token(
                        user_data["username"], user_data["email"]
                    )

                    session_data = {
                        "token": token,
                        "username": user_data["username"],
                        "email": user_data["email"],
                        "user_id": user_data["id"],
                        "login_time": datetime.now().isoformat(),
                    }

                    return (
                        session_data,
                        "Login successfully!",
                        True,
                        "success",
                        "/dashboard",
                    )

                else:
                    error_message = (
                        "Invalid username or password. Please try again.",
                    )

                    return (
                        dash.no_update,
                        error_message,
                        True,
                        "danger",
                        dash.no_update,
                    )

            elif not n_clicks:
                return [dash.no_update] * 5

            else:
                return (
                    dash.no_update,
                    "Please fill in all required fields.",
                    True,
                    "danger",
                    dash.no_update,
                )

        @app.callback(
            Output("url", "pathname", allow_duplicate=True),
            [Input("show-register-btn", "n_clicks")],
            prevent_initial_call=True,
        )
        def toggle_to_sign_up(n_clicks):
            if n_clicks:
                return "/sign_up"
            return dash.no_update


class SignUpScreen(BaseComponent):
    """
    Sign up screen component.

    Components/Ids:
        - reg-username-input: reg-username-input
        - reg-email-input: reg-email-input
        - reg-password-input: reg-password-input
        - reg-confirm-password-input: reg-confirm-password-input
        - register-btn: register-btn
        - show-login-btn: show-login-btn
    """

    @staticmethod
    def render():
        return html.Div(
            style={
                "minHeight": "100vh",
                "display": "flex",
                "alignItems": "center",
                "justifyContent": "center",
                "padding": "20px",
                "background": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
                "width": "100%",
                "height": "100%",
                "position": "absolute",
            },
            children=[
                dbc.Card(
                    [
                        dbc.CardBody(
                            [
                                # Title
                                html.H2(
                                    "Sign up",
                                    className="text-center",
                                    style={
                                        "fontWeight": "600",
                                        "color": "#2c3e50",
                                        "marginBottom": "2.5rem",
                                        "textAlign": "center",
                                        "fontSize": "50px",
                                    },
                                ),
                                # Registration Form
                                dbc.Form(
                                    [
                                        # Username Input
                                        dbc.Input(
                                            id="reg-username-input",
                                            type="text",
                                            placeholder="Username",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Email Input
                                        dbc.Input(
                                            id="reg-email-input",
                                            type="email",
                                            placeholder="Email",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Password Input
                                        dbc.Input(
                                            id="reg-password-input",
                                            type="password",
                                            placeholder="Password",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Confirm Password Input
                                        dbc.Input(
                                            id="reg-confirm-password-input",
                                            type="password",
                                            placeholder="Re-type password",
                                            style={
                                                "borderRadius": "8px",
                                                "border": "1px solid #e1e8ed",
                                                "padding": "14px 3px",
                                                "fontSize": "14px",
                                                "backgroundColor": "#f8f9fa",
                                                "width": "100%",
                                                "marginBottom": "25px",
                                                "textAlign": "center",
                                            },
                                        ),
                                        # Sign Up Button (centered)
                                        html.Div(
                                            [
                                                dbc.Button(
                                                    "Sign up",
                                                    id="register-btn",
                                                    style={
                                                        "backgroundColor": "#4db6ac",
                                                        "borderColor": "#4db6ac",
                                                        "borderRadius": "8px",
                                                        "padding": "12px 24px",
                                                        "fontSize": "14px",
                                                        "fontWeight": "500",
                                                        "border": "none",
                                                        "minWidth": "100px",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "textAlign": "center",
                                                "marginBottom": "30px",
                                            },
                                        ),
                                    ]
                                ),
                                # Back to Login Link
                                html.Div(
                                    [
                                        html.Hr(
                                            style={
                                                "borderColor": "#e1e8ed",
                                                "width": "100%",
                                                "marginBottom": "20px",
                                            }
                                        ),
                                        html.P(
                                            [
                                                "Already have an account? ",
                                                html.A(
                                                    "Log in",
                                                    id="show-login-btn",
                                                    href="#",
                                                    style={
                                                        "color": "#4db6ac",
                                                        "textDecoration": "none",
                                                        "fontWeight": "500",
                                                        "cursor": "pointer",
                                                    },
                                                ),
                                            ],
                                            style={
                                                "color": "#6c757d",
                                                "fontSize": "14px",
                                                "textAlign": "center",
                                                "margin": "0",
                                            },
                                        ),
                                    ],
                                    style={"textAlign": "center"},
                                ),
                            ],
                            style={"padding": "40px 35px 35px 35px"},
                        )
                    ],
                    style={
                        "maxWidth": "700px",
                        "width": "100%",
                        "borderRadius": "12px",
                        "boxShadow": "0 10px 25px rgba(0,0,0,0.1)",
                        "border": "none",
                        "backgroundColor": "white",
                        "margin": "0 auto",
                    },
                ),
            ],
        )

    @staticmethod
    def register_callbacks(app: dash.Dash):
        """Register callbacks for the sign up screen."""

        @app.callback(
            [
                Output("session-store", "data", allow_duplicate=True),
                Output("global-alert-tab", "children", allow_duplicate=True),
                Output("global-alert-tab", "is_open", allow_duplicate=True),
                Output("global-alert-tab", "color", allow_duplicate=True),
                Output("url", "pathname", allow_duplicate=True),
            ],
            [Input("register-btn", "n_clicks")],
            [
                State("reg-username-input", "value"),
                State("reg-email-input", "value"),
                State("reg-password-input", "value"),
                State("reg-confirm-password-input", "value"),
            ],
            prevent_initial_call=True,
        )
        def handle_registration(
            n_clicks,
            reg_username_input,
            reg_email_input,
            reg_password_input,
            reg_confirm_password_input,
        ):
            if (
                n_clicks
                and reg_username_input
                and reg_email_input
                and reg_password_input
                and reg_confirm_password_input
            ):
                # Check if passwords match
                if reg_password_input != reg_confirm_password_input:
                    return (
                        dash.no_update,
                        "Passwords do not match. Please try again.",
                        True,
                        "danger",
                        dash.no_update,
                    )

                # Check if username already exists
                if (
                    BACKEND_API_CLIENT.get_user_by_username(
                        reg_username_input
                    ).get("message")
                    == "User found!"
                ):
                    return (
                        dash.no_update,
                        "Username already exists. Please try again.",
                        True,
                        "danger",
                        dash.no_update,
                    )

                # Check if email already exists
                if (
                    BACKEND_API_CLIENT.get_user_by_email(reg_email_input).get(
                        "message"
                    )
                    == "User found!"
                ):
                    return (
                        dash.no_update,
                        "Email already exists. Please try again.",
                        True,
                        "danger",
                        dash.no_update,
                    )

                # Create user
                try:
                    user_data = BACKEND_API_CLIENT.create_user(
                        reg_username_input, reg_email_input, reg_password_input
                    ).get("data")

                except Exception as e:
                    error_message = f"Error creating user: {e}"
                    file_logger.error(error_message)
                    stream_logger.error(error_message)
                    return (
                        dash.no_update,
                        error_message,
                        True,
                        "danger",
                        dash.no_update,
                    )

                if user_data:
                    token = JWT_AUTH_UTILS.generate_jwt_token(
                        user_data["username"], user_data["email"]
                    )

                    session_data = {
                        "token": token,
                        "username": user_data["username"],
                        "email": user_data["email"],
                        "user_id": user_data["id"],
                        "login_time": datetime.now().isoformat(),
                    }

                    return (
                        session_data,
                        "User created successfully!",
                        True,
                        "success",
                        "/login",
                    )

            elif not n_clicks:
                return [dash.no_update] * 5

            else:
                return (
                    dash.no_update,
                    "Please fill in all required fields.",
                    True,
                    "danger",
                    dash.no_update,
                )

        @app.callback(
            Output("url", "pathname", allow_duplicate=True),
            [Input("show-login-btn", "n_clicks")],
            prevent_initial_call=True,
        )
        def toggle_to_login(n_clicks):
            if n_clicks:
                return "/login"
            return dash.no_update
