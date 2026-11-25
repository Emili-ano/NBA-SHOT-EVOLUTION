"""Funciones del analisis clutch de NBA SHOT IQ.

Replica en pandas la definicion de clutch usada en el notebook de
Databricks (notebooks/NBA_SHOT_IQ_01_BRONZE_SILVER_GOLD.ipynb):

- ventana final: ultimos 5 minutos del 4o periodo o cualquier tiempo extra;
- marcador estimado: ultimo marcador conocido ANTES del instante del tiro;
- clutch: ventana final y diferencia estimada <= 5 puntos;
- se excluyen instantes ambiguos (varios tiros en el mismo segundo de juego)
  y tiros sin marcador estimado.
"""
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[2]
SHOT_DETAIL = ROOT / "data" / "processed" / "shot_detail"

CLUTCH_SECONDS = 300
CLUTCH_MARGIN = 5
RANGE_ORDER = ["0-4", "5-14", "15-24", "25+"]

REQUIRED_COLUMNS = [
    "game_id", "season", "period", "clock", "team_tricode",
    "person_id", "player_name", "sub_type", "shot_value",
    "shot_distance", "score_home", "score_away", "is_made",
]


def load_shot_detail(path=SHOT_DETAIL):
    """Lee las particiones season_year=AAAA/ del dataset procesado.

    Cada archivo se lee por separado porque la columna season_year
    tambien esta guardada dentro del archivo y choca con la particion.
    """
    files = sorted(Path(path).glob("season_year=*/*.parquet"))
    if not files:
        raise FileNotFoundError(
            f"No hay datos en {path}. Ejecuta antes: "
            "python -m src.processing.build_dataset"
        )
    df = pd.concat((pd.read_parquet(f) for f in files), ignore_index=True)
    missing = set(REQUIRED_COLUMNS) - set(df.columns)
    if missing:
        raise ValueError(f"Faltan columnas: {sorted(missing)}")
    return df


def clock_to_seconds(clock):
    """Convierte 'PT04M59.00S' en segundos restantes del periodo."""
    clock = clock.astype(str)
    minutes = clock.str.extract(r"PT(\d+)M", expand=False).astype(float)
    seconds = clock.str.extract(r"(\d+(?:\.\d+)?)S", expand=False).astype(float)
    return minutes.fillna(0) * 60 + seconds.fillna(0)


def elapsed_seconds(period, remaining):
    """Segundos transcurridos desde el inicio del partido."""
    regular = (period - 1) * 720 + 720 - remaining
    overtime = 2880 + (period - 5) * 300 + 300 - remaining
    return np.where(period <= 4, regular, overtime)


def distance_range(distance):
    return pd.cut(
        distance, bins=[-np.inf, 4, 14, 24, np.inf],
        labels=RANGE_ORDER,
    ).astype(str)


def add_clutch_flags(df):
    """Agrega marcador estimado, ventana final y bandera clutch."""
    df = df.copy()
    df["segundos_restantes"] = clock_to_seconds(df["clock"])
    df["tiempo_transcurrido"] = elapsed_seconds(
        df["period"].to_numpy(), df["segundos_restantes"].to_numpy()
    )

    home = pd.to_numeric(df["score_home"].replace("", np.nan), errors="coerce")
    away = pd.to_numeric(df["score_away"].replace("", np.nan), errors="coerce")
    known = pd.DataFrame({
        "game_id": df["game_id"],
        "tiempo_transcurrido": df["tiempo_transcurrido"],
        "home": home,
        "away": away,
    })

    # Un registro por instante de juego; el marcador de un instante es el
    # mayor marcador conocido en ese instante.
    instants = (
        known.groupby(["game_id", "tiempo_transcurrido"], as_index=False)
        .agg(home=("home", "max"), away=("away", "max"),
             tiros_en_instante=("home", "size"))
        .sort_values(["game_id", "tiempo_transcurrido"])
    )
    # Ultimo marcador conocido en instantes ANTERIORES (no el actual).
    by_game = instants.groupby("game_id")
    instants["home_prev"] = by_game["home"].ffill()
    instants["away_prev"] = by_game["away"].ffill()
    instants["home_prev"] = instants.groupby("game_id")["home_prev"].shift(1)
    instants["away_prev"] = instants.groupby("game_id")["away_prev"].shift(1)

    df = df.merge(
        instants[["game_id", "tiempo_transcurrido", "home_prev",
                  "away_prev", "tiros_en_instante"]],
        on=["game_id", "tiempo_transcurrido"], how="left",
    )
    df["diferencia_estimada"] = (df["home_prev"] - df["away_prev"]).abs()
    df["ventana_final"] = (
        ((df["period"] == 4) & (df["segundos_restantes"] <= CLUTCH_SECONDS))
        | (df["period"] >= 5)
    )
    df["clutch"] = df["ventana_final"] & (df["diferencia_estimada"] <= CLUTCH_MARGIN)
    df["instante_ambiguo"] = df["tiros_en_instante"] > 1
    df["rango_distancia"] = distance_range(df["shot_distance"])
    df["grupo"] = np.where(df["clutch"], "Clutch", "No clutch")
    return df


def analysis_base(df):
    """Base comparable: sin instantes ambiguos ni marcador desconocido."""
    base = df[
        ~df["instante_ambiguo"]
        & df["diferencia_estimada"].notna()
        & df["is_made"].isin([0, 1])
        & df["shot_value"].isin([2, 3])
    ].copy()
    base["is_made"] = base["is_made"].astype(int)
    base["puntos"] = base["is_made"] * base["shot_value"]
    return base


def two_proportion_ci(made_a, n_a, made_b, n_b, z=1.96):
    """Diferencia de proporciones (a - b) con IC normal al 95%."""
    p_a, p_b = made_a / n_a, made_b / n_b
    se = np.sqrt(p_a * (1 - p_a) / n_a + p_b * (1 - p_b) / n_b)
    diff = p_a - p_b
    return diff, diff - z * se, diff + z * se


def benjamini_hochberg(p_values):
    """Valores q de Benjamini-Hochberg (control de falsos descubrimientos)."""
    p = np.asarray(p_values, dtype=float)
    n = len(p)
    order = np.argsort(p)
    ranked = p[order] * n / np.arange(1, n + 1)
    q = np.minimum.accumulate(ranked[::-1])[::-1]
    out = np.empty(n)
    out[order] = np.clip(q, 0, 1)
    return out
