# Vérifications de FEAT-002

Le [registre du lot](task.json) conserve les empreintes et dates des fichiers observés. Les deux références initiales concernent la maquette de cadrage.

- [Premier test HTTP en échec](evidence/web-red.log), conservé à titre historique. Avant la réalisation, la route Clients retournait 404 au lieu de diriger le visiteur vers la connexion. La suite finale vérifie cette route.
- [Suite PostgreSQL](evidence/postgresql.log) et [suite SQLite](evidence/sqlite.log). Le test de deux sessions concurrentes demande les verrous PostgreSQL. La suite SQLite le signale comme ignoré.
- [Migration depuis FEAT-001](evidence/migration.log) et [pile de développement](evidence/poste.json). La migration a aussi été appliquée sur la pile habituelle avec son volume existant.
- [Parcours Chromium](evidence/browser.json), [fiche desktop](evidence/fiche-desktop.png) et [fiche mobile](evidence/fiche-mobile.png). L’analyse automatisée axe porte sur ces deux états de la fiche.
- [Exercice sur données fictives](evidence/privacy.json). PostgreSQL a fourni la sauvegarde et la restauration du registre utilisé pour l’exercice.
- [Revue indépendante](REVIEW.md). L’avis distingue le cadrage et le code exécuté.
