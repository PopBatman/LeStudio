# Pièces du cadrage
Les pièces sous evidence/ portent sur le prototype autonome. Le registre task.json en conserve les empreintes SHA-256. Le fichier [VISUAL-REVIEW.md](VISUAL-REVIEW.md) identifie la décision à recueillir. Les observations de l’exécutant de recette sont conservées dans [REVIEW.md](REVIEW.md).

Le validateur v1 réserve sa syntaxe CLI aux identifiants parents. Pour rejouer le contrôle de ce sous-lot depuis la racine, utiliser la même procédure que pour les sous-lots de FEAT-003. Le format accepté est limité à l’identifiant de ce dossier pendant ce processus.

```sh
python3 -B - <<'PY'
import re
import sys
from pathlib import Path
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
lot = 'UI-003-01'
workflow.TASK_ID = re.compile(re.escape(lot))
print(workflow.check_task(Path('studio'), lot, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), lot))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Responsabilités
- /root/u301ux a la charge du prototype de conception.
- /root/u301design documente les fondations graphiques, les commandes et le support de validation.
- /root/u301qa examine la version du prototype dans le navigateur indépendamment de son auteur.

## Consultation des pièces
- [Prototype à télécharger](evidence/prototype.html) et à ouvrir localement. La démonstration conserve les modifications en mémoire pendant la session de la page. Un rechargement réinitialise les données fictives.
- [Création vierge sur mobile](evidence/parcours-vierge-mobile.png), [modèle sur ordinateur](evidence/parcours-modele-bureau.png) et [brouillon Figma sur tablette](evidence/parcours-figma-tablette.png).
- [Résultats dans Chromium](evidence/qualification-prototype.json) avec l’empreinte du HTML, les parcours au clavier, les révisions simulées, les messages d’incident et le contrôle du réseau.

## Clôture du prototype
La [recette rejouée](evidence/recette-cloture.json) et les captures de clôture enregistrées dans task.json concernent le HTML autonome exécuté dans Chromium. La [revue indépendante](evidence/revue-cloture.md) et la [décision de l’utilisateur](VISUAL-REVIEW.md) précisent la portée de la validation.
