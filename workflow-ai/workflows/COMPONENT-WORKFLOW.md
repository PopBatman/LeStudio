# Développer un composant UX/UI

Ce parcours complète [FEATURE-WORKFLOW.md](FEATURE-WORKFLOW.md). L’UX décrit le parcours ; le composant UI rend un contrat de présentation et d’interaction.

Une tâche dont `kind` vaut `component` impose `ui_required: true` dans `task.json`. Sa conception visuelle et ses captures font partie des contrôles applicables ; modifier ce booléen ne permet pas de les contourner.

## Concevoir

| Partie | Contenu |
|---|---|
| Usage | Problème, contexte et niveau : primitive, composé, métier ou écran |
| Entrées | Propriétés, types attendus, variantes et valeurs par défaut |
| Composition | Emplacements personnalisables et assemblages |
| États | Normal, actif, indisponible, chargement, vide, erreur, succès selon pertinence |
| Interactions | Actions, clavier, focus, messages et annonces |
| Adaptation | Responsive, contenu absent, textes longs et réduction des animations |
| Dépendances | JavaScript nécessaire, version et justification |

Réutiliser les composants existants pertinents. Garder les composants métier proches de leur domaine ; partager les primitives réellement communes. Les thèmes de Studio et des sites peuvent différer.

## Construire et vérifier

1. Décrire le parcours et le [contrat du composant](../templates/COMPONENT-SPEC.md).
2. Écrire la tasklist puis produire les maquettes ou références.
3. Implémenter le rendu et les interactions dans les conventions du design system.
4. Ajouter des exemples à la galerie interne et tester les comportements utiles.
5. Vérifier dans un navigateur réel : états, clavier, focus et tailles.
6. Conserver captures, écarts, revue et limites.

Cotton/templates composent des données préparées. Tailwind porte les styles et variantes explicites. HTMX définit un contrat de requête/réponse et de remplacement de fragment. Alpine porte l’état local temporaire. Les permissions et invariants restent côté serveur.

La sélection d’un composant shadcn-django exige une revue adaptée de ses dépendances, usages et maintenance ; sa présence dans le catalogue n’implique pas son adoption.

Les retouches cosmétiques utilisent une vérification proportionnée. Une image conceptuelle, un prototype et une capture d’implémentation gardent des statuts distincts.

