# Fiche Site et premier parcours de l’Atelier

Ouvrir la [maquette interactive autonome](evidence/maquettes.html) dans un navigateur. Au bas de la page, « Scénarios de la maquette » permet de changer de mandat, de choisir un brouillon et d’examiner une observation de raccordement fictive. Les styles du registre, les couleurs, les badges, la marque et la typographie sont repris de Studio. Les sélecteurs de scénarios appartiennent uniquement au prototype.

| Parcours | Vue examinable |
|---|---|
| Fiche gestionnaire avec brouillon. « Reprendre le brouillon » ouvre la composition du site. La date d’enregistrement du brouillon et les dates des vérifications Wagtail sont distinctes. | [Fiche sur ordinateur](evidence/fiche-bureau.png) |
| Consultation avec dernier échec du moteur. Le succès antérieur reste daté. L’opérateur en lecture peut consulter le brouillon et les versions du moteur. Les UUID, l’alias et le diagnostic technique restent réservés au gestionnaire. | [Fiche sur mobile](evidence/fiche-mobile-lecture.png) |
| Depuis une fiche sans liaison ni brouillon, un gestionnaire peut choisir un template personnalisable ou un départ vierge. L’entrée Figma indique la dépendance à la disponibilité de la proposition d’import. | [Premier démarrage sur mobile](evidence/creation-mobile.png) |
| Le prototype représente la sélection de la page et la modification de son nom. Enregistrer permet de relire la révision sur la fiche puis de retrouver la saisie dans l’éditeur. | [Éditeur structuré sur ordinateur](evidence/atelier-bureau.png) |

Les révisions locales et les valeurs techniques du site fictif sont simulées en mémoire. Une version appliquée ou précédente inconnue est indiquée comme non renseignée. Le scénario de conflit conserve la saisie pendant la comparaison. Le prototype représente l’entrée de la fiche et le premier parcours de l’éditeur ; le canvas, le portail graphiste et l’analyse Figma auront leurs propres maquettes d’interaction et recettes. Les éléments de navigation hérités de FEAT-002 servent de repères de contexte sur cette maquette. La fiche est un rendu immédiat de données centrales, sans attente de réponse du moteur.

## Examen avant développement

Dans Chromium, 18 combinaisons de la fiche (trois mandats, deux états de brouillon, trois états de raccordement) ont été exercées à chacune des largeurs 1440, 390 et 320 pixels. Les tests ont aussi exercé les deux démarrages opérables, l’enregistrement et la reprise, le traitement du conflit, le parcours en lecture, l’accès refusé et les détails du moteur au clavier. Le lien de saut puis Tabulation et Entrée atteignent la création ; le focus passe au titre du nouvel écran. Aucune erreur navigateur, requête HTTP ou sortie de la largeur de fenêtre n’a été observée. [Résultats des contrôles](evidence/examen-maquettes.json)

Les captures concernent le prototype. La persistance entre sessions, les habilitations réelles, les sauvegardes concurrentes, les contrôles sur deux sites et la comparaison à la future page Django appartiennent aux sous-lots de développement. L’examen visuel par l’utilisateur et l’essai avec lecteur d’écran restent ouverts.
