# Workflow commun de développement

Le type de travail est **feature**, **connecteur**, **composant UI** ou **architecture**. Le mandat et le risque déterminent les contrôles applicables.

## États

| État | Résultat attendu |
|---|---|
| DRAFT | Dossier créé ; contenu et mandat d’implémentation à établir |
| DISCOVERY | Besoin compris, existant examiné, questions et recherche utile identifiées |
| SPECIFIED | Règles, données, permissions, erreurs et critères décrits ; décisions nécessaires identifiées |
| PLANNED | Tasklist ordonnée, dépendances, périmètre et vérifications préparés |
| READY | Prérequis applicables disponibles, maquette examinable si UI, blocages structurants résolus |
| IMPLEMENTING | Travail exécuté dans le mandat, avec tests et preuves progressives |
| VERIFIED | Vérifications applicables exécutées et écarts connus |
| REVIEWED | Revue requise réalisée, défauts traités ou explicitement acceptés dans le périmètre |
| DONE | Livrable cohérent, rapport et mémoire à jour, critères de fin satisfaits |

Le parcours est `DRAFT → DISCOVERY → SPECIFIED → PLANNED → READY → IMPLEMENTING → VERIFIED → REVIEWED → DONE`. Un retour en arrière conserve l’historique et réexamine les preuves touchées. Le CLI local contrôle des prérequis ; il ne fait pas évoluer automatiquement ces états.

## Exécuter le parcours

1. [Découvrir le besoin](FEATURE-DISCOVERY.md), sans choisir silencieusement une fonctionnalité différente.
2. Rédiger la spécification et appliquer les [contrats d’architecture](../../studio/docs/ARCHITECTURE-CONTRACTS.md).
3. Écrire le [plan en tasklist](FEATURE-PLANNING.md).
4. Préparer la [conception visuelle](FEATURE-VISUAL-REVIEW.md) si le frontend change.
5. Vérifier le mandat existant et les prérequis, puis [développer](FEATURE-DEVELOPPEMENT.md).
6. Appliquer le [TDD pertinent](FEATURE-TDD.md), vérifier l’intégration et le rendu réel.
7. Réaliser la [revue](FEATURE-REVIEW.md), puis le [rapport](FEATURE-RAPPORT.md).
8. [Capitaliser](FEATURE-CAPITALISATION.md) ; effectuer une [livraison](FEATURE-RELEASE.md) uniquement lorsqu’elle appartient au mandat.

`READY` ne donne pas d’autorisation. `DONE` ne signifie pas publié. Un contrôle bloqué reste visible et ne devient pas « réussi » pour clore la tâche.

Les variantes [connecteur](CONNECTOR-WORKFLOW.md) et [composant](COMPONENT-WORKFLOW.md) précisent leurs livrables. Les [contrôles qualité](../governance/QUALITY-GATES.md) restent proportionnés au changement.

