# Verificacion independiente del pipeline - Sofia

## Entorno

- Equipo: computadora de Sofia.
- Entorno: Anaconda PowerShell Prompt.
- Python: 3.12.7.
- Instalacion de dependencias en entorno virtual independiente.

## Pruebas realizadas

- Pruebas automatizadas: 8 aprobadas.
- Ingesta: tres archivos Parquet descargados.
- Exploracion: tres temporadas analizadas.
- Procesamiento: 703781 tiros limpios.
- Validacion: 60 comprobaciones aprobadas y 0 fallidas.

## Benchmark independiente

Se comparo la lectura de 233776 registros con tres repeticiones por formato.

| Formato | Mediana de lectura |
| --- | ---: |
| CSV | 1.1742 segundos |
| Parquet | 0.1533 segundos |

Parquet fue aproximadamente 7.66 veces mas rapido en esta ejecucion. La memoria utilizada por Parquet no fue menor.

## Conclusion

El pipeline pudo ejecutarse desde una segunda computadora, utilizando un entorno virtual propio. Se comprobaron los resultados de procesamiento, validacion y rendimiento.

Estos resultados corresponden al entorno y a los datos probados; no garantizan el mismo rendimiento en cualquier computadora.
