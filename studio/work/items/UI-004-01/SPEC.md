# UI-004-01 · T01 — Audit ciblé et référence produit

20 novembre 2026. Mandat utilisateur : « Lance UI-004-01 — T01 · Audit ciblé et référence produit conformément au Notion et au Workflow AI. » [Carte](https://app.notion.com/p/41e49e23bbdb81a2b7e5e3f522012be7). Parent [UI-004](../UI-004/SPEC.md), plan courant 21 tâches dont retrait physique T21.

## Résultat à livrer et limites

Produire l’audit complet du périmètre de composition, une matrice des acquis/écarts et consommateurs, un inventaire de retrait V1/V2, le contrat UX de référence, une décision technique frontend motivée et les scénarios/pages du premier parcours T03. Présenter installé/cible sur une même page identifiable, avec captures et comparaison. Les constats distinguent observation navigateur, déduction du code et hypothèse à éprouver.

L’acteur est l’opérateur existant habilité à gérer Tennis AI. Entrées : code local, services installés, révision enregistrée, catalogue, prototype Notion adopté et contraintes du parent. Sorties : documents, inventaires, références et preuves du présent lot. T01 ne réalise ni nouvel éditeur, ni nouveau schéma, ni suppression V1/V2, ni application au site ; les corrections restent rattachées une seule fois aux tâches propriétaires.

## Acceptation

| Critère Notion | Livrable et preuve |
|---|---|
| AC1 — Capacités, fichiers/services et consommateurs ; réutiliser/adapter/ajouter/supprimer ; retrait V1/V2 tracé | AUDIT.md, inventaire T21 avec usages réellement partagés, recherches de références et empreintes |
| AC2 — Insertion, déplacement interne/entre sections, sections, resize, édition, réglages et undo | REFERENCE-PRODUIT.md : contrat des gestes, erreurs/annulation, clavier/tactile, états et données de référence |
| AC3 — Décision frontend, périmètre, migration et Wagtail | DECISION-FRONTEND.md : décision technique de l’auteur d’audit, options/coûts/conséquences ; aucune approbation humaine inventée |
| AC4 — Pages/scénarios pour placement, contenu long et mobile | Référence Tennis AI/page/révision/UUID identifiée ; même contenu dans comparaison installé/cible, scénarios vide/dense/long/mobile et périmètre exact T03 |

## Couverture et vérification

Auditer accès/site → composition/commandes/révisions → bibliothèque/édition → sélection/rendu → sauvegarde/conflits → navigation et imports partagés → build/routes/configuration. Le catalogue et les références restent bornés au site. Les refus, droits et limites sont lus et vérifiés au niveau annoncé ; aucune collecte de secret ni journal de contenu privé.

Réemployer la suite ciblée existante sur une base de test isolée pour les contrats de sauvegarde/permissions/renderer, si disponible. Vérifier le navigateur réel sans modifier le brouillon Tennis AI : ouvrir, sélectionner, formats, projection locale et annulation non sauvegardée. L’aperçu privé peut créer un reçu temporaire mais ne publie pas. Les performances et l’accessibilité avec lecteur d’écran restent à T18/UI-002 ; la référence simulée ne prouve pas le futur raccordement.

## Clôture

Audit remis, chaque AC relié à des preuves observées, limites et décisions de T02/T03 identifiées, revue indépendante effectuée, carte et parent actualisés si le jalon avance. Un audit achevé ne rend pas le nouvel éditeur disponible. Aucune nouvelle autorisation n’est requise pour préparer et vérifier ces livrables dans le mandat présent.

