# Revue du travail

<!-- WORKFLOW-AI:TODO -->

| Champ | À renseigner |
|---|---|
| Travail et révision | Entrées réellement examinées |
| Reviewer | Identité / identifiant d’exécution observé |
| Indépendance | Distinct de l’auteur : oui/non et contexte |
| Périmètre | Fichiers, contrats et preuves examinés |
| Vérifications | Commandes exécutées et résultats |
| Limites | Non examiné / non exécuté |
| Conclusion | Favorable, corrections nécessaires ou bloquée |

| ID | Constat | Gravité | Référence | Correction / décision | Vérification |
|---|---|---|---|---|---|
| À compléter | À compléter | À compléter | À compléter | À compléter | À compléter |

Une auto-revue est nommée comme telle. Une conclusion favorable ne donne pas de permission de livraison.

Pour les contrôles locaux, la preuve de revue inclut les empreintes des entrées et du contrat concerné. L’authenticité du reviewer reste à établir par le runtime ou le système de revue utilisé.

## Provenance et séparation de la revue

| Information | Valeur à renseigner |
|---|---|
| Identifiant du run reviewer | Référence technique observable |
| Fournisseur / modèle | Modèle utilisé et limites de diversité par rapport aux contributeurs |
| Runs contributeurs | Identifiants auteur code, QA tests et autres auteurs des preuves |
| Contributions du reviewer | Fichiers/tests/preuves auxquels le reviewer a contribué, ou aucune connue |
| Révision examinée | SHA exact et critères/spec/version |
| Indépendance par zone | Zones examinées sans contribution du reviewer ; éventuels contrôles restant ouverts |
| Vérification de provenance | Source des identifiants, limites de corroboration |

Ne pas considérer une nouvelle session comme indépendante des fichiers ou preuves auxquels le même exécutant a contribué ; obtenir une revue distincte lorsque QG-11 l'exige.
