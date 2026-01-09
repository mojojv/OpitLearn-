import dask.dataframe as dd
import pandas as pd
import logging
from src.validation.validator import AcademicValidator

logger = logging.getLogger(__name__)

class DataTransformer:
    """
    Módulo de transformación de datos académicos.
    Utiliza Dask para procesamiento distribuido/escalable.
    """
    
    def __init__(self):
        self.validator = AcademicValidator()

    def procesar(self, ddf_estudiantes, ddf_historico):
        """
        Calcula dataset final uniendo estudiantes con su historia académica reciente o agregada.
        """
        logger.info("Iniciando transformación de datos...")
        
        # 1. Limpieza básica
        ddf_est = self._limpiar_estudiantes(ddf_estudiantes)
        ddf_hist = self._limpiar_historico(ddf_historico)
        
        # 2. Agregar información histórica (Perfilamiento de estudiante)
        # Calculamos el promedio acumulado más reciente y el estado actual
        # Dask no soporta 'sort_values' global eficientemente, por ahora agrupamos
        
        # Estrategia: Tomar el último semestre reportado por estudiante
        # Asumimos que 'semestre_ordinal' define el orden
        
        # Para simplificar en Dask, convertimos ddf_hist a algo manejable o 
        # hacemos map_partitions. Dado el volumen (csv pequeño), compute() es viable aquí 
        # pero mantendremos semántica Dask donde sea posible.
        
        # 2. Agregar información histórica (Perfilamiento de estudiante)
        # Calcular agregados simples (Sumas)
        hist_stats = ddf_hist.groupby('estudiante_id').agg({
            'creditos_aprobados': 'sum',
            'materias_reprobadas': 'sum'
        }).reset_index()
        
        hist_stats = hist_stats.rename(columns={
            'creditos_aprobados': 'total_creditos_aprobados',
            'materias_reprobadas': 'total_materias_reprobadas'
        })

        # Obtener el último promedio reportado (basado en semestre_ordinal máximo)
        # 1. Encontrar el max semestre por estudiante
        max_semestre = ddf_hist.groupby('estudiante_id')['semestre_ordinal'].max().reset_index()
        
        # 2. Unir con el histórico para filtrar solo las filas del último semestre
        # Nota: Esto nos da el estado más reciente
        ultimo_estado = dd.merge(ddf_hist, max_semestre, on=['estudiante_id', 'semestre_ordinal'], how='inner')
        
        # Seleccionar columnas de interés del último estado
        ultimo_estado = ultimo_estado[['estudiante_id', 'semestre_ordinal', 'promedio_acumulado']]
        ultimo_estado = ultimo_estado.rename(columns={
            'semestre_ordinal': 'ultimo_semestre_cursado',
            'promedio_acumulado': 'promedio_ultimo_semestre'
        })

        # 3. Unir todo
        # Primero unir stats con último estado
        hist_perfil = dd.merge(hist_stats, ultimo_estado, on='estudiante_id', how='left')
        
        # Luego unir con estudiantes
        ddf_final = dd.merge(ddf_est, hist_perfil, on='estudiante_id', how='inner')
        
        return ddf_final

    def _limpiar_estudiantes(self, ddf):
        # Estandarizacion
        if 'programa' in ddf.columns:
            ddf['programa'] = ddf['programa'].str.upper().str.strip()
        return ddf

    def _limpiar_historico(self, ddf):
        # Validar rangos
        return ddf
