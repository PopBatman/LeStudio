# Sources de cadrage
Le [sous-lot Notion](https://app.notion.com/p/41d49e23bbdb81ba839be769de8b1248), le [parent UI-003](../UI-003/SPEC.md) et la [vision produit](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539) demandent une manipulation directe et trois origines pour un document canonique. La [maquette du parent](../UI-003/evidence/maquette.html) présentait les panneaux et les cas de révision. Le prototype du sous-lot étend l’examen à un parcours depuis la fiche et au retour à la gestion.
 
| Existant Studio examiné | Application au cadrage |
| --- | --- |
| registre/urls.py, templates/composition/editor.html et canvas_surface.html | Les deux entrées Structure et Canvas actuelles partagent les données. La cible rassemble navigation, sélection et propriétés dans le même espace. |
| composition/editor.py, placement.py, services.py | Les sections accueillent les blocs autorisés. Une modification cible une occurrence ; l’ordre et la révision gouvernent la sauvegarde. |
| composition/preview_views.py et templates/composition/preview_view.html | L’aperçu réel se prépare par site, révision et page. Illustrer le retard et la panne dans le prototype, réserver la preuve de fidélité au lot 02. |
| depots/imports.py et rapport FEAT-003-08 | Reprendre un brouillon confirmé par l’opérateur. Le graphiste invité ne reçoit aucun accès à l’atelier. |
| docs/COMPOSANTS-UI.md, frontend/gallery.css et captures des lots 04/05 de FEAT-003 | Reprendre la lisibilité des libellés, le focus visible et les messages d’état. Rendre la sélection et les opérations courantes perceptibles dans la page. |
