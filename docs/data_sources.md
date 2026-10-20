# Fuentes de datos - NBA SHOT IQ

## 1. Origen y responsable

La fuente original es NBA Stats (stats.nba.com),
plataforma de estadisticas de la NBA.

Los archivos utilizados por el proyecto son
distribuidos por SportsDataverse mediante
GitHub Releases en formato Parquet.

Se distingue entre:
- Fuente original: NBA Stats.
- Procesador y distribuidor: SportsDataverse.
- Consumidor academico: NBA SHOT IQ.

No se consulta directamente la API de la NBA
durante la ejecucion del proyecto.

## 2. Metodo de acceso

Repositorio:
https://github.com/sportsdataverse/sportsdataverse-data

Release:
https://github.com/sportsdataverse/sportsdataverse-data/releases/tag/nba_stats_shots

API de GitHub utilizada:
https://api.github.com/repos/sportsdataverse/sportsdataverse-data/releases/tags/nba_stats_shots

Archivos descargados:
- shots_2024.parquet: temporada 2023-24.
- shots_2025.parquet: temporada 2024-25.
- shots_2026.parquet: temporada 2025-26.

Los nombres emplean el anio de finalizacion
de la temporada.

El programa de descarga se encuentra en:
src/ingestion/download_data.py

Ejecutar desde la raiz del proyecto:

    python -m src.ingestion.download_data --years 2024 2025 2026

Los archivos originales se guardan en data/raw/.
La descarga de estos assets no requiere API key.

## 3. Formato y volumen

Formato de origen: Apache Parquet.
Unidad de analisis: un evento de intento de tiro.
Columnas originales: 19.

Temporada | Registros originales | Procesados
2023-24   | 233789               | 233776
2024-25   | 235140               | 235132
2025-26   | 234876               | 234873

Total original: 703805 registros.
Total procesado: 703781 registros.
Duplicados exactos eliminados: 24.

Estas cifras corresponden a los archivos
analizados por el equipo y pueden cambiar si
el proveedor publica nuevas versiones.

Los datasets completos no se suben a GitHub.
Se conserva una muestra en data/sample/.

## 4. Frecuencia de actualizacion

SportsDataverse dispone de procesos
automatizados de adquisicion y publicacion.

La documentacion del release indica una
programacion de NBA Stats durante buena parte
de la temporada, con ejecuciones diarias.

Una ejecucion programada no garantiza que
cada dataset sea actualizado diariamente.

Al consultar la ficha del release, se reporta
como ultima escritura de assets el 2026-10-01.

La disponibilidad, cobertura y fecha de
actualizacion deben verificarse al descargar.

Referencia:
https://github.com/sportsdataverse/sportsdataverse-data/releases/tag/nba_stats_shots

## 5. Restricciones de uso

Este proyecto utiliza datos para investigacion
y evaluacion academica no comercial.

El repositorio de SportsDataverse contiene
una licencia MIT para su software. Esta licencia
no debe interpretarse como una autorizacion
general para explotar comercialmente los
datos originales de NBA Stats.

Los terminos de NBA.com establecen condiciones
para el uso y publicacion de estadisticas:
atribucion a NBA.com, restricciones comerciales
y otras limitaciones de uso y redistribucion.

Se debe comprobar la autorizacion correspondiente
antes de reutilizar datos fuera de este proyecto.

Referencias:
https://github.com/sportsdataverse/sportsdataverse-data/blob/main/LICENSE
https://www.nba.com/termsofuse

Atribucion: NBA.com / SportsDataverse.

## 6. Variables disponibles

Las 19 variables originales son:

1. game_id: identificador de partido.
2. season: temporada registrada.
3. season_type_id: tipo de temporada.
4. period: cuarto o periodo extra.
5. clock: tiempo de juego indicado.
6. team_id: identificador de equipo.
7. team_tricode: abreviatura de equipo.
8. person_id: identificador de jugador.
9. player_name: nombre de jugador.
10. action_type: tipo de accion.
11. sub_type: subtipo de accion.
12. shot_result: acierto o fallo.
13. shot_value: valor del intento, 2 o 3.
14. shot_distance: distancia en pies.
15. x_legacy: coordenada X del tiro.
16. y_legacy: coordenada Y del tiro.
17. description: descripcion del evento.
18. score_home: marcador del local.
19. score_away: marcador del visitante.

El diccionario detallado se documentara
por separado en docs/data_dictionary.md.

Documentacion del esquema:
https://py.sportsdataverse.org/docs/nba/reference/loaders/stats-2

## 7. Problemas de calidad conocidos

### Duplicados

Se identificaron 24 filas exactamente repetidas
entre las tres temporadas utilizadas.

El procesamiento elimina duplicados exactos.
Sin un identificador unico por intento, no se
puede asegurar que todo evento repetido sea
necesariamente un error de origen.

### Marcadores faltantes

Los campos score_home y score_away pueden
contener cadenas vacias, especialmente en
intentos fallados.

No debe interpretarse una cadena vacia como
un marcador de cero.

### Interpretacion del marcador

Los marcadores asociados a un evento no
representan necesariamente el marcador previo
al tiro. Para analizar situaciones clutch se
requiere reconstruir correctamente el estado
anterior del partido.

### Tiempo y coordenadas

El campo clock debe interpretarse segun el
formato del proveedor.

Las coordenadas legacy requieren revisar
su convencion antes de construir mapas.

### Tipos de temporada

Los datos pueden incluir partidos de temporada
regular, playoffs y otros tipos. No debe
asumirse que todos son de temporada regular.

### Cambios del proveedor

El contenido de los assets puede actualizarse.
El proceso registra informacion de descarga
y conserva los archivos originales para
permitir repetir la preparacion de datos.

## 8. Reproducibilidad y trazabilidad

Descarga:
src/ingestion/download_data.py

Exploracion preliminar:
src/analysis/inspect_data.py

Procesamiento:
src/processing/build_dataset.py

Validacion:
src/validation/validate_dataset.py

Documentacion complementaria:
docs/architecture.md
docs/validation.md
docs/reproducibility.md

Flujo:

SportsDataverse
    -> data/raw/
    -> data/interim/
    -> data/processed/
    -> validacion y analisis

Los resultados se regeneran mediante los
comandos documentados en README.md.

## 9. Limitaciones del alcance

El conjunto contiene intentos de tiro de
tres temporadas especificas.

La informacion disponible no permite
demostrar por si sola causalidad deportiva.

Shot Selection, Hot Hand y Clutch requeriran
metodologias adicionales para responder
las preguntas definitivas del proyecto.
