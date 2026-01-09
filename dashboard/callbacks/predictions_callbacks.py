"""
Predictions page callbacks
"""
from dash import Input, Output, html, dash_table
import dash_bootstrap_components as dbc
from components.data_loader import load_master_data
from components.metrics import identify_at_risk_students, calculate_risk_score
import pandas as pd

def register_callbacks(app):
    """Register predictions page callbacks"""
    
    @app.callback(
        [
            Output('high-risk-count', 'children'),
            Output('medium-risk-count', 'children'),
            Output('low-risk-count', 'children'),
            Output('at-risk-table', 'children'),
            Output('recommendations-list', 'children'),
        ],
        Input('url', 'pathname')
    )
    def update_predictions(pathname):
        """Update predictions page"""
        if pathname != '/predictions':
            return "0", "0", "0", None, None
        
        df = load_master_data()
        
        if df.empty:
            empty_msg = dbc.Alert("No hay datos disponibles", color="info")
            return "0", "0", "0", empty_msg, empty_msg
        
        # Calculate risk scores
        df['risk_score'] = df.apply(calculate_risk_score, axis=1)
        
        # Categorize risk levels
        high_risk = df[df['risk_score'] >= 70]
        medium_risk = df[(df['risk_score'] >= 40) & (df['risk_score'] < 70)]
        low_risk = df[df['risk_score'] < 40]
        
        # At-risk table
        at_risk_df = high_risk.copy()
        if not at_risk_df.empty:
            display_cols = ['estudiante_id', 'programa', 'promedio_ultimo_semestre', 
                           'total_materias_reprobadas', 'risk_score']
            display_cols = [col for col in display_cols if col in at_risk_df.columns]
            
            table = dash_table.DataTable(
                data=at_risk_df[display_cols].head(50).to_dict('records'),
                columns=[{'name': col, 'id': col} for col in display_cols],
                page_size=10,
                style_table={'overflowX': 'auto'},
                style_cell={'textAlign': 'left', 'padding': '10px'},
                style_header={'backgroundColor': 'rgb(230, 230, 230)', 'fontWeight': 'bold'},
                style_data_conditional=[
                    {
                        'if': {'filter_query': '{risk_score} >= 70'},
                        'backgroundColor': '#ffebee',
                        'color': 'black'
                    }
                ],
                sort_action="native",
            )
        else:
            table = dbc.Alert("No hay estudiantes en alto riesgo", color="success")
        
        # Recommendations
        recommendations = html.Div([
            dbc.ListGroup([
                dbc.ListGroupItem([
                    html.H6("📚 Tutorías Académicas", className="mb-1"),
                    html.P(f"Asignar tutores a {len(high_risk)} estudiantes de alto riesgo", className="mb-0 small")
                ]),
                dbc.ListGroupItem([
                    html.H6("👥 Asesoría Psicológica", className="mb-1"),
                    html.P(f"Ofrecer apoyo emocional a estudiantes con múltiples reprobaciones", className="mb-0 small")
                ]),
                dbc.ListGroupItem([
                    html.H6("📊 Monitoreo Continuo", className="mb-1"),
                    html.P(f"Seguimiento semanal de {len(medium_risk)} estudiantes en riesgo moderado", className="mb-0 small")
                ]),
                dbc.ListGroupItem([
                    html.H6("💰 Apoyo Financiero", className="mb-1"),
                    html.P("Evaluar becas para estudiantes de estratos bajos con buen desempeño", className="mb-0 small")
                ]),
            ])
        ])
        
        return str(len(high_risk)), str(len(medium_risk)), str(len(low_risk)), table, recommendations
