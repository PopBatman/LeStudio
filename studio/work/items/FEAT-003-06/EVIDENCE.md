# Preuves du cadrage

| Pièce | Ce qu’elle permet de contrôler |
|---|---|
| [Essai du socle Studio](evidence/socle-studio.json) | Édition locale en V4 avec préservation du placement et de l’historique, refus des données invalides ou étrangères ; état du résolveur livré. |
| [Essai du moteur](evidence/revisions-wagtail.json) | Quatre routes existantes, distinction brouillon/publication et effet d’une restriction héritée avec Wagtail 7.4.4. |
| [Maquette interactive](evidence/maquettes.html) et [revue visuelle](VISUAL-REVIEW.md) | Changements locaux et comparaison d’une référence sur données fictives. Le prototype simule l’échange éditorial. |
| [Revue indépendante](REVIEW.md) | Rapprochement avec les cinq critères Notion et vérifications distinctes du socle et du parcours. |

Les essais futurs sur le nouveau connecteur, les deux instances, la concurrence et les permissions administratives sont inscrits dans la [tasklist](TASKLIST.md). Les sources du contrôle d’intégrité des pièces sont consignées dans le [registre](task.json).

Le CLI Workflow AI v1 filtre les identifiants de sous-lots avant lecture de leur dossier. Comme pour le lot 05, on peut exécuter la vérification depuis la racine avec le seul identifiant local autorisé pour ce processus.

```sh
python3 -B - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
task = 'FEAT-003-06'
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path('studio'), task, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), task))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Vérifications de réalisation

| Contrôle | Résultat enregistré |
|---|---|
| Édition locale, historique, image révoquée et destination de bouton invalide | [Parcours HTTP sur le site B](evidence/edition-simple.json) |
| Comparer, conserver, adopter après une troisième publication, détacher | [Parcours Chromium](evidence/navigateur.json), [capture de comparaison](evidence/application-comparaison-bureau.png) |
| Consultation mobile et annonce d’un refus au clavier | [Lecture à 320 px](evidence/application-lecture-320.png), [annonces Orca](evidence/lecteur-ecran.json) |
| Deux moteurs, anciens profils, migrations, permissions de publication et TLS | [Recette Wagtail](evidence/moteur-qualification.md) |
| Préservation du brouillon avant et après la migration centrale | [Empreintes de la révision de recette](evidence/migration.json) |
| Image Studio, migrations, couverture concurrente et contrôle local | [PostgreSQL](evidence/tests-postgresql.log), [SQLite](evidence/tests-sqlite.log), [poste local](evidence/poste-local.json) |
| Revue indépendante et correctifs requalifiés | [Revue de réalisation](REVIEW.md) |

Pour contrôler la livraison avec la commande ci-dessus, utiliser la phase `verification`.
