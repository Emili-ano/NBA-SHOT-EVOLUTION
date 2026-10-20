# Guia de contribucion - NBA SHOT IQ

## Integrantes

El proyecto es desarrollado por Emiliano,
Majo y Sofia.

## Flujo de trabajo

1. Registrar una tarea en GitHub Issues.
2. Asignar un responsable.
3. Crear una rama relacionada con el issue.
4. Realizar los cambios correspondientes.
5. Ejecutar las pruebas necesarias.
6. Crear un Pull Request hacia main.
7. Solicitar una revision a otro integrante.
8. Integrar los cambios despues de revisarlos.
9. Cerrar el issue cuando la tarea este terminada.

## Convenciones de ramas

- feat/numero-descripcion
- fix/numero-descripcion
- docs/numero-descripcion
- test/numero-descripcion

## Convenciones de commits

- feat: nueva funcionalidad
- fix: correccion
- docs: documentacion
- test: pruebas
- refactor: mejora interna

## Revision de Pull Requests

Antes de aprobar un PR se debe comprobar:

- Que cumple el objetivo del issue.
- Que no elimina funcionalidades existentes.
- Que los archivos estan correctamente ubicados.
- Que las instrucciones sean reproducibles.
- Que no se incluyan contrasenas ni datos sensibles.
- Que los resultados esten sustentados por los datos.

## Ejecucion de pruebas

Desde la raiz del repositorio:

    python -m unittest discover -s tests -v

Para validar los datos procesados:

    python -m src.validation.validate_dataset

## Requisitos de participacion

Segun el PDF del proyecto, en el primer
parcial cada integrante debe tener:

- Al menos dos commits.
- Al menos un Pull Request propio.
- Al menos una revision de Pull Request.
- Participacion en al menos un issue.

En el segundo parcial deben existir:

- Issues por tarea principal.
- Ramas relacionadas con issues.
- Pull Requests revisados.
- Contribuciones tecnicas por integrante.
- Contribuciones de documentacion o validacion.
- Evidencia de integracion.

La evidencia debe corresponder a actividades
realmente realizadas y registradas.

## Datos y seguridad

Los datasets completos permanecen en data/raw/,
data/interim/ y data/processed/.

No se deben subir archivos grandes, contrasenas,
tokens ni credenciales personales.

La muestra de datos se encuentra en data/sample/.

## Integracion

La rama main contiene la version integrada
del proyecto. Los cambios se incorporan
mediante Pull Requests revisados.
