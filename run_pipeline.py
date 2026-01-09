import logging
import sys
from pathlib import Path

# Configurar path
ROOT_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT_DIR))

from opitlearn.config import settings
from opitlearn.src.etl.extract import DataExtractor
from opitlearn.src.etl.transform import DataTransformer
from opitlearn.src.etl.load import DataLoader
from opitlearn.src.validation.validator import AcademicValidator

def configurar_logs():
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[logging.StreamHandler()]
    )

def main():
    configurar_logs()
    logger = logging.getLogger("Orquestador")
    logger.info("Iniciando Pipeline OpitLearn con Datos Reales...")

    extractor = DataExtractor(data_dir=settings.DATA_DIR)
    transformer = DataTransformer()
    loader = DataLoader(db_url=settings.DATABASE_URL)
    validator = AcademicValidator()

    try:
        # 1. Extracción
        ddf_estudiantes = extractor.leer_estudiantes()
        ddf_historico = extractor.leer_historico()
        
        logger.info(f"Estudiantes cargados (lazy): {ddf_estudiantes.npartitions} particiones")
        logger.info(f"Historico cargado (lazy): {ddf_historico.npartitions} particiones")

        # 2. Transformación y Merge
        ddf_final = transformer.procesar(ddf_estudiantes, ddf_historico)
        
        # 3. Validación (sobre una muestra o todo si es pequeño)
        # Al ser lazy, esto no ejecuta todavía.
        
        # 4. Carga
        output_path = settings.CURATED_DATA_DIR / "master_table.parquet"
        loader.guardar_parquet(ddf_final, str(output_path))
        
        # Generar vista previa
        preview = ddf_final.head()
        logger.info("\nVista previa de datos curados:\n" + str(preview))
        
        # Validación de salida
        valid_mask = validator.validar_reglas_negocio(preview) # Validar la muestra
        if not valid_mask.all():
            logger.warning("Algunos registros en la muestra fallaron validación.")

    except Exception as e:
        logger.critical(f"Pipeline falló: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
