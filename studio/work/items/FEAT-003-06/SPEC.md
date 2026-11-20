# FEAT-003-06 — Édition simple dans Studio et contenus Wagtail

Depuis **Mes sites → fiche Site → Atelier**, un opérateur peut modifier un titre ou une image de la page et savoir immédiatement où modifier un article qu’elle référence. Structure et Canvas reprennent le même brouillon et la même sélection. Ce lot complète l’inspecteur livré en 04 et 05 et introduit un composant de référence éditoriale. [Carte du lot](https://app.notion.com/p/41d49e23bbdb813fb814de85024ce68d) · [Contrat fonctionnel parent](../FEAT-003/SPEC.md)

## Propriété et parcours

| Élément sélectionné | Source de vérité et action proposée |
|---|---|
| Titre ou texte court | **Brouillon Studio**. Modifier le texte brut et, pour un titre, son niveau. Réutiliser les contraintes de la définition épinglée. Un homonyme dans une autre section conserve sa valeur. |
| Image | **Brouillon Studio** pour le choix d’un média attribué au site et son alternative. Expliquer comment obtenir une attribution lorsque le sélecteur est vide. Le remplacement conserve la position et les réglages du bloc. |
| Bouton ou lien | **Brouillon Studio** pour le libellé, la destination HTTPS et les réglages admis. Conserver la saisie en cas d’erreur. Les liens internes vers des pages du menu restent gérés dans Menus. |
| Article et contenu structuré | **Wagtail** pour le corps, le cycle éditorial, les permissions et la publication de l’article. **Brouillon Studio** pour l’emplacement du composant et le choix de la révision publiée de référence. Afficher l’identifiant de page et les révisions comparées avec leur origine. |

Un gestionnaire ouvre le bloc depuis le canvas ou l’éditeur structuré. La même commande d’édition par occurrence enregistre une révision locale avec sa base, préserve l’historique et fonctionne hors raccordement pour les valeurs simples. Une saisie identique conserve la tête. Le lecteur peut sélectionner les blocs et consulter les réglages enregistrés.

### Associer un article

Le premier type proposé est une page Article exposée par un moteur compatible. Dans le formulaire d’insertion du composant éditorial, le gestionnaire donne le numéro de page Wagtail puis demande une vérification sur l’instance confirmée de ce site. Studio présente le résultat autorisé, le numéro de page et la révision publiée observée. La confirmation crée ensemble la première occurrence et son repère dans la révision Studio. Annuler quitte le formulaire et conserve la tête. Un détachement ultérieur retire l’occurrence après confirmation ; le repère reste accessible aux anciennes révisions. Un identifiant identique sur une autre instance désigne une autre ressource. Une fiche Studio créée seule permet de travailler sur les contenus simples et indique le prérequis pour associer un article.

Pour écrire le corps de l’article, l’équipe utilise sa session habituelle dans l’administration Wagtail et ses droits éditoriaux. Un raccourci éventuel utilise une adresse de gestion explicitement configurée pour le navigateur. À défaut, l’inspecteur indique d’ouvrir l’administration habituelle et donne le numéro de page autorisé. Les coordonnées internes du profil technique servent au connecteur.

### Interpréter les deux révisions

Exemple fictif : le brouillon **Studio 12** pointe vers la **page Wagtail 42, révision publiée 7**. Une vérification ultérieure observe la publication 9. La révision Studio reste 12 pendant la comparaison. **Conserver la référence** laisse le repère sur 7. **Adopter la révision publiée 9** confirme une nouvelle révision Studio dont seule la référence concernée change. L’historique garde le repère 7. Un autre brouillon éditorial en préparation dans Wagtail reste sous le contrôle de son équipe. La révision épinglée désigne une observation historique ; la garantie de pouvoir rendre son ancien contenu devra être qualifiée au stade de l’application FEAT-005.

| État dans l’inspecteur | Information et action |
|---|---|
| Première insertion, aucun repère | Montrer comment vérifier puis associer sur une instance éligible avant de créer l’occurrence. En consultation, indiquer l’absence de référence. |
| Dernière observation concordante | Afficher le repère et la date de vérification. L’ouverture de la page relit les observations centrales ; le gestionnaire peut demander une nouvelle lecture. |
| Nouvelle révision publiée | Montrer le repère conservé et la révision observée, permettre de conserver ou d’adopter. L’adoption recontrôle l’identité, la source et la tête locale. Une troisième révision impose une nouvelle comparaison. |
| Source inaccessible, retirée ou protégée | Afficher **Référence à vérifier**. Conserver le brouillon et l’historique. Ne communiquer aucune donnée nouvelle identifiant une ressource inaccessible. Les contenus locaux indépendants restent éditables. |
| Moteur sans capacité, identité modifiée ou délai dépassé | Indiquer que la vérification éditoriale est indisponible. Une ancienne observation reste datée. Une confirmation ARCH-002 réussie ne suffit pas à déclarer l’article à jour. |
| Conflit local, erreur ou lecture seule | Préserver la proposition si le bloc existe encore, montrer la tête actuelle et demander confirmation après relecture. Refuser les mutations sans droit de gestion. Annoncer le résultat, le champ en erreur et la révision au clavier. |

## Critères d’acceptation du développement

1. Dans un site fictif A, changer successivement un titre, une image et un bouton depuis l’inspecteur. Rouvrir depuis l’autre vue. Comparer valeur, révision, ancienne tête, UUID, placement responsive et menus. Contrôler l’absence d’effet sur le site actif.
2. Créer dans le moteur de recette un article public avec un compte Wagtail habilité et un autre compte sans permission éditoriale. Vérifier les possibilités effectives de chacun. Tester aussi un article privé et une restriction héritée. L’inspecteur Studio offre des actions sur la référence locale.
3. Épingler une publication, préparer une nouvelle révision privée puis la publier dans Wagtail. Vérifier les deux états successifs dans Studio, comparer, conserver, puis adopter explicitement. Rejouer pendant une modification simultanée du brouillon Studio et pendant une troisième publication distante.
4. Sur deux fiches et deux instances, essayer un numéro de page identique, une référence étrangère, un média révoqué, une URL invalide et un mandat retiré pendant l’échange. Constater refus, absence de révélation et conservation des révisions.
5. Vérifier les requêtes et les deux historiques pour les actions ouvrir, vérifier, associer, adopter et détacher. Le moteur détient l’article ; Studio conserve le repère et les réglages de composition. La publication de la composition reste suivie dans FEAT-005.

[Contrat technique](ARCHITECTURE.md) · [Plan de réalisation](TASKLIST.md) · [Maquette et états](VISUAL-REVIEW.md)
