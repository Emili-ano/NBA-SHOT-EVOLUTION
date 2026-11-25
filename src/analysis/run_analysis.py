"""Analisis final de NBA SHOT IQ: rendimiento clutch ajustado por dificultad.

Uso:
    python -m src.analysis.run_analysis

Requiere haber ejecutado antes:
    python -m src.ingestion.download_data --years 2024 2025 2026
    python -m src.processing.build_dataset

Genera:
    reports/tables/*.csv
    reports/figures/*.png
    reports/analysis_summary.json
"""
import json
import logging

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, log_loss
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder

from src.analysis.clutch import (
    ROOT, RANGE_ORDER, add_clutch_flags, analysis_base, benjamini_hochberg,
    load_shot_detail, two_proportion_ci,
)

TABLES = ROOT / "reports" / "tables"
FIGURES = ROOT / "reports" / "figures"
SUMMARY = ROOT / "reports" / "analysis_summary.json"

RANDOM_STATE = 42
MIN_CLUTCH_SHOTS = 50
TOP_SUB_TYPES = 15

# Paleta validada (azul / naranja) y tintas neutras.
C_NO_CLUTCH = "#257de0"
C_CLUTCH = "#f47230"
C_NEUTRAL = "#9c9c9c"
INK = "#191919"
INK_2 = "#666666"
GRID = "#e6e6e6"

plt.rcParams.update({
    "figure.dpi": 150, "savefig.dpi": 150, "font.size": 10,
    "axes.edgecolor": GRID, "axes.labelcolor": INK_2,
    "axes.titlecolor": INK, "axes.titlesize": 12, "axes.titleweight": "bold",
    "xtick.color": INK_2, "ytick.color": INK_2,
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.color": GRID, "grid.linewidth": 0.8,
    "legend.frameon": False,
})


# ----------------------------------------------------------------------
# Modelo de dificultad del tiro
# ----------------------------------------------------------------------
def shot_features(df, top_sub_types):
    distance = df["shot_distance"].clip(0, 36).astype(int).astype(str)
    sub_type = df["sub_type"].where(df["sub_type"].isin(top_sub_types), "Otro")
    return pd.DataFrame({
        "distancia_pie": distance,
        "valor": df["shot_value"].astype(str),
        "tipo": sub_type.fillna("Otro").astype(str),
    })


def fit_difficulty_model(base):
    """Regresion logistica entrenada SOLO con tiros no clutch.

    Asi la probabilidad esperada de un tiro clutch representa lo que
    encestaria un tiro equivalente fuera de la presion.
    """
    no_clutch = base[~base["clutch"]]
    top = no_clutch["sub_type"].value_counts().head(TOP_SUB_TYPES).index
    X = shot_features(no_clutch, top)
    y = no_clutch["is_made"].to_numpy()
    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.2, random_state=RANDOM_STATE, stratify=y
    )
    encoder = OneHotEncoder(handle_unknown="ignore")
    model = LogisticRegression(max_iter=1000)
    model.fit(encoder.fit_transform(X_tr), y_tr)

    p_te = model.predict_proba(encoder.transform(X_te))[:, 1]
    p_all = model.predict_proba(encoder.transform(shot_features(base, top)))[:, 1]
    metrics = {
        "auc_prueba": float(roc_auc_score(y_te, p_te)),
        "log_loss_prueba": float(log_loss(y_te, p_te)),
        "log_loss_base": float(log_loss(y_te, np.full_like(p_te, y_tr.mean()))),
        "tiros_entrenamiento": int(len(y_tr)),
        "tiros_prueba": int(len(y_te)),
    }
    clutch_mask = base["clutch"].to_numpy()
    metrics["auc_clutch"] = float(
        roc_auc_score(base.loc[clutch_mask, "is_made"], p_all[clutch_mask])
    )
    calibration = pd.DataFrame({"p": p_te, "y": y_te})
    calibration["decil"] = pd.qcut(calibration["p"], 10, labels=False, duplicates="drop")
    calibration = calibration.groupby("decil").agg(
        prob_media=("p", "mean"), acierto_real=("y", "mean"), tiros=("y", "size")
    ).reset_index()
    return p_all, metrics, calibration


