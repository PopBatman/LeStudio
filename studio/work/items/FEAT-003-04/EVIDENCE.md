# Preuves de cadrage

La [maquette autonome](evidence/maquettes.html) illustre l’entrée Atelier et l’édition d’une page. Les états examinés, les captures et les limites du prototype sont décrits dans la [revue visuelle](VISUAL-REVIEW.md). Le [modèle V3 fictif](evidence/template-v3.json) accompagne le [contrat de création et d’édition](ARCHITECTURE.md). La [revue indépendante](REVIEW.md) précise les vérifications sur la fixture, le socle et l’interface. Le fichier [task.json](task.json) conserve les empreintes.

Le CLI Workflow AI v1.0 refuse la forme d’identifiant d’un sous-lot avant de lire ses pièces. Pour contrôler le dossier exact, conserver FEAT-003-04 et exécuter les fonctions de planification installées avec cet identifiant pour le seul processus de vérification. Depuis la racine de LeStudio, lancer les commandes suivantes.

```bash
python3 -B - <<'PY'
import re, sys
from pathlib import Path
sys.path.insert(0, "workflow-ai/scripts")
import workflow
task = "FEAT-003-04"
workflow.TASK_ID = re.compile(re.escape(task))
print(workflow.check_task(Path("studio"), task, "planning"))
print(workflow.contract_fingerprint(Path("studio"), task))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Vérification de réalisation

| Contrôle | Preuve |
|---|---|
| Création, édition et droits par site | [Tests métier](evidence/services-green.log), [vues Django](evidence/web-green.log) et [entrée depuis la fiche](evidence/fiche-green.log) |
| Création simultanée depuis Pages et Atelier, écriture simultanée depuis Apparence et Atelier | [Deux courses PostgreSQL indépendantes](evidence/editor-concurrency-postgres.log) |
| Régressions sur l’image de livraison | [Suite PostgreSQL](evidence/tests-postgresql.log) et [suite SQLite](evidence/tests-sqlite.log) |
| Parcours sur trois largeurs, clavier, erreur et reprise après conflit | [Observations Chromium](evidence/navigateur.json), [départ sur téléphone](evidence/application-depart-mobile.png), [éditeur sur bureau](evidence/application-atelier-bureau.png), [conflit](evidence/application-conflit-mobile.png), [erreur](evidence/application-erreur-mobile.png) et [lecture seule à 320 px](evidence/application-lecture-320.png) |
| Annonces et focus | [Énoncés produits par Orca](evidence/application-orca.json) |
| Revue de la réalisation et mise à jour du poste | [Revue indépendante](REVIEW.md) et [contrôle du Studio local](evidence/poste-local.json) |

La phase `verification` contrôle le dossier de réalisation avec le même adaptateur d’identifiant que pour le cadrage. Les trois journaux se terminant par `-red.log` proviennent de la première exécution, avant l’implémentation.
