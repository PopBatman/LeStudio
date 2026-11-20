# Pièces du cadrage
- [Socle de composition, catalogue et canvas](evidence/socle.log). Trente tests de l’image Studio sur SQLite en mémoire.
- [Socle de concurrence](evidence/concurrence-socle.log). Cinq tests existants de l’éditeur, du catalogue et des services éditoriaux sur une instance PostgreSQL temporaire, dans un réseau interne isolé.
- [Maquette interactive](evidence/maquette.html), [revue visuelle](VISUAL-REVIEW.md) et [revue indépendante](REVIEW.md). La direction artistique de référence est celle de UI-003-01.
- /root/u303_arch a étudié les contrats serveur et leur sécurité ; /root/u303_mock a préparé la maquette et son examen au navigateur ; /root/u303_review a assuré la revue indépendante du cadrage.

Le contrôle documentaire du sous-lot reprend la procédure déjà employée pour UI-003-02. Depuis la racine de l’espace, la restriction locale de format applique le validateur v1 à l’identifiant exact du sous-lot.

```sh
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
lot = 'UI-003-03'
workflow.TASK_ID = re.compile(re.escape(lot))
print(workflow.check_task(Path('studio'), lot, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), lot))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Vérifications de réalisation

Les [tests PostgreSQL](evidence/realisation-tests-postgresql.log) et [SQLite](evidence/realisation-tests-sqlite.log) couvrent le service de lot et son entrée HTTP avec le reste de Studio. Les recettes sur sites fictifs couvrent les [droits par opérateur et site](evidence/realisation-droits.json), le [rejeu après une réponse perdue](evidence/realisation-modele.json), le [conflit concurrent](evidence/realisation-conflit.json), la [panne moteur et la révocation](evidence/realisation-indisponibilite.json). Les captures du produit sont référencées dans la [revue visuelle](VISUAL-REVIEW.md).
