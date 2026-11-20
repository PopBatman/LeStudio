# Existant et décisions de périmètre
La [carte Notion](https://app.notion.com/p/41d49e23bbdb81089152dbddcc2e2893), la [vision produit](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539) et le [lot parent](../UI-003/SPEC.md) demandent une édition directe dans un atelier unique. Le [prototype UX approuvé](../UI-003-01/VISUAL-REVIEW.md) sert de référence pour la bibliothèque, la page et l’inspecteur. La [livraison de UI-003-02](../UI-003-02/REPORT.md) fournit le rendu privé et la sélection identifiée de blocs réels.

| Source Studio | Réemploi ou écart |
| --- | --- |
| composition/catalogue.py, catalogue_v1.py, appearance_contract.py | Les définitions ont une clé, une version et une portée. Le service fournit les médias du site et les propriétés typées du composant. Catégories, vignettes et recherche sont à présenter dans la bibliothèque de l’atelier. |
| composition/editor.py, services.py | La V1 sait créer, modifier, déplacer et retirer des occurrences. Elle enregistre les commandes structurelles individuellement. La V2 doit permettre plusieurs gestes annulables avant une sauvegarde atomique. |
| composition/placement.py, validation.py | Les surcharges tablette/mobile se résolvent depuis la base. Le validateur vérifie les limites de grille et de placement ; l’interface doit rendre visible la destination et qualifier les collisions. |
| composition/builder_views.py, static/ui/builder*.js | L’iframe privée rend une page enregistrée et transmet la sélection de l’occurrence. Les calques et l’inspecteur sont dans Studio. Les mesures de sélection ne confèrent aucun droit d’écriture. |
| composition/editorial.py et depots/imports.py | Les droits et confirmations de références éditoriales existent déjà. Une origine Figma validée aboutit au même modèle canonique. |

Le contrôle de départ a rejoué 30 tests existants dans l’image Studio locale, sur SQLite en mémoire et sans réseau. [Journal](evidence/socle.log)
