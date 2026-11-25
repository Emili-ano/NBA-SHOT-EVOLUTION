# Reflexion individual - Sofía Villegas Sánchez 0261377

## ¿Cual fue mi contribucion principal?
    Principalmente hice el diccionario de datos y la verificación de datos y los tipos de datos en cada columna. Además hice multiples prubeas del pipeline para ver que el proyecto no solo funcionara en mi computadora o la Emiliano. Corri las validaciones, en especial las pruebas de CSV y Parquet, donde nos dimos cuanta qye en Parquet eran 7 veces más rápidas

## ¿Que decision tecnica tome?
    Tome la desicion de usar Parquet en lugar de CVS, principalmente por la rapidez que por la memoria. 
    Tambié participe en la desición de tomar las cadenas vacías del marcador como faltantes y no como cero. 

## ¿Que problema enfrente?
    El primer reto fue formular una pregunta que realmente pudiera responderse con estadística. Al principio queríamos estudiar en general la eficiencia por zona, las rachas y los cierres de partido, pero era demasiado amplio. La redujimos a si existen jugadores clutch estadísticamente superiores a lo esperado.
    En segundo lugar, no entendiamos bien como conectar el data lake de Databricks con el repositorio de Github, asi que al principio hicimos todo en Databricks y exportamos los notebooks y los subimos como archivos al repositorio. Cuando nos dimos cuenta de que esta escencial que estos estuvieran conectados tuvimos que resolverlo con una conexión en Python a Databricks SQL que lee directamente las tablas de la capa Silver.

## ¿Que aprendi de Git y GitHub?
    Aprendí como funcionan los merge de las branches con los Pull request. Al principio hice uno de mis propios pull requests pero entendi que GitHub tiene un sistema en el que podemos pedir revisión de los demás participantes de mi equipo. Tambien aprendí como hacer los commits atravez del Power Shell de mi computadora para luego escribir código en Visual Studio.  Aprendí como funcionan los issues y entendi que podemos mandar tareas a los demas integrantes con estas funciones. Personalmente entiendo github como un espacio de programacion que da multiples herramientas para trabajo colaborativo. Aprendí que en github se guarda toda laa actividad y cambios que se hacen durante el proyecto incluyendo el tiempo que se pasa editando y trabajando en el repositorio. 

## ¿Que aprendi sobre trabajo colaborativo?
    Aprendí que en un proyecto de datos el trabajo de cada integrante depende del de los demás. Por ejemplo, el diccionario de datos se construyó sobre los archivos que descargaba el pipeline de Emiliano, y mi prueba de reproducibilidad sirvió para validar su trabajo en otra computadora. Aprendí que las branches nos ayudan a haceer cambios sin crear errores que hagamos directo en la versión principal sin que antes pasen por lo demas integrantes y puedan encontrar estos errores potenciales. Aprendí que la comunicación y la planeación son my importantes para que el trabajo pueda ser más sencillo y se pueda hacere sin contratiempos. 

## ¿Que parte mejoraria?
    Tal vez si hubieramos entendido mejor como funcionaban las colaboraciones y lso commits pudimos haber trabajado más intedependientement4e. Muchas veces por las computadoras que otros integrantes tenemos eran más facil que en la computadora de emiliano manejaranos todo lo de los codigo pero ahora entiendo que para que fuera más evidente nuestra participación podiamos documentar toda nuestra participación. Entiendo que los issue ta,bien pudieron haber sido utiles si los hubieramos ud¿sado desde el principio para dividir tareas sin tener que reunirnos para ir haciendo avances. Si volviera a empezar, usaría issues, ramas y revisiones de pull requests desde el primer día, para que cada aporte quedara registrado con el nombre de quien lo hizo

## ¿Que contribucion de otro integrante fue importante?
    De Emiliano considero que  contribución más importante fue la de Emiliano al construir el pipeline base del proyecto. Desarrolló el código que descarga automáticamente los datos de la NBA, los organiza en capas (raw, interim y processed), elimina duplicados y verifica su calidad con 60 validaciones y pruebas automatizadas. Majo aporto mucho en la creación de nuestro producto final que es la página web que estamos proponiendo, muchas de las decisiones tecnicas que tomamos para el este producto fueron  tomadas por ella. Tambien colaboro mucho en la construccion del datalake una vez que nos dimos cuenta que no teniamos la conexión que era escencial. 
