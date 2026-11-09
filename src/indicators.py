"""Calcul des indicateurs : bornes par habitant, puissance, mises en service."""

import pandas as pd

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
