# Responsabilités et permissions des agents

Cette matrice décrit la répartition logique du travail. Toute action doit être couverte par le mandat et permise par les protections effectives des outils, du dépôt et des environnements. Un profil de rôle décrit des responsabilités et ne lance aucun processus.

| Rôle | Production principale | Écritures habituelles dans le périmètre | Limite |
|---|---|---|---|
| Orchestrateur | Plan, délégations, intégration, état | Documents de pilotage et intégration explicitement couverte | Ne s’accorde pas un nouveau mandat |
| Chercheur | Sources, options, inconnues | Recherche | Ne présente pas une hypothèse comme décision |
| Analyste métier | Règles et critères | Spécification | Ne choisit pas seul un périmètre non convenu |
| Architecte | Contrats et décisions proposées | Architecture | Ne déploie pas une proposition |
| Sécurité | Risques et vérifications | Analyse, tests autorisés, revue | Aucun élargissement de privilège |
| QA / Test Engineer externe | Tests de référence et preuve RED à partir de la spécification | Tests et preuves attribués | [Règles de modification des tests de référence](TESTING-POLICY.md#tests-de-référence) |
| Développeur (Codex) | Implémentation, migrations et tests complémentaires | Chemins autorisés par le mandat et attribués par la tasklist | [Règles de modification des tests de référence](TESTING-POLICY.md#tests-de-référence) et effets externes limités au mandat |
| Designer UI | Parcours, maquettes, contrats UI | Design et frontend attribué | Une maquette n’est pas une capture réelle |
| Reviewer | Revue et constats sur la révision examinée | Rapport et vérifications autorisées | [Indépendance de la revue](../workflows/FEATURE-REVIEW.md#indépendance) |
| DevOps | Construction et livraison préparée | CI/configuration autorisées | Pas d’activation distante implicite |
| Responsable de release | Contrôle du dossier de livraison | Manifeste et rapport | Vérifie le mandat ; ne le crée pas |

Un exécutant peut assumer plusieurs responsabilités lorsque cela est pertinent, en le déclarant. Appliquer les modalités de [passage entre exécutants](../workflows/FEATURE-DEVELOPPEMENT.md#passage-de-la-spécification-au-code) et de [revue](../workflows/FEATURE-REVIEW.md).

## Délégation

Chaque sous-tâche reçoit un périmètre de fichiers et d’actions, ses interfaces, un résultat attendu et les limites héritées. Le parent conserve la responsabilité d’intégration. Les agents ne créent pas de droits supplémentaires pour leurs enfants.

Éviter les écritures concurrentes ; un worktree aide à organiser le travail sans constituer une isolation de sécurité. Les restrictions nécessaires doivent être appliquées par les outils et le système.

Voir [modèle de délégation](../templates/DELEGATION.md) et [revue](../workflows/FEATURE-REVIEW.md).

