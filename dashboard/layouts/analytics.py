"""
Analytics page layout - Detailed analysis with filters
"""
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

def create_layout():
    """Create analytics page layout"""
    return dbc.Container([
        html.H1("📈 Análisis Detallado", className="mb-4"),
        
        # Filters Row
        dbc.Card([
            dbc.CardBody([
                html.H5("Filtros", className="mb-3"),
                dbc.Row([
                    dbc.Col([
                        html.Label("Programa:"),
                        dcc.Dropdown(
                            id='filter-programa',
                            placeholder="Seleccionar programa...",
                            multi=False
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label("Estrato:"),
                        dcc.Dropdown(
                            id='filter-estrato',
                            placeholder="Seleccionar estrato...",
                            multi=False
                        )
                    ], width=4),
                    dbc.Col([
                        html.Label("Acciones:"),
                        html.Br(),
                        dbc.Button("Aplicar Filtros", id="apply-filters", color="primary", className="me-2"),
                        dbc.Button("Limpiar", id="clear-filters", color="secondary")
                    ], width=4),
                ])
            ])
        ], className="mb-4 shadow-sm"),
        
        # Charts Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="analytics-chart-1")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="analytics-chart-2")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ], className="mb-4"),
        
        # Heatmap Row
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="analytics-heatmap")
                    ])
                ], className="shadow-sm")
            ], width=12),
        ], className="mb-4"),
        
        # Data Table
        dbc.Card([
            dbc.CardBody([
                html.H5("Tabla de Datos", className="mb-3"),
                html.Div([
                    dbc.Button("📥 Exportar CSV", id="export-csv", color="success", size="sm", className="me-2"),
                    dbc.Button("📊 Exportar Excel", id="export-excel", color="info", size="sm"),
                ], className="mb-3"),
                html.Div(id="data-table-container")
            ])
        ], className="shadow-sm"),
        
        # Download components
        dcc.Download(id="download-csv"),
        dcc.Download(id="download-excel"),
        
    ], fluid=True)
