# Sources et écarts observés
Le [lot parent](https://app.notion.com/p/41d49e23bbdb81dd983eff8b4010cf39), la [vision validée le 19 novembre](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539) et leurs cinq cartes filles donnent le périmètre et les conditions de sortie.

| Point de départ local | Conséquence pour la V2 |
| --- | --- |
| composition/editor.py et composition/assets/presentation-activite-v1.json initialisent les origines vierge et modèle ; editor_views.py et canvas_views.py portent deux interfaces. | Conserver les commandes et comparer les tâches réalisées, puis réunir les entrées dans un seul atelier. |
| composition/catalogue.py, placement.py, validation.py et services.py portent le catalogue, les règles, la validation et les révisions. | Vérifier pour chaque composant son rendu, ses propriétés, ses enfants et sa portée à partir de ces contrats. |
| composition/preview_views.py remet un ticket lié à la session et sert un document isolé sous CSP sandbox. | L’aperçu livré permet la comparaison par révision. La sélection d’un bloc dans ce document est un travail distinct à qualifier en 02. |
| depots/imports.py et composition/figma_mapping.py assurent revue et correspondances. La recette du lot 08 est documentée sur source simulée. | Repartir du brouillon confirmé. La provenance accompagne la comparaison sans créer un autre document éditable. |

La direction visuelle des écrans FEAT-003-04/05 a été refusée dans Notion. Leur historique technique DONE et leurs brouillons servent de référence de parité. La qualification transverse UI-002 et l’application FEAT-005 conservent leurs périmètres.

## Inventaire de départ pour la recette de parité

| Famille V1 (catalogue global) | Contrôle V2 à démontrer avec la même occurrence |
| --- | --- |
| Titre | Modifier le texte et le niveau, vérifier le niveau sémantique rendu et l’identité du bloc |
| Texte | Modifier un paragraphe, tester sa lecture, les textes longs et leur retour à la ligne |
| Image | Choisir un média du site, éditer le texte alternatif et diagnostiquer un média devenu indisponible |
| Bouton | Éditer libellé et destination admise en conservant le focus dans l’atelier |
| Conteneur | Sélectionner un enfant imbriqué, déplacer au clavier, vérifier ordre de lecture et héritage de placement |

Une section de page et une occurrence du catalogue ont des rôles distincts dans editor.py. Une composition de type Hero peut servir de modèle d’assemblage. Sa présence dans une maquette ne crée aucune nouvelle définition dans le catalogue. Vérifier aussi les définitions particulières au site, leurs versions et la provenance des médias. Les preuves de comparaison avec le rendu Wagtail se trouvent dans le [rapport FEAT-004](../FEAT-004/REPORT.md) et les limites de la recette fournisseur dans le [rapport FEAT-003-08](../FEAT-003-08/REPORT.md).
