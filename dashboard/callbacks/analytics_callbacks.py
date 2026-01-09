"""
Analytics page callbacks
"""
from dash import Input, Output, State, dash_table, html
import dash_bootstrap_components as dbc
from components.data_loader import load_master_data, get_filtered_data, get_unique_programs, get_unique_estratos
from components.charts import (
    create_credits_vs_gpa_scatter,
    create_program_distribution_chart,
    create_performance_heatmap
)
import pandas as pd

def register_callbacks(app):
    """Register analytics page callbacks"""
    
    @app.callback(
        [
            Output('filter-programa', 'options'),
            Output('filter-estrato', 'options'),
        ],
        Input('url', 'pathname')
    )
    def populate_filters(pathname):
        """Populate filter dropdowns"""
        if pathname != '/analytics':
            return [], []
        
        programs = get_unique_programs()
        estratos = get_unique_estratos()
        
        program_options = [{'label': 'Todos', 'value': 'Todos'}] + [{'label': p, 'value': p} for p in programs]
        estrato_options = [{'label': 'Todos', 'value': 'Todos'}] + [{'label': str(e), 'value': str(e)} for e in estratos]
        
        return program_options, estrato_options
    
    @app.callback(
        [
            Output('analytics-chart-1', 'children'),
            Output('analytics-chart-2', 'children'),
            Output('analytics-heatmap', 'children'),
            Output('data-table-container', 'children'),
        ],
        [
            Input('apply-filters', 'n_clicks'),
            Input('url', 'pathname')
        ],
        [
            State('filter-programa', 'value'),
            State('filter-estrato', 'value'),
        ]
    )
    def update_analytics(n_clicks, pathname, programa, estrato):
        """Update analytics based on filters"""
        if pathname != '/analytics':
            return None, None, None, None
        
        df = get_filtered_data(programa, estrato)
        
        if df.empty:
            empty_msg = dbc.Alert("No hay datos disponibles con los filtros seleccionados", color="info")
            return empty_msg, empty_msg, empty_msg, empty_msg
        
        # Charts
        chart1 = create_credits_vs_gpa_scatter(df)
        chart2 = create_program_distribution_chart(df)
        heatmap = create_performance_heatmap(df)
        
        # Data table
        display_cols = ['estudiante_id', 'programa', 'promedio_ultimo_semestre', 
                       'total_creditos_aprobados', 'total_materias_reprobadas']
        display_cols = [col for col in display_cols if col in df.columns]
        
        table = dash_table.DataTable(
            data=df[display_cols].head(100).to_dict('records'),
            columns=[{'name': col, 'id': col} for col in display_cols],
            page_size=10,
            style_table={'overflowX': 'auto'},
            style_cell={'textAlign': 'left', 'padding': '10px'},
            style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
            filter_action="native",
            sort_action="native",
        )
        
        return chart1, chart2, heatmap, table
    
    @app.callback(
        Output('filter-programa', 'value'),
        Output('filter-estrato', 'value'),
        Input('clear-filters', 'n_clicks'),
        prevent_initial_call=True
    )
    def clear_filters(n_clicks):
        """Clear all filters"""
        return 'Todos', 'Todos'
    
    @app.callback(
        Output('download-csv', 'data'),
        Input('export-csv', 'n_clicks'),
        State('filter-programa', 'value'),
        State('filter-estrato', 'value'),
        prevent_initial_call=True
    )
    def export_csv(n_clicks, programa, estrato):
        """Export filtered data to CSV"""
        df = get_filtered_data(programa, estrato)
        return dict(content=df.to_csv(index=False), filename="opitlearn_data.csv")
    
    @app.callback(
        Output('download-excel', 'data'),
        Input('export-excel', 'n_clicks'),
        State('filter-programa', 'value'),
        State('filter-estrato', 'value'),
        prevent_initial_call=True
    )
    def export_excel(n_clicks, programa, estrato):
        """Export filtered data to Excel"""
        df = get_filtered_data(programa, estrato)
        return dict(content=df.to_excel(index=False, engine='openpyxl'), filename="opitlearn_data.xlsx")
