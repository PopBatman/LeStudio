# Installation et mise à jour

## Préparer

Utiliser Python 3.11+ sur Linux ou macOS. Windows : WSL recommandé, commandes et dépôt dans Linux. L’exécution a été vérifiée sur Linux pour cette livraison ; macOS et WSL ne sont pas déclarés testés.

La source contient les deux dossiers frères `workflow-ai/` et `studio/`. Conserver cette disposition ainsi que `workflow-ai/MANIFEST.json`. L’installateur vérifie la taille et l’empreinte SHA256 des fichiers des deux dossiers avant la copie.

Pour installer une seconde copie, choisir un espace cible dont `workflow-ai/` et `studio/` deviendront deux sous-dossiers directs. Donner à `--target` le chemin physique de cet espace parent. L’espace source est déjà utilisable.

## Installer

Depuis la racine de l’espace source, examiner la simulation puis appliquer la copie.

```bash
python3 workflow-ai/install.py --target "/chemin/vers/MonEspace"
python3 workflow-ai/install.py --target "/chemin/vers/MonEspace" --apply
```

| Opération | Effet |
|---|---|
| Sans `--apply` | Simulation et contrôle des conflits ; pas d’écriture |
| Avec `--apply` | Règles et outils dans `workflow-ai/`, documents du projet dans `studio/`, pointeurs dans `AGENTS.md` et `CLAUDE.md` à la racine de l’espace |
| Seconde installation identique | Réutilisation des fichiers identiques, sans multiplication des blocs gérés |
| Fichier déjà présent et différent | Refus avant l’application prévue, sans option d’écrasement forcé |
| Fichier d’instructions racine existant | Texte hors bloc géré conservé |

L’installateur ne lance ni gestionnaire de paquets, ni Docker, ni Git, ni appel réseau. Une erreur système pendant la copie peut laisser une installation partielle : corriger sa cause puis relancer ; les fichiers identiques sont reconnus. Il ne s’agit pas d’une transaction atomique couvrant tous les fichiers.

Les fichiers neufs sont publiés après écriture complète, en mode privé `0600`, par création d’un lien physique sans écrasement. Utiliser un système de fichiers qui prend en charge ces liens, comme les systèmes Linux/macOS usuels. Les permissions des fichiers d’instructions existants sont conservées. Les scripts se lancent avec `python3` et ne demandent pas de bit exécutable.

## Vérifier

Depuis la racine de l’espace installé, exécuter les contrôles suivants.

```bash
python3 workflow-ai/scripts/validate_workspace.py
python3 workflow-ai/scripts/workflow.py status
python3 workflow-ai/scripts/workflow.py check --id ARCH-001 --phase planning
python3 -m unittest discover -s workflow-ai/tests -v
```

Le dossier ARCH-001 contient un plan préparé, avec un mandat d’implémentation non renseigné. Le contrôle `implementation` doit donc refuser son lancement tant que le mandat réel et les chemins du dépôt cible ne sont pas renseignés. Ce comportement attendu n’est pas un échec d’installation.

Les champs déclaratifs ne remplacent pas les autorisations de l’utilisateur ni les protections des outils. Lire [CAPABILITIES.md](CAPABILITIES.md) avant d’interpréter un contrôle réussi comme une garantie de sécurité.

## Raccorder l’assistant

Ouvrir l’espace parent dans l’environnement agentique choisi et lire les pointeurs de son `AGENTS.md`. Ils mènent aux instructions dans `workflow-ai/` et au projet dans `studio/`. `CLAUDE.md` indique les mêmes entrées.

Les rôles de `agents/` sont des instructions. La disponibilité des sous-agents, du navigateur et de la génération d’images dépend du runtime. Relever les capacités réellement exposées, puis appliquer la procédure de [MCP-ET-OUTILS.md](MCP-ET-OUTILS.md). Aucun serveur MCP n’est ajouté automatiquement au compte ou à la machine.

## Mettre à jour un workspace existant

Pour migrer depuis le paquet v1.0.0 monolithique, installer les deux dossiers dans un nouvel espace, comparer les versions puis reporter les adaptations. Les décisions, références et lots existants du projet rejoignent `studio/`. Les règles, modèles et outils de travail rejoignent `workflow-ai/`.

Pour un dossier personnalisé, réaliser la mise à niveau par comparaison et fusion manuelles : conserver les tâches, décisions et adaptations utiles, puis contrôler le résultat avec le validateur. Ne pas relancer l’installateur comme étape de validation de cette fusion : les adaptations conservées diffèrent du paquet et seraient refusées. La réinstallation automatique convient seulement aux fichiers identiques au paquet source, par exemple pour compléter une installation interrompue.

Les instructions racine doivent conserver un seul bloc géré et une seule référence active au processus retenu. Les anciennes consignes incompatibles doivent être corrigées dans un changement explicite.

## Désinstaller

Après avoir conservé les décisions, tâches et preuves utiles, retirer le dossier `workflow-ai/` et uniquement les blocs de référence marqués par l’installateur dans les instructions racine. Aucun script de suppression automatique n’est fourni. Les pages Notion publiées sont indépendantes et ne sont pas supprimées.
