from pathlib import Path
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
RAW = ROOT / "data/raw"
INTERIM = ROOT / "data/interim"
PROCESSED = ROOT / "data/processed"
REPORTS = ROOT / "reports/tables"
DOCS = ROOT / "docs"

YEARS = [2024, 2025, 2026]

REQUIRED = [
    "game_id", "season", "season_type_id",
    "period", "clock", "team_tricode",
    "player_name", "shot_result", "shot_value",
    "shot_distance", "x_legacy", "y_legacy",
    "is_made", "points_scored", "season_year",
]

results = []


def check(scope, name, condition, detail):
    status = "PASS" if bool(condition) else "FAIL"
    results.append({
        "scope": scope,
        "check": name,
        "status": status,
        "detail": str(detail),
    })
    print(f"[{status}] {scope} - {name}")


def validate_season(year):
    raw = pd.read_parquet(
        RAW / f"shots_{year}.parquet"
    )
    clean = pd.read_parquet(
        INTERIM / f"shots_{year}_clean.parquet"
    )
    detail = pd.read_parquet(
        PROCESSED / "shot_detail" /
        f"season_year={year}" / "shots.parquet"
    )

    scope = str(year)

    missing_columns = sorted(
        set(REQUIRED) - set(detail.columns)
    )
    check(
        scope, "Columnas obligatorias",
        not missing_columns, missing_columns
    )

    if missing_columns:
        return

    numeric_columns = [
        "period", "shot_value", "shot_distance",
        "is_made", "points_scored", "season_year",
        "x_legacy", "y_legacy",
    ]

    invalid_types = [
        col for col in numeric_columns
        if not pd.api.types.is_numeric_dtype(detail[col])
    ]

    check(
        scope, "Tipos numericos",
        not invalid_types, invalid_types
    )

    nulls = detail[REQUIRED].isna().sum()
    check(
        scope, "Valores faltantes obligatorios",
        int(nulls.sum()) == 0,
        f"Total faltantes: {int(nulls.sum())}"
    )

    duplicates = int(raw.duplicated().sum())

    check(
        scope, "Trazabilidad de duplicados",
        len(raw) - len(clean) == duplicates,
        f"Originales={len(raw)}, duplicados={duplicates}, "
        f"interim={len(clean)}"
    )

    check(
        scope, "Duplicados exactos en processed",
        not detail.duplicated().any(),
        f"Duplicados={int(detail.duplicated().sum())}"
    )

    check(
        scope, "Consistencia interim/processed",
        clean.equals(detail),
        f"Interim={len(clean)}, processed={len(detail)}"
    )

    check(
        scope, "Valores de tiros",
        detail["shot_value"].isin([2, 3]).all(),
        "Valores permitidos: 2 y 3"
    )

    check(
        scope, "Resultado binario",
        detail["is_made"].isin([0, 1]).all(),
        "Valores permitidos: 0 y 1"
    )

    check(
        scope, "Distancias no negativas",
        detail["shot_distance"].ge(0).all(),
        "Distancia minima >= 0"
    )

    check(
        scope, "Puntos calculados",
        (
            detail["points_scored"]
            == detail["shot_value"] * detail["is_made"]
        ).all(),
        "Puntos = valor del tiro x acierto"
    )

    check(
        scope, "Temporada correcta",
        detail["season_year"].eq(year).all(),
        f"Temporada esperada: {year}"
    )

    periods = detail["period"]

    check(
        scope, "Periodos validos",
        periods.ge(1).all(),
        f"Min={periods.min()}, Max={periods.max()}"
    )

    clock_parts = (
        detail["clock"]
        .astype("string")
        .str.extract(
            r"^PT(?:(\d+)M)?(?:(\d+(?:\.\d+)?)S)?$"
        )
    )

    minutes = pd.to_numeric(
        clock_parts[0], errors="coerce"
    ).fillna(0)

    seconds = pd.to_numeric(
        clock_parts[1], errors="coerce"
    ).fillna(0)

    total_seconds = minutes * 60 + seconds

    parsed = clock_parts.notna().any(axis=1)
    valid_clock = (
        parsed
        & seconds.lt(60)
        & total_seconds.ge(0)
        & (
            ((periods <= 4) & total_seconds.le(720))
            | ((periods >= 5) & total_seconds.le(300))
        )
    )

    check(
        scope, "Consistencia temporal",
        valid_clock.all(),
        f"Relojes invalidos={int((~valid_clock).sum())}"
    )

    home = pd.to_numeric(
        detail["score_home"], errors="coerce"
    )
    away = pd.to_numeric(
        detail["score_away"], errors="coerce"
    )

    missing_home = home.isna()
    missing_away = away.isna()
    missing_scores = missing_home | missing_away

    result = (
        detail["shot_result"]
        .astype("string")
        .str.strip()
        .str.lower()
    )

    made = result.eq("made")
    missed = result.eq("missed")

    check(
        scope, "Marcadores completos por pareja",
        (missing_home == missing_away).all(),
        f"Pares incompletos: "
        f"{int((missing_home != missing_away).sum())}"
    )

    check(
        scope, "Marcadores disponibles en encestes",
        not (made & missing_scores).any(),
        f"Encestes sin marcador: "
        f"{int((made & missing_scores).sum())}"
    )

    check(
        scope, "Marcadores ausentes solo en fallos",
        not (missing_scores & ~missed).any(),
        f"Ausencias inesperadas: "
        f"{int((missing_scores & ~missed).sum())}"
    )

    valid_ranges = (
        home.between(0, 300)
        & away.between(0, 300)
    )

    invalid_present = ~missing_scores & ~valid_ranges

    check(
        scope, "Rangos de marcadores disponibles",
        not invalid_present.any(),
        f"Invalidos presentes: {int(invalid_present.sum())}; "
        f"sin marcador: {int(missing_scores.sum())}"
    )

    check(
        scope, "Volumen esperado",
        len(raw) >= 100000,
        f"Filas={len(raw)}, minimo de control=100000"
    )


