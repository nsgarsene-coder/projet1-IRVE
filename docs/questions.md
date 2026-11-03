# Questions analytiques (EF-01)

Questions proposées au commanditaire (SDEC Énergie, Calvados). Les colonnes ont été vérifiées
sur les fichiers téléchargés le 2026-11-03 : IRVE consolidé (schéma v2.3.1, 1 895 lignes pour
le Calvados) et populations de référence INSEE 2023 (526 communes du Calvados).

| N° | Question | Colonnes utilisées |
| --- | --- | --- |
| Q1 | Quelles communes n'ont aucune borne, ou trop peu pour 10 000 habitants (zones blanches) ? | IRVE : `code_insee_commune`, `id_pdc_itinerance` ; INSEE : `GEO` (code commune), `OBS_VALUE` avec `GEO_OBJECT = COM` et `POPREF_MEASURE = PMUN` |
| Q2 | Quelle part des bornes est lente, rapide ou ultra-rapide, et où sont les rapides ? | `puissance_nominale` (kW), `consolidated_longitude`, `consolidated_latitude`, `code_insee_commune` |
| Q3 | Combien de bornes sont mises en service chaque année, et le département avance-t-il plus ou moins vite que la France ? | `date_mise_en_service`, `code_insee_commune` (fichier national pour la comparaison) |
| Q4 | Quels opérateurs détiennent quelle part du réseau ? | `nom_operateur`, `nom_amenageur`, `id_pdc_itinerance` |
| Q5 | Quelle part des bornes est accessible à tous (voirie, 24 h/24, paiement par carte) ? | `implantation_station`, `condition_acces`, `horaires`, `paiement_cb` |

L'unité d'analyse est le point de charge (`id_pdc_itinerance`), pas la station : une station
(`id_station_itinerance`) regroupe plusieurs points de charge (`nbre_pdc`).

## Points relevés sur les colonnes (Calvados)

À traiter dans le nettoyage et à consigner dans `docs/anomalies.md` (issue #5).

| Colonne | Constat | Question touchée |
| --- | --- | --- |
| `code_insee_commune` | 5 valeurs sont des codes postaux, pas des codes INSEE (14000, 14170, 14470, 14600, 14800) ; 21 lignes ont `consolidated_is_code_insee_verified = False` | Q1 |
| `id_pdc_itinerance` | 1 894 valeurs distinctes pour 1 895 lignes : au moins un doublon | Toutes |
| `puissance_nominale` | 2 points à 0 kW ; valeurs de 0 à 400 kW | Q2 |
| `coordonneesXY` | Format texte variable (`[x,y]` avec ou sans espace) : utiliser `consolidated_longitude` et `consolidated_latitude` | Q2 |
| `date_mise_en_service` | 4,3 % de valeurs manquantes (70 % de dates lisibles seulement au niveau national) | Q3 |
| `implantation_station`, `condition_acces` | Accents abîmés dans une partie des lignes (« ŕ », « Accčs ») : mêmes catégories écrites de deux façons | Q5 |
| `paiement_cb` | Booléens écrits de 5 façons (`False`, `false`, `FALSE`, `TRUE`, `true`) et 2,3 % de manquants | Q5 |
| `horaires` | « 24/7 » parfois précédé d'un espace ; « Mo-Su 00:00-23:57 » est aussi un accès 24 h/24 | Q5 |

Pour Q2, les seuils de puissance restent à fixer et à noter dans `docs/decisions.md`
(proposition : lente ≤ 22 kW, rapide entre 22 et 150 kW exclus, ultra-rapide ≥ 150 kW).

## Historique

| Date | Version | Validé par |
| --- | --- | --- |
| 2026-10-29 | v1, proposée par l'équipe | *(en attente du commanditaire)* |
| 2026-11-03 | v2, colonnes vérifiées sur les fichiers téléchargés, département Calvados | *(en attente du commanditaire)* |
