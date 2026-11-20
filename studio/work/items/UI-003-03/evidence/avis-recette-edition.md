# Recette navigateur de UI-003-03

La recette du 20 novembre 2026 a démarré depuis les fiches Site de deux sites fictifs. Studio et les deux instances Wagtail utilisaient PostgreSQL et leurs propres certificats mTLS. Les gestes ont été exécutés avec Chromium. Le glissement tactile utilise des événements tactiles Chromium. Le fichier Figma provient d’un fournisseur simulé et a suivi le processus de confirmation de l’import dans Studio.

| Situation | Observation |
| --- | --- |
| Page modèle longue du site A | La sélection d’une image dans les calques reste active au passage en édition. Le glissement d’un bouton depuis la bibliothèque, puis la modification du bouton, du titre, du texte et de l’image produisent un brouillon local. La copie d’un conteneur et de son image crée deux nouvelles identités. Annuler, rétablir, supprimer puis annuler restaurent les mêmes occurrences. |
| Réponse de sauvegarde perdue | La première requête est exécutée, puis sa réponse est coupée dans le navigateur. Le second clic envoie exactement le même JSON. Studio crée uniquement R5. Les textes sont retrouvés sur le rendu Wagtail privé, y compris après réouverture depuis la fiche. |
| Deux gestionnaires sur R5 | Le premier enregistre R6. Le deuxième reçoit HTTP 409 et retrouve sa saisie dans l’éditeur mobile. La page tient dans un écran de 390 pixels. |
| Page Collections initialement vide | Une section, un titre et un texte sont ajoutés au clavier. Le glissement tactile réordonne le texte sous le titre. L’enregistrement suivant produit R7 et les deux contenus se retrouvent dans Wagtail. |
| Droit de gestion retiré pendant l’édition | Studio refuse le lot valide avec HTTP 403 et désactive Enregistrer. La révision reste R7. Un lecteur du site A voit le canvas, tandis que le site B lui renvoie HTTP 404. |
| Passerelle du moteur A arrêtée | Studio enregistre R8 et explique que l’aperçu pourra être préparé à nouveau. Après le redémarrage de la passerelle, Wagtail rend le nouveau texte. |
| Page issue de Figma sur le site B | L’éditeur tablette conserve l’identité du titre. R6 contient le nouveau texte et le moteur B le rend. La page modèle de B reste identique. |
| Sites publics | Les deux réponses HTTP publiques, les révisions Wagtail, les identifiants publiés et les renditions sont identiques avant et après les cinq nouvelles révisions Studio. |

Le premier essai de glissement natif a révélé que le navigateur annulait le placement après le début du geste. Le premier essai tactile a également montré que le clic sur Enregistrer pouvait être absorbé juste après le dépôt. Les parcours ci-dessus ont été rejoués après correction. Les mesures et captures portent le préfixe `realisation-`. Les comparaisons des deux moteurs figurent dans `non-publication.json` et `pages-publiees.json`.

La contre-épreuve responsive applique au titre de Collections un placement mobile libre à X 20 %, Y 30 px et largeur 55 %. Bureau et tablette gardent leur flux. Revenir au format mobile restaure sa position et « Hériter du bureau » rétablit le flux. Un placement X 90 % avec largeur 50 % a été refusé avant inscription dans l’historique. Sur B, le dépôt au pointeur d’un conteneur dans sa descendance a affiché le guide de refus et son motif. Aucune des deux sessions n’a créé de révision. Les captures correspondantes sont `realisation-placement-libre.png` et `realisation-depot-refuse.png`.