# ----------------------------------------------------------------------
# Tablas
# ----------------------------------------------------------------------
def global_comparison(base):
    g = base.groupby("grupo").agg(
        tiros=("is_made", "size"), encestes=("is_made", "sum"),
        puntos=("puntos", "sum"), triples=("shot_value", lambda s: (s == 3).sum()),
        distancia_media=("shot_distance", "mean"),
        prob_esperada_media=("p_esperada", "mean"),
    )
    g["efectividad"] = g["encestes"] / g["tiros"]
    g["puntos_por_tiro"] = g["puntos"] / g["tiros"]
    g["pct_triples"] = g["triples"] / g["tiros"]
    g["diferencia_vs_esperado"] = g["efectividad"] - g["prob_esperada_media"]
    return g.reset_index()


def range_comparison(base):
    t = base.groupby(["rango_distancia", "grupo"]).agg(
        tiros=("is_made", "size"), encestes=("is_made", "sum"),
        puntos=("puntos", "sum"),
    ).reset_index()
    t["efectividad"] = t["encestes"] / t["tiros"]
    t["puntos_por_tiro"] = t["puntos"] / t["tiros"]
    t["proporcion_de_tiros"] = t["tiros"] / t.groupby("grupo")["tiros"].transform("sum")
    t["rango_distancia"] = pd.Categorical(t["rango_distancia"], RANGE_ORDER, ordered=True)
    return t.sort_values(["rango_distancia", "grupo"])


def player_table(base):
    """Por jugador: clutch observado vs esperado y vs su propio nivel."""
    base = base.assign(residuo=base["is_made"] - base["p_esperada"],
                       var=base["p_esperada"] * (1 - base["p_esperada"]))
    agg = base.groupby(["person_id", "clutch"]).agg(
        tiros=("is_made", "size"), encestes=("is_made", "sum"),
        esperados=("p_esperada", "sum"), var=("var", "sum"),
    ).unstack("clutch")
    agg.columns = [f"{m}_{'c' if c else 'nc'}" for m, c in agg.columns]
    agg = agg.dropna(subset=["tiros_c", "tiros_nc"])
    agg = agg[agg["tiros_c"] >= MIN_CLUTCH_SHOTS].copy()

    names = (base.sort_values("season")
             .groupby("person_id")
             .agg(jugador=("player_name", "last"), equipo=("team_tricode", "last")))
    agg = agg.join(names)

    # (A) Clutch vs probabilidad esperada de la liga.
    agg["efectividad_clutch"] = agg["encestes_c"] / agg["tiros_c"]
    agg["esperada_clutch"] = agg["esperados_c"] / agg["tiros_c"]
    agg["encestes_sobre_esperado"] = agg["encestes_c"] - agg["esperados_c"]
    agg["z_vs_liga"] = agg["encestes_sobre_esperado"] / np.sqrt(agg["var_c"])

    # (B) Efecto clutch propio: (obs - esp) en clutch menos (obs - esp) fuera.
    res_c = (agg["encestes_c"] - agg["esperados_c"]) / agg["tiros_c"]
    res_nc = (agg["encestes_nc"] - agg["esperados_nc"]) / agg["tiros_nc"]
    se = np.sqrt(agg["var_c"] / agg["tiros_c"] ** 2 + agg["var_nc"] / agg["tiros_nc"] ** 2)
    agg["efectividad_no_clutch"] = agg["encestes_nc"] / agg["tiros_nc"]
    agg["ventaja_ajustada_no_clutch"] = res_nc
    agg["ventaja_ajustada_clutch"] = res_c
    agg["efecto_clutch_ajustado"] = res_c - res_nc
    agg["ic95_inf"] = agg["efecto_clutch_ajustado"] - 1.96 * se
    agg["ic95_sup"] = agg["efecto_clutch_ajustado"] + 1.96 * se
    agg["z"] = agg["efecto_clutch_ajustado"] / se
    agg["p_valor"] = 2 * stats.norm.sf(agg["z"].abs())
    agg["q_valor_bh"] = benjamini_hochberg(agg["p_valor"])
    agg["significativo_bh"] = agg["q_valor_bh"] < 0.05

    cols = [
        "jugador", "equipo", "tiros_c", "encestes_c", "efectividad_clutch",
        "esperada_clutch", "encestes_sobre_esperado", "z_vs_liga",
        "tiros_nc", "efectividad_no_clutch", "ventaja_ajustada_no_clutch",
        "ventaja_ajustada_clutch", "efecto_clutch_ajustado", "ic95_inf",
        "ic95_sup", "z", "p_valor", "q_valor_bh", "significativo_bh",
    ]
    out = agg[cols].rename(columns={"tiros_c": "tiros_clutch",
                                    "encestes_c": "encestes_clutch",
                                    "tiros_nc": "tiros_no_clutch"})
    out["tiros_clutch"] = out["tiros_clutch"].astype(int)
    out["encestes_clutch"] = out["encestes_clutch"].astype(int)
    out["tiros_no_clutch"] = out["tiros_no_clutch"].astype(int)
    return out.sort_values("efecto_clutch_ajustado", ascending=False).reset_index()


