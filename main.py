"""Ejecuta el pipeline completo de NBA SHOT IQ.

Uso:
    python main.py                 # descarga, procesa, valida y analiza
    python main.py --skip-download # si data/raw ya tiene los archivos
"""
import argparse
import subprocess
import sys

STEPS = [
    ("Adquisicion", ["-m", "src.ingestion.download_data", "--years", "2024", "2025", "2026"]),
    ("Procesamiento", ["-m", "src.processing.build_dataset"]),
    ("Validacion", ["-m", "src.validation.validate_dataset"]),
    ("Pruebas", ["-m", "unittest", "discover", "-s", "tests"]),
    ("Analisis", ["-m", "src.analysis.run_analysis"]),
]


def main():
    parser = argparse.ArgumentParser(description="Pipeline NBA SHOT IQ")
    parser.add_argument("--skip-download", action="store_true",
                        help="Omite la descarga si data/raw ya tiene los datos")
    args = parser.parse_args()

    for name, cmd in STEPS:
        if args.skip_download and name == "Adquisicion":
            print(f"\n=== {name}: omitida ===")
            continue
        print(f"\n=== {name} ===", flush=True)
        result = subprocess.run([sys.executable, *cmd])
        if result.returncode != 0:
            print(f"\n{name} fallo (codigo {result.returncode}). Pipeline detenido.")
            return result.returncode

    print("\nPipeline completo. Resultados en reports/tables y reports/figures.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
