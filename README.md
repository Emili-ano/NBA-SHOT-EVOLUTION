# NBA SHOT IQ

### Data Engineering & Basketball Analytics

## Descripción

NBA SHOT IQ es un pipeline reproducible de ingeniería de datos que descarga, limpia, valida y analiza más de 700,000 intentos de tiro de la NBA (temporadas 2023-24 a 2025-26). Su objetivo es evaluar con estadística si existen jugadores realmente "clutch", es decir, que rindan por encima de lo esperado en los momentos decisivos.

## Integrantes

- Emiliano
- Majo
- Sofía

## Problema

Las estadísticas tradicionales no distinguen si un jugador mejora en los momentos decisivos o si su fama de "clutch" se debe a la dificultad de sus tiros, al número de oportunidades o al azar.

## Pregunta principal

¿Existen jugadores de la NBA cuyo rendimiento en situaciones clutch sea estadísticamente superior al esperado, considerando la dificultad de sus lanzamientos, o las diferencias observadas pueden explicarse por la variación estadística?

Las preguntas secundarias y las hipótesis están en `docs/project_scope.md`.

## Arquitectura

```
SportsDataverse (GitHub Releases)
   -> src/ingestion      -> data/raw        (Parquet original)
   -> src/processing     -> data/interim    (limpio por temporada)
                         -> data/processed  (particionado por temporada)
   -> src/validation     -> docs/validation.md
   -> src/analysis       -> reports/tables, reports/figures
```

Hay una versión paralela Bronze/Silver/Gold en Databricks con PySpark. El detalle de ambas está en `docs/architecture.md`.

## Requisitos

- Python 3.11 o superior
- Las dependencias de `requirements.txt`: pandas, pyarrow, psutil, scikit-learn, scipy y matplotlib
- Conexión a internet para la descarga inicial (unos 13 MB)
- Opcional: Jupyter para abrir los notebooks

La conexión a Databricks (`conexion_databricks.py` y `src/analysis/inspect_data.py`) es **opcional** y requiere la variable de entorno `DATABRICKS_TOKEN`. El pipeline principal funciona sin ella.

## Instalación

Windows (PowerShell o Anaconda PowerShell):

    py -m venv .venv
    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

macOS / Linux:

    python3 -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt

## Obtención de datos

    python -m src.ingestion.download_data --years 2024 2025 2026

Los archivos se guardan en `data/raw/` junto con `ingestion_manifest.json` (tamaño y SHA-256). No se suben a GitHub. Para revisar la estructura sin descargar nada, hay una muestra de 300 tiros en `data/sample/nba_shots_sample.csv`.

## Ejecución

Pipeline completo con un solo comando:

    python main.py

Si los datos ya están descargados:

    python main.py --skip-download

O paso por paso:

    python -m src.ingestion.download_data --years 2024 2025 2026
    python -m src.processing.build_dataset
    python -m src.validation.validate_dataset
    python -m unittest discover -s tests -v
    python -m src.analysis.run_analysis
    python -m src.analysis.benchmark

En Windows se puede usar `.\.venv\Scripts\python.exe` en lugar de `python`.

## Resultados principales

| Resultado | Valor |
|---|---|
| Tiros procesados | 703,781 (24 duplicados eliminados) |
| Comprobaciones de calidad | 60 / 60 aprobadas |
| Pruebas automatizadas | 16 / 16 aprobadas |
| Efectividad clutch vs no clutch | 43.55% vs 47.16% (−3.60 pp, IC 95% −4.25 a −2.96) |
| Efectividad esperada en clutch por dificultad | 46.17% → caída ajustada −2.62 pp (IC 95% −3.23 a −2.01) |
| Jugadores evaluados (≥ 50 tiros clutch) | 162 |
| Jugadores con efecto clutch significativo (Benjamini-Hochberg) | **0** |

**Conclusión:** la liga encesta menos en clutch, y unas tres cuartas partes de esa caída no se explican por la dificultad del tiro. Sin embargo, ningún jugador muestra un rendimiento clutch superior al esperado que sea estadísticamente significativo, así que no se rechaza H0.

- Reporte completo: `docs/final_report.md`
- Tablas: `reports/tables/`
- Figuras: `reports/figures/`
- Herramienta interactiva: `reports/NBA_SHOT_IQ_Clutch_Strategy.html` (abrir en Chrome o Edge)
- Notebooks: `notebooks/03_analysis.ipynb` y `notebooks/04_results.ipynb`

## Estructura del repositorio

    config/          configuración de ejemplo
    data/            raw, interim, processed (no versionados) y sample
    docs/            alcance, fuentes, diccionario, arquitectura, decisiones,
                     validación, rendimiento, reproducibilidad, reporte final
                     y reflexiones individuales
    notebooks/       01 exploración, 03 análisis, 04 resultados y pipeline Databricks
    reports/         tablas, figuras, resumen del análisis y herramienta interactiva
    src/ingestion/   descarga de datos
    src/processing/  limpieza y capas de datos
    src/validation/  comprobaciones de calidad
    src/analysis/    análisis clutch, benchmark y exploración
    tests/           pruebas automatizadas
    main.py          ejecución completa del pipeline

## Documentación

- Alcance: `docs/project_scope.md`
- Fuente de datos: `docs/data_sources.md`
- Diccionario: `docs/data_dictionary.md`
- Arquitectura: `docs/architecture.md`
- Decisiones: `docs/decisions.md`
- Validaciones: `docs/validation.md`
- Rendimiento: `docs/performance.md`
- Reproducibilidad: `docs/reproducibility.md`
- Reporte final: `docs/final_report.md`
- Reflexiones: `docs/reflections/`

## Limitaciones

- El marcador previo a cada tiro se estima con el último enceste de campo. La fuente no incluye tiros libres.
- No hay información sobre la defensa, el cansancio ni el reloj de posesión.
- Tres temporadas dan poca potencia estadística para detectar efectos individuales pequeños.
- Es un análisis observacional: muestra asociaciones, no causas.

El detalle está en `docs/final_report.md#limitaciones`.

## Requisitos de la evaluación final

Cinco V, repetición de la carga, capas Bronze/Silver/Gold, escala y uso de IA: `docs/requisitos_evaluacion.md`
