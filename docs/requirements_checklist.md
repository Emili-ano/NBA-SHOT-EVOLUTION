# NBA SHOT IQ - Control de requisitos

Basado en Proyecto Semestral de Datos Masivos.pdf.
Una casilla se marca solamente cuando existe evidencia comprobable.

## PRIMER PARCIAL

- [x] README inicial completo
- [x] Alcance y pregunta de investigacion documentados (docs/project_scope.md)
- [x] Fuente de datos completamente documentada (docs/data_sources.md)
- [x] Muestra real en data/sample/
- [x] Diccionario de datos (docs/data_dictionary.md)
- [x] Notebook 01_exploration.ipynb
- [x] Arquitectura inicial documentada (docs/architecture.md)
- [ ] Colaboracion GitHub verificada (revisar por integrante abajo)

## SEGUNDO PARCIAL

- [x] Script ejecutable de adquisicion (src/ingestion/download_data.py)
- [x] Trazabilidad de descargas (log + manifiesto SHA-256)
- [x] Datos crudos en data/raw/ (no versionados, con instrucciones)
- [x] Pipeline automatizado de procesamiento (src/processing/build_dataset.py)
- [x] Capas raw, interim y processed
- [x] Validar columnas y tipos
- [x] Validar faltantes y duplicados
- [x] Validar rangos y consistencia temporal
- [x] Validar relaciones entre capas y volumen
- [x] Documentar resultados de validacion (docs/validation.md, 60/60)
- [x] Comparacion de desempeno con tiempo y memoria (docs/performance.md)
- [x] Decisiones tecnicas documentadas (docs/decisions.md)
- [x] Pruebas automatizadas (tests/, 16 pruebas)
- [x] Arquitectura real actualizada

## EXAMEN FINAL

- [x] Pipeline completo ejecutable (python main.py)
- [x] Analisis en src/analysis/ (run_analysis.py, clutch.py)
- [x] Notebooks 03_analysis y 04_results
- [x] Tablas y figuras en reports/
- [x] Reporte final (docs/final_report.md)
- [x] README final
- [ ] Reflexion individual de Emiliano
- [ ] Reflexion individual de Majo
- [ ] Reflexion individual de Sofia
- [ ] Presentacion final (12-15 min, participan todos)

## REQUISITOS GITHUB

### Por integrante
- [ ] Al menos 2 commits
- [ ] Al menos 1 pull request propio
- [ ] Al menos 1 revision de pull request ajeno
- [ ] Participacion en al menos 1 issue
- [ ] Contribucion tecnica
- [ ] Contribucion de documentacion o validacion

### Equipo
- [ ] Issues por tareas principales
- [ ] Ramas asociadas a issues
- [ ] Pull requests revisados por otra persona
- [ ] Evidencia de integracion o resolucion de conflictos

## VERIFICACION FINAL

- [x] Ejecucion desde entorno limpio
- [x] Dependencias declaradas (requirements.txt, pyproject.toml)
- [x] Sin credenciales ni contrasenas en el codigo
- [x] Sin archivos grandes en GitHub
- [x] README con comandos de ejecucion
- [x] Resultados y limitaciones documentados
