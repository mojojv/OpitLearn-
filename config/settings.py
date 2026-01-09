import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# Rutas Base
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
RAW_DATA_DIR = DATA_DIR / "raw"
CURATED_DATA_DIR = DATA_DIR / "curated"
FEATURES_DIR = DATA_DIR / "features"

# Base de Datos
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "opitlearn")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Configuración Dask
DASK_SCHEDULER_HOST = os.getenv("DASK_SCHEDULER_HOST", "localhost")

# Parámetros Académicos
MIN_PASSING_GRADE = 3.0
MAX_GPA = 5.0
