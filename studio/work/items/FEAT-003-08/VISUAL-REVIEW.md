# Revue visuelle du cadrage

La [maquette interactive](evidence/maquettes.html) s’ouvre dans un navigateur depuis un fichier local. Cliquer sur **Analyser la remise**, choisir une décision pour le composant et sa couleur, puis **Examiner le résultat**. La confirmation du résumé est le seul geste d’écriture simulé. En bas de page, **Scénarios de la maquette** permet d’examiner les quatre situations sur des données fictives.

| Écran | Parcours examiné |
|---|---|
| [Revue sur bureau](evidence/correspondances-bureau.png) | La colonne source indique la version de remise, la révision Figma, la frame et l’origine du texte. La lecture observée et la confiance dans la correspondance ont leurs propres libellés. Le panneau des décisions propose un composant interne versionné et une propriété de couleur. Le ruban animé inconnu et les formats tablette/mobile absents restent consignés comme écarts. |
| [Confirmation à 320 px](evidence/ajout-mobile.png) | Sur le scénario de brouillon existant, la confirmation précise la page ajoutée sous Accueil, la révision 4 de départ et les éléments retenus. Revenir aux décisions conserve les choix. Le reçu simulé affiche la révision 5. Pour un site vierge, le résumé précise que la page deviendra l’accueil de la première révision. |
| [Lecture indisponible](evidence/indisponible-mobile.png) | Un retour générique invite à vérifier l’accès pour ce site. L’écran garde le contexte de la remise et retire les noms de calques, métadonnées et valeurs du fichier. |
| [Source modifiée](evidence/source-modifiee-mobile.png) | Une publication fictive du fichier entre la revue et la confirmation demande une nouvelle analyse. La remise garde son numéro, la source passe de R17 à R18 et les choix repartent à l’état indécis. |

Le scénario de démonstration comporte un seul bloc de texte. Le corriger en texte courant remplace la définition « Titre » par « Texte » v1. Accepter, corriger ou écarter le token d’encre détermine le réglage de cette occurrence. Écarter l’unique bloc laisse la sélection vide et désactive la création au moment de l’examen. L’opérateur peut revenir à la remise sans enregistrer.

Chromium a activé le lien de saut et les boutons au clavier. Les écrans changent le focus vers leur titre. Une décision manquante ou une sélection vide renvoie le focus vers le choix à reprendre. Les quatre captures ont été prises à 1 280 ou 320 px sans débordement horizontal. Le parcours a enregistré zéro requête HTTP et zéro erreur JavaScript. [Résultats des essais](evidence/examen-maquettes.json)

L’exercice évalue des interactions en mémoire. La comparaison affiche des métadonnées fictives et un extrait de texte, sans prétendre reproduire les pixels de Figma ou le rendu Wagtail. Les droits effectifs, la disponibilité API, le rapprochement réel des contenus, la persistance canonique, la concurrence et les annonces au lecteur d’écran seront à qualifier sur l’application. L’examen humain de direction artistique pourra utiliser cette maquette.

Le prototype commence avec une seule frame choisie. La sélection parmi plusieurs frames, la résolution d’un slug déjà utilisé, les images attribuées au site et le conflit avec une nouvelle tête locale figurent dans la recette de réalisation. Le dernier écran propose le retour à la remise. L’ouverture de la révision dans le véritable atelier et sa réédition y seront vérifiées après intégration.

## Écrans livrés

Les vues Django ont été examinées dans Chromium à 1 280 et 320 pixels sur une remise fictive. Au clavier, le gestionnaire a corrigé une correspondance et la couleur proposée, écarté un élément inconnu et confirmé une seule frame mobile. La révision obtenue s’est ouverte dans l’atelier. [Correction dans Studio](evidence/realisation-correspondance.png) · [Récapitulatif mobile](evidence/realisation-confirmation-mobile.png) · [Relevé](evidence/realisation-navigateur.json)
