# Concordance et autorité des documents

## Références

| Information | Référence à examiner |
|---|---|
| Objectif et mandat | Instruction explicite de l’utilisateur, décision authentifiée ou périmètre convenu |
| Code, tests, migrations et dépendances | Révision du dépôt concerné |
| Contrat retenu | Version identifiée de la spécification et décision associée |
| Recherche et hypothèse | Source, date, contexte et niveau de confiance |
| Exécution | Résultat observé, entrées, environnement et identité de l’exécuteur |
| Suivi et décisions du lot | Carte Notion du Kanban, décision humaine datée et reliée à la version examinée |
| Reprise technique | Compte rendu court dans `work/items/ID/REPORT.md`, contrat, registre et preuves du dépôt |
| Procédure réutilisable | Guide opérateur ou technique de référence, lié depuis la carte |

Une clarification explicite de l’utilisateur peut remplacer une ancienne orientation. Conserver le texte source et noter la décision qui l’actualise. L’heure de modification d’une page ne suffit pas à lui donner autorité.

## Règles de mise à jour

1. Identifier le document, sa version et son périmètre.
2. Comparer la modification aux décisions applicables et à la situation réelle.
3. Classer les éléments : source, exigence, proposition, décision, réalisation ou preuve.
4. Modifier les documents concernés sans effacer les justifications utiles.
5. Actualiser les références et signaler les copies qui ne sont pas encore synchronisées.

Une case cochée de tasklist rapporte une action accomplie. Elle ne prouve pas l’acceptation du produit. Une décision ne prouve pas son implémentation. Un rapport ne remplace pas ses preuves.

Notion ne déclenche pas automatiquement une action produit. Une idée reçue depuis Notion entre dans le workflow comme une proposition à examiner, selon [FEATURE-REIMPORT.md](../workflows/FEATURE-REIMPORT.md).

La mémoire est séparée par projet. Les anciennes hypothèses du prototype Studio, notamment le choix Contact et l’usage local de SQLite, ne sont pas réintroduites comme décisions actives.

