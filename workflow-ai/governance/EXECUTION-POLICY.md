# Politique d’exécution

## Mandat persistant

Le mandat précise projet, objectif, opérations, ressources, limites et condition de fin. Sa référence peut renvoyer à une instruction explicite de l’utilisateur ou à une décision authentifiée du système concerné. La transcription locale conserve une trace ; elle ne crée pas cette autorité.

| Situation | Conduite |
|---|---|
| Recherche, rédaction ou préparation demandée | Réaliser et vérifier les livrables dans ce périmètre |
| Implémentation autorisée d’un périmètre défini | Préparer critères et tasklist, puis développer et vérifier |
| Test, correction ou sous-tâche nécessaire au même lot | Continuer sans confirmation répétée |
| Choix structurant encore ouvert | Présenter les options et conséquences ; ne pas inscrire son propre choix comme accepté |
| Nouvelle cible, coût, accès, effet destructif ou production non couverts | Préparer le résultat examinable et obtenir le mandat manquant |
| Contrôle impossible | Conserver son état ouvert et expliquer la limite observée |

## États de travail

Le parcours commun est `DRAFT → DISCOVERY → SPECIFIED → PLANNED → READY → IMPLEMENTING → VERIFIED → REVIEWED → DONE`. Il décrit le progrès du travail. L’autorisation et la livraison sont suivies séparément.

Un changement de périmètre peut rouvrir la spécification ou le plan. Les preuves touchées deviennent à réexaminer ; l’historique est conservé. Une correction interne au périmètre ne requiert pas de recommencer toutes les étapes sans raison.

## Contrôles techniques

Les instructions et registres sont coopératifs. Le CLI local ne dispose pas, par la seule lecture d’un fichier, d’une preuve d’identité ou d’autorité humaine. Consulter son aide et le statut de livraison avant de lui attribuer un contrôle.

Les permissions des outils, du système, des runners et des environnements restent la frontière technique. Un agent ne modifie pas ces protections pour faire passer une opération refusée.

En cas de refus automatique, appliquer une alternative réellement plus sûre si elle répond au besoin. Sinon, expliquer l’action rejetée et son motif, puis demander l’autorisation manquante sans contourner le contrôle.

Voir [mandat](../templates/MANDATE.md), [permissions](AGENT-PERMISSIONS.md) et [livraison](../workflows/FEATURE-RELEASE.md).

## Vérifications locales disponibles

Le CLI propose des contrôles documentaires sans mutation automatique d’état :

| Phase de check | Pièces et données attendues |
|---|---|
| planning | SPEC.md et TASKLIST.md complétés |
| implementation | Pièces de planning, ARCHITECTURE.md, SECURITY.md, périmètre autorisé non vide et référence de mandat couvrant `implement` ; si UI, VISUAL-REVIEW.md et preuve de maquette |
| verification | Contrat d’implémentation, REPORT.md et preuves actives de test réussies ; captures actives réussies si UI |
| release | Contrat de vérification, REVIEW.md, référence et déclaration d’indépendance de revue, preuves actives de revue réussies, mandat couvrant `release` |

Les modèles incomplets portent `<!-- WORKFLOW-AI:TODO -->`. Retirer ce marqueur après complétion ; sa disparition ne prouve pas à elle seule la qualité du contenu. Les empreintes lient les pièces, entrées et preuves ; elles ne certifient ni la sincérité de l’auteur ni son autorité.

Chaque type requis doit disposer d’une preuve active ; toutes ses preuves actives doivent satisfaire les conditions de la phase. `active` vaut `true` par défaut. Les preuves historiques avec `active: false` ne satisfont aucun contrôle, tout en conservant leurs vérifications d’artefact et de métadonnées.

Consulter l’aide de `scripts/workflow.py` pour `status`, `new`, `check` et `fingerprint`. Le contrat exact des preuves figure dans [EVIDENCE.md](../templates/EVIDENCE.md). Le résultat d’un check reste distinct du mandat du runtime et d’une permission de production.

