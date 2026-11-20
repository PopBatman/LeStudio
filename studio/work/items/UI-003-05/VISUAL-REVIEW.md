# Examiner la navigation avant le retrait de la V1

La [maquette interactive](evidence/maquette.html) reprend la fiche Site et la direction Atlas du Sud déjà examinée en UI-003-01. Les deux sélecteurs en tête du fichier servent à jouer les scénarios de recette. Dans le produit, le responsable de déploiement applique la bascule selon la décision consignée. Les opérateurs utilisent les accès qui correspondent au déploiement de leur site.

| État de la simulation | Parcours visible |
| --- | --- |
| Coexistence | **Reprendre le brouillon** ouvre l’éditeur structuré V1. **Canvas Wagtail** ouvre la V2. Le détail des autres accès permet aussi d’ouvrir le canvas V1. [Fiche Site sur bureau](evidence/coexistence-bureau.png) |
| Bascule approuvée | L’entrée principale ouvre le Visual Builder. L’opérateur retrouve l’origine, la page et le numéro du brouillon. [Page issue de Figma sur tablette](evidence/bascule-tablette.png) |
| Retour arrière | L’accès principal rouvre l’éditeur structuré sur le brouillon courant. [Page vierge sur mobile](evidence/retour-mobile.png) |
| Retrait approuvé | L’opérateur conserve l’entrée V2. Les commandes V1 restent absentes. La distinction avec le masquage temporaire se vérifie sur les anciennes routes et leurs consommateurs lors de la réalisation. |

Dans le simulateur, choisir **Retour arrière** dans le sélecteur de scénario rétablit les accès V1. La preuve du rétablissement sur le produit devra partir du mécanisme de déploiement prévu et vérifier ensuite l’accès effectif de l’opérateur à la dernière tête.

Les trois origines permettent de vérifier l’identification de l’état retrouvé après navigation. La page vierge présente son emplacement vide. Le modèle conserve son titre et son illustration. La page importée signale sa remise confirmée et le format disposant d’une référence. Les accès de domaine Pages, Menus, Bibliothèque, Apparence et Aperçu restent identifiés sur la fiche. Les libellés et les regroupements de cette maquette sont des propositions à examiner sur la future interface.

## Contrôles réalisés sur la maquette

Chromium 156.0.8078.4 a parcouru 36 combinaisons de scénario (trois origines, trois tailles, quatre états de navigation). Les tailles étaient 1 440 × 960, 820 × 1 060 et 390 × 844. Entrée sur l’action principale a ouvert l’interface attendue et placé le focus sur son titre. Le retour à la fiche a rétabli le focus sur l’action principale. Le statut accessible contenait la page et la révision R8. Les accès secondaires aux deux canvas ont été activés au clavier. Le masquage et le retour des anciennes entrées ont été contrôlés. Le contrôle supplémentaire à 320 px a constaté l’absence de débordement horizontal. Aucune exception JavaScript et aucune requête HTTP pendant ces parcours.

Les pages, la révision et les destinations sont fictives. La simulation a vérifié l’orientation et le focus. La recette sur Studio devra vérifier les routes réelles, les brouillons persistés, les annonces entendues avec le lecteur d’écran, l’édition, les conflits, les tâches métier et le rendu Wagtail. La revue UX/DA humaine des trois parcours sur le produit réalisé et la décision de bascule restent à recueillir. [Référence approuvée UI-003-01](../UI-003-01/VISUAL-REVIEW.md) · [Plan de réalisation](TASKLIST.md)

## Revue du produit réalisé

Le [comparatif V1/V2](evidence/comparatif-produit.pdf) contient neuf paires de captures. Sur chaque paire, le site, la page et la révision sont identiques. Les fenêtres mesurent 1 440 × 960, 820 × 1 060 et 390 × 844 px. Le rendu intégré a été mesuré séparément. Les origines sont une page issue du départ vierge, un modèle et une page ajoutée depuis une remise Figma simulée. [Mesures par capture](evidence/comparaison-navigateur.json)

Orca a annoncé la destination, l’annulation, l’insertion du composant puis le numéro de la révision enregistrée. Chromium a exercé la sélection historique, une largeur de 455 px et le refus d’un formulaire périmé. L’essai de clavier avec lecteur d’écran a été automatisé. [Journal Orca](evidence/orca-clavier.json) · [Signets](evidence/signet-canvas.json)

Le PDF est joint à la carte Notion pour l’examen humain. Les points à juger comprennent la densité de l’atelier sur mobile, l’usage des champs de géométrie pour redimensionner et le passage par la Bibliothèque pour remplacer une définition. Le verdict UX/DA, les réserves éventuelles et la décision de bascule sont consignés dans le rapport au moment où l’opérateur les communique.
