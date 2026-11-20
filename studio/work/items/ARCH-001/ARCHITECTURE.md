# Fondation locale du Studio central

Le dossier `studio/` devient la racine du produit. Au début du lot, le dossier contenait project, docs, reference, work et le README. L’inventaire n’avait trouvé ni dépôt Git, ni code applicatif, ni CI produit. Les empreintes SHA256 identifieront la révision examinée.

- `manage.py` et `central/` portent les paramètres, le routage et le contrôle de disponibilité. Le serveur Django de développement s’exécute dans le service Compose `web`. Le démarrage applique les migrations sur PostgreSQL.
- `db` utilise PostgreSQL 17 et un volume propre au projet Compose. Django utilise un rôle applicatif distinct du compte d’initialisation. Le schéma initial utilise les deux migrations de `django.contrib.contenttypes`. 
- `GET /health/` lance une requête `SELECT 1`. Une réponse JSON minimale indique la disponibilité, avec HTTP 200 ou 503 si PostgreSQL est indisponible.
- Les fonctionnalités futures portent leurs règles et leurs permissions dans le backend. Les connecteurs adaptent les systèmes extérieurs, les templates présentent leurs résultats. Le moteur éditorial Wagtail relève d’un futur lot. Les [contrats du produit](../../../docs/ARCHITECTURE-CONTRACTS.md) décrivent ces frontières.

L’environnement local utilise un service web et une seule instance PostgreSQL. Les vérifications isolent leur propre volume et publient le port HTTP sur l’interface de boucle locale. La CI produit utilise Python et un service PostgreSQL jetable.
