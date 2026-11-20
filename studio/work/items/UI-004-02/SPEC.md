# UI-004-02 — T02 · Contrat des gestes et modèle de disposition

Version de cadrage : 1 · 20 novembre 2026 · état visé : PLANNED.

## Objectif, mandat et sources

Préparer le document canonique et les commandes permettant de déplacer et redimensionner réellement titre/image, conserver cette intention après enregistrement et la rendre avec Wagtail. La demande utilisateur « Cadre UI-004-02 — T02 · Contrat des gestes et modèle de disposition conformément au Notion et au Workflow AI » autorise ce cadrage, sa revue et sa restitution documentaire sur la carte existante. Elle ne lance pas la réalisation de T02, T03 ou une migration de données.

Carte : https://app.notion.com/p/41e49e23bbdb817695efdccd260a063f ; parent UI-004, audit T01 DONE, vision et prototype adoptés le 20 novembre. [Sources relues](RESEARCH.md), [instantané Notion](evidence/sources-notion.json). Risque STANDARD : transformation de brouillons, erreurs de placement, contenu masqué, isolement et concurrence. Aucune nouvelle validation humaine des options techniques n’est enregistrée.

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

[CONTRAT-PROPOSE.md](CONTRAT-PROPOSE.md) fixe les options de travail, unités, règles de voisins, conversion de parent, annulation et migration. Il distingue l’existant des ajouts proposés. La grille à 12 colonnes et les coordonnées du prototype ne sont pas une décision de production. La décision finale est prise et documentée après les essais T02-02/03 ; toute réduction de la liberté produit requiert un arbitrage utilisateur.

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

