# NBA SHOT IQ - Alcance del proyecto

## Integrantes
- Emiliano
- Majo
- Sofía

## Contexto del problema

Las estadísticas tradicionales de la NBA permiten identificar quiénes anotan más puntos y qué jugadores tienen mejores porcentajes de tiro. Sin embargo, estas métricas no siempre permiten distinguir si un jugador realmente mejora su rendimiento en los momentos decisivos o si su reputación como jugador clutch se debe a la dificultad de sus lanzamientos, al número de oportunidades y a la variación estadística.

NBA SHOT IQ propone construir una base de datos reproducible de lanzamientos de la NBA y utilizar métodos estadísticos para investigar el rendimiento de los jugadores bajo presión. El proyecto conservará el análisis de zonas, distancias y eficiencia de tiro como fundamento para evaluar si determinados jugadores superan las probabilidades esperadas de enceste en situaciones clutch.

## Pregunta principal

¿Existen jugadores de la NBA cuyo rendimiento en situaciones clutch sea estadísticamente superior al esperado, considerando la dificultad de sus lanzamientos, o las diferencias observadas pueden explicarse por la variación estadística?

## Hipótesis de investigación

**Hipótesis nula (H0):** Después de ajustar por la dificultad de los lanzamientos, no existe evidencia estadística de que determinados jugadores encesten más de lo esperado en situaciones clutch.

**Hipótesis alternativa (H1):** Algunos jugadores presentan una efectividad significativamente superior a la esperada en situaciones clutch, incluso después de considerar la dificultad de sus lanzamientos.

**Método estadístico propuesto:** Se utilizará regresión logística para estimar la probabilidad de enceste de cada lanzamiento a partir de las variables disponibles, como distancia, valor del tiro y características del jugador. Posteriormente se compararán los encestes observados con los esperados mediante análisis estadístico e intervalos de confianza.

**Condición de viabilidad:** Antes de identificar situaciones clutch, será necesario verificar que los datos de tiempo y marcador permiten reconstruir correctamente el contexto previo a cada lanzamiento. Si esta información es insuficiente, se documentarán las limitaciones y se evaluará complementar los datos con otra fuente.

## Preguntas secundarias

1. Identificación de situaciones clutch: ¿Qué lanzamientos ocurren durante los últimos cinco minutos del cuarto periodo o tiempo extra, cuando la diferencia en el marcador es de cinco puntos o menos?
2. Rendimiento esperado: ¿Qué probabilidad de enceste tiene cada lanzamiento según su distancia, valor y otras características disponibles?
3. Jugadores clutch: ¿Qué jugadores consiguen más encestes o puntos de los que estadísticamente se esperarían en situaciones de alta presión?
4. Significancia estadística: ¿Las diferencias entre el rendimiento observado y el esperado son suficientemente grandes para descartar que se deban al azar?
5. Comparación de rendimiento: ¿Los jugadores identificados como clutch presentan un rendimiento superior al de sus propios lanzamientos fuera de situaciones clutch, después de ajustar por la dificultad del tiro?

## Unidad de analisis

### ¿Que representa una fila?

Cada registro representa un intento individual de tiro
de campo realizado durante un partido de la NBA.

Un mismo jugador puede aparecer en muchos registros
y un mismo partido contiene multiples tiros.

## Alcance

Se utilizaran inicialmente las temporadas:

- 2023-24
- 2024-25
- 2025-26

El sistema permitira adquirir archivos Parquet,
almacenarlos, transformarlos, validar su calidad
y generar datasets preparados para los tres analisis.

## Metricas propuestas

* Porcentaje de acierto (FG%): proporción de lanzamientos encestados por jugador.
* Puntos por intento: promedio de puntos generados por cada lanzamiento.
* Probabilidad esperada de enceste (xFG%): probabilidad estimada mediante regresión logística según las características disponibles del tiro.
* Puntos esperados (xPTS): suma de las probabilidades de enceste multiplicadas por el valor de cada lanzamiento.
* Puntos por encima de lo esperado (PTS − xPTS): diferencia entre los puntos realmente anotados y los puntos esperados.
* Clutch FG%: porcentaje de acierto durante los últimos cinco minutos del cuarto periodo o tiempo extra, con diferencia de cinco puntos o menos.
* Clutch PTS − xPTS: puntos anotados por encima o por debajo de lo esperado específicamente en situaciones clutch.
* Significancia estadística: evaluación de si el rendimiento superior al esperado puede explicarse por la variación aleatoria, mediante intervalos de confianza y pruebas estadísticas.

Estas métricas se proponen para el análisis posterior. Su cálculo en situaciones clutch dependerá de verificar la disponibilidad y calidad de los datos temporales y del marcador.

## Fuente de datos

NBA Stats mediante archivos publicados por
SportsDataverse en GitHub Releases.

La GitHub REST API se utiliza para descubrir los
archivos y obtener sus metadatos.

## Limitaciones

- Los datos son observacionales; no demuestran causalidad.
- La distancia no representa toda la dificultad del tiro.
- No se dispone necesariamente de presion defensiva
  ni informacion completa sobre fatiga.
- Las secuencias deben verificarse cronologicamente.
- El analisis clutch depende de validar los marcadores.
- Las conclusiones se limitaran a los datos disponibles.

## Posibles usuarios

- Analistas deportivos
- Entrenadores
- Investigadores de estadistica deportiva
- Aficionados interesados en analytics

## Valor esperado

Construir una base analitica reproducible que permita
identificar patrones, evaluar hipotesis y comparar
la eficiencia de los tiros NBA mediante datos reales.

## Resultado esperado para el segundo parcial

Un pipeline ejecutable desde terminal que incluya
adquisicion, capas raw/interim/processed, validaciones,
pruebas automatizadas y mediciones de rendimiento.

Los analisis deportivos definitivos se completaran
en la etapa final del proyecto.
