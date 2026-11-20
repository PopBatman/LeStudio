# Raccordement GitLab

Le fragment fourni vérifie le **workflow**. Le pipeline du produit Studio sera défini dans ARCH-001 selon le dépôt, les versions et le runner réellement disponibles.

## Inclure le fragment

Le fragment s’exécute depuis la racine de l’espace qui contient `workflow-ai/` et `studio/`. Si cet espace est suivi dans GitLab, ajouter le fragment aux inclusions de son `.gitlab-ci.yml`.

```yaml
include:
  - local: 'workflow-ai/integrations/gitlab/workflow-ai.gitlab-ci.yml'
```

Le job utilise le stage `test`, l’image `python:3.12-slim`, le validateur, les tests Python et la simulation de projection Notion. Dans un dépôt neuf sans liste `stages` personnalisée, `test` fait partie des stages par défaut. Dans un pipeline existant, vérifier que ce stage est présent ou adapter celui du job à un stage existant. Le job ne publie rien. Le tag d’image est une base de configuration ; fixer son digest lors du raccordement si la politique du dépôt exige une image immuable.

| Élément | Action dans le dépôt cible |
|---|---|
| YAML | Vérifier la configuration fusionnée dans CI Lint |
| Runner | Confirmer sa disponibilité et l’accès à l’image nécessaire |
| Branches et fusion | Définir les branches protégées, droits et conditions réellement disponibles |
| Tests produit | Préparer la CI Django/PostgreSQL/Docker du produit dans `studio/` lors d’ARCH-001 |
| Secrets | Utiliser les variables et restrictions adaptées au contexte ; aucune valeur n’est livrée |
| Déploiement | Spécifier séparément cible, mandat, sauvegarde, migrations et reprise |

Un job réussi ne prouve pas que toutes les tâches produit sont terminées. Pour un lot, lancer aussi `workflow.py check --id ID --phase ...` avec la phase utile. Ne pas faire échouer tout le dépôt parce qu’un lot futur reste volontairement à l’état de brouillon.

## Limite des contrôles

Le code d’échec d’un script bloque ce job. Le blocage d’une fusion ou d’un déploiement dépend des réglages de GitLab, des permissions et des autres chemins d’accès. Ces réglages ne sont pas installés par le ZIP. Une personne ou un agent autorisé à modifier la CI peut en changer les règles ; séparer les responsabilités selon le risque du projet.

Configuration fournie, **aucun pipeline exécuté sur le compte GitLab de l’utilisateur pendant cette livraison**. Les commandes locales équivalentes sont consignées dans le rapport de vérification.

Sources officielles : [inclure une configuration CI GitLab](https://docs.gitlab.com/ci/yaml/includes/) et [stages du pipeline](https://docs.gitlab.com/ci/yaml/#stages), consultées le 18 novembre 2026.
