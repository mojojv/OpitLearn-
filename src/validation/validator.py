import pandas as pd
import numpy as np
import logging

# Configurar logger
logger = logging.getLogger(__name__)

class AcademicValidator:
    """
    Clase para validación de datos académicos y calidad de datos.
    """
    
    @staticmethod
    def validar_esquema(df, columnas_requeridas):
        """
        Valida que el DataFrame contenga las columnas requeridas.
        """
        columnas_faltantes = [col for col in columnas_requeridas if col not in df.columns]
        if columnas_faltantes:
            raise ValueError(f"Faltan columnas requeridas: {columnas_faltantes}")
        return True

    @staticmethod
    def validar_reglas_negocio(df):
        """
        Aplica reglas de negocio académicas.
        Retorna el DataFrame con una columna 'is_valid' y logs de errores.
        """
        # Inicializar máscara de validación
        valid_mask = pd.Series(True, index=df.index)
        
        # Regla 1: Promedios (0-5.0)
        for col in ['promedio_semestral', 'promedio_acumulado', 'nota_final', 'gpa']:
            if col in df.columns:
                mask_gpa = df[col].between(0.0, 5.0) | df[col].isna()
                valid_mask &= mask_gpa
                invalid_count = (~mask_gpa).sum()
                if invalid_count > 0:
                    logger.warning(f"Columna {col}: {invalid_count} registros fuera de rango [0-5].")

        # Regla 2: Puntaje Saber 11 (0-500)
        if 'puntaje_saber11' in df.columns:
             mask_saber = df['puntaje_saber11'].between(0, 500) | df['puntaje_saber11'].isna()
             valid_mask &= mask_saber
             invalid_count = (~mask_saber).sum()
             if invalid_count > 0:
                 logger.warning(f"Saber 11: {invalid_count} registros fuera de rango [0-500].")

        # Regla 3: Estrato (1-6)
        if 'estrato' in df.columns:
            mask_estrato = df['estrato'].between(1, 6) | df['estrato'].isna()
            valid_mask &= mask_estrato
            
        # Regla 4: Créditos
        if 'creditos_aprobados' in df.columns and 'creditos_matriculados' in df.columns:
            mask_creditos = df['creditos_aprobados'] <= df['creditos_matriculados']
            # Permitir casos donde matriculados sea 0 o nulo si aplica
            valid_mask &= (mask_creditos | df['creditos_matriculados'].isna())

        return valid_mask

    @staticmethod
    def detectar_outliers(df, columna, metodo='iqr', umbral=1.5):
        """
        Detecta outliers en una columna numérica.
        """
        if metodo == 'iqr':
            Q1 = df[columna].quantile(0.25)
            Q3 = df[columna].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - (umbral * IQR)
            upper_bound = Q3 + (umbral * IQR)
            return ~df[columna].between(lower_bound, upper_bound)
        return pd.Series(False, index=df.index)
