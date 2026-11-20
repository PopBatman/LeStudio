# UI-003-01 · Parcours UX, design system et prototype V2
## Objectif et livrable
Faire décider de l’expérience du futur atelier sur un prototype interactif autonome. L’opérateur peut aller de la fiche d’un site à la modification d’un bloc, observer la révision proposée à l’aperçu, puis revenir à la gestion du site. Le cadrage livre le prototype, le contrat d’interaction, la matrice d’accessibilité et une fiche de décision artistique. Studio et Wagtail en fonctionnement restent les références de la qualification technique ultérieure.

## Carte des tâches
| Départ et intention | Manipulation attendue | Observation de réussite |
| --- | --- | --- |
| Fiche Site, nouvelle page | Ouvrir « Page vierge », trouver la bibliothèque, insérer un bloc à une destination valide et modifier son texte | Le premier contenu est visible dans la page et sa sélection est identifiable dans l’atelier |
| Modèle | Choisir le modèle, sélectionner un bloc existant dans la page ou les calques et modifier son contenu | L’opérateur voit immédiatement le bloc concerné et peut poursuivre dans l’inspecteur sans changer d’écran |
| Remise Figma confirmée | Reprendre le brouillon de la remise fictive et identifier les écarts de correspondance | Les commandes de modification et d’aperçu sont celles de la page créée manuellement. Une référence absente est compréhensible et conserve les éléments éditables |
| Révision et retour | Modifier, enregistrer, ouvrir l’aperçu puis revenir à la fiche du site | L’état de la saisie et l’identité de la révision rendue sont discernables. L’opérateur sait retrouver le site et la page |
| Page longue | Changer de page, atteindre un bloc éloigné par les calques et y reprendre l’édition | La sélection et les commandes restent accessibles après défilement |
| Incident | Comparer un aperçu périmé au brouillon, rencontrer une erreur ou un conflit, puis reprendre | Le message indique ce qui est encore utilisable et le prochain geste. La maquette rend visibles les conséquences sur la saisie |

## Contrat de sortie
L’opérateur doit pouvoir expliquer ce que modifie chaque panneau, terminer les trois trajets au clavier, trouver la commande d’insertion sans saisir de coordonnées et distinguer les trois formats. La décision humaine porte sur la direction visuelle, la hiérarchie, la densité, les gestes et la lisibilité des états d’erreur. Elle mentionne la version examinée, les corrections prioritaires et l’autorisation éventuelle de reprendre ces décisions dans les sous-lots suivants. Une capture ou un contrôle automatique ne remplit pas ce critère.

Le rendu Wagtail réel et son pont de sélection relèvent de UI-003-02. L’intégration des commandes aux services de brouillon relève de UI-003-03. L’origine Figma du prototype est une fixture locale conforme à la consigne de simulation.
