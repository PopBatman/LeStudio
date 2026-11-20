# FEAT-003-03 — Bibliothèque de composants et apparence

L’opérateur ouvre la bibliothèque depuis le contexte du site. Il voit les composants partagés et ceux développés pour ce site. Il peut comparer les variantes d’une version, régler l’apparence du brouillon et identifier la page et le bloc concernés lorsqu’une référence devient indisponible. Ce parcours fonctionne avant le raccordement du site à Wagtail.

## Scénarios à livrer

| Critère Notion | Exemple de recette après développement |
|---|---|
| Identité, origine, version et paramètres validés | Examiner un bouton global et un composant de site. Afficher portée, provenance et version exacte. Enregistrer une variante autorisée, refuser une propriété inconnue ou un type erroné. Sur échec, la tête du brouillon reste la même. |
| Variantes isolées par site | Sur le site A, changer la couleur d’accent et la variante d’une occurrence. Recharger A puis B. Le changement apparaît sur A, l’autre occurrence conserve ses réglages propres et le document de B reste identique. Réinitialiser une surcharge redonne la valeur héritée. |
| Promotion contrôlée | Un gestionnaire de B ne trouve pas le composant spécifique à A. Proposer la version de A, contrôler l’origine des créations, remplacer le média propriétaire et faire examiner la version destinée au partage. Un refus laisse le catalogue global identique. Après acceptation, B peut choisir explicitement la version globale. |
| Nouvelle version globale | Publier une seconde version dans la bibliothèque, relire le site déjà configuré et sa révision historique. Ses blocs pointent toujours sur la première. Une adoption explicite vérifie les paramètres et produit une nouvelle révision du seul brouillon choisi. |
| Référence manquante ou incompatible | Ouvrir un brouillon qui contient une ancienne définition ou un média indisponible. Afficher l’occurrence, sa version et le diagnostic, préserver la révision et proposer une correction explicite. Une révision présentant ce diagnostic est signalée comme impropre à une future application. |

## Catalogue et parcours du premier lot

Le catalogue de départ comprend **titre, texte, conteneur, image et bouton**. L’équipe livre les types, leurs rendus et leurs schémas de paramètres. Un opérateur de site peut choisir les variantes disponibles et leurs valeurs autorisées. L’apparence couvre les couleurs, les polices embarquées, les espacements et les médias référencés. Les paramètres propres à une occurrence s’appliquent à ce bloc. La fiche de définition rend visibles l’origine et la version utilisée. Le catalogue d’un site reste consultable si son brouillon est vide. Sans brouillon, renvoyer vers la création vierge déjà disponible dans Pages. Avec une page encore vide, les réglages du site et les exemples de la bibliothèque restent accessibles. La composition générale de nouvelles sections et occurrences appartient à l’éditeur 04. Le lot 03 inclut le réglage, le remplacement et le retrait explicite d’une occurrence existante, ainsi que la réparation d’une référence indisponible.

Les vues spécialisées **Bibliothèque** et **Apparence** appartiennent au lot 03. Une démonstration de composant utilise des valeurs fictives. L’éditeur structuré de pages (04), le canvas (05), les contenus éditoriaux reliés à Wagtail (06) et l’import Figma (08) consommeront ce contrat. FEAT-004 permettra d’examiner le rendu d’une page entière et FEAT-005 d’appliquer une composition. La sauvegarde d’un réglage dans le brouillon demeure locale à Studio.

## Décisions proposées

Adopter un schéma V3 à la première modification qui le nécessite, épingler les versions et réserver la revue de promotion à une seconde personne habilitée. Ces choix de conception sont proposés dans le cadre du mandat de cadrage. Le développement devra démontrer la compatibilité avec les pages, les liens et les menus livrés en 02.

[Carte Notion](https://app.notion.com/p/41d49e23bbdb81d69beec505505929a3) · [Architecture](ARCHITECTURE.md) · [Maquettes](VISUAL-REVIEW.md) · [Recette](TASKLIST.md)
