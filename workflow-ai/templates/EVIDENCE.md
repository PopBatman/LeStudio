# Registre des preuves

<!-- WORKFLOW-AI:TODO -->

| Date | Nature | Entrées / révision | Commande ou observation | Résultat | Active / historique | Artefact | Limite |
|---|---|---|---|---|---|---|---|
| À renseigner | Test, revue, capture… | À renseigner | À renseigner | PASS / FAIL / BLOCKED / NOT RUN | À renseigner | À renseigner | À renseigner |

## Enregistrement dans task.json

Les chemins d’artefacts sont relatifs au dossier de travail, sous `evidence/`. Conserver l’artefact réellement produit et son SHA-256.

| Champ | Contenu |
|---|---|
| kind | Type de preuve attendu par l’aide du CLI |
| path | Chemin relatif de l’artefact |
| sha256 | Empreinte de ses octets |
| observed_at | Horodatage ISO avec fuseau |
| revision | Révision ou référence précise observée |
| outcome | Résultat observé ; `passed` pour une preuve de réussite, `illustrative` pour une maquette |
| active | Booléen optionnel, `true` par défaut ; `false` conserve une preuve historique sans lui faire satisfaire un contrôle |
| inputs | Chemins relatifs à la racine du produit (`studio/` par défaut) et SHA-256 des fichiers vérifiés |
| contract_sha256 | Empreinte renvoyée par la commande fingerprint pour les preuves qui l’exigent |

Pour les types requis par la phase — `test`, `screenshot` si UI, et `review` en release — toutes les preuves actives doivent avoir `outcome: "passed"`, des `inputs` non vides et actuels dans le périmètre autorisé, et le `contract_sha256` courant. Une réussite ne masque pas une autre preuve active en échec ou non exécutée. Une maquette reste illustrative. Les métadonnées ne remplacent pas la provenance de l’exécution.

## Historique et remplacement d’une preuve

Conserver les RED du TDD et les anciennes révisions avec `active: false` lorsqu’ils ne représentent plus la vérification courante. Leur fichier, son SHA-256, la date, la révision et la forme des entrées restent contrôlés ; les anciennes sources ne sont pas relues pour vérifier leurs empreintes. Ces preuves ne satisfont aucun contrôle de phase.

Consigner la raison du passage à l’historique et la preuve qui remplace l’ancienne. Conserver son résultat original : un RED observé ne devient pas `passed`. Un défaut encore présent ne doit pas être masqué en désactivant sa preuve.

Ne jamais inventer une commande, un résultat, un horodatage, une empreinte ou une identité. Omettre secrets et données clients inutiles.

