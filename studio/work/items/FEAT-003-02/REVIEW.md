# Revue indépendante du cadrage

Le 19 novembre 2026, le réviseur `/root/nav_review` a rapproché les cinq critères de la [carte Notion](https://app.notion.com/p/41d49e23bbdb81e397a7e9419df59f8c) du [découpage parent](../FEAT-003/TASKLIST.md), de la [validation V1](../../../composition/validation.py) et des [services de brouillon](../../../composition/services.py).

**Constats sur le socle.** Le validateur exige en V1 une liste de menus vide. Le service de lecture classe actuellement les versions autres que 1 comme incompatibles. Le service d’enregistrement verrouille le site et l’habilitation puis compare l’identité de la tête avant de créer une révision. Le changement de version et le contrôle d’impact doivent donc être qualifiés à travers ces points d’entrée.

**Exemple vérifié.** Une lecture indépendante de l’[exemple V2](evidence/navigation-v2.json) a résolu le parent de chaque page, le parent de chaque entrée dans son propre menu et toutes les cibles internes. « Sur invitation » existe hors menu. « Dessin », enfant de « Les ateliers », est référencée par les menus Principal et Pied de page. Changer le chemin de « Les ateliers » affecte donc aussi ces deux entrées, en plus du lien du menu Secondaire vers le parent.

**Questions soulevées.** La recette devra isoler le retrait d’une entrée qui porte elle-même des enfants, préserver les blocs et le thème lors d’une mutation de navigation, et distinguer les écrans spécialisés du lot 02 de l’entrée générale de la fiche prévue au lot 04.

**Résolution des questions.** Le contrat prévoit la conservation des contenus des pages survivantes, le choix de déplacer les enfants d’une entrée ou de confirmer la suppression de sa branche, puis le recalcul d’impact sous verrou. La tasklist prévoit leurs tests. La spécification réserve l’entrée générale du site au lot 04 et définit une entrée directe pour vérifier les vues spécialisées du lot 02.

**Parcours rejoué sur la maquette.** Dans Chromium à 360 × 740, la touche Entrée après modification du segment de « La maison » ouvre le bilan et place le focus sur son titre. Le parent et l’enfant ont chacun un nouveau chemin, trois entrées sont signalées dans deux menus. Après annulation, « Carnet de saison » apparaît hors menu. Lors d’une suppression, la confirmation est indisponible avant les trois décisions. J’ai retiré deux entrées et reciblé la troisième sur « Contact » ; le pied de page affiche ensuite « Hébergement » vers `/contact/`. Le contrôle de l’intégrité serveur, la concurrence et la persistance après rechargement figurent dans la recette de développement.

**Avis favorable au passage en READY pour le cadrage.** Le plan, le contrat V2 et les parcours illustrés couvrent les cinq critères de la carte. Les valeurs de validité des URL et les plafonds de navigation sont des choix techniques proposés pour la réalisation. [Plan de développement](TASKLIST.md) · [Maquette interactive](evidence/maquettes.html) · [Relevé navigateur](evidence/examen-maquettes.json)

## Revue indépendante de réalisation

Le 19 novembre 2026, le réviseur `/root/navigation_release_review` a examiné la validation V1/V2, le remappage des identités, les services de lecture et d’écriture, les formulaires, les vues et le gabarit Django. La recette a utilisé des données fictives dans l’environnement PostgreSQL isolé.

**Déplacement et autorisations.** J’ai déplacé « Les ateliers » sous « Sur invitation ». Le bilan a présenté deux chemins sous `/invitation/ateliers/` et les trois entrées affectées dans trois menus. Après confirmation, j’ai relu l’ancienne révision et vérifié la conservation des menus et du thème. J’ai préparé la suppression, reciblé les trois entrées puis retiré le mandat de gestion avant confirmation. Le service a refusé l’écriture et la tête est demeurée celle du déplacement.

**Écarts traités pendant la revue.** Les commandes spécialisées préservent les feuilles personnalisées déjà admises sur la même page d’une ancienne révision. Une mutation directe du document reste soumise aux résolveurs. Le bilan empêche de confirmer un retrait laissant des enfants rattachés à l’entrée supprimée. Le formulaire garde le reciblage choisi jusqu’à la confirmation et les menus affichent l’intersection des formats de visibilité de l’entrée et de ses parents. Le serveur retourne un conflit lorsqu’une confirmation porte sur un bilan périmé. Les contrôles couvrent aussi l’historique, le refus d’une rétrogradation en V1 et la protection CSRF.

**Conflit et preuves.** La relecture conserve les anciennes décisions comme texte de comparaison et permet un nouveau bilan sur la tête courante. J’ai rejoué les tests des validateurs, du service et de l’interface après correction, avec 24 réussites sur SQLite. Le [parcours navigateur sur Django et PostgreSQL](evidence/application-navigateur.json) consigne la suppression mixte et le conflit entre deux lectures. L’avis porte sur le Studio central local et ses brouillons.

**Avis de réalisation favorable.** Les critères du lot sont couverts et les écarts identifiés pendant la revue ont été corrigés.
