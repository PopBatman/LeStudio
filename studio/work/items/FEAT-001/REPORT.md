# FEAT-001 — Accès opérateur et espace de travail

L’[espace de travail local](http://127.0.0.1:8000/) accueille l’opérateur et affiche son identifiant et son rôle. Un visiteur est dirigé vers la connexion. Le [guide de démarrage](../../../README.md) explique comment créer le premier compte avec une saisie masquée. Le compte fictif des captures a été créé dans la pile de qualification.

| Critère de la carte | Résultat vérifié |
|---|---|
| Accès direct | La racine redirige un visiteur vers la connexion. Le statut de superutilisateur seul ne donne pas le droit opérateur. |
| Accès autorisé | La commande crée un compte actif du groupe Opérateurs Studio, sans droits staff ni superutilisateur. La connexion ouvre l’accueil, qui affiche l’identifiant après rechargement. |
| Refus et expiration | Une erreur générique couvre les identifiants invalides et les droits insuffisants. Le formulaire efface le mot de passe. Une session expirée revient à la connexion. Un retrait de groupe produit un écran 403 et permet de quitter la session. |
| Déconnexion | Le bouton utilise POST avec CSRF. La session disparaît en base et la visite suivante demande de se connecter. |
| Formulaires et compte local | Les tests contrôlent les jetons CSRF, le hachage et la validation du mot de passe, les doublons et l’annulation d’une création incomplète. |
| Rendu | Connexion et accueil examinés à 1440 × 960 et 390 × 844. Le refus a aussi été vérifié à 390 px. Les styles restent accessibles quand la galerie est désactivée. |

Les 19 tests Django ont réussi sur SQLite en mémoire, puis sur une base PostgreSQL dédiée dans Docker. Les parcours navigateur ont utilisé le serveur Django et les sessions PostgreSQL de la pile de qualification. La pile locale habituelle a ensuite été contrôlée avec son volume existant, les migrations Auth et Sessions appliquées et la galerie active. Le job GitLab est configuré pour préparer une base PostgreSQL de test. Sa qualification dans un runner hébergé reste ouverte.

L’agent `/root/operator_auth` a réalisé les vues, les contrôles et leurs tests. `/root/operator_creation` a réalisé la commande et ses tests. `/root/operator_ui` a réalisé les écrans. `/root` a intégré Docker, les réglages de test, la documentation et la qualification. `/root/operator_review` a rendu un [avis indépendant favorable](REVIEW.md). Les résultats détaillés et leurs limites figurent dans le [registre de preuves](EVIDENCE.md).
