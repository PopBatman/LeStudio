# Contrat de disposition : UI-004-02 / T02

**État : première tranche implémentée en PR, contrat de disposition complet encore en construction.**

Référence produit : [UI-004-02 dans Notion](https://app.notion.com/p/41e49e23bbdb817695efdccd260a063f).
Le premier objectif est de regrouper les déplacements d'occurrences sans faire échouer
une collision *transitoire*. Il ne s'agit pas encore d'un éditeur de manipulation
directe complet, ni d'un nouveau schéma de rendu Wagtail.

## Invariants conservés

| Propriété | Contrat de la première tranche |
| --- | --- |
| Document | Schémas 1 à 4 toujours lisibles ; aucune version 5 introduite |
| Identité | UUID des sections, pages et blocs conservés ; aucune duplication implicite |
| Composition | Parent unique, arbre acyclique, destination vérifiée par le backend |
| Formats | `base`, `tablet`, `mobile`, avec héritage existant |
| Placements | `flow` / `free` ; boîtes locales au parent, bornes déjà en vigueur |
| Conflits | Une nouvelle collision non explicitement autorisée est rejetée |
| Historique | Une révision par sauvegarde validée, ou aucune si une commande échoue |
| Sécurité | Contrôle de l'acteur et du site, clé de requête idempotente, base verrouillée |
| Rendu | Wagtail reste la source de l'aperçu réel ; aucun changement de rendu dans cette tranche |

## Commande expérimentale `gesture_group`

Un lot de sauvegarde existant peut contenir une nouvelle commande :

```json
{
  "action": "gesture_group",
  "steps": [
    {"action": "block_place", "id": "uuid-a", "format": "base", "patch": {"x": 55}},
    {"action": "block_place", "id": "uuid-b", "format": "base", "patch": {"x": 0}}
  ]
}
```

La commande regroupe **entre 2 et 8** `block_place` portant sur des
**occurrences distinctes**. Cette limite est provisoire et restrictive :
pas de `block_remove`, `section_*`, `block_add`, groupe imbriqué,
ni de superposition `overlap: true` dans cette première tranche.
Le plafond historique de **128 opérations effectives par sauvegarde**
reste appliqué même si plusieurs opérations sont enveloppées dans un groupe.

Les étapes sont calculées en mémoire sur la copie de la révision autorisée.
Le backend valide **le document final**, tous les formats et les collisions
des cibles, puis ajoute une seule révision et un seul reçu idempotent si
le lot entier est cohérent. Une collision intermédiaire due à l'ordre des
deux déplacements n'est pas une collision finale.

Les anciennes commandes demeurent inchangées : `block_place` hors groupe
est toujours validée immédiatement. Aucun changement silencieux du sens du
schéma 4 ou des clients existants.

### Refus et annulation

- Même UUID répété dans un groupe : refus.
- Nombre d'opérations insuffisant, trop élevé ou action inconnue : refus.
- Placement final hors du parent, structure incompatible, dépassement d'une
  boîte libre ou nouvelle superposition : refus.
- Permissions révoquées ou révision `base` périmée : refus avant persistance.
- Une commande du lot échoue : **zéro révision et zéro reçu** pour ce lot.
- Un retry strictement identique avec la même `key` retourne le reçu existant.
- L'annulation d'un geste provisoire dans le navigateur appartient au lot
  UI/T03 : elle n'est pas simulée par cette API de sauvegarde.

## État RED → GREEN de la première tranche

La [PR applicative](https://github.com/PopBatman/LeStudio/pull/4)
contient les tests PostgreSQL d'échange de positions A/B, collision finale,
rollback, idempotence et permissions. La première exécution des tests
nouveaux a échoué avec `Commande de composition inconnue`
[CI RED](https://github.com/PopBatman/LeStudio/actions/runs/45063220017),
puis le code a passé la suite ciblée sur
[CI GREEN](https://github.com/PopBatman/LeStudio/actions/runs/45063269211).
Ces contrôles sont observés sur des données jetables et non sur Tennis AI.

## Modèle de gestes local (incrément JS)

La projection locale `static/ui/builder-edit-model.js` reconnaît désormais
`gesture_group` dans son modèle en mémoire. Un groupe unique peut être
prévisualisé, confirmé, annulé et rétabli sans exposer les collisions
intermédiaires aux interactions UI. Le moteur local applique également
`parent` et `before` de `block_place` pour se rapprocher du serveur,
avec refus d'un déplacement dans sa descendance.

Cette projection JS **n'est pas une autorité** : Django continue d'appliquer
les contrôles de site, les permissions, la validation multiformat,
l'atomicité SQL et l'idempotence. L'interface visuelle de manipulation
directe, le pont Wagtail et la sauvegarde automatique seront qualifiés
dans T03/T04/T08 ; aucun nouveau bouton ni déploiement n'a été ajouté.

La [CI JS RED](https://github.com/PopBatman/LeStudio/actions/runs/45063818689)
observait le refus « Commande inconnue », puis la
[CI JS GREEN + Django](https://github.com/PopBatman/LeStudio/actions/runs/45063893529)
a validé la parité sur des fixtures fictives :
- **253 tests Django** sur PostgreSQL, 16 ignorés ;
- **27 tests ciblés**, 1 ignoré ;
- test JavaScript Node du modèle, déplacement et retour arrière : **PASS**.

## Preuve du vrai renderer Wagtail sur une composition fictive

La [CI #45064784828](https://github.com/PopBatman/LeStudio/actions/runs/45064784828)
a exécuté deux jobs indépendants sur PostgreSQL éphémère :

- `t02-atomic-gestures` : **254 tests Django complets** (16 ignorés),
  **28 tests ciblés** (1 ignoré), parité JavaScript Node PASS.
- `t02-wagtail-render` : **5 tests Wagtail** dans le vrai projet
  `studio/engine`, dont le nouveau
  `test_grouped_final_positions_are_rendered_without_publishing`.
  Le rendu compare deux titres et leurs placements libres
  `x=0` et `x=55` après échange, préserve leurs UUID,
  produit un nouveau hash HTML et constate que le nombre de
  révisions Wagtail ainsi que la révision publiée restent inchangés.

Il s'agit d'une **preuve de rendu du document final synthétique**, pas
d'une interaction de navigateur avec Wagtail, ni d'une édition de la
vraie page Tennis AI. Les tests du backend sont responsables de la
transition atomique ; Wagtail rend la composition finale reçue.

## Conditions de continuation T02 (non acquises)

- Comparer réellement les solutions flux/grille et documenter le placement
  horizontal, l'auto-height du titre et les ratios d'image.
- Définir si la nouvelle sémantique exige une version 5, sans réinterpréter
  silencieusement les schémas 1–4.
- Qualifier `block_place` avec `parent`/`before`, le placement des
  voisins, les collisions et les formats de façon exhaustive.
- Mettre le modèle de gestes JS en parité avec le contrat backend.
- Faire une démonstration avec le **renderer Wagtail réel** sur compositions
  fictives ; le parcours Tennis AI appartient à T03.
- Exécuter des scénarios de concurrence PostgreSQL, un audit indépendant
  sur le dernier SHA et la recette des AC1 à AC4 avant de clore T02.

**Cette tranche n'active aucun déploiement, aucune publication et aucun
automatisme d'agent.**
