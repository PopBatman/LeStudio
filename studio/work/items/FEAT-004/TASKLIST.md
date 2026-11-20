# FEAT-004 — Ordre de réalisation

Le mandat du 20 novembre porte sur le cadrage. Les tâches suivantes décrivent le développement à lancer séparément. Les critères A1 à A8 sont définis dans SPEC.md.

| Ordre | Travail à fournir | Dépendance | Contrôle avant de poursuivre |
|---|---|---|---|
| 1 | Préparer deux sites et deux sessions de qualification, des révisions historiques, une page avec article, média et blocs internes. Relever les états active et live avant intervention. | ARCH-002 et services FEAT-003 | Tests initialement en échec sur la demande de rendu et le refus inter-sites. A1, A3, A4 |
| 2 | Étendre le contrat de raccordement et la passerelle mTLS pour la seule opération de préparation. Définir manifeste, bornes et diagnostics partagés, y compris pour une ancienne image. | 1 | Contrat sur requêtes/réponses, absence de capacité et identité inattendue. A1, A6 |
| 3 | Résoudre révision, versions et ressources puis rendre une page par les gabarits Wagtail internes. Rendre les IDs de blocs, les menus et les trois placements. | 2 | Rapprocher manifeste et HTML, tester anciennes révisions, article republié, média illisible et absence d’effet sur la base. A1, A3–A5 |
| 4 | Orchestrer la préparation depuis Studio, la session, la péremption, l’échéance et l’élimination des instantanés. Protéger chaque accès au document et aux médias. | 2–3 | Horloge contrôlée, concurrence, changement de droits, coupure pendant préparation et reprise. A2–A4, A6 |
| 5 | Relier fiche Site et atelier au parcours maquetté. Intégrer états, changement de page/format, comparaison précédente et retour. | 3–4 | Navigation clavier et mobile, page absente, brouillon modifié, état actif inconnu. A2, A5–A8 |
| 6 | Qualifier le moteur et la passerelle réels sur données fictives. Relever empreintes, révisions live, captures dans les trois formats, erreurs et reprise. | 1–5 | Recette A1–A8 et revue indépendante. Transmettre à UI-003 le contrat effectivement qualifié, actualiser le Kanban. |

Le socle de composition FEAT-003-01 à 07 et le raccordement ARCH-002 sont livrés. Le parent FEAT-003 est encore en réalisation, FEAT-003-08 est cadré. L’ordre du Kanban place l’import avant l’aperçu. Le rendu peut être qualifié avec les révisions internes existantes. La recette d’un parcours issu de Figma utilisera les correspondances effectivement livrées par FEAT-003-08.

## Réalisation du 20 novembre

Les tâches 1 à 6 ont été exécutées sous le mandat « Lance FEAT-004 ». `render_engine` a livré les gabarits et la passerelle, `render_bridge` le connecteur et la purge, `render_ui` la session et les écrans. `render_review` a revérifié la navigation secondaire, le refus entre sessions et la purge. Les preuves de qualification sont indexées dans [EVIDENCE.md](EVIDENCE.md).