def dashboard_export(base):
    """Datos agregados para reports/NBA_SHOT_IQ_Clutch_Strategy.html."""
    g = base.groupby(["season", "team_tricode", "person_id", "player_name",
                      "grupo", "rango_distancia"]).agg(
        intentos=("is_made", "size"), encestes=("is_made", "sum")).reset_index()
    return g


# ----------------------------------------------------------------------
# Figuras
# ----------------------------------------------------------------------
def pct_axis(ax, axis="y", decimals=0):
    fmt = matplotlib.ticker.PercentFormatter(1.0, decimals=decimals)
    (ax.yaxis if axis == "y" else ax.xaxis).set_major_formatter(fmt)


def fig_range(t, path):
    fig, axes = plt.subplots(1, 2, figsize=(11, 4.2))
    x = np.arange(len(RANGE_ORDER))
    w = 0.38
    for ax, col, title in [
        (axes[0], "proporcion_de_tiros", "Qué tiros se lanzan"),
        (axes[1], "efectividad", "Qué tan seguido entran"),
    ]:
        for i, (grupo, color) in enumerate([("No clutch", C_NO_CLUTCH), ("Clutch", C_CLUTCH)]):
            vals = t[t["grupo"] == grupo].set_index("rango_distancia").reindex(RANGE_ORDER)[col]
            bars = ax.bar(x + (i - 0.5) * (w + 0.02), vals, w, color=color, label=grupo)
            for b, v in zip(bars, vals):
                ax.text(b.get_x() + b.get_width() / 2, v + 0.008, f"{v:.0%}",
                        ha="center", va="bottom", fontsize=8, color=INK_2)
        ax.set_xticks(x, [f"{r} pies" for r in RANGE_ORDER])
        ax.set_title(title, loc="left")
        ax.grid(axis="x", visible=False)
        pct_axis(ax)
        ax.set_ylim(0, max(t[col]) * 1.18)
    handles, labels = axes[0].get_legend_handles_labels()
    fig.legend(handles, labels, loc="upper right", ncol=2)
    fig.suptitle("Clutch vs. no clutch por distancia", x=0.01, ha="left",
                 fontweight="bold", color=INK)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    fig.savefig(path)
    plt.close(fig)


