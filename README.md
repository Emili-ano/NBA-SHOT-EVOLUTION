# NBA SHOT IQ

### Data Engineering & Basketball Analytics

**Integrantes:** Emiliano, Majo y Sofía

## Problema

La eficiencia de los tiros NBA puede estar relacionada
con su ubicacion, la secuencia de aciertos y el
contexto del partido.

## Pregunta principal

¿Que patrones de eficiencia de tiro se observan en la
NBA y como se relacionan con la zona de lanzamiento,
las rachas y las situaciones de cierre de partido?

## Objetivo

Construir un pipeline reproducible para adquirir,
limpiar, validar y preparar datos de tiros NBA,
y utilizarlos para investigar tres preguntas deportivas.

## Modulos de investigacion

1. Shot Selection: eficiencia por zona y tipo de tiro.
2. Hot Hand: efectividad despues de rachas.
3. Clutch Performance: rendimiento bajo presion.

## Fuente

Datos NBA Stats publicados por SportsDataverse.

Adquisicion mediante la API publica de GitHub
y descargas de archivos Parquet.

## Arquitectura

Fuente -> Raw -> Interim -> Processed -> Analisis

## Tecnologias

Python, pandas, PyArrow, Git y GitHub.
VS Code y PowerShell como entorno de desarrollo.

## Instalacion

Crear el entorno virtual:

    py -m venv .venv

Instalar dependencias:

    .\.venv\Scripts\python.exe -m pip install -r requirements.txt

## Adquisicion

    .\.venv\Scripts\python.exe -m src.ingestion.download_data --years 2024 2025 2026

## Exploracion preliminar

    .\.venv\Scripts\python.exe -m src.analysis.inspect_data

## Estructura

- data/: raw, interim, processed y sample
- docs/: documentacion y decisiones
- notebooks/: exploracion y resultados
- src/: adquisicion, procesamiento y validacion
- tests/: pruebas automatizadas
- reports/: tablas y graficas
- config/: configuracion

## Estado

Adquisicion automatizada y exploracion preliminar
funcionando. Procesamiento, validacion, benchmarks
y documentacion adicional en desarrollo.

## Limitaciones

Consultar docs/project_scope.md.

## Seguimiento de requisitos

Consultar docs/requirements_checklist.md.

## Ejecucion completa del pipeline

Ejecutar los siguientes comandos desde la raiz del repositorio.

### 1. Adquisicion
```powershell
python -m src.ingestion.download_data --years 2024 2025 2026
```

### 2. Exploracion preliminar
```powershell
python -m src.analysis.inspect_data
```

### 3. Procesamiento
```powershell
python -m src.processing.build_dataset
```

### 4. Validaciones
```powershell
python -m src.validation.validate_dataset
```

### 5. Pruebas automatizadas
```powershell
python -m unittest discover -s tests -v
```

### 6. Benchmark
```powershell
python -m src.analysis.benchmark
```

En Windows se puede utilizar
.\.venv\Scripts\python.exe en lugar de python.

## Resultados verificados

- Tres temporadas NBA descargadas.
- 703781 intentos de tiro procesados.
- 60 comprobaciones de calidad aprobadas.
- 8 pruebas automatizadas exitosas.
- Comparacion CSV vs Parquet ejecutada.
- Reproduccion completa verificada desde una
  copia nueva en la misma computadora.

## Documentacion

- Fuente de datos: docs/data_sources.md
- Alcance: docs/project_scope.md
- Arquitectura: docs/architecture.md
- Decisiones: docs/decisions.md
- Reproducibilidad: docs/reproducibility.md
- Validaciones: docs/validation.md
- Rendimiento: docs/performance.md
- Requisitos: docs/requirements_checklist.md

## Limitaciones

Los resultados deportivos definitivos de
Shot Selection, Hot Hand y Clutch se desarrollaran
en la siguiente etapa del proyecto.

La documentacion detalla las limitaciones de
duplicados, marcadores y cronologia.
