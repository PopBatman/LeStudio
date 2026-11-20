# Examen de la fiche Site avant développement

Ouvrir la [maquette interactive](evidence/maquettes.html) dans le navigateur. Les sélecteurs « Scénario » et « Mandat sur la fiche » figurent en bas du document. Ils permettent de passer d’une observation à l’autre avec des données fictives. La fiche « Atelier du Chenal » reprend la typographie, le panneau, le badge et le focus de UI-001, ainsi que la mise en page de FEAT-002. Les liens de navigation et le bouton de modification existants sont représentés comme repères visuels. La divulgation des détails est interactive.

| Vue à examiner | Illustration |
|---|---|
| Gestion, raccordement confirmé. Les détails associent le site, l’instance et l’alias à la dernière confirmation. | [Bureau avec détails](evidence/bureau-confirme.png) |
| Lecture, site sans liaison. Les deux lignes indiquent explicitement l’absence de vérification et de confirmation. | [Bureau sans liaison](evidence/bureau-vide.png) |
| Gestion, échec après confirmation. Les deux dates, le diagnostic et les versions historiques restent distincts. | [Mobile après échec](evidence/mobile-echec.png) |
| Lecture, succès confirmé. Les détails consultables présentent les versions. | [Mobile en lecture](evidence/mobile-lecture.png) |

Le résumé est placé après « Fiche du site ». Le badge fournit le résultat le plus récent et le texte précise qu’il s’agit d’un historique. Les lecteurs autorisés accèdent aux dates et aux versions attestées. Les identifiants techniques, l’alias confirmé et le code de diagnostic sont réservés à la gestion. L’état sans mandat reprend « Fiche introuvable ». La maquette comprend aussi une première tentative en échec, une tentative en cours, une tentative expirée, une incompatibilité, une identité non conforme, une version manquante et un diagnostic inconnu. Les variantes utilisent un jeu de données de présentation local. Le produit devra composer son contexte au serveur sous les habilitations réelles.

## Vérifications réalisées

Le 19 novembre 2026, Chromium 156.0.8078.4 a rendu dix scénarios avec chacun des trois niveaux de mandat, aux dimensions 1440 × 960, 390 × 844 et 320 × 720. Le lien de saut a conduit au contenu. Tabulation a atteint la divulgation native avec un contour de focus visible ; Entrée l’a ouverte et Espace l’a refermée. Les détails ouverts, les UUID et les dates sont restés dans la largeur de chaque fenêtre. Le texte et les libellés des états restent lisibles en une colonne sur mobile. Les assertions ont vérifié le refus sans mandat, les champs autorisés pour la lecture, l’absence de destination technique cliquable et la présence des deux dates lors de l’échec ultérieur. [Résultats du navigateur](evidence/examen-maquettes.json)

Les images capturent le contenu principal du prototype. La [tasklist](TASKLIST.md) prévoit des captures et contrôles distincts sur la future page Django, dont la navigation réelle, les droits vérifiés côté serveur et la comparaison maquette/produit. La validation visuelle par l’utilisateur reste ouverte.
