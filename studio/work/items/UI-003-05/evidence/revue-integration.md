# Revue indépendante des entrées et des articles

Le 20 novembre 2026, la revue de la navigation a porté sur les routes `atelier/` et `atelier/canvas/`, le choix d’entrée de la fiche Site, la résolution côté serveur de la révision/page/section/occurrence et leur utilisation effective dans le navigateur.

Le premier passage a relevé deux pertes de contexte. Le serveur de compatibilité transmettait les coordonnées dans l’URL, mais le canvas de préparation ne restaurait ni la largeur ni la sélection du signet. Le formulaire V1 périmé affichait le refus 409 et renvoyait à la première page. Ces deux points ont été corrigés puis rejoués.

## Signet et formulaire périmé

Un serveur Studio temporaire du banc, configuré en `compatibility`, a permis de tester les anciennes URL en parallèle de la coexistence. Chromium a suivi un signet du site fictif B et vérifié le contenu de l’inspecteur sur le bloc attendu. Le passage par « Afficher le rendu » a conservé sa sélection et sa largeur de 455 px sur le reçu privé Wagtail. Les signets vers une section et un bloc de R2 ont permis leur consultation après la création de R3, avec l’édition indisponible dans l’historique. Un identifiant absent a produit un repli explicite. Un ancien POST autorisé avec une commande de retrait a reçu 409, et son lien de relecture a conservé la page et le bloc. La tête est restée R3. Le serveur temporaire a été arrêté après l’essai. [Résultats Chromium](signet-canvas.json)

Les tests Django ont également couvert les trois modes de navigation, le POST sans mandat de gestion, le site hors périmètre, le conflit de tête, le rejeu et la réouverture en V1 après une écriture V2 sur les schémas 1 à 4. [Exécution isolée des 18 tests](articles-et-navigation.log)

## Article Wagtail

Sur le même site fictif, Chromium a vérifié la page Wagtail 4 de l’instance raccordée. Sa révision publiée était 2. Le brouillon Studio est resté en R2 après vérification. La confirmation de cette observation a créé R3 et renvoyé à l’occurrence introduite dans la page Atlas du Sud. La Bibliothèque a ouvert la référence de cette même occurrence et son lien de retour a repris ses coordonnées. [Observation](article-wagtail.json) et [capture](article-wagtail.png)

Les tests de l’écran métier ont utilisé un transport simulé pour obtenir successivement une nouvelle publication, son adoption explicite, un remplacement dont la publication change avant confirmation et une source indisponible. Ils contrôlent aussi le maintien de la référence lors d’une simple consultation, l’historique en lecture seule, le refus après retrait de la gestion et l’isolation des sites. La modification des publications des deux moteurs de recette est ainsi restée hors du test de divergence. [Tests exécutés](articles-et-navigation.log)

Ces vérifications techniques portent sur les parcours rejoués. L’appréciation humaine de la parité ergonomique et l’autorisation de bascule restent à consigner séparément.
