# Revue indépendante du cadrage

Le 19 novembre 2026, l’exécutant `/root/editor_review` a rapproché les cinq critères Notion du parcours de création et des services déjà livrés. [Carte de référence](https://app.notion.com/p/41d49e23bbdb8168b7f3e3ad6dca78ba)

## Points d’intégration vérifiés

- Le socle vérifie le mandat, verrouille le site et refuse une deuxième création si une révision existe déjà. La création vierge utilisée dans Pages produit une racine V1. Le résolveur de modèles peut livrer un document V3, le faire valider, renouveler les identités puis revalider le résultat pour le site destinataire. En V3, les sources privées doivent attester leur portée. [Services de composition](../../../composition/services.py)
- La fiche Site donne déjà accès à Pages, Menus, Bibliothèque et Apparence ainsi qu’au panneau de raccordement. La reprise de l’éditeur doit utiliser la tête existante, même sur un site dépourvu de liaison moteur. Une modification de structure doit conserver les menus indépendants, les versions épinglées et les réglages d’apparence. [Fiche actuelle](../../../templates/registre/site.html) · [Service d’apparence](../../../composition/appearance.py)
- Les primitives Cotton du projet comprennent champ, bouton, alerte et état vide. La tasklist prévoit l’essai du lecteur d’écran sur l’application réalisée et la conservation des observations en complément des preuves de la maquette. [Plan de vérification](TASKLIST.md)

## Essai indépendant du modèle

Dans une base SQLite en mémoire migrée par l’image Studio locale, j’ai créé deux sites fictifs puis fourni le modèle Présentation à `creer_brouillon` via un résolveur local. Les deux copies possédaient chacune une page, une section et deux blocs. Les huit UUID générés étaient distincts entre eux et de ceux du modèle. Les deux têtes relues avaient conservé leur origine, le format V3 et l’ordre titre puis texte. Une seconde création vierge a été refusée sur chacun des deux sites. L’essai vérifie la fixture avec le socle existant. [Modèle examiné](evidence/template-v3.json)

## Parcours et verdict

Dans Chromium sur un écran de 360 × 740, j’ai activé le lien de saut par Entrée, examiné les trois points de départ et créé une page vierge avec une section. J’ai ouvert séparément le modèle « Présentation d’activité », sélectionné le titre dans l’inspecteur, puis activé « Descendre » au clavier. Après retour à la fiche et reprise, le texte précédait toujours le titre dans la révision simulée. Le document tenait dans la largeur de l’écran aux étapes vérifiées. J’ai signalé un écart de contenu entre le modèle et sa représentation et rejoué le parcours après correction. Le titre et le texte affichés correspondent désormais à la fixture. [Maquette interactive](evidence/maquettes.html)

La spécification associe les cinq critères Notion à une recette vérifiable. Le contrat décrit la création V3 depuis les deux départs, la reprise de la création historique de Pages, l’insertion, le déplacement et les diagnostics de références anciennes. Le choix Figma reste informatif jusqu’à la disponibilité d’une proposition autorisée du lot 08. Les contrôles d’accès, l’essai de concurrence, la persistance entre sessions et la qualification au lecteur d’écran sur Django sont inscrits au plan de développement. [Spécification](SPEC.md) · [Contrat](ARCHITECTURE.md) · [Sécurité](SECURITY.md)

**Avis favorable au passage en READY pour le cadrage.** Les preuves actuelles couvrent la maquette et l’essai du modèle avec le socle livré. Les tests et la revue de l’éditeur Django relèvent de sa réalisation.

## Revue indépendante de la réalisation du 19 novembre 2026

L’exécutant `/root/structured_review` a suivi une requête depuis la fiche et l’inspecteur jusqu’à l’écriture de la révision. L’autorisation du site est contrôlée à la lecture, puis sous verrou à l’écriture. L’origine, la définition et la destination sont résolues par Studio. Les deux courses PostgreSQL opposant l’atelier aux panneaux Pages et Apparence ont chacune produit un seul enregistrement sur la base de départ. [Services](../../../composition/editor.py) · [Résultats de concurrence](evidence/editor-concurrency-postgres.log)

Un essai indépendant sur Django et SQLite en mémoire a repris une V2 contenant une section en grille, des dispositions distinctes sur tablette et téléphone, un conteneur et un thème. La soumission des valeurs initiales a conservé la tête. Le changement d’espacement a créé une V3 fille avec les deux surcharges et le thème intacts. Le changement de variante du conteneur a conservé sa propre grille. L’ancienne révision a été relue à l’identique et les cinq vues de composition ont répondu sur la nouvelle tête.

La revue a conduit à vérifier le traitement des champs textuels historiques nommés `layout` et `media`, le rejet d’une destination HTTPS mal formée avec restitution du formulaire, l’édition d’une version épinglée retirée et la distinction des pages homonymes par leur chemin. Les corrections sont présentes. J’ai rejoué les 25 tests HTTP, service et fiche concernés avec succès. Les contrôles clavier, la consultation en largeur de 320 px et les annonces d’Orca sont consignés dans la recette navigateur de l’équipe. [Tests HTTP](../../../tests/test_editor_web.py) · [Parcours Chromium](evidence/navigateur.json) · [Énoncés Orca](evidence/application-orca.json)

**Avis favorable à la réalisation de FEAT-003-04.** La qualification transverse auprès d’utilisateurs relève de UI-002.
