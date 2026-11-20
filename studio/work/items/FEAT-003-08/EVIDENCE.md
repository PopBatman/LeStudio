# Preuves de cadrage

| Pièce | Ce qui a été vérifié |
|---|---|
| [Essai de composition V4](evidence/essai-composition.json) | Services existants, périmètre du dépôt, UUID remappés, conservation de la racine et de l’historique. Le résolveur utilise un document fictif. |
| [Suites existantes](evidence/socle.log) | 28 réussites sur SQLite, cinq tests réservés à PostgreSQL. L’adaptateur Figma reste à développer. |
| [Prototype interactif](evidence/maquettes.html) · [Examen Chromium](evidence/examen-maquettes.json) | Parcours de décision, saisie au clavier, comparaison devenue périmée, refus et ajout de pages simulés sur données fictives. |
| [Captures et limites de la revue visuelle](VISUAL-REVIEW.md) · [Revue indépendante](REVIEW.md) | États bureau/mobile, distinctions entre remise, version fournisseur et révision locale, points à éprouver pendant le développement. |

Le registre conserve l’identifiant métier FEAT-003-08 et le type local feature imposé par ce préfixe. Le type Connecteur de la carte Notion est matérialisé par [son contrat](CONNECTOR-SPEC.md) et le parcours Connecteur du Workflow AI. Pour contrôler ce sous-lot avec le validateur v1 depuis la racine, limiter le format d’identifiant à ce seul dossier pour le processus courant.

```sh
python3 -B - <<'PY'
from pathlib import Path
import re, sys
sys.path.insert(0, 'workflow-ai/scripts')
import workflow
lot = 'FEAT-003-08'
workflow.TASK_ID = re.compile(re.escape(lot))
print(workflow.check_task(Path('studio'), lot, 'planning'))
print(workflow.contract_fingerprint(Path('studio'), lot))
PY
python3 -B workflow-ai/scripts/validate_workspace.py
```

## Réalisation locale avec fournisseur simulé

- Une API HTTPS de recette sur un réseau Docker interne a fourni l’inventaire et les nœuds d’un fichier fictif. Le vrai client HTTP et le profil par site ont été utilisés dans Studio. Première création en R1, confirmation répétée, édition dans l’atelier en R2 et ajout d’une page en R3 avec conservation de la page existante. [Résultats de bout en bout](evidence/import-https-simule.json)
- Chromium a parcouru la remise, le choix d’une frame, la correction d’un titre en texte et de sa couleur, le rejet d’un élément inconnu, la sélection mobile seule et l’ouverture du résultat dans l’atelier. [Relevé navigateur](evidence/realisation-navigateur.json) · [Correspondance](evidence/realisation-correspondance.png) · [Confirmation mobile](evidence/realisation-confirmation-mobile.png)
- L’image Studio a passé les 211 tests sur PostgreSQL. Sur SQLite, 197 réussites et 14 cas réservés à PostgreSQL. Le connecteur couvre notamment le retrait d’accès, la version obsolète, le quota, la portée du nœud, les délais et les réponses incomplètes. Les courses de confirmation, d’effacement et de retrait du mandat ont été exercées sur PostgreSQL. [Suite PostgreSQL](evidence/tests-postgresql.log) · [Suite SQLite](evidence/tests-sqlite.log)
- Le reviewer indépendant a restauré une sauvegarde de recette puis vérifié le retrait du profil, l’effacement, la purge et la conservation de la révision canonique acceptée. [Revue indépendante](REVIEW.md)
- L’actualisation du poste porte sur Studio local. Les révisions et la liaison existantes ont été comparées avant/après. Le moteur Wagtail Tennis AI a conservé son processus. [Contrôle du poste](evidence/poste-local.json)

Le mandat a été précisé par « pour le moment tu simules ». Les vérifications qualifient l’intégration locale dans ce périmètre. La disponibilité, les permissions et les quotas d’un véritable fichier restent à observer avant exploitation.
