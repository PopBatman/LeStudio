# Revue indépendante de cadrage · UI-003-03

Exécutant /root/u303_review, 20 novembre 2026. La [carte Notion](https://app.notion.com/p/41d49e23bbdb81089152dbddcc2e2893) associe l’insertion, la manipulation et l’édition directe au même atelier et au même brouillon versionné. La direction validée de [UI-003-01](../UI-003-01/VISUAL-REVIEW.md) et la [recette du canvas de consultation](../UI-003-02/REPORT.md) fournissent les références d’interface et de rendu.

## Socle contrôlé
Les commandes de [structure](../../../composition/editor.py) traitent sections, occurrences, ordre et parents. Les [règles de placement](../../../composition/placement.py) vérifient les limites et la compatibilité par format. La [bibliothèque](../../../composition/catalogue.py) résout la portée de chaque définition et les médias actifs du site. Le [service de sauvegarde](../../../composition/services.py) verrouille la tête et conserve les révisions. Le [canvas livré](../../../composition/builder_views.py) fournit un rendu en lecture avec un reçu privé.

J’ai rejoué les 26 tests existants des modules tests.test_editor_services, tests.test_editor_web, tests.test_canvas_web et tests.test_builder_canvas. Tous passent dans l’image Studio locale, sur SQLite en mémoire, dans un conteneur jetable sans réseau. Ils couvrent entre autres la conservation des descendants, le refus d’une destination invalide, la confrontation des révisions, le reçu et les droits de lecture.

## Preuves à constituer en réalisation
- Sur deux sites fictifs, distinguer consultation et gestion. Retirer une version ou un média entre proposition et sauvegarde et examiner le diagnostic par occurrence. Vérifier qu’une opération étrangère n’altère aucun historique.
- Copier un conteneur imbriqué, comparer les UUID de chaque descendant, annuler et rétablir. Refuser le déplacement dans son propre descendant et contrôler l’ordre canonique après réouverture.
- Rejouer la même insertion au pointeur, au toucher et au clavier dans une grille. Changer de format, tenter un placement libre en collision et contrôler le guide, le focus et l’état après refus.
- Éditer les quatre familles simples depuis le canvas, enregistrer plusieurs gestes ensemble, puis préparer le rendu de la révision enregistrée. Couper le moteur après l’écriture centrale et vérifier que l’opérateur retrouve le brouillon.
- Éditer simultanément depuis deux sessions, perdre une réponse après sauvegarde puis retenter. Comparer le nombre de révisions et vérifier que la publication et les sites tiers restent identiques.

## Examen du dossier et de la maquette
La spécification couvre les cinq critères de sortie de la carte Notion. Le contrat distingue la surface locale modifiée du rendu Wagtail d’une révision enregistrée. Il décrit la sélection dans un cadre isolé, la destination par identité, la sauvegarde atomique protégée par mandat, la reprise après une réponse perdue et le traitement d’un nouveau reçu de rendu. Les choix sur les versions retirées, le remappage des identités et le responsive se rattachent à des tests identifiés dans la tasklist.

J’ai ouvert la maquette autonome dans Chromium à 360 × 800 px. Après recherche du composant Titre, Entrée sur le résultat et sur le premier guide ajoute un calque. Les commandes Annuler et Rétablir restaurent successivement les deux nombres de calques attendus. Le libellé de saisie locale apparaît. Aucun débordement horizontal général, appel HTTP(S) ou incident JavaScript n’a été observé sur ce trajet.

**Avis favorable pour le cadrage.** Le prototype illustre les commandes et leurs états. La projection géométrique sur le rendu réel, les écritures et reprises concurrentes, les collisions sur trois formats et le contrôle de publication doivent être qualifiés sur la réalisation. La maquette de ce lot n’a reçu aucune nouvelle approbation artistique humaine.

## Revue de la réalisation

La [revue indépendante de la coque et du navigateur](evidence/revue-realisation.md) a identifié deux défauts de reprise. L’essai après correction couvre un refus HTTP 413, une coupure réseau, le retour du focus et la restauration d’un bloc au clavier. Une [vérification complémentaire sous Orca](evidence/realisation-clavier-orca.json) a relevé les libellés effectivement annoncés lors de l’ouverture, de l’ajout d’une section et de l’annulation.

La [revue indépendante du service](evidence/revue-service.md) a identifié le cas de deux blocs superposés ramenés ensuite au même plan. Le test de régression a reproduit ce cas avant correction. Le refus conserve la révision précédente. La [recette de bout en bout](evidence/avis-recette-edition.md) a utilisé deux instances Wagtail.
