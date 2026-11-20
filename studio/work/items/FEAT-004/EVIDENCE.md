# Pièces du cadrage

- [Maquette interactive](evidence/maquettes.html), [observations Chromium](evidence/examen-maquettes.json) et [revue visuelle](VISUAL-REVIEW.md). Les captures illustrent les états et les révisions fictives du parcours.
- [Tests du socle Studio](evidence/socle.log). L’image du conteneur local web a exécuté les suites tests.test_composition_services, tests.test_editorial_transport, tests.test_editorial_services et tests.test_registre_grants avec central.test_settings dans un conteneur jetable sans réseau. SQLite en mémoire, 24 réussites et trois cas ignorés.
- [Revue indépendante](REVIEW.md). Les vérifications du socle et de la maquette précèdent l’intégration prévue dans la [tasklist](TASKLIST.md). Les captures du futur moteur et les relevés de non-publication seront produits lors de cette intégration.

Pour contrôler le dossier depuis la racine, exécuter `python3 -B workflow-ai/scripts/workflow.py check --id FEAT-004 --phase planning`.

## Qualification de la réalisation

| Vérification | Résultat observé |
|---|---|
| Moteur précédent | [Le POST de préparation était absent](evidence/avant-developpement.json). |
| Tests de l’image Studio | [190 réussites sur PostgreSQL](evidence/tests-postgresql.log). [178 réussites sur SQLite, 12 tests réservés à PostgreSQL](evidence/tests-sqlite.log). |
| Moteur Wagtail | [9 tests sur PostgreSQL](evidence/tests-moteur.log). Deux instances indépendantes ont rendu leur page et leur article de même ID natif dans des bases distinctes. Les manifestes et les empreintes identifient chaque instance. Le certificat de diagnostic est refusé pour la préparation. [Transport et refus](evidence/rendu-mtls.json) |
| Absence d’effet métier | Les compteurs, pointeurs live et empreintes de rendu sont identiques avant/après sur les deux instances et les révisions Studio sont identiques. Un GET HTTP de la page publique de chaque article a donné les mêmes octets avant et après le parcours navigateur. [Bases et contenus](evidence/non-publication.json) · [Pages publiques](evidence/pages-publiees.json) |
| Fidélité, isolement et reprise | Parcours au clavier depuis la fiche, formats de 1 200, 820 et 320 pixels, police DM Sans, cinq UUID, image, menu et article. Autre session refusée. Comparaison, suspension hors connexion, reprise et fermeture vérifiées. [Chromium](evidence/navigateur.json) · [Interruption](evidence/interruption-mobile.png) |
| Révision postérieure | Sur la fixture A, une modification intentionnelle crée R4 après les mesures. Le reçu R3 garde l’ancien contenu, indique la nouvelle tête et restitue un diagnostic à expiration. La variante secondaire est visible dans R4. [Contrôle](evidence/peremption.json) |
| Installation locale | Studio et le worker utilisent l’image actualisée. Les 16 révisions et le raccordement existant sont conservés. Sauvegarde locale privée avant activation de Tennis AI, vérification mTLS par l’opérateur, deux pages R16 rendues, connexion Wagtail et page publique disponibles. [Studio](evidence/poste-local.json) · [Tennis AI](evidence/tennis-ai.json) |

Pour rejouer les suites sur des bases de recette dédiées avec le droit de créer une base de test, lancer `python manage.py test tests --settings=central.settings` dans Studio et `python manage.py test reference` dans le moteur. Le laboratoire utilise des projets Compose et des autorités TLS privés et distincts des services du poste.
