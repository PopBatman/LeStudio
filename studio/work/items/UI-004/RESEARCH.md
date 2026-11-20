# Recherche et rapprochement UI-004

Cadrage v1 · 20 novembre 2026. Lecture initiale pour le parent ; ne clôture pas l’audit complet T01. [Instantané des sources Notion](evidence/sources-notion.json).

## Sources et portée

| Source | Fait utile | Limite |
|---|---|---|
| Carte UI-004, vision, roadmap, quatorze sous-lots, règle « 03 », guide de prise en charge | Direction adoptée, 21 tâches, responsabilités et dépendances explicites après relecture | Statuts DRAFT ne prouvent aucun comportement réalisé |
| FEAT-003/01/03 et FEAT-004 dans Notion | Brouillons, catalogue interne et aperçu sont des acquis documentés | Anciennes mesures de tests ne sont pas rejouées ici |
| Code composition, frontend, moteur et tests associés | Matrice ci-dessous ; contribution indépendante lecture seule `/root/audit_existant` | Lecture statique, pas de recette des nouveaux gestes |
| UI-003-05/REPORT et anciens dossiers V1/V2 | Bascule locale historique, coexistence et preuves conservées | Les cartes ont été supprimées dans Notion ; code encore présent, retrait physique obligatoire dans T21 |
| Prototype joint à la vision, copie exacte locale | Bibliothèque à gauche, déplacement spatial, resize, texte/contextuel, autosave simulé | Grille/pas/délai ne constituent pas le modèle final |
| [Inspection Chromium du prototype](evidence/inspection-reference.json) | Ouverture en 1440/390, dix éléments, deux sections, aucune erreur JS observée ; images examinées | Aucun geste intégré ni test du produit ; réseau bloqué |
| Lecture locale Docker et métadonnées Tennis AI | Studio démarré, image web f7e13c3a559f ; Tennis AI R18 schéma 4, Accueil deux sections, A propos vide | Ne démontre pas le raccordement/rendu actuel ; aucune écriture ni sauvegarde effectuée |

L’espace n’a pas de dépôt Git exploitable à sa racine ni dans `studio/`. Un manifeste SHA-256 identifie donc les fichiers examinés. Ne pas inventer un commit.

## Matrice : réutiliser, adapter, ajouter

| Capacité | Fichier / fonction observé | Écart vers UI-004 et responsable |
|---|---|---|
| Canonique et révisions | `validation.py` : schémas 1–4, UUID, profondeur 12, 2 000 nœuds/1 Mio ; `services.py` tête verrouillée | Réutiliser ; T02 éprouve modèle/versionnement, T19/T21 compatibilité |
| Disposition/dimensions | `placement.py::effective_layout/effective_placement/validate_placement/patch_format` | Réutiliser flux/libre, pourcentages/px et héritage ; T02 qualifie voisins, limites et retour à la ligne |
| Rendu réel | `engine/reference/preview.py::Composition`, fonctions placement/CSS, templates preview | Réutiliser, schéma maximal 4 ; une évolution doit atteindre aussi le moteur |
| Sélection sécurisée | `builder_views.py::document`, `builder.js`, `builder-frame.js` | Réutiliser iframe/CSP/port et rectangles UUID ; T03 prolonge jusqu’au travail immédiat |
| Surface d’édition | `builder-edit.js::renderPage`, `builder-edit.css` | Cartes locales distinctes, images visuellement limitées à 220 px ; canvas Wagtail masqué en édition. Écart majeur T01/T03 |
| Bibliothèque | `builder-edit.js::catalog`, `builder_views.py::render_shell`, `catalogue.py` | Services/définitions conservés ; bibliothèque permanente dans la projection, palette limitée dans Wagtail ; T04/T10 |
| Insertion dans rendu | `builder-drop.js`, `builder-frame.js::dropTarget` | Ciblage réel puis édition locale ; à prolonger pour toute bibliothèque et zones vides |
| Déplacement bloc | `builder-edit.js::startPlacement/commitDrop/dropAt`, `BuilderWorkingPage::drop/apply` | Transfert parent/entre sections réel dans modèle ; choix avant/après selon Y. Translation X/Y par geste à ajouter T04 |
| Sections | `editor.py::_FIELDS` et modèle JS : section_move | Commande existante, destination par sélecteur ; glissement direct à adapter T04 |
| Resize | `builder-edit.js::settings` produit block_place | Dimensions numériques déjà persistables ; poignées/guides manquent T05. Pas de token de taille typographique actuellement |
| Texte/menu | `editItem/entryForm/settings`, `editorial.py` | Formulaires dans carte existants ; texte sur place dans rendu et menu court à ajouter T06 ; préserver Wagtail avancé |
| Undo/redo | `builder-edit-model.js::BuilderWorkingPage`, curseur/replay, 128 gestes | Réutiliser ; mémoire seulement, historique réinitialisé après sauvegarde. T08 définit continuité avec autosave |
| Sauvegarde | `builder_batch.py::save_batch`, `models.py::BuilderSave` | Atomicité, validation, mapping et reçu déjà présents ; autosave/ordonnanceur/acquittement sans reload à ajouter T03/T08 |
| Réessai/conflit | `_fingerprint`, `services._current_head`, `builder-edit.js::save/conflict` | Même clé/requête, refus base périmée ; conservation en mémoire. T09 qualifie interruption durable et concurrence |
| Reprise | `beforeunload`, online/offline, HEAD des droits dans builder-edit JS | Aucun journal durable observé ; T09 choisit stockage/portée/rétention/purge, sans promesse hors ligne universelle |
| Responsive | `placement.py`, `canvas_format.py`, modèle JS et renderer | base/tablet/mobile, clear héritage ; seuils 768/1024, largeurs libres 320–1920 ; à qualifier avec gestes et textes longs T07 |
| Superposition | `builder_batch._collisions` | Rectangles entre frères libres, intention/z explicites ; pas un moteur complet de guides ou débordement typographique |
| Droits | `services._writing_site`, `builder_views.save`, CSRF Django | Réutiliser sur tous points d’entrée, réessai compris ; frontend n’accorde aucun droit |
| Pages/imports | `navigation.py`, `builder.html`, `depots/imports.py` | Document multipage et reprise import présents ; navigation avec gestes non acquittés à qualifier T11 ; source réelle FEAT-006 |

