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


def main():
    brut = pd.read_csv(
        RACINE / "data" / "raw" / "irve_consolide.csv", dtype=str, low_memory=False
    )
    propre = nettoyer(brut)
    ecrire_parquet(propre, RACINE / "data" / "processed" / "irve_nettoye.parquet")
    print(len(brut), "->", len(propre), "lignes")


if __name__ == "__main__":
    main()
