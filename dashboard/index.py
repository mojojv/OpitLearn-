"""
OpitLearn Analytics Dashboard - Main Entry Point
URL routing and page rendering
"""
from dash import dcc, html, Input, Output
from flask import session
from app import app, server
from components.auth import is_authenticated, get_current_user, create_login_layout
from components.navbar import create_navbar
from layouts import overview, analytics, predictions, settings, advanced

# Import callbacks
from callbacks import (
    auth_callbacks,
    overview_callbacks,
    analytics_callbacks,
    predictions_callbacks,
    settings_callbacks,
    advanced_callbacks
)

# Register all callbacks
auth_callbacks.register_callbacks(app)
overview_callbacks.register_callbacks(app)
analytics_callbacks.register_callbacks(app)
predictions_callbacks.register_callbacks(app)
settings_callbacks.register_callbacks(app)
advanced_callbacks.register_callbacks(app)

# Main app layout
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    """Route to appropriate page based on URL"""
    
    # Check authentication
    if not is_authenticated():
        if pathname != '/login':
            return dcc.Location(pathname='/login', id='redirect')
        return create_login_layout()
    
    # Get current user
    current_user = get_current_user()
    
    # Create navbar
    navbar = create_navbar(current_user)
    
    # Route to pages
    if pathname == '/overview' or pathname == '/':
        return html.Div([navbar, overview.create_layout()])
    
    elif pathname == '/analytics':
        return html.Div([navbar, analytics.create_layout()])
    
    elif pathname == '/advanced':
        return html.Div([navbar, advanced.create_layout()])
    
    elif pathname == '/predictions':
        return html.Div([navbar, predictions.create_layout()])
    
    elif pathname == '/settings':
        # Check if user is admin
        if current_user['role'] != 'admin':
            return html.Div([
                navbar,
                html.Div([
                    html.H3("Acceso Denegado"),
                    html.P("Solo los administradores pueden acceder a esta página."),
                ], className="container mt-5")
            ])
        return html.Div([navbar, settings.create_layout()])
    
    elif pathname == '/login':
        return dcc.Location(pathname='/overview', id='redirect-to-overview')
    
    else:
        return html.Div([
            navbar,
            html.Div([
                html.H3("404: Página no encontrada"),
                html.P("La página que buscas no existe."),
            ], className="container mt-5")
        ])

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=8051)
