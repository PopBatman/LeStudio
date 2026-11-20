# Vérifications ARCH-002

Le [registre du lot](task.json) relie les sources et les résultats par empreintes. Les vérifications du moteur et du Studio concernent deux projets Django distincts.

| Observation | Artefact |
|---|---|
| Premier test de raccordement en échec avant la création du service, remplacé par la suite centrale complète | [RED historique](evidence/central-red.log) |
| Suite centrale sur PostgreSQL avec concurrence, puis SQLite en mémoire avec les deux cas réservés à PostgreSQL ignorés | [PostgreSQL](evidence/central-postgresql.log) et [SQLite](evidence/central-sqlite.log) |
| Suite moteur sur PostgreSQL, brouillon distinct du contenu publié et réinitialisation idempotente | [Tests Wagtail](evidence/engine-postgresql.log) |
| Passage d’une base FEAT-002 avec une fiche sans domaine | [Migration](evidence/migration.log) |
| Deux instances au digest commun, lectures mTLS, refus, rotation, panne, restauration et mesures | [Observations du laboratoire](evidence/laboratoire.json) et [procédure reproductible](../../../engine/lab/README.md) |
| Migration et disponibilité du Studio habituel | [Contrôle du poste](evidence/poste.json) |
| Examen des corrections sur les diagnostics et la qualification | [Revue](REVIEW.md) |
