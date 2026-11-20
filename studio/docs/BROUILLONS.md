# Brouillons de composition du Studio central

Le service Python de [composition](../composition/services.py) est destiné aux parcours Atelier. Il prépare des révisions dans la base du Studio. Le site peut déjà être raccordé à Wagtail ou être une simple fiche du registre. La consultation de la fiche et celle du raccordement gardent leurs propres sources.

## Lecture, création et enregistrement

Les exemples ci-dessous supposent un acteur Django et une fiche Site déjà résolus par l’appelant. La création et la sauvegarde nécessitent le mandat de gestion sur ce site. En lecture, le mandat de lecture suffit. L’exemple crée des données et doit être utilisé sur un site de démonstration.

```python
from composition.services import (
    creer_brouillon, enregistrer_brouillon, lire_brouillon, lire_revision,
)

tete = lire_brouillon(acteur, site.pk)
if tete is None:
    tete = creer_brouillon(acteur, site.pk, {"kind": "blank"})

document = tete["document"]
document["pages"][0]["title"] = "Bienvenue"
suivante = enregistrer_brouillon(acteur, site.pk, tete["id"], document)
precedente = lire_revision(acteur, site.pk, tete["id"])
```

Le numéro identifie l’ordre des révisions d’un site. L’UUID de la tête sert de précondition de sauvegarde. Si la tête a avancé, le service signale un conflit ; garder la saisie et relire la tête pour comparer les changements. Un essai répété sur la même base ne produit pas une deuxième révision gagnante. Un refus d’accès doit être traité avant de présenter toute métadonnée de révision à l’appelant.

La [forme V1](../work/items/FEAT-003-01/COMPOSITION.md) précise les identifiants, le contenu admis, les valeurs responsive et les bornes. Un document compact peut atteindre 1 Mio en UTF-8. Pour les entrées JSON brutes, un plafond distinct de 4 Mio, espaces compris, est appliqué avant décodage. Les pages, sections et blocs gardent leur identité avec les modifications successives. À la création depuis une source externe de confiance, leurs identifiants sont renouvelés et les références entre pages remappées. Les résolveurs utilisés pour l’origine et les références sont des dépendances locales de l’appelant autorisé ; ils valident la portée effective du site. Les futurs sous-lots fourniront les catalogues et propositions réels.

La version courante du brouillon et ses versions antérieures sont locales. Une confirmation technique de raccordement ne désigne aucune version appliquée. Lire ou enregistrer un brouillon n’appelle pas Wagtail. Depuis la fiche Site, ouvrir **Atelier du site** pour créer ou reprendre le brouillon. Les entrées **Pages** et **Menus** ouvrent leurs outils spécialisés.

## Organiser les pages et la navigation

1. Ouvrir **Mes sites**, choisir la fiche du site et ouvrir **Pages**. Avec le droit de gestion, créer un brouillon vierge si le site en est dépourvu.
2. Créer la page sous le parent voulu, avec son titre et son segment d’URL. Elle peut rester hors menu. Modifier le titre conserve le chemin. Modifier le segment ou déplacer un parent présente les chemins concernés, y compris ceux des descendants.
3. Dans **Menus**, choisir ou créer un menu. Ajouter un groupe, un lien vers une page de ce brouillon ou un lien HTTPS externe. Le libellé, la position et les formats de visibilité appartiennent à l’entrée. Les formats d’un parent limitent aussi la visibilité de ses enfants.
4. Pour supprimer une branche, examiner les pages et les entrées affectées. Choisir les liens à retirer ou leur nouvelle cible. Examiner le bilan puis confirmer pour enregistrer une seule révision. Annuler conserve la révision précédente.

Les anciennes révisions restent lisibles dans leur format d’origine. La première modification depuis ces vues sur un brouillon V1 écrit une nouvelle révision V2. En cas de conflit, relire la révision courante et vérifier de nouveau la proposition avant de l’enregistrer. [Contrat de navigation](../work/items/FEAT-003-02/ARCHITECTURE.md)

## Régler les composants et l’apparence

Depuis **Mes sites**, ouvrir la fiche du site puis **Bibliothèque**. Les fiches présentent la portée, la version et les paramètres du composant. Titre, texte, conteneur, image et bouton sont disponibles au catalogue global. Un composant de site reste privé jusqu’à une promotion revue. Choisir une version pour une occurrence ne modifie aucune autre occurrence.

Dans **Apparence**, enregistrer les réglages du brouillon, notamment les couleurs, la typographie et l’espacement. Une préférence pour une définition s’applique à la version choisie. Sur un bloc déjà présent, la variante et les valeurs propres au bloc prennent la priorité. Retirer la surcharge redonne la valeur héritée. Les réglages d’apparence sont utilisables sur une page encore vide. Pour insérer de nouveaux blocs, ouvrir **Atelier du site** depuis la fiche.

