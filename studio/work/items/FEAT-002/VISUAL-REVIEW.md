# Parcours et maquettes du registre

Ouvrir la [maquette autonome](evidence/maquettes.html). Le menu « Parcours de la maquette » permet de choisir un écran. Les liens entre les écrans simulent les actions et leurs résultats avec des exemples fictifs. Les saisies restent dans le navigateur. L’en-tête, les couleurs, les champs, les boutons, les listes et le focus s’inspirent de [UI-001](../../../docs/COMPOSANTS-UI.md).

| Parcours représenté | Points à examiner avant puis pendant la réalisation |
|---|---|
| Clients actifs, archivés et recherche | Entrée par nom, filtre de type, accès à la fiche, première utilisation et recherche sans résultat. Les écrans illustrent des résultats prédéfinis. |
| Fiche active et formulaires client | Nom et type du client, modification, contacts autorisés et sites visibles pour cet opérateur. Les listes ne révèlent aucun total portant sur les sites hors périmètre. |
| Contacts | Nom, rôle principal et deux champs de coordonnées. L’état en erreur garde le nom et le rôle, relie les deux champs au même message et indique comment corriger la saisie. |
| Sites | Création depuis un client identifié, domaine facultatif, fiche et modification. Le lecteur limité à un site peut consulter sa fiche. Pour le gestionnaire limité, « Mes sites » mène à la fiche et à son formulaire. Annuler revient à la fiche du site. Après enregistrement, il peut retrouver la fiche ou sa liste. Le nom du client, ses contacts et sa fiche sont absents de ce parcours. |
| Archivage et réactivation | Confirmation avec nom du client, effet sur la liste courante, annulation et retour de succès. Une fiche archivée consultable permet de la réactiver. |
| Visibilité et refus | Une opération indisponible sur un objet visible conduit à « Action indisponible ». Une fiche hors périmètre conduit à « Fiche introuvable », avec une sortie vers les sites accessibles. |

Les maquettes proposent un rendu HTML autonome à partir de la tasklist. Leur traitement futur côté Django est décrit dans la [spécification](SPEC.md). Les demandes de listes et les enregistrements sont prévus par navigation serveur et soumission de formulaires. En cas d’attente, la future réalisation conserve les valeurs saisies et prévient la double soumission.

## Examen du support

Le 18 novembre 2026, l’agent de cadrage a ouvert les 27 vues dans Chromium 156.0.8078.4, en 1440 × 960 puis 390 × 844. Chaque ancre a affiché une seule vue et chaque vue tenait dans la largeur de la fenêtre. Toutes les destinations internes ont été retrouvées. Le premier arrêt clavier atteint « Aller au contenu ». Les contacts et les sites de la fiche s’empilent sur petit écran.

La validation des filtres, des formulaires, des habilitations, du focus après réponse et des annonces d’erreur ou de succès reste à effectuer sur l’application réalisée. L’examen ci-dessus porte exclusivement sur la maquette.
