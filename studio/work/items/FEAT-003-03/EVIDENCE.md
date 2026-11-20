# Preuves de cadrage

La [maquette autonome](evidence/maquettes.html) illustre les parcours sur données fictives. Les captures et leurs conditions de vérification sont décrites dans la [revue visuelle](VISUAL-REVIEW.md). L’[exemple de catalogue](evidence/catalogue.json) accompagne le [contrat](ARCHITECTURE.md). Le registre [task.json](task.json) conserve les empreintes des pièces examinées.

Le CLI Workflow AI v1.0 limite la forme des identifiants à un segment numérique. Pour conserver le même identifiant de sous-lot dans Studio et Notion, le contrôle de planification utilise les fonctions installées avec ce seul identifiant admis pour la durée du processus. Depuis la racine de LeStudio, le contrôle se reproduit ainsi.

```bash
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, "workflow-ai/scripts")
import workflow
task = "FEAT-003-03"
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path("studio"), task, "planning"))
print(workflow.contract_fingerprint(Path("studio"), task))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

La [revue indépendante](REVIEW.md) porte sur les documents et le prototype. Les critères de réalisation et leurs tests figurent dans le [plan](TASKLIST.md).

## Vérification de réalisation

| Entrée vérifiée | Résultat observé |
|---|---|
| Migration depuis l’image précédente | [Comparaison des deux brouillons V2 avant et après les migrations](evidence/migration.json) |
| Services, catalogue et vues | [Apparence](evidence/appearance-green.log), [catalogue et promotion](evidence/catalogue-green.log), [vues Django](evidence/web-green.log) et [écritures concurrentes sur PostgreSQL](evidence/concurrence-green.log) |
| Paquet Docker final | [Suite PostgreSQL](evidence/tests-postgresql.log) et [suite SQLite](evidence/tests-sqlite.log) |
| Utilisation dans Chromium | [Relevé](evidence/application-navigateur.json), [bibliothèque](evidence/application-bibliotheque.png), [apparence](evidence/application-apparence.png), [revue de promotion](evidence/application-promotion.png), [occurrence sur téléphone](evidence/application-occurrence-mobile.png), [conflit](evidence/application-conflit-mobile.png), [lecture seule](evidence/application-lecture-mobile.png) et [diagnostic](evidence/application-diagnostic.png) |
| Studio local | [Santé et empreinte des révisions réelles après mise à jour](evidence/poste-local.json) |

Les tests en échec avant développement restent archivés sous leur nom se terminant par `-red.log`. Le contrôle complémentaire présenté plus haut vérifie le registre de réalisation en remplaçant la phase `planning` par `verification`. Les essais d’écriture et de revue ont utilisé des sites fictifs.
