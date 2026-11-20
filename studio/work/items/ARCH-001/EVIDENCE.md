# ARCH-001 — Preuves du 18 novembre 2026

| Artefact | Ce qui a été observé |
|---|---|
| [Configuration avant correction](evidence/configuration-red.json) | Cinq réglages invalides acceptés à tort, commande en échec. Version historique conservée avec ses entrées propres. |
| [Reproduction isolée](evidence/integration.json) | Versions, empreintes des entrées, identité des images, commandes, migrations, tests, panne et reprise de PostgreSQL, puis nettoyage du projet temporaire. |
| [CI reproduite localement](evidence/ci.json) | Commandes du job GitLab exécutées dans son image avec PostgreSQL. |
| [Démarrage sur le poste](evidence/poste.json) | Services du projet de développement sains, contrôle HTTP 200, mode du fichier local et contenu de l’image. |
| [Revue indépendante](REVIEW.md) | Conclusions de l’exécution distincte et portée de la revue. |

Le registre [task.json](task.json) relie les artefacts à leur SHA256, aux fichiers examinés et à l’empreinte du contrat du lot. L’empreinte des entrées tient lieu de révision pour ce dossier sans historique Git. Les valeurs de configuration privées sont exclues des preuves.
