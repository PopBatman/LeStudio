# Référence et recette visuelles UI-004

## Avant le code

Le frontend futur est concerné ; aucun écran applicatif ne change dans ce cadrage. La tasklist précède ce document. La référence est le prototype fluide joint à la [vision Notion](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539), adopté par l’utilisateur le 20 novembre 2026 selon cette page. [Copie exacte locale](evidence/prototype-adopte.html), téléchargée au cadrage, origine `lestudio-prototype-simule-manipulation-directe.html`. L’auteur/générateur de la pièce jointe n’est pas attesté ; aucune paternité nouvelle n’est inventée.

L’adoption concerne la direction : bibliothèque gauche, page prioritaire, gestes, poignées, texte sur place, menus courts et annulation. Grille 12 colonnes, pas 16 px et délai simulé 650 ms ne sont pas des décisions de production. Document en mémoire de session, sauvegarde et publication simulées.

## États à qualifier

| État / parcours | Intention | Recette |
|---|---|---|
| Normal/sélection | Bibliothèque accessible, page centrale, contrôles selon contexte, pas d’inspecteur droit obligatoire | T01/T03/T06 |
| Page/section vide | Dépôt compréhensible et cible accessible au clavier | T03/T04 |
| Drag/resize provisoire | Cible/guides/voisins, annulation Échap/capture perdue et focus conservé | T02/T04/T05 |
| Texte long/saisie | Double-clic, sélection préservée, validation et retour focus ; pas de masquage | T03/T06 |
| Menu | Clic droit, Options, clavier/tactile, fermeture et retour composant | T06/T18 |
| Sauvegarde | Modifié/en cours/enregistré/erreur selon acquittement réel | T03/T08 |
| Conflit/réponse inconnue | État local préservé, diagnostic et reprise explicite | T09 |
| Rendu périmé/indisponible | Travail courant distinct de l’aperçu enregistré ; pas de geste spatial sans mesure fiable | T03 |
| Formats/contenu limite | Bureau/tablette/mobile/intermédiaire, héritage et ordre de lecture | T02/T07 |
| Origines | Vierge/template/Figma réel vers le même éditeur et document | T11/T19, FEAT-006 |

T01/T02 examinent présentation mobile et clavier/contextuel. La direction adoptée ne prouve pas chaque état. Préparer menu/focus selon [W3C APG — Menu Button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/) et interruption des gestes selon [W3C Pointer Events](https://www.w3.org/TR/pointerevents3/), consultés le 20 novembre 2026. Une recette navigateur demeure nécessaire.

## Après réalisation

Capturer page simple/dense sur candidat identifié aux largeurs 1200/820/390 et intermédiaire. Comparer travail immédiat, sauvegarde et Wagtail à largeur identique. Consigner URL, navigateur, viewport, date, sources/empreinte et état de données. Les captures du prototype restent étiquetées simulation ; elles ne sont pas celles du produit futur.

J1 montre Tennis AI réel ; T18/UI-002 mesurent et qualifient clavier, tactile et lecteur d’écran ; T19 recueille séance réelle et décision de bascule versionnée. Aucun test applicatif ou audit d’accessibilité n’est déclaré réussi par ce document.


## Requalification après retrait

T21 supprime physiquement les anciens builders après T19 et réexécute les parcours critiques et captures sur le candidat nettoyé. Le résultat de T19 ne suffit pas pour livrer cet autre artefact. Les anciennes URLs ne chargent aucun ancien écran ; T20 utilise la révision nettoyée qualifiée.
