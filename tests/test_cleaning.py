import pandas as pd

from src.cleaning import (
    charger_population,
    controle_jointure,
    corriger_dates,
    joindre_population,
    normaliser_booleens,
    remplacer_manquants_deguises,
    supprimer_doublons,
)


def test_supprimer_doublons_garde_la_date_maj_la_plus_recente():
    df = pd.DataFrame(
        {
            "id_pdc_itinerance": ["A", "A", "B"],
            "date_maj": ["2024-01-01", "2025-01-01", "2023-01-01"],
        }
    )
    res = supprimer_doublons(df)
    assert len(res) == 2
    assert res.loc[res["id_pdc_itinerance"] == "A", "date_maj"].iloc[0] == "2025-01-01"


def test_remplacer_manquants_deguises():
    df = pd.DataFrame(
        {
            "num_pdl": ["inconnu", "0000000000000", "1.2E+13", "123"],
            "restriction_gabarit": ["x", "Aucune Restriction", "Inconnu", "non"],
        }
    )
    res = remplacer_manquants_deguises(df)
    assert res["num_pdl"].isna().sum() == 3
    assert res["restriction_gabarit"].isna().sum() == 2


def test_normaliser_booleens():
    df = pd.DataFrame({"gratuit": ["TRUE", "false", "1", "0", None]})
    res = normaliser_booleens(df, ["gratuit"])
    assert res["gratuit"].tolist()[:4] == [True, False, True, False]
    assert pd.isna(res["gratuit"].iloc[4])


def test_corriger_dates():
    df = pd.DataFrame(
        {"date_mise_en_service": ["1900-01-01", "2022-03-22", "2099-01-01", None]}
    )
    res = corriger_dates(df)
    assert res["date_mise_en_service"].isna().sum() == 3
    assert res["date_mise_en_service"].notna().sum() == 1


def test_joindre_population_et_controle():
    df = pd.DataFrame({"code_insee_commune": ["14118", "99999", None]})
    pop = pd.DataFrame({"code_insee_commune": ["14118"], "population": [100]})
    res = joindre_population(df, pop)
    assert len(res) == 3
    assert controle_jointure(res) == {
        "lignes_sans_code_insee": 1,
        "lignes_code_sans_population": 1,
        "communes_sans_correspondance": 1,
    }


def test_charger_population_garde_pmun_commune_et_arrondissement(tmp_path):
    fichier = tmp_path / "pop.csv"
    fichier.write_text(
        "GEO;GEO_OBJECT;FREQ;POPREF_MEASURE;TIME_PERIOD;OBS_VALUE\n"
        "14118;COM;A;PMUN;2023;1000\n"
        "14118;COM;A;PTOT;2023;1100\n"
        "75101;ARM;A;PMUN;2023;16000\n"
        "14;DEP;A;PMUN;2023;700000\n",
        encoding="utf-8",
    )
    res = charger_population(fichier)
    assert sorted(res["code_insee_commune"]) == ["14118", "75101"]
    assert res["population"].sum() == 17000
