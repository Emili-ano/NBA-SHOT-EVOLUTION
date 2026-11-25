# Requisitos de la evaluación final

Este documento reúne la evidencia que pide la rúbrica final: las cinco V, la repetición de la carga, las capas Bronze/Silver/Gold, la escala y el uso de IA.

## 1. Las cinco V de datos masivos

### Veracidad (principal)

**Reto.** La fuente tiene problemas de calidad que afectan directamente la pregunta clutch:
- 24 registros duplicados exactos (13 en 2023-24, 8 en 2024-25 y 3 en 2025-26).
- El marcador (`score_home`, `score_away`) está vacío en unos 124,000 tiros por temporada, aproximadamente el 52%. La fuente solo registra el marcador después de un enceste.
- 2,352 tiros comparten el mismo segundo de juego con otro tiro, por lo que su orden es ambiguo.

**Cómo se abordó.**
- Los duplicados se eliminan en `src/processing/build_dataset.py`.
- Las cadenas vacías del marcador se tratan como faltantes, no como cero (`docs/data_dictionary.md`, sección 7).
- Para cada tiro se estima el marcador con el último marcador conocido en un instante anterior (`src/analysis/clutch.py`, función `add_clutch_flags`).
- Los instantes ambiguos y los tiros sin marcador previo se excluyen de la comparación. Quedan 692,926 tiros comparables.
- 60 comprobaciones automáticas de calidad y 16 pruebas automatizadas.

**Dónde verificarlo.** `docs/validation.md`, `reports/tables/validation_results.csv`, `reports/tables/processing_summary.csv`, `tests/test_analysis.py` y `notebooks/03_analysis.ipynb` (sección 1).

### Volumen

**Reto.** 703,805 intentos de tiro en tres temporadas, con 19 columnas por registro.

**Cómo se abordó.** Los datos se procesan por temporada y se guardan en Parquet particionado por `season_year` (`data/processed/shot_detail/season_year=AAAA/`). En Databricks se usó PySpark con tablas Delta Bronze, Silver y Gold.

**Dónde verificarlo.** `reports/tables/processing_summary.csv`, `docs/performance.md` y `notebooks/NBA_SHOT_IQ_01_BRONZE_SILVER_GOLD.ipynb`.

### Valor

**Reto.** Que el análisis sirva para una decisión concreta: a quién darle el último tiro y qué defender en un cierre de partido.

**Cómo se abordó.** Se comparó la efectividad real en clutch contra la esperada por dificultad. Resultado: ningún jugador tiene un efecto clutch significativo tras corregir por comparaciones múltiples (0 de 162), mientras que la liga en conjunto baja 2.62 pp. Esto respalda la decisión de elegir al tirador más eficiente en general y no al que tiene fama de clutch. La herramienta interactiva convierte estos datos en propuestas ofensivas y defensivas.

**Dónde verificarlo.** `docs/final_report.md` (Resultados y Conclusiones), `reports/tables/jugadores_clutch_ajustado.csv` y `reports/figures/03_jugadores_funnel.png`.

## 2. Repetir la carga sin duplicar registros

La fuente es estática para las temporadas usadas: los archivos publicados de 2023-24 a 2025-26.

- **Descarga.** `src/ingestion/download_data.py` revisa si cada archivo ya existe con el tamaño esperado. Si existe, no lo vuelve a descargar ("Archivo existente"). Cada ejecución registra el tamaño y la huella SHA-256 en `data/raw/ingestion_manifest.json`, lo que permite comprobar que el archivo no cambió.
- **Procesamiento.** `build_dataset.py` sobrescribe las capas interim y processed en lugar de agregar filas, así que repetirlo no duplica registros.
- **Comprobación.** Se ejecutó el procesamiento dos veces seguidas. Ambas dieron 703,781 filas y la misma huella del contenido de `data/processed/shot_detail` (`ca0b7f108c64cd9e`).
- **Si la fuente se actualiza.** Un archivo con distinto tamaño se vuelve a descargar y el manifiesto registra su nueva huella. Limitación: un cambio que conserve exactamente el mismo tamaño no se detectaría; se podría resolver comparando la huella SHA-256 publicada por la fuente.

## 3. Capas Bronze, Silver y Gold

