# NBA SHOT IQ - Decisiones tecnicas

## Decision 1: Utilizar NBA Stats mediante SportsDataverse

### Decision
Utilizar archivos de tiros NBA publicados por
SportsDataverse y descubrirlos con GitHub REST API.

### Razon
Los datos estan organizados por temporadas y
pueden descargarse programaticamente.

### Alternativas consideradas
Consultar directamente NBA Stats o utilizar
datasets individuales de Kaggle.

### Consecuencias
Dependemos de la disponibilidad y actualizacion
de los archivos de SportsDataverse.

La API de GitHub proporciona metadatos, mientras
que los datos se descargan desde sus releases.

---

## Decision 2: Utilizar Parquet

### Decision
Almacenar los datos crudos descargados y los
procesados en formato Parquet.

### Razon
Parquet conserva tipos de datos, permite
compresion y lectura columnar.

En nuestro benchmark, la lectura de Parquet fue
aproximadamente 9.9 veces mas rapida que CSV.

### Alternativas consideradas
CSV, JSON y bases de datos relacionales.

### Consecuencias
Se requiere PyArrow.

Parquet no necesariamente consume menos memoria
en todas las operaciones.

---

## Decision 3: Arquitectura de tres capas

### Decision
Implementar RAW, INTERIM y PROCESSED.

### Razon
Separar los datos recibidos, las transformaciones
y los resultados facilita la trazabilidad.

### Alternativas consideradas
Procesar directamente los archivos descargados.

### Consecuencias
Se generan archivos intermedios adicionales,
pero cada etapa puede verificarse por separado.

---

## Decision 4: Utilizar Python y pandas

### Decision
Implementar los pipelines utilizando Python,
pandas y PyArrow.

### Razon
Son herramientas conocidas, accesibles y
suficientes para el volumen probado.

### Alternativas consideradas
PySpark, SQL y procesamiento distribuido.

### Consecuencias
El procesamiento actual depende de la memoria
de una computadora.

Para volumenes mayores podria ser necesario
procesamiento por lotes o distribuido.

---

## Decision 5: Tratamiento de duplicados

### Decision
Identificar y eliminar filas exactamente iguales
en la version actual del pipeline.

### Razon
Se encontraron 24 filas duplicadas exactamente
en las tres temporadas.

### Alternativas consideradas
Conservar todas las filas o deduplicar utilizando
una clave compuesta.

### Consecuencias
No existe un identificador unico confirmado
para cada intento de tiro.

Por lo tanto, dos eventos distintos podrian
tener atributos identicos.

Esta decision debe revisarse antes de realizar
analisis secuenciales definitivos.

---

## Decision 6: Marcadores ausentes

### Decision
Conservar los tiros cuyos marcadores aparecen
vacios y adaptar las validaciones.

### Razon
Detectamos que los marcadores ausentes se
asocian con tiros fallados en los archivos
analizados.

Eliminar estos registros produciria una
distorsion importante en los resultados.

### Alternativas consideradas
Eliminar filas incompletas o reemplazar
marcadores vacios con valores inventados.

### Consecuencias
Shot Selection y Hot Hand pueden conservar
los intentos fallados.

El modulo Clutch necesita reconstruir y
verificar el marcador anterior a cada tiro.

---

## Decision 7: Separar el pipeline del analisis final

### Decision
Construir primero un sistema reproducible de
adquisicion, procesamiento y validacion.

### Razon
El proyecto se entrega incrementalmente.

Los parciales 1 y 2 requieren una base tecnica,
datos preparados y documentacion.

### Alternativas consideradas
Comenzar directamente con visualizaciones
y conclusiones deportivas.

### Consecuencias
Los resultados definitivos del analisis clutch se
implementaron en src/analysis/run_analysis.py (examen final).

El pipeline ya permite preparar datos para
desarrollar posteriormente esos analisis.

---

## Decision 8: Definicion operativa de clutch

### Decision
Un tiro es clutch si ocurre en los ultimos 5 minutos del 4o periodo
o en tiempo extra y la diferencia estimada es de 5 puntos o menos.
El marcador se estima con el ultimo marcador conocido en un instante
anterior al tiro.

### Razon
Es la definicion usada por NBA Stats. La fuente solo registra el
marcador despues de encestes, por lo que se usa el marcador previo
para no incluir el resultado del propio tiro.

### Alternativas consideradas
Ultimos 2 minutos y 3 puntos (muy pocos tiros por jugador) y usar el
marcador del mismo registro (contamina con el resultado del tiro).

### Consecuencias
Se excluyen 2,352 tiros en instantes ambiguos y los tiros sin
marcador previo. La version pandas reproduce las cifras de Databricks.

---

## Decision 9: Regresion logistica como modelo de dificultad

### Decision
Estimar la probabilidad de enceste con regresion logistica usando
distancia en pies, valor del tiro y tipo de tiro, entrenada solo con
tiros no clutch.

### Razon
Es interpretable, rapida con 670,000 tiros y produce probabilidades
bien calibradas. Entrenar sin tiros clutch evita que el modelo
aprenda el propio efecto que se quiere medir.

### Alternativas consideradas
Promedio por rango de distancia (menos preciso), gradient boosting
(menos interpretable, mejora marginal) y modelos con jugador
(mezclarian habilidad con dificultad).

### Consecuencias
AUC de 0.66. El modelo no observa defensa ni reloj de posesion;
se documenta como limitacion.

---

## Decision 10: Correccion por comparaciones multiples

### Decision
Comparar a cada jugador contra su propio nivel ajustado fuera de
clutch y corregir los p-valores con Benjamini-Hochberg.

### Razon
Con 162 pruebas simultaneas, al 5% se esperan unos 8 falsos
positivos solo por azar.

### Alternativas consideradas
Sin correccion (infla falsos positivos) y Bonferroni (demasiado
conservador).

### Consecuencias
Ningun jugador resulta significativo. Se reportan tambien los
p-valores sin corregir para transparencia.

---

## Decision 11: Herramienta interactiva con suavizado

### Decision
Publicar una pagina HTML autocontenida con datos agregados
(reports/tables/dashboard_data.csv) y suavizar la ventaja de cada
jugador sumando 25 tiros ficticios con la efectividad de la liga.

### Razon
Permite explorar resultados sin instalar nada. El suavizado evita
que un jugador con 3 de 3 aparezca como el mejor.

### Alternativas consideradas
Dashboard en Databricks (requiere cuenta) o Streamlit (requiere
servidor).

### Consecuencias
La pagina es exploratoria: no sustituye las pruebas estadisticas del
analisis principal.

---

## Decisiones pendientes de revision

- Confirmar el identificador unico de cada tiro.
- Verificar la cronologia de eventos simultaneos.
- Reconstruir el marcador exacto con play-by-play completo
  (resuelto parcialmente con el marcador previo estimado).
- Confirmar los tipos de temporada incluidos.
- Evaluar herramientas distribuidas al escalar.

Estas decisiones se revisaran si aparecen
nuevas evidencias durante el proyecto.
