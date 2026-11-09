"""src/download.py - Téléchargement des jeux de données bruts IRVE."""

import urllib.request
from pathlib import Path

# URL officielle data.gouv.fr découpée pour respecter la limite PEP 8 (< 88 caractères)
URL_IRVE = "https://www.data.gouv.fr/fr/datasets/r/0e917d97-de04-4cc4-b4a1-ec3304b40742"


def download_irve_data(output_dir: str = "data/raw") -> Path:
    """Télécharge le fichier consolidé IRVE si absent."""
    destination_dir = Path(output_dir)
    destination_dir.mkdir(parents=True, exist_ok=True)
    destination_file = destination_dir / "irve_national.csv"

    if not destination_file.exists():
        urllib.request.urlretrieve(URL_IRVE, destination_file)

    return destination_file


if __name__ == "__main__":
    download_irve_data()