def validate_aggregates():
    team = pd.read_parquet(
        PROCESSED / "shots_by_team_zone.parquet"
    )
    player = pd.read_parquet(
        PROCESSED / "shots_by_player_zone.parquet"
    )

    total_attempts = 0
    total_makes = 0
    total_points = 0

    for year in YEARS:
        detail = pd.read_parquet(
            PROCESSED / "shot_detail" /
            f"season_year={year}" / "shots.parquet"
        )
        total_attempts += len(detail)
        total_makes += int(detail["is_made"].sum())
        total_points += int(detail["points_scored"].sum())

    for name, df in [
        ("Equipos", team), ("Jugadores", player)
    ]:
        check(
            name, "Intentos entre tablas",
            int(df["attempts"].sum()) == total_attempts,
            f"Detalle={total_attempts}, "
            f"agregado={int(df['attempts'].sum())}"
        )

        check(
            name, "Encestes entre tablas",
            int(df["makes"].sum()) == total_makes,
            f"Detalle={total_makes}, "
            f"agregado={int(df['makes'].sum())}"
        )

        check(
            name, "Puntos entre tablas",
            int(df["total_points"].sum()) == total_points,
            f"Detalle={total_points}, "
            f"agregado={int(df['total_points'].sum())}"
        )

    return total_attempts


def main():
    REPORTS.mkdir(parents=True, exist_ok=True)
    DOCS.mkdir(parents=True, exist_ok=True)

    for year in YEARS:
        print(f"\nVALIDANDO TEMPORADA {year}")
        validate_season(year)

    print("\nVALIDANDO RELACIONES ENTRE TABLAS")
    total = validate_aggregates()

    report = pd.DataFrame(results)

    report.to_csv(
        REPORTS / "validation_results.csv",
        index=False,
    )

    passed = int((report["status"] == "PASS").sum())
    failed = int((report["status"] == "FAIL").sum())

    lines = [
        "# Validacion del dataset NBA SHOT IQ",
        "",
        f"- Tiros procesados: {total:,}",
        f"- Comprobaciones aprobadas: {passed}",
        f"- Comprobaciones fallidas: {failed}",
        "",
        "## Resultados",
        "",
        "| Ambito | Comprobacion | Estado | Detalle |",
        "|---|---|---|---|",
    ]

    for row in results:
        lines.append(
            f"| {row['scope']} | {row['check']} | "
            f"{row['status']} | {row['detail']} |"
        )

    lines.extend([
        "",
        "## Limitaciones",
        "",
        "- No existe un identificador unico del intento.",
        "- Los duplicados exactos requieren revision.",
        "- El orden de eventos simultaneos no esta confirmado.",
        "- Los marcadores pueden faltar en tiros fallados.",
        "- No se ha verificado si el marcador es pre o post tiro.",
        "- Estas pruebas no demuestran causalidad.",
        "",
    ])

    (DOCS / "validation.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )

    print("\nVALIDACION TERMINADA")
    print("Comprobaciones aprobadas:", passed)
    print("Comprobaciones fallidas:", failed)
    print("Reporte: docs/validation.md")

    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()

