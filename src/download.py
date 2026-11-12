"""Téléchargement des données sources (fichier IRVE consolidé, populations INSEE).

Usage : python -m src.download
"""

import csv
import zipfile
from datetime import datetime
from pathlib import Path

import requests

RACINE = Path(__file__).resolve().parent.parent
DOSSIER_BRUT = RACINE / "data" / "raw"
JOURNAL = DOSSIER_BRUT / "sources.csv"

SOURCES = {
    # Version figée : consolidation data.gouv.fr du 2026-11-12 (décision du 2026-11-12).
    # Le lien permanent du jeu (…/r/eb76d20a-…) suit la dernière consolidation et
    # changerait les chiffres à chaque téléchargement.
    "irve": {
        "url": (
            "https://static.data.gouv.fr/resources/"
            "base-nationale-des-irve-data-gouv-infrastructures-de-recharge-pour-"
            "vehicules-electriques-donnees-statiques/20261112-053200/"
            "consolidation-etalab-schema-irve-statique-v-2.3.1-20261112.csv"
        ),
        "fichier": "irve_consolide.csv",
    },
    # Populations de référence 2023, en vigueur au 1er janvier 2026.
    "insee": {
        "url": "https://api.insee.fr/melodi/file/DS_POPULATIONS_REFERENCE/DS_POPULATIONS_REFERENCE_2023_CSV_FR",
        "fichier": "insee_populations_2023.zip",
    },
}


def telecharger(url: str, destination: Path | str, timeout: int = 60) -> Path:
    """Télécharge url dans destination et renvoie le chemin du fichier écrit."""
    destination = Path(destination)
    destination.parent.mkdir(parents=True, exist_ok=True)
    # On écrit d'abord dans un .part : un téléchargement coupé ne doit pas laisser
    # un fichier incomplet qui ressemblerait à un fichier valide.
    partiel = destination.with_name(destination.name + ".part")
    try:
        with requests.get(url, stream=True, timeout=timeout) as reponse:
            reponse.raise_for_status()
            with partiel.open("wb") as f:
                for bloc in reponse.iter_content(chunk_size=1 << 20):
                    f.write(bloc)
    except BaseException:
        partiel.unlink(missing_ok=True)
        raise
    partiel.replace(destination)
    return destination


def extraire_zip(archive: Path | str, dossier: Path | str) -> list[str]:
    """Extrait l'archive dans dossier et renvoie la liste des fichiers extraits."""
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(dossier)
        return zf.namelist()


def noter_source(
    nom: str, url: str, chemin: Path | str, journal: Path | str = JOURNAL
) -> None:
    """Ajoute au journal la source, son URL, la date et la taille du fichier."""
    chemin, journal = Path(chemin), Path(journal)
    nouveau = not journal.exists() or journal.stat().st_size == 0
    with journal.open("a", newline="", encoding="utf-8") as f:
        ecrivain = csv.writer(f)
        if nouveau:
            ecrivain.writerow(["source", "url", "fichier", "date", "octets"])
        ecrivain.writerow(
            [
                nom,
                url,
                chemin.name,
                datetime.now().isoformat(timespec="seconds"),
                chemin.stat().st_size,
            ]
        )


def main() -> None:
    for nom, source in SOURCES.items():
        chemin = telecharger(source["url"], DOSSIER_BRUT / source["fichier"])
        noter_source(nom, source["url"], chemin)
        print(f"{nom} : {chemin.relative_to(RACINE)} ({chemin.stat().st_size} octets)")
        if zipfile.is_zipfile(chemin):
            print(f"  extrait : {', '.join(extraire_zip(chemin, DOSSIER_BRUT))}")


if __name__ == "__main__":
    main()
