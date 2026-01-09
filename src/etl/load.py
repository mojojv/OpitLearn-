from sqlalchemy import create_engine
import logging
import dask.dataframe as dd

logger = logging.getLogger(__name__)

class DataLoader:
    """
    Módulo para cargar datos procesados a almacenamiento persistente (PostgreSQL).
    """

    def __init__(self, db_url):
        self.db_url = db_url
        self.engine = create_engine(self.db_url)

    def guardar_en_sql(self, ddf, nombre_tabla, if_exists='append'):
        """
        Guarda un Dask DataFrame en SQL.
        Se calcula (compute) y se guarda. Nota: Para muy grandes volúmenes, 
        se recomienda usar COPY command o 'to_sql' por particiones.
        """
        logger.info(f"Guardando datos en tabla: {nombre_tabla}")
        
        try:
            # Opimización: map_partitions para escribir en paralelo si es soportado,
            # o compute() para dataset mediano.
            
            # Método simple: compute() y pandas to_sql
            # OJO: Esto trae todo a memoria. Para producción masiva, iterar particiones.
            PDF = ddf.compute() 
            
            PDF.to_sql(name=nombre_tabla, con=self.engine, if_exists=if_exists, index=False)
            logger.info("Carga completada exitosamente.")
            
        except Exception as e:
            logger.error(f"Error guardando en base de datos: {e}")
            raise

    def guardar_parquet(self, ddf, ruta_salida):
        """
        Guarda en formato Parquet (eficiente para analítica local).
        """
        try:
            ddf.to_parquet(ruta_salida, engine='pyarrow')
            logger.info(f"Datos guardados en Parquet: {ruta_salida}")
        except Exception as e:
            logger.error(f"Error exportando a Parquet: {e}")
            raise
