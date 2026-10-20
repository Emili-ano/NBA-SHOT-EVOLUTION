# NBA SHOT IQ - Guia de reproducibilidad

## Objetivo

Permitir que otra persona reproduzca la adquisicion,
procesamiento, validacion y pruebas del proyecto.

## Requisitos

- Windows con PowerShell
- Python compatible con requirements.txt
- Git
- Conexion a internet

El proyecto se desarrollo con Python 3.14.7.

## 1. Obtener el repositorio

Clonar el repositorio autorizado:

git clone https://github.com/Emili-ano/NBA-SHOT-EVOLUTION.git

cd NBA-SHOT-EVOLUTION

Nota: el repositorio es privado y requiere acceso.

## 2. Crear entorno virtual

py -m venv .venv

## 3. Instalar dependencias

.\.venv\Scripts\python.exe -m pip install -r requirements.txt

## 4. Descargar datos

.\.venv\Scripts\python.exe -m src.ingestion.download_data --years 2024 2025 2026

Resultado esperado:

Archivos Parquet en data/raw/.

## 5. Ejecutar exploracion preliminar

.\.venv\Scripts\python.exe -m src.analysis.inspect_data

Resultados:

- data/sample/nba_shots_sample.csv
- reports/tables/initial_profile.csv

## 6. Ejecutar procesamiento

.\.venv\Scripts\python.exe -m src.processing.build_dataset

Resultados:

- Archivos limpios en data/interim/
- Detalle de tiros en data/processed/
- Agregaciones por equipo y jugador
- reports/tables/processing_summary.csv

## 7. Ejecutar validaciones

.\.venv\Scripts\python.exe -m src.validation.validate_dataset

Resultados:

- docs/validation.md
- reports/tables/validation_results.csv

Ultima ejecucion verificada:
60 comprobaciones aprobadas, 0 fallidas.

## 8. Ejecutar pruebas automatizadas

.\.venv\Scripts\python.exe -m unittest discover -s tests -v

Ultima ejecucion verificada:
8 pruebas exitosas.

## 9. Ejecutar benchmark

.\.venv\Scripts\python.exe -m src.analysis.benchmark

Resultados:

- docs/performance.md
- reports/tables/benchmark_results.csv

## 10. Volumen esperado

Temporadas utilizadas:
2023-24, 2024-25 y 2025-26.

En la ejecucion registrada:
703781 registros procesados.

Los resultados pueden cambiar si la fuente
publica archivos actualizados.

## 11. Seguridad

No se incluyen contrasenas ni tokens.
Los datos grandes se excluyen del repositorio.
El entorno virtual no se sube a GitHub.

## 12. Limitaciones

La fuente puede cambiar con el tiempo.
El acceso depende de GitHub y SportsDataverse.
El rendimiento depende del hardware.
Los archivos completos deben descargarse.

## 13. Estado de verificacion

Los comandos se han ejecutado individualmente
en el equipo de desarrollo.

Se verifico el proyecto desde una copia nueva del
repositorio de GitHub en el mismo equipo.

Resultados:
- Instalacion de dependencias: exitosa.
- Pruebas automatizadas: 8 de 8 aprobadas.
- Adquisicion de datos: exitosa.
- Procesamiento de tres temporadas: exitoso.
- Validaciones: 60 aprobadas, 0 fallidas.
- Benchmark CSV vs Parquet: completado.

Limitacion: no se ha realizado esta prueba
en una computadora diferente.

