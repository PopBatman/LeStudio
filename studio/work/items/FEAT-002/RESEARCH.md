# Inventaire et choix de périmètre

Le 18 novembre 2026, la carte était en DISCOVERY avec les règles métier confirmées. Le cadrage rapproche ces règles des composants effectivement présents. [Carte FEAT-002](https://app.notion.com/p/41c49e23bbdb81ed98b0c5d404d27dbf) · [Procédure du Kanban](https://app.notion.com/p/41c49e23bbdb8171b997d6b24d1ca43a).

| Source examinée | Constat | Conséquence pour le lot |
|---|---|---|
| [Projet](../../../project/PROJECT.md) et [contrats](../../../docs/ARCHITECTURE-CONTRACTS.md) | L’opérateur prépare les sites dans le Studio central. Le client est l’entité de rattachement. | Un registre privé suffit. L’édition Wagtail, l’aperçu et la publication relèvent d’autres lots. |
| [Contrôle d’accès](../../../workspace/access.py), [vues](../../../workspace/views.py), [routes](../../../central/urls.py) et [rapport FEAT-001](../FEAT-001/REPORT.md) | Le compte doit être actif et membre du groupe Opérateurs Studio. La commande crée ce compte. Le dépôt ne contient aucun mandat sur un client ou un site. | Conserver cette condition à l’entrée, ajouter des habilitations par objet. Les UUID et le type de client ne confèrent aucun droit. |
| [Composants UI](../../../docs/COMPOSANTS-UI.md) et [accueil](../../../templates/workspace/home.html) | Les champs, alertes, badges, tableaux et états vides sont réutilisables. Les sites de la galerie sont des exemples statiques. | Ajouter la navigation à l’espace protégé et prévoir les écrans du registre. La base métier démarre vide. |
| [Réglages](../../../central/settings.py) et [construction](../../../Dockerfile) | Django, PostgreSQL, sessions et Cotton sont installés. Aucun modèle métier Client, Contact ou Site du Studio n’est enregistré. Le contexte Docker énumère les paquets copiés. | Ajouter une application métier et ses migrations à l’image lors de la réalisation. Conserver le rôle PostgreSQL applicatif existant. |

La carte est la source des règles métier reprises en [spécification](SPEC.md). La proposition technique privilégie une application Django locale et deux tables d’habilitations. Les permissions de modèle seules n’expriment pas l’accès à un site particulier. Une intégration CRM nécessiterait une synchronisation et une diffusion des coordonnées sans besoin identifié dans le lot.

Les contraintes en base et les transactions sont documentées pour la version Django 5.2 du dépôt. Les responsabilités de traitement et les conditions d’usage avec des données réelles figurent dans la [procédure proposée](PROTECTION-DONNEES.md). [Contraintes Django](https://docs.djangoproject.com/en/5.2/ref/models/constraints/) · [Transactions Django](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).
