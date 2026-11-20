# Sources et pièces du cadrage

| Pièce | Ce qui a été vérifié |
| --- | --- |
| [Matrice](MATRICE-PARITE.md) et [inventaire](RESEARCH.md) | Tâches, destinations d’écran et dépendances du code effectivement présent. |
| [Socle PostgreSQL](evidence/socle-postgresql.log) et [socle SQLite](evidence/socle-sqlite.log) | Suites existantes de l’image installée, avec bases éphémères isolées. |
| [Sonde de lecture des quatre schémas](evidence/lecture-schemas.json) | Trois entrées HTTP authentifiées par schéma sur des documents simples à deux pages. Aucun enregistrement ni rendu moteur demandé. |
| [Maquette interactive](evidence/maquette.html) et [revue visuelle](VISUAL-REVIEW.md) | Navigation simulée, focus, états et captures aux trois tailles. |
| [Revue indépendante](REVIEW.md) | Relecture du périmètre, des preuves, des dépendances de routage, de la réversibilité et des décisions réservées à la réalisation. |

Les exécutants `/root/u305_parity`, `/root/u305_design` et `/root/u305_review` ont produit l’audit et les tests de socle, la maquette et son contrôle navigateur, puis la revue indépendante. Le responsable du lot a rapproché la carte Notion et le dépôt, défini les contrats de migration et de décision, et exercé les lectures sur quatre schémas. Le contrôle de planification suit la procédure des sous-lots UI-003, avec le validateur v1 restreint à l’identifiant exact du sous-lot.

## Preuves de réalisation

- [Comparatif de neuf paires de captures](evidence/comparatif-produit.pdf), [mesures de rendu](evidence/comparaison-navigateur.json) et [annonces Orca](evidence/orca-clavier.json).
- [Démarrages vierge, modèle et Figma initial](evidence/demarrages.json), [ajout et purge Figma](evidence/temoin-figma-purge.json), [gestes de section et remplacement de version](evidence/realisation-gestes-v2.json).
- [Vérification et confirmation Wagtail](evidence/article-wagtail.json), [signets historiques](evidence/signet-canvas.json) et [revue indépendante](evidence/revue-integration.md).
- [Conflit entre deux gestionnaires et révocation](evidence/conflit-et-droits.json), [réponse interrompue, reçu expiré et passerelle indisponible](evidence/rejeu-expiration-indisponibilite.json).
- [Tests PostgreSQL](evidence/realisation-tests-postgresql.log), [tests SQLite](evidence/realisation-tests-sqlite.log) et [test du modèle JavaScript](evidence/test-sections.log).
- [Réinstallation depuis le candidat au retrait](evidence/retour-image.json), [état des deux moteurs](evidence/non-publication.json), [réponses publiques avant et après](evidence/pages-publiees.json) et [vérification du Studio local](evidence/installation-locale.json).
