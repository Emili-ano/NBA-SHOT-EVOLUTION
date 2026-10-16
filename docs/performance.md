# Benchmark: CSV vs Parquet

## Objetivo

Comparar lectura completa de una misma temporada NBA en dos formatos.

## Metodologia

- Dataset: tiros limpios de 2023-24.
- Tres lecturas independientes por formato.
- Se alterno el orden de los formatos.
- Tiempo: mediana de las tres lecturas.
- Memoria: mediana del incremento maximo de RSS observado por muestreo.
- Cada lectura se ejecuto en otro proceso.
- La creacion del CSV no se cronometro.

## Resultados

| Formato | Filas | Tamano MB | Tiempo s | Memoria MB |
|---|---:|---:|---:|---:|
| CSV | 233,776 | 37.85 | 0.9330 | 104.83 |
| PARQUET | 233,776 | 5.33 | 0.0939 | 112.49 |

## Interpretacion

Formato con menor mediana de tiempo: Parquet.

CSV requiere interpretar texto y tipos de datos. Parquet almacena datos en formato columnar.

La memoria es una estimacion por muestreo y no un pico exacto.

Los tiempos pueden variar por cache, hardware y procesos en segundo plano.

## Escalabilidad

Con mas temporadas, el volumen aumenta. Parquet permite lectura selectiva de columnas y particionamiento. Para confirmar el comportamiento a mayor escala se requieren mediciones adicionales.

## Comprobacion

Ambos formatos generaron iguales totales de filas, encestes y puntos.
