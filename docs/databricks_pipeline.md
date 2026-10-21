Pipeline Medallion en Databricks — NBA SHOT IQ

1. Objetivo

Implementar un proceso de ingesta, limpieza, transformación y análisis de datos de tiros de la NBA utilizando PySpark y la arquitectura Medallion (Bronze, Silver y Gold) en Databricks Free Edition.

El análisis comprende las temporadas 2023-24, 2024-25 y 2025-26.

2. Fuente de datos

Los archivos originales provienen de SportsDataverse y contienen registros de tiros de la NBA en formato Parquet.

Se procesaron tres archivos, correspondientes a las temporadas identificadas como 2024, 2025 y 2026.

3. Arquitectura Medallion

Bronze — Datos originales

Se conservaron los datos de entrada sin eliminar registros ni modificar las 19 columnas originales.

Resultado: 703,805 registros.

Silver — Limpieza y transformación

Se aplicaron operaciones de limpieza mediante PySpark, incluyendo la eliminación de duplicados exactos y la preparación de los datos para el análisis.

Resultados:

* Registros iniciales: 703,805.
* Duplicados exactos eliminados: 24.
* Registros resultantes: 703,781.

Los campos de marcador score_home y score_away presentan valores faltantes o vacíos en parte de los registros. No se deben interpretar automáticamente como marcadores iguales a cero.

Gold — Tablas analíticas

Se generaron tres tablas para facilitar el análisis:

* gold_temporadas: indicadores agregados por temporada.
* gold_zonas: indicadores de tiros agrupados por zona.
* gold_jugadores: indicadores agregados por jugador.

Las tablas permiten estudiar volumen de tiros, efectividad, puntos generados y distancia de lanzamiento, según las dimensiones disponibles.

4. Validación de calidad

Se ejecutaron diez comprobaciones en Databricks, con 10 resultados aprobados.

Entre las verificaciones realizadas se encuentran:

* Conservación de 703,805 registros en Bronze.
* Conservación de las 19 columnas originales.
* Obtención de 703,781 registros en Silver.
* Eliminación de 24 duplicados exactos.
* Ausencia de duplicados exactos en Silver.
* Ausencia de distancias de tiro negativas.
* Validez del indicador de enceste.
* Presencia de las tres temporadas.
* Conservación del total de intentos en la agregación Gold.
* Tres registros en la tabla Gold por temporada.

5. Resultados generales

Temporada	Intentos	Efectividad
2023-24	233,776	47.35%
2024-25	235,132	46.64%
2025-26	234,873	46.98%

Los intentos corresponden a los registros posteriores a la eliminación de duplicados exactos.

6. Decisiones y limitaciones

La eliminación de duplicados se realizó sobre registros completamente idénticos. Esta decisión debe considerarse al interpretar los resultados, ya que la fuente no proporciona necesariamente un identificador único por intento.

Los valores vacíos en los marcadores no se reemplazaron arbitrariamente por cero.

La clasificación de zonas de tiro es una transformación analítica y depende de los criterios definidos en el notebook.

Los datos se procesaron en Databricks; el repositorio de GitHub conserva el código y la documentación, mientras que los archivos originales no se incluyen en los commits.

7. Reproducibilidad y evidencia

El notebook utilizado se encuentra en:

notebooks/NBA_SHOT_IQ_01_BRONZE_SILVER_GOLD.ipynb

La implementación utiliza Databricks Free Edition, PySpark y tablas Delta.

Para reproducir el proceso es necesario contar con acceso a los archivos de origen y a un entorno Databricks con permisos para crear tablas en el esquema correspondiente.

8. Conclusión

Se implementó y ejecutó un pipeline Medallion para transformar datos originales de tiros de la NBA en conjuntos limpios y tablas analíticas.

Los resultados de Bronze, Silver y Gold fueron comprobados mediante validaciones automatizadas dentro del notebook, proporcionando evidencia técnica del procesamiento realizado.
