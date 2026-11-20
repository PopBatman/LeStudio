# Plan de réalisation FEAT-003-01

Toutes les lignes de réalisation attendent un mandat de développement. La fiche Site et ses maquettes relèvent du parent et de ARCH-002-01.

| Ordre | Livrable, zone et responsable futur | Dépendances | Vérification de sortie |
|---|---|---|---|
| 1 | QA/backend : fixtures synthétiques A/B, origines, documents valides/invalides et tests rouges du service | Contrats de ce dossier | AC1–5 : lecture vide, autorisations, exemple canonique, conflit et état initial sans ligne. |
| 2 | Backend : app de composition centrale, stockage d’instantanés et migration additive | 1 | AC1/5 : migrer une copie de base avec Site et SiteConnection ; aucune révision implicite. Relire depuis une autre connexion, vérifier unicité et filiation. |
| 3 | Backend : validateur V1 et résolution des références de confiance | 1, 2 | AC2–4 : tester trois origines, deux consommateurs, version de schéma inconnue, limites exactes et dépassements, doublons, cycle, référence absente/étrangère, document partiel ou invalide. |
| 4 | Backend : lecture ciblée, création et sauvegarde transactionnelles | 2, 3 | AC1/3/4 : tester droits directs, révocation, course première création, course de sauvegarde et nouvelle tentative après réponse perdue. PostgreSQL requis pour les courses. |
| 5 | QA : recette locale et compatibilité | 4 | AC1–5 : deux sites, brouillon indépendant du raccordement, droits lecture/gestion, erreur injectée pendant écriture, ancienne révision relisible ; aucun appel au moteur. Mesurer document à la limite sur le poste avant de fixer les budgets de production. |
| 6 | Réviseur indépendant puis responsable du lot : revue, rapport, preuves et rapprochement Notion | 5 | Rattacher résultats, révision et limites à chaque critère. Les interfaces 02–08 consommeront le service ultérieurement. |

Le cadrage a examiné le contrat parent, les lots livrés, le mandat et le document exemple. La vérification actuelle est documentaire ; la suite de tests et les preuves d’exécution ci-dessus sont à produire lors du développement.
