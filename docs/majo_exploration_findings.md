# Hallazgos de exploracion - NBA SHOT IQ

Responsable: Majo

## Alcance

Exploracion inicial de 703805 intentos de tiro de las temporadas 2023-24, 2024-25 y 2025-26.

## Resultados

- Tiros encestados: 330699.
- Tiros fallados: 373106.
- Efectividad general: 46.99 %.
- Intentos de dos puntos: 415305.
- Intentos de tres puntos: 288500.
- Distancia promedio: 14.28 pies.
- Duplicados exactos detectados: 24.

## Observaciones

Los tiros se concentran cerca del aro y alrededor de la linea de tres puntos.

La efectividad tiende a disminuir al aumentar la distancia.

Las tres temporadas tienen volumenes de tiros similares.

Las columnas score_home y score_away contienen cadenas vacias asociadas con tiros fallados.

## Limitaciones

Los resultados son descriptivos y corresponden a los datos originales, antes de eliminar duplicados.

La exploracion no demuestra relaciones causales.

Los analisis de rachas y situaciones clutch requieren procesamiento adicional.

## Evidencia

Notebook: notebooks/01_exploration.ipynb
