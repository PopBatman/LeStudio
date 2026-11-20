# Pièces de cadrage
- [Maquette interactive](evidence/maquette.html). Les captures illustrent la [sélection sur ordinateur](evidence/selection-bureau.png), le [rendu périmé sur tablette](evidence/rendu-perime-tablette.png) et le [repli sur mobile](evidence/lecture-mobile.png).
- [Exécution du socle](evidence/socle-feat004.log). Treize tests d’aperçu de l’image Studio locale, exécutés dans un conteneur éphémère sans réseau avec SQLite en mémoire. La nouvelle surface de sélection relève de la réalisation de UI-003-02.
- [Recherche](RESEARCH.md), [revue de conception](VISUAL-REVIEW.md) et [revue indépendante](REVIEW.md). /root/u302architecture a étudié les contrats techniques, /root/u302ux a préparé la maquette et /root/u302review a examiné le cadrage et ses preuves.

Rejouer le contrôle documentaire depuis la racine du projet. La v1 du CLI accepte les identifiants parents ; le contrôle d’un sous-lot reprend la procédure de UI-003-01 et limite le format à son identifiant exact pour la durée du processus.

```sh
python3 -B - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
lot = 'UI-003-02'
workflow.TASK_ID = re.compile(re.escape(lot))
print(workflow.check_task(Path('studio'), lot, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), lot))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Preuves de livraison
- [Comparaison appariée](evidence/comparaison-pixels.json) et [rendu réel au navigateur](evidence/recette-canvas-reel.json). Les deux sites utilisent des données fictives et des instances privées raccordées en mTLS.
- [Sélection, zoom et défilement](evidence/contour-occurrences.json), [incidents et retraits](evidence/recette-canvas-incidents.json), [annonces Orca](evidence/realisation-orca.json).
- [État des bases](evidence/non-publication.json) et [pages publiques](evidence/pages-publiees.json) avant/après le parcours de lecture.
- [Tests PostgreSQL](evidence/realisation-tests-postgresql.log), [tests SQLite](evidence/realisation-tests-sqlite.log), [image et contrôles du poste](evidence/realisation-poste-local.json).
- /root/canvas_server a réalisé le contrat serveur avec tests, /root/canvas_front la coque et le module isolé, /root/canvas_qual le laboratoire de comparaison et /root/u302_real_review la revue indépendante. Le journal de tests conserve les refus attendus et le cas de révocation en cours de rendu.
