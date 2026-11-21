# TDD et tests de comportement

Choisir les scénarios selon la [politique de tests](../governance/TESTING-POLICY.md#choisir-une-vérification-utile) et les relier aux critères d’acceptation de la spécification versionnée. Le [workflow de développement](FEATURE-DEVELOPPEMENT.md#passage-de-la-spécification-au-code) décrit le passage entre le Test Engineer et Codex.

| Étape | Exécution et preuve |
|---|---|
| RED | Exécuter le test de référence sur un commit contenant le test et ses prérequis, avant l’implémentation visée. Vérifier que le test atteint l’assertion pertinente et que l’écart observé correspond au comportement absent ou incorrect attendu. Conserver l’identifiant exact du commit, celui du critère, la commande et la sortie qui montre l’échec. |
| GREEN | Implémenter le comportement prévu, puis rejouer les mêmes scénarios et les vérifications affectées. Consigner la révision et les résultats observés. Pour toute modification d’un scénario, appliquer la [politique des tests de référence](../governance/TESTING-POLICY.md#tests-de-référence). |
| REFACTOR | Si une amélioration de structure est utile, la faire après GREEN en préservant les comportements attendus. Rejouer les vérifications affectées et consigner les résultats sur la révision obtenue. |
| Intégration | Vérifier ensemble les composants concernés dans l’environnement pertinent. |

Un échec d’import, de collecte, de configuration ou de préparation des données ne prouve pas le RED métier. Un scénario de refus passe lorsqu’il observe le refus attendu. Si le test est déjà vert sur la base, vérifier si le comportement existe ou si le scénario manque son objectif. Consigner le constat sans fabriquer d’échec. Si le commit RED ou son exécution manque, signaler la preuve manquante dans le rapport.

Avant de considérer GREEN, comparer le contenu des tests de référence du commit RED à celui du commit GREEN : les tests et assertions approuvés doivent être présents sans affaiblissement. Toute différence exige la décision et la revue prévues dans [TESTING-POLICY.md](../governance/TESTING-POLICY.md#tests-de-référence). La CI exécute les scénarios retenus sur le SHA GREEN et lie les résultats au run, sans se satisfaire d'un rapport de développeur.

Le passage à GREEN conserve la sortie RED et son résultat d’origine. Enregistrer le remplacement selon le [registre des preuves](../templates/EVIDENCE.md#historique-et-remplacement-dune-preuve).

## Scénarios prioritaires

- Action permise et action refusée selon acteur, ressource et contexte.
- Entrée invalide, état incompatible, doublon et modification concurrente.
- Erreur de connecteur, délai dépassé et résultat distant incertain.
- Migration et conservation des données lorsque le lot les modifie.
- Intégration des formulaires et réponses serveur.

## Provenance et blocage du RED

Pour chaque test RED requis, relier l'identifiant réel du run QA, le mandat, la version de spécification, le critère couvert, le commit de base, le commit de tests, le diff base → RED, l'environnement, la commande exécutée, l'horodatage et la sortie conservée. Le contrôleur vérifie par l'API de la plateforme d'exécution que la commande et son résultat proviennent du run QA sur ce SHA, et vérifie l'empreinte des artefacts ; une déclaration textuelle d'agent ne suffit pas. Si le runtime ne fournit pas ces éléments, la provenance reste non vérifiée. Vérifier que le diff introduit les tests et leurs seuls prérequis sans introduire l'implémentation attendue. Le statut RED correspond à l'échec métier attendu constaté, pas à un simple échec de processus.

Si l'exécution QA distincte, le commit, la sortie ou la vérification du diff manque alors que le RED externe est requis, conserver QG-08 comme BLOQUÉ ou À FAIRE. Ni le GREEN ni la revue favorable ne transforment rétroactivement un RED non prouvé en succès. Seule une décision de dispense conforme aux [permissions](../governance/AGENT-PERMISSIONS.md#séparation-opérationnelle-des-responsabilités) peut modifier cette exigence.
