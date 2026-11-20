# Preuves du cadrage

Le [contrôle du format existant](evidence/contrat-v3.json) décrit les réponses du validateur livré pour une grille responsive et pour les extensions de placement proposées. Le [contrat technique](ARCHITECTURE.md) indique les modifications nécessaires avant de pouvoir enregistrer une disposition libre dans un vrai brouillon.

La [maquette interactive](evidence/maquettes.html) utilise des données fictives. La [revue visuelle](VISUAL-REVIEW.md) détaille les interactions éprouvées sur le prototype. La [revue indépendante](REVIEW.md) rapproche le résultat des critères de la carte. Le [registre](task.json) référence les empreintes des pièces de cadrage.

La commande générale de contrôle est `python3 -B workflow-ai/scripts/validate_workspace.py`. Le CLI v1 ne reconnaît pas les identifiants des sous-lots. Le contrôle de planification peut être reproduit depuis la racine de LeStudio avec l’identifiant du dossier pour ce seul processus, comme pour FEAT-003-04.

```sh
python3 -B - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
task = 'FEAT-003-05'
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path('studio'), task, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), task))
PY
```

Les essais de persistance entre éditeurs, de concurrence PostgreSQL, de performance en charge, d’accessibilité sur Django et de non-modification du site actif sont prévus dans la [tasklist](TASKLIST.md).

## Réalisation

| Contrôle | Preuves |
|---|---|
| Contrat V4, compatibilité, accès, conflits et entrée depuis la fiche | [Domaine](evidence/domain-green.log), [HTTP](evidence/http-green.log) et [concurrence PostgreSQL et fiche](evidence/integration-green.log) |
| Régressions dans le paquet livré | [PostgreSQL](evidence/tests-postgresql.log) et [SQLite](evidence/tests-sqlite.log) |
| Déplacement, dimensions, annulation et relecture | [Parcours Chromium](evidence/navigateur.json), [insertion et déplacement au clavier](evidence/clavier.json), [geste tactile](evidence/application-tactile.json) |
| Consultation et erreurs | [Bureau](evidence/application-canvas-bureau.png), [mobile](evidence/application-mobile.png), [lecture seule](evidence/application-lecture-320.png), [conflit](evidence/application-conflit.png), [saisie invalide](evidence/application-erreur.png) |
| Qualification complémentaire | [Annonces Orca et focus](evidence/application-orca.json), [mesures de chargement et dépôt](evidence/performance.json), [revue indépendante](REVIEW.md) |
| Studio local | [Santé, lecture des pages réelles et comparaison des révisions avant et après](evidence/poste-local.json) |

Les enregistrements de recette utilisent des sites fictifs. Dans la phase de réalisation, utiliser `verification` dans le contrôle documentaire décrit plus haut.
