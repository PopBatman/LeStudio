# ARCH-001 — Tasklist de réalisation

Plan du 18 novembre 2026 pour `studio/`. Les résultats et les commandes observées sont consignés dans [REPORT.md](REPORT.md).

1. Poser les tests des réglages obligatoires et du contrat HTTP, puis réaliser `manage.py`, `central/` et `tests/`. Le service web écoute sur 8000 et répond sur `/health/`.
2. Verrouiller les dépendances dans `requirements.txt` et les images dans `Dockerfile` et `compose.yaml`. Ajouter les fichiers d’exclusion, un exemple de configuration, la génération locale des secrets et l’initialisation du rôle PostgreSQL sous `infra/`.
3. Exécuter la CI minimale définie dans `.gitlab-ci.yml` au niveau de ses commandes locales. Vérifier une première migration sur un volume isolé, une seconde migration, le signal HTTP et le comportement lors d’une indisponibilité de PostgreSQL.
4. Reproduire le démarrage du [guide produit](../../../README.md), faire examiner les fichiers et les preuves par une exécution indépendante, puis compléter le registre et le rapport.

Les identifiants ci-dessous sont des repères de travail. Une case cochée doit correspondre à un résultat réellement observé ; elle ne crée aucune autorisation.

## A. Préparer le périmètre sur le dépôt cible

- [x] **ARCH-T01 — Examiner l’existant en lecture seule.** Identifier les fichiers pertinents, la structure, les dépendances et la CI ; ne pas lire de secrets.
- [x] **ARCH-T02 — Rapprocher le mandat et les chemins.** Identifier les actions autorisées, renseigner la portée réelle dans le dossier de travail et exposer les écarts qui changent le besoin.
- [x] **ARCH-T03 — Qualifier la stack.** Relever l’environnement, vérifier les documentations primaires, choisir les versions compatibles et la stratégie de verrouillage.
- [x] **ARCH-T04 — Compléter l’architecture et la sécurité du lot.** Fixer les entrées, responsabilités, services locaux, variables et critères de refus ; préciser la place du moteur.
- [x] **ARCH-T05 — Ajuster ce plan.** Décrire les fichiers effectivement concernés et leurs dépendances avant de coder.

## B. Installer la fondation locale du Studio

- [x] **ARCH-T06 — Créer ou adapter la structure Django centrale.** Préserver l’existant et utiliser le découpage minimal justifié par le lot.
- [x] **ARCH-T07 — Mettre en place la configuration.** Séparer paramètres et valeurs secrètes, préparer un exemple sans secret et valider les paramètres indispensables.
- [x] **ARCH-T08 — Définir l’exécution Docker locale.** Construire l’application et définir PostgreSQL, services, réseau et volumes de développement.
- [x] **ARCH-T09 — Préparer la persistance.** Appliquer les migrations sur une base PostgreSQL de test identifiée.
- [x] **ARCH-T10 — Préparer le signal technique.** Vérifier le démarrage et le raccordement requis sans exposer de données sensibles.
- [x] **ARCH-T11 — Documenter les points d’extension.** Rendre les frontières métier/connecteur/UI lisibles ; ne créer que les structures utiles.

## C. Vérifier et préparer la suite

- [x] **ARCH-T12 — Vérifier les comportements de configuration.** Tester le démarrage autorisé et le refus de paramètres invalides, avec diagnostics sans secret.
- [x] **ARCH-T13 — Vérifier les migrations PostgreSQL.** Utiliser une base neuve jetable puis une nouvelle exécution, sans toucher aux données existantes.
- [x] **ARCH-T14 — Exécuter les contrôles Django et les tests pertinents.** Enregistrer commandes, codes retour et environnement.
- [x] **ARCH-T15 — Préparer ou adapter la CI minimale.** Préserver la CI existante ; reproduire les contrôles locaux retenus, sans job de déploiement implicite.
- [x] **ARCH-T16 — Vérifier la reproductibilité documentaire.** Relire et, si possible, refaire le démarrage avec les instructions écrites.
- [x] **ARCH-T17 — Effectuer la revue.** Utiliser une exécution distincte lorsque la revue indépendante est requise et disponible ; signaler toute limite.
- [x] **ARCH-T18 — Rédiger le rapport et capitaliser.** Relier preuves et révision, décrire écarts et décisions, préparer la prochaine feature sans la choisir implicitement.

## Dépendances et délégation

| Travail | Dépend de | Délégation possible |
|---|---|---|
| Recherche de compatibilité | Inventaire initial | Recherche en parallèle de l’analyse documentaire |
| Structure et configuration | Mandat, versions, contrats du lot | Backend avec périmètre de fichiers explicite |
| Docker et CI | Versions et structure convenues | DevOps, en coordination avec les fichiers de configuration |
| Vérification | Résultat implémenté et critères | QA distincte si le runtime le permet |
| Revue | Diff final et preuves | Relecteur distinct du développeur |

La présence de rôles dans le paquet ne les lance pas. Les tâches concurrentes ne modifient pas le même fichier sans coordination.

## UI et TDD

UI : **non requise** pour ce lot technique ; maquette et validation visuelle non applicables dans le périmètre actuel. Toute addition d’un écran déclenche une mise à jour du périmètre et des paliers UI.

Le TDD est pertinent pour les comportements de validation ou de refus ajoutés. Un test qui échoue uniquement parce que Docker ou une dépendance manque ne constitue pas un RED métier. Les fichiers de configuration reçoivent les contrôles de démarrage et de compatibilité adaptés.

## Conditions de fin

Les critères AC-01 à AC-12 de [SPEC.md](SPEC.md) sont renseignés par des preuves ou des écarts explicitement ouverts. Les contrôles non exécutés ne sont pas présentés comme réussis. Aucun push, déploiement distant ou changement de permissions n’est inclus par défaut.

