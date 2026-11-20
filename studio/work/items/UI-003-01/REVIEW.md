# Revue indépendante du cadrage · 20 novembre 2026

L’exécutant /root/u301qa a examiné la carte Notion, la spécification, le contrat d’interaction, la grille de revue artistique et le prototype autonome. Les gestes ci-dessous ont été exercés dans Chromium 156.0.8078.4 avec Playwright. Le [relevé des observations](evidence/qualification-prototype.json) identifie le fichier HTML par son empreinte.

| Parcours | Résultat observé |
| --- | --- |
| [Page vierge, 360 × 800](evidence/parcours-vierge-mobile.png) | Un parcours entièrement au clavier va de la fiche à l’insertion et à l’édition du titre. Enregistrement R2, même valeur en aperçu. La fermeture de l’aperçu et celle de l’inspecteur rendent le focus à leur commande. Le retour ramène à Atlas du Sud. |
| [Modèle, 1440 × 950](evidence/parcours-modele-bureau.png) | L’édition en place, l’annulation, le rétablissement et les commandes de changement d’ordre sont opérants. L’aperçu R9 contient la valeur sauvegardée. La page longue a 30 blocs. Choisir le dernier calque déplace le focus sur le bloc 30. |
| [Figma, 820 × 1080](evidence/parcours-figma-tablette.png) | L’inspecteur décrit la remise simulée. Une référence absente masque la couverture et laisse le texte éditable. Le bandeau distingue l’aperçu R8 et le brouillon R9. Sur conflit, la sauvegarde est bloquée, annuler le rechargement préserve la saisie et le confirmer recharge la valeur enregistrée en R10. |
| Parcours croisés | Les trois origines ont été ouvertes, prévisualisées et quittées au clavier sur chacune des largeurs de 360, 820 et 1440 px. À 320 px, le panneau Navigation s’ouvre au clavier, Échap redonne le focus au bouton et le document tient dans la largeur. |
| Annonces et isolation | L’arbre d’accessibilité de Chromium contient la zone principale et les champs de bloc nommés. Le chargement, le rendu périmé et l’indisponibilité ont chacun un message et une action de reprise vérifiés. L’exécution observée compte zéro exception JavaScript et zéro requête HTTP(S). |

Deux corrections demandées pendant l’examen ont été vérifiées sur la version finale. Les boîtes de dialogue référencent leur titre et leur description. Un bouton de reprise dans les bandeaux permet de revenir à un aperçu disponible. Les captures sont issues du prototype avec les données fictives intégrées.

**Avis favorable pour soumettre ce cadrage à la revue UX et artistique.** L’écoute au lecteur d’écran avec une personne, la décision artistique et les corrections que cette personne demandera restent à consigner dans la [fiche de revue](VISUAL-REVIEW.md). Les trois parcours, les états de révision et le moteur représentés par la maquette sont simulés. La fidélité à une instance Wagtail, les droits réels et les écritures sur des révisions persistantes seront qualifiés dans les sous-lots d’intégration.

## Suite de la revue
La décision humaine figure dans [la fiche de revue](VISUAL-REVIEW.md). L’[examen indépendant de clôture](evidence/revue-cloture.md) complète le constat initial.
