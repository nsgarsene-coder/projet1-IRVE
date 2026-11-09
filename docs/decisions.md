# Journal des décisions

Toute décision structurante, datée et justifiée.

| Date | Décision | Justification |
| --- | --- | --- |
| 2026-10-29 | Sujet retenu : annexe A, n° 9, bornes de recharge électrique (IRVE) | *(à compléter par l'équipe)* |
| 2026-11-03 | Département étudié : Calvados (14), commanditaire SDEC Énergie | Parmi les 20 départements qui passent les critères (au moins 300 points de charge, au moins 95 % de dates lisibles, 30 à 90 % de communes sans borne, hors Paris et petite couronne), celui qui a le plus de données : 1 883 points de charge, 95,7 % de dates de mise en service lisibles, 56 % des 528 communes sans borne (mélange Caen / rural). Alternatives écartées : Puy-de-Dôme (63), Morbihan (56, trop peu de communes sans borne). Calculé sur le fichier IRVE du 2026-11-03. |
| 2026-11-08 | Ordre de passage sur 01_exploration.ipynb en S47 : Arianne, puis Arsene, puis Dieudonné, puis Ali | Un notebook modifié par deux personnes en même temps crée un conflit Git. Arianne ouvre (profil, qualité) ; Ali passe en dernier car le croisement et la synthèse ont besoin des résultats des autres. Chacun prévient sur WhatsApp avant de commencer et fusionne sous 24 h. |
| 2026-11-09 | Dates de mise en service invalides (ANO-01) : les 33 dates antérieures à 2000 ou dans le futur sont mises à vide ; aucune date n'est imputée pour les lignes vides ; les lignes restent dans les données. | Inventer une date fausserait le rythme de mise en service par année (Q3), et supprimer les lignes ferait perdre des points utiles aux autres questions. Au niveau national, 44,2 % des dates sont vides (74 269 lignes sur 168 013) : Q3 y est calculée sur environ 56 % des lignes, limite à écrire dans le README. Dans le Calvados, 95,7 % des dates sont lisibles (décision du 2026-11-03). Fiche ANO-01. |
| 2026-11-10 | Les fichiers sont lus en texte (`dtype=str`) ; un seul point de charge par `id_pdc_itinerance` ; valeurs bidon remplacées par des vides ; oui/non normalisés en booléens. | Le texte conserve les codes INSEE à 5 caractères (95 181 lignes vérifiées). Les doublons (ANO-02) surévalueraient les comptages d'environ 8 %. Fiches ANO-02 à ANO-04. |
