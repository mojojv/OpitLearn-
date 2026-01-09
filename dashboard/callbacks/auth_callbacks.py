"""
Authentication callbacks for login/logout functionality
"""
from dash import Input, Output, State, html, dcc, no_update
from flask import session
import dash_bootstrap_components as dbc
from components.auth import authenticate_user, login_user, logout_user

def register_callbacks(app):
    """Register authentication callbacks"""
    
    @app.callback(
        [
            Output('login-alert', 'children'),
            Output('url', 'pathname'),
        ],
        Input('login-button', 'n_clicks'),
        [
            State('login-username', 'value'),
            State('login-password', 'value'),
        ],
        prevent_initial_call=True
    )
    def handle_login(n_clicks, username, password):
        """Handle login attempt"""
        if not username or not password:
            alert = dbc.Alert("Por favor ingrese usuario y contraseña", color="warning")
            return alert, no_update
        
        user_data = authenticate_user(username, password)
        if user_data:
            login_user(user_data)
            return None, '/overview'
        else:
            alert = dbc.Alert("Usuario o contraseña incorrectos", color="danger")
            return alert, no_update
    
    @app.callback(
        Output('url', 'pathname', allow_duplicate=True),
        Input('logout-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def handle_logout(n_clicks):
        """Handle logout"""
        logout_user()
        return '/login'
