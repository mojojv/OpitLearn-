"""
Overview page layout - Executive dashboard with KPIs
"""
import dash_bootstrap_components as dbc
from dash import html, dcc
from components.charts import create_kpi_card

def create_layout():
    """Create overview page layout"""
    return dbc.Container([
        html.H1("📊 Dashboard General", className="mb-4"),
        
        # KPI Cards Row
        dbc.Row([
            dbc.Col(html.Div(id="kpi-total-students"), width=3),
            dbc.Col(html.Div(id="kpi-avg-gpa"), width=3),
            dbc.Col(html.Div(id="kpi-retention"), width=3),
            dbc.Col(html.Div(id="kpi-at-risk"), width=3),
        ], className="mb-4"),
        
        # Charts Row 1
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="chart-program-distribution")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="chart-gpa-distribution")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ], className="mb-4"),
        
        # Charts Row 2
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.Div(id="chart-estrato-distribution")
                    ])
                ], className="shadow-sm")
            ], width=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Estadísticas Rápidas"),
                        html.Div(id="quick-stats")
                    ])
                ], className="shadow-sm")
            ], width=6),
        ]),
        
        # Hidden div for triggering updates
        dcc.Interval(id='overview-interval', interval=60000, n_intervals=0)
        
    ], fluid=True)
