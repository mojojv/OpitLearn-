import dask.dataframe as dd
import os
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

class DataExtractor:
    """
    Módulo encargado de la extracción de datos desde diversas fuentes.
    Soporta lectura diferida (lazy evaluation) con Dask.
    """
    
    def __init__(self, data_dir):
        self.data_dir = Path(data_dir)

    def leer_estudiantes(self):
        """
        Lee dataset_estudiantes_v2.csv
        """
        path = self.data_dir / "raw" / "dataset_estudiantes_v2.csv"
        logger.info(f"Leyendo estudiantes: {path}")
        return dd.read_csv(path, assume_missing=True)

    def leer_historico(self):
        """
        Lee dataset_historico_v2.csv
        """
        path = self.data_dir / "raw" / "dataset_historico_v2.csv"
        logger.info(f"Leyendo historico: {path}")
        return dd.read_csv(path, assume_missing=True)
