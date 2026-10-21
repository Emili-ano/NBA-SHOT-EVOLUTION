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

### 1. Shot Selection

¿Que zonas y tipos de lanzamiento generan mas puntos
por intento y como varian entre jugadores y equipos?

### 2. Hot Hand

¿Cambia la probabilidad de encestar despues de varios
tiros consecutivos acertados, considerando el jugador
y la dificultad aproximada del lanzamiento?

### 3. Clutch Performance

¿Como cambia la efectividad de los jugadores durante
los minutos finales de partidos cerrados?

Este tercer modulo depende de comprobar que los
marcadores y tiempos disponibles permiten identificar
correctamente el estado del partido antes de cada tiro.

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

- Porcentaje de tiros acertados (FG%)
- Puntos por intento de tiro
- Frecuencia de lanzamiento por zona
- Eficiencia por jugador y equipo
- Porcentaje de acierto despues de rachas
- Eficiencia en situaciones clutch, si es viable

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
