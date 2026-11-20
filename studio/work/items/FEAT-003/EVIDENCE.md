# Pièces de cadrage

- [Sources et observation de la liaison réelle](RESEARCH.md). La consultation a utilisé la commande centrale etat.
- [Maquettes de la fiche Site](evidence/maquettes.html) et [vérifications du prototype](VISUAL-REVIEW.md). Les exemples visuels sont fictifs.
- [Avis indépendant](REVIEW.md) et [registre des empreintes](task.json). La phase planning et l’empreinte du contrat se vérifient depuis la racine avec les commandes suivantes.

```bash
python3 -B workflow-ai/scripts/workflow.py check --id FEAT-003 --phase planning
python3 -B workflow-ai/scripts/workflow.py fingerprint --id FEAT-003
python3 -B workflow-ai/scripts/validate_workspace.py
```
