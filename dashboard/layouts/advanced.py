"""
Advanced Analytics page layout - For data analysts and ML engineers
"""
import dash_bootstrap_components as dbc
from dash import html, dcc

def create_layout():
    """Create advanced analytics page layout"""
    return dbc.Container([
        html.H1("🔬 Análisis Avanzado", className="mb-4"),
        html.P("Herramientas avanzadas de análisis para científicos de datos y analistas", className="text-muted mb-4"),
        
        # ML Metrics Summary
        dbc.Card([
            dbc.CardBody([
                html.H5("📊 Métricas ML Avanzadas", className="mb-3"),
                dbc.Row([
                    dbc.Col(html.Div(id="ml-metric-api"), width=3),
                    dbc.Col(html.Div(id="ml-metric-risk"), width=3),
                    dbc.Col(html.Div(id="ml-metric-efficiency"), width=3),
                    dbc.Col(html.Div(id="ml-metric-mobility"), width=3),
                ])
            ])
        ], className="shadow-sm mb-4"),
        
        # Feature Importance Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🎯 Importancia de Variables", className="mb-3"),
                        html.P("Correlación de features con rendimiento académico", className="small text-muted"),
                        html.Div(id="feature-importance-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🔗 Matriz de Correlación", className="mb-3"),
                        html.P("Relaciones entre variables numéricas", className="small text-muted"),
                        html.Div(id="correlation-matrix-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ], className="mb-4"),
        
        # Cohort Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("👥 Análisis de Cohortes", className="mb-3"),
                        html.P("Evolución de métricas por semestre", className="small text-muted"),
                        html.Div(id="cohort-analysis-chart")
                    ])
                ], className="shadow-sm")
            ], width=12),
        ], className="mb-4"),
        
        # Retention and Progression
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📈 Curva de Retención", className="mb-3"),
                        html.Div(id="retention-curve-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🎯 Embudo de Progresión", className="mb-3"),
                        html.Div(id="funnel-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ], className="mb-4"),
        
        # Advanced Visualizations
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("🌐 Análisis 3D Multivariado", className="mb-3"),
                        html.P("Exploración interactiva de relaciones complejas", className="small text-muted"),
                        html.Div(id="3d-scatter-chart")
                    ])
                ], className="shadow-sm")
            ], width=12),
        ], className="mb-4"),
        
        # Hierarchical Analysis
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("☀️ Análisis Jerárquico", className="mb-3"),
                        html.P("Distribución por Programa → Estrato → Riesgo", className="small text-muted"),
                        html.Div(id="sunburst-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("📦 Distribución por Programa", className="mb-3"),
                        html.P("Box plots comparativos", className="small text-muted"),
                        html.Div(id="boxplot-chart")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ], className="mb-4"),
        
        # Program Benchmarks Table
        dbc.Card([
            dbc.CardBody([
                html.H5("📋 Benchmarks por Programa", className="mb-3"),
                html.P("Estadísticas comparativas detalladas", className="small text-muted"),
                html.Div(id="program-benchmarks-table")
            ])
        ], className="shadow-sm"),
        
    ], fluid=True)
