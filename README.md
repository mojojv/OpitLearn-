# OpitLearn: Plataforma de Analítica Académica

OpitLearn es un sistema integral para la gestión, análisis y predicción de trayectorias académicas. Utiliza pipelines de datos robustos (ETL) y dashboards interactivos para potenciar la toma de decisiones en instituciones educativas.

## Características Principales
- 🔄 **ETL Pipeline**: Procesamiento de datos escalable con Dask y Pandas.
- 📊 **Dashboard Interactivo**: Visualización avanzada con Dash (Plotly).
- 🔐 **Seguridad**: Autenticación basada en roles (Admin/Analista).
- 🔬 **ML & Analytics**: Métricas predictivas y análisis de cohortes.

## Estructura del Proyecto

- `dashboard/`: Aplicación web de analítica (Dash).
- `data/`: Almacén de datos (crudos, curados).
- `src/`: Código fuente del pipeline.
    - `etl/`: Extracción y transformación.
    - `validation/`: Reglas de negocio y calidad.
    - `features/`: Ingeniería de características.
- `run_pipeline.py`: Orquestador del proceso ETL.

## Instalación

1.  Crear entorno virtual:
    ```bash
    python -m venv .venv
    ```
2.  Activar entorno (Windows):
    ```bash
    .venv\Scripts\activate
    ```
3.  Instalar dependencias:
    ```bash
    pip install -r dashboard/requirements.txt
    ```

## Uso

### 1. Ejecutar Pipeline ETL
Procesa los datos crudos y genera la tabla maestra en parquet.
```bash
python run_pipeline.py
```

### 2. Iniciar Dashboard
Lanza la interfaz web de analítica.
```bash
python dashboard/index.py
```
> Acceder en: `http://127.0.0.1:8050`

**Credenciales Demo:**
- **Admin**: `admin` / `admin123`
- **Analista**: `analyst` / `analyst123`
