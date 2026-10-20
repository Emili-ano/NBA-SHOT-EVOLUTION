# Diccionario de datos - NBA SHOT IQ

## 1. Descripcion del conjunto de datos

Fuente original: NBA Stats.
Distribucion: SportsDataverse.
Formato original: Apache Parquet.
Temporadas: 2023-24, 2024-25 y 2025-26.

Unidad de analisis: un registro de intento de tiro.

Los archivos originales contienen 19 columnas y
703805 registros entre las tres temporadas.

El procesamiento conserva 703781 registros
despues de eliminar 24 duplicados exactos.

## 2. Diccionario de variables originales

Los tipos indicados son tipos logicos esperados.
El tipo fisico exacto debe comprobarse en los
archivos Parquet originales.

| Variable | Tipo logico | Descripcion | Unidad | Faltantes y observaciones |
|---|---|---|---|---|
| game_id | Texto/ID | Identificador del partido | No aplica | No convertir a numero para evitar perder ceros |
| season | Texto | Temporada NBA | No aplica | Verificar formato entre temporadas |
| season_type_id | Entero/codigo | Tipo de temporada | No aplica | No asumir que todos los partidos son de temporada regular |
| period | Entero | Cuarto o periodo adicional | Periodos | Puede incluir tiempos extra |
| clock | Texto temporal | Tiempo indicado en el reloj | Minutos y segundos | Requiere conversion para calculos temporales |
| team_id | Texto/ID | Identificador del equipo | No aplica | Identificador, no medida numerica |
| team_tricode | Texto | Abreviatura del equipo | No aplica | Revisar consistencia de nombres |
| person_id | Texto/ID | Identificador del jugador | No aplica | Identificador, no medida numerica |
| player_name | Texto | Nombre del jugador | No aplica | Puede requerir normalizacion |
| action_type | Texto | Tipo de accion de tiro | No aplica | Categorias definidas por el proveedor |
| sub_type | Texto | Subtipo de accion | No aplica | Puede tener categorias diferentes |
| shot_result | Texto | Resultado del intento | No aplica | Valores como Made y Missed |
| shot_value | Entero | Valor del intento | Puntos | Valores esperados: 2 o 3 |
| shot_distance | Numerico | Distancia del lanzamiento | Pies | Verificar valores negativos o extremos |
| x_legacy | Numerico | Coordenada horizontal del tiro | Escala legacy | No asumir equivalencia directa con pies |
| y_legacy | Numerico | Coordenada vertical del tiro | Escala legacy | Revisar convencion de coordenadas |
| description | Texto | Descripcion del evento | No aplica | Texto libre |
| score_home | Texto/numerico convertible | Marcador del equipo local | Puntos | Puede contener cadenas vacias |
| score_away | Texto/numerico convertible | Marcador del visitante | Puntos | Puede contener cadenas vacias |

## 3. Valores faltantes

En los datos originales, los campos score_home
y score_away presentan cadenas vacias en
numerosos registros.

Estas cadenas deben tratarse como valores
faltantes al convertir marcadores a numeros,
no como un marcador de cero.

En el perfil inicial se observaron los siguientes
conteos de marcadores faltantes por temporada:

- 2023-24: 123093 registros.
- 2024-25: 125475 registros.
- 2025-26: 124538 registros.

Estos conteos deben contrastarse con el reporte
de exploracion y distinguirse de los nulos
fisicos del archivo Parquet.

Para las demas columnas no se declara ausencia
de faltantes sin revisar el perfil correspondiente.

## 4. Variables derivadas del procesamiento

| Variable | Tipo logico | Descripcion | Unidad | Observaciones |
|---|---|---|---|---|
| is_made | Booleano | Indica si el tiro fue acertado | No aplica | Derivada de shot_result |
| points_scored | Entero | Puntos anotados en el intento | Puntos | Cero para un intento fallado |
| season_year | Entero | Anio final de la temporada | Anios | Permite particionar los archivos |
| distance_band | Categoria | Grupo de distancia del lanzamiento | Pies | Intervalos definidos por el pipeline |

Bandas de distancia utilizadas:

- 0 a 4 pies.
- Mas de 4 a 14 pies.
- Mas de 14 a 22 pies.
- Mas de 22 pies.

## 5. Calidad y limitaciones

### Duplicados

Se identificaron 24 registros exactamente
repetidos en los tres archivos originales.

El pipeline elimina duplicados exactos, pero
la fuente no proporciona un identificador
unico de intento que permita comprobar
todos los posibles casos ambiguos.

### Marcadores

Los marcadores pueden estar ausentes.
Ademas, el marcador registrado junto al tiro
no necesariamente representa el marcador
anterior al lanzamiento.

### Cronologia

El campo clock necesita interpretarse junto
con period y game_id para ordenar eventos.

### Coordenadas

Las variables x_legacy y y_legacy utilizan
una convencion que debe verificarse antes
de elaborar mapas de tiro.

### Alcance

El conjunto contiene eventos de intentos
de tiro de tres temporadas. No permite
inferir causalidad ni responder por si solo
todas las preguntas deportivas del proyecto.

## 6. Referencias internas

- docs/data_sources.md
- docs/validation.md
- docs/architecture.md
- src/processing/build_dataset.py
- src/analysis/inspect_data.py

Los tipos fisicos, porcentajes de faltantes
y distribuciones detalladas deben contrastarse
con la exploracion ejecutada sobre los datos.
