"""
Chart generation utilities using Plotly
"""
import plotly.express as px
import plotly.graph_objects as go
from dash import dcc
import pandas as pd

def create_program_distribution_chart(df):
    """Create bar chart of student distribution by program"""
    if df.empty or 'programa' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    program_counts = df['programa'].value_counts().reset_index()
    program_counts.columns = ['Programa', 'Estudiantes']
    
    fig = px.bar(
        program_counts,
        x='Programa',
        y='Estudiantes',
        title='Distribución de Estudiantes por Programa',
        color='Estudiantes',
        color_continuous_scale='Blues'
    )
    
    fig.update_layout(
        template='plotly_white',
        hovermode='x unified',
        showlegend=False
    )
    
    return dcc.Graph(figure=fig)

def create_gpa_distribution_chart(df):
    """Create histogram of GPA distribution"""
    if df.empty or 'promedio_ultimo_semestre' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    gpa_data = df['promedio_ultimo_semestre'].dropna()
    
    fig = px.histogram(
        gpa_data,
        nbins=20,
        title='Distribución de Promedios (GPA)',
        labels={'value': 'Promedio', 'count': 'Frecuencia'},
        color_discrete_sequence=['#1f77b4']
    )
    
    # Add mean line
    mean_gpa = gpa_data.mean()
    fig.add_vline(
        x=mean_gpa,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Media: {mean_gpa:.2f}",
        annotation_position="top"
    )
    
    fig.update_layout(
        template='plotly_white',
        showlegend=False
    )
    
    return dcc.Graph(figure=fig)

def create_credits_vs_gpa_scatter(df):
    """Create scatter plot of credits vs GPA"""
    if df.empty:
        return dcc.Graph(figure=go.Figure())
    
    required_cols = ['total_creditos_aprobados', 'promedio_ultimo_semestre']
    if not all(col in df.columns for col in required_cols):
        return dcc.Graph(figure=go.Figure())
    
    plot_df = df[required_cols + ['programa']].dropna()
    
    fig = px.scatter(
        plot_df,
        x='total_creditos_aprobados',
        y='promedio_ultimo_semestre',
        color='programa',
        title='Créditos Aprobados vs Promedio',
        labels={
            'total_creditos_aprobados': 'Créditos Aprobados',
            'promedio_ultimo_semestre': 'Promedio (GPA)'
        },
        hover_data=['programa']
    )
    
    fig.update_layout(template='plotly_white')
    
    return dcc.Graph(figure=fig)

def create_estrato_distribution_pie(df):
    """Create pie chart of socioeconomic stratum distribution"""
    if df.empty or 'estrato' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    estrato_counts = df['estrato'].value_counts().reset_index()
    estrato_counts.columns = ['Estrato', 'Estudiantes']
    estrato_counts['Estrato'] = estrato_counts['Estrato'].astype(str)
    
    fig = px.pie(
        estrato_counts,
        values='Estudiantes',
        names='Estrato',
        title='Distribución por Estrato Socioeconómico',
        hole=0.4
    )
    
    fig.update_layout(template='plotly_white')
    
    return dcc.Graph(figure=fig)

def create_performance_heatmap(df):
    """Create heatmap of performance metrics by program"""
    if df.empty or 'programa' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    # Calculate metrics by program
    metrics = df.groupby('programa').agg({
        'promedio_ultimo_semestre': 'mean',
        'total_creditos_aprobados': 'mean',
        'total_materias_reprobadas': 'mean'
    }).reset_index()
    
    # Normalize for heatmap
    programs = metrics['programa'].tolist()
    
    fig = go.Figure(data=go.Heatmap(
        z=[
            metrics['promedio_ultimo_semestre'].tolist(),
            metrics['total_creditos_aprobados'].tolist(),
            metrics['total_materias_reprobadas'].tolist()
        ],
        x=programs,
        y=['Promedio GPA', 'Créditos Aprobados', 'Materias Reprobadas'],
        colorscale='RdYlGn',
        text=[[f'{val:.2f}' for val in row] for row in [
            metrics['promedio_ultimo_semestre'].tolist(),
            metrics['total_creditos_aprobados'].tolist(),
            metrics['total_materias_reprobadas'].tolist()
        ]],
        texttemplate='%{text}',
        textfont={"size": 10}
    ))
    
    fig.update_layout(
        title='Mapa de Calor: Métricas por Programa',
        template='plotly_white'
    )
    
    return dcc.Graph(figure=fig)

def create_kpi_card(title, value, icon, color="primary"):
    """Create a KPI card component"""
    import dash_bootstrap_components as dbc
    from dash import html
    
    return dbc.Card([
        dbc.CardBody([
            html.Div([
                html.I(className=f"fas fa-{icon} fa-2x", style={'color': f'var(--bs-{color})'}),
                html.H4(title, className="card-title mt-2"),
                html.H2(value, className="card-text", style={'color': f'var(--bs-{color})'})
            ], className="text-center")
        ])
    ], className="shadow-sm mb-3")
