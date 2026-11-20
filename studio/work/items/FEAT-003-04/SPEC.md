# FEAT-003-04 — Éditeur structuré et parcours de création

L’opérateur veut remplir une page vide depuis Studio, puis retrouver son contenu dans le même ordre à la prochaine ouverture. Depuis la fiche Site, **Atelier du site** crée le premier brouillon ou reprend celui qui existe déjà. Pour une fiche comme Tennis AI, qui possède déjà des pages et des menus, le parcours attendu est la reprise directe. Le raccordement Wagtail est facultatif.

## Entrée depuis la fiche

| Situation | Action et résultat attendus |
|---|---|
| Gestion, aucun brouillon | Choisir « Présentation d’activité » pour démarrer avec un titre et un texte, ou « Page vierge » pour partir de l’accueil vide. Examiner le choix et confirmer. Annuler conserve l’état vide. |
| Proposition Figma | Montrer « Indisponible » et expliquer qu’une proposition analysée et acceptée sera nécessaire. Le lot 08 fournira cette source au même service de création. |
| Brouillon déjà présent | Afficher sa révision et proposer de reprendre l’atelier. Une demande de création simultanée retrouve la tête créée par le premier opérateur. |
| Lecture seule | Consulter les pages, la structure et les propriétés enregistrées. Expliquer l’état vide ou l’accès en lecture. |
| Version inconnue | Afficher la révision et l’incompatibilité avec les informations autorisées. Conserver l’instantané pour reprise par une version compatible. |

Les entrées Pages, Menus, Bibliothèque et Apparence restent accessibles depuis la fiche. Le raccourci existant de création vierge dans Pages utilise le même brouillon que l’atelier. Une fiche ouverte en consultation réutilise les données de raccordement du lot ARCH-002-01.

## Composer une page

1. Sélectionner une page du site. Sur une page vide, ajouter une section, puis un premier bloc. Les opérations sur la hiérarchie des **pages** et les conséquences d’un changement de chemin utilisent les services de Pages et Menus.
2. Choisir une définition et une version disponibles pour le site. Par exemple, insérer un **titre**, un **texte**, puis un **bouton**, et renseigner son libellé et sa destination HTTPS. Pour une image, choisir un média autorisé et saisir l’alternative textuelle. En l’absence de média, expliquer le prérequis.
3. Sélectionner une section, un conteneur ou un bloc dans la structure. L’inspecteur présente les champs de la définition et les réglages applicables. Identifier la sélection par son UUID pour que deux titres identiques restent éditables séparément.
4. Réordonner les sections dans la page et les blocs dans leur section ou conteneur. Offrir un choix explicite de destination et de position, utilisable au clavier. Avant un retrait, montrer l’élément, le nombre de descendants et les conséquences. Annuler conserve la révision.
5. Enregistrer et rouvrir le brouillon. Retrouver textes, version des composants, variantes, conteneurs, ordre et liens des menus. Un champ invalide conserve la saisie. En cas de conflit, montrer la révision courante et permettre une nouvelle soumission après comparaison.

## Contrat des éléments d’interface

| Élément | Données, interaction et états de recette |
|---|---|
| Entrée Atelier et choix de départ | Site autorisé, droit, tête et origine disponible. Sélection native, description du contenu initial, création explicite. Pendant soumission, annoncer l’action et éviter les doubles clics. |
| Structure de la page | Titres et identités de la page, sections et occurrences ordonnées. Afficher la profondeur, la sélection, l’état vide et les actions permises. Libellés distincts pour la hiérarchie des pages et le contenu de la page sélectionnée. |
| Inspecteur et formulaire | Valeurs enregistrées, nouvelle saisie, version épinglée et erreurs par champ. Relier les erreurs aux champs, déplacer le focus vers le résumé ou le premier champ en erreur. Un succès annonce la révision. Après retrait, replacer le focus sur un élément survivant. |
| Petit écran et clavier | Ordre de lecture page → structure → inspecteur. Prévoir un accès direct à la sélection et un retour à la structure, des commandes de déplacement sans glisser-déposer et des noms accessibles. Vérifier contrastes, longs libellés et annonces avec un lecteur d’écran dans la recette applicative. |

## Critères de la carte traduits en tests

| Critère | Vérification observable |
|---|---|
| Modèle et page vierge rééditables | Créer A depuis le modèle, B depuis zéro. Comparer les formes métier, la provenance et les UUID distincts. Enregistrer puis rouvrir chaque site. |
| Modifier et réordonner | Dans A, insérer un conteneur, y déplacer un texte, modifier un titre et réordonner deux blocs. Recharger. Comparer ordre, parent, valeurs et ancienne révision. |
| Évolution Figma | Avant 08, vérifier l’état indisponible sur l’écran de création et le refus d’une soumission directe. À l’intégration de 08, tester une proposition acceptée, versionnée et autorisée dans le même éditeur. |
| Erreur et isolation | Proposer un champ invalide, un identifiant d’un autre site, une écriture en lecture seule et une révision périmée. Comparer les refus, les données visibles et le nombre de révisions. |
| Clavier et écran étroit | Refaire création, sélection, insertion, déplacement, annulation et reprise sans souris, sur bureau et téléphone. Contrôler focus, absence de débordement, annonces et conservation des valeurs après erreur. |

Le canvas appartient à FEAT-003-05, l’intégration éditoriale avancée avec Wagtail à FEAT-003-06, l’aperçu à FEAT-004 et l’application au site à FEAT-005. [Carte Notion](https://app.notion.com/p/41d49e23bbdb8168b7f3e3ad6dca78ba) · [Architecture](ARCHITECTURE.md) · [Maquettes](VISUAL-REVIEW.md) · [Recette](TASKLIST.md)
