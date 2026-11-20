# Vérification documentaire

La [fixture](evidence/composition-v1.json) contient des valeurs fictives. Le registre référence son empreinte et le [compte rendu de contrôle](evidence/examen-document.json). Le contrôle de cette fixture porte sur sa structure, les identités, la parenté, les blocs et les valeurs de l’exemple ; il ne constitue pas une implémentation du validateur ni une preuve de migration ou de concurrence. [Revue indépendante](REVIEW.md)

Le CLI Workflow AI v1.0 filtre les identifiants à un seul segment numérique et refuse FEAT-003-01 avant de lire son dossier. Le contrôle complémentaire conserve l’identifiant Notion et applique les fonctions installées au dossier exact. Depuis la racine de l’espace :

```bash
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, "workflow-ai/scripts")
import workflow
task = "FEAT-003-01"
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path("studio"), task, "planning"))
print(workflow.contract_fingerprint(Path("studio"), task))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Preuves de réalisation

| Contrôle | Résultat conservé |
|---|---|
| Avant implémentation | [RED du service](evidence/service-red.log) et [RED du validateur](evidence/validation-red.log) |
| Validation du contrat V1 | [Essais ciblés du validateur](evidence/validation-green.log) |
| Suites centrales | [PostgreSQL](evidence/tests-postgresql.log) et [SQLite](evidence/tests-sqlite.log) |
| Migration et relecture d’une base de la version précédente | [Migration additive](evidence/migration.log) et [qualification à la limite de taille](evidence/qualification-postgresql.json) |
| Installation locale Studio | [Contrôle du poste](evidence/poste.json) |
| Revue de réalisation | [Avis indépendant](REVIEW.md) |

Le contrôle complémentaire décrit plus haut s’applique à la phase verification pour les pièces de réalisation. La portée du sous-lot est le backend central.

[Mesure après corrections de revue](evidence/limite-finale.json) : 1 Mio compact, 256 blocs, relecture du document identique et des deux révisions. Le contrôle du poste porte sur l’installation habituelle ; les essais d’écriture ont utilisé la base PostgreSQL jetable.