def fig_observed_expected(g, path):
    fig, ax = plt.subplots(figsize=(7, 4))
    order = ["No clutch", "Clutch"]
    g = g.set_index("grupo").loc[order]
    y = np.arange(len(order))
    for i, grupo in enumerate(order):
        color = C_CLUTCH if grupo == "Clutch" else C_NO_CLUTCH
        obs, esp = g.loc[grupo, "efectividad"], g.loc[grupo, "prob_esperada_media"]
        ax.plot([esp, obs], [i, i], color=C_NEUTRAL, lw=2, zorder=1)
        ax.scatter(esp, i, s=70, facecolor="white", edgecolor=color, lw=2, zorder=2)
        ax.scatter(obs, i, s=70, color=color, zorder=3)
        ax.text(obs, i + 0.18, f"real {obs:.1%}", ha="center", fontsize=9, color=INK)
        ax.text(esp, i - 0.28, f"esperado {esp:.1%}", ha="center", fontsize=9, color=INK_2)
    ax.set_yticks(y, order)
    ax.set_ylim(-0.6, 1.6)
    pct_axis(ax, "x", decimals=1)
    ax.set_xlabel("Efectividad de tiro de campo")
    ax.set_title("Efectividad real vs. esperada por dificultad del tiro", loc="left")
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_funnel(players, path):
    fig, ax = plt.subplots(figsize=(8, 5))
    nominal = players["p_valor"] < 0.05
    sig = players["significativo_bh"]
    ax.scatter(players.loc[~nominal, "tiros_clutch"], players.loc[~nominal, "efecto_clutch_ajustado"],
               s=22, color=C_NO_CLUTCH, alpha=0.55, label="p ≥ 0.05")
    ax.scatter(players.loc[nominal, "tiros_clutch"], players.loc[nominal, "efecto_clutch_ajustado"],
               s=30, color=C_CLUTCH,
               label=f"p < 0.05 sin corregir ({nominal.sum()}; ~{0.05 * len(players):.0f} esperados por azar)")
    if sig.any():
        ax.scatter(players.loc[sig, "tiros_clutch"], players.loc[sig, "efecto_clutch_ajustado"],
                   s=60, facecolor="none", edgecolor=INK, lw=1.5, label="Significativo tras BH")
    ax.axhline(0, color=INK_2, lw=1)
    for _, r in players.nlargest(3, "efecto_clutch_ajustado").iterrows():
        ax.annotate(r["jugador"], (r["tiros_clutch"], r["efecto_clutch_ajustado"]),
                    xytext=(5, 3), textcoords="offset points", fontsize=8, color=INK)
    for _, r in players.nsmallest(3, "efecto_clutch_ajustado").iterrows():
        ax.annotate(r["jugador"], (r["tiros_clutch"], r["efecto_clutch_ajustado"]),
                    xytext=(5, -9), textcoords="offset points", fontsize=8, color=INK)
    pct_axis(ax)
    ax.set_xlabel("Tiros clutch del jugador")
    ax.set_ylabel("Efecto clutch ajustado (pp)")
    ax.set_title(f"{len(players)} jugadores con ≥{MIN_CLUTCH_SHOTS} tiros clutch: "
                 f"{int(sig.sum())} significativos tras corregir por comparaciones múltiples",
                 loc="left", fontsize=11)
    ax.legend(loc="upper right", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_forest(players, path, k=10):
    sel = pd.concat([players.head(k), players.tail(k)]).iloc[::-1]
    fig, ax = plt.subplots(figsize=(8, 7))
    y = np.arange(len(sel))
    colors = [C_CLUTCH if v > 0 else C_NO_CLUTCH for v in sel["efecto_clutch_ajustado"]]
    ax.hlines(y, sel["ic95_inf"], sel["ic95_sup"], color=C_NEUTRAL, lw=2)
    ax.scatter(sel["efecto_clutch_ajustado"], y, color=colors, s=40, zorder=3)
    ax.axvline(0, color=INK_2, lw=1)
    labels = [f"{j} ({e}) · {n} tiros" for j, e, n in
              zip(sel["jugador"], sel["equipo"], sel["tiros_clutch"])]
    ax.set_yticks(y, labels, fontsize=8)
    pct_axis(ax, "x")
    ax.set_xlabel("Efecto clutch ajustado con IC 95%")
    ax.set_title(f"Top y bottom {k} en efecto clutch ajustado (IC 95% sin corregir)",
                 loc="left", fontsize=11)
    ax.grid(axis="y", visible=False)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


def fig_calibration(cal, path):
    fig, ax = plt.subplots(figsize=(5.5, 5))
    ax.plot([0, 1], [0, 1], color=C_NEUTRAL, lw=1.5, ls="--", label="Calibración perfecta")
    ax.plot(cal["prob_media"], cal["acierto_real"], color=C_NO_CLUTCH, lw=2,
            marker="o", ms=7, label="Modelo (deciles)")
    pct_axis(ax)
    pct_axis(ax, "x")
    lim = (min(cal["prob_media"].min(), cal["acierto_real"].min()) - 0.05,
           max(cal["prob_media"].max(), cal["acierto_real"].max()) + 0.05)
    ax.set_xlim(lim)
    ax.set_ylim(lim)
    ax.set_xlabel("Probabilidad predicha")
    ax.set_ylabel("Acierto real")
    ax.set_title("Calibración del modelo de dificultad", loc="left")
    ax.legend(loc="upper left", fontsize=8)
    fig.tight_layout()
    fig.savefig(path)
    plt.close(fig)


# ----------------------------------------------------------------------
def main():
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    TABLES.mkdir(parents=True, exist_ok=True)
    FIGURES.mkdir(parents=True, exist_ok=True)

    logging.info("Leyendo data/processed/shot_detail")
    df = add_clutch_flags(load_shot_detail())
    base = analysis_base(df)
    logging.info("Base comparable: %s tiros (%s clutch)", f"{len(base):,}", f"{base['clutch'].sum():,}")

    logging.info("Entrenando modelo de dificultad (regresion logistica)")
    base["p_esperada"], metrics, calibration = fit_difficulty_model(base)

    g = global_comparison(base)
    c = g.set_index("grupo")
    diff, lo, hi = two_proportion_ci(c.loc["Clutch", "encestes"], c.loc["Clutch", "tiros"],
                                     c.loc["No clutch", "encestes"], c.loc["No clutch", "tiros"])

    clutch = base[base["clutch"]]
    adj = (clutch["is_made"] - clutch["p_esperada"]).mean()
    adj_se = np.sqrt((clutch["p_esperada"] * (1 - clutch["p_esperada"])).sum()) / len(clutch)
    ks = stats.ks_2samp(clutch["shot_distance"], base.loc[~base["clutch"], "shot_distance"])

    t = range_comparison(base)
    players = player_table(base)

    g.to_csv(TABLES / "clutch_vs_no_clutch.csv", index=False)
    t.to_csv(TABLES / "clutch_por_distancia.csv", index=False)
    players.to_csv(TABLES / "jugadores_clutch_ajustado.csv", index=False)
    calibration.to_csv(TABLES / "calibracion_modelo.csv", index=False)
    dashboard_export(base).to_csv(TABLES / "dashboard_data.csv", index=False)

    fig_range(t, FIGURES / "01_clutch_por_distancia.png")
    fig_observed_expected(g, FIGURES / "02_real_vs_esperado.png")
    fig_funnel(players, FIGURES / "03_jugadores_funnel.png")
    fig_forest(players, FIGURES / "04_top_bottom_jugadores.png")
    fig_calibration(calibration, FIGURES / "05_calibracion_modelo.png")

    summary = {
        "tiros_procesados": int(len(df)),
        "tiros_base_comparable": int(len(base)),
        "tiros_clutch": int(base["clutch"].sum()),
        "efectividad_clutch": float(c.loc["Clutch", "efectividad"]),
        "efectividad_no_clutch": float(c.loc["No clutch", "efectividad"]),
        "diferencia_bruta": float(diff), "diferencia_bruta_ic95": [float(lo), float(hi)],
        "esperada_clutch": float(c.loc["Clutch", "prob_esperada_media"]),
        "diferencia_ajustada_clutch": float(adj),
        "diferencia_ajustada_ic95": [float(adj - 1.96 * adj_se), float(adj + 1.96 * adj_se)],
        "puntos_por_tiro_clutch": float(c.loc["Clutch", "puntos_por_tiro"]),
        "puntos_por_tiro_no_clutch": float(c.loc["No clutch", "puntos_por_tiro"]),
        "pct_triples_clutch": float(c.loc["Clutch", "pct_triples"]),
        "pct_triples_no_clutch": float(c.loc["No clutch", "pct_triples"]),
        "ks_distancia": {"estadistico": float(ks.statistic), "p_valor": float(ks.pvalue)},
        "modelo": metrics,
        "jugadores_evaluados": int(len(players)),
        "jugadores_p_menor_005": int((players["p_valor"] < 0.05).sum()),
        "jugadores_esperados_por_azar_p005": round(0.05 * len(players), 1),
        "jugadores_significativos_bh": int(players["significativo_bh"].sum()),
        "jugadores_superan_liga_p005": int(((players["z_vs_liga"] > 1.96)).sum()),
    }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    logging.info("Efectividad clutch %.2f%% vs no clutch %.2f%% (dif %.2f pp, IC [%.2f, %.2f])",
                 100 * summary["efectividad_clutch"], 100 * summary["efectividad_no_clutch"],
                 100 * diff, 100 * lo, 100 * hi)
    logging.info("Esperada en clutch %.2f%% -> diferencia ajustada %.2f pp",
                 100 * summary["esperada_clutch"], 100 * adj)
    logging.info("Jugadores evaluados: %d | p<0.05: %d (por azar ~%.1f) | significativos BH: %d",
                 summary["jugadores_evaluados"], summary["jugadores_p_menor_005"],
                 summary["jugadores_esperados_por_azar_p005"],
                 summary["jugadores_significativos_bh"])
    logging.info("Resultados en reports/tables, reports/figures y %s", SUMMARY.name)


if __name__ == "__main__":
    main()
