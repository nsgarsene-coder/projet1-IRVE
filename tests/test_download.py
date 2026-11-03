import csv

import pytest
import requests

from src import download


class FausseReponse:
    """Remplace la réponse de requests.get : aucun appel réseau dans les tests."""

    def __init__(self, blocs, erreur=None):
        self.blocs = blocs
        self.erreur = erreur

    def __enter__(self):
        return self

    def __exit__(self, *args):
        return False

    def raise_for_status(self):
        pass

    def iter_content(self, chunk_size):
        yield from self.blocs
        if self.erreur:
            raise self.erreur


def test_telecharger_ecrit_le_fichier(tmp_path, monkeypatch):
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: FausseReponse([b"a;b\n", b"1;2\n"])
    )

    chemin = download.telecharger("https://exemple.fr/f.csv", tmp_path / "f.csv")

    assert chemin.read_bytes() == b"a;b\n1;2\n"
    assert list(tmp_path.iterdir()) == [chemin]


def test_telecharger_coupe_ne_laisse_aucun_fichier(tmp_path, monkeypatch):
    coupure = requests.ConnectionError("connexion coupée")
    monkeypatch.setattr(
        requests, "get", lambda *a, **k: FausseReponse([b"debut"], erreur=coupure)
    )

    with pytest.raises(requests.ConnectionError):
        download.telecharger("https://exemple.fr/f.csv", tmp_path / "f.csv")

    assert list(tmp_path.iterdir()) == []


def test_noter_source_ecrit_l_entete_une_seule_fois(tmp_path):
    fichier = tmp_path / "f.csv"
    fichier.write_bytes(b"12345")
    journal = tmp_path / "sources.csv"

    download.noter_source("irve", "https://exemple.fr/f.csv", fichier, journal)
    download.noter_source("irve", "https://exemple.fr/f.csv", fichier, journal)

    lignes = list(csv.reader(journal.open(encoding="utf-8")))
    assert lignes[0] == ["source", "url", "fichier", "date", "octets"]
    assert len(lignes) == 3
    assert lignes[1][:3] == ["irve", "https://exemple.fr/f.csv", "f.csv"]
    assert lignes[1][4] == "5"
