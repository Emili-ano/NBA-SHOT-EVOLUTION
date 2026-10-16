import argparse
import json
import statistics
import subprocess
import sys
import threading
import time
from pathlib import Path

import pandas as pd
import psutil

ROOT = Path(__file__).resolve().parents[2]
INTERIM = ROOT / "data" / "interim"
REPORTS = ROOT / "reports" / "tables"
DOCS = ROOT / "docs"

PARQUET = INTERIM / "shots_2024_clean.parquet"
CSV = INTERIM / "shots_2024_clean.csv"


def measure(fmt):
    path = CSV if fmt == "csv" else PARQUET
    process = psutil.Process()

    baseline = process.memory_info().rss
    peak = [baseline]
    stop = threading.Event()

    def monitor():
        while not stop.is_set():
            peak[0] = max(
                peak[0],
                process.memory_info().rss
            )
            stop.wait(0.005)

    thread = threading.Thread(target=monitor)
    thread.start()

    start = time.perf_counter()

    try:
        if fmt == "csv":
            text_columns = [
                "game_id", "season", "clock",
                "team_tricode", "player_name",
                "action_type", "sub_type",
                "shot_result", "description",
                "score_home", "score_away",
                "distance_band",
            ]

            df = pd.read_csv(
                path,
                dtype={
                    col: "string"
                    for col in text_columns
                },
                keep_default_na=False,
            )
        else:
            df = pd.read_parquet(path)

        elapsed = time.perf_counter() - start

    finally:
        peak[0] = max(
            peak[0],
            process.memory_info().rss
        )
        stop.set()
        thread.join()

    return {
        "format": fmt.upper(),
        "file_mb": round(
            path.stat().st_size / 1024**2, 2
        ),
        "seconds": round(elapsed, 5),
        "memory_mb": round(
            max(0, peak[0] - baseline) / 1024**2,
            2,
        ),
        "rows": len(df),
        "makes": int(df["is_made"].sum()),
        "points": int(df["points_scored"].sum()),
    }


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    if not PARQUET.exists():
        raise FileNotFoundError(
            "Primero ejecuta build_dataset.py"
        )

    print("Preparando archivos equivalentes...")

    original = pd.read_parquet(PARQUET)
    original.to_csv(CSV, index=False)

    print("Registros:", len(original))
    print("Ejecutando 3 lecturas por formato...\n")

    order = [
        "csv", "parquet",
        "parquet", "csv",
        "csv", "parquet",
    ]

    results = []

    for fmt in order:
        command = [
            sys.executable,
            "-m",
            "src.analysis.benchmark",
            "--worker",
            fmt,
        ]

        run = subprocess.run(
            command,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=True,
        )

        result = json.loads(run.stdout)
        results.append(result)

        print(
            f"{result['format']:8} "
            f"Tiempo: {result['seconds']:.4f}s | "
            f"Memoria: {result['memory_mb']:.2f}MB"
        )

    reference = {
        (r["rows"], r["makes"], r["points"])
        for r in results
    }

    if len(reference) != 1:
        raise ValueError(
            "CSV y Parquet no producen los "
            "mismos totales de control"
        )

    pd.DataFrame(results).to_csv(
        REPORTS / "benchmark_results.csv",
        index=False,
    )

    summary = {}

    for fmt in ["CSV", "PARQUET"]:
        subset = [
            r for r in results
            if r["format"] == fmt
        ]

        summary[fmt] = {
            "size": subset[0]["file_mb"],
            "time": statistics.median(
                r["seconds"] for r in subset
            ),
            "memory": statistics.median(
                r["memory_mb"] for r in subset
            ),
            "rows": subset[0]["rows"],
        }

    lines = [
        "# Benchmark: CSV vs Parquet",
        "",
        "## Objetivo",
        "",
        "Comparar lectura completa de una misma "
        "temporada NBA en dos formatos.",
        "",
        "## Metodologia",
        "",
        "- Dataset: tiros limpios de 2023-24.",
        "- Tres lecturas independientes por formato.",
        "- Se alterno el orden de los formatos.",
        "- Tiempo: mediana de las tres lecturas.",
        "- Memoria: mediana del incremento maximo "
        "de RSS observado por muestreo.",
        "- Cada lectura se ejecuto en otro proceso.",
        "- La creacion del CSV no se cronometro.",
        "",
        "## Resultados",
        "",
        "| Formato | Filas | Tamano MB | "
        "Tiempo s | Memoria MB |",
        "|---|---:|---:|---:|---:|",
    ]

    for fmt in ["CSV", "PARQUET"]:
        s = summary[fmt]

        lines.append(
            f"| {fmt} | {s['rows']:,} | "
            f"{s['size']:.2f} | "
            f"{s['time']:.4f} | "
            f"{s['memory']:.2f} |"
        )

    csv = summary["CSV"]
    parquet = summary["PARQUET"]

    faster = (
        "Parquet" if parquet["time"] < csv["time"]
        else "CSV"
    )

    lines.extend([
        "",
        "## Interpretacion",
        "",
        f"Formato con menor mediana de tiempo: {faster}.",
        "",
        "CSV requiere interpretar texto y tipos de datos. "
        "Parquet almacena datos en formato columnar.",
        "",
        "La memoria es una estimacion por muestreo "
        "y no un pico exacto.",
        "",
        "Los tiempos pueden variar por cache, "
        "hardware y procesos en segundo plano.",
        "",
        "## Escalabilidad",
        "",
        "Con mas temporadas, el volumen aumenta. "
        "Parquet permite lectura selectiva de "
        "columnas y particionamiento. Para "
        "confirmar el comportamiento a mayor "
        "escala se requieren mediciones adicionales.",
        "",
        "## Comprobacion",
        "",
        "Ambos formatos generaron iguales totales "
        "de filas, encestes y puntos.",
        "",
    ])

    (DOCS / "performance.md").write_text(
        "\n".join(lines),
        encoding="utf-8",
    )

    print("\nBENCHMARK COMPLETADO")
    print("Resultados: reports/tables/benchmark_results.csv")
    print("Informe: docs/performance.md")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--worker",
        choices=["csv", "parquet"],
    )
    args = parser.parse_args()

    if args.worker:
        print(json.dumps(measure(args.worker)))
    else:
        main()
