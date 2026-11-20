# ARCH-001 — Fondation locale du Studio central

Le 18 novembre 2026, le projet Compose `lestudio-local` a démarré dans `studio/`. Django répond sur [le signal local](http://127.0.0.1:8000/health/). Le [guide produit](../../../README.md) décrit le démarrage, l’arrêt et la conservation des données. Le moteur éditorial Wagtail sera traité dans un lot ultérieur.

| Critères | Observations |
|---|---|
| AC-01, AC-02 | L’[inventaire et la qualification](RESEARCH.md) décrivent la documentation de départ et les versions retenues. L’installation dans l’image utilise les empreintes vérifiées des distributions Python. |
| AC-03, AC-04 | Construction de l’image, démarrage de deux services sains. Django 5.2.19 utilise Psycopg 3.3.9 avec PostgreSQL 17.12. Le processus web s’exécute sous l’UID 10001. |
| AC-05 | Les deux migrations de `contenttypes` se sont appliquées sur un volume neuf. Le deuxième passage et le redémarrage après `down` n’ont annoncé aucune migration à appliquer. |
| AC-06 | Requête HTTP réelle après démarrage, après arrêt de PostgreSQL, puis après reprise. Les réponses ont été 200, 503 et 200, avec pour seul champ JSON `status`. |
| AC-07, AC-08 | Quatre méthodes de test Django réussies, dont une couvre cinq configurations invalides. Avant correction, ces cinq cas étaient acceptés. Les vérifications couvrent les diagnostics, les hôtes autorisés, les méthodes HTTP et la réponse d’erreur. Le compte applicatif ne possède aucun des privilèges superuser, createdb et createrole. Le fichier de secrets local a le mode 0600 et est absent de l’image. |
| AC-09 | Les commandes du job GitLab ont été exécutées localement dans l’image Python désignée, avec un service PostgreSQL jetable, le rôle applicatif, les migrations, les tests et le signal de disponibilité. Le pipeline hébergé, ses variables et son runner restent à qualifier dans GitLab. |
| AC-10 | `central/` regroupe les réglages et la route technique. Les frontières entre fonctionnalités, connecteurs et présentation sont consignées dans [l’architecture](ARCHITECTURE.md). |
| AC-11 | La procédure du README a été reproduite sur une copie isolée, avec ses propres secrets, réseau, volume et port. La configuration existante a été conservée au second appel du générateur. |
| AC-12 | Les commandes observées, les résultats, les empreintes de révision et la [revue indépendante](REVIEW.md) sont reliés au [registre des preuves](EVIDENCE.md). |

## Exécutions

`/root/versions` a qualifié la compatibilité en lecture seule. `/root/django` a réalisé le backend, le verrou Python et les tests. `/root/infra` a réalisé Docker, la configuration locale et le job CI. `/root` a intégré, documenté et reproduit le démarrage. `/root/revue_arch` a rendu un avis favorable après revue indépendante.

Le poste a été vérifié sous Linux amd64. Les images versionnées sont identifiées dans Dockerfile et compose.yaml. Le verrou Python inclut les roues amd64 et arm64. Seule l’exécution amd64 a été observée. La portée de cette réalisation est le développement local.
