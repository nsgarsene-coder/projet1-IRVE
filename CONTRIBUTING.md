# Règles de travail de l'équipe

Ces règles évitent les conflits Git et les conflits humains. Elles s'appuient sur les
exigences GIT-01 à GIT-06 et la section 11 du cahier des charges. Tout le monde les accepte
avant le premier commit.

## 1. Rôles

| Rôle | Responsabilité | Rotation |
| --- | --- | --- |
| Chef de projet | Planning, suivi des issues, **seul interlocuteur du prof** | Fixe |
| Responsable données | Chargement, qualité, journal des anomalies | Change à chaque semaine école |
| Responsable dépôt | Revue des PR, tags, propreté de l'historique | Change à chaque semaine école |
| Responsable restitution | Cohérence des graphiques, trame de la soutenance | Change à chaque semaine école |

À 3, le chef de projet cumule un second rôle. **Tout le monde code et commite** : la note est
individuelle et une contribution absente de l'historique est un motif de refus.

## 2. Tâches : une issue par tâche

1. Toute tâche est une issue GitHub, assignée à **une** personne, avec le jalon visé.
2. On déplace sa carte dans le tableau GitHub Projects : À faire, En cours, En revue, Fait.
3. Pas de travail sans issue : si on découvre une tâche, on crée l'issue d'abord.

## 3. Branches

- `main` est protégée : personne ne pousse dessus directement.
- Une branche par issue, nommée `type/numero-description` :
  `feat/12-indicateur-par-habitant`, `fix/15-coordonnees-inversees`, `docs/3-questions-v1`,
  `data/8-profil-jeu`.
- Une branche vit peu : quelques jours au maximum, puis PR.
- Avant de commencer la journée : `git switch main && git pull`, puis
  `git switch ma-branche && git merge main` (ou `git rebase main` si on est à l'aise).

## 4. Commits (GIT-03, GIT-05)

- Un commit = un changement cohérent (atomique).
- Message à l'impératif, en français, qui dit ce que fait le commit :
  « Ajoute le calcul du nombre de points pour 10 000 habitants »,
  « Corrige l'inversion des coordonnées », « Documente l'anomalie ANO-03 ».
- Chacun commite **depuis son propre compte**, avec son nom et son email GitHub configurés
  (`git config user.name` / `git config user.email`). En pair programming, ajouter la ligne
  `Co-authored-by: Nom <email>` en fin de message.
- Jamais de données, de sorties de notebook lourdes ou de mots de passe dans un commit
  (pre-commit et la CI bloquent la plupart des cas).

## 5. Pull requests (GIT-02)

1. On ouvre la PR tôt (en brouillon si besoin), avec `Ferme #numero` dans la description.
2. On remplit la liste de vérification du modèle de PR.
3. **Au moins un autre membre relit et approuve.** La CI doit être verte.
4. Le relecteur répond sous **24 h** (48 h le week-end). Il commente le code, pas la personne.
5. C'est l'auteur qui fusionne, en « Squash and merge » si sa branche a des commits brouillons,
   sinon « Merge ». Puis il supprime la branche.
6. Petites PR : moins de 300 lignes modifiées si possible. Une grosse PR ne se relit pas bien.

## 6. Notebook : la source n° 1 de conflits

Un notebook est un fichier JSON : deux personnes qui le modifient en même temps produisent un
conflit presque impossible à résoudre à la main.

- La logique va dans `src/` (fonctions testées) ; le notebook ne fait qu'appeler et commenter.
- **Une seule personne modifie `01_exploration.ipynb` à la fois** : on l'annonce sur le groupe
  avant de commencer, et on fusionne vite.
- Pour explorer librement, chacun peut créer `notebooks/brouillon_<prenom>.ipynb`, à ne pas
  fusionner dans `main` (ou à supprimer avant la PR).
- Sorties effacées avant commit (nbstripout le fait automatiquement après `pre-commit install`).

## 7. Qualité (QC-01 à QC-05)

Avant de pousser : `ruff check .`, `ruff format .`, `pytest`.
Toute fonction ajoutée dans `src/` a au moins un test dans `tests/`.
Les commentaires expliquent le **pourquoi**, pas le quoi.

## 8. Données et traçabilité

- Toute anomalie trouvée va dans `docs/anomalies.md` (format ANO-xx), dans la même PR que son
  traitement.
- Toute décision structurante va dans `docs/decisions.md`, datée et justifiée.
- Toute question au prof passe par le chef de projet, par écrit, via une issue
  « Question au commanditaire » où l'on archive la réponse.

## 9. Jalons et tags (GIT-06)

| Tag | Jalon | Qui le pose |
| --- | --- | --- |
| `v0.1` | J1, lancement | Responsable dépôt |
| `v0.2` | J2, exploration (fin S44) | Responsable dépôt |
| `v0.3` | J3, construction (fin S47) | Responsable dépôt |
| `v1.0` | Remise finale (S50) | Responsable dépôt |

`git tag -a v0.2 -m "Jalon J2 : exploration" && git push origin v0.2`

## 10. Communication et conflits

- Un canal de groupe unique (à choisir : Discord, WhatsApp...) ; les décisions s'écrivent
  ensuite dans `docs/decisions.md` ou une issue, pas seulement dans le chat.
- Chaque semaine école commence par le rappel de 15 minutes : où on en est, ce qui bloque,
  ce qu'on fait cette semaine.
- Un désaccord se règle d'abord en parlant, arguments et données à l'appui. Si personne ne
  tranche, le chef de projet décide et on le note.
- **Un conflit non résolu en 48 h est signalé à l'intervenant référent** (règle du cahier des
  charges).
- Quelqu'un en retard prévient avant l'échéance, pas après. On réassigne l'issue si besoin.

## 11. Définition de « fini »

Une tâche est finie quand : la PR est fusionnée, la CI est verte, le notebook tourne de bout en
bout, l'anomalie ou la décision est consignée, et l'issue est fermée.
