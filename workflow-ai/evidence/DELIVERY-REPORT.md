# Rapport de livraison — Workflow AI v1.0.0

Date : 18 novembre 2026. Ce rapport concerne le **workflow installable**. Aucune réalisation du produit Studio n’est attribuée à ces vérifications.

## Résultat observé

| Vérification | Résultat |
|---|---|
| Tests de l’installateur | 14 / 14 réussis |
| Tests des contrôles de workflow | 25 / 25 réussis |
| Tests de l’adaptateur Notion, transport simulé | 18 / 18 réussis |
| Total de la suite | **57 / 57 réussis**, Python 3.12.14 sous Linux |
| Installation dans un dossier contenant des instructions existantes | Réussie ; texte d’origine et fichier témoin conservés |
| Simulation | Aucune modification du dossier cible |
| Seconde installation identique | Aucune écriture supplémentaire |
| Validation de la copie installée | Structure, JSON, schémas de tâches et liens locaux acceptés |
| ARCH-001 : phase planning | Réussie ; état DRAFT inchangé |
| ARCH-001 : phase implementation | Refus attendu, mandat et périmètre non renseignés |
| Nouveau composant UI | Créé DRAFT avec UI requise, sans mandat implicite ; plan incomplet refusé |
| Notion REST en simulation depuis la copie installée | 23 documents préparés, zéro appel réseau et aucun registre créé |

Les preuves exactes sont dans [tests.json](tests.json), [tests.log](tests.log) et [install-smoke.json](install-smoke.json). Le test d’installation utilise un chemin contenant un espace et dix commandes réelles. Les chemins temporaires sont remplacés dans le rapport JSON par des repères lisibles.

La validation globale n’exige pas que chaque lot futur soit prêt à implémenter. ARCH-001 garde des marqueurs explicites dans ses documents à compléter et un mandat nul. Le contrôle de planification vérifie la présence de la spécification et de la tasklist ; il n’approuve pas sémantiquement leur contenu.

## Revue distincte et corrections

Les contributions ont été réellement déléguées à des exécutions distinctes : processus, documentation du projet, installateur/CLI. Les fichiers ont été répartis par responsabilité. Une revue distincte du code et une revue des instructions de démarrage ont ensuite identifié les corrections suivantes.

| Constat | Correction et vérification |
|---|---|
| Un job CI seul en stage `.pre` ne créait pas le pipeline attendu dans un dépôt neuf | Utilisation du stage `test` et procédure de raccordement adaptée ; CI distante toujours à qualifier |
| La commande fingerprint était proposée trop tôt sur ARCH-001 | Prérequis et refus attendu expliqués ; aucun contrat incomplet présenté comme prêt |
| La procédure de mise à niveau ne préservait pas correctement le cas de fichiers personnalisés | Fusion manuelle documentée ; réinstallation réservée aux fichiers identiques |
| Une panne d’écriture pouvait laisser un fichier neuf tronqué | Publication du fichier après écriture complète, sans écrasement ; test de panne ciblé réussi |
| Un ancien PASS pouvait masquer un FAIL actuel | Toutes les preuves actives des types requis doivent réussir ; cas contradictoire refusé |
| Un RED historique empêchait le GREEN courant | Historique explicite avec `active: false`, artefact conservé et entrées historiques non relues |
| Un composant pouvait déclarer UI non requise | Invariant de schéma : `component` exige `ui_required: true` |

Le reviewer distinct a reproduit les cas de preuves et de schéma UI après correction, puis relancé les suites installateur et CLI. Aucun défaut bloquant restant n’a été relevé dans ce périmètre. Ce constat est une revue ciblée, pas une certification de sécurité.

## Notion

Quatre pages documentaires v1.0 ont été créées sous la page de workflow existante : installation et capacités, processus de développement, gouvernance et mémoire, ARCH-001. La page d’accueil et la page des processus ont été actualisées avec conservation de l’historique. Les dernières règles de preuves actives et historiques ont été répercutées.

Les identifiants des pages sont conservés dans `integrations/notion/pages.reference.json`. La publication a utilisé la connexion interactive de la session. L’adaptateur REST livré possède ses propres tests hors ligne ; aucune écriture avec un jeton REST local n’a été annoncée ou réalisée pour sa qualification.

## Intégrité et portée

Le fichier `MANIFEST.json` identifie les fichiers du paquet par taille et SHA256. Il est généré pour la livraison ; il n’est pas une signature d’éditeur. Les scripts d’installation vérifient le paquet source. Le validateur du workspace ne contraint pas les futurs documents de travail à ces empreintes, afin qu’ils puissent évoluer dans le dépôt.

Le fichier `reference/source-original.txt` conserve la source utilisateur, SHA256 `3ebb5f058ba72b1bf1fa17bafce63b3e93d8cfe291a64134951473e631bfb956`. Les clarifications actuelles se trouvent dans `project/DECISIONS.md`.

## Non exécuté et limites

- Installation sur la machine de l’utilisateur, macOS ou WSL : non exécutée dans cette session.
- Pipeline GitLab distant, protections de branches, Docker/Scaleway et production : non configurés par cette livraison.
- Application Studio, base PostgreSQL produit et moteurs de sites : non implémentés par ce paquet.
- Écrans, images de maquette et screenshots de Studio : non produits ici ; ARCH-001 n’a pas de périmètre UI.
- Runtime agentique durable, mémoire vectorielle, service d’autorisation et moteur transactionnel de transitions : non fournis.
- Authentification des déclarations d’autorité, qualité sémantique et exhaustivité des preuves : non garanties par des fichiers locaux.
- Retour arrière de l’installateur : best-effort ; aucune transaction multi-fichiers ou protection contre une concurrence hostile n’est promise.

Les contrôles locaux ne donnent aucun droit supplémentaire. Les instructions de l’utilisateur et les permissions effectives des outils demeurent applicables.
