"""
Settings page callbacks
"""
from dash import Input, Output, html
import dash_bootstrap_components as dbc
from components.data_loader import load_master_data, refresh_data
from datetime import datetime
import pandas as pd

def register_callbacks(app):
    """Register settings page callbacks"""
    
    @app.callback(
        Output('refresh-status', 'children'),
        Input('refresh-data-button', 'n_clicks'),
        prevent_initial_call=True
    )
    def refresh_data_callback(n_clicks):
        """Refresh data cache"""
        try:
            df = refresh_data()
            return dbc.Alert(f"Datos actualizados exitosamente. {len(df)} registros cargados.", color="success", duration=4000)
        except Exception as e:
            return dbc.Alert(f"Error al actualizar datos: {str(e)}", color="danger", duration=4000)
    
    @app.callback(
        Output('system-info', 'children'),
        Input('url', 'pathname')
    )
    def display_system_info(pathname):
        """Display system information"""
        if pathname != '/settings':
            return None
        
        df = load_master_data()
        
        info = html.Div([
            html.P([html.Strong("Versión del Sistema: "), "1.0.0"]),
            html.P([html.Strong("Última Actualización: "), datetime.now().strftime("%Y-%m-%d %H:%M:%S")]),
            html.P([html.Strong("Total de Registros: "), f"{len(df):,}"]),
            html.P([html.Strong("Tamaño de Datos: "), f"{df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB" if not df.empty else "0 MB"]),
            html.P([html.Strong("Framework: "), "Dash (Plotly)"]),
            html.P([html.Strong("Backend: "), "Flask + Pandas"]),
        ])
        
        return info
    
    @app.callback(
        Output('user-management-section', 'children'),
        Input('url', 'pathname')
    )
    def display_user_management(pathname):
        """Display user management section"""
        if pathname != '/settings':
            return None
        
        # For now, just show a placeholder
        return dbc.Alert([
            html.H6("Gestión de Usuarios"),
            html.P("Funcionalidad en desarrollo. Próximamente podrás:"),
            html.Ul([
                html.Li("Crear nuevos usuarios"),
                html.Li("Modificar roles y permisos"),
                html.Li("Desactivar cuentas"),
                html.Li("Cambiar contraseñas"),
            ])
        ], color="info")
