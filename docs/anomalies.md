# Journal des anomalies

Chaque anomalie trouvée dans les données ou le code est consignée ici, dans la même pull
request que son traitement. Une fiche par anomalie, numérotée ANO-01, ANO-02, etc.

## Modèle de fiche

### ANO-01 : *(titre court)*

- **Colonne(s) concernée(s)** : nom exact dans la source.
- **Description** : ce qui est observé, avec un exemple de valeur.
- **Ampleur** : nombre de lignes et part du total concernées.
- **Cause probable** : erreur de saisie, changement de nomenclature, secret statistique,
  doublon structurel, etc.
- **Traitement retenu** : conservé, corrigé, imputé, exclu ou signalé, avec la justification.
- **Impact sur l'analyse** : indicateurs ou conclusions affectés.


## ANO-01 : date de mise en service absente ou invalide

- **Colonnes :** `date_mise_en_service`
- **Description :** la date est vide, ou fixée à une valeur antérieure à 2000 (dont `1900-01-01`), ou postérieure à la date du jour.
- **Ampleur :** 74 269 lignes vides sur 168 013 (44,2 %) ; 32 lignes antérieures à 2000 ; 1 ligne dans le futur (`2028-08-27`).
- **Cause probable :** champ facultatif dans le schéma de déclaration. Les années anciennes ressemblent à une valeur par défaut. La date future peut être une mise en service annoncée (hypothèse non vérifiée).
- **Traitement :** conserver les lignes dans `data/processed/` avec la date mise à vide (`NaT`) pour les 33 dates invalides. Ne pas imputer de date. Exclure ces lignes uniquement des calculs de la question Q3.
- **Impact :** au niveau national, la question Q3 repose sur 93 711 lignes sur 168 013 (environ 56 %) ; cette limite sera écrite dans le README. Pour le Calvados, 95,7 % des dates sont lisibles, donc l'impact y est faible. Les autres questions ne sont pas touchées.

## ANO-02 : même point de charge déclaré plusieurs fois

- **Colonnes :** `id_pdc_itinerance`
- **Description :** un même identifiant de point de charge apparaît sur plusieurs lignes, qui ne sont pas identiques sur toutes les colonnes.
- **Ampleur :** 26 709 lignes concernées ; 154 294 identifiants distincts sur 168 013 lignes, soit 13 719 lignes en trop (8,2 %). Aucune ligne identique à 100 %.
- **Cause probable :** le fichier consolidé réunit plusieurs jeux de données de data.gouv. Pour les 12 990 identifiants concernés, la ressource, le jeu de données et l'organisation source diffèrent : le même point est déclaré par deux sources (observé sur les colonnes `datagouv_*`).
- **Traitement :** garder une seule ligne par `id_pdc_itinerance`, celle dont `date_maj` est la plus récente. Les lignes sans `date_maj` passent en dernier.
- **Impact :** sans ce traitement, tous les comptages de points de charge (Q1, Q2, Q4) seraient surévalués d'environ 8 %.

## ANO-03 : manquants déguisés

- **Colonnes :** `num_pdl`, `restriction_gabarit`
- **Description :** des valeurs qui signifient « inconnu » sont écrites comme de vraies valeurs : `inconnu`, `x`, « Restriction de gabarit non précisée », `0000000000000`, valeurs blanches. Une partie de `num_pdl` est en notation scientifique (`E+13`), ce qui a détruit l'identifiant.
- **Ampleur :** `restriction_gabarit` : environ 86 000 lignes (51 %), en plus des 2,06 % de vides. `num_pdl` : plus de 7 800 lignes de valeurs bidon, en plus de 66,9 % de vides.
- **Cause probable :** saisie libre sans contrôle côté déclarant, et passage par un tableur pour `num_pdl` (hypothèse non vérifiée).
- **Traitement :** remplacer ces valeurs par une valeur vide (`NaN`) dans `data/processed/`. Garder « Aucune Restriction » comme vraie valeur.
- **Impact :** les taux de manquants réels sont plus élevés que ceux du profil. Si Q5 utilise `restriction_gabarit`, elle doit le dire. Pas d'impact sur Q1 à Q4.

## ANO-04 : oui/non écrits de plusieurs façons

- **Colonnes :** `paiement_cb`, `gratuit`, `cable_t2_attache`
- **Description :** la même information est écrite `True`, `true`, `TRUE`, `False`, `false`, `FALSE`, `1` ou `0`, soit 8 valeurs distinctes au lieu de 2.
- **Ampleur :** `paiement_cb` : 7,3 % de vides, le reste réparti sur les 8 formes. `cable_t2_attache` : 47,9 % de vides (80 434 lignes).
- **Cause probable :** déclarations venant de sources différentes, sans format imposé (hypothèse non vérifiée).
- **Traitement :** normaliser en vrai booléen, sans tenir compte de la casse. `1` devient vrai et `0` faux (hypothèse à confirmer), les vides restent vides.
- **Impact :** Q5 (part des points payables par carte) serait faussée si on ne comptait qu'une seule forme de « vrai ».

## ANO-05 : code INSEE de la commune absent

- **Colonnes :** `code_insee_commune` (et `consolidated_commune`, `consolidated_code_postal`)
- **Description :** le code INSEE est vide pour une grande partie des points de charge, ce qui empêche de les rattacher à une commune et de leur associer une population.
- **Ampleur :** 66 010 lignes sur 154 294 après suppression des doublons (42,8 %).
- **Cause probable :** champ de géolocalisation consolidée non renseigné quand l'adresse n'a pas pu être rattachée à une commune (hypothèse non vérifiée).
- **Traitement :** conserver les lignes, ne pas inventer de commune. Exclure ces lignes des calculs par commune (Q1) et indiquer leur part dans les résultats. Récupérer la commune à partir des coordonnées ou du code postal est une piste à décider avec le groupe.
- **Impact :** Q1 (points de charge pour 10 000 habitants par commune) n'est calculée que sur environ 52 % des lignes. Les taux par commune sont sous-estimés.
