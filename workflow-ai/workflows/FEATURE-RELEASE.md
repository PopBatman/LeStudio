# Préparation et exécution d’une livraison

La livraison est distincte de l’état du travail. Un lot DONE peut être livré sous forme de fichier ou de revue sans être déployé en production.

## Préparer un résultat examinable

| Sujet | Éléments |
|---|---|
| Cible | Projet, environnement et destinataires autorisés |
| Artefact | Version, révision, empreinte et contenu |
| Compatibilité | Code, configuration, contrats et données |
| Vérifications | Résultats applicables et limites |
| Migration | Effets sur les données et procédure prévue |
| Reprise | Arrêt, restauration ou compensation selon le changement |
| Mandat | Référence couvrant la livraison et ses effets |

Construire puis qualifier l’artefact approprié. Une image candidate peut être déposée dans un registre privé pour être analysée ; cette présence ne vaut pas autorisation de production. Relier la livraison à l’artefact effectivement qualifié.

## Exécuter

Vérifier le mandat déjà disponible. Si un accord manque, présenter le résultat concret préparé et demander uniquement cet accord. Ne pas redemander une permission déjà donnée pour la même opération.

Après exécution, observer le résultat, les vérifications de mise en service et les erreurs éventuelles. Un lancement réussi ne prouve pas que la livraison s’est terminée.

Les templates GitLab et scripts ne configurent pas automatiquement les branches protégées, runners, comptes, secrets ou environnements. Les droits réels restent appliqués par ces systèmes.

Consigner le résultat dans [IMPLEMENTATION-REPORT.md](../templates/IMPLEMENTATION-REPORT.md).