| Capa | Función | Implementación local | Implementación en Databricks |
|---|---|---|---|
| Bronze | Datos originales sin modificar | `data/raw/` (Parquet de la fuente + manifiesto) | `bronze_shots` (703,805 registros) |
| Silver | Datos limpios y tipados, sin duplicados | `data/interim/` y `data/processed/shot_detail/` (703,781) | `silver_shots` (703,781) |
| Gold | Datos listos para responder la pregunta | `data/processed/*_zone.parquet`, `reports/tables/` y `reports/analysis_summary.json` | `gold_temporadas`, `gold_zonas` y `gold_jugadores` |

## 4. Escala y decisiones técnicas

**Carga real medida** con las 3 temporadas, en un equipo de prueba con 4 núcleos y 15 GB de RAM:

| Etapa | Tiempo | Memoria pico |
|---|---|---|
| Procesamiento (`build_dataset`) | 3.2 s | 651 MB |
| Validación (`validate_dataset`) | 4.1 s | ≤ 651 MB |
| Análisis (`run_analysis`) | 18.1 s | 1,322 MB |
| Lectura CSV vs Parquet (1 temporada) | 0.93 s vs 0.09 s | 105 MB vs 112 MB |

**Qué se saturaría primero.** La etapa de análisis, porque carga las tres temporadas completas en memoria. Además, reconstruye el marcador ordenando todos los tiros de cada partido y entrena la regresión logística con más de 500,000 filas. Consume el doble de memoria que el procesamiento.

**Cambio propuesto.** Reconstruir el marcador por temporada o por partido (cada partido es independiente) o con ventanas de PySpark por `game_id`, como en el notebook de Databricks. Para el modelo, entrenar con una muestra estratificada o con Spark MLlib.

**Qué mediríamos.** El tiempo y la memoria pico de `run_analysis` con 1, 2 y 3 temporadas (y con los datos duplicados 2 y 4 veces) antes y después del cambio. Esperamos que la memoria deje de crecer con el número de temporadas al procesarlas por partes, y comprobaríamos que los resultados (43.55%, 47.16% y −2.62 pp) no cambian.

## 5. Uso de inteligencia artificial

**Sí utilizamos IA.**

- **Herramientas:** Claude (Anthropic) para el análisis final y la documentación, y ChatGPT (OpenAI) para crear la página interactiva `reports/NBA_SHOT_IQ_Clutch_Strategy.html`.
- **Caso Claude (análisis).** Le pedimos ayuda para implementar en Python local el análisis clutch que habíamos hecho en Databricks. Generó `src/analysis/clutch.py`, `src/analysis/run_analysis.py`, `tests/test_analysis.py`, `main.py`, los notebooks 03 y 04 y un primer borrador de `docs/final_report.md`.
  - **Qué aceptamos.** El código del análisis y las gráficas, después de verificarlos.
  - **Qué modificamos.** Se corrigieron títulos de gráficas que afirmaban algo incorrecto (por ejemplo, que todos los intervalos de confianza cruzaban el cero) y una prueba automatizada con un valor esperado equivocado. En las reflexiones individuales solo aceptamos correcciones de ortografía y formato, y mantuvimos nuestra redacción.
  - **Qué descartamos.** Una primera versión de `run_analysis.py` que buscaba columnas que no existen en nuestros datos y respondía una pregunta distinta (la evolución del tiro por temporada).
  - **Cómo lo verificamos.** El código reproduce exactamente las cifras de nuestro notebook de Databricks: 692,926 tiros comparables, 23,483 clutch, 43.55% de efectividad en clutch y 47.16% fuera de clutch. Las 16 pruebas automatizadas pasan, las 60 validaciones de calidad siguen aprobadas y el pipeline se ejecutó completo en un entorno limpio. El modelo se evaluó con datos apartados del entrenamiento y contra una línea base sencilla (log-loss 0.642 vs 0.692).
- **Caso ChatGPT (página HTML).** Lo usamos para generar la página con las pestañas Jugadores, Ofensiva y Defensa rival a partir de los datos agregados de nuestro pipeline. Aceptamos la estructura y el diseño de la página. Definimos nosotros la comparación contra el promedio de la NBA desde la misma distancia, el suavizado de muestras pequeñas y el mínimo de intentos por zona. Lo verificamos comprobando que los totales de la página coinciden con nuestro pipeline: 692,926 tiros comparables y 23,483 tiros clutch, con los mismos datos que `reports/tables/dashboard_data.csv`.
