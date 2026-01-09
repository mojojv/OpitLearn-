"""
OpitLearn Analytics Dashboard
Main Dash application initialization
"""
import dash
import dash_bootstrap_components as dbc
from flask import Flask

# Initialize Flask server
server = Flask(__name__)
server.config['SECRET_KEY'] = 'opitlearn-secret-key-change-in-production'
server.config['SESSION_TYPE'] = 'filesystem'

# Initialize Dash app
app = dash.Dash(
    __name__,
    server=server,
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        dbc.icons.FONT_AWESOME,
    ],
    suppress_callback_exceptions=True,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1"}
    ],
    title="OpitLearn Analytics"
)

# Expose server for deployment
server = app.server
