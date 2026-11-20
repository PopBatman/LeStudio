# T02 — Références et démonstration à préparer

Version 1 · lot d’architecture, UI requise = non dans Notion. Le cadrage ne modifie aucun écran ; il ne nécessite pas de nouvelle maquette de coque ni de captures d’implémentation. Ce document fixe les observations visuelles nécessaires à la réalisation du modèle.

Références réemployées : [prototype adopté du parent](../UI-004/evidence/prototype-adopte.html), [contrat UX T01](../UI-004-01/REFERENCE-PRODUIT.md), [comparaison installée/cible R18](../UI-004-01/evidence/comparaison-reference.html). Le prototype est simulé ; la cible de T01 est illustrative ; aucune de ces pièces ne prouve le nouveau modèle.

| Composition | Variantes à comparer | Observation attendue |
|---|---|---|
| C1 : titre + image dans deux sections/conteneurs | Flux puis grille, déplacement X et transfert, largeur titre 100 % puis 50 % | Même UUID, contenu/version/média ; voisins et retours à la ligne définis |
| C2 : contenu variable | Titre deux puis cinq lignes, image paysage remplacée par portrait ; 390/820/980/1200 px | Aucun texte masqué, ratio/boîte explicites, hauteur du parent et voisins cohérents |
| C3 : vide / imbriqué | Section vide, conteneur, feuille et descendant | Cibles valides et interdites ; aucun cycle ni déplacement partiel |
| C4 : composition superposée conditionnelle | À rattacher à une référence explicite avant d’activer un nouveau libre borné | Bornes/calques/repli mobile/ordre de lecture ; documenter N/A si non nécessaire |
| C5 : historique | Mêmes déplacements avec Escape, capture perdue, undo/redo cible + voisins | État provisoire absent du document et de l’historique ; focus restitué |

Référence réelle reprise pour T03 : Tennis AI / Accueil, UUID cbf41f07-a35b-4043-81df-98e91c8118a5, audit R18 schéma 4. T01 a observé deux sections, deux conteneurs, deux boutons et un texte, sans titre/image ni média disponible. Ces éléments manquants sont préparés explicitement au lancement T03 ; aucune recette T02 ne suppose leur présence actuelle. Les métadonnées T01 sont historiques et non une lecture de tête rejouée ici.

En réalisation T02 : utiliser données fictives et média autorisé sur le banc Wagtail, avec manifestes versions/UUID et captures navigateur identifié. Mesurer aussi les seuils 767/768/1023/1024, zoom/scroll et chargement police/image pour les repères. T03 vérifie la surface interactive et le clavier/focus ; T18 qualifie fluidité, lecteur d’écran et tactile matériel. Les captures seules ne démontrent ni accessibilité ni sauvegarde.

