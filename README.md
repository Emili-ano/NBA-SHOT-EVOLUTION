# NBA Shot Evolution

Proyecto semestral de ingeniería de datos.

## Integrantes
- Emiliano
- Majo
- Sofía

## Problema
Estudiar la evolución de la selección y efectividad
de los tiros de campo en la NBA.

## Pregunta principal
¿Cómo cambia la selección y efectividad de los
tiros de la NBA según temporada, equipo y zona?

## Objetivo
Construir un pipeline reproducible para adquirir,
procesar, validar y analizar datos de tiros NBA.

## Fuentes de datos
NBA Stats, mediante archivos publicados por
SportsDataverse en GitHub Releases.

## Estructura del repositorio
- data/: datos crudos, intermedios y procesados
- docs/: documentación
- notebooks/: exploración y análisis
- src/: código del pipeline
- tests/: pruebas automatizadas
- reports/: resultados y métricas
- config/: configuración

## Instrucciones iniciales de ejecución
Instalar las dependencias:

    python -m pip install -r requirements.txt

Descargar los datos:

    python -m src.ingestion.download_data --years 2024 2025 2026

Explorar los datos:

    python -m src.analysis.inspect_data

## Estado actual
Adquisición automatizada y exploración preliminar
implementadas. Procesamiento y validación pendientes.
