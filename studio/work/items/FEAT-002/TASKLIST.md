# Plan de réalisation du registre clients et sites

Le mandat courant couvre la préparation documentaire. Les lignes 2 à 7 décrivent la future réalisation. Les identifiants AC renvoient à la [spécification](SPEC.md).

| Ordre | Résultat et dépendance | Zone et responsabilité prévue | Vérification attendue |
|---|---|---|---|
| 1 | Rapprocher la carte, FEAT-001 et UI-001. Préparer règles, droits, données, parcours et maquettes. | Cadrage produit et technique, dossier du lot | Contrôle documentaire et examen des références visuelles. |
| 2 | Écrire les tests en échec pour les règles de fiches et les accès. Dépend du contrat proposé. | Auteur backend, tests du registre | AC1–AC9. Isoler deux clients, deux sites frères, plusieurs acteurs et des homonymes. |
| 3 | Introduire les modèles, les contraintes, les habilitations et leur attribution locale. Dépend des scénarios. | Backend, nouvelle application de registre et migrations Django | Migration PostgreSQL depuis FEAT-001, compte/session préservés, zéro droit accordé automatiquement. |
| 4 | Implémenter les recherches filtrées, créations, modifications et transitions d’archive dans des transactions. | Backend, services et formulaires de la feature | AC1–AC8. Contrôler requêtes directes, doublons, valeurs limites, conflit d’édition, perte de droit et absence d’écriture partielle. |
| 5 | Relier Clients et Sites à l’accueil opérateur, composer listes, fiches, formulaires et confirmations. Dépend des maquettes et des services. | Auteur UI, vues du registre, gabarit espace de travail et composants UI-001 | AC1–AC9. États vides, formulaires erronés, confirmation, focus, contenu long et petit écran. |
| 6 | Exercer le parcours complet sur données fictives et la procédure de protection des données. | Intégration, tests Django, PostgreSQL et navigateur | AC1–AC10. Captures réelles desktop/mobile, traces expurgées, procédure éprouvée avant toute donnée personnelle réelle. |
| 7 | Faire relire la révision et rapprocher résultats, limites et carte. | Réviseur distinct de l’auteur, puis responsable du lot | Avis indépendant, rapport, empreintes des preuves et actualisation de Notion. |
