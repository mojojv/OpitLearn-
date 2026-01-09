"""
Navigation bar component for OpitLearn Dashboard
"""
import dash_bootstrap_components as dbc
from dash import html

def create_navbar(current_user=None):
    """Create navigation bar with user info"""
    if not current_user:
        return None
    
    return dbc.Navbar(
        dbc.Container([
            dbc.Row([
                dbc.Col([
                    html.Img(src="/assets/logo.png", height="40px"),
                    dbc.NavbarBrand("OpitLearn Analytics", className="ms-2"),
                ], width="auto"),
            ], align="center", className="g-0"),
            
            dbc.NavbarToggler(id="navbar-toggler"),
            
            dbc.Collapse(
                dbc.Nav([
                    dbc.NavItem(dbc.NavLink("📊 Overview", href="/overview", active="exact")),
                    dbc.NavItem(dbc.NavLink("📈 Analytics", href="/analytics", active="exact")),
                    dbc.NavItem(dbc.NavLink("🔬 Análisis Avanzado", href="/advanced", active="exact")),
                    dbc.NavItem(dbc.NavLink("🎯 Predicciones", href="/predictions", active="exact")),
                    dbc.NavItem(dbc.NavLink("⚙️ Configuración", href="/settings", active="exact")) if current_user['role'] == 'admin' else None,
                    
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem(f"👤 {current_user['name']}", header=True),
                            dbc.DropdownMenuItem(f"Rol: {current_user['role'].title()}", disabled=True),
                            dbc.DropdownMenuItem(divider=True),
                            dbc.DropdownMenuItem("🚪 Cerrar Sesión", id="logout-button"),
                        ],
                        nav=True,
                        in_navbar=True,
                        label=current_user['name'],
                        className="ms-auto"
                    ),
                ], className="ms-auto", navbar=True),
                id="navbar-collapse",
                navbar=True,
            ),
        ], fluid=True),
        color="dark",
        dark=True,
        className="mb-4"
    )
