# NBA SHOT IQ - Alcance del proyecto

## Integrantes
- Emiliano
- Majo
- Sofía

## Contexto del problema

Las estadisticas tradicionales de basketball no siempre
permiten explicar como la seleccion de tiros, las rachas
de aciertos y el contexto del partido se relacionan con
la eficiencia de los jugadores.

NBA SHOT IQ propone un sistema de ingenieria de datos
para investigar estos fenomenos utilizando registros
individuales de tiros de la NBA.

## Pregunta principal

¿Que patrones de eficiencia de tiro se observan en la NBA
y como se relacionan con la zona de lanzamiento, las
rachas de anotacion y las situaciones de cierre de partido?

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
