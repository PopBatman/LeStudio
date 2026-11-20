# Workflow AI pour Studio

Ce dossier regroupe les règles de travail des agents et les outils qui les accompagnent. Le dossier voisin `studio/` contient les documents propres au produit et les lots de développement. [Projet Studio](../studio/README.md)

| Dossier | Usage |
|---|---|
| [Instructions des agents](AGENTS.md) et `agents/` | Méthode commune et responsabilités des rôles |
| `governance/` | Mandats, permissions, sécurité, tests et preuves |
| `workflows/` et `templates/` | Procédures et modèles de documents pour les lots |
| `scripts/` et `tests/` | Création de lots, contrôles documentaires et tests des outils |
| `integrations/` | Adaptateur Notion et configuration CI GitLab |
| `evidence/` | Preuves de livraison du paquet v1.0.0 |

Les outils se lancent depuis la racine commune, avec Python 3.11 ou supérieur.

```bash
python3 workflow-ai/scripts/validate_workspace.py
python3 workflow-ai/scripts/workflow.py status
```

Pour installer ces deux dossiers dans un autre espace, consulter le [guide d’installation](docs/INSTALLATION.md). Les documents du workflow figurent dans [l’index](docs/INDEX.md).

## Comment une demande devient du code

| Palier | Résultat attendu |
|---|---|
| Découverte | Besoin, sources, périmètre, inconnues et recherche métier proportionnée |
| Spécification | Règles, données, permissions, erreurs et critères d’acceptation |
| Planification | Découpage d’architecture, tasklist ordonnée, stratégie de test |
| Préparation UI, si applicable | Parcours, états, maquette ou références et revue visuelle avant le code |
| Développement | TDD pour les comportements pertinents, changements dans le mandat établi |
| Vérification | Tests observés, intégrations qualifiées au niveau annoncé, navigateur pour l’UI |
| Revue et clôture | Revue, preuves, rapport et mémoire à jour ; publication seulement dans le mandat prévu |

États documentaires : `DRAFT → DISCOVERY → SPECIFIED → PLANNED → READY → IMPLEMENTING → VERIFIED → REVIEWED → DONE`. Ils décrivent le travail ; ils n’accordent aucun droit système et ne déploient rien automatiquement.

## Commandes utiles

Depuis le dossier qui contient `workflow-ai/` et `studio/`, choisir la commande correspondant au besoin.

```bash
python3 workflow-ai/scripts/workflow.py new --id FEAT-001 --kind feature --title "Une capacité métier"
python3 workflow-ai/scripts/workflow.py new --id CONN-001 --kind connector --title "Une intégration fournisseur"
python3 workflow-ai/scripts/workflow.py new --id UI-001 --kind component --title "Un composant partagé" --ui
python3 workflow-ai/scripts/workflow.py check --id ARCH-001 --phase planning
python3 -m unittest discover -s workflow-ai/tests -v
```

Ne pas lancer les trois commandes `new` uniquement pour essayer : elles créent les dossiers de lot dans `studio/work/items/`. Choisir le type correspondant au besoin. Les contrôles disponibles sont `planning`, `implementation`, `verification` et `release`. Une sortie non nulle signale les prérequis manquants ; le script ne modifie pas automatiquement l’état du lot.

Après avoir complété les documents de contrat du lot, utiliser `python3 workflow-ai/scripts/workflow.py fingerprint --id ARCH-001` pour obtenir leur empreinte. Cette commande refuse les documents encore marqués à compléter ; ce refus est attendu sur le dossier ARCH-001 livré avant son travail de conception dans le dépôt cible.

Pour une preuve d’exécution, le registre référence le fichier de preuve, son SHA256, la date, la révision examinée et les fichiers d’entrée. Les preuves de test, capture et revue requises sont aussi reliées à cette empreinte du contrat. Cela permet de repérer des preuves devenues périmées, sans certifier l’identité de leur auteur.

Le champ `active` vaut `true` par défaut. Toutes les preuves actives d’un type requis doivent être réussies et actuelles : un ancien PASS ne masque pas un échec actif. Les RED du TDD et les anciennes révisions sont conservés avec `active: false`, leur résultat original et la raison de leur remplacement. Leurs artefacts restent contrôlés, sans relire les anciennes sources. Une tâche `component` impose `ui_required: true`.

## Capacités et intégrations

| Élément | État livré |
|---|---|
| Processus et contrats | Écrits et installables |
| Installateur, création de lots, contrôles locaux | Code livré et vérifié ; voir les tests du paquet et le rapport de livraison v1.0.0 |
| Délégation aux sous-agents | Protocole prêt ; exécution par les capacités du runtime choisi |
| Notion | Documentation de session mise à jour ; adaptateur local séparé, configuration requise |
| GitLab CI | Fragment de pipeline fourni ; branchement et qualification sur le dépôt cible à effectuer |
| Maquettes et captures | Paliers, critères et livrables définis ; outil disponible à configurer selon le runtime |
| Mémoire | Fichiers persistants et versionnables ; aucune mémoire vectorielle ni service automatique fourni |
| Autorisations et transitions | Vérification documentaire locale ; aucun moteur d’autorisation inviolable livré |

Voir [l’état détaillé](docs/CAPABILITIES.md), [Notion](integrations/notion/ADAPTER.md), [GitLab](integrations/gitlab/README.md) et [les outils MCP](docs/MCP-ET-OUTILS.md).

## Évolution

Les règles évoluent dans `workflow-ai/`. Les décisions et les lots du produit évoluent dans `studio/`. La carte Notion porte la synthèse de pilotage et les décisions humaines du lot. Le dépôt conserve les contrats, le compte rendu technique court et les preuves versionnées. Les procédures réutilisables sont tenues dans leur guide de référence. [Règles de compte rendu](workflows/FEATURE-RAPPORT.md) Une mise à niveau ne doit pas écraser les adaptations du projet : examiner le diff et fusionner explicitement. Ce paquet n’installe pas de daemon, n’altère pas les permissions de l’assistant et n’enregistre aucun secret.
