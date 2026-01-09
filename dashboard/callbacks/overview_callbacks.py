"""
Overview page callbacks
"""
from dash import Input, Output, html
import dash_bootstrap_components as dbc
from components.data_loader import load_master_data
from components.metrics import calculate_kpis
from components.charts import (
    create_kpi_card,
    create_program_distribution_chart,
    create_gpa_distribution_chart,
    create_estrato_distribution_pie
)

def register_callbacks(app):
    """Register overview page callbacks"""
    
    @app.callback(
        [
            Output('kpi-total-students', 'children'),
            Output('kpi-avg-gpa', 'children'),
            Output('kpi-retention', 'children'),
            Output('kpi-at-risk', 'children'),
            Output('chart-program-distribution', 'children'),
            Output('chart-gpa-distribution', 'children'),
            Output('chart-estrato-distribution', 'children'),
            Output('quick-stats', 'children'),
        ],
        Input('overview-interval', 'n_intervals')
    )
    def update_overview(n):
        """Update all overview components"""
        df = load_master_data()
        kpis = calculate_kpis(df)
        
        # KPI Cards
        kpi_students = create_kpi_card(
            "Total Estudiantes",
            f"{kpis['total_students']:,}",
            "users",
            "primary"
        )
        
        kpi_gpa = create_kpi_card(
            "Promedio General",
            f"{kpis['avg_gpa']:.2f}",
            "chart-line",
            "success"
        )
        
        kpi_retention = create_kpi_card(
            "Tasa de Retención",
            f"{kpis['retention_rate']:.1f}%",
            "graduation-cap",
            "info"
        )
        
        kpi_risk = create_kpi_card(
            "Estudiantes en Riesgo",
            f"{kpis['at_risk_count']}",
            "exclamation-triangle",
            "danger"
        )
        
        # Charts
        chart_programs = create_program_distribution_chart(df)
        chart_gpa = create_gpa_distribution_chart(df)
        chart_estrato = create_estrato_distribution_pie(df)
        
        # Quick stats
        stats = html.Div([
            html.P([html.Strong("Total de Registros: "), f"{len(df):,}"]),
            html.P([html.Strong("Programas Activos: "), f"{df['programa'].nunique() if not df.empty else 0}"]),
            html.P([html.Strong("Créditos Promedio: "), 
                   f"{df['total_creditos_aprobados'].mean():.1f}" if not df.empty and 'total_creditos_aprobados' in df.columns else "N/A"]),
        ])
        
        return kpi_students, kpi_gpa, kpi_retention, kpi_risk, chart_programs, chart_gpa, chart_estrato, stats
