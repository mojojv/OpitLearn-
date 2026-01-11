"""
KPI and metrics calculation for OpitLearn Dashboard
"""
import pandas as pd
import numpy as np

def calculate_kpis(df):
    """Calculate key performance indicators from dataframe"""
    if df.empty:
        return {
            'total_students': 0,
            'avg_gpa': 0,
            'retention_rate': 0,
            'at_risk_count': 0
        }
    
    kpis = {}
    
    # Total students
    kpis['total_students'] = len(df)
    
    # Average GPA (using promedio_ultimo_semestre if available)
    gpa_col = 'promedio_ultimo_semestre' if 'promedio_ultimo_semestre' in df.columns else None
    if gpa_col and df[gpa_col].notna().any():
        kpis['avg_gpa'] = df[gpa_col].mean()
    else:
        kpis['avg_gpa'] = 0
    
    # Retention rate (students with credits > 0)
    if 'total_creditos_aprobados' in df.columns:
        active_students = df[df['total_creditos_aprobados'] > 0].shape[0]
        kpis['retention_rate'] = (active_students / len(df) * 100) if len(df) > 0 else 0
    else:
        kpis['retention_rate'] = 0
    
    # At-risk students (GPA < 3.0 or high failed courses)
    at_risk = 0
    if gpa_col and df[gpa_col].notna().any():
        at_risk += df[df[gpa_col] < 3.0].shape[0]
    if 'total_materias_reprobadas' in df.columns:
        at_risk += df[df['total_materias_reprobadas'] > 3].shape[0]
    kpis['at_risk_count'] = at_risk
    
    return kpis

def calculate_program_stats(df):
    """Calculate statistics by program"""
    if df.empty or 'programa' not in df.columns:
        return pd.DataFrame()
    
    stats = df.groupby('programa').agg({
        'estudiante_id': 'count',
        'promedio_ultimo_semestre': 'mean',
        'total_creditos_aprobados': 'mean'
    }).reset_index()
    
    stats.columns = ['Programa', 'Total Estudiantes', 'Promedio GPA', 'Créditos Promedio']
    return stats

def identify_at_risk_students(df, threshold_gpa=3.0, threshold_failed=3):
    """Identify at-risk students"""
    if df.empty:
        return pd.DataFrame()
    
    at_risk = df.copy()
    
    # Filter conditions
    conditions = []
    if 'promedio_ultimo_semestre' in df.columns:
        conditions.append(df['promedio_ultimo_semestre'] < threshold_gpa)
    if 'total_materias_reprobadas' in df.columns:
        conditions.append(df['total_materias_reprobadas'] > threshold_failed)
    
    if conditions:
        mask = pd.concat(conditions, axis=1).any(axis=1)
        at_risk = df[mask]
    
    return at_risk

def calculate_risk_scores_vectorized(df):
    """
    Calculate risk scores for the entire dataframe utilizing vectorization (0-100).
    Faster than row-by-row application.
    """
    if df.empty:
        return pd.Series(dtype=float)

    scores = pd.Series(0.0, index=df.index)

    # GPA component (40 points)
    if 'promedio_ultimo_semestre' in df.columns:
        gpa = df['promedio_ultimo_semestre'].fillna(3.0)  # Neutral fill
        gpa_score = np.maximum(0, (3.0 - gpa) / 3.0 * 40)
        scores += gpa_score

    # Failed courses component (30 points)
    if 'total_materias_reprobadas' in df.columns:
        failed = df['total_materias_reprobadas'].fillna(0)
        failed_score = np.minimum(failed / 5 * 30, 30)
        scores += failed_score

    # Credit progress component (30 points)
    if 'total_creditos_aprobados' in df.columns:
        credits_aprob = df['total_creditos_aprobados'].fillna(30) # Neutral fill
        credits_score = np.maximum(0, (30 - credits_aprob) / 30 * 30)
        scores += credits_score
    
    return np.minimum(scores, 100)

def calculate_risk_score(row):
    """
    Calculate risk score for a student (0-100) - Legacy row-wise version.
    Kept for backward compatibility if needed, but vectorized is preferred.
    """
    score = 0
    
    # GPA component (40 points)
    if 'promedio_ultimo_semestre' in row and pd.notna(row['promedio_ultimo_semestre']):
        gpa = row['promedio_ultimo_semestre']
        if gpa < 3.0:
            score += (3.0 - gpa) / 3.0 * 40
    
    # Failed courses component (30 points)
    if 'total_materias_reprobadas' in row and pd.notna(row['total_materias_reprobadas']):
        failed = row['total_materias_reprobadas']
        score += min(failed / 5 * 30, 30)
    
    # Credit progress component (30 points)
    if 'total_creditos_aprobados' in row and pd.notna(row['total_creditos_aprobados']):
        credits_val = row['total_creditos_aprobados']
        if credits_val < 30:  # Assuming 30 is low
            score += (30 - credits_val) / 30 * 30
    
    return min(score, 100)
