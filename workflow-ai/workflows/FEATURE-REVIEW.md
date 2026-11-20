# Revue

## Préparer

Fournir au reviewer le besoin, la spécification, les décisions, la tasklist, le diff et les preuves correspondant à la révision examinée. Indiquer les contrôles non exécutés et les risques connus.

## Examiner

| Domaine | Questions |
|---|---|
| Produit | Le résultat répond-il aux critères retenus ? |
| Architecture | Les responsabilités et contrats sont-ils respectés ? |
| Données et droits | Les invariants, permissions et migrations sont-ils corrects ? |
| Connecteurs | Les erreurs, doublons et résultats incertains sont-ils traités ? |
| UX/UI | Le parcours, les états et les interactions sont-ils cohérents ? |
| Preuves | Les vérifications correspondent-elles au code réellement livré ? |

Classer les constats par gravité et relier chaque correction à sa vérification. Une suggestion facultative ne devient pas automatiquement un blocage.

## Indépendance

Pour une revue indépendante, utiliser une exécution distincte de l’auteur, lancée réellement par le runtime ou effectuée par un reviewer humain. Le rapport identifie cet exécutant et le périmètre examiné. L’auteur qui relit son travail le signale comme auto-revue.

Si l’indépendance requise n’est pas disponible, conserver la revue ouverte ou obtenir une revue humaine. Ne pas inventer un second rôle pour satisfaire le contrôle.

Une revue favorable n’élargit pas le mandat et n’autorise pas un déploiement. Utiliser [REVIEW.md](../templates/REVIEW.md).