Un diagnostic indique la page et le bloc à corriger si une version ou un média est indisponible. Remplacer la référence par un choix autorisé, ou demander le retrait explicite du bloc, puis relire le diagnostic. La publication du site et l’aperçu de page sont suivis dans FEAT-005 et FEAT-004.

Pour proposer un composant local au catalogue global, préparer un libellé public, le motif du partage et la référence de la preuve des droits. Un second opérateur habilité au site et membre du groupe de revue vérifie la proposition avant de l’accepter ou de la refuser. L’acceptation crée une définition partagée. Les sites gardent la version déjà choisie.

### Ressource de démonstration et livraison technique

Le catalogue fournit une illustration de démonstration attribuable par l’équipe. Depuis `studio/`, remplacer `UUID_SITE` par l’identifiant de la fiche concernée. L’attribution la rend sélectionnable dans ce site. La révocation rend le diagnostic visible dans les brouillons qui la référencent.

```sh
docker compose exec -T web python manage.py catalogue media UUID_SITE attribuer
docker compose exec -T web python manage.py catalogue media UUID_SITE revoquer
```

Pour rendre l’encart codé « signature » disponible dans la bibliothèque d’un site de démonstration, l’équipe peut livrer sa première version. Le premier `signature` est la clé de définition et le second est l’identifiant du rendu livré.

```sh
docker compose exec -T web python manage.py catalogue version UUID_SITE signature 1 signature "Encart"
```

Le groupe **Réviseurs du catalogue Studio** complète le mandat de gestion du site source pour la seconde personne qui décide d’une promotion. Les droits de réutilisation et la copie destinée au partage sont vérifiés lors de cette décision.

## Composer le contenu d’une page

1. Dans **Mes sites**, ouvrir la fiche puis **Reprendre le brouillon**. Le numéro de révision figure sur la fiche. Pour un premier brouillon, choisir **Créer le brouillon**, sélectionner **Page vierge** ou **Présentation d’activité**, puis confirmer. Le modèle contient déjà une section, un titre et un texte.
2. Sous **Page à composer**, choisir la page et cliquer sur **Ouvrir la page**. Si elle est vide, cliquer sur **Ajouter une section**, choisir sa disposition et **Enregistrer**.
3. Sélectionner la section dans **Structure de la page**. Dans l’inspecteur, sélectionner le **Composant à insérer**, puis **Ajouter un composant**. Renseigner les champs et enregistrer. Pour un bouton, saisir le libellé et la destination HTTPS. Pour une image, sélectionner un média attribué au site et remplir l’alternative.
4. Pour changer un texte, sélectionner son occurrence et cliquer sur **Modifier le composant**. Pour déplacer un bloc, ouvrir **Déplacer le composant**, choisir la section ou le conteneur de destination, puis le frère devant lequel l’insérer ou **À la fin de la destination**. Le déplacement conserve les enfants du bloc.
5. Rouvrir la page pour retrouver sa structure et ses valeurs. Avant un retrait, l’inspecteur indique le nombre de descendants concernés. **Annuler** conserve la révision. Si deux fenêtres modifient le même brouillon, **Relire la révision courante** permet de comparer avant de confirmer la proposition.

