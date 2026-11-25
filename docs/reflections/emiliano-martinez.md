# Reflexión individual - Emiliano Martínez Quijano 0269027

## ¿Cuál fue mi contribución principal?

Mi contribución principal fue construir la estructura inicial del proyecto y desarrollar el pipeline que descarga automáticamente los datos de tiros de la NBA. Organicé los archivos en las etapas raw, interim y processed, e implementé procesos de limpieza, eliminación de duplicados y validación de datos. También participé en la integración del proyecto con Databricks y en la organización de las tablas Bronze, Silver y Gold. Para la entrega final, propuse convertir nuestro análisis estadístico en una aplicación interactiva que pudiera servir a entrenadores para identificar las fortalezas de sus jugadores y las debilidades de sus rivales en situaciones clutch.

## ¿Qué decisión técnica tomé?

Una de mis decisiones principales fue automatizar la adquisición y organización de los datos en lugar de trabajar manualmente con los archivos. Esto permitió que el proceso fuera más ordenado, reproducible y fácil de actualizar con nuevas temporadas. También decidí estructurar la limpieza y las validaciones dentro del pipeline para detectar registros duplicados y problemas de calidad antes de realizar los análisis. En la aplicación final propuse incorporar comparaciones contra el promedio de la NBA desde la misma distancia, para identificar las fortalezas particulares de cada jugador y no solamente los tiros con mayor porcentaje de enceste.

## ¿Qué problema enfrenté?

Uno de los retos más importantes fue conseguir que las diferentes partes del proyecto funcionaran juntas, especialmente el código de Python, el repositorio de GitHub y las tablas de Databricks. Al principio trabajábamos con archivos y notebooks separados, pero después tuvimos que encontrar una manera de conectar nuestro programa directamente con los datos procesados. También enfrentamos problemas de registros duplicados e información incompleta del marcador, que complicaban la clasificación de los tiros clutch. Otro reto fue desarrollar una aplicación que no solo mostrara estadísticas, sino que las convirtiera en recomendaciones útiles para los entrenadores.

## ¿Qué aprendí de Git y GitHub?

Aprendí a crear y organizar un repositorio desde cero, utilizar ramas para trabajar en diferentes partes del proyecto, hacer commits y manejar pull requests para integrar cambios. También entendí cómo funcionan las revisiones de código y los issues para organizar tareas entre los integrantes. Una de las cosas más importantes que aprendí fue que GitHub no sirve únicamente para almacenar archivos, sino para mantener un historial del desarrollo y permitir que varias personas trabajen sobre un mismo proyecto sin perder sus avances.

## ¿Qué aprendí sobre trabajo colaborativo?

Aprendí que un proyecto de datos requiere que el trabajo de todos los integrantes esté conectado. Por ejemplo, el pipeline que desarrollé permitió obtener y organizar los datos que después Sofía utilizó para construir el diccionario y realizar sus pruebas, mientras que el análisis y procesamiento de la información fueron fundamentales para desarrollar nuestra aplicación final. También entendí que es importante dividir las tareas desde el principio, comunicarnos constantemente y utilizar las herramientas de GitHub para que cada integrante pueda trabajar de manera independiente sin afectar el trabajo de los demás.

## ¿Qué parte mejoraría?

Mejoraría la organización del trabajo desde el inicio, especialmente la distribución de tareas y el uso de branches e issues para que cada contribución quedara mejor documentada. En cuanto a nuestro producto final, me gustaría incorporar coordenadas exactas de los tiros y datos sobre la posición de los defensores. Actualmente nuestra aplicación identifica fortalezas según la distancia al aro, pero con información más detallada podríamos diseñar recomendaciones ofensivas y defensivas más precisas. También buscaría automatizar la actualización de la página con nuevos datos de la NBA.

## ¿Qué contribución de otro integrante fue importante?

La contribución de Sofía fue importante porque elaboró el diccionario de datos, verificó los tipos de información de cada columna y realizó pruebas del pipeline en otra computadora para comprobar su reproducibilidad. También participó en las pruebas de rendimiento entre CSV y Parquet y en la conexión con Databricks. Por otra parte, Majo contribuyó al desarrollo de nuestra página web final y a la preparación de la presentación, ayudando a transformar los resultados estadísticos en una herramienta más visual, interactiva y fácil de explicar.
