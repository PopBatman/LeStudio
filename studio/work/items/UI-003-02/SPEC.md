# UI-003-02 · Canvas fidèle au rendu Wagtail
## Parcours opérateur
Depuis la fiche d’un site autorisé, l’opérateur ouvre la page d’une révision enregistrée dans la coque définie en UI-003-01. La barre nomme le site, la page, la révision demandée, celle effectivement rendue et le format de la page. Les calques à gauche, le contour dans la page et l’inspecteur de lecture à droite désignent la même occurrence. Le clic, le toucher et la sélection par clavier doivent aboutir au même bloc.

La page vierge peut être rendue sans bloc sélectionnable. Pour les trois origines (vierge, modèle ou Figma confirmé), le canvas consomme le même document Studio et le même service d’aperçu. La source de la maquette ne conditionne ni le droit d’accès ni le comportement de sélection.

## Contrat de recette
| Cas à reproduire | Résultat à observer |
| --- | --- |
| Ouvrir N puis comparer avec l’aperçu FEAT-004 | Même site, instance, version moteur, UUID de page, UUID de révision, ressources validées et liste ordonnée d’occurrences. Capturer les deux rendus à largeur interne égale, une fois images et polices chargées ; comparer la zone de page hors contours Studio. Tout écart visuel doit être localisé, expliqué et examiné avant acceptation. |
| Deux occurrences de même type et libellé, dont une imbriquée | Un clic sur l’enfant sélectionne son UUID ; la commande de calque permet de retrouver le parent. Les deux panneaux concordent sans prendre le texte ni l’index DOM comme identité. La sélection ne modifie aucune révision. |
| Parcourir une page longue au clavier, défiler, redimensionner, changer de format | Retrouver le bloc sélectionné à l’écran et entendre son libellé et son état. Vérifier bureau, tablette, mobile et zoom. Détecter les débordements et signaler les limites observées ; la largeur seule ne transforme pas le document. |
| Une réponse arrive après le passage à une autre page ou un nouveau rendu | Seul le contexte actif peut mettre à jour l’interface. Vider la sélection si l’occurrence est absente du nouveau document. Empêcher la sélection spatiale tant que l’identité ou les mesures sont ambiguës. |
| N est encore lisible, mais la tête est N+1 | Identifier le rendu historique et proposer d’ouvrir la tête. Si la page a été retirée, indiquer son absence et proposer le choix d’une autre page. |
| Reçu expiré, ressource ou rendu divergent, composant incompatible, moteur indisponible | Retirer toute surface dont l’intégrité ou le droit de lecture n’est plus établi. Expliquer la cause accessible et proposer une nouvelle préparation. Si Studio autorise toujours la lecture, offrir la structure canonique intitulée « Structure du brouillon », avec la révision et le motif. |
| Droit du site perdu ou reçu d’une autre session | Fermer le contenu privé et les repères. La structure de repli est elle aussi soumise au contrôle d’accès. |
| Ouvrir, sélectionner, changer de largeur, actualiser et quitter | Comparer avant/après les révisions Studio, les pointeurs de publication et le contenu public des deux sites de recette. Seuls les reçus techniques prévus par FEAT-004 peuvent évoluer. |

## Périmètre
La cohérence visuelle concerne le rendu du brouillon N fourni par le moteur raccordé. Les contrôles Studio entourent cette page. Le dépôt, la saisie inline, la sauvegarde, l’annulation et les mutations du catalogue relèvent de UI-003-03. Le lot 04 reprend les diagnostics propres à Figma. La bascule des écrans V1 relève du lot 05. La proposition de pont décrite dans ARCHITECTURE.md doit franchir son essai de faisabilité avant intégration.
