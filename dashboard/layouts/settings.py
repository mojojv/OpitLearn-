"""
Settings page layout - Admin configuration
"""
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    """Create settings page layout"""
    return dbc.Container([
        html.H1("⚙️ Configuración", className="mb-4"),
        
        # Data Management
        dbc.Card([
            dbc.CardBody([
                html.H5("🔄 Gestión de Datos", className="mb-3"),
                html.P("Actualizar y refrescar los datos del sistema"),
                dbc.Button(
                    "Refrescar Datos",
                    id="refresh-data-button",
                    color="primary",
                    className="me-2"
                ),
                dbc.Spinner(html.Div(id="refresh-status"), size="sm")
            ])
        ], className="shadow-sm mb-4"),
        
        # System Information
        dbc.Card([
            dbc.CardBody([
                html.H5("ℹ️ Información del Sistema", className="mb-3"),
                html.Div(id="system-info")
            ])
        ], className="shadow-sm mb-4"),
        
        # User Management (Admin only)
        dbc.Card([
            dbc.CardBody([
                html.H5("👥 Gestión de Usuarios", className="mb-3"),
                html.P("Administrar usuarios del sistema (Solo administradores)", className="text-muted"),
                html.Div(id="user-management-section")
            ])
        ], className="shadow-sm"),
        
    ], fluid=True)
