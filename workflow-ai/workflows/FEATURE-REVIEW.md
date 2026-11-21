# Revue

## Préparer

Fournir au reviewer le besoin, la spécification, les décisions, la tasklist, le diff et les preuves correspondant à la révision examinée. Indiquer les contrôles non exécutés et les risques connus. Lorsque le TDD s’applique, joindre le commit RED, la révision GREEN et les preuves des vérifications après refactor éventuel. Inclure les résultats CI applicables et les décisions relatives aux changements de critères ou de tests de référence.

## Examiner

| Domaine | Questions |
|---|---|
| Produit | Le résultat répond-il aux critères retenus ? |
| Architecture | Les responsabilités et contrats sont-ils respectés ? |
| Données et droits | Les invariants, permissions et migrations sont-ils corrects ? |
| Connecteurs | Les erreurs, doublons et résultats incertains sont-ils traités ? |
| UX/UI | Le parcours, les états et les interactions sont-ils cohérents ? |
| Preuves | Les vérifications portent-elles sur la révision examinée ? Le RED échoue-t-il pour le motif attendu, le GREEN couvre-t-il le même critère et les modifications des tests de référence respectent-elles la [politique de tests](../governance/TESTING-POLICY.md#tests-de-référence) ? |

Classer les constats par gravité et relier chaque correction à sa vérification. Une suggestion facultative ne devient pas automatiquement un blocage.

## Indépendance

Pour une revue indépendante, utiliser une exécution distincte de l’auteur, lancée réellement par le runtime ou effectuée par un reviewer humain. Le rapport identifie le reviewer, son identifiant d’exécution s’il est fourni par le runtime, ainsi que la révision et le périmètre examinés. L’auteur qui relit son travail le signale comme auto-revue.

Si l’indépendance requise n’est pas disponible, conserver la revue ouverte ou obtenir une revue humaine. Ne pas inventer un second rôle pour satisfaire le contrôle.

Utiliser [REVIEW.md](../templates/REVIEW.md). Toute livraison suit sa [procédure dédiée](FEATURE-RELEASE.md).

## Vérification d'indépendance

Le reviewer déclare l'identité et l'identifiant du run, le fournisseur/modèle utilisé, la révision examinée, ses éventuelles contributions aux spécifications, au code, aux tests et aux preuves, et les liens vers les runs producteurs. La revue indépendante requise ne peut être satisfaite par une personne ou exécution qui a produit les changements ou les preuves qu'elle valide. Si le reviewer a contribué à une partie du travail, cette partie exige une autre revue distincte. Une nouvelle session du même modèle réduit la continuité de contexte, sans garantir une diversité de modèles ni l'absence d'erreurs communes.

Le système de vérification doit corroborer les identifiants et traces lorsque le runtime le permet. Un formulaire rempli et une déclaration d'indépendance ne prouvent pas à eux seuls l'absence de contribution. En cas de doute substantiel, QG-11 reste ouvert.
