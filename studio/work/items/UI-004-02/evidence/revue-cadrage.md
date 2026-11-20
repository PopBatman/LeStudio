# UI-004-02 — Revue indépendante du cadrage

Date UTC : 2026-11-20T17:41:28.173279+00:00.
Exécutant réel : /root/t02_revue. Auteur du cadrage : /root. Inspection amont : /root/t02_existant.
Mandat : revue documentaire uniquement ; écriture limitée à cette pièce, aucun test métier, aucune écriture Notion ou donnée applicative.

## Avis

**Favorable pour le cadrage PLANNED. Aucun défaut bloquant ou correction de fond demandé.**

Le dossier représente correctement l’objectif et AC1–AC4 de la carte Notion, sans les déclarer réalisés. Il distingue les décisions humaines de direction produit des propositions techniques et du choix frontend arrêté par l’audit T01. L’autorisation du présent travail reste limitée à plan/review/publish_docs dans le dossier T02 ; aucune autorisation d’implémentation ou de release ajoutée.

## Contrats et frontières examinés

- Geste cible/voisins validé à son état final, distinct de la transaction de lot : l’écart constaté dans builder_batch.py est pris en charge, y compris les enfants affectés par un réglage de parent et les formats cachés.
- Déplacement horizontal, conversion de parent et boîte, contenu long et ratio d’image sont traduits en essais observables. Le tri vertical et la grille universelle à douze colonnes ne sont pas présentés comme réponse produit acquise.
- Le candidat de version 5 demeure conditionnel aux nouvelles sémantiques ; les lecteurs 1–4 et révisions immuables restent conservés, conversion explicite sans mise à jour forcée du catalogue ou des références.
- L’écart JS/serveur sur block_place avec parent/before est réel dans les sources lues et explicitement planifié. La limite des collisions libres et le mélange flux/libre sont signalés.
- T02 possède le modèle et sa démonstration ciblée sur rendu moteur ; T03 conserve le parcours réel Tennis AI, ses données titre/image manquantes et l’historique/autosave minimaux. Le connecteur Figma réel et le retrait physique V1/V2 ne sont pas déclarés livrés.
- Le contrôle complémentaire s’adapte seulement à l’identité préexistante UI-004-02/type Architecture dans un module en mémoire. Il réutilise le validateur documentaire, garde ui_required=false et ne lance pas la réalisation. L’échec attendu du CLI standard est conservé et n’est pas déguisé en PASS standard.

## Preuves vérifiées

Contrat Workflow initial : 011c8ccfc0e5d5702ba311bceb145fd7e90ea18ca4f241d8ae7c3b3601122b6e. Après les seules retouches de suivi examinées ci-dessous, contrat courant : a799ac6eeb5564308b5bf723a6e8b63fe0110a48f95b29c84db18d400638d4ea.
Lecture de controles.json : contrôle standard en échec sur l’identifiant suffixé, complémentaire réussi ; aucune réussite métier ou navigateur annoncée.
Vérification indépendante par hashlib : les 24 entrées du manifeste des sources et les 9 pièces du manifeste de contrat correspondent aux fichiers présents au moment de la revue. Les 11 instantanés Notion incluent carte, parent, T01, règle de relecture et acquis applicables.
Les tests de modèle, du renderer et de concurrence restent planifiés, sans exécution dans cette revue.

## Limites de cet avis

L’avis concerne la suffisance et la cohérence du cadrage, pas la validité d’un schéma final ni la réussite des gestes futurs. Les champs exacts, la nécessité du libre borné et la version finale doivent être arrêtés après les essais prévus ; ils ne sont pas encore une API acceptée. La restitution finale de la carte/pièce Notion et l’indexation de cette revue dans task.json sont suivies par l’auteur ; leur exécution n’est pas vérifiée par cette revue. Toute modification de fond du contrat doit être soumise à une nouvelle lecture.

## Actualisation après clôture documentaire

Seconde lecture par /root/t02_revue le 2026-11-20T17:42:52.348039+00:00. Les modifications de TASKLIST.md, RESEARCH.md, EVIDENCE.md et REVIEW.md concernent uniquement le suivi de revue, les identités et la comparaison de fraîcheur. Aucun scénario, proposition technique, mandat ou partage T02/T03 n’est altéré. Le contrôle complémentaire relancé annonce le contrat courant ci-dessus ; les neuf empreintes du manifeste courant sont vérifiées.

La comparaison de fraîcheur a aussi été vérifiée indépendamment par hachage : les 213 sources du manifeste T01 correspondent au workspace courant. Aucune image Docker ni tête de brouillon réinterrogée.

**Avis favorable maintenu, sans réserve de fond.** Les empreintes ci-dessous sont celles des pièces finales lues, remplaçant les empreintes initiales de cette table. Aucune réussite produit déduite des retouches de suivi.

## Empreintes des pièces lues

| Pièce | SHA-256 |
|---|---|
| SPEC.md | 06d2bc599523fecf78c3fe7614ca44071264d710545d08d8fb24fcf3349e2775 |
| TASKLIST.md | b6bd646a13d3402ebb59a71729b2af7c80077f963f02ea21ce11afbf2069a8ff |
| ARCHITECTURE.md | 7ea57286dc96125dcbf432349ad413c877ad04494f1f4d4242af200cb423c5b4 |
| SECURITY.md | 0a243110ec867b105b55a83f6acd92924d203bd13749949c2be8ce71305e8cdc |
| CONTRAT-PROPOSE.md | 4dd193e93e5a68eb7dcc8f872d81e5fdf84216c0bc6da03fb25d1dab81ad1788 |
| VISUAL-REVIEW.md | ba1d5fb04fa7d8f698cd07ec7b4d8bc0a94726b306ba7ad0b3bde65f8ec37ab9 |
| RESEARCH.md | 54f78afd548d77a5629764f3d79b8c2d67f3e0acc6b278893b5ab544b47248d6 |
| REPORT.md | 5917701856d7181f527141839fdad4dfa25216af3554087007bf558d0a811e7e |
| EVIDENCE.md | 2a4a9db301ceaa99ff2207005466219b2559c781098265f790d18cc0d40208f3 |
| task.json | d365310632a5162363fcfba63587ecd9d8fd42854df10d507af8f4258fd03bc0 |
| evidence/check-planning.py | 913464fa1d7dca4d539328f4e86ece5161f2557f6ac78eeb335ef4e9fd68da0c |
| evidence/controles.json | e495ad18014ec97535c4027cc44d04584c2f7c9eb77a998e7cd2f87cd9193323 |
| evidence/manifest-contrat.json | aaa28d22b84a6fb83c29857ea928e8ddaf43d1b3751a47d2f4aaff64c99adc95 |
| evidence/manifest-sources.json | 6cd5ab3ad8550bca8021acec29d8f6fed1fa49a88d0fcd88dc945c6e362566fc |
| evidence/sources-notion.json | 277955a36535b82377ffbba6c082305e1eb3ae483458159e4331477cfc2921ac |
| REVIEW.md | 34c20e9cabef901718e8a72f01cfff22f1b60b4288197398f68edfd3c62a6b71 |
| evidence/comparaison-sources-t01.json | 3f3e16c5bc39aedd11c39da41b572c1015d937f4372139502b1e09468aa4e642 |
