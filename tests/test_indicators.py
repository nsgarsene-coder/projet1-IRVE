import pandas as pd
import pytest

from src import indicators


def donnees_exemple():
    irve = pd.DataFrame(
        {
            "code_insee_commune": ["14001", "14001", "14001", "14000"],
            "id_pdc_itinerance": ["p1", "p2", "p2", "p3"],
        }
    )
    population = pd.DataFrame(
        {"code_insee_commune": ["14001", "14002"], "population": [5000, 20000]}
    )
    return irve, population


print(donnees_exemple())


def test_pdc_par_habitant_compte_un_doublon_une_seule_fois():
    irve, population = donnees_exemple()
    resultat = indicators.pdc_par_habitant(irve, population)
    par_commune = resultat.set_index("code_insee_commune")
    assert par_commune.loc["14001", "nb_pdc"] == 2
    assert par_commune.loc["14001", "pdc_10000"] == pytest.approx(4.0)


def test_pdc_par_habitant_commune_sans_borne_vaut_zero():
    irve, population = donnees_exemple()
    resultat = indicators.pdc_par_habitant(irve, population)
    par_commune = resultat.set_index("code_insee_commune")
    assert par_commune.loc["14002", "nb_pdc"] == 0
    assert par_commune.loc["14002", "pdc_10000"] == pytest.approx(0.0)


def test_pdc_par_habitant_ignore_un_code_hors_communes():
    irve, population = donnees_exemple()
    resultat = indicators.pdc_par_habitant(irve, population)
    assert len(resultat) == 2


def donnees_q3():
    return pd.DataFrame(
        {
            "id_pdc_itinerance": ["a", "a", "b", "c", "d", "e"],
            "code_insee_commune": ["14118", "14118", "14118", "75056", None, "14001"],
            "date_mise_en_service": [
                "2019-05-01",
                "2019-05-01",
                "2021-02-01",
                "2017-07-01",
                "2021-09-01",
                None,
            ],
        }
    )


def test_mises_en_service_par_an_compte_les_pdc_distincts_et_comble_les_trous():
    par_an = indicators.mises_en_service_par_an(donnees_q3())
    assert par_an.to_dict() == {2017: 1, 2018: 0, 2019: 1, 2020: 0, 2021: 2}


def test_comparer_departement_france():
    table = indicators.comparer_departement_france(donnees_q3(), "14")
    assert table.loc[2021, "departement"] == 1
    assert table.loc[2021, "france"] == 2
    assert table.loc[2021, "part_departement_pct"] == pytest.approx(50)
    assert table.loc[2017, "departement"] == 0
    assert table.loc[2020, "departement"] == 0
    assert table.index.is_monotonic_increasing


def test_tester_h2_compare_les_moyennes_annuelles():
    par_an = pd.Series({2018: 1, 2019: 1, 2020: 1, 2021: 1, 2022: 2, 2023: 2})
    res = indicators.tester_h2(par_an, annee_en_cours=2026)
    assert res["moyenne_avant"] == 1
    assert res["moyenne_apres"] == 1  # 2024 et 2025 absentes comptent pour 0
    assert res["confirmee"] is False


def test_tester_h2_refuse_une_annee_incomplete():
    with pytest.raises(ValueError):
        indicators.tester_h2(
            pd.Series(dtype=int), apres=(2022, 2026), annee_en_cours=2026
        )