Chemins abrégés ci-dessus : Python sous `studio/composition/`, JavaScript/CSS sous `studio/static/ui/`, templates sous `studio/templates/composition/`.

## Scénarios de référence proposés

- **R1 — Accueil Tennis AI actuel** : deux sections observées en R18, titre et image à confirmer/choisir en T01. Déplacement horizontal et transfert entre sections, resize de boîte, texte plus long, undo/redo, autosave, réouverture et aperçu Wagtail identique.
- **R2 — Page vide puis contenu long** : A propos est vide dans l’état observé. Déposer section/conteneur, titre, image et texte ; éprouver zones vides, imbrication et menu. Toute préparation de données se fera dans le mandat de lancement.
- **R3 — Page dense de recette** : copies de composants internes, imbrication autorisée, médias et contenus longs fictifs ; T18 définit volume/appareil/budget dès T03, sans inventer de mesure.
- Pour chaque scénario : bureau/tablette/mobile/intermédiaire ; clavier/tactile, ordre de lecture, capture perdue et droits. Les trois origines sont qualifiées au niveau complet en T19, avec Figma réel dans FEAT-006.

## Recommandation et inconnues

Réemploi du backend, des UUID, du catalogue et du pont. Proposition JS modulaire pour éprouver J1, React/TypeScript limité possible si T01 justifie son coût. Écart structurant : rendu immédiat de travail distinct du rendu Wagtail. T02/T03 doivent choisir et prouver sa fidélité ; le prototype ne l’apporte pas.

Décisions encore à produire : organisation frontend en T01 ; flux/grille/libre et migration éventuelle en T02 ; protocole de travail/sélection en T03 ; historique/autosave/reprise en T08/T09 ; appareils/budgets dès T03 puis qualification T18. Ces travaux à venir ne bloquent pas la rédaction du plan parent.

Sources techniques primaires consultées le 20 novembre 2026 : [React, intégration dans l’existant](https://react.dev/learn/add-react-to-an-existing-project), [W3C Pointer Events](https://www.w3.org/TR/pointerevents3/), [W3C APG Menu Button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/). Elles éclairent les options d’intégration, de capture/interruption et de focus/menu ; elles ne prouvent ni un choix approuvé ni une performance du produit.

## Évolution Notion pendant le cadrage

La relecture indépendante a détecté la modification de la carte, de la vision et de la roadmap vers 16:56 UTC le 20 novembre 2026. [Versions actualisées](evidence/sources-notion-actualisees.json) : ajout de UI-004-14/T21, 14 sous-lots du parent et 21 tâches au total. Séquence T19 → T21 → T20 ; inventaire des consommateurs dès T01, suppression physique du code et des artefacts exclusifs, tests/revue sur le candidat nettoyé. Le premier instantané reste historique. Les services partagés, migrations utiles et preuves passées sont conservés avec usage justifié ; aucun ancien builder dormant dans le code courant.
