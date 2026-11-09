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
- **Impact :** la question Q3 repose sur 93 711 lignes sur 168 013 (environ 56 %). Cette limite sera écrite dans le README. Les autres questions ne sont pas touchées.
