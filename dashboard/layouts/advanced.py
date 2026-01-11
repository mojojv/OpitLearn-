"""
Advanced Analytics page layout - For data analysts and ML engineers
"""
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    """Create advanced analytics page layout"""
    return dbc.Container([
        html.Div([
            html.H1("🔬 Análisis Avanzado", className="display-4 mb-2"),
            html.P("Herramientas de inteligencia artificial y minería de datos", className="lead text-muted"),
        ], className="mb-5"),
        
        # ML Metrics Summary
        dbc.Card([
            dbc.CardBody([
                html.H4("📊 Métricas del Modelo en Tiempo Real", className="mb-4"),
                dbc.Row([
                    dbc.Col(html.Div(id="ml-metric-api", className="h-100"), width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                    dbc.Col(html.Div(id="ml-metric-risk", className="h-100"), width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                    dbc.Col(html.Div(id="ml-metric-efficiency", className="h-100"), width=12, md=6, lg=3, className="mb-3 mb-lg-0"),
                    dbc.Col(html.Div(id="ml-metric-mobility", className="h-100"), width=12, md=6, lg=3),
                ])
            ])
        ], className="mb-4"),
        
        # Feature Importance Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Importancia de Variables", className="mb-3"),
                        html.P("Impacto relativo de cada variable en el rendimiento estudiantil", className="small text-muted mb-4"),
                        html.Div(id="feature-importance-chart", style={'height': '350px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🔗 Matriz de Correlación", className="mb-3"),
                        html.P("Análisis de relaciones entre indicadores académicos", className="small text-muted mb-4"),
                        html.Div(id="correlation-matrix-chart", style={'height': '350px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
        ], className="mb-4"),
        
        # Cohort Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("👥 Análisis de Cohortes", className="mb-3"),
                        html.P("Evolución longitudinal del rendimiento por semestre de ingreso", className="small text-muted mb-4"),
                        html.Div(id="cohort-analysis-chart", style={'height': '400px'})
                    ])
                ], className="h-100")
            ], width=12, className="mb-4"),
        ], className="mb-4"),
        
        # Retention and Progression
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📈 Curva de Retención", className="mb-3"),
                        html.Div(id="retention-curve-chart", style={'height': '350px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🎯 Embudo de Progresión", className="mb-3"),
                        html.Div(id="funnel-chart", style={'height': '350px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
        ], className="mb-4"),
        
        # Advanced Visualizations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("🌐 Análisis Multidimensional", className="mb-3"),
                        html.P("Exploración interactiva de clusters de estudiantes", className="small text-muted mb-4"),
                        html.Div(id="3d-scatter-chart", style={'height': '600px'})
                    ])
                ], className="h-100")
            ], width=12, className="mb-4"),
        ], className="mb-4"),
        
        # Hierarchical Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("☀️ Desglose Jerárquico", className="mb-3"),
                        html.P("Distribución por Programa → Estrato → Nivel de Riesgo", className="small text-muted mb-4"),
                        html.Div(id="sunburst-chart", style={'height': '450px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("📦 Distribución Comparativa", className="mb-3"),
                        html.P("Análisis de variabilidad por programa académico", className="small text-muted mb-4"),
                        html.Div(id="boxplot-chart", style={'height': '450px'})
                    ])
                ], className="h-100")
            ], width=12, lg=6, className="mb-4"),
        ], className="mb-4"),
        
        # Program Benchmarks Table
        dbc.Card([
            dbc.CardBody([
                html.H4("📋 Benchmarks por Programa", className="mb-3"),
                html.P("Tabla detallada de indicadores clave de rendimiento (KPIs)", className="small text-muted mb-4"),
                html.Div(id="program-benchmarks-table", className="dash-table-container")
            ])
        ], className="shadow-sm"),
        
    ], fluid=True, className="py-4")
