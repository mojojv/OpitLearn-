"""
Advanced analytics page callbacks
"""
from dash import Input, Output, html, dash_table
import dash_bootstrap_components as dbc
from components.data_loader import load_master_data
from components.ml_metrics import (
    calculate_advanced_metrics,
    calculate_feature_importance,
    perform_cohort_analysis,
    calculate_retention_curve,
    calculate_program_benchmarks
)
from components.advanced_charts import (
    create_correlation_matrix,
    create_feature_importance_chart,
    create_cohort_analysis_chart,
    create_retention_curve,
    create_3d_scatter,
    create_funnel_chart,
    create_sunburst_chart,
    create_boxplot_by_program
)
from components.charts import create_kpi_card

def register_callbacks(app):
    """Register advanced analytics page callbacks"""
    
    @app.callback(
        [
            Output('ml-metric-api', 'children'),
            Output('ml-metric-risk', 'children'),
            Output('ml-metric-efficiency', 'children'),
            Output('ml-metric-mobility', 'children'),
            Output('feature-importance-chart', 'children'),
            Output('correlation-matrix-chart', 'children'),
            Output('cohort-analysis-chart', 'children'),
            Output('retention-curve-chart', 'children'),
            Output('funnel-chart', 'children'),
            Output('3d-scatter-chart', 'children'),
            Output('sunburst-chart', 'children'),
            Output('boxplot-chart', 'children'),
            Output('program-benchmarks-table', 'children'),
        ],
        Input('url', 'pathname')
    )
    def update_advanced_analytics(pathname):
        """Update all advanced analytics components"""
        if pathname != '/advanced':
            return [None] * 13
        
        df = load_master_data()
        
        if df.empty:
            empty_msg = dbc.Alert("No hay datos disponibles", color="info")
            return [empty_msg] * 13
        
        # Calculate advanced metrics
        ml_metrics = calculate_advanced_metrics(df)
        
        # ML Metric Cards
        api_card = create_kpi_card(
            "Academic Performance Index",
            f"{ml_metrics.get('avg_api', 0):.2f}",
            "chart-line",
            "primary"
        )
        
        risk_card = create_kpi_card(
            "Alto Riesgo (%)",
            f"{ml_metrics.get('high_risk_pct', 0):.1f}%",
            "exclamation-triangle",
            "danger"
        )
        
        efficiency_card = create_kpi_card(
            "Eficiencia de Créditos",
            f"{ml_metrics.get('avg_credit_efficiency', 0):.2f}",
            "tachometer-alt",
            "success"
        )
        
        mobility_card = create_kpi_card(
            "Movilidad Social",
            f"{ml_metrics.get('social_mobility_count', 0)}",
            "arrow-up",
            "info"
        )
        
        # Feature Importance
        importance_df = calculate_feature_importance(df)
        feature_chart = create_feature_importance_chart(importance_df)
        
        # Correlation Matrix
        corr_chart = create_correlation_matrix(df)
        
        # Cohort Analysis
        cohort_df = perform_cohort_analysis(df)
        cohort_chart = create_cohort_analysis_chart(cohort_df)
        
        # Retention Curve
        retention_df = calculate_retention_curve(df)
        retention_chart = create_retention_curve(retention_df)
        
        # Funnel Chart
        funnel = create_funnel_chart(df)
        
        # 3D Scatter
        scatter_3d = create_3d_scatter(df)
        
        # Sunburst
        sunburst = create_sunburst_chart(df)
        
        # Boxplot
        boxplot = create_boxplot_by_program(df, 'promedio_ultimo_semestre')
        
        # Program Benchmarks Table
        benchmarks_df = calculate_program_benchmarks(df)
        if not benchmarks_df.empty:
            benchmarks_table = dash_table.DataTable(
                data=benchmarks_df.to_dict('records'),
                columns=[{'name': col, 'id': col} for col in benchmarks_df.columns],
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '12px', 'fontSize': '12px', 'backgroundColor': 'rgba(30, 41, 59, 0.7)', 'color': '#f8fafc', 'border': 'none'},
                style_header={'backgroundColor': '#0f172a', 'fontWeight': 'bold', 'color': '#f8fafc', 'borderBottom': '1px solid #334155'},
                page_size=10,
            )
        else:
            benchmarks_table = dbc.Alert("No hay datos suficientes", color="warning")
        
        return (
            api_card, risk_card, efficiency_card, mobility_card,
            feature_chart, corr_chart, cohort_chart, retention_chart,
            funnel, scatter_3d, sunburst, boxplot, benchmarks_table
        )
