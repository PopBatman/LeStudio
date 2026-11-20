# Revue indépendante de cadrage

Le 19 novembre 2026, `/root/canvas_review` a examiné la frontière entre le canvas prévu et l’éditeur structuré livré. Le contrat parent demande que les deux modes conservent les mêmes identités, le même ordre de lecture et le même brouillon révisé. [Carte Notion](https://app.notion.com/p/41d49e23bbdb81e386a3ef5f4bf26492) · [Contrat parent](../FEAT-003/ARCHITECTURE.md)

## Vérification du socle livré

Dans l’image locale Studio, avec SQLite en mémoire migrée, un document fictif V3 contenant une grille à trois colonnes, une surcharge tablette à deux colonnes et un affichage mobile en pile a été validé à l’identique. La valeur `free` ajoutée à la disposition V3 a déclenché une erreur sur le champ. Le même document en version 4 a déclenché une erreur de version incompatible. L’essai a utilisé un conteneur sans réseau et aucune donnée opérateur. [Validation courante](../../../composition/validation.py)

La revue du code a identifié les écritures de version dans l’éditeur et l’apparence et les vérifications strictement V3 dans la validation et dans la copie des origines privées. La compatibilité doit être éprouvée sur ces chemins avant d’ouvrir le premier brouillon V4 en écriture. Les formats tablette et mobile héritent chacun de la base, propriété par propriété. [Services](../../../composition/services.py) · [Éditeur structuré](../../../composition/editor.py) · [Apparence](../../../composition/appearance.py)

## Correspondance avec la carte

| Critère | Preuve demandée pour la réalisation |
|---|---|
| Déplacement conservé | Réouvrir une autre session, retrouver l’UUID déplacé et son parent et comparer la révision d’origine. |
| Parité structure et canvas | Effectuer une édition dans chaque mode, relire la même tête et vérifier les panneaux qui réenregistrent le document. |
| Grilles et superpositions responsives | Comparer les valeurs effectives et propres aux trois formats après changement d’une seule propriété puis retour à l’héritage. |
| Alternative au geste | Insérer, déplacer, redimensionner et changer de niveau au clavier, sélectionner dans la structure une occurrence recouverte et écouter le retour d’état. |
| Erreurs et site actif | Essayer deux sites, un lecteur, une géométrie invalide et deux écritures concurrentes. Contrôler les révisions conservées et l’absence d’appel moteur. |

Ces cinq scénarios figurent dans la [spécification](SPEC.md). La [tasklist](TASKLIST.md) prévoit les essais de persistance PostgreSQL, de performance aux limites du document, de focus et de lecteur d’écran sur l’interface Django.

## Essai de la maquette

Dans Chromium à 320 px de large, j’ai activé le lien de saut au clavier, déplacé le titre en troisième position avec le formulaire et retrouvé ce titre en dernière position dans l’éditeur structuré. J’ai placé le titre en mode libre, puis modifié x et le niveau de superposition en mobile. Au retour au bureau, x et le niveau avaient gardé leurs valeurs de base. Une largeur mobile de 98 % avec x à 15 % a produit un message de dépassement et transféré le focus sur l’erreur. Aucun débordement horizontal de la fenêtre ni erreur JavaScript pendant ce parcours. [Maquette examinée](evidence/maquettes.html)

La première version de la commande de retour à l’héritage effaçait simultanément plusieurs réglages. Après correction, j’ai repris sur mobile un bloc avec x à 15 % et un niveau de superposition à 4. Rétablir seulement x a redonné 10 % depuis le bureau et conservé le niveau mobile à 4. Le contrat V4 sépare le placement de l’apparence et impose la validation des trois formats effectifs, y compris après modification du parent. [Architecture](ARCHITECTURE.md)

**Avis favorable au passage en READY pour le cadrage.** Les preuves couvrent le validateur déjà livré et les interactions de la maquette en mémoire. La persistance V4, les écritures concurrentes, la performance et le lecteur d’écran sur Django restent des critères de recette du futur développement.

## Revue indépendante de réalisation

L’exécutant `/root/canvas_release_review` a suivi le parcours de la fiche Site au niveau de l’occurrence, puis le dépôt jusqu’au verrou de révision. Structure et Canvas soumettent des commandes à la même tête du site. Le contrôle de la géométrie s’applique aux trois formats et précède la conservation des propriétés opaques. Les services de navigation, d’édition et d’apparence conservent la version d’un document V4. La copie depuis une source privée est contrôlée au niveau du site. [Validation du placement](../../../composition/placement.py) · [Services du brouillon](../../../composition/services.py)

Sur Chromium, en consultation à 390 px, j’ai ouvert une sélection avec une largeur simulée personnalisée de 767 px puis alterné les deux vues au clavier. L’identité du bloc, sa sélection annoncée et la largeur simulée ont été conservées. La page en lecture n’expose aucune poignée de déplacement ou redimensionnement ni formulaire de geste. La recette de l’équipe complète cet essai par les dépôts, la gestion des erreurs et la mesure aux limites du document. [Recette navigateur](evidence/navigateur.json) · [Mesures sur 2 000 nœuds](evidence/performance.json)

La revue a reproduit une défaillance avec un brouillon V1 valide. Une ancienne propriété textuelle nommée `layout` correspondait désormais à une définition locale de conteneur avec la même clé et version. L’ouverture du canvas levait une exception. Après correction du domaine et de la projection, mon essai indépendant retrouve une page consultable (HTTP 200), un diagnostic sur le composant et un refus maîtrisé (404) pour les deux accès GET et POST au réglage du faux conteneur. Le domaine vérifie également le type de la destination lors d’une insertion. La largeur personnalisée est transmise au changement de page et le résultat d’un enregistrement dans le canvas annonce son format. J’ai rejoué les 26 tests ciblés des domaines Canvas, vues Canvas, services de l’éditeur et navigation sur SQLite en mémoire. [Tests des vues](../../../tests/test_canvas_web.py) · [Tests métier](../../../tests/test_canvas_domain.py)

**Avis favorable à la réalisation de FEAT-003-05.** La qualification auprès d’utilisateurs et la direction artistique transverse restent suivies dans UI-002.
