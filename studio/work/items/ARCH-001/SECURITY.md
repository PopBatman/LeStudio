# Sécurité du développement local

Le port web est publié sur 127.0.0.1. Le service PostgreSQL écoute uniquement sur le réseau Compose. Django tourne avec un utilisateur système non privilégié, `DEBUG=False` et une liste de noms d’hôte locaux. Le signal de disponibilité ne contient que l’état du service.

Les clés Django, le mot de passe du rôle applicatif et celui d’initialisation de PostgreSQL sont générés séparément. Le fichier local `.env` est créé exclusivement pour son propriétaire et exclu de Git et de l’image. Les variables manquantes sont signalées par leur nom. Le compte Django dispose des droits nécessaires aux migrations dans sa base et ne détient pas les privilèges d’administration du cluster. Les commandes de vérification n’affichent pas l’environnement résolu.

Les essais utilisent un projet Compose distinct et un volume neuf. Seules les ressources créées par l’essai peuvent être nettoyées. L’arrêt documenté du projet de développement conserve son volume. La configuration du serveur de développement est limitée au poste local.
