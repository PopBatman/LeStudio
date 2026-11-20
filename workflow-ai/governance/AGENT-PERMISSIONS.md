# Responsabilités et permissions des agents

Cette matrice décrit la répartition logique du travail. Les droits réels viennent du mandat et du runtime. Un rôle ne confère aucun accès supplémentaire.

| Rôle | Production principale | Écritures habituelles dans le périmètre | Limite |
|---|---|---|---|
| Orchestrateur | Plan, délégations, intégration, état | Documents de pilotage et intégration explicitement couverte | Ne s’accorde pas un nouveau mandat |
| Chercheur | Sources, options, inconnues | Recherche | Ne présente pas une hypothèse comme décision |
| Analyste métier | Règles et critères | Spécification | Ne choisit pas seul un périmètre non convenu |
| Architecte | Contrats et décisions proposées | Architecture | Ne déploie pas une proposition |
| Sécurité | Risques et vérifications | Analyse, tests autorisés, revue | Aucun élargissement de privilège |
| QA | Scénarios et preuves | Tests et rapports | N’altère pas les critères pour masquer un défaut |
| Développeur | Code du lot, migrations et tests | Chemins attribués par la tasklist | Pas d’effet externe non couvert |
| Designer UI | Parcours, maquettes, contrats UI | Design et frontend attribué | Une maquette n’est pas une capture réelle |
| Reviewer | Revue d’un travail distinct | Rapport et vérifications nécessaires | Ne se déclare pas indépendant de son propre travail |
| DevOps | Construction et livraison préparée | CI/configuration autorisées | Pas d’activation distante implicite |
| Responsable de release | Contrôle du dossier de livraison | Manifeste et rapport | Vérifie le mandat ; ne le crée pas |

Un exécutant peut assumer plusieurs responsabilités lorsque cela est pertinent, en le déclarant. Cette polyvalence ne satisfait pas une exigence de revue indépendante.

## Délégation

Chaque sous-tâche reçoit un périmètre de fichiers et d’actions, ses interfaces, un résultat attendu et les limites héritées. Le parent conserve la responsabilité d’intégration. Les agents ne créent pas de droits supplémentaires pour leurs enfants.

Éviter les écritures concurrentes ; un worktree aide à organiser le travail sans constituer une isolation de sécurité. Les restrictions nécessaires doivent être appliquées par les outils et le système.

Voir [modèle de délégation](../templates/DELEGATION.md) et [revue](../workflows/FEATURE-REVIEW.md).

