"""
Predictions page layout - At-risk students and predictions
"""
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    """Create predictions page layout"""
    return dbc.Container([
        html.H1("🎯 Predicciones y Alertas", className="mb-4"),
        
        # Alert Summary Cards
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🔴 Alto Riesgo", className="text-danger"),
                        html.H2(id="high-risk-count", children="0"),
                        html.P("Estudiantes en riesgo crítico")
                    ])
                ], className="shadow-sm border-danger")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🟡 Riesgo Moderado", className="text-warning"),
                        html.H2(id="medium-risk-count", children="0"),
                        html.P("Requieren atención")
                    ])
                ], className="shadow-sm border-warning")
            ], width=4),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🟢 Bajo Riesgo", className="text-success"),
                        html.H2(id="low-risk-count", children="0"),
                        html.P("Desempeño satisfactorio")
                    ])
                ], className="shadow-sm border-success")
            ], width=4),
        ], className="mb-4"),
        
        # At-Risk Students Table
        dbc.Card([
            dbc.CardBody([
                html.H5("Estudiantes en Riesgo", className="mb-3"),
                html.P("Lista de estudiantes que requieren intervención académica", className="text-muted"),
                html.Div(id="at-risk-table")
            ])
        ], className="shadow-sm mb-4"),
        
        # Recommendations
        dbc.Card([
            dbc.CardBody([
                html.H5("💡 Recomendaciones de Intervención", className="mb-3"),
                html.Div(id="recommendations-list")
            ])
        ], className="shadow-sm"),
        
    ], fluid=True)
