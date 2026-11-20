# T02 — Index des preuves de cadrage

Les pièces ci-dessous prouvent des lectures et contrôles documentaires, jamais la réalisation des gestes.

| Pièce | Portée |
|---|---|
| evidence/sources-notion.json | Instantanés des 11 pages applicables relues avant cadrage, dont carte, parent et dépendances |
| evidence/manifest-sources.json | Empreinte des sources locales et références T01 examinées ; absence de Git explicitée |
| evidence/comparaison-sources-t01.json | 213 sources du workspace identiques au manifeste T01 ; image Docker non réinterrogée |
| evidence/check-planning.py | Contrôle complémentaire borné à UI-004-02, Architecture, cadrage uniquement |
| evidence/controles.json | Commandes, date UTC, Python, codes retour, résultats standard et complémentaire, liens et empreintes |
| evidence/manifest-contrat.json | Empreinte Workflow des quatre documents de base et empreinte élargie des pièces de cadrage |
| evidence/revue-cadrage.md | Avis d’un exécutant distinct sur le dossier final, avec limites |
| evidence/publication-notion.json | Identifiants et résultat de publication de la synthèse/pièce examinable |

La collecte n’interroge pas la tête actuelle du brouillon et n’exécute pas les scénarios métier. Les captures de T01 restent des preuves historiques référencées ; aucune capture de nouveau geste n’est annoncée.

Les empreintes du registre task.json lient la revue au contrat et aux pièces examinées. PLANNED et un contrôle documentaire réussi ne remplacent pas les essais AC1–AC4. Le CLI standard reste incompatible avec l’identifiant suffixé/type Architecture ; cette limite est conservée dans controles.json.

