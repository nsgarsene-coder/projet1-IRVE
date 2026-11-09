"""
src/indicators.py - Calculs statistiques et indicateurs métier SDIRVE.
Conforme aux exigences EF-03, EF-04, EF-07 et QC-03.
"""

import pandas as pd


def compute_kpis(df: pd.DataFrame, pop_totale: int = 700_000) -> dict[str, float]:
    """Calcule les métriques synthétiques d'en-tête pour le département (TB-01)."""
    total_pdc = len(df)
    total_stations = (
        int(df["id_station_itinerance"].nunique())
        if "id_station_itinerance" in df.columns
        else 0
    )

    if "puissance_nominale" in df.columns and total_pdc > 0:
        part_rapide = float((df["puissance_nominale"] >= 50).mean() * 100)
    else:
        part_rapide = 0.0

    ratio_10k = float((total_pdc / pop_totale) * 10_000) if pop_totale > 0 else 0.0

    return {
        "total_pdc": total_pdc,
        "total_stations": total_stations,
        "part_rapide": part_rapide,
        "ratio_10k": ratio_10k,
    }


def compute_temporal_evolution(df: pd.DataFrame) -> pd.DataFrame:
    """Agrège le nombre de mises en service par année (EF-04)."""
    if "annee_mise_en_service" not in df.columns or df.empty:
        return pd.DataFrame(columns=["annee", "nb_mises_en_service"])

    df_clean = df.dropna(subset=["annee_mise_en_service"])
    evol = (
        df_clean.groupby("annee_mise_en_service")
        .size()
        .reset_index(name="nb_mises_en_service")
        .rename(columns={"annee_mise_en_service": "annee"})
    )
    evol["annee"] = evol["annee"].astype(int)
    return evol.sort_values("annee")


def compute_power_distribution(df: pd.DataFrame) -> pd.DataFrame:
    """Calcule la proportion des points de charge par catégorie de puissance (EF-04)."""
    if "categorie_puissance" not in df.columns or df.empty:
        return pd.DataFrame(columns=["Catégorie", "Proportion"])

    dist = df["categorie_puissance"].value_counts(normalize=True).mul(100).reset_index()
    dist.columns = ["Catégorie", "Proportion"]
    return dist
