# Qualification du 18 novembre 2026

L’inventaire de `studio/` a trouvé la documentation produit et ARCH-001, sans application, historique Git ni CI existante. Ubuntu 24.04.4, Python hôte 3.12.3, Docker client/serveur 29.6.1 et Compose 5.3.1 ont été observés. Le port local 8000 était disponible.

| Choix | Version | Qualification |
|---|---|---|
| Python | 3.12.16, image slim Bookworm | [Image officielle Python](https://hub.docker.com/_/python) |
| Django | 5.2.19 LTS | Python 3.12 pris en charge. [Django 5.2](https://docs.djangoproject.com/en/5.2/releases/5.2/) |
| PostgreSQL | 17.12, image Bookworm | Branche maintenue et compatible avec Django. [Versions PostgreSQL](https://www.postgresql.org/support/versioning/) et [backend Django](https://docs.djangoproject.com/en/5.2/ref/databases/#postgresql-notes) |
| Psycopg | 3.3.9, distribution binaire | [Publication Psycopg](https://pypi.org/project/psycopg/3.3.9/) |
| Wagtail | 7.4.4, compatibilité du moteur futur | [Matrice Wagtail 7.4](https://docs.wagtail.org/en/stable-7.4.x/releases/upgrading.html) |
| Compose | 5.3.1 sur le poste | [Dépendance sur un service sain](https://docs.docker.com/compose/how-tos/startup-order/) |

Les versions Python directes et transitives sont verrouillées dans `requirements.txt`. Les deux images de base sont identifiées par leur empreinte de manifeste. Recherche de compatibilité déléguée à `/root/versions`.
