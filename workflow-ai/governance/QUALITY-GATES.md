# Contrôles qualité du workflow

Un contrôle qualité apporte une preuve ; il n’accorde pas de permission. Chaque contrôle a un état : **À FAIRE**, **SATISFAIT**, **ÉCHEC**, **BLOQUÉ** ou **NON APPLICABLE avec motif**.

| ID | Contrôle | Preuve attendue | Moment |
|---|---|---|---|
| QG-01 | Besoin et périmètre | Objectif, acteur, ressources et mandat applicable | DISCOVERY |
| QG-02 | Recherche adaptée | Sources primaires, options, inconnues du domaine | Avant SPECIFIED |
| QG-03 | Spécification | Règles, données, permissions, erreurs et critères | SPECIFIED |
| QG-04 | Architecture | Responsabilités, contrats et décisions nécessaires | SPECIFIED / PLANNED |
| QG-05 | Risques et sécurité | Risques utiles au lot, données et contrôles prévus | Avant READY |
| QG-06 | Tasklist | Ordre, dépendances, fichiers, tests et conditions de fin | PLANNED |
| QG-07 | Conception frontend | Maquette ou référence, états et statut d’examen | Avant READY si UI |
| QG-08 | Construction et TDD pertinent | Comportements testés, RED/GREEN observés lorsqu’applicables | IMPLEMENTING |
| QG-09 | Vérification UI réelle | Navigateur, clavier, états, captures et écarts | Avant VERIFIED si UI |
| QG-10 | Intégration | Tests et parcours exécutés sur les entrées identifiées | VERIFIED |
| QG-11 | Revue | Exécutant, constats, preuves examinées et écarts traités | REVIEWED |
| QG-12 | Livraison | Cible, artefact, compatibilité, reprise et mandat | Si une livraison est demandée |

Les preuves sont actives par défaut. Pour chaque type requis par une phase du CLI, toutes les preuves actives doivent être réussies et liées au contrat et aux sources courants. Une réussite ne masque pas un échec actif. Les preuves historiques marquées `active: false` restent conservées et contrôlées comme artefacts, sans satisfaire le contrôle ni imposer la relecture des anciennes sources. Documenter leur remplacement selon [EVIDENCE.md](../templates/EVIDENCE.md).

## Proportionner les contrôles

| Niveau | Application |
|---|---|
| LIGHT | Travail limité et réversible : vérifications ciblées, recherche supplémentaire seulement si une inconnue le justifie |
| STANDARD | Nouveau comportement ou intégration : spécification, tests métier, intégration et revue adaptée |
| CRITICAL | Permissions sensibles, données importantes, migrations risquées, effets irréversibles : cas négatifs, revue indépendante et décisions explicites sur les risques résiduels |

La classification dépend des effets du changement. Une correction de sécurité peut être critique malgré peu de lignes modifiées.

QG-07 et QG-09 sont non applicables pour un travail sans frontend. QG-08 ne force pas un test artificiel pour une retouche de texte ou de style. QG-12 reste non applicable lorsqu’aucune livraison n’appartient au lot.

Une maquette peut être examinée dans le mandat déjà donné. Ne pas inventer un accord visuel, ni imposer une confirmation nouvelle à chaque sous-tâche lorsqu’elle n’est pas nécessaire. Les arbitrages produit encore ouverts sont distingués des détails d’implémentation couverts.

`READY` ne vaut pas autorisation. `DONE` n’implique aucune mise en production. Voir [workflow](../workflows/FEATURE-WORKFLOW.md).

