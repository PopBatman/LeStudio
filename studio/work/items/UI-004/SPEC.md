# UI-004 — Édition par manipulation directe

Cadrage v1 · 20 novembre 2026 · **PLANNED**. [Carte de pilotage](https://app.notion.com/p/41e49e23bbdb81eab216e51aec661753).

## Besoin et mandat

L’opérateur habilité construit une page dans son rendu : bibliothèque permanente à gauche, déplacement des composants et sections, poignées, texte sur place et réglages contextuels. L’enregistrement automatique conserve un brouillon versionné ; seul le serveur confirme sa sauvegarde. L’aperçu Wagtail identifie la révision effectivement rendue.

La [vision du 20 novembre](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539) adopte cette direction et remplace les prescriptions UX des anciens builders. Le mandat présent est « Cadre UI-004 […] conformément au Notion et au Workflow AI » : examiner les sources et le code, spécifier, planifier, préparer les références, faire relire et actualiser la carte. Il ne lance pas les quatorze sous-lots. L’adoption du prototype ne valide pas d’avance le modèle de disposition ou une bibliothèque frontend.

## Périmètre du programme

| Domaine | Résultat attendu | Responsable |
|---|---|---|
| Fondation réelle | Matrice des acquis, choix frontend argumenté, modèle des gestes, premier parcours Wagtail | T01–T03 |
| Gestes directs | Bibliothèque, déplacement interne/entre sections, tri des sections, poignées, édition et menus, responsive | T04–T07 |
| Fiabilité | Annulation par geste, autosauvegarde acquittée, reprise et conflits sans écrasement silencieux | T08–T09 |
| Site complet | Catalogue interne, thèmes, templates et navigation multipage dans le même parcours | T10–T11 |
| Qualité et bascule | Mesures dès T03, qualification accessible avec UI-002, séance réelle, compatibilité, suppression physique V1/V2 et requalification | T18/T19/T21 |

Les vingt et une tâches et quatre jalons de la [roadmap](https://app.notion.com/p/41c49e23bbdb810d9b63c90efd1aeff6) restent inchangés. T12–T15 appartiennent à FEAT-006 (Figma réel), T16–T17 à FEAT-005 (publication/restauration) et T20 à ARCH-003 (environnement cible). UI-004 définit leurs interfaces et prérequis, sans absorber leur réalisation. Aucune suppression de route, migration ou activation n’est effectuée par ce cadrage.

## Contrat UX et gestes

Écran métier de composition. Entrées : acteur, site autorisé, page, UUID de révision de base, document canonique, définitions/version/portée, médias autorisés, format et raccordement. Sélection, menu, geste provisoire et focus sont locaux ; la révision validée est la référence persistée.

| Intention | Interaction et résultat | Refus / récupération | Recette |
|---|---|---|---|
| Insérer | Attraper dans la bibliothèque gauche ; cible et effet visibles avant dépôt ; nouveaux UUID au commit | Composant incompatible, média absent ou parent interdit : raison et document intact | T03/T04/T10 |
| Déplacer un composant | Translation dans la section, transfert entre sections/conteneurs compatibles ; prévisualiser les voisins | Descendance interdite, cible disparue, Échap, sortie ou capture perdue : aucun commit | T02/T04 |
| Déplacer une section | Poignée contextuelle, glissement avant/après une autre section, défilement pendant geste | Annulation conserve ordre, enfants et références | T04 |
| Redimensionner | Poignées, guides, dimensions bornées, ratio et réaction des voisins définis | Aucun texte masqué silencieusement ; dépassement diagnostiqué | T02/T03/T05 |
| Éditer | Double-clic sur le texte ; préserver curseur/sélection ; média et lien selon composant | Pas de drag pendant saisie ; validation annoncée, saisie gardée en erreur | T03/T06 |
| Régler | Menu court au clic droit ou bouton Options ; réglages approfondis à la demande | Clavier/tactile équivalents ; retour du focus au déclencheur | T06/T18 |
| Annuler/rétablir | Un geste terminé = une entrée ; le geste provisoire n’est pas une révision | Distinguer annulation du travail et restauration d’une ancienne version | T03/T08 |
| Sauvegarder | Regrouper les gestes terminés ; états modifié/en cours/confirmé/erreur selon serveur | Clé/requête conservées si réponse incertaine ; conflit explicite | T03/T08/T09 |
| Adapter au format | Héritage bureau et surcharges tablette/mobile visibles et réinitialisables | Un transfert de parent partagé n’est jamais annoncé comme mobile seulement | T02/T07 |
| Changer de page | Page/sélection/révision identifiables et gestes non acquittés traités | Ne pas abandonner implicitement la saisie | T08/T09/T11 |

Sur petit écran, la bibliothèque reste accessible par un accès stable ; T01 éprouve sa présentation sans empêcher la manipulation de la page. Les largeurs 390, 820 et 1200 px et une largeur intermédiaire sont des cas de recette. Noms accessibles, focus visible, ordre de lecture, annonces, réduction du mouvement et équivalents clavier/tactile font partie du contrat. Les raccourcis de texte gardent leur sens pendant la saisie.

## Données, droits et invariants

- Pointeur, clavier et tactile portent la même intention : site, page, base, occurrence, destination/format et valeurs typées. Autorisations et validation complète restent côté serveur.
- Un déplacement conserve UUID, contenus, versions et références. Une copie reçoit de nouveaux UUID pour sa descendance. Une nouvelle définition globale ne met pas à jour silencieusement les occurrences épinglées.
- Seul le code interne livré et compatible est insérable. Les cinq types globaux historiques sont titre, texte, image, bouton et conteneur. Hero/galerie/footer ne sont pas présumés disponibles.
- Pas de HTML, CSS ou JavaScript arbitraire provenant de Figma ou d’un dépôt exécutable comme composant. Médias et références d’un autre site refusés.
- Les schémas 1–4 restent traçables. T02 arrête leur compatibilité et les éventuelles migrations ; T19/T21 prouvent compatibilité et repli. Ne pas réécrire une révision historique.
- Une requête logique et sa clé produisent au plus une sauvegarde acceptée. Base périmée : conflit ; révocation : refus même pour une ancienne clé.
- Travail immédiat, révision enregistrée et aperçu Wagtail confirmé sont distincts. Le reçu d’aperçu lie site, instance, page, révision et empreinte. Rendu périmé/indisponible signalé ; aucun geste/autosave n’applique au site actif.

## Premier jalon et acceptation

J1 suit T01 → T02 → T03 sur **une vraie page Tennis AI** avec image et titre. T01 consignera page, UUID et révision de recette au lancement.

| ID | Critère observable | Tâches / preuve attendue |
|---|---|---|
| AC-J1 | Déplacer une image, redimensionner la boîte du titre et modifier son texte, annuler/rétablir, enregistrer, rouvrir et retrouver contenu/place/dimensions dans Wagtail | T01–T03 ; vraie instance, révision/empreinte, commandes et captures avant/après, site actif préservé |
| AC-G | Bibliothèque permanente, gestes internes/entre sections et sections entières ; preview et commit concordent ; annulation sans effet | T04–T06 ; pointeur/clavier/tactile, vides, imbrication, capture perdue et textes longs |
| AC-R | Surcharge mobile indépendante, retour héritage, largeurs intermédiaires et ordre de lecture cohérents | T02/T07 ; modèle, moteur et comparaison aux mêmes largeurs |
| AC-S | Un undo par geste à travers l’autosave ; acquittement exact ; réponse tardive/perdue et concurrence sans perte silencieuse | T03/T08/T09 ; atomicité, idempotence, concurrence et navigateur avec interruption |
| AC-C | Chaque composant exposé passe gestes/rendu ; templates indépendants ; pages, médias et portée partagée cohérents | T10/T11 ; accueil/contenu/contact, navigation et réutilisation autorisée entre sites |
| AC-Q | Page simple/dense mesurées ; fonctions sans souris ; décisions humaines distinctes des mesures | T18/UI-002 ; appareils et budgets définis dès T03, traces et séance accessible |
| AC-B | Vierge/template/Figma réel convergent ; anciens documents repris ; publication/restauration observées ; bascule liée à un candidat et repli vérifié | T19 avec FEAT-006/FEAT-005 ; recette et décision humaines |
| AC-N | Aucun ancien builder V1/V2 réactivable ni ressource exclusive dans le code courant et l’artefact ; chaque élément conservé a un usage partagé ou de migration démontré ; tous parcours critiques passent après nettoyage | T21 après T19, avant T20 ; inventaire avant/après, références/consommateurs, build propre, installation/mise à niveau, tests et revue du candidat nettoyé |

Redimensionner le titre éprouve d’abord sa boîte et le retour à la ligne. La taille typographique n’est pas configurable dans les tokens actuels : si le geste retenu la modifie, T02 définit et versionne cette propriété jusqu’au moteur avant T03.

## Décisions et suite

La direction UX est adoptée par l’utilisateur dans Notion le 20 novembre 2026. Les propositions techniques de ce dossier restent des propositions : [options frontend/rendu](ARCHITECTURE.md), [conditions de passage](TASKLIST.md), [référence visuelle](VISUAL-REVIEW.md). Le parent est PLANNED : le plan est préparé ; T01/T02 et la qualification T03 ne sont pas achevés. Prochaine unité : cadrage T01 à partir de la matrice initiale, avec inventaire supprimer/remplacer/conserver des anciens builders, puis contrat T02. La clôture de UI-004 exige T21 terminé : masquer les menus ou désactiver des flags ne suffit pas. La production T20 utilise l’artefact requalifié après T21.

