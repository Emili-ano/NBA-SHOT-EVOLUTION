from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw"
SAMPLE = ROOT / "data" / "sample"
REPORTS = ROOT / "reports" / "tables"

SAMPLE.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)

samples = []
profiles = []

for year in [2024, 2025, 2026]:
    path = RAW / f"shots_{year}.parquet"

    if not path.exists():
        raise FileNotFoundError(path)

    df = pd.read_parquet(path)

    print("\n" + "=" * 50)
    print(f"TEMPORADA: {year}")
    print("=" * 50)

    print("Filas:", len(df))
    print("Columnas:", len(df.columns))
    print("Duplicados exactos:", df.duplicated().sum())

    if "game_id" in df.columns:
        print("Partidos distintos:", df["game_id"].nunique())

    if "season" in df.columns:
        print("Temporadas:", df["season"].unique())

    for column in ["shot_result", "shot_value", "season_type_id"]:
        if column in df.columns:
            print(f"\nDistribucion de {column}:")
            print(df[column].value_counts(dropna=False))

    print("\nTipos de datos:")
    print(df.dtypes.to_string())

    print("\nValores faltantes:")
    print(df.isna().sum().to_string())

    for column in df.columns:
        profiles.append({
            "archivo": path.name,
            "variable": column,
            "tipo": str(df[column].dtype),
            "faltantes": int(df[column].isna().sum()),
            "porcentaje_faltantes": round(
                df[column].isna().mean() * 100, 2
            ),
        })

    samples.append(
        df.sample(n=min(100, len(df)), random_state=42)
    )

sample = pd.concat(samples, ignore_index=True)
sample.to_csv(
    SAMPLE / "nba_shots_sample.csv",
    index=False,
    encoding="utf-8",
)

pd.DataFrame(profiles).to_csv(
    REPORTS / "initial_profile.csv",
    index=False,
    encoding="utf-8",
)

print("\nEXPLORACION INICIAL COMPLETADA")
print("Muestra creada:", len(sample), "registros")
print("Perfil de variables guardado correctamente")
