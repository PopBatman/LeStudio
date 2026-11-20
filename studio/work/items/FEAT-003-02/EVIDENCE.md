# Preuves de cadrage

- [Maquette interactive](evidence/maquettes.html) et [examen des parcours](VISUAL-REVIEW.md).
- [Exemple de document V2](evidence/navigation-v2.json) et [contrat associé](ARCHITECTURE.md).
- [Revue indépendante](REVIEW.md) et registre d’empreintes dans [task.json](task.json).

Le CLI Workflow AI v1.0 refuse les identifiants de sous-lot avant la lecture des documents. Le contrôle suivant applique les fonctions du workflow à l’identifiant exact de Notion. Depuis la racine de LeStudio, exécuter ce contrôle puis le validateur de l’espace.

```bash
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, "workflow-ai/scripts")
import workflow
task = "FEAT-003-02"
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path("studio"), task, "planning"))
print(workflow.contract_fingerprint(Path("studio"), task))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

Les captures concernent la maquette locale avec données fictives. La vérification de persistance, d’isolation et d’impact réel sur le moteur appartient à la recette après développement.

## Vérifications de réalisation

| Vérification | Résultat |
|---|---|
| TDD validation, services et vues | [Validation](evidence/validation-green.log), [services](evidence/services-green.log), [vues Django](evidence/web-green.log). Les échecs initiaux sont archivés dans le registre. |
| Image Docker Studio et suites complètes | [PostgreSQL](evidence/tests-postgresql.log) et [SQLite](evidence/tests-sqlite.log) |
| Parcours Chromium contre Django et PostgreSQL isolés | [Observations](evidence/application-navigateur.json), [arbre sur bureau](evidence/application-pages-bureau.png), [bilan de renommage](evidence/application-impact-bureau.png), [menu sur téléphone](evidence/application-menus-mobile.png) et [conflit sur petit écran](evidence/application-conflit-mobile.png) |
| Revue indépendante de la réalisation | [Constats, corrections et conclusion](REVIEW.md) |
| Poste Studio, raccordement et état des brouillons | [Contrôle local avant et après mise à jour](evidence/poste-local.json) |

Le contrôle du registre décrit plus haut s’applique également à la phase `verification`. Les écritures de recette ont utilisé des données fictives dans un réseau Docker isolé.
