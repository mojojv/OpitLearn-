"""
Predictions page layout - At-risk students and predictions
"""
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    """Create predictions page layout"""
    return dbc.Container([
        html.Div([
            html.H1("🎯 Predicciones y Alertas", className="display-4 mb-2"),
            html.P("Monitor de riesgo académico en tiempo real", className="lead text-muted"),
        ], className="mb-5"),
        
        # Alert Summary Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H5("🔴 Alto Riesgo", className="mb-0"),
                            html.Div(className="display-6", children="⚠️")
                        ], className="d-flex justify-content-between align-items-center mb-3"),
                        html.H2(id="high-risk-count", children="0", className="mb-2"),
                        html.P("Estudiantes en riesgo crítico", className="mb-0")
                    ])
                ], className="h-100 border-danger card-hover")
            ], width=12, md=4, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H5("🟡 Riesgo Moderado", className="mb-0"),
                            html.Div(className="display-6", children="⚡")
                        ], className="d-flex justify-content-between align-items-center mb-3"),
                        html.H2(id="medium-risk-count", children="0", className="mb-2"),
                        html.P("Requieren atención preventiva", className="mb-0")
                    ])
                ], className="h-100 border-warning card-hover")
            ], width=12, md=4, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H5("🟢 Bajo Riesgo", className="mb-0"),
                            html.Div(className="display-6", children="✨")
                        ], className="d-flex justify-content-between align-items-center mb-3"),
                        html.H2(id="low-risk-count", children="0", className="mb-2"),
                        html.P("Desempeño satisfactorio", className="mb-0")
                    ])
                ], className="h-100 border-success card-hover")
            ], width=12, md=4, className="mb-4"),
        ], className="mb-4"),
        
        # Main Content Row
        dbc.Row([
            # At-Risk Table
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div([
                            html.H4("📋 Estudiantes Prioritarios", className="mb-0"),
                            dbc.Button("Exportar Reporte", color="primary", size="sm", outline=True)
                        ], className="d-flex justify-content-between align-items-center mb-4"),
                        html.Div(id="at-risk-table", className="dash-table-container")
                    ])
                ], className="h-100")
            ], width=12, lg=8, className="mb-4"),

            # Recommendations
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("💡 Recomendaciones IA", className="mb-4"),
                        html.Div(id="recommendations-list", className="recommendations-container")
                    ])
                ], className="h-100")
            ], width=12, lg=4, className="mb-4"),
        ]),
        
    ], fluid=True, className="py-4")
