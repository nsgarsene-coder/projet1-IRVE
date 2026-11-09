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
