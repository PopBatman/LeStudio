# FEAT-001 — Accès opérateur et espace de travail

Un opérateur local peut ouvrir Studio à la racine, se connecter, retrouver son identité et ses droits, puis sortir de sa session. Les sites et clients sont traités dans FEAT-002. [Carte du Kanban](https://app.notion.com/p/41c49e23bbdb81bb9f5ef1f4e259ff5a).

| Situation | Comportement attendu |
|---|---|
| Visiteur ou session expirée | La racine redirige vers la connexion. Le formulaire permet d’ouvrir ou de reprendre une session. |
| Identifiants invalides, compte inactif ou hors groupe | Erreur générique sans détail sur le compte. Le mot de passe est effacé. |
| Compte actif membre du groupe Opérateurs Studio | Connexion puis accueil protégé, identité affichée et navigation au clavier. Une prochaine visite retrouve sa session. |
| Compte déjà authentifié dont le droit est retiré | Refus serveur 403 avec moyen de quitter la session. Le statut staff ou superutilisateur seul ne confère aucun accès opérateur. |
| Déconnexion | Action POST avec CSRF, session invalidée, retour à la connexion. |
| Premier compte | Commande locale interactive, mot de passe validé et haché. Aucun compte prédéfini, aucune inscription publique. |
