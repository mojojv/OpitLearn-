"""
Advanced ML metrics and feature engineering for OpitLearn Dashboard
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

def calculate_advanced_metrics(df):
    """Calculate advanced ML-ready metrics"""
    if df.empty:
        return {}
    
    metrics = {}
    
    # Academic Performance Index (API)
    if all(col in df.columns for col in ['promedio_ultimo_semestre', 'total_creditos_aprobados']):
        df['academic_performance_index'] = (
            df['promedio_ultimo_semestre'] * 0.6 + 
            (df['total_creditos_aprobados'] / df['total_creditos_aprobados'].max()) * 5 * 0.4
        )
        metrics['avg_api'] = df['academic_performance_index'].mean()
    
    # Retention Risk Score
    if 'total_materias_reprobadas' in df.columns:
        df['retention_risk'] = np.where(
            df['total_materias_reprobadas'] > 3, 'Alto',
            np.where(df['total_materias_reprobadas'] > 1, 'Medio', 'Bajo')
        )
        metrics['high_risk_pct'] = (df['retention_risk'] == 'Alto').sum() / len(df) * 100
    
    # Credit Efficiency Ratio
    if all(col in df.columns for col in ['total_creditos_aprobados', 'ultimo_semestre_cursado']):
        df['credit_efficiency'] = df['total_creditos_aprobados'] / (df['ultimo_semestre_cursado'] + 1)
        metrics['avg_credit_efficiency'] = df['credit_efficiency'].mean()
    
    # Socioeconomic Impact Score
    if all(col in df.columns for col in ['estrato', 'promedio_ultimo_semestre']):
        # Students from lower strata with high performance
        low_strata_high_perf = df[(df['estrato'] <= 2) & (df['promedio_ultimo_semestre'] >= 4.0)]
        metrics['social_mobility_count'] = len(low_strata_high_perf)
    
    return metrics

def calculate_feature_importance(df):
    """Calculate feature correlations with academic success"""
    if df.empty or 'promedio_ultimo_semestre' not in df.columns:
        return pd.DataFrame()
    
    # Select numeric columns
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if 'promedio_ultimo_semestre' not in numeric_cols:
        return pd.DataFrame()
    
    # Calculate correlations with GPA
    correlations = df[numeric_cols].corr()['promedio_ultimo_semestre'].drop('promedio_ultimo_semestre')
    
    # Create feature importance dataframe
    importance_df = pd.DataFrame({
        'Feature': correlations.index,
        'Correlation': correlations.values,
        'Abs_Correlation': np.abs(correlations.values)
    }).sort_values('Abs_Correlation', ascending=False)
    
    return importance_df

def perform_cohort_analysis(df):
    """Analyze student cohorts by semester"""
    if df.empty or 'ultimo_semestre_cursado' not in df.columns:
        return pd.DataFrame()
    
    cohort_stats = df.groupby('ultimo_semestre_cursado').agg({
        'estudiante_id': 'count',
        'promedio_ultimo_semestre': 'mean',
        'total_creditos_aprobados': 'mean',
        'total_materias_reprobadas': 'mean'
    }).reset_index()
    
    cohort_stats.columns = [
        'Semestre', 'Total Estudiantes', 'Promedio GPA',
        'Créditos Promedio', 'Materias Reprobadas Promedio'
    ]
    
    return cohort_stats

def calculate_retention_curve(df):
    """Calculate retention rates by semester"""
    if df.empty or 'ultimo_semestre_cursado' not in df.columns:
        return pd.DataFrame()
    
    # Assuming students should progress ~1 semester per period
    retention_data = df.groupby('ultimo_semestre_cursado').size().reset_index()
    retention_data.columns = ['Semestre', 'Estudiantes']
    
    # Calculate retention rate (students remaining vs initial)
    if len(retention_data) > 0:
        initial_count = retention_data['Estudiantes'].iloc[0]
        retention_data['Tasa_Retencion'] = (retention_data['Estudiantes'] / initial_count) * 100
    
    return retention_data

def generate_ml_features(df):
    """Generate ML-ready features for predictive modeling"""
    if df.empty:
        return df
    
    df_ml = df.copy()
    
    # Interaction features
    if all(col in df.columns for col in ['promedio_ultimo_semestre', 'total_creditos_aprobados']):
        df_ml['gpa_credits_interaction'] = df_ml['promedio_ultimo_semestre'] * df_ml['total_creditos_aprobados']
    
    # Polynomial features
    if 'promedio_ultimo_semestre' in df.columns:
        df_ml['gpa_squared'] = df_ml['promedio_ultimo_semestre'] ** 2
    
    # Binned features
    if 'puntaje_saber11' in df.columns:
        df_ml['saber11_category'] = pd.cut(
            df_ml['puntaje_saber11'],
            bins=[0, 200, 300, 400, 500],
            labels=['Bajo', 'Medio', 'Alto', 'Muy Alto']
        )
    
    # Risk flags
    if 'total_materias_reprobadas' in df.columns:
        df_ml['has_failed_courses'] = (df_ml['total_materias_reprobadas'] > 0).astype(int)
    
    return df_ml

def calculate_program_benchmarks(df):
    """Calculate benchmarks for each program"""
    if df.empty or 'programa' not in df.columns:
        return pd.DataFrame()
    
    benchmarks = df.groupby('programa').agg({
        'promedio_ultimo_semestre': ['mean', 'std', 'min', 'max'],
        'total_creditos_aprobados': ['mean', 'std'],
        'total_materias_reprobadas': ['mean', 'std'],
        'estudiante_id': 'count'
    }).round(2)
    
    benchmarks.columns = ['_'.join(col).strip() for col in benchmarks.columns.values]
    benchmarks = benchmarks.reset_index()
    
    return benchmarks
