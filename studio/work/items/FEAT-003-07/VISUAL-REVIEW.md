# Maquette du dépôt de maquettes Figma

La [maquette interactive autonome](evidence/maquettes.html) s’ouvre dans un navigateur. Elle reprend la typographie DM Sans, les panneaux, les libellés et les actions de la fiche Site existante. Les données et les échéances illustrent le site fictif Atelier Papier. Le panneau « Parcours de la maquette » sert à passer d’un rôle simulé à un autre. Recharger le fichier réinitialise la démonstration.

## Examiner le parcours

1. Sur la fiche Site, ouvrir **Consulter les dépôts Figma** puis **Créer une invitation de 7 jours**. Le gestionnaire voit le lien fictif à transmettre et son échéance. **Examiner le portail simulé** ouvre l’écran invité.
2. Saisir le lien d’une maquette, par exemple `https://www.figma.com/design/ExempleFictif01/Accueil`. Le commentaire est facultatif. Le formulaire conserve les valeurs après une erreur et replace le focus sur le champ concerné.
3. Transmettre, lire le reçu puis choisir **Déposer une autre version**. Le formulaire accepte un lien unique, quelle que soit la déclinaison fournie. La simulation ne contacte aucun fichier Figma.
4. Dans le sélecteur de démonstration, choisir **Fiche Site · Lecture**. La date et le numéro du dernier dépôt apparaissent sur la fiche. Ouvrir l’historique pour retrouver l’invitation, les versions dans l’ordre décroissant, la date et le commentaire associé. Revenir à la fiche conserve le signal.
5. En gestion, essayer la révocation, d’abord en conservant l’invitation, puis en la confirmant. L’historique reste consultable. Un nouveau dépôt via une nouvelle invitation reprend au numéro 1. Côté invité, la même page explique comment obtenir une nouvelle invitation quand le lien est expiré, inconnu ou révoqué.

## Résultats observés avant développement

| Vue examinée | Résultat |
|---|---|
| [Fiche Site, bureau](evidence/site-dernier-depot-bureau.png) | Le signal du dernier dépôt indique l’invitation, la version et la date avant consultation. |
| [Historique, bureau](evidence/operateur-depots-bureau.png) | Les deux premières remises se distinguent par leur numéro. L’ordre affiché est 2, puis 1. Après recréation, l’historique contient aussi la version 1 de la seconde invitation. |
| [Portail invité à 320 px](evidence/portail-graphiste-mobile.png) | Un seul champ obligatoire pour déposer. Les libellés restent lisibles et les champs tiennent dans la largeur de l’écran. |
| [Erreur de lien à 320 px](evidence/depot-erreur-mobile.png) | L’URL non admise et le commentaire restent dans le formulaire. Le focus revient au lien, associé à son message d’erreur. |
| [Invitation indisponible à 320 px](evidence/invitation-indisponible-mobile.png) | Les trois états de refus affichent la même instruction, sans formulaire ni données de site dans le contenu public. |

Chromium a exécuté les parcours de création, de remise successive, de consultation, de révocation et de renouvellement. Le lien de saut et l’ouverture du portail ont été activés au clavier. Les cinq captures tiennent dans leur largeur de fenêtre. Le navigateur a enregistré zéro requête HTTP et zéro erreur JavaScript. [Compte rendu d’exécution](evidence/examen-maquettes.json)

Ce contrôle porte sur l’ergonomie simulée. L’application Django devra qualifier les mandats réels, la conservation et la purge, la pagination, les refus et quotas côté serveur, le reçu après actualisation, la concurrence PostgreSQL ainsi que les annonces au lecteur d’écran. La validation humaine de l’interface peut s’appuyer sur ce fichier avant le développement. [Plan de réalisation](TASKLIST.md)
