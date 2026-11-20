# UI-001 — Fondations de l’interface Studio

La [galerie locale](http://127.0.0.1:8000/ui/) présente cinq sections et sept composants Cotton réutilisables. Le [contrat des composants](../../../docs/COMPOSANTS-UI.md) décrit leurs entrées, leurs états et leur usage. Le [guide de démarrage](../../../README.md) explique comment ouvrir la galerie et recompiler les styles.

La [maquette préparatoire](evidence/maquette.html) a fixé la composition desktop et mobile avant le développement. Le gabarit Django, la navigation, les tokens de couleur, la typographie et les composants sont séparés des démonstrations. Celles-ci utilisent des sites fictifs et s’exécutent dans le navigateur. Compose active la galerie sur la boucle locale. Hors Compose, son activation requiert explicitement `STUDIO_UI_GALLERY=1`.

| Vérification | Résultat |
|---|---|
| Django et PostgreSQL sous Docker | Services sains, contrôles système et migrations réussis, sept tests réussis. La route de santé et la galerie ont répondu en HTTP 200. Les trois ressources servies correspondent aux sources locales. |
| Rendu Chromium | [Desktop 1440 × 960](evidence/desktop.png) et [mobile 390 × 844](evidence/mobile.png), police locale chargée, aucun débordement de page. |
| Parcours interactif | Saut au contenu, navigation, boutons, validation vide puis valide et nom de 80 lettres. Le filtre passe de trois lignes à une, affiche l’état vide, puis revient à trois. |
| Accessibilité | Focus visible. Axe-core 4.14.1 a relevé zéro violation dans les règles WCAG A/AA testées aux deux formats. Trois éléments décoratifs ont un contraste indéterminé par l’outil. |
| Revue | Le réviseur a repéré un débordement avec un nom long et a confirmé sa correction sur la pile reconstruite. [Revue indépendante](REVIEW.md). |

`/root/ui_runtime` a intégré Django, `/root/ui_gallery` a produit les composants et les interactions, `/root/ui_styles` a réalisé la présentation. `/root` a assuré l’intégration locale et les tests de parcours. `/root/ui_review` a rendu l’avis indépendant.

Le [registre des preuves](EVIDENCE.md) rattache les contrôles aux fichiers exécutés. La qualification couvre Chromium sous Linux, avec deux dimensions de fenêtre et un contrôle de largeurs supplémentaires. La direction graphique est une proposition du lot. L’authentification relève de FEAT-001.
