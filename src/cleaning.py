from pathlib import Path

import pandas as pd

RACINE = Path(__file__).resolve().parent.parent
VALEURS_BIDON = {
    "",
    "inconnu",
    "x",
    "restriction de gabarit non précisée",
    "0000000000000",
}
COLONNES_BIDON = ["num_pdl", "restriction_gabarit"]
COLONNES_BOOLEENNES = ["paiement_cb", "gratuit", "cable_t2_attache"]
VRAI = {"true", "1"}
FAUX = {"false", "0"}


def supprimer_doublons(df, cle="id_pdc_itinerance"):
    tri = df.assign(_d=pd.to_datetime(df["date_maj"], errors="coerce"))
    tri = tri.sort_values("_d", ascending=False, na_position="last")
    return tri.drop_duplicates(cle, keep="first").drop(columns="_d").sort_index()


def remplacer_manquants_deguises(df):
    df = df.copy()
    for col in COLONNES_BIDON:
        propre = df[col].str.strip().str.lower()
        masque = propre.isin(VALEURS_BIDON)
        if col == "num_pdl":
            masque = masque | propre.str.contains("e+", regex=False, na=False)
        df.loc[masque, col] = pd.NA
    return df


def normaliser_booleens(df, colonnes=COLONNES_BOOLEENNES):
    df = df.copy()
    for col in colonnes:
        propre = df[col].str.strip().str.lower()
        df[col] = propre.map(
            lambda v: True if v in VRAI else (False if v in FAUX else pd.NA)
        ).astype("boolean")
    return df


def corriger_dates(df, colonne="date_mise_en_service"):
    df = df.copy()
    dates = pd.to_datetime(df[colonne], errors="coerce")
    invalide = (dates < "2000-01-01") | (dates > pd.Timestamp.today())
    df[colonne] = dates.mask(invalide)
    return df


def nettoyer(df):
    df = supprimer_doublons(df)
    df = remplacer_manquants_deguises(df)
    df = normaliser_booleens(df)
    return corriger_dates(df)


def ecrire_parquet(df, chemin):
    chemin = Path(chemin)
    chemin.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(chemin, index=False)


def charger_population(chemin):
    pop = pd.read_csv(chemin, sep=";", dtype=str)
    pop = pop[
        (pop["POPREF_MEASURE"] == "PMUN") & (pop["GEO_OBJECT"].isin(["COM", "ARM"]))
    ]
    pop = pop.rename(columns={"GEO": "code_insee_commune", "OBS_VALUE": "population"})
    pop["population"] = pd.to_numeric(pop["population"])
    return pop[["code_insee_commune", "population"]]


def joindre_population(df, pop):
    return df.merge(pop, on="code_insee_commune", how="left", validate="many_to_one")


def controle_jointure(df):
    sans_code = df["code_insee_commune"].isna()
    sans_pop = df["population"].isna() & ~sans_code
    return {
        "lignes_sans_code_insee": int(sans_code.sum()),
        "lignes_code_sans_population": int(sans_pop.sum()),
        "communes_sans_correspondance": int(
            df.loc[sans_pop, "code_insee_commune"].nunique()
        ),
    }


def main():
    brut = pd.read_csv(
        RACINE / "data" / "raw" / "irve_consolide.csv", dtype=str, low_memory=False
    )
    propre = nettoyer(brut)
    pop = charger_population(
        RACINE / "data" / "raw" / "DS_POPULATIONS_REFERENCE_2023_data.csv"
    )
    final = joindre_population(propre, pop)
    print(controle_jointure(final))
    ecrire_parquet(final, RACINE / "data" / "processed" / "irve_nettoye.parquet")
    print(len(brut), "->", len(final), "lignes")


if __name__ == "__main__":
    main()
