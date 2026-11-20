# Revue visuelle du canvas

Ouvrir la [maquette interactive](evidence/maquettes.html) dans un navigateur. « Atelier Papier » est un site fictif. Pour comparer les deux éditeurs, déplacer un bloc dans le canvas, puis ouvrir **Éditeur structuré**. Les deux vues utilisent la même sélection, le même ordre de lecture et le même numéro de révision simulé. La police DM Sans et sa licence sont embarquées dans le fichier.

## Parcours examinés

| Situation | Interaction et résultat observé dans Chromium |
|---|---|
| Flux sur bureau | Le lien de saut reçoit le premier focus et conduit au contenu. Passer le parent en grille affiche deux colonnes. Le bouton déplacé au pointeur devant le titre devient le premier frère dans les deux vues. Après sélection de la dernière position au clavier dans la structure, le canvas présente le bouton en dernier. [Grille sur bureau](evidence/flux-bureau.png) |
| Placement libre | Le texte sélectionné passe en placement libre. Le déplacement à la souris change ses coordonnées dans le repère du parent. Le cadre et le premier plan situent le texte par rapport au titre. Le sélecteur de l’inspecteur permet d’atteindre un bloc couvert. Les champs X, Y, largeur, hauteur et plan donnent accès aux mêmes réglages depuis les deux vues. [Superposition sur bureau](evidence/placement-bureau.png) |
| Formats indépendants | Avec une largeur de base de 60 %, régler la largeur tablette à 45 %, puis passer le bloc mobile en flux. La tablette relue conserve 45 % et le bureau 60 %. En retirant uniquement la surcharge de position X sur mobile, la largeur propre au mobile reste à 66 %. Le parent possède une commande distincte de retour à la disposition héritée. [Flux sur téléphone](evidence/flux-mobile.png) |
| Débordement | Saisir X à 92 % et largeur à 66 %. Le résumé reçoit le focus, la révision reste identique et les deux saisies restent disponibles pour correction. Le document tient à 320 px sur l’écran d’erreur. [Erreur sur téléphone](evidence/erreur-mobile.png) |

Les quatre captures présentent l’état en pleine page. L’interface conserve l’ordre canvas puis inspecteur sur téléphone, avec un lien de saut entre les deux. Le banc d’essai a contrôlé l’absence de défilement horizontal global à chaque capture et n’a relevé ni exception JavaScript ni requête HTTP. [Relevé des essais du prototype](evidence/examen-maquettes.json)

## Fidélité et recette à réaliser

Le prototype illustre une section, trois composants initiaux et l’insertion d’un texte. La révision et les valeurs vivent en mémoire jusqu’au rechargement. Les formats de travail représentent 1 200, 820 et 390 px ; le papier se réduit pour tenir dans l’espace visible. Une mesure de cette maquette ne qualifie donc pas le rendu CSS du site à ces dimensions. Le test applicatif devra employer un véritable espace de rendu de largeur connue, y compris aux seuils de 768 et 1 024 px.

La recette Django devra vérifier les poignées de redimensionnement, le drag tactile avec défilement et annulation, le placement dans des conteneurs imbriqués, l’historique après réouverture, les conflits inter-éditeurs, la lecture seule et les changements d’habilitation. Elle devra éprouver les textes longs et les médias réels aux trois formats, les annonces du lecteur d’écran et la réactivité sur de grands brouillons. La revue métier et la direction artistique transversale restent suivies dans UI-002.
