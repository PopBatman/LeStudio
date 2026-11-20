# Preuves du cadrage

- Le [relevé de la lecture centrale](RESEARCH.md) décrit le cas tennis-ai et la provenance des champs.
- La [maquette HTML](evidence/maquettes.html) s’ouvre localement dans le dépôt. Le [compte rendu visuel](VISUAL-REVIEW.md) renvoie aux captures du prototype et au résultat des vérifications clavier et mobile.
- Les sources et résultats de la [relecture indépendante](REVIEW.md) portent sur le cadrage. La prochaine mission prévoit ses propres tests d’intégration sur la fiche Django.
- Le [registre](task.json) conserve le mandat, l’identifiant exact du Kanban et les empreintes des pièces de conception.

Le CLI Workflow AI 1.0 accepte les identifiants à un seul segment numérique. La commande standard de planification refuse ARCH-002-01 avant de lire ses documents. Pour rendre le contrôle complémentaire reproductible, depuis la racine commune, exécuter le bloc suivant. Il adapte uniquement la reconnaissance de cet identifiant le temps du processus puis réutilise les vérifications de planification et le calcul d’empreinte du paquet installé.

```bash
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, "workflow-ai/scripts")
import workflow
task = "ARCH-002-01"
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path("studio"), task, "planning"))
print(workflow.contract_fingerprint(Path("studio"), task))
PY
```

## Vérifications de réalisation

| Observation | Pièces |
|---|---|
| RED sur la page initiale, GREEN des neuf tests ciblés | [RED](evidence/produit-red.log) et [suite ciblée](evidence/produit-tests-fiche.log) |
| Suites complètes | [PostgreSQL](evidence/produit-postgresql.log) et [SQLite](evidence/produit-sqlite.log) |
| Parcours réel et clavier | [Résultats Chromium](evidence/produit-navigateur.json), [bureau confirmé](evidence/produit-bureau-confirme.png), [bureau vide](evidence/produit-bureau-vide.png), [mobile après échec](evidence/produit-mobile-echec.png), [mobile en lecture](evidence/produit-mobile-lecture.png) |
| Vérification sur le poste et revue | [Lecture de tennis-ai](evidence/produit-poste.json) et [avis indépendant](REVIEW.md) |

Pour contrôler les preuves produit, le même bloc Python de contrôle complémentaire s’applique avec la phase verification. Le contrôle global standard reste disponible via validate_workspace.py.
