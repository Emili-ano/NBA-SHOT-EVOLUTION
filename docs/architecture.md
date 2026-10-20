# Arquitectura de NBA SHOT IQ

## 1. Objetivo

Construir un sistema reproducible de ingenieria
de datos para adquirir, transformar, validar y
preparar estadisticas de tiros de la NBA.

El sistema se desarrollo utilizando Python,
pandas, PyArrow, Git y GitHub.

## 2. Arquitectura propuesta - Primer parcial

Fuente NBA Stats
        |
        v
SportsDataverse
        |
        v
Adquisicion programatica
        |
        v
Datos crudos (RAW)
        |
        v
Limpieza (INTERIM)
        |
        v
Datos preparados (PROCESSED)
        |
        v
Analisis deportivo

Se propuso utilizar archivos Parquet para
facilitar el almacenamiento y procesamiento.

## 3. Arquitectura implementada - Segundo parcial

SportsDataverse / GitHub Releases
        |
        v
GitHub REST API
        |
        v
src/ingestion/download_data.py
        |
        v
data/raw/
        |
        v
src/processing/build_dataset.py
        |
        v
data/interim/
        |
        v
data/processed/
        |
        +----> src/validation/validate_dataset.py
        |                  |
        |                  v
        |          docs/validation.md
        |
        +----> src/analysis/benchmark.py
                           |
                           v
                   docs/performance.md

## 4. Adquisicion

El programa consulta la API de GitHub para
identificar los archivos publicados por
SportsDataverse.

Posteriormente descarga los archivos Parquet
correspondientes a las temporadas seleccionadas.

Se implementaron registros de descarga,
verificacion de tamanos y calculo SHA-256.

Las descargas existentes se omiten cuando su
tamano coincide con el esperado.

## 5. Almacenamiento

RAW:
Conserva los archivos descargados sin modificar.

INTERIM:
Contiene datos con tipos normalizados,
textos estandarizados y duplicados exactos
eliminados por la version actual del pipeline.

PROCESSED:
Contiene registros preparados y estadisticas
agregadas por equipo, jugador y distancia.

Los archivos grandes se excluyen de GitHub.

## 6. Procesamiento

El pipeline realiza:

- Comprobacion de columnas obligatorias.
- Conversion de variables numericas.
- Estandarizacion de nombres y equipos.
- Identificacion de duplicados exactos.
- Creacion de variables de acierto y puntos.
- Clasificacion por bandas de distancia.
- Particionamiento por temporada.
- Agregaciones por jugador y equipo.
- Exportacion a formato Parquet.

## 7. Validacion

Se implementaron comprobaciones de:

- Existencia de columnas.
- Tipos de datos.
- Valores faltantes.
- Duplicados.
- Rangos numericos.
- Consistencia temporal.
- Consistencia entre tablas.
- Volumen esperado.

La ultima ejecucion registrada obtuvo
60 comprobaciones aprobadas y 0 fallidas.

## 8. Rendimiento

Se comparo la lectura completa del mismo
dataset en CSV y Parquet.

Se midieron tiempo, memoria y tamano.

En el experimento realizado, Parquet presento
un tiempo mediano aproximadamente 9.9 veces
menor que CSV.

La memoria no necesariamente fue menor.

## 9. Escalabilidad

El procesamiento actual utiliza pandas y
carga temporadas completas en memoria.

Esto funciona para el volumen probado, pero
puede convertirse en un cuello de botella
al aumentar significativamente los registros.

Posibles mejoras:
- Procesamiento por lotes.
- Lectura selectiva de columnas.
- Particionamiento adicional.
- Herramientas de procesamiento distribuido.

## 10. Limitaciones

Los registros no tienen un identificador
unico e inequívoco para cada intento.

Los marcadores no estan disponibles
numericamente en todos los tiros.

El orden exacto de eventos simultaneos
necesita verificarse para Hot Hand.

El analisis Clutch requiere reconstruir
y verificar el estado previo del marcador.

## 11. Reproducibilidad

Los programas se ejecutan desde terminal
mediante modulos de Python.

Las dependencias se registran en
requirements.txt.

Los archivos procesados se pueden generar
de nuevo a partir de los datos crudos.

## 12. Estado

Adquisicion, procesamiento, validaciones,
pruebas basicas y benchmark implementados.

Los analisis deportivos definitivos y
el dashboard pertenecen al examen final.
