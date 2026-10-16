from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]

RAW = ROOT / "data" / "raw"
INTERIM = ROOT / "data" / "interim"
PROCESSED = ROOT / "data" / "processed"
REPORTS = ROOT / "reports" / "tables"

YEARS = [2024, 2025, 2026]

REQUIRED = [
    "game_id",
    "season",
    "season_type_id",
    "period",
    "clock",
    "team_tricode",
    "player_name",
    "shot_result",
    "shot_value",
    "shot_distance",
    "x_legacy",
    "y_legacy",
]

RESULT_MAP = {
    "made": 1,
    "missed": 0,
    "made shot": 1,
    "missed shot": 0,
    "make": 1,
    "miss": 0,
}


def prepare_shots(df, year):
    missing = set(REQUIRED) - set(df.columns)

    if missing:
        raise ValueError(
            f"Faltan columnas: {sorted(missing)}"
        )

    original_rows = len(df)
    duplicates = int(df.duplicated().sum())

    df = df.drop_duplicates().copy()

    df["season_year"] = year

    for column in ["team_tricode", "player_name"]:
        df[column] = df[column].astype("string").str.strip()

    df["team_tricode"] = df["team_tricode"].str.upper()

    result = (
        df["shot_result"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    unknown = result[~result.isin(RESULT_MAP)].unique()

    if len(unknown):
        raise ValueError(
            f"Resultados de tiro desconocidos: {list(unknown)}"
        )

    df["is_made"] = result.map(RESULT_MAP).astype("Int8")

    for column in [
        "shot_value",
        "shot_distance",
        "period",
        "x_legacy",
        "y_legacy",
    ]:
        df[column] = pd.to_numeric(
            df[column], errors="coerce"
        )

    df["points_scored"] = (
        df["is_made"] * df["shot_value"]
    )

    df["distance_band"] = pd.cut(
        df["shot_distance"],
        bins=[-0.001, 4, 14, 22, float("inf")],
        labels=[
            "0-4 ft",
            "5-14 ft",
            "15-22 ft",
            "23+ ft",
        ],
    ).astype("string")

    return df, {
        "season_year": year,
        "raw_rows": original_rows,
        "exact_duplicates": duplicates,
        "clean_rows": len(df),
        "missing_distance_band": int(
            df["distance_band"].isna().sum()
        ),
    }


def aggregate_shots(df, dimensions):
    result = (
        df.groupby(dimensions, dropna=False)
        .agg(
            attempts=("is_made", "size"),
            makes=("is_made", "sum"),
            total_points=("points_scored", "sum"),
        )
        .reset_index()
    )

    result["fg_pct"] = (
        100 * result["makes"] / result["attempts"]
    ).round(2)

    result["points_per_attempt"] = (
        result["total_points"] / result["attempts"]
    ).round(3)

    return result


def main():
    for folder in [INTERIM, PROCESSED, REPORTS]:
        folder.mkdir(parents=True, exist_ok=True)

    all_shots = []
    summaries = []

    for year in YEARS:
        source = RAW / f"shots_{year}.parquet"

        if not source.exists():
            raise FileNotFoundError(source)

        print(f"\nProcesando temporada {year}...")

        raw = pd.read_parquet(source)

        clean, summary = prepare_shots(raw, year)

        interim_path = (
            INTERIM / f"shots_{year}_clean.parquet"
        )

        clean.to_parquet(
            interim_path,
            index=False,
            compression="snappy",
        )

        detail_folder = (
            PROCESSED / "shot_detail" /
            f"season_year={year}"
        )
        detail_folder.mkdir(
            parents=True, exist_ok=True
        )

        clean.to_parquet(
            detail_folder / "shots.parquet",
            index=False,
            compression="snappy",
        )

        all_shots.append(clean)
        summaries.append(summary)

        print("Filas originales:", summary["raw_rows"])
        print("Duplicados:", summary["exact_duplicates"])
        print("Filas limpias:", summary["clean_rows"])

    combined = pd.concat(
        all_shots, ignore_index=True
    )

    shared_dimensions = [
        "season_year",
        "season_type_id",
        "distance_band",
        "shot_value",
    ]

    by_team = aggregate_shots(
        combined,
        shared_dimensions + ["team_tricode"],
    )

    by_player = aggregate_shots(
        combined,
        shared_dimensions + [
            "team_tricode", "player_name"
        ],
    )

    by_team.to_parquet(
        PROCESSED / "shots_by_team_zone.parquet",
        index=False,
    )

    by_player.to_parquet(
        PROCESSED / "shots_by_player_zone.parquet",
        index=False,
    )

    pd.DataFrame(summaries).to_csv(
        REPORTS / "processing_summary.csv",
        index=False,
    )

    print("\nPIPELINE COMPLETADO")
    print("Total de tiros procesados:", len(combined))
    print("Registros agrupados por equipo:", len(by_team))
    print("Registros agrupados por jugador:", len(by_player))
    print("Capas INTERIM y PROCESSED generadas")


if __name__ == "__main__":
    main()
