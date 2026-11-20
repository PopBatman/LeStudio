# Protection de l’espace de travail

Le serveur contrôle l’activité du compte et l’appartenance explicite au groupe à chaque accès protégé. Le formulaire de connexion et la déconnexion exigent un jeton CSRF. Le cookie de session est HttpOnly et SameSite Lax sur la boucle locale HTTP. La déconnexion invalide la session en base. Les réponses sensibles ne sont pas mises en cache. Les fixtures utilisent des mots de passe éphémères exclus des traces et des captures. L’opérateur reçoit un compte sans privilège administratif Django. Le rôle PostgreSQL applicatif garde ses droits initiaux.
