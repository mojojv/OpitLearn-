"""
Authentication module for OpitLearn Dashboard
Handles user login, session management, and role-based access
"""
import json
import bcrypt
from pathlib import Path
from flask import session
import dash_bootstrap_components as dbc
from dash import html, dcc

# Path to users database
USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def load_users():
    """Load users from JSON file"""
    if not USERS_FILE.exists():
        # Create default users if file doesn't exist
        default_users = {
            "admin": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "Administrador"
            },
            "analyst": {
                "password": hash_password("analyst123"),
                "role": "analyst",
                "name": "Analista"
            },
            "viewer": {
                "password": hash_password("viewer123"),
                "role": "viewer",
                "name": "Observador"
            }
        }
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
        return default_users
    
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def authenticate_user(username, password):
    """Authenticate a user with username and password"""
    users = load_users()
    if username in users:
        if verify_password(password, users[username]['password']):
            return {
                'username': username,
                'role': users[username]['role'],
                'name': users[username]['name']
            }
    return None

def is_authenticated():
    """Check if user is authenticated"""
    return session.get('authenticated', False)

def get_current_user():
    """Get current logged in user"""
    if is_authenticated():
        return {
            'username': session.get('username'),
            'role': session.get('role'),
            'name': session.get('name')
        }
    return None

def login_user(user_data):
    """Log in a user and create session"""
    session['authenticated'] = True
    session['username'] = user_data['username']
    session['role'] = user_data['role']
    session['name'] = user_data['name']

def logout_user():
    """Log out current user"""
    session.clear()

def create_login_layout():
    """Create the login page layout"""
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.Img(
                        src="/assets/logo.png",
                        style={
                            'width': '200px',
                            'margin': '20px auto',
                            'display': 'block'
                        }
                    ),
                    html.H2("OpitLearn Analytics", className="text-center mb-4"),
                    html.P("Sistema de Análisis Académico", className="text-center text-muted mb-4"),
                    
                    dbc.Card([
                        dbc.CardBody([
                            html.H4("Iniciar Sesión", className="card-title text-center mb-4"),
                            
                            dbc.Input(
                                id="login-username",
                                placeholder="Usuario",
                                type="text",
                                className="mb-3"
                            ),
                            dbc.Input(
                                id="login-password",
                                placeholder="Contraseña",
                                type="password",
                                className="mb-3"
                            ),
                            
                            html.Div(id="login-alert", className="mb-3"),
                            
                            dbc.Button(
                                "Ingresar",
                                id="login-button",
                                color="primary",
                                className="w-100",
                                size="lg"
                            ),
                            
                            html.Hr(),
                            html.P([
                                html.Small([
                                    html.Strong("Usuarios de prueba:"), html.Br(),
                                    "Admin: admin / admin123", html.Br(),
                                    "Analista: analyst / analyst123", html.Br(),
                                    "Observador: viewer / viewer123"
                                ], className="text-muted")
                            ], className="text-center mt-3")
                        ])
                    ], className="shadow")
                ], style={
                    'maxWidth': '450px',
                    'margin': '50px auto',
                    'padding': '20px'
                })
            ], width=12)
        ])
    ], fluid=True, style={'minHeight': '100vh', 'backgroundColor': '#f8f9fa'})
