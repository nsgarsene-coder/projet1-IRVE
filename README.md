# Bornes de recharge électrique : où financer les prochaines ?

[![CI](https://github.com/nsgarsene-coder/projet1-IRVE/actions/workflows/ci.yml/badge.svg)](https://github.com/nsgarsene-coder/projet1-IRVE/actions/workflows/ci.yml)

## Contexte

- **Commanditaire** : SDEC Énergie, syndicat départemental d'énergies du Calvados, qui prépare son schéma directeur des bornes de recharge.
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
| [Fichier consolidé des bornes de recharge (IRVE)](https://www.data.gouv.fr/fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques/) | Aménageurs, consolidé par data.gouv.fr | Licence Ouverte Etalab 2.0 | 2026-11-12 (version figée) | Calvados (14) + comparaison nationale |
| [Populations de référence 2023, en vigueur au 1er janvier 2026](https://www.data.gouv.fr/datasets/populations-de-reference) | INSEE | Licence Ouverte Etalab 2.0 | 2026-11-03 | Communes du Calvados (population municipale) |

- **Version IRVE figée.** Le fichier consolidé est republié chaque jour. Le projet utilise la
  consolidation du **12/11/2026** (`consolidation-etalab-schema-irve-statique-v-2.3.1-20261112.csv`,
  169 279 lignes), pour que tout le monde obtienne les mêmes chiffres. Voir `docs/decisions.md`.
- **Pas de données dans Git** (`data/` est dans `.gitignore`). `python -m src.download` les
  récupère dans `data/raw/` et note l'URL, la date et la taille de chaque fichier dans
  `data/raw/sources.csv`.
- **Fichiers produits :**

| Fichier | Produit par | Contenu |
| --- | --- | --- |
| `data/raw/irve_consolide.csv` | `src.download` | Points de charge, France entière (brut) |
| `data/raw/DS_POPULATIONS_REFERENCE_2023_data.csv` | `src.download` (extrait du zip INSEE) | Populations de référence par commune |
| `data/raw/sources.csv` | `src.download` | Journal des téléchargements |
| `data/processed/irve_nettoye.parquet` | `src.cleaning` | Données nettoyées, avec la population de la commune |

## Installation

Python 3.11 ou plus. Toutes les commandes se lancent **depuis la racine du dépôt**.

```bash
git clone https://github.com/nsgarsene-coder/projet1-IRVE.git
cd projet1-IRVE
python -m venv .venv
source .venv/bin/activate        # Windows (PowerShell) : .venv\Scripts\Activate.ps1
pip install -r requirements.txt  # pour relancer l'analyse
```

Pour contribuer au code, installer en plus les outils de développement :

```bash
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

Avec l'environnement `.venv` activé, depuis la racine du dépôt, dans cet ordre :

| Étape | Commande | Résultat attendu |
| --- | --- | --- |
| 1. Télécharger les données | `python -m src.download` | `data/raw/irve_consolide.csv` (environ 118 Mo) et les populations INSEE extraites dans `data/raw/` |
| 2. Nettoyer et joindre la population | `python -m src.cleaning` | `data/processed/irve_nettoye.parquet`, avec le nombre de lignes avant et après nettoyage et le contrôle de la jointure |
| 3. Relancer l'analyse | `jupyter notebook notebooks/01_exploration.ipynb`, puis *Kernel > Restart & Run All* | Le notebook tourne de bout en bout sans erreur |
| 4. Ouvrir le tableau de bord | `streamlit run app/dashboard.py` | Le tableau de bord s'ouvre dans le navigateur (http://localhost:8501) |

Les étapes 1 et 2 ne sont à faire qu'une fois. Il faut les relancer si `data/` a été supprimé.

> ⚠️ **État au 12/11/2026** : le tableau de bord lit `data/processed/irve_calvados.parquet`,
> que le nettoyage ne produit pas encore. En attendant, il affiche des **données de
> démonstration générées au hasard**, pas les vraies bornes. Ses chiffres ne doivent pas être cités.

**En cas de problème**

- `CERTIFICATE_VERIFY_FAILED` au téléchargement : un antivirus inspecte probablement le trafic
  HTTPS (c'est le cas d'Avast). Ajoutez `data.gouv.fr`, `static.data.gouv.fr` et `api.insee.fr`
  aux exceptions de son agent Web, ou désactivez temporairement l'analyse HTTPS.
- `ModuleNotFoundError: No module named 'src'` : la commande a été lancée hors de la racine du
  dépôt, ou sans `python -m`.
- `FileNotFoundError` sur `irve_consolide.csv` ou `irve_nettoye.parquet` : l'étape précédente
  n'a pas été lancée.

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
| *Mohamed Ali BAMBA* | Chef de projet |https://github.com/Ali77225 |
|MALTA TENDE Gertrude Arianne | Responsable données |https://github.com/maltaarianne6-sudo |
|N’SOUGAN Kossigan Arsene | Responsable dépôt |https://github.com/nsgarsene-coder |
| Etoune Dieudonne | Responsable restitution |https://github.com/dicoretoune5-maker |

Règles de travail : [`CONTRIBUTING.md`](CONTRIBUTING.md).