Un opérateur en lecture ouvre **Consulter le brouillon**. Toutes les sauvegardes de l’atelier alimentent le brouillon de Studio. L’application au site Wagtail relève de FEAT-005. Le point de départ Figma ouvre les remises du site. Une proposition confirmée crée le premier brouillon ou ajoute des pages à la révision existante. [Importer une remise](REGISTRE.md#importer-une-remise-dans-le-brouillon) [Contrat de l’éditeur structuré](../work/items/FEAT-003-04/ARCHITECTURE.md)

## Déplacer un bloc dans le canvas

1. Dans **Mes sites**, ouvrir la fiche puis **Ouvrir le canvas**. Depuis l’atelier, choisir **Canvas** à côté d’**Éditeur structuré**. Les deux vues travaillent sur le même brouillon. Si la page est vide, **Ajouter une section**, la sélectionner puis insérer un composant dans l’inspecteur.
2. Choisir **Format de travail** puis **Afficher le format**. Dans une grille ou une pile, saisir le bloc par la poignée en haut à droite et le déposer avant ou après un autre bloc, ou dans un conteneur. Le repère indique la destination. L’ordre de lecture est commun aux trois formats. Échap annule le geste en cours.
3. Pour superposer un bloc, le sélectionner puis ouvrir **Régler le placement**. Choisir **Libre**, remplir X et largeur en pourcentage du parent, Y et hauteur en pixels, puis enregistrer. Par exemple, X à 10 %, Y à 20 px, largeur à 50 %, hauteur à 120 px. Le niveau de superposition détermine quel frère passe devant. La poignée inférieure droite permet de redimensionner le bloc. **Sélectionner dans la structure** permet de retrouver un bloc recouvert.
4. Sur tablette ou mobile, modifier uniquement les propriétés qui doivent différer du bureau. Pour reprendre une valeur de base, cocher la propriété sous **Rétablir les valeurs héritées ou par défaut** puis enregistrer. Pour une section ou un conteneur, **Disposition responsive** permet d’adapter la pile, la grille et l’espacement au format choisi.
5. Au clavier ou au tactile, les formulaires **Déplacer le composant** et **Régler le placement** donnent accès à l’ordre et à la géométrie. Après une modification concurrente, relire la révision puis confirmer la proposition voulue. En lecture seule, la sélection et le changement de format permettent d’examiner la page.

Un dépôt valide enregistre une révision locale lorsqu’il modifie la disposition. Le contenu et ses identifiants suivent le bloc lorsqu’on change de vue. [Contrat du canvas](../work/items/FEAT-003-05/ARCHITECTURE.md)

## Modifier une page qui référence un article Wagtail

Dans **Mes sites → fiche du site → Atelier**, ouvrir la page puis sélectionner le bloc dans **Éditeur structuré** ou **Canvas**. Un titre, un texte court, le libellé et la destination HTTPS d’un bouton se modifient dans l’inspecteur Studio. Pour une image, choisir un média attribué à ce site et renseigner son texte alternatif. Ces champs restent disponibles quand le moteur est hors ligne. Enregistrer crée une révision du brouillon si la valeur change.

Pour un article, les deux numéros affichés ont des usages distincts. Le numéro de **page Wagtail** identifie l’article sur cette instance. Le numéro de **révision publiée Wagtail** désigne la publication que l’opérateur a choisie pour cette occurrence.

1. Dans l’administration Wagtail de ce site, ouvrir la page Article. Relever son numéro dans l’adresse d’édition, par exemple **42** dans `/admin/pages/42/edit/`. Pour préparer le texte, enregistrer un brouillon dans Wagtail. Pour le rendre disponible à la vérification Studio, un utilisateur habilité publie la page et vérifie son accès public.
2. Dans Studio, sélectionner la section de destination et ouvrir l’association d’un article. Saisir le numéro de page et choisir **Vérifier la source**. Comparer le numéro de page et la publication observée, puis **Associer l’article** pour enregistrer le bloc dans le brouillon Studio.
3. Après une nouvelle publication Wagtail, sélectionner le bloc et choisir **Vérifier la source**. **Conserver la référence** garde le repère actuel. **Adopter la révision publiée** le remplace dans une nouvelle révision Studio. Si une autre publication intervient entre les deux actions, relire les numéros avant de confirmer.
4. Pour modifier le corps, reprendre la session éditoriale habituelle dans Wagtail. L’inspecteur propose un raccourci lorsque l’adresse d’administration est configurée pour ce navigateur. Si la source est inaccessible ou protégée, l’ancienne référence reste consultable dans le brouillon. Un lecteur Studio peut consulter le repère et la dernière observation datée.

L’association et le retrait concernent l’emplacement de l’article dans la composition. La publication de la composition sur le site public relève de FEAT-005. [Configuration du moteur](MOTEUR-WAGTAIL.md)

## Ouvrir le Visual Builder sur Studio local

Dans **Mes sites**, ouvrir la fiche puis **Reprendre le brouillon**. Choisir la page et la révision puis **Afficher le rendu**. Avec un mandat de gestion, ouvrir l’éditeur sur la dernière révision. Pendant l’observation, les liens directs vers `/sites/<uuid>/atelier/` et `/sites/<uuid>/atelier/canvas/` donnent accès à la V1. Les deux entrées retrouvent les mêmes enregistrements.

- Pour insérer une section à une position précise, sélectionner la section qui doit la suivre et choisir **Insérer une section avant**. Vérifier les descendants annoncés avant le retrait d’une branche. **Annuler** et **Rétablir** agissent sur les gestes locaux. **Enregistrer** crée la révision commune aux deux ateliers.
- Pour un réglage responsive, saisir une largeur de travail de 320 à 1 920 px, choisir le bloc ou la section, puis modifier la propriété au format voulu. L’inspecteur permet de rétablir l’héritage d’une seule propriété.
- Pour remplacer la définition d’une occurrence, enregistrer les gestes en cours puis suivre le lien de l’inspecteur vers la **Bibliothèque**. Vérifier la définition et ses champs avant de confirmer. Le bloc conserve son identifiant.
- Pour associer une publication, choisir une section ou un conteneur puis ouvrir **Articles Wagtail**. Après **Vérifier la source**, comparer la page et la révision publiée. Seule la confirmation modifie le brouillon. Le lien de retour rouvre la page et l’occurrence dans le Visual Builder.

Avec un mandat de lecture, les signets et l’historique permettent de retrouver la page et son rendu privé. Le dossier de recette présente les parcours sur les deux interfaces. [Comparatif produit](../work/items/UI-003-05/evidence/comparatif-produit.pdf)
