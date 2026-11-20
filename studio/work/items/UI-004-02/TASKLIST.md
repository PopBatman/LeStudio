# T02 — Tasklist ordonnée

Version 1 · [SPEC.md](SPEC.md). Cadrage mandaté uniquement ; toutes les tâches de réalisation ci-dessous restent à faire.

| ID | Résultat | Dépend de | Zones prévues | Vérification / critères | Exécutant |
|---|---|---|---|---|---|
| T02-01 | Relire carte/vision/T01, état réel et mandat ; arrêter compositions fictives, limites et références | Lancement distinct | Lot, métadonnées Studio sans réécriture | Écarts datés, tête relue ; aucun écrasement client | Agent de réalisation à désigner |
| T02-02 | Comparer flux et grille sur titre/image, tester contenu/largeur ; cas libre si superposition requise | 01 | Banc limité + renderer Wagtail | X réel, taille, deux parents ; texte cinq lignes, ratio image, 390/820/980/1200 ; AC1/2 | Auteur modèle/rendu |
| T02-03 | Arrêter unités/champs/bornes, conversions, voisins et héritage ; publier le contrat canonique | 02 | docs/DISPOSITION.md, contrat versionné | Décision étayée version 4 ou 5 ; chaque besoin représentable ou arbitrage explicite | Auteur contrat |
| T02-04 | Ajouter règles modèle et groupe de geste atomique cible/voisins par TDD | 03 | composition/validation.py, placement.py, editor.py, builder_batch.py ; tests | RED métier avant correction puis GREEN : collision transitoire, état final invalide, multi-formats, parent_layout ; AC1/3 | Auteur backend |
| T02-05 | Aligner les consommateurs et le modèle JS extrait sur la même sémantique | 03/04 | Modèle JS, engine/reference, producteurs vierge/template/Figma | Parité transfert parent/before+resize, rendu moteur, aucun schema 4 réinterprété ; AC1/2 | Auteur intégration |
| T02-06 | Qualifier conservation, migration explicite et erreurs de version | 04/05 | Fixtures 1–4, migration JSON si nécessaire, tests producteurs/renderer | Aller-retour sans changement d’UUID/version/média/menus ; historique identique ; AC4 | Auteur tests |
| T02-07 | Éprouver transport existant adapté, droits et concurrence | 04/06 | Tests batch/services/PostgreSQL | Course deux connexions, retry même clé, clé différente/base périmée, autre site, révocation, limites | Auteur backend |
| T02-08 | Démontrer les scénarios dans le banc moteur et préparer le passage T03 | 02–07 | Captures et exports fictifs, guide | AC1–4, erreurs/annulation et voisinage ; versions et mesures réelles identifiées | Auteur intégration |
| T02-09 | Revue indépendante, corrections puis contrôles ciblés, compte rendu et carte | 08 | Lot et docs de référence | Avis distinct, preuves actuelles, limites déclarées ; T03 reste non lancé | Reviewer distinct + auteur |

Les responsabilités peuvent revenir au même auteur séquentiellement ; la revue exige un autre exécutant réel. Ne pas déléguer simultanément l’écriture des mêmes fichiers ni le protocole avant son contrat.

## Cadrage accompli

- [x] Carte, parent, vision, dépendance T01, acquis FEAT-003-01/03 et aperçu FEAT-004 examinés.
- [x] Dépôt et consommateurs ciblés relus ; options/propositions distinguées des acquis.
- [x] Objectif, risques, interfaces, critères et tâches préparés.
- [x] Références de démonstration préparées dans VISUAL-REVIEW.md ; aucun changement d’interface produit par ce cadrage.
- [x] Revue indépendante favorable et contrôle complémentaire de planification réussi : résultats dans REVIEW.md et EVIDENCE.md.
- Restitution sur la carte existante : résultat suivi dans evidence/publication-notion.json.

## Réalisation non lancée

- [ ] Décision finale schéma/disposition étayée et document canonique livré.
- [ ] RED/GREEN, migration et parité JS/serveur/moteur observés.
- [ ] Démonstration AC1–AC4 observée, concurrence PostgreSQL vérifiée.
- [ ] Livraison T02 revue et prouvée ; aucun résultat produit déduit du seul cadrage.

