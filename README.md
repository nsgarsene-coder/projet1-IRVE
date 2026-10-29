# Bornes de recharge électrique : où financer les prochaines ?

[![CI](https://github.com/nsgarsene-coder/projet1-Equipe_bornes_de_recharges/actions/workflows/ci.yml/badge.svg)](https://github.com/nsgarsene-coder/projet1-Equipe_bornes_de_recharges/actions/workflows/ci.yml)

## Contexte

- **Commanditaire** : syndicat départemental d'énergie qui prépare son schéma directeur des bornes de recharge.
- **Question posée** : « Avant de financer de nouvelles bornes, nous voulons savoir où sont les zones blanches, quelle puissance est disponible et à quel rythme le réseau s'est développé ces dernières années. »
- **Sujet retenu** : annexe A, n° 9, Bornes de recharge électrique (Projet 1 DIA2, CDC-DIA2-UE01-2026).

## Questions analytiques

Version proposée, en attente de validation par le commanditaire. Détail et historique dans
[`docs/questions.md`](docs/questions.md).

1. Quelles communes n'ont aucune borne, ou trop peu pour 10 000 habitants (zones blanches) ?
2. Quelle part des bornes est lente, rapide ou ultra-rapide, et où sont les rapides ?
3. Combien de bornes sont mises en service chaque année, et le département avance-t-il plus
   ou moins vite que la France ?
4. Quels opérateurs détiennent quelle part du réseau ?
5. Quelle part des bornes est accessible à tous (voirie, 24 h/24, paiement par carte) ?

## Données

| Source | Producteur | Licence | Date de téléchargement | Périmètre retenu |
| --- | --- | --- | --- | --- |
| [Fichier consolidé des bornes de recharge (IRVE)](https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/) | Aménageurs, consolidé par data.gouv.fr | Licence Ouverte Etalab 2.0 | *(à compléter)* | Département *(à choisir)* + comparaison nationale |
| Populations légales par commune | INSEE | Licence Ouverte Etalab 2.0 | *(à compléter)* | Communes du département |

Les données ne sont pas versionnées (`data/` est dans `.gitignore`) : elles se récupéreront avec un script de téléchargement.

## Installation

Python 3.11 ou plus.

```bash
git clone https://github.com/nsgarsene-coder/projet1-Equipe_bornes_de_recharges.git
cd projet1-Equipe_bornes_de_recharges
python -m venv .venv
source .venv/bin/activate        # Windows : .venv\Scripts\activate
pip install -r requirements-dev.txt
pre-commit install               # active les vérifications à chaque commit
```

## Vérifier avant de pousser

Les mêmes vérifications que la CI :

```bash
ruff check .
ruff format --check .
pytest
```

## Reproduire l'analyse

*(à compléter au fil du projet : téléchargement, nettoyage, notebook, tableau de bord)*

## Structure du dépôt

```
├── app/                      # tableau de bord Streamlit
├── data/raw/                 # données brutes, non versionnées
├── data/processed/           # données nettoyées, non versionnées
├── docs/                     # questions, anomalies, décisions, post-mortem
├── notebooks/                # notebook d'analyse
├── src/                      # fonctions partagées par le notebook et le tableau de bord
├── tests/                    # tests pytest des fonctions de src/
└── .github/                  # CI, modèles d'issue et de pull request
```

Ajouts par rapport à l'annexe B : `tests/`, `requirements-dev.txt`, `pyproject.toml` (configuration ruff et pytest), `.pre-commit-config.yaml`, `.github/`.

## Résultats principaux

*(Trois à cinq constats, une phrase chacun, en fin de projet.)*

## Limites

*(Principales limites des données et de l'analyse. Voir [`docs/anomalies.md`](docs/anomalies.md).)*

## Extensions de périmètre

*(Toute source ou question ajoutée, avec la date de validation par le commanditaire.)*

## Équipe

| Nom | Rôle | GitHub |
| --- | --- | --- |
| *Mohamed Ali BAMBA* | Chef de projet | |
|MALTA TENDE Gertrude Arianne | Responsable données | |
|N’SOUGAN Kossigan Arsene | Responsable dépôt | |
| Etoune Dieudonne | Responsable restitution | |

Règles de travail : [`CONTRIBUTING.md`](CONTRIBUTING.md).
