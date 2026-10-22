from pathlib import Path
import os
import pandas as pd
from databricks import sql

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "data" / "sample"
REPORTS = ROOT / "reports" / "tables"

SAMPLE.mkdir(parents=True, exist_ok=True)
REPORTS.mkdir(parents=True, exist_ok=True)


def cargar_credenciales():
    env_path = Path.home() / ".databricks.env"

    if not env_path.exists():
        raise FileNotFoundError(
            f"No se encontro el archivo de credenciales: {env_path}"
        )

    for line in env_path.read_text(
        encoding="utf-8-sig"
    ).splitlines():
        line = line.strip()

        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        os.environ[key.strip()] = (
            value.strip().strip('"').strip("'")
        )


def conectar_databricks():
    return sql.connect(
        server_hostname=os.environ["DATABRICKS_SERVER_HOSTNAME"],
        http_path=os.environ["DATABRICKS_HTTP_PATH"],
        access_token=os.environ["DATABRICKS_TOKEN"],
    )


def main():
    cargar_credenciales()

    samples = []
    profiles = []

    with conectar_databricks() as connection:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT DISTINCT season
                FROM workspace.nba_shot_iq.silver_shots
                ORDER BY season
            """)

            temporadas = [
                row[0] for row in cursor.fetchall()
            ]

            print("CONEXION EXITOSA CON DATABRICKS")
            print("TEMPORADAS DISPONIBLES:", temporadas)

            if not temporadas:
                raise ValueError(
                    "La tabla Silver no contiene temporadas."
                )

            for year in temporadas:
                print("\n" + "=" * 50)
                print(f"TEMPORADA: {year}")
                print("=" * 50)

                cursor.execute(
                    """
                    SELECT *
                    FROM workspace.nba_shot_iq.silver_shots
                    WHERE season = ?
                    """,
                    [year],
                )

                columns = [
                    column[0]
                    for column in cursor.description
                ]

                df = pd.DataFrame(
                    cursor.fetchall(),
                    columns=columns,
                )

                print("Filas:", len(df))
                print("Columnas:", len(df.columns))
                print(
                    "Duplicados exactos:",
                    df.duplicated().sum(),
                )

                if "game_id" in df.columns:
                    print(
                        "Partidos distintos:",
                        df["game_id"].nunique(),
                    )

                if "season" in df.columns:
                    print(
                        "Temporadas:",
                        df["season"].unique(),
                    )

                for column in [
                    "shot_result",
                    "shot_value",
                    "season_type_id",
                ]:
                    if column in df.columns:
                        print(
                            f"\nDistribucion de {column}:"
                        )
                        print(
                            df[column].value_counts(
                                dropna=False
                            )
                        )

                print("\nTipos de datos:")
                print(df.dtypes.to_string())

                print("\nValores faltantes:")
                print(df.isna().sum().to_string())

                for column in df.columns:
                    profiles.append({
                        "archivo": f"databricks_silver_{year}",
                        "variable": column,
                        "tipo": str(df[column].dtype),
                        "faltantes": int(
                            df[column].isna().sum()
                        ),
                        "porcentaje_faltantes": round(
                            df[column].isna().mean() * 100,
                            2,
                        ),
                    })

                if not df.empty:
                    samples.append(
                        df.sample(
                            n=min(100, len(df)),
                            random_state=42,
                        )
                    )

    if not samples:
        raise ValueError(
            "No se encontraron tiros para analizar."
        )

    sample = pd.concat(
        samples,
        ignore_index=True,
    )

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
    print("ORIGEN DE LOS DATOS: DATABRICKS SILVER")


if __name__ == "__main__":
    main()