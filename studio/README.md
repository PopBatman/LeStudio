# Studio

Studio permet de préparer et de maintenir des sites clients. Le Studio central s’exécute localement avec Django et PostgreSQL dans Docker. L’accueil protégé permet à l’opérateur d’ouvrir sa session. Le serveur expose aussi le signal de disponibilité `/health/` et une galerie de composants. Wagtail est prévu pour le moteur éditorial des sites.

Le [guide d’exploitation dans Notion](https://www.notion.so/41e49e23bbdb8169be2de690a427bc5c) donne les commandes pour créer un Studio indépendant, provisionner un site Wagtail et reprendre la configuration Tennis AI existante.

## Démarrer sur son poste

Depuis `studio/`, avec Python 3, Docker et son plugin Compose, exécuter :

```bash
python3 scripts/init_env.py
docker compose up -d --build --wait
curl --fail http://127.0.0.1:8000/health/
```

Le premier démarrage télécharge les images, initialise le volume PostgreSQL et applique les migrations. La réponse attendue est `{"status": "ok"}`. Si la base devient indisponible, le même point de contrôle renvoie HTTP 503.

Les secrets de développement se trouvent dans le fichier local `.env` créé au premier lancement. Conserver ce fichier avec le volume PostgreSQL pour les démarrages suivants. Pour choisir un autre port, définir `STUDIO_PORT` dans `.env`, puis relancer Compose. Les paramètres sont décrits dans l’[exemple de configuration](local.env.example).

## Premier accès opérateur

Depuis `studio/`, créer un compte sur la pile démarrée. Remplacer `mon-identifiant` par l’identifiant choisi.

```bash
docker compose exec web python manage.py create_operator mon-identifiant
```

Saisir le mot de passe aux deux invites masquées, puis ouvrir [l’espace de travail](http://127.0.0.1:8000/). La commande crée un utilisateur actif du groupe **Opérateurs Studio**, avec un mot de passe haché, et refuse de modifier un identifiant existant. La connexion ouvre l’accueil personnel. Le bouton **Se déconnecter** termine cette session. Après expiration, ouvrir de nouveau l’accueil pour se reconnecter.

Le serveur vérifie le groupe à chaque consultation. Un compte déjà connecté dont on retire le droit reçoit un refus et peut se déconnecter. Les privilèges d’administration Django sont distincts de cet accès.

## Clients et sites

Depuis l’espace privé, ouvrir **Clients** ou **Mes sites** pour consulter les fiches autorisées. Un nouveau compte opérateur commence avec un portefeuille vide. Le [guide du registre](docs/REGISTRE.md) décrit les mandats et leur attribution.

## Moteur Wagtail

Une fiche Site peut être raccordée manuellement à une instance Wagtail indépendante. Le [guide de raccordement](docs/MOTEUR-WAGTAIL.md) décrit le profil de confiance, les droits et les commandes.

## Galerie de composants

Après le démarrage, ouvrir [la galerie locale](http://127.0.0.1:8000/ui/). Le sommaire donne accès aux fondations visuelles, aux actions, aux formulaires, aux messages et aux tableaux. Les exemples utilisent des données fictives.

Le service Compose active la galerie avec `STUDIO_UI_GALLERY=1`. Lorsque cette option est désactivée, Django masque la galerie. L’espace opérateur conserve ses styles. Le CSS compilé et la police sont livrés avec le projet. Pour modifier les styles, exécuter depuis `studio/` avec Node 22 ou supérieur :

```bash
cd frontend
npm ci
npm run build
cd ..
docker compose up -d --build --wait web
```

Le [contrat des composants](docs/COMPOSANTS-UI.md) précise les entrées et les états réutilisables dans les prochains écrans.

## Vérifier, arrêter et reprendre

```bash
docker compose ps
docker compose exec -T web python manage.py check
docker compose exec -T web python manage.py migrate --check
docker compose exec -T web python manage.py test
docker compose down
docker compose up -d --wait
```

La commande locale de test utilise SQLite en mémoire. Le job GitLab prépare une base PostgreSQL de test dédiée au rôle applicatif. Le parcours d’intégration du [lot opérateur](work/items/FEAT-001/REPORT.md) utilise PostgreSQL dans Docker.

L’arrêt avec `down` conserve les données dans le volume du projet. Si le démarrage échoue, consulter `docker compose logs --tail=50 web db`. Un port déjà utilisé se règle via `STUDIO_PORT`. Si PostgreSQL refuse la connexion après une modification des identifiants, restaurer les valeurs qui correspondent au volume ou effectuer une rotation coordonnée du mot de passe dans la base et la configuration.

## CI du projet

Le [job GitLab](.gitlab-ci.yml) utilise `studio/` comme racine du dépôt et un runner qui prend en charge les services Docker. Configurer la variable masquée `STUDIO_CI_POSTGRES_PASSWORD` avec un secret réservé à la base jetable du job. La clé Django et le mot de passe du rôle applicatif sont générés pour chaque exécution.

## Documents du produit

| Pour consulter | Document |
|---|---|
| Le produit, ses utilisateurs et ses parcours | [Fiche projet](project/PROJECT.md) |
| Les décisions retenues et les questions ouvertes | [Décisions](project/DECISIONS.md) |
| Les technologies prévues | [Stack](project/STACK.md) |
| Le service de révisions locales par site | [Brouillons de composition](docs/BROUILLONS.md) |
| Les responsabilités métier, connecteurs et UI | [Contrats d’architecture](docs/ARCHITECTURE-CONTRACTS.md) |
| Les fondations locales du Studio central | [Spécification ARCH-001](work/items/ARCH-001/SPEC.md) et [liste des tâches](work/items/ARCH-001/TASKLIST.md) |
| Les règles produit et les idées de modules d’origine | [Règles techniques](reference/REGLES-SOURCE.md) et [catalogue](reference/CATALOGUE.md) |
