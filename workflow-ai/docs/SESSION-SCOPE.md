# Mandat de la livraison du Workflow AI

Date : 18 novembre 2026.

## Demande utilisateur à l’origine du travail

L’utilisateur demande d’écrire et de mettre à jour les processus, de les documenter dans Notion et de fournir un Workflow AI téléchargeable et installable. Il indique que le travail produit commencera ensuite par l’installation de l’architecture.

Cette page retranscrit la portée de cette demande. **Elle ne peut pas créer elle-même une autorisation nouvelle ni prouver l’identité d’un approbateur.**

## Portée de cette livraison

| Action | Portée |
|---|---|
| Consolider les processus | Incorporer les règles de développement des features, connecteurs et composants UX/UI |
| Préparer le paquet installable | Fichiers, installateur, outils locaux, documentation et exemples |
| Vérifier le paquet | Contrôles documentaires et tests locaux pertinents de ses propres outils |
| Mettre à jour Notion | Documentation du Workflow dans le wiki existant |
| Préparer ARCH-001 | Spécification, recherche à conduire, architecture proposée, tasklist et critères |
| Distribuer le livrable | Archive téléchargeable avec état réel et instructions d’installation |

Le mandat couvre les corrections nécessaires à cette livraison et ses vérifications locales. Il n’exige pas de redemander une confirmation pour chaque sous-tâche réversible déjà comprise dans ce périmètre.

## Produit Studio

La fabrication du Workflow ne constitue pas l’installation du produit Studio dans le dépôt de l’utilisateur. ARCH-001 est **préparé, non exécuté** dans cette livraison. Aucun résultat de démarrage, migration PostgreSQL, capture de Studio ou pipeline distant n’est revendiqué pour ce lot.

L’utilisateur lancera ARCH-001 dans le dépôt cible après l’installation du Workflow. L’agent devra alors rattacher les actions à ce mandat concret, examiner les fichiers existants et renseigner les chemins réellement concernés. Il réutilisera l’autorisation applicable tant que le périmètre reste respecté.

## Limites

| Limite | Conséquence |
|---|---|
| Aucun déploiement de production demandé dans cette livraison | Pas de mutation distante du produit |
| Aucun push ou changement de protection de dépôt demandé | La documentation et les exemples CI ne valent pas activation distante |
| Aucun secret à inclure | Les exemples présentent des noms de variables et références, sans valeur réelle |
| Aucun premier module métier choisi | Ne pas réintroduire Contact comme lot adopté |
| Aucune validation humaine à inventer | Un état READY, un test ou un fichier de mandat n’équivaut pas à une approbation |
| Aucun effacement de code existant autorisé implicitement | L’audit du dépôt précède les changements ; les conflits sont exposés |

## Statuts à ne pas confondre

La définition documentaire, la réalisation, la configuration d’un outil et sa vérification réelle sont suivies séparément. Une instruction d’agent ne crée pas une isolation système. Un rôle Markdown ne lance pas un sous-agent. Une projection Notion ne déclenche aucune livraison.

La [spécification ARCH-001](../../studio/work/items/ARCH-001/SPEC.md) détaille le prochain résultat technique envisagé.

