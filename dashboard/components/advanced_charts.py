"""
Advanced chart components for data analysts
"""
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc
import pandas as pd
import numpy as np

# Common layout for dark theme
DARK_LAYOUT = dict(
    template='plotly_dark',
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    font=dict(color='#94a3b8'),
    margin=dict(l=40, r=40, t=40, b=40)
)

def create_correlation_matrix(df):
    """Create interactive correlation heatmap"""
    if df.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if len(numeric_cols) < 2:
        return dcc.Graph(figure=go.Figure())
    
    # Calculate correlation matrix
    corr_matrix = df[numeric_cols].corr()
    
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmid=0,
        text=corr_matrix.values.round(2),
        texttemplate='%{text}',
        textfont={"size": 10},
        colorbar=dict(title="Correlación")
    ))
    
    fig.update_layout(
        title='Matriz de Correlación de Variables',
        height=600,
        xaxis={'side': 'bottom'},
        yaxis={'autorange': 'reversed'},
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_feature_importance_chart(importance_df):
    """Create feature importance bar chart"""
    if importance_df.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Take top 10 features
    top_features = importance_df.head(10)
    
    fig = go.Figure(data=[
        go.Bar(
            x=top_features['Abs_Correlation'],
            y=top_features['Feature'],
            orientation='h',
            marker=dict(
                color=top_features['Correlation'],
                colorscale='Viridis',
                showscale=True,
                colorbar=dict(title="Correlación")
            ),
            text=top_features['Correlation'].round(3),
            textposition='auto',
        )
    ])
    
    fig.update_layout(
        title='Top 10 Features Correlacionadas',
        xaxis_title='Correlación Absoluta',
        yaxis_title='Variable',
        height=500,
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_cohort_analysis_chart(cohort_df):
    """Create cohort analysis multi-line chart"""
    if cohort_df.empty:
        return dcc.Graph(figure=go.Figure())
    
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=('Estudiantes por Semestre', 'Promedio GPA', 
                       'Créditos Promedio', 'Materias Reprobadas'),
        specs=[[{'type': 'scatter'}, {'type': 'scatter'}],
               [{'type': 'scatter'}, {'type': 'scatter'}]]
    )
    
    # Students count
    fig.add_trace(
        go.Scatter(x=cohort_df['Semestre'], y=cohort_df['Total Estudiantes'],
                  mode='lines+markers', name='Estudiantes',
                  line=dict(color='#6366f1', width=3)),
        row=1, col=1
    )
    
    # GPA
    fig.add_trace(
        go.Scatter(x=cohort_df['Semestre'], y=cohort_df['Promedio GPA'],
                  mode='lines+markers', name='GPA',
                  line=dict(color='#10b981', width=3)),
        row=1, col=2
    )
    
    # Credits
    fig.add_trace(
        go.Scatter(x=cohort_df['Semestre'], y=cohort_df['Créditos Promedio'],
                  mode='lines+markers', name='Créditos',
                  line=dict(color='#f59e0b', width=3)),
        row=2, col=1
    )
    
    # Failed courses
    fig.add_trace(
        go.Scatter(x=cohort_df['Semestre'], y=cohort_df['Materias Reprobadas Promedio'],
                  mode='lines+markers', name='Reprobadas',
                  line=dict(color='#ef4444', width=3)),
        row=2, col=2
    )
    
    fig.update_layout(
        title_text='Análisis de Cohortes por Semestre',
        height=700,
        showlegend=False,
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_retention_curve(retention_df):
    """Create retention curve visualization"""
    if retention_df.empty:
        return dcc.Graph(figure=go.Figure())
    
    fig = go.Figure()
    
    # Retention rate line
    fig.add_trace(go.Scatter(
        x=retention_df['Semestre'],
        y=retention_df['Tasa_Retencion'],
        mode='lines+markers',
        name='Tasa de Retención',
        line=dict(color='#10b981', width=4),
        marker=dict(size=10),
        fill='tozeroy',
        fillcolor='rgba(16, 185, 129, 0.2)'
    ))
    
    # Add reference line at 80%
    fig.add_hline(y=80, line_dash="dash", line_color="#ef4444",
                  annotation_text="Meta: 80%", annotation_position="right")
    
    fig.update_layout(
        title='Curva de Retención Estudiantil',
        xaxis_title='Semestre',
        yaxis_title='Tasa de Retención (%)',
        hovermode='x unified',
        height=400,
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_boxplot_by_program(df, metric='promedio_ultimo_semestre'):
    """Create box plot comparing programs"""
    if df.empty or metric not in df.columns or 'programa' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    fig = go.Figure()
    
    programs = df['programa'].unique()
    colors = px.colors.qualitative.Pastel
    
    for i, program in enumerate(programs):
        program_data = df[df['programa'] == program][metric]
        fig.add_trace(go.Box(
            y=program_data,
            name=program,
            marker_color=colors[i % len(colors)],
            boxmean='sd'  # Show mean and standard deviation
        ))
    
    fig.update_layout(
        title=f'Distribución de {metric} por Programa',
        yaxis_title=metric,
        height=500,
        showlegend=False,
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_3d_scatter(df):
    """Create 3D scatter plot for multivariate analysis"""
    if df.empty:
        return dcc.Graph(figure=go.Figure())
    
    required_cols = ['total_creditos_aprobados', 'promedio_ultimo_semestre', 'total_materias_reprobadas']
    if not all(col in df.columns for col in required_cols):
        return dcc.Graph(figure=go.Figure())
    
    fig = px.scatter_3d(
        df,
        x='total_creditos_aprobados',
        y='promedio_ultimo_semestre',
        z='total_materias_reprobadas',
        color='programa' if 'programa' in df.columns else None,
        title='Análisis Multivariado 3D',
        labels={
            'total_creditos_aprobados': 'Créditos Aprobados',
            'promedio_ultimo_semestre': 'Promedio (GPA)',
            'total_materias_reprobadas': 'Materias Reprobadas'
        },
        height=700
    )
    
    fig.update_layout(
        scene=dict(
            xaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
            yaxis=dict(backgroundcolor="rgba(0,0,0,0)"),
            zaxis=dict(backgroundcolor="rgba(0,0,0,0)")
        ),
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': True})

def create_funnel_chart(df):
    """Create funnel chart for student progression"""
    if df.empty or 'ultimo_semestre_cursado' not in df.columns:
        return dcc.Graph(figure=go.Figure())
    
    # Count students by semester
    semester_counts = df.groupby('ultimo_semestre_cursado').size().sort_index()
    
    fig = go.Figure(go.Funnel(
        y=[f'Semestre {i}' for i in semester_counts.index],
        x=semester_counts.values,
        textinfo="value+percent initial",
        marker=dict(color=px.colors.sequential.Purp)
    ))
    
    fig.update_layout(
        title='Embudo de Progresión Estudiantil',
        height=500,
        **DARK_LAYOUT
    )
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})

def create_sunburst_chart(df):
    """Create sunburst chart for hierarchical data"""
    if df.empty:
        return dcc.Graph(figure=go.Figure())
    
    # Create hierarchical structure: Programa -> Estrato -> Risk Level
    if not all(col in df.columns for col in ['programa', 'estrato']):
        return dcc.Graph(figure=go.Figure())
    
    # Add risk level
    if 'total_materias_reprobadas' in df.columns:
        df['risk_level'] = pd.cut(
            df['total_materias_reprobadas'],
            bins=[-1, 0, 2, 100],
            labels=['Bajo', 'Medio', 'Alto']
        )
    else:
        return dcc.Graph(figure=go.Figure())
    
    # Create sunburst data
    fig = px.sunburst(
        df,
        path=['programa', 'estrato', 'risk_level'],
        title='Distribución Jerárquica',
        height=600,
        color='risk_level',
        color_discrete_map={
            'Bajo': '#10b981',
            'Medio': '#f59e0b',
            'Alto': '#ef4444'
        }
    )
    
    fig.update_layout(**DARK_LAYOUT)
    
    return dcc.Graph(figure=fig, config={'displayModeBar': False})
