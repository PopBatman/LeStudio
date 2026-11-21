# UI-004-02 — Dossier de cadrage v1

20 novembre 2026 · PLANNED · réalisation non lancée.

Contrat : a799ac6eeb5564308b5bf723a6e8b63fe0110a48f95b29c84db18d400638d4ea

Carte : https://app.notion.com/p/41e49e23bbdb817695efdccd260a063f

Les chemins relatifs ci-dessous désignent le dossier local studio/work/items/UI-004-02/. Les preuves détaillées sont conservées dans ce dossier.


---

## Fichier : REPORT.md

# Cadrage T02 · 20 novembre 2026

- **Version et cible** — Cadrage v1 de UI-004-02, type Architecture, contrat de disposition et gestes ; code et références Notion rapprochés. Pas de Git exploitable ; manifeste des sources dans evidence/.
- **Résultat utilisable** — [Spécification](../SPEC.md), [options de contrat](../CONTRAT-PROPOSE.md), [tasklist](../TASKLIST.md), architecture/risques, compatibilité et références de démonstration préparés. Le point principal est le geste atomique cible/voisins, distinct du lot de sauvegarde.
- **Choix proposés** — Comparer flux/grille et libre borné si nécessaire ; version 5 uniquement si les champs ou nouvelles sémantiques le justifient. Préserver la lecture 1–4 et migrer explicitement une copie. Corriger la parité parent/before du placement local lors de la réalisation.
- **Vérifications** — Lecture des consommateurs, contrôle documentaire complémentaire, liens et empreintes ; résultat et revue indépendante dans [EVIDENCE.md](../EVIDENCE.md) et [REVIEW.md](../REVIEW.md). Les contrôles partagés ne supportent pas directement cet identifiant/type ; aucune extension globale du workflow.
- **Limites et suite** — Aucun code applicatif, migration, manipulation de données, nouvel écran ou test métier exécuté. AC1–AC4 restent à démontrer au lancement T02 ; le parcours Tennis AI/historique/autosave minimal appartient à T03. Relire carte/références et mandat avant tout lancement.
- **Pilotage** — [Carte T02](https://app.notion.com/p/41e49e23bbdb817695efdccd260a063f). PLANNED décrit le cadrage achevé, sans lancement ni nouvelle approbation technique humaine.



---

## Fichier : SPEC.md

# UI-004-02 — T02 · Contrat des gestes et modèle de disposition

Version de cadrage : 1 · 20 novembre 2026 · état visé : PLANNED.

## Objectif, mandat et sources

Préparer le document canonique et les commandes permettant de déplacer et redimensionner réellement titre/image, conserver cette intention après enregistrement et la rendre avec Wagtail. La demande utilisateur « Cadre UI-004-02 — T02 · Contrat des gestes et modèle de disposition conformément au Notion et au Workflow AI » autorise ce cadrage, sa revue et sa restitution documentaire sur la carte existante. Elle ne lance pas la réalisation de T02, T03 ou une migration de données.

Carte : https://app.notion.com/p/41e49e23bbdb817695efdccd260a063f ; parent UI-004, audit T01 DONE, vision et prototype adoptés le 20 novembre. [Sources relues](../RESEARCH.md), [instantané Notion](sources-notion.json). Risque STANDARD : transformation de brouillons, erreurs de placement, contenu masqué, isolement et concurrence. Aucune nouvelle validation humaine des options techniques n’est enregistrée.

## Résultat à livrer lors de T02

Un contrat durable dans studio/docs/DISPOSITION.md, un schéma identifié, une matrice de compatibilité et des scénarios aller-retour exécutables. Un banc de rendu limité aux compositions fictives doit démontrer les choix flux/grille et examiner le libre borné si une référence exige une superposition. Il réutilise le renderer Wagtail ; un second renderer de cartes ne constitue pas la preuve.

T02 possède le modèle, la sémantique du geste atomique et leur vérification ciblée. T03 possède le raccordement de la petite surface d’édition sur Tennis AI, le titre/image et le média de démonstration, l’historique/autosave minimaux et la réouverture dans le vrai parcours. T04–T09 industrialisent les gestes, formats, historique et reprise ; FEAT-006 qualifie Figma réel ; T21 retire les anciens builders. Aucun de ces livrables n’est déclaré acquis par le présent cadrage.

## Invariants à préserver

- Studio possède brouillons/révisions et contrôle acteur/site/base ; le moteur possède le rendu et ses contenus éditoriaux. Enregistrement et aperçu ne publient pas.
- Les tableaux portent l’ordre et l’arbre porte le parent unique ; les UUID de page, section et occurrence restent stables lors d’un déplacement ou d’une migration. Une duplication ou instanciation de template crée de nouvelles occurrences avec correspondance explicite.
- Une page porte des sections ; une section porte des blocs ; seul un conteneur compatible porte des enfants. Ni cycle, ni feuille devenue parent, ni parent d’un autre site/page. Le déplacement entre pages n’est pas inclus dans J1.
- Définitions scope/key/version, provenance, références médias/contenus, menus et apparence sont conservés. Une migration du schéma ne met pas à jour le catalogue. Les ressources restent résolues dans le site.
- Base, tablet et mobile : surcharges indépendantes de base, structure/contenu partagés. Aucun ordre mobile divergent implicite. Un changement de parent est structurel et doit produire un état valide dans tous les formats.
- Un geste possède une seule intention confirmable et annulable, cible ET voisins inclus. Annulation provisoire : aucun document, historique ni reçu modifié. Undo après sauvegarde : nouvelle intention, jamais suppression d’une révision.
- Le backend valide chaque groupe de geste à son état final. Le lot autosave reste entièrement atomique ; reporter toutes les validations à sa seule fin laisserait passer des gestes individuellement invalides.
- Les limites actuelles restent le point de départ : 1 Mio JSON compact, 2 000 nœuds, profondeur 12, 128 commandes par lot. Les futures limites de groupes/opérations doivent être bornées sans multiplier ces budgets.

## Contrat proposé à éprouver

[CONTRAT-PROPOSE.md](../CONTRAT-PROPOSE.md) fixe les options de travail, unités, règles de voisins, conversion de parent, annulation et migration. Il distingue l’existant des ajouts proposés. La grille à 12 colonnes et les coordonnées du prototype ne sont pas une décision de production. La décision finale est prise et documentée après les essais T02-02/03 ; toute réduction de la liberté produit requiert un arbitrage utilisateur.

## Critères et preuve attendue

| Critère Notion | Scénario de réalisation | Preuve attendue, encore à produire |
|---|---|---|
| AC1 | Déplacer horizontalement et entre deux parents titre/image, changer leur largeur et la boîte image ; sauvegarder/recharger puis rendre | Documents avant/après/relecture, UUID et versions conservés, rendu moteur même version, largeurs mesurées |
| AC2 | Titre deux puis cinq lignes, remplacement par image d’autre ratio, 390/820/980/1200 px | Règle de hauteur/voisins explicite, aucune perte de texte, mesures et captures ; 767/768/1023/1024 aux seuils |
| AC3 | Cycle, feuille, autre page/site, dépôt hors bornes, collision non autorisée, cible disparue, Escape/capture perdue | Refus précis sans révision partielle ; empreinte et historique identiques après annulation ; geste cible/voisins undo/redo |
| AC4 | Lire fixtures versions 1, 2, 3, 4 et R18, migrer une copie explicitement si nécessaire, relire/rendre | Identités/références conservées, ancien instantané inchangé, diagnostic version future/incompatible, rapport de migration |

Aucun critère de réalisation n’est coché à ce stade. La couverture de cadrage est la définition de ces scénarios et de leur tasklist, pas leur réussite.

## Questions et conditions de décision

1. Faut-il étendre le schéma 4 ? Proposition : version 5 seulement pour les nouvelles sémantiques effectivement retenues ; mesurer si les champs actuels suffisent avant d’écrire. Décision T02-03, sans changement silencieux du sens de la version 4.
2. Le libre borné est-il nécessaire aux références retenues ? Comparer une composition côte à côte et une superposition explicitement identifiée. Si aucune maquette n’en exige, conserver la lecture legacy libre sans généraliser ce mode ; ne pas déclarer le libre final éprouvé.
3. Quel rendu immédiat ? T02 livre les règles et un cas moteur de référence ; T03 choisit/qualifie le protocole de travail en préservant le DOM de saisie, l’identité du frame et l’obsolescence des mesures. Le pont actuel ne sait pas muter ce document.
4. Lancement : relire carte, références et tête réelle. Le dossier est PLANNED ; il ne constitue pas une autorisation d’implémenter.



---

## Fichier : CONTRAT-PROPOSE.md

# T02 — Options de contrat à éprouver

Version 1 · proposition technique de /root ; aucune réalisation ni approbation humaine nouvelle.

## Représentation et compatibilité de départ

L’existant accepte les schémas 1–4 ; version 4 ajoute placement base/tablet/mobile. Layout : stack/grid, columns 1–12, gap 0–128 px. Placement flow : span, largeur optionnelle en pourcentage et hauteur optionnelle en px ; free : x/width en pourcentage du parent, y/height en px et z. Ces unités sont locales au parent, jamais des coordonnées de la fenêtre. L’héritage tablet/mobile part directement de base ; les seuils existants sont 768 et 1024 px. Les largeurs 1200/820/390 sont des références de recette et non des seuils.

La proposition conserve arbre, tableaux, définition épinglée, props typées, apparence et références. Pas de duplication du parent dans un deuxième index persistant ni de géométrie DOM enregistrée en parallèle. Toute nouvelle sémantique exige une version explicite ; le moteur annonce/refuse cette version avant de prétendre rendre.

## Comparer avant de figer le schéma

| Mode | Usage et position réelle | Taille, voisins et limites proposées |
|---|---|---|
| Flux | Ordre dans le parent, largeur et alignement contrôlés ; pas seulement monter/descendre | Hauteur texte intrinsèque ; gap du parent ; voisins repoussés par le flux. Une translation libre X/Y ne doit pas être annoncée si seul l’ordre change |
| Grille responsive | Colonnes configurées par le parent, départ de colonne explicite si nécessaire + span et ordre de lecture | Auto-placement des autres enfants selon ordre ; aucun dense qui change la lecture ; collision gérée dans le groupe. La boîte texte grandit avec son contenu |
| Libre borné, conditionnel | Groupe/parent local avec bornes et règles de superposition explicites | Le libre legacy reste lisible. Nouveau libre seulement si une référence le justifie, calques explicites, hauteur du groupe suffisante, repli par format et ordre de lecture conservé |

Candidat d’extension minimal si la grille est retenue : départ de colonne et alignement de l’occurrence (start/center/end/stretch), hauteur auto ou minimale pour les textes/conteneurs ; pas de pixel absolu global ni de placement CSS arbitraire. Définir noms, types, valeurs et bornes exacts dans DISPOSITION.md après comparaison ; ce tableau n’est pas une API acceptée. Conserver columns 1–12 comme borne technique actuelle est une option, jamais la preuve d’une grille universelle à 12.

Espacement : réutiliser gap validé du parent ; padding ou alignement nouveaux seulement s’ils sont requis par les compositions, sous forme de champs bornés. Une section occupe la largeur disponible et se réordonne ; sa position horizontale libre n’est pas proposée.

## Contenu variable et redimensionnement

Redimensionner un titre change sa boîte et le retour à la ligne ; le niveau de titre et la taille typographique restent des réglages distincts. En flux/grille, hauteur auto/minimale, texte intégral et voisins recalculés. Une réduction de hauteur qui masquerait le texte est refusée ou convertie explicitement en minimum ; ne pas conserver un height fixe avec débordement accidentel comme réponse produit.

Pour une image, choisir explicitement entre ratio intrinsèque avec hauteur automatique et boîte bornée avec ajustement contain/cover si cette capacité est livrée. Défaut proposé : ratio intrinsèque, aucune coupe silencieuse. Remplacement de média : même occurrence, nouveau ref_id autorisé, largeur préservée ; recalcul après chargement, voisins ajustés dans la même intention. Un média absent reste signalé, sans URL distante arbitraire.

En libre, un contenu qui dépasse ne doit ni être masqué ni chevaucher un voisin implicitement : agrandir le groupe et les voisins dans un geste atomique si une solution déterministe existe, sinon refuser la confirmation en proposant le retour au flux. Cette alternative doit être éprouvée ; elle ne devient pas un moteur de résolution générique.

## Dépôt et conversion de repère

Un dépôt valide fournit parent UUID, ancre before (UUID frère ou null), format et intention de position/taille. Le modèle résout l’emplacement ; les mesures DOM ne sont pas des droits. Pour une boîte libre, x = 100 × (gauche cible − gauche de la zone de contenu du parent) / largeur de cette zone ; largeur exprimée dans le même repère, y en px locaux. Définir l’arrondi et vérifier les bornes après arrondi. Recalculer après scroll, chargement image/police ou resize ; annuler une confirmation si la génération de mesures ou la cible est périmée.

Vers flux/grille : convertir vers ordre, départ/span et alignement disponibles, sans conserver des coordonnées inactives trompeuses. Vers libre : matérialiser la boîte complète du parent cible. Parent et ordre sont partagés ; calculer/revalider tous les formats, ne pas rebaser seulement celui qui est visible. Si une conversion n’est pas représentable, refuser le dépôt et garder la source ; aucune conversion silencieuse destructrice. Un changement local de mode doit respecter les règles d’héritage, et leur remise à zéro doit être testée.

## Unité atomique du geste

Candidat de protocole versionné : un groupe identifié contient les opérations bornées de structure, placement, propriétés et voisins d’une seule intention. Le lot de sauvegarde conserve key/base/page et contient des groupes ordonnés. Le schéma exact du transport est décidé avec la compatibilité des consommateurs existants ; ne pas modifier sous le même contrat une liste historique de commandes.

Traitement : contrôler acteur/site/base et structure d’enveloppe → copier l’état précédent → appliquer les opérations du groupe sans publier d’intermédiaire → valider document, permissions/références et collisions de l’ensemble affecté dans tous les formats → accepter une entrée d’historique. Répéter pour chaque groupe ; sauvegarder une seule révision/reçu pour le lot complet, ou rien. Tous les enfants affectés par parent_layout et les descendants transférés sont inclus dans la validation, pas seulement le bloc sélectionné.

Exemple conceptuel : A et B voisins se déplacent ensemble ; A vers la place actuelle de B, B vers une place libre. L’état intermédiaire A/B en collision n’est jamais validé comme un geste ; l’état final sans collision doit passer. Un deuxième groupe indépendamment invalide annule le lot entier. Une superposition voulue exige une intention et un ordre de calques explicites dans chaque format concerné.

Insertion/duplication : conserver le mapping local/canonique existant ; remapper aussi commandes en attente, sélection et historique avant une nouvelle soumission. Rejouer exactement key/payload sur résultat inconnu ; clé réutilisée avec autre contenu refusée. Une permission révoquée est vérifiée avant tout reçu retourné. La concurrence sur base périmée refuse l’écrasement.

## Prévisualisation, annulation et focus

États : repos → geste provisoire → destination valide ou refus expliqué → confirmation locale → modifié → sauvegarde en cours → acquittement de la seule version envoyée. Le rendu de travail et l’aperçu certifié d’une révision restent identifiables. Aucune requête persistante pour chaque mouvement du pointeur.

Escape, pointercancel, capture perdue ou cible retirée annulent la session provisoire et restaurent document, voisins, sélection et focus. Le geste provisoire n’entre pas dans l’historique. Une saisie texte est traitée avant une navigation/page/format ; le clic ou la sélection de texte ne commence pas un drag. Les alternatives clavier aux dépôt/taille/options produisent la même intention.

Undo/redo porte sur la cible et tous les effets induits ; après sauvegarde, undo crée un nouvel état à sauvegarder. Prévoir continuité après acquittement sans recharge, mais sa mise en œuvre UI appartient à T03/T08.

## Lecture et migration

Lire les versions 1–4 sans réécrire leurs révisions. Pour une extension version 5 : copie normalisée déterministe, UUID/ordre/props/définitions/références inchangés sauf champs explicitement migrés ; conserver les hauteurs fixes legacy et leur sens dans l’ancienne version. Convertir une hauteur fixe en minimum requiert un rapport visible et une nouvelle révision, car cela peut modifier le rendu.

Pas de migration automatique des données réelles pendant T02. Tester les fixtures 1–4, un export minimal de R18 et un schéma futur rejeté. Une définition indisponible reste consultable selon le contrat de conservation existant ; elle ne devient ni insérable ni publiable. Si une transformation n’est pas sans perte, garder le document ancien lisible, expliquer la limite et exiger une conversion explicite. Repli : lecteur/image précédente compatible pour l’ancienne version, jamais rétroconversion silencieuse d’une version 5 déjà écrite.

Les trois origines vierge/template/Figma accepté consomment ce même document. Adapter les producteurs sans nouvelle occurrence lors d’une migration ; les instanciations de template ont de nouveaux UUID. Les références Figma non représentables restent des écarts/propositions, pas du HTML/CSS exécutable.



---

## Fichier : TASKLIST.md

# T02 — Tasklist ordonnée

Version 1 · [SPEC.md](../SPEC.md). Cadrage mandaté uniquement ; toutes les tâches de réalisation ci-dessous restent à faire.

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



---

## Fichier : ARCHITECTURE.md

# T02 — Architecture du périmètre préparé

Version 1 · cadrage ; les chemins ci-dessous sont les zones de réalisation futures, pas un mandat d’écriture actuel.

| Propriétaire | Réemploi constaté | Travail prévu |
|---|---|---|
| Modèle central | composition/validation.py, placement.py, appearance_contract.py, models.py, services.py | Schéma/compatibilité, règles finales parent/format/boîte ; sauvegarde et droits existants |
| Commandes | composition/editor.py, builder_batch.py | Groupe atomique cible/voisins, contrôle final par geste et transaction de lot |
| État local | static/ui/builder-edit-model.js ; gestes canvas.js historiques | Isoler modèle utile sans dépendance DOM V1/V2, parité parent/before/placement ; aucune ancienne interface conservée comme cible |
| Rendu moteur | engine/reference/preview.py, assets/preview.css et templates/reference/preview_blocks.html | Même sémantique par version, texte/ratio/voisins, diagnostics version incompatible |
| Producteurs | composition/editor.py, assets/presentation-activite-v1.json, figma_mapping.py | Aucun producteur laissé en version 4 si le contrat requiert la version 5 ; conserver imports déjà enregistrés |
| Pont / aperçu | composition/preview.py, static/ui/builder-frame.js et pont de prévisualisation existant | T02 fixe identité/repère/génération ; protocole de mutation et surface qualifiés en T03 |
| Documentation | docs/DISPOSITION.md prévu ; docs/BROUILLONS.md et docs/COMPOSANTS-UI.md | Une référence durable et liens de contrats ; pas de copie concurrente par origine |

## Interfaces

Voir [contrat proposé](../CONTRAT-PROPOSE.md). Transport versionné, entrées bornées, acteur/site/base explicites. Réutiliser le reçu idempotent et le mapping UUID. Erreurs : document/commande/format invalide, cible incompatible, collision, ressource/composant indisponible, clé réutilisée, base périmée, moteur incompatible ou indisponible. Conserver leurs codes existants quand applicables ; nouveaux codes et statuts HTTP documentés avec les tests du transport au lancement.

Un batch atomique existant n’est pas un groupe de geste : la validation intermédiaire dans _command est l’écart principal. La parité JS/serveur doit inclure block_place avec parent/before, que le modèle local actuel ne traite pas comme le serveur. Ne pas déplacer une validation uniquement dans le navigateur.

## Réalisation bornée

T02 livre contrats, extension minimale nécessaire et démonstrateur/tests de modèle + rendu. Son lancement éventuel doit autoriser explicitement ces zones ; task.json n’autorise actuellement que work/items/UI-004-02/. Aucun nouvel écran d’édition, bundle React/TypeScript, import Figma réel, endpoint d’application ou retrait physique V1/V2 pendant ce cadrage.

Architecture frontend retenue par T01 : JavaScript natif organisé par responsabilités, servi par Django. Ce choix est technique, sans nouvelle validation humaine inventée. Extraire et qualifier les mécanismes utiles ; conserver l’inventaire T21.

## Options et décision attendue

Réutiliser version 4 si les essais représentent toute l’intention ; sinon étendre par version 5. Comparer flux/grille pour déplacement X et contenu variable, libre borné conditionnel pour superposition. Rejeter le tri vertical comme réponse intégrale à AC1 ; ne pas figer une grille universelle depuis la maquette.

Le rendu immédiat de T03 doit partager effectivement les règles du moteur. Le présent cadrage ne promet pas qu’une projection de cartes et l’aperçu sont équivalents. Les manifests/identités/version et génération de mesures doivent permettre de détecter un état périmé.

## Vérification prévue

Tests de schéma/placement/commandes, parité JS/serveur, concurrence et reçu sur PostgreSQL, fixtures historiques, adaptateurs vierge/template/Figma simulé au niveau annoncé. Renderer Wagtail réel sur compositions fictives et largeurs de référence. T03 reprend la vraie page et la chaîne complète sans publication ; T19/T21 couvrent la bascule et le retrait.



---

## Fichier : SECURITY.md

# T02 — Risques, permissions et erreurs

Version 1 · risque STANDARD, aucune donnée réelle modifiée par le cadrage.

| Risque | Contrat et preuve prévue |
|---|---|
| Écriture ou lecture d’un autre site | Contexte acteur/site et habilitation dans le service, vérifiés avant reçu/rejeu ; tests deux sites et révocation |
| Geste partiellement appliqué | Copie par groupe puis validation finale ; transaction de lot et aucune révision/reçu sur échec |
| Écrasement concurrent | Révision de base contrôlée sous verrou de site ; course PostgreSQL et reçu idempotent |
| Contenu caché / voisin perdu | Hauteur et reflow explicites ; pas de conversion/migration silencieuse ; aller-retour et texte long |
| Import ou configuration exécutables | Champs typés/bornés et catalogue interne versionné ; aucun CSS/HTML/JS libre ni URL média arbitraire |
| Surcharge ou structure cyclique | Budgets taille/nœuds/profondeur/commandes ; groupes et opérations dans budget global ; refus avant traitement coûteux |
| Pont de rendu détourné ou périmé | Réemploi nonce/MessageChannel/CSP et contexte frame/page/version ; mesures périmées invalidées ; extensions qualifiées en T03 |
| Ressource retirée | Références média/contenu résolues dans le site ; diagnostic distinct de la conservation d’un historique ; pas de réautorisation par migration |
| Version moteur divergente | Version supportée vérifiée, refus explicite ; ne jamais certifier l’état de travail comme aperçu enregistré |

Les preuves utilisent des données fictives ou les métadonnées minimales de T01 ; pas de secret, cookie, token, export complet client ni consultation de .env. Studio ne modifie pas directement les bases des moteurs, n’emploie pas SSH et ne publie pas par l’autosave.

Pas de migration de base nécessaire présumée pour un changement JSON ; examiner les besoins réels avant de générer une migration Django. Pour les brouillons, conserver les révisions anciennes et créer une nouvelle révision de conversion explicite. Repli sur version/image compatible selon schéma réellement écrit.

Le cadrage est documentaire. Les tests de sécurité ci-dessus sont planifiés ; ils n’ont pas été rejoués pendant cette mission.



---

## Fichier : VISUAL-REVIEW.md

# T02 — Références et démonstration à préparer

Version 1 · lot d’architecture, UI requise = non dans Notion. Le cadrage ne modifie aucun écran ; il ne nécessite pas de nouvelle maquette de coque ni de captures d’implémentation. Ce document fixe les observations visuelles nécessaires à la réalisation du modèle.

Références réemployées : [prototype adopté du parent](../../UI-004/evidence/prototype-adopte.html), [contrat UX T01](../../UI-004-01/REFERENCE-PRODUIT.md), [comparaison installée/cible R18](../../UI-004-01/evidence/comparaison-reference.html). Le prototype est simulé ; la cible de T01 est illustrative ; aucune de ces pièces ne prouve le nouveau modèle.

| Composition | Variantes à comparer | Observation attendue |
|---|---|---|
| C1 : titre + image dans deux sections/conteneurs | Flux puis grille, déplacement X et transfert, largeur titre 100 % puis 50 % | Même UUID, contenu/version/média ; voisins et retours à la ligne définis |
| C2 : contenu variable | Titre deux puis cinq lignes, image paysage remplacée par portrait ; 390/820/980/1200 px | Aucun texte masqué, ratio/boîte explicites, hauteur du parent et voisins cohérents |
| C3 : vide / imbriqué | Section vide, conteneur, feuille et descendant | Cibles valides et interdites ; aucun cycle ni déplacement partiel |
| C4 : composition superposée conditionnelle | À rattacher à une référence explicite avant d’activer un nouveau libre borné | Bornes/calques/repli mobile/ordre de lecture ; documenter N/A si non nécessaire |
| C5 : historique | Mêmes déplacements avec Escape, capture perdue, undo/redo cible + voisins | État provisoire absent du document et de l’historique ; focus restitué |

Référence réelle reprise pour T03 : Tennis AI / Accueil, UUID cbf41f07-a35b-4043-81df-98e91c8118a5, audit R18 schéma 4. T01 a observé deux sections, deux conteneurs, deux boutons et un texte, sans titre/image ni média disponible. Ces éléments manquants sont préparés explicitement au lancement T03 ; aucune recette T02 ne suppose leur présence actuelle. Les métadonnées T01 sont historiques et non une lecture de tête rejouée ici.

En réalisation T02 : utiliser données fictives et média autorisé sur le banc Wagtail, avec manifestes versions/UUID et captures navigateur identifié. Mesurer aussi les seuils 767/768/1023/1024, zoom/scroll et chargement police/image pour les repères. T03 vérifie la surface interactive et le clavier/focus ; T18 qualifie fluidité, lecteur d’écran et tactile matériel. Les captures seules ne démontrent ni accessibilité ni sauvegarde.



---

## Fichier : RESEARCH.md

# T02 — Sources et état réel rapprochés

20 novembre 2026 · lecture de cadrage, sans tests applicatifs ni interrogation de la tête courante. Pas de dépôt Git exploitable dans LeStudio ou studio ; identification par manifeste SHA-256.

## Notion relu avant cadrage

Les pages complètes relues figurent dans [sources-notion.json](sources-notion.json) : carte T02, parent UI-004, T01, règle de relecture « 03 — Workflow, tasklist et preuves », guide de prise de lot, vision produit, roadmap, socle FEAT-003-01, catalogue FEAT-003-03, aperçu FEAT-004 et futur parcours T03. Leurs dates d’édition ne valent pas approbation. La carte T02 initiale est DRAFT, type Architecture, UI requise non ; T01 est DONE, parent PLANNED.

Décisions humaines reprises : manipulation directe/prototype adoptés et retrait physique V1/V2 imposé dans le plan courant du 20 novembre. Choix frontend : décision technique de l’auteur T01, JS natif sur Django. Aucun choix de grille, schéma ou protocole de rendu immédiat n’est présenté comme accepté par l’utilisateur.

## Matrice de l’existant

| Source locale | Constat observé en lecture | Conséquence T02 |
|---|---|---|
| composition/validation.py, placement.py | Schémas 1–4 ; flow/free et stack/grid ; unités locales, champs et limites stricts | Comparer avant extension, préserver lecteurs et bornes |
| composition/editor.py | block_place peut appliquer parent/before et placement | Garder le transfert atomique et tester les repères |
| composition/builder_batch.py | Transaction/idempotence/base existent ; document et collisions validés après chaque commande | Nouveau groupe de geste final cible/voisins, distinct du lot |
| static/ui/builder-edit-model.js | block_place n’applique pas parent/before comme le serveur | Test de parité explicite avant réemploi/extraction |
| engine/reference/preview.py | Rendu schémas 1–4, min-height calculée depuis les enfants free ; hauteur fixe des boîtes | Contrat contenu long et nouveaux champs à propager au renderer |
| composition/figma_mapping.py | Produit du schéma 4, identités source/occurrence ; ne traduit pas toute position/dimension | Adapter au contrat final sans prétendre qualifier Figma réel |
| composition/canvas_format.py et renderer | Seuils 768/1024 ; formats de démonstration 390/820/1200 | Tester aussi largeur 980 et voisinage des seuils |
| Catalogue et services | Définitions versionnées, médias par site, historique/conflits/droits | Migration sans propagation de catalogue ni contournement |
| T01 / REFERENCE-PRODUIT.md et page-reference.json | Audit R18 sans titre/image ni média disponible | Préparation contrôlée en T03, aucune donnée créée ici |

La collision existante compare les frères libres ; le mélange flux/libre n’est pas couvert par cette détection. La largeur flow en grille est relative à l’aire de grille, contrairement à la largeur free relative au parent contenant. Ces écarts interdisent de recopier naïvement une boîte entre modes/parents.

## Vérifications prévues et limites actuelles

Prolonger tests/test_composition_validation.py, test_composition_services.py, test_builder_batch.py, test_builder_parity.py, test_builder_canvas.py, test_preview_bridge.py, test_figma_mapping.py, test_figma_imports.py et test_figma_provenance.py ; moteur engine/reference/test_preview.py. Les tests déjà réussis dans T01/FEAT-004 ne sont pas déclarés rejoués.

La mission ne modifie que le dossier T02 et sa restitution Notion. Aucun rendu navigateur nouveau nécessaire pour les documents de cadrage ; la preuve de rendu appartient à la réalisation planifiée. Aucun connecteur Figma réel appelé.

## Délégation réelle

/root/t02_existant : lecture seule indépendante des modèles, commandes, renderer et producteurs ; aucun fichier autorisé à l’écriture ; rapport reçu, limites intégrées. /root/t02_revue : revue indépendante favorable du cadrage, sans réserve de fond ; compte rendu dans REVIEW.md et evidence/revue-cadrage.md.

Comparaison de fraîcheur : les 213 sources du manifeste T01 sont identiques au workspace courant. Cette comparaison est enregistrée dans evidence/comparaison-sources-t01.json ; elle ne réinterroge ni l’image Docker ni la tête du brouillon.

## Limite des outils Workflow AI

Le CLI partagé ne reconnaît que des identifiants sans suffixe et lie Architecture au préfixe ARCH. T02 possède déjà l’identité Notion UI-004-02 et le type Architecture ; ne pas renommer la carte ni la transformer en composant pour contourner cette limite. Le contrôle complémentaire local evidence/check-planning.py adapte uniquement l’identité/type de ce lot dans un module chargé en mémoire, vérifie les documents et refuse les opérations hors cadrage. Le workflow partagé reste inchangé. Le PASS complémentaire n’est ni une validation des gestes ni un mandat d’implémenter.



---

## Fichier : REVIEW.md

# T02 — Revue du cadrage

Avis indépendant favorable de /root/t02_revue, distinct de l’auteur /root et de l’inspecteur /root/t02_existant. Aucun constat de fond restant. [Compte rendu indépendant](revue-cadrage.md), empreintes des pièces et limites incluses.

La revue porte sur le cadrage PLANNED, sa fidélité aux sources, les scénarios AC1–AC4 et le découpage T02/T03. Elle ne valide ni une réalisation des gestes ni un schéma 5 définitif. Aucun test métier, lecture de tête courante ou appel Notion effectué par le reviewer.



---

## Fichier : EVIDENCE.md

# T02 — Index des preuves de cadrage

Les pièces ci-dessous prouvent des lectures et contrôles documentaires, jamais la réalisation des gestes.

| Pièce | Portée |
|---|---|
| evidence/sources-notion.json | Instantanés des 11 pages applicables relues avant cadrage, dont carte, parent et dépendances |
| evidence/manifest-sources.json | Empreinte des sources locales et références T01 examinées ; absence de Git explicitée |
| evidence/comparaison-sources-t01.json | 213 sources du workspace identiques au manifeste T01 ; image Docker non réinterrogée |
| evidence/check-planning.py | Contrôle complémentaire borné à UI-004-02, Architecture, cadrage uniquement |
| evidence/controles.json | Commandes, date UTC, Python, codes retour, résultats standard et complémentaire, liens et empreintes |
| evidence/manifest-contrat.json | Empreinte Workflow des quatre documents de base et empreinte élargie des pièces de cadrage |
| evidence/revue-cadrage.md | Avis d’un exécutant distinct sur le dossier final, avec limites |
| evidence/publication-notion.json | Identifiants et résultat de publication de la synthèse/pièce examinable |

La collecte n’interroge pas la tête actuelle du brouillon et n’exécute pas les scénarios métier. Les captures de T01 restent des preuves historiques référencées ; aucune capture de nouveau geste n’est annoncée.

Les empreintes du registre task.json lient la revue au contrat et aux pièces examinées. PLANNED et un contrôle documentaire réussi ne remplacent pas les essais AC1–AC4. Le CLI standard reste incompatible avec l’identifiant suffixé/type Architecture ; cette limite est conservée dans controles.json.



---

## Fichier : evidence/revue-cadrage.md

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


