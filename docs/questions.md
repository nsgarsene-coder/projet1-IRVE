# Questions analytiques (EF-01)

Questions proposées au commanditaire. Les noms de colonnes sont ceux du schéma IRVE
consolidé (data.gouv.fr) ; ils seront vérifiés sur le fichier téléchargé.

| N° | Question | Colonnes utilisées |
| --- | --- | --- |
| Q1 | Quelles communes n'ont aucune borne, ou trop peu pour 10 000 habitants (zones blanches) ? | IRVE : `code_insee_commune`, `id_pdc_itinerance` ; INSEE : code commune, population municipale |
| Q2 | Quelle part des bornes est lente, rapide ou ultra-rapide, et où sont les rapides ? | `puissance_nominale`, `coordonneesXY`, `code_insee_commune` |
| Q3 | Combien de bornes sont mises en service chaque année, et le département avance-t-il plus ou moins vite que la France ? | `date_mise_en_service`, `code_insee_commune` |
| Q4 | Quels opérateurs détiennent quelle part du réseau ? | `nom_operateur`, `nom_amenageur`, `id_pdc_itinerance` |
| Q5 | Quelle part des bornes est accessible à tous (voirie, 24 h/24, paiement par carte) ? | `implantation_station`, `condition_acces`, `horaires`, `paiement_cb` |

## Historique

| Date | Version | Validé par |
| --- | --- | --- |
| 2026-10-29 | v1, proposée par l'équipe | *(en attente du commanditaire)* |
