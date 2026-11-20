# Examen visuel préalable du canvas

La [maquette du canvas](evidence/maquette.html) reprend la coque, la typographie et l’illustration d’Atlas du Sud approuvées dans UI-003-01. Ouvrir le HTML téléchargé dans un navigateur. Les deux pages, les révisions R7 et R8 et les occurrences sont des données fictives. Le rendu est illustré dans le fichier autonome.

| Situation | Geste à essayer | Résultat observé dans Chromium |
| --- | --- | --- |
| [Sélection sur ordinateur](evidence/selection-bureau.png) | Activer un titre depuis la page puis un texte au clavier depuis les calques ; changer de page. | Le contour, l’état pressé et l’UUID de l’inspecteur suivent la même occurrence. Le titre de la seconde page reçoit son propre identifiant. |
| [Péremption sur tablette](evidence/rendu-perime-tablette.png) | Choisir le scénario périmé et consulter l’inspecteur. | R7 est affichée et R8 demandée. Le texte historique reste visible ; la sélection du rendu est suspendue. |
| [Lecture de repli sur mobile](evidence/lecture-mobile.png) | Simuler l’indisponibilité puis activer « Lire la structure » avec Entrée. | La page rendue est retirée. Le focus rejoint les calques du brouillon R8 en lecture. « Actualiser le rendu » rétablit R8 dans la simulation. |
| Format et diagnostic | Choisir la vue mobile sur ordinateur. Passer par préparation, composant incompatible et moteur indisponible. | La page se limite à 360 px, les erreurs ont des libellés distincts, la disponibilité revient après actualisation. |

Captures prises à 1440 × 900, 820 × 1050 et 360 × 800 (page entière pour la dernière). Chromium 156.0.8078.4 a également contrôlé l’absence de débordement horizontal général à 320 px, d’exception JavaScript et de requête HTTP(S). Cette revue porte sur la maquette. La direction artistique de base a été approuvée dans UI-003-01. Aucune nouvelle approbation humaine de ces écrans n’a été recueillie.

Pour la réalisation, comparer la même page et la même révision sur le moteur et dans le canvas aux trois largeurs, y compris après chargement des polices, défilement et changement de taille. Vérifier la précision du surlignage, la conservation du focus, les annonces au lecteur d’écran et la désactivation effective d’un reçu périmé. Les captures de cette page ne couvrent pas ces mesures du produit.

## Examen de la réalisation dans Chromium
Les captures appariées comparent le document de référence et le canvas du même reçu à 1 200, 820 et 390 px de largeur interne. [Comparaison des pixels](evidence/comparaison-pixels.json) · [Coque avec sélection](evidence/canvas-site-b-bureau.png) · [Historique](evidence/canvas-revision-historique.png) · [Lecture de repli](evidence/canvas-repli-lecture.png).

Le laboratoire a vérifié les cibles imbriquées et répétées, le tactile et le défilement vers le dernier bloc au clavier. Les [mesures du contour](evidence/contour-occurrences.json) portent aussi sur le redimensionnement et le zoom à 125 %. Orca a généré les annonces du premier calque, de la sélection et de la largeur mobile sur une session de recette isolée. Le séparateur entre le type du bloc et son texte a été corrigé puis revérifié. Les [énoncés observés](evidence/realisation-orca.json) proviennent d’un pilotage clavier automatisé.
