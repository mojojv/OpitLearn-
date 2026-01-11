import dash
from dash import Input, Output, State, callback_context, html, dcc
import dash_bootstrap_components as dbc
from components.auth import create_login_form, create_register_form, authenticate_user, login_user, save_user

def register_callbacks(app):
    """Register authentication callbacks"""

    # Callback to toggle between Login and Register forms
    @app.callback(
        Output("auth-form-content", "children"),
        [Input("url", "pathname"), Input("auth-url", "pathname")]
    )
    def render_auth_form(pathname, auth_path):
        ctx = callback_context
        # Use auth-url trigger if available (internal link click), else url
        path = pathname
        if ctx.triggered and "auth-url" in ctx.triggered[0]['prop_id']:
             path = auth_path
             
        if path == "/register":
            return create_register_form()
        else:
            return create_login_form()

    # Callback for Registration
    @app.callback(
        Output("reg-alert", "children"),
        Input("reg-button", "n_clicks"),
        [
            State("reg-name", "value"),
            State("reg-email", "value"),
            State("reg-password", "value"),
            State("reg-password-confirm", "value")
        ],
        prevent_initial_call=True
    )
    def register_new_user(n_clicks, name, email, password, confirm):
        if not n_clicks:
            return None
        
        if not all([name, email, password, confirm]):
            return dbc.Alert("Todos los campos son obligatorios", color="warning")
        
        if password != confirm:
            return dbc.Alert("Las contraseñas no coinciden", color="danger")
        
        success, message = save_user(email, password, name)
        
        if success:
            return html.Div([
                dbc.Alert(message, color="success"),
                html.P("Redirigiendo al inicio de sesión...", className="text-muted small"),
                dcc.Location(id='redirect-login', href='/login') # Auto redirect
            ])
        else:
            return dbc.Alert(message, color="danger")

    # Callback for Login (Updated)
    @app.callback(
        [Output("url", "pathname"), Output("login-alert", "children")],
        Input("login-button", "n_clicks"),
        [State("login-email", "value"), State("login-password", "value")],
        prevent_initial_call=True
    )
    def login(n_clicks, email, password):
        if not n_clicks:
            return dash.no_update, None
        
        email_alert = None
        if not email or not password:
             email_alert = dbc.Alert("Ingrese correo y contraseña", color="warning")
             return dash.no_update, email_alert
        
        user = authenticate_user(email, password)
        
        if user:
            login_user(user)
            return "/overview", None
        else:
            return dash.no_update, dbc.Alert("Usuario o contraseña incorrectos", color="danger")

    # Callback for Microsoft Login (Simulation/Info)
    @app.callback(
        Output("login-alert", "children", allow_duplicate=True),
        Input("microsoft-login-button", "n_clicks"),
        prevent_initial_call=True
    )
    def microsoft_login_info(n_clicks):
        if not n_clicks:
            return None
        return dbc.Alert([
            html.H5("Configuración Requerida", className="alert-heading"),
            html.P("El inicio de sesión con Microsoft requiere credenciales de Azure AD (Client ID, Tenant ID)."),
            html.Hr(),
            html.P("Por ahora, use el correo institucional y contraseña.", className="mb-0")
        ], color="info")
