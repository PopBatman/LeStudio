# FEAT-004 — Aperçu du site

Depuis la fiche Site, l’opérateur choisit une page et une révision enregistrée pour examiner ce que le moteur Wagtail du site rendrait. Le même parcours permet d’examiner une ancienne révision avant une éventuelle restauration. L’atelier reste propriétaire des brouillons. UI-003 consommera le rendu et la correspondance des blocs. FEAT-005 portera les opérations de publication et de restauration.

## Parcours retenu

1. Afficher le site, la page et la dernière révision enregistrée. Depuis un formulaire modifié, proposer de revenir enregistrer ou d’ouvrir explicitement la révision indiquée. Préparer un aperçu ne sauvegarde aucun champ.
2. Vérifier la portée opérateur/site, la liaison à l’instance et les capacités du moteur. Présenter « Préparation de l’aperçu » puis afficher le résultat authentifié. Conserver un retour à la fiche ou à l’atelier.
3. Afficher nom du site, page, numéro de révision, heure de préparation et échéance. Les détails présentent l’instance, les versions de composants et les références éditoriales/médias utilisées. Bureau, tablette et mobile consultent le même instantané.
4. Si une nouvelle sauvegarde intervient, conserver le numéro examiné et signaler la nouvelle révision. Une demande explicite prépare celle-ci. Lorsqu’une ressource devient interdite, retirer l’accès au rendu. Après expiration ou perte de vérification, présenter une action pour reprendre.
5. Pour comparer, choisir la révision précédente et la même page par identifiant stable. Présenter les deux révisions avec leur provenance, leurs différences de composition et leur rendu si disponibles. Indiquer page ajoutée/supprimée si elle manque d’un côté. Une version active n’est proposée que sur preuve d’application au site. En son absence afficher « Version active inconnue ». Un article publié n’établit pas quelle composition est active.

## Décisions du cadrage

| Sujet | Règle proposée pour le développement |
|---|---|
| Brouillon | Composition Studio enregistrée et immuable. Le numéro est qualifié par le site et l’UUID de révision. Les références éditoriales Wagtail portent la révision publiée explicitement épinglée, encore accessible. L’accès aux brouillons privés de l’administration Wagtail exige un autre contrat de droits. |
| Acteurs | Lecture ou gestion du site pour préparer et relire son propre aperçu de session. Gestion pour enregistrer via le parcours existant. Aucune URL publique de partage. |
| Durée | Dix minutes absolues à compter de la préparation, sans prolongation à la lecture. Changer de format conserve l’échéance. Repréparer réévalue les droits et les sources. |
| Fidélité | Moteur et gabarits internes versionnés, structure des pages, menus, sections, blocs, variantes, tokens, placement par format, texte simple, références autorisées. Une capacité, police, version ou ressource requise indisponible produit un état explicite. |
| Historique | Lire les schémas de composition 1 à 4 conservés par Studio. Tester une projection de lecture des formats pris en charge. Si un ancien schéma ne peut être rendu fidèlement, le signaler avant de présenter le résultat. Aucune migration implicite. |
| Édition et mise en ligne | La présentation permet inspection, navigation interne sous contrôle et comparaison. Les opérations de modification du builder, d’import Figma, de publication et de restauration ont leurs propres lots. |

## Recette à réaliser sur le produit

| ID | Action et résultat observable |
|---|---|
| A1 | Sur deux sites de test, demander la révision N du premier. Le HTML Wagtail, les témoins de données et le manifeste concordent avec ce site, son instance, la page et N. Un changement d’instance, une confusion d’identités ou une version incompatible interrompt l’ouverture. |
| A2 | Préparer avec des champs non enregistrés puis sauvegarder N+1 pendant la préparation de N. L’aperçu reste marqué N, affiche l’écart puis permet d’ouvrir N+1 explicitement. Une double demande ne modifie aucune composition. |
| A3 | Contrôler avant/après les révisions Studio et Wagtail, la révision live, les contenus publics et l’URL publique du site témoin. Toute préparation, comparaison, expiration et reprise conserve ces valeurs. |
| A4 | Tester méconnaissance du site, accès d’un autre opérateur ou d’une autre session, retrait de droit, média désactivé, article devenu privé ou republié. Refuser la ressource, y compris après la préparation. Aucun ancien HTML ou média ne doit être resservi sur échec de vérification. |
| A5 | Contrôler les trois formats sur une fixture comprenant navigation, sections imbriquées, variantes, police, image, contenu local et article Wagtail. Chaque bloc visible retrouve exactement son UUID sur la page. Documenter les différences visuelles et les captures du moteur. |
| A6 | Couper la connexion, simuler l’expiration, une version absente et un résultat incomplet. Afficher un diagnostic et une action praticable. Réessayer sur la même révision après rétablissement. |
| A7 | Comparer deux révisions, une première révision sans parent et une page supprimée. Distinguer chaque résultat, la dernière sauvegarde et la version active attestée ou inconnue. Le retour à l’atelier conserve le contexte du site. |
| A8 | Tester clavier seul, lecture des statuts, intitulé du cadre, retour de focus, largeur de 320 pixels et navigation au sein de la seule révision. Aucun contrôle de publication dans l’aperçu. |

Décisions produit et critères d’origine dans la [carte du lot](https://app.notion.com/p/41c49e23bbdb81aaa190ee5c236cbe8b). Le délai de dix minutes et les modalités de comparaison sont des choix de cadrage.
