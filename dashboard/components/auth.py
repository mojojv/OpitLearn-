"""
Authentication module for OpitLearn Dashboard
Handles user login, registration, session management, and role-based access
"""
import json
import bcrypt
import re
from datetime import datetime
from pathlib import Path
from flask import session
import dash_bootstrap_components as dbc
from dash import html, dcc

# Path to users database
USERS_FILE = Path(__file__).parent.parent / "data" / "users.json"

ALLOWED_DOMAIN = "@eafit.edu.co"

def hash_password(password):
    """Hash a password using bcrypt"""
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(password, hashed):
    """Verify a password against its hash"""
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

def validate_email_domain(email):
    """Check if email belongs to allowed domain"""
    return email.lower().endswith(ALLOWED_DOMAIN)

def load_users():
    """Load users from JSON file"""
    if not USERS_FILE.exists():
        # Create default users if file doesn't exist
        # Using emails for new structure, ensuring they match domain or allow admin exception
        default_users = {
            f"admin{ALLOWED_DOMAIN}": {
                "password": hash_password("admin123"),
                "role": "admin",
                "name": "Administrador",
                "joined": datetime.now().isoformat()
            },
            f"analyst{ALLOWED_DOMAIN}": {
                "password": hash_password("analyst123"),
                "role": "analyst",
                "name": "Analista",
                "joined": datetime.now().isoformat()
            }
        }
        USERS_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(USERS_FILE, 'w') as f:
            json.dump(default_users, f, indent=2)
        return default_users
    
    with open(USERS_FILE, 'r') as f:
        return json.load(f)

def save_user(email, password, name, role="student"):
    """Register a new user"""
    if not validate_email_domain(email):
        return False, f"El correo debe ser institucional ({ALLOWED_DOMAIN})"
    
    users = load_users()
    if email in users:
        return False, "Este correo ya está registrado"
    
    users[email] = {
        "password": hash_password(password),
        "role": role,
        "name": name,
        "joined": datetime.now().isoformat()
    }
    
    with open(USERS_FILE, 'w') as f:
        json.dump(users, f, indent=2)
    
    return True, "Registro exitoso"

def authenticate_user(email, password):
    """Authenticate a user with email and password"""
    users = load_users()
    if email in users:
        if verify_password(password, users[email]['password']):
            return {
                'username': email, 
                'role': users[email]['role'],
                'name': users[email]['name']
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

def create_login_form():
    """Return the login form content"""
    return html.Div([
        html.H4("Iniciar Sesión", className="card-title text-center mb-4 text-dark"),
        
        dbc.Input(
            id="login-email",
            placeholder="Correo Institucional (@eafit.edu.co)",
            type="email",
            className="mb-3",
        ),
        dbc.Input(
            id="login-password",
            placeholder="Contraseña",
            type="password",
            className="mb-3",
        ),
        
        html.Div(id="login-alert", className="mb-3"),
        
        dbc.Button(
            "Ingresar",
            id="login-button",
            color="primary",
            className="w-100 mb-3",
            size="lg",
            style={'background': 'linear-gradient(135deg, #6366f1 0%, #a855f7 100%)', 'border': 'none', 'fontWeight': '600'}
        ),
        
        html.Div("o", className="text-center text-muted mb-3"),

        # Placeholder for Microsoft Auth
        dbc.Button(
            [html.I(className="fab fa-microsoft me-2"), "Ingresar con Microsoft"],
            id="microsoft-login-button",
            color="light",
            className="w-100 mb-3 border",
            # Enabled but will show alert
            style={'color': '#5e5e5e', 'cursor': 'pointer'}
        ),

        html.Hr(),
        html.Div([
            html.Span("¿No tienes cuenta? ", className="text-muted"),
            html.A("Regístrate aquí", href="/register", id="register-link", className="text-primary fw-bold", style={'cursor': 'pointer'})
        ], className="text-center mt-3")
    ])

def create_register_form():
    """Return the register form content"""
    return html.Div([
        html.H4("Crear Cuenta", className="card-title text-center mb-4 text-dark"),
        
        dbc.Input(
            id="reg-name",
            placeholder="Nombre Completo",
            type="text",
            className="mb-3",
        ),
        dbc.Input(
            id="reg-email",
            placeholder="Correo Institucional (@eafit.edu.co)",
            type="email",
            className="mb-3",
        ),
        dbc.Input(
            id="reg-password",
            placeholder="Contraseña",
            type="password",
            className="mb-3",
        ),
         dbc.Input(
            id="reg-password-confirm",
            placeholder="Confirmar Contraseña",
            type="password",
            className="mb-3",
        ),
        
        html.Div(id="reg-alert", className="mb-3"),
        
        dbc.Button(
            "Registrarse",
            id="reg-button",
            color="success",
            className="w-100 mb-3",
            size="lg",
            style={'border': 'none', 'fontWeight': '600'}
        ),
        
        html.Hr(),
        html.Div([
            html.Span("¿Ya tienes cuenta? ", className="text-muted"),
            html.A("Inicia Sesión", href="/login", id="login-link", className="text-primary fw-bold", style={'cursor': 'pointer'})
        ], className="text-center mt-3")
    ])

def create_login_layout():
    """Create the login/register page layout"""
    return html.Div([
        dcc.Location(id='auth-url', refresh=False),
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Div([
                        dbc.Card([
                            dbc.CardBody([
                                html.Img(
                                    src="/assets/logo.png",
                                    style={
                                        'width': '180px',
                                        'margin': '0 auto 1.5rem auto',
                                        'display': 'block'
                                    }
                                ),
                                html.H2("OpitLearn Analytics", className="text-center mb-1 text-dark font-weight-bold"),
                                html.P("Sistema de Análisis Académico", className="text-center text-muted mb-4"),
                                
                                html.Div([
                                    html.Small("Credenciales de Acceso (Piloto):", className="text-muted d-block mb-2"),
                                    dbc.Badge("admin@eafit.edu.co / admin123", color="light", text_color="dark", className="me-2 p-2 border mb-1"),
                                    dbc.Badge("analyst@eafit.edu.co / analyst123", color="light", text_color="dark", className="p-2 border"),
                                ], className="text-center mt-3"),
                                # Toggle between Login and Register
                                html.Div(id="auth-form-content")
                            ])
                        ], className="login-card")
                    ], className="login-content d-flex flex-column align-items-center")
                ], width=12, md=8, lg=6, xl=4)
            ], justify="center")
        ], fluid=True)
    ], className="login-container")
