# Plan de passage
| Ordre | Travail et périmètre | Condition de passage |
| --- | --- | --- |
| 01 | Cartographier les tâches V1, partir de la maquette parent, prototyper les trois entrées. Fixer tokens, états, gestes, focus, densité et panneaux sur bureau/tablette/mobile. | Prototype haute fidélité jouable, matrice clavier, revue UX/DA humaine et décision explicite avant code UI. |
| 02 | À partir de FEAT-004, confronter le rendu privé et le contrat de sélection à deux pages ayant des blocs imbriqués. Vérifier URL, révision, page, droits et expiration. | Comparaison éditeur/moteur sur la même révision et preuves du mode dégradé. |
| 03 | Brancher catalogue, édition simple, calques, guides, inspecteur, historique et variantes responsive sur les services de composition. | Tests métier puis navigateur sur deux sites, concurrence, rechargement et parcours entièrement clavier. |
| 04 | Reprendre une confirmation FEAT-003-08. Comparer référence, résultat canonique et rendu identifié. Présenter éléments manquants et écarts. | Brouillon importé modifiable par les mêmes commandes. Provenance conservée et droits de site revérifiés. |
| 05 | Coexister avec les entrées Structure et Canvas. Rejouer les tâches V1 sur anciens brouillons, inspecter responsive et accessibilité avec UI-002. | Rapport avant/après, captures, revue indépendante, validation humaine et répétition du retour V1. Masquer les entrées, surveiller les régressions, retirer seulement après décision documentée. |

La carte parent coordonne la séquence. Aucun sous-lot n’est lancé par ce cadrage. Les fonctionnalités à qualifier dans Studio, le moteur et l’import sont délimitées dans ARCHITECTURE.md. Conserver les preuves navigateur des trois origines, l’audit lecteur d’écran, les conflits et la décision de bascule dans les sous-lots concernés.

La matrice de composants de 02–03 indique, par version et portée, le moteur compatible, les propriétés éditables, les restrictions de placement et les cas de rendu vérifiés. Le dossier de compatibilité Figma de 04 relie les versions sources, largeurs disponibles, décisions opérateur, écarts connus et révision résultante aux captures de comparaison.
