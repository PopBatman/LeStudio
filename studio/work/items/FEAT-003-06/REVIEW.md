# Revue indépendante du cadrage

Le 19 novembre 2026, `/root/hybrid_review` a confronté les cinq critères de la [carte FEAT-003-06](https://app.notion.com/p/41d49e23bbdb813fb814de85024ce68d) au [contrat parent](../FEAT-003/ARCHITECTURE.md), au validateur du Studio et aux routes du moteur.

## Essai du socle livré

Dans l’image locale de FEAT-003-05, un processus Docker sans réseau a migré une base SQLite en mémoire et créé deux sites fictifs. Sur le premier, j’ai démarré du modèle, réglé la largeur mobile du titre, puis modifié son texte et inséré un bouton HTTPS et une image attribuée avec une alternative. La tête relue était en V4, révision 5. Le titre avait gardé son UUID et sa largeur mobile, le bouton sa destination, l’image son alternative. Une destination HTTP, un média attribué seulement à l’autre site et une écriture sur une ancienne base ont tous été refusés. J’ai relu la première révision à l’identique. [Observations](evidence/socle-studio.json)

Le résolveur livré par la bibliothèque accepte les médias attribués. Mon appel de vérification pour une référence éditoriale Wagtail a renvoyé faux. Les quatre routes moteur identifiées servent l’identité, la version, la santé et le rendu de référence. La comparaison d’une révision éditoriale demande une capacité distincte. Le profil de transport contient une origine technique, et le snapshot du raccordement n’enregistre aucune URL d’administration validée pour le navigateur. [Résolveur](../../../composition/catalogue.py) · [Routes du moteur](../../../engine/cmengine/urls.py) · [Contrat de raccordement](../ARCH-002-01/ARCHITECTURE.md)

## Manipulation indépendante de la maquette

Sur Chromium, à 320 px de large, j’ai utilisé le clavier pour sélectionner un bouton, saisir une destination HTTP puis enregistrer. Le focus est revenu au champ en erreur et la révision du brouillon est restée à 7. Une destination HTTPS valide a produit la révision Studio 8. J’ai ouvert la référence éditoriale, demandé la vérification puis conservé le repère d’origine. La révision Studio était toujours 8. La confirmation de l’adoption du repère Wagtail 24 a produit la révision Studio 9. En lecture seule, la maquette affichait les valeurs et retirait la commande de vérification. Le document tenait dans la largeur de l’écran, sans erreur JavaScript. [Maquette](evidence/maquettes.html)

J’ai signalé une comparaison incohérente dans le scénario simulé après adoption. La maquette affichait une divergence et proposait une nouvelle adoption pour deux numéros de révision identiques. Après correction, j’ai rejoué l’intégralité du parcours. Avec 24 retenu et 24 observé, la nouvelle vérification indique « Référence confirmée » et la commande d’adoption disparaît.

## Couverture des exigences

| Critère de la carte | Condition vérifiable inscrite au plan |
|---|---|
| Modifications simples retrouvées, site actif préservé | Comparer historique, titre, lien, image et placement après ouverture dans les deux vues ; observer les requêtes et les versions du site actif. |
| Responsabilité éditoriale de Wagtail | Essayer deux sessions Wagtail avec des droits distincts ; couvrir publication, restriction de la page et restriction héritée. |
| Divergence de révision | Distinguer brouillon éditorial et publication, revalider le numéro de publication avant adoption, puis refaire la comparaison en cas de nouvelle publication ou de changement du brouillon Studio. |
| Refus des données invalides et de l’accès croisé | Deux sites avec numéros de page identiques, média étranger, URL invalide, retrait de mandat et changement d’instance. |
| Propriété et synchronisation | Relire dans un ancien instantané la révision source retenue auparavant ; comparer les historiques après consultation, vérification, association, adoption et détachement. |

[Spécification](SPEC.md) · [Sécurité](SECURITY.md) · [Plan](TASKLIST.md)

## Avis

Le contrat technique conserve un repère immuable par site, instance, type, page et révision source ; une observation indépendante porte la date et le résultat d’une lecture. L’adoption contrôle à nouveau la publication, les identités et le mandat, puis conditionne la nouvelle révision Studio à la tête attendue. Ce choix préserve les anciennes révisions et traite la possibilité d’une publication après la lecture. Le composant éditorial attendu, le modèle Article, le filtre sur la racine et les droits de lecture, ainsi que le transport versionné figurent dans le périmètre de réalisation. [Architecture](ARCHITECTURE.md) · [Examen des révisions Wagtail](evidence/revisions-wagtail.json)

**Avis favorable au passage en READY pour le cadrage.** La présente revue qualifie le comportement local déjà livré et les interactions simulées. La recette de réalisation devra démontrer sur deux instances l’isolement des références, les restrictions d’accès, la divergence réelle des révisions publiées et la persistance après adoption.

## Revue indépendante de réalisation

L’exécutant `/root/article_review` a suivi la sélection du bloc, la vérification sur le profil du site, les contrôles de mandat au retour de l’appel réseau et le verrouillage du brouillon à la confirmation. Le moteur lit le jeton de publication du type Article dans la racine Wagtail effective en appliquant les restrictions héritées. L’inspecteur lit le repère et l’observation séparément. Les deux vues passent par le même service d’écriture. La consultation des preuves de concurrence PostgreSQL complète les essais indépendants ci-dessous. [Service éditorial](../../../composition/editorial.py) · [Lecture Wagtail](../../../engine/reference/editorial.py) · [Essais PostgreSQL](evidence/domain-postgres.log)

Deux régressions de compatibilité ont été corrigées au cours de la revue.

1. Un ancien document V1 contenait un champ `content` textuel dont la définition est désormais celle d’un article. Sur la première version, la sélection de cette occurrence donnait HTTP 500 en Structure et en Canvas. Après correction, les deux vues renvoient HTTP 200, proposent la vérification ou le remplacement et conservent la révision originale. J’ai rejoué ce scénario en SQLite en mémoire avec un document créé par le service historique. [Inspecteur](../../../composition/editor_views.py) · [Tests de régression](../../../tests/test_editorial_web.py)
2. Une promotion effectuée avant le lot pouvait avoir réservé la clé globale `article` en version 1 pour un rendu texte. Dans mon essai de migration 0003 vers 0004, la première version du code laissait cette ligne seule et rendait l’insertion d’un article impossible. Après correction, la migration conserve la version 1 promue et crée le composant standard en version 2. J’ai vérifié puis confirmé une association dans une base migrée ainsi. Le document épingle la version 2, le rendu de la version 1 reste texte et le connecteur de test compte deux lectures. [Migration](../../../composition/migrations/0004_editorial.py) · [Association](../../../composition/editorial.py)

J’ai également exécuté 20 tests ciblés sur SQLite pour les services éditoriaux, le transport, les deux inspecteurs et le canvas. Ils passent tous. La recette navigateur de l’équipe documente deux publications intervenues entre la comparaison et l’adoption ainsi que le retrait du bloc. [Recette navigateur](evidence/navigateur.json)

**Avis favorable à la réalisation du lot FEAT-003-06 après correction des deux régressions examinées.** L’application de la composition à un site public relève de FEAT-005.
