# Politique de tests et de preuves

## Choisir une vérification utile

| Changement | Vérification attendue |
|---|---|
| Invariant ou transition métier | Scénarios positifs, refus et cas limites |
| Autorisation | Acteur, action, ressource et contexte ; appels directs concernés |
| Connecteur | Contrat, erreurs, délais, doublons, résultat incertain et qualification ciblée |
| Modification de données | Contraintes, migration et reprise selon le risque |
| Interaction UI | Parcours, erreurs, clavier et focus |
| Retouche visuelle ou documentation | Contrôle visuel, cohérence et liens ; pas de tests imitant le texte |

Les tests s’exécutent dans l’environnement pertinent. Pour Studio, PostgreSQL est le choix exprimé ; un résultat obtenu sur une autre base ne qualifie pas silencieusement PostgreSQL.

## Cycle TDD

Pour un nouveau comportement testable : écrire le scénario depuis l’exigence, constater un échec pour la raison attendue, implémenter le comportement, puis vérifier après un refactor utile. Un import manquant ou un environnement cassé ne constitue pas le RED métier attendu.

Modifier un test est légitime lorsqu’une exigence change explicitement ou lorsqu’un test est erroné. Documenter la raison ; ne pas réduire les critères pour faire disparaître un défaut.

## Preuves

Enregistrer commande, révision ou empreinte des entrées, environnement, date, résultat et artefacts utiles. Les données sensibles et secrets sont omis. Distinguer **PASS**, **FAIL**, **BLOCKED** et **NOT RUN**.

Conserver les anciennes preuves sans les faire passer pour des résultats courants : `active: false` les classe dans l’historique, avec un motif et un remplacement identifié. Une preuve est active par défaut. Pour les types requis par la phase, tous les résultats actifs doivent être `passed`, avec des entrées et une empreinte de contrat courantes ; un PASS ne masque aucun FAIL ou NOT RUN actif. L’artefact et les métadonnées historiques restent contrôlés, sans relire les anciennes sources.

Un test simulé prouve notre comportement face à la simulation ; une qualification fournisseur réelle prouve seulement les opérations effectivement essayées. Une capture prouve un rendu observé, pas l’intégralité de l’accessibilité.

Arrêter les tests supplémentaires lorsque les critères et risques identifiés sont suffisamment couverts. Refaire les vérifications affectées par une modification ultérieure ; ne pas réutiliser une preuve devenue périmée.

Voir [TDD](../workflows/FEATURE-TDD.md) et [modèle de preuve](../templates/EVIDENCE.md).

