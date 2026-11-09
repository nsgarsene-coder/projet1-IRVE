"""src/download.py - Téléchargement et traçabilité des données brutes IRVE."""

import csv
from datetime import datetime, timezone
from pathlib import Path

import requests

URL_IRVE = (
    "https://www.data.gouv.fr/fr/datasets/r/"
    "0e917d97-de04-4cc4-b4a1-ec3304b40742"
)


def noter_source(
    source: str,
    url: str,
    fichier: Path | str,
    journal: Path | str = Path("data/raw/sources.csv"),
) -> None:
    """Consigne l'origine et la taille du fichier téléchargé dans le journal CSV."""
    fichier_path = Path(fichier)
    journal_path = Path(journal)
    journal_path.parent.mkdir(parents=True, exist_ok=True)

    ecrire_entete = not journal_path.exists() or journal_path.stat().st_size == 0
    taille_octets = str(fichier_path.stat().st_size) if fichier_path.exists() else "0"
    date_iso = datetime.now(timezone.utc).isoformat()

    with journal_path.open("a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        if ecrire_entete:
            writer.writerow(["source", "url", "fichier", "date", "octets"])
        writer.writerow([source, url, fichier_path.name, date_iso, taille_octets])


def telecharger(
    url: str = URL_IRVE,
    destination: Path | str = Path("data/raw/irve_national.csv"),
) -> Path:
    """Télécharge un fichier de données de manière sécurisée (streaming)."""
    destination_path = Path(destination)
    destination_path.parent.mkdir(parents=True, exist_ok=True)
    fichier_partiel = destination_path.with_suffix(".part")

    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        with fichier_partiel.open("wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)

        fichier_partiel.replace(destination_path)
    except Exception:
        if fichier_partiel.exists():
            fichier_partiel.unlink()
        if destination_path.exists():
            destination_path.unlink()
        raise

    return destination_path


def download_irve_data(output_dir: str = "data/raw") -> Path:
    """Télécharge le jeu national IRVE dans le dossier cible."""
    dest = Path(output_dir) / "irve_national.csv"
    return telecharger(URL_IRVE, dest)


if __name__ == "__main__":
    dest_path = telecharger()
    noter_source("irve", URL_IRVE, dest_path, Path("data/raw/sources.csv"))