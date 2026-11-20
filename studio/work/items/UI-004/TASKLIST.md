# Plan du programme UI-004

Version 1 · 20 novembre 2026 · [Spécification](SPEC.md). Repères et dépendances repris des cartes Notion lues. Chaque sous-lot conserve son cadrage, son mandat et ses preuves. Aucun exécutant futur ni délai ferme attribué.

## Cadrage présent

- [x] Lire parent, quatorze cartes, vision, roadmap, règle de relecture et socles.
- [x] Examiner code et preuves historiques ; contribution lecture seule `/root/audit_existant`.
- [x] Écrire spécification, frontières, risques, tasklist et référence visuelle.
- [x] Revue indépendante et correction des écarts ; voir REVIEW.md.
Le contrôle documentaire et la publication de la synthèse sont tracés dans les preuves et la carte existante.

## Réalisation à préparer

| Repère / carte | Résultat / critères parent | Dépend de (livraison) | Zone | Vérification de passage | Exécutant / état |
|---|---|---|---|---|---|
| T01 · UI-004-01 | Audit, UX, décision frontend ; AC-J1 | FEAT-003-01, FEAT-003-03, FEAT-004 | Composition, builder JS/templates, moteur, dossier T01 | Comparaison installé/cible sur même page, texte long/mobile ; choix frontend motivé, périmètre T03 et inventaire V1/V2 supprimer/remplacer/conserver avec consommateurs | Non attribué · à cadrer ; lecture initiale disponible |
| T02 · UI-004-02 | Modèle durable et commandes ; AC-J1/G/R | T01 | Validation, placement, editor, batch, schéma moteur/import | Flux/grille/libre borné, boîte titre/image, voisins, dépôts interdits, aller-retour et compatibilité 1–4 | Non attribué · à cadrer |
| T03 · UI-004-03 | Première tranche réelle, historique et autosave minimaux ; AC-J1/S | T02, FEAT-004 | Pont/frame, rendu de travail, sauvegarde, moteur | J1 Tennis AI réel, réouverture, même révision Wagtail, droits/non-application ; début mesures T18 | Non attribué · à cadrer |
| T04 · UI-004-04 | Dépôt et déplacement direct composants/sections ; AC-G | T03 | Gestes et commandes structure/placement | Vides, scroll, imbrication, voisins, Échap/capture perdue, alternative clavier | Non attribué · à cadrer |
| T05 · UI-004-05 | Poignées et guides ; AC-G/R | T04 | Dimensions UI/modèle/renderer | Taille affichée/sauvegardée/rendue identique, ratio, texte long, annulation et réouverture | Non attribué · à cadrer |
| T06 · UI-004-06 | Texte sur place et menu ; AC-G | T03, T04 | Édition simple, menus, lien Wagtail avancé | Double-clic/sélection, média/lien, copie/suppression/undo, clavier/tactile/focus | Non attribué · à cadrer |
| T07 · UI-004-07 | Formats et héritage ; AC-R | T04, T05, T06 | Disposition, responsive, ordre et moteur | Mobile indépendant du bureau, retour héritage, intermédiaire, lecture/liens | Non attribué · à cadrer |
| T08 · UI-004-08 | Historique/autosave complets ; AC-S | T07 | Modèle, ordonnanceur, reçus | Undo par geste à travers autosave, acquittement exact, gestes rapides/navigation/reload | Non attribué · à cadrer |
| T09 · UI-004-09 | Reprise et conflits ; AC-S | T08 | Client/reçus, session/droits, conservation | Réponse perdue, fermeture, clé identique, concurrence, révocation ; garanties bornées | Non attribué · à cadrer |
| T10 · UI-004-10 | Catalogue/thèmes/templates ; AC-C | T07, T08 | Catalogue, médias, templates, renderers | Cinq types d’abord, copies UUID indépendantes, références privées et versions | Non attribué · à cadrer |
| T11 · UI-004-11 | Site multipage ; AC-C | T06, T07, T09, T10 | Pages/navigation/médias/partage | Accueil/contenu/contact, menus/liens, contenus avancés et navigation sans perte | Non attribué · à cadrer |
| T18 · UI-004-12 | Fluidité/accessibilité ; AC-Q | T07, T09, T14 (FEAT-006-03), UI-002 | Instrumentation/navigateur/UI-002 | Appareils/budgets dès T03 ; simple/dense, clavier, lecteur d’écran, tactile/interruption | Non attribué · à cadrer ; observations dès T03 |
| T19 · UI-004-13 | Recette/bascule ; AC-B | T11, T15 (FEAT-006-04), T17 (FEAT-005-02), T18 | Anciennes routes/documents, candidat, activation/repli | Trois origines dont Figma réel, anciens documents, publication/restauration, séance réelle et décision versionnée | Non attribué · à cadrer |
| T21 · UI-004-14 | Retrait physique V1/V2 et requalification ; AC-N | T19 | Routes/handlers, frontend/assets, flags/fallbacks, endpoints/settings/dépendances, CI/build/tests/docs exclusifs | Inventaire avant/après et usages conservés justifiés ; build propre et fichiers servis sans anciens builders ; installation/mise à niveau, anciens documents et tous parcours critiques APRÈS nettoyage ; revue du diff | Non attribué · à cadrer ; inventaire dès T01 |

URL et critères détaillés des cartes : [instantané Notion](evidence/sources-notion.json). Le parent conserve FEAT-003/FEAT-004 et inclut maintenant T21 comme condition de clôture ; T21 dépend de T19. Aucun sous-lot ne dépend du parent : pas de boucle. Les versions actualisées sont dans [sources-notion-actualisees.json](evidence/sources-notion-actualisees.json).

## Jalons et préparations indépendantes

1. **J1 — Une page réelle : T01 → T02 → T03.** Historique et autosave minimaux font partie de T03 et n’attendent pas T08. Le modèle des voisins/formats s’éprouve dès T02.
2. **J2 — Édition quotidienne fiable : T04–T11.** Mesures T18 au fil des candidats. Contrat T10 préparé après T02 ; clôture après T07/T08.
3. **J3 — Maquette réelle éditable : T12–T15, FEAT-006.** T12 préparé après T01 sur source réelle autorisée ; T13 reprend T02. Une simulation ne satisfait pas ce jalon.
4. **J4 — Pilote : T16–T21.** FEAT-005 qualifie publication/restauration ; T18/UI-002 qualifient l’usage ; **T19 → T21 → T20** : recette/compatibilité, suppression physique et non-régression sur le candidat nettoyé, puis production de cet artefact par ARCH-003 dans son mandat propre. T19 ne dépend pas de T21. UI-004 reste ouvert tant que T21 n’est pas achevé.

Les dépendances décrivent la clôture, pas l’interdiction d’une préparation indépendante. Délai d’autosave, rétention, budgets et grille ne sont pas figés par le parent.

## Lancement et preuves futures

Avant chaque lancement, rouvrir carte/références, rapprocher dépôt/écarts, écrire tasklist, contrats/risques/conception du sous-lot et vérifier le mandat. Avant READY, résoudre les choix structurants applicables et présenter les supports examinables. Les preuves historiques ne prouvent pas les nouveaux gestes.

TDD pour commandes/refus, validation, idempotence, conflit, droits et concurrence. Reprendre notamment `test_builder_batch.py`, `test_builder_canvas.py`, `test_builder_edit_web.py`, `test_builder_parity.py` et `engine/reference/test_preview.py`. Consigner RED/GREEN pour les nouveaux comportements. Pour l’UI : parcours réels, clavier/tactile, formats, captures et revue sur les mêmes sources. La documentation seule du parent ne justifie pas de rejouer la suite applicative.

