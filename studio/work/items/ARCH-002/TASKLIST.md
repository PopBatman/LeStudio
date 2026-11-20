# Plan de réalisation ARCH-002

| Ordre | Travail prévu et dépendance | Responsable et zone | Vérification attendue |
|---|---|---|---|
| 1 | Partir du contrat cadré et fixer les versions exactes et les fixtures A/B. | Intégration, futur moteur | Manifeste de versions et digest identique, identités et marqueurs distincts. AC3–4. |
| 2 | Écrire les tests des droits, des états, de l’identité, des conflits et des erreurs avant implémentation. | Backend central, tests de raccordement | Cas initial sans instance, domaines absents, mandats FEAT-002, révocation et reprise. AC1–6. |
| 3 | Préparer le moteur, son image, les deux configurations, les données de démonstration et les routes internes. | Auteur moteur et intégration locale | Migrations Wagtail indépendantes, vérification réelle du rendu, refus des écritures et de l’accès sans certificat valide. AC3–5, AC7–9. |
| 4 | Créer modèle de liaison, migration additive, profil de confiance, client de lecture et commande manuelle. | Backend Studio et connecteur | Migration depuis FEAT-002, validation bornée des réponses, tentative concurrente et absence de liaison partielle. AC1–6, AC9. |
| 5 | Exercer la matrice locale avec deux instances. | Qualification indépendante du développement | Succès A et B, permutation des identités et marqueurs, mauvaise version, certificat refusé, service indisponible et délai dépassé. Tester séparément les rôles PostgreSQL, les médias homonymes et les sessions éditeur. Mesurer les ressources, tester une restauration isolée. AC3–9. |
| 6 | Relire la réalisation, rattacher commandes, versions, preuves et limites à la révision. | Réviseur distinct puis responsable du lot | Rapports locaux expurgés et rapprochement de la carte Notion. |

La commande de vérification sera exercée sur des données fictives. Les résultats prévus ci-dessus sont des critères de fin du futur développement.
