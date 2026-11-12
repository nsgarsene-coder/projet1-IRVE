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


"""Calcul des indicateurs : bornes par habitant, puissance, mises en service."""


# Q1 : zones blanches


def pdc_par_habitant(irve: pd.DataFrame, population: pd.DataFrame) -> pd.DataFrame:
    """Points de charge pour 10 000 habitants, pour chaque commune de population."""
    nb = irve.groupby("code_insee_commune")["id_pdc_itinerance"].nunique()
    nb = nb.reset_index(name="nb_pdc")
    resultat = population.merge(nb, on="code_insee_commune", how="left")
    resultat["nb_pdc"] = resultat["nb_pdc"].fillna(0).astype(int)
    resultat["pdc_10000"] = resultat["nb_pdc"] / resultat["population"] * 10000
    return resultat

    # nunique et pas size car un même point de charge peut être déclaré deux fois


# Q3 : mises en service par an


def mises_en_service_par_an(
    irve: pd.DataFrame, colonne: str = "date_mise_en_service"
) -> pd.Series:
    """Nombre de points de charge distincts mis en service chaque année.

    Les dates vides ou illisibles sont ignorées (ANO-01). Les années sans mise en
    service, entre la première et la dernière, valent 0.
    """
    annees = pd.to_datetime(irve[colonne], errors="coerce").dt.year
    nb = irve.assign(annee=annees).dropna(subset=["annee"])
    nb = nb.groupby("annee")["id_pdc_itinerance"].nunique()
    nb.index = nb.index.astype(int)
    if not nb.empty:
        nb = nb.reindex(range(nb.index.min(), nb.index.max() + 1), fill_value=0)
    return nb.rename("nb_pdc").rename_axis("annee")


def comparer_departement_france(irve: pd.DataFrame, departement: str = "14"):
    """Mises en service par an : département, France, et part du département (%).

    Le département est repéré par le début du code INSEE de la commune.
    """
    dans_dep = irve["code_insee_commune"].str.startswith(departement, na=False)
    table = pd.concat(
        {
            "departement": mises_en_service_par_an(irve[dans_dep]),
            "france": mises_en_service_par_an(irve),
        },
        axis=1,
    )
    table = table.sort_index().fillna(0).astype(int)
    table["part_departement_pct"] = table["departement"] / table["france"] * 100
    return table


def tester_h2(
    par_an: pd.Series,
    avant: tuple[int, int] = (2018, 2021),
    apres: tuple[int, int] = (2022, 2025),
    annee_en_cours: int | None = None,
) -> dict:
    """H2 : la moyenne annuelle de la période après dépasse celle de la période avant.

    Seules les années complètes sont acceptées : une période qui touche l'année en
    cours lève une erreur. Une année absente de par_an compte pour 0.
    """
    if annee_en_cours is None:
        annee_en_cours = pd.Timestamp.today().year
    if max(avant[1], apres[1]) >= annee_en_cours:
        raise ValueError("H2 ne porte que sur des années complètes.")
    moyenne_avant = par_an.reindex(range(avant[0], avant[1] + 1), fill_value=0).mean()
    moyenne_apres = par_an.reindex(range(apres[0], apres[1] + 1), fill_value=0).mean()
    return {
        "moyenne_avant": float(moyenne_avant),
        "moyenne_apres": float(moyenne_apres),
        "rapport": float(moyenne_apres / moyenne_avant) if moyenne_avant else None,
        "confirmee": bool(moyenne_apres > moyenne_avant),
    }
