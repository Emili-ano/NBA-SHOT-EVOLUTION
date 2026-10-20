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
Los resultados definitivos de Shot Selection,
Hot Hand y Clutch quedaran para el examen final.

El pipeline ya permite preparar datos para
desarrollar posteriormente esos analisis.

---

## Decisiones pendientes de revision

- Confirmar el identificador unico de cada tiro.
- Verificar la cronologia de eventos simultaneos.
- Reconstruir correctamente los marcadores.
- Confirmar los tipos de temporada incluidos.
- Evaluar herramientas distribuidas al escalar.

Estas decisiones se revisaran si aparecen
nuevas evidencias durante el proyecto.
