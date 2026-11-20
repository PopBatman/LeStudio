# Preuves du cadrage

| Pièce | Portée |
|---|---|
| [Maquette interactive](evidence/maquettes.html) | Prototype local en mémoire. Les exemples utilisent un site fictif et les rôles sont sélectionnables pour la revue. |
| [Revue visuelle](VISUAL-REVIEW.md) et [contrôle navigateur](evidence/examen-maquettes.json) | Parcours, états, captures et dimensions du prototype éprouvés au cadrage. |
| [Contrôle du socle](evidence/tests-socle.log) | Image locale Studio, conteneur jetable sans réseau, SQLite en mémoire. Les suites test_operator_access, test_registre, test_registre_grants et test_registre_web découvrent 21 tests. Vingt passent et un test de concurrence est réservé à PostgreSQL. |
| [Audit du dépôt](RESEARCH.md) et [revue indépendante](REVIEW.md) | Prérequis réutilisables et rapprochement des cinq critères Notion avec les contrats, la maquette et les essais de réalisation prévus. |

Les fichiers et leurs empreintes sont référencés dans le [registre du lot](task.json). Le CLI v1 attend un identifiant à un seul suffixe numérique. Pour vérifier ce sous-lot existant, charger le même validateur en autorisant uniquement son identifiant dans le processus local.

```sh
python3 -B - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
lot = 'FEAT-003-07'
workflow.TASK_ID = re.compile(re.escape(lot))
print(workflow.check_task(Path('studio'), lot, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), lot))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Vérifications de réalisation

| Contrôle | Pièces |
|---|---|
| Interface réelle, reçu, révocation et mandats | [Recette dans Chromium](evidence/recette-navigateur.json), [portail à 320 px](evidence/app-portail-mobile.png), [reçu](evidence/app-recu-mobile.png), [fiche Site](evidence/app-fiche-site.png), [historique lecteur](evidence/app-historique-lecture.png), [refus](evidence/app-invitation-indisponible.png) |
| Accès public HTTPS, confidentialité et lecture au clavier | [Hôte de portail dédié](evidence/https-local.json), [journaux de recette](evidence/journaux.json), [annonces Orca](evidence/lecteur-ecran.json) |
| Migration depuis Studio existant, restauration et purge | [Migration](evidence/migration.json), [sauvegarde et restauration](evidence/restauration.json), [poste local](evidence/poste-local.json) |
| Image Studio empaquetée et revue | [Suite PostgreSQL](evidence/tests-postgresql.log), [suite SQLite](evidence/tests-sqlite.log), [revue indépendante](REVIEW.md) |

Le contrôle de la livraison utilise la phase `verification` dans la commande ci-dessus. Les fichiers RED conservent les échecs initiaux avant l’implémentation des comportements correspondants.
