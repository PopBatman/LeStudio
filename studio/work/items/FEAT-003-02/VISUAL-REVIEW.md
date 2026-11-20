# Pages et navigation dans l’Atelier

Depuis la fiche Site du parcours parent, l’opérateur ouvre le brouillon, puis **Pages** ou **Menus**. La [maquette autonome](evidence/maquettes.html) s’ouvre localement. Les données de Maison des dunes sont fictives. L’en-tête, la police DM Sans embarquée, les couleurs et le focus reprennent l’identité visuelle de Studio.

| Parcours | Ce que l’opérateur peut examiner |
|---|---|
| Consulter l’arborescence | Sélectionner « Carnet de saison » indique que cette page existe hors des menus. La racine garde le chemin `/`. [Vue Pages sur ordinateur](evidence/pages-bureau.png) |
| Modifier une branche | Sélectionner « La maison », changer son segment d’URL et examiner les chemins. La comparaison énumère aussi le chemin de « Les chambres » et les libellés des liens internes des deux menus touchés. L’opérateur confirme ou annule. [Impact du renommage](evidence/chemins-bureau.png) |
| Supprimer une branche | La confirmation attend une décision pour **chaque entrée** concernée. L’opérateur peut retirer l’entrée ou choisir une cible survivante. L’annulation conserve la branche et les menus. [Résolutions sur téléphone](evidence/suppression-mobile.png) |
| Consulter les menus | Le principal présente un groupe, deux pages enfants et un lien externe HTTPS. Chaque entrée indique ses formats de visibilité. Dans « Pied de page », « Monter Contact » modifie son ordre. [Menu sur téléphone](evidence/menus-mobile.png) |
| Lecture, refus, concurrence | Les scénarios en pied de maquette proposent la lecture seule, le refus sans identité du site et le conflit simulé. Après conflit, « Relire la révision courante » garde la proposition visible pour comparaison. |

## Examen avant développement

Chromium a exécuté les parcours sur 1440, 390 et 320 pixels. Le lien de saut, le passage de Pages à Menus et l’activation des commandes utilisent les contrôles natifs. À l’examen d’un changement, le focus arrive sur le titre de l’impact. Le contrôle automatisé a vérifié l’annulation, le retrait et le reciblage distincts, le conflit, les restrictions de lecture et l’absence de débordement horizontal aux points observés. Les captures illustrent le prototype. [Résultats du navigateur](evidence/examen-maquettes.json)

Les changements sont simulés en mémoire. Les formulaires de création de page et de menu, le déplacement vers un autre parent et l’édition de la visibilité restent à réaliser selon le contrat du lot. Au développement, éprouver sur Django le rechargement persistant, les erreurs de champ, les parcours clavier complets, la gestion du focus après une suppression et l’annonce d’un conflit avec un lecteur d’écran. La validation visuelle par l’utilisateur reste ouverte.
