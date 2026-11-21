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

## Tests de référence

Les tests de référence traduisent les critères d’acceptation de la spécification versionnée. Les assertions portent sur des résultats observables.

Modifier un test de référence uniquement pour corriger une erreur démontrée au regard de la spécification ou pour appliquer un changement de critère explicitement décidé par une personne habilitée selon le mandat. Avant la modification, consigner le motif, le critère et sa version, les assertions touchées et, si le critère change, la référence de la décision. Soumettre le diff à la [revue](../workflows/FEATURE-REVIEW.md), avec les vérifications rejouées et les preuves remplacées. Lorsqu’une ambiguïté implique un changement de critère, la faire trancher avant de modifier le test concerné.

Aucun rôle ne peut modifier silencieusement un critère ni affaiblir, supprimer, ignorer ou marquer comme échec attendu un test de référence pour obtenir un GREEN. Un écart de l’implémentation à la spécification se corrige dans l’implémentation.

## CI déterministe

La CI exécute des commandes définies pour la révision contrôlée. À mêmes sources et mêmes entrées, le verdict repose sur les mêmes règles et codes de sortie. Maîtriser les versions d’outils et de dépendances, isoler les données de test et fixer les sources de variabilité utiles (heure, aléa, ordre, services externes). Isoler les qualifications qui exigent un service réel et consigner leur résultat séparément.

La CI n’utilise aucun verdict d’agent ou de modèle et ne réécrit ni la spécification, ni les tests, ni le code. Consigner la révision, les commandes, l’environnement et les résultats selon les règles de preuve ci-dessous. La gouvernance des accès relève de la [politique d’exécution](EXECUTION-POLICY.md).

## Preuves

Enregistrer commande, révision ou empreinte des entrées, environnement, date, résultat et artefacts utiles. Les données sensibles et secrets sont omis. Distinguer **PASS**, **FAIL**, **BLOCKED** et **NOT RUN**.

Conserver les anciennes preuves sans les faire passer pour des résultats courants : `active: false` les classe dans l’historique, avec un motif et un remplacement identifié. Une preuve est active par défaut. Pour les types requis par la phase, tous les résultats actifs doivent être `passed`, avec des entrées et une empreinte de contrat courantes ; un PASS ne masque aucun FAIL ou NOT RUN actif. L’artefact et les métadonnées historiques restent contrôlés, sans relire les anciennes sources.

Un test simulé prouve notre comportement face à la simulation ; une qualification fournisseur réelle prouve seulement les opérations effectivement essayées. Une capture prouve un rendu observé, pas l’intégralité de l’accessibilité.

Arrêter les tests supplémentaires lorsque les critères et risques identifiés sont suffisamment couverts. Refaire les vérifications affectées par une modification ultérieure ; ne pas réutiliser une preuve devenue périmée.

Voir [TDD](../workflows/FEATURE-TDD.md) et [modèle de preuve](../templates/EVIDENCE.md).

