# Revue visuelle du cadrage · 20 novembre 2026
La [maquette interactive](evidence/maquette.html) prolonge la direction artistique Atlas du Sud approuvée en UI-003-01. La barre supérieure distingue la dernière révision enregistrée de la saisie locale. À gauche, le catalogue présente vignette, catégorie, portée et version. Le guide de placement nomme une destination avant un bloc ou en fin de section. L’inspecteur donne accès au déplacement, à la duplication et au retrait. Le composant sélectionné s’édite à son emplacement dans la page.

| Parcours | Observation dans Chromium 156.0.8078.4 |
| --- | --- |
| [Placement sur ordinateur](evidence/placement-bureau.png) | Sur 1 440 × 960, la recherche sans résultat et le filtre « Texte » ont été exercés. Entrée sur la carte expose les guides, le texte d’un bloc refuse de recevoir un enfant, puis Entrée sur un guide insère le bloc. Un second ajout a été effectué par glisser-déposer au pointeur. |
| [Édition sur tablette](evidence/edition-tablette.png) | Édition du titre en place, Annuler/Rétablir, duplication, retrait, déplacement via destination puis enregistrement en R9 ont été vérifiés. Le champ de saisie est visible dans la capture à 820 × 1 060. |
| [Conflit sur mobile](evidence/conflit-mobile.png) | À 360 × 820, une sauvegarde concurrente simulée avance la tête à R10. Conserver la saisie maintient le titre local ; abandonner explicitement la saisie recharge la version de la démonstration. À 320 px, le document tient dans la largeur. |

Le fichier HTML utilise des ressources intégrées et des données fictives en mémoire. Aucune exception JavaScript ni requête HTTP(S) observée durant ces essais. La démonstration de placement porte sur une section linéaire ; arborescences imbriquées, collision en placement libre, glisser tactile, restrictions intersites, sauvegarde transactionnelle et rendu Wagtail après relecture relèvent de la recette de réalisation. La direction artistique du socle a reçu l’accord documenté en UI-003-01. Les interactions supplémentaires du présent cadrage ont fait l’objet d’un examen technique.

## Recette de l’interface réalisée

Le parcours Chromium part de la fiche Site et utilise la coque Django et son iframe Wagtail privée. La [bibliothèque sur ordinateur](evidence/realisation-placement-bureau.png), l’[édition en contexte](evidence/realisation-edition-bureau.png), le [brouillon importé sur tablette](evidence/realisation-figma-tablette.png) et le [conflit sur mobile](evidence/realisation-conflit-mobile.png) montrent les états du produit. Le [journal du dépôt](evidence/realisation-depot-rendu.json) vérifie l’ouverture par double-clic et deux insertions sur le rendu réel, au clic et par glissement. La [réouverture](evidence/realisation-rendu-enregistre.png) présente le nouveau rendu après sauvegarde.

Le [placement libre sur mobile](evidence/realisation-placement-libre.png) et le [guide de dépôt refusé](evidence/realisation-depot-refuse.png) complètent la recette. Les mesures de [position et héritage par format](evidence/realisation-responsive.json) confirment le maintien du flux sur bureau et tablette après modification du mobile.
