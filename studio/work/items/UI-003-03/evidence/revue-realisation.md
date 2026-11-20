# Revue indépendante de réalisation · UI-003-03

La revue porte sur la coque HTTP Django, le modèle de travail JavaScript, les commandes de l’inspecteur et le retour au canvas Wagtail. L’auteur du service de lot a relu ici les changements d’intégration réalisés par les autres intervenants.

## Accès et reprise

La consultation, la vérification du mandat et la sauvegarde passent par des vues réservées aux opérateurs authentifiés. La sauvegarde accepte un POST JSON protégé par CSRF. Le service recontrôle le mandat avant de répondre à une répétition. Le sélecteur d’une révision historique et le mandat de lecture donnent accès au parcours de consultation. Le test HTTP vérifie également le conflit de base, le rejet d’un corps illisible et le retour identique après répétition.

La réponse à un conflit propose d’examiner la dernière sauvegarde dans un autre onglet. Une confirmation précède l’abandon des gestes locaux. La clé de répétition est conservée avec le contenu exact du lot en mémoire. La création du reçu Wagtail intervient après la réponse du service de sauvegarde.

## Accessibilité des gestes

La bibliothèque et les calques utilisent des boutons natifs. Les champs ont des libellés, le calque sélectionné porte un état accessible et les messages de placement disposent d’une région de statut. Le sélecteur de destination permet de choisir le parent et un voisin au clavier. Échap annule le placement. Après une suppression, le code rend le focus au voisin ou au parent. L’examen du code ne constitue pas un essai avec lecteur d’écran.

## Incidents reproduits avant correction

Dans Chromium, sur le site fictif du laboratoire, un ajout de section depuis R4 a créé une modification locale. Une interception de la requête de sauvegarde a renvoyé un refus HTTP 413. L’éditeur l’a présenté comme un résultat inconnu et a désactivé Annuler et Revenir au canvas. Dans le même essai, une coupure du réseau a supprimé la coque privée. Le retour en ligne n’a pas restauré l’éditeur. Ces deux comportements empêchaient la reprise sans perte. Le parcours a utilisé uniquement un changement local et une réponse HTTP simulée.

La relecture a aussi identifié une différence entre le contrôle local et le contrôle serveur pour une superposition volontaire avec deux blocs au même plan. La revue a transmis ces constats aux auteurs de l’intégration.

Une contre-vérification dans Chromium a exercé le parcours sans souris sur le site fictif. Entrée a donné le focus au sélecteur de destination et Échap l’a fermé. L’insertion d’un titre a ajouté un calque. La saisie « Édition clavier » a été confirmée depuis le formulaire. Après suppression, le focus était sur un bouton de titre survivant. Annuler a restauré le texte, le nombre de calques et l’identité du bloc sélectionné. Aucun enregistrement serveur n’était nécessaire pour ces gestes.

## Contre-recette des corrections

Le même essai Chromium sur R4 affiche désormais le motif du 413. Annuler et Revenir au canvas restent utilisables immédiatement. La coupure masque la zone privée ; après reconnexion et revérification du mandat, la vue de travail réapparaît avec « Base R4 · Modifications non enregistrées » et son bouton Annuler actif. Le modèle local refuse désormais un nouveau chevauchement entre plans identiques avant de confirmer le geste. Les deux blocages de reprise constatés dans cette revue sont levés.
