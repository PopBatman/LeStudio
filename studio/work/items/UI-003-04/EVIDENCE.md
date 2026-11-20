# Pièces du cadrage

| Pièce | Portée |
| --- | --- |
| [Analyse du socle](RESEARCH.md) | Lecture du modèle, de la projection et des parcours déjà livrés. |
| [Socle PostgreSQL](evidence/socle-postgresql.log) et [socle SQLite](evidence/socle-sqlite.log) | Sept modules existants rejoués en environnement isolé. Recette Figma simulée. |
| [Maquette](evidence/maquette.html) et [revue visuelle](VISUAL-REVIEW.md) | Support interactif de conception, avec captures aux formats ordinateur, tablette et mobile. |
| [Revue du cadrage](REVIEW.md) | Relecture indépendante de la couverture de la carte Notion, de la filiation, de l’accès privé et des décisions de comparaison. |

Le responsable du lot a rapproché la [carte](https://www.notion.so/41d49e23bbdb81218933e4095ea7ebe8), le dépôt et le Workflow AI. Les exécutants `/root/u304_domain`, `/root/u304_design` et `/root/u304_review` ont assuré respectivement l’analyse et les tests du socle, la maquette et sa vérification au navigateur, puis la revue indépendante. Le contrôle documentaire de planification emploie la procédure des sous-lots UI-003, avec le validateur v1 restreint à l’identifiant exact du lot.

## Preuves de réalisation

Les [tests PostgreSQL](evidence/realisation-tests-postgresql.log) et [SQLite](evidence/realisation-tests-sqlite.log) portent sur l’image Studio. La [recette navigateur](evidence/realisation-parcours.json) et les [contrôles de reprise](evidence/realisation-comparaison-erreurs.json) portent sur des sites fictifs. Les [revues du service](evidence/revue-service.md) et [de l’intégration](evidence/revue-integration.md) proviennent d’exécutants distincts des auteurs des surfaces examinées. Le [contrôle d’installation](evidence/realisation-poste-local.json) compare les révisions existantes et le raccordement avant/après.

Le [compte rendu de recette](evidence/recette-navigateur.md) rapproche les écrans, les droits et les [empreintes des pages publiques](evidence/pages-publiees.json). Les exécutants de réalisation sont `/root/u304_source` pour la provenance et la revue du service, `/root/u304_service` pour la persistance et la revue de l’intégration, `/root/u304_browser` pour la présentation et la recette navigateur. Le responsable du lot a réalisé le raccordement HTTP, la vérification sous Orca et l’installation locale.
