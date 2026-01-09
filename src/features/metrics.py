import numpy as np

class AcademicMetrics:
    """
    Implementación de modelos matemáticos para analítica académica.
    """

    @staticmethod
    def calcular_indice_riesgo(promedio, tasa_reprobacion, semestre_actual):
        """
        Calcula un Índice de Riesgo Académico Continuo (0 a 1).
        
        Fórmula propuesta:
        Riesgo = w1 * (1 - Promedio/MaxPromedio) + w2 * TasaReprobación + w3 * FactorSemestre
        
        Donde:
        - Promedio normalizado invierte la lógica (mayor promedio, menor riesgo).
        - Tasa reprobación aumenta el riesgo.
        - Factor Semestre ajusta riesgo en primeros semestres (mayor deserción temprana).
        """
        MAX_PROMEDIO = 5.0
        w1, w2, w3 = 0.5, 0.3, 0.2
        
        norm_promedio = min(promedio / MAX_PROMEDIO, 1.0)
        risk_promedio = 1.0 - norm_promedio
        
        # Factor corrector para semestres iniciales (ej. < 3)
        factor_semestre = 1.1 if semestre_actual <= 2 else 0.9
        
        indice = (w1 * risk_promedio) + (w2 * tasa_reprobacion)
        indice *= factor_semestre
        
        return min(max(indice, 0.0), 1.0) # Clip entre 0 y 1

    @staticmethod
    def calcular_tasa_progresion(creditos_aprobados, creditos_totales_programa):
        """
        Avance porcentual en la malla curricular.
        """
        if creditos_totales_programa == 0:
            return 0.0
        return min(creditos_aprobados / creditos_totales_programa, 1.0)

    @staticmethod
    def probabilidad_desercion_logistica(features, coeficientes, intercepto):
        """
        Implementación manual de regresión logística para inferencia rápida.
        P(Y=1) = 1 / (1 + e^-(beta0 + beta*x))
        """
        z = intercepto + np.dot(features, coeficientes)
        return 1 / (1 + np.exp(-z))
