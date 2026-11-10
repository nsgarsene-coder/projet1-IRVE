import pandas as pd

from src.cleaning import (
    corriger_dates,
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
