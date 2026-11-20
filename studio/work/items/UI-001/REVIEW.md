# Revue indépendante de UI-001

Le 18 novembre 2026, l’agent `/root/ui_review`, distinct des auteurs du code, a examiné les contrats, le routage, les composants Cotton, le rendu Django et les captures en 1440 et 390 px. Il a contrôlé le sommaire, le focus, le champ dans l’arbre d’accessibilité et le comportement responsive.

| Constat | Correction | Contre-vérification |
|---|---|---|
| À 390 px, un nom valide de 80 W sans espace portait la largeur de page à 1 124 px après validation. | Le résultat de validation autorise les coupures à l’intérieur d’un mot. Le scénario figure dans le parcours Chromium. | Sur la pile Compose reconstruite, le réviseur a confirmé une largeur finale de 390 px et un texte intégralement visible. |

Le réviseur a contrôlé l’absence de débordement initial à neuf largeurs additionnelles entre 320 et 1280 px. Sur mobile, les trois premiers arrêts clavier atteignent le lien de saut, la marque et le sommaire. Échap ramène le focus au résumé. Choisir « Formulaires » ferme le menu et cible la section.

**Avis final favorable** sur la version servie localement. L’examen couvre Chromium et son arbre d’accessibilité. Un essai avec lecteur d’écran et les autres moteurs de navigateur restent hors de cette qualification.
