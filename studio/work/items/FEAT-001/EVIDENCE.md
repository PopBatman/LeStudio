# Preuves du parcours opérateur

Le [registre du lot](task.json) conserve l’instant de chaque observation, la révision des sources et les SHA-256 des artefacts.

| Preuve | Observation du 18 novembre 2026 |
|---|---|
| [Référence avant développement](evidence/maquette.html) | Schéma illustratif des trois états, avec les fondations UI-001. |
| [Premier test en échec](evidence/red.json) | RED historique. Avant la nouvelle route, l’accès anonyme recevait 404 au lieu de la redirection attendue. La suite courante le remplace. |
| [Suite Django et provisionnement](evidence/integration.json) | 19 tests réussis sur chacun des deux moteurs, migrations appliquées et commande interactive exercée via terminal sur une base isolée. Le compte créé était actif, membre du groupe et dépourvu de privilèges administratifs. |
| [Résultat Chromium](evidence/navigateur.json) | Connexion invalide et valide, rechargement, expiration réelle en base, retrait du groupe, 403, déconnexion et refus de l’accès suivant. Aucune violation axe-core détectée dans les règles A/AA exécutées. L’outil laisse un contrôle de contraste indéterminé sur la connexion. |
| [Connexion desktop](evidence/connexion-desktop.png) et [mobile](evidence/connexion-mobile.png) | Formulaire servi par Django, galerie publique de démonstration désactivée dans la pile de test. |
| [Accueil desktop](evidence/accueil-desktop.png) et [mobile](evidence/accueil-mobile.png) | Compte fictif dans l’espace de travail protégé. |
| [Refus mobile](evidence/refus-mobile.png) | Compte authentifié après retrait du groupe. |
| [Pile locale](evidence/poste.json) | Contrôle sur le port 8000, migrations Auth et Sessions appliquées, réponse de santé valide et galerie disponible. |
| [Revue indépendante](REVIEW.md) | Verdict favorable, écrans et comportement clavier examinés. |

La suite automatisée s’exécute avec `docker compose exec -T web python manage.py test`. Les tests de permissions et de création de compte se trouvent dans [test_operator_access.py](../../../tests/test_operator_access.py) et [test_create_operator.py](../../../tests/test_create_operator.py).
