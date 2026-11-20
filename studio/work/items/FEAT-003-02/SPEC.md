# FEAT-003-02 — Pages, arborescence et navigation autonome

Un opérateur prépare les pages et les menus d’un site dans son brouillon Studio. La hiérarchie donne son chemin à chaque page. L’opérateur décide séparément où les visiteurs pourront la trouver dans la navigation. Le raccordement Wagtail est facultatif pour ce travail.

## Parcours et critères de recette

| Situation | Résultat attendu après développement |
|---|---|
| Créer « Contact » sous l’accueil | La page possède une identité stable et un chemin. Elle reste absente des menus jusqu’à l’ajout explicite d’une entrée. |
| Modifier le titre seul | Le slug et les libellés personnalisés des entrées restent identiques. Les destinations internes continuent de référencer l’identité de page. |
| Déplacer une page ou modifier son slug | Présenter les chemins avant/après de la branche et les entrées concernées dans chaque menu. Demander confirmation quand une destination change. Annuler conserve la révision. |
| Supprimer une branche | Montrer les descendants et les entrées touchées. L’opérateur choisit explicitement le retrait ou une nouvelle cible autorisée pour chacune, ou annule. Tant qu’une référence reste invalide, l’enregistrement échoue intégralement. Protéger la racine. |
| Configurer plusieurs menus | Créer et nommer par exemple Principal, Secondaire et Pied de page. Chaque menu possède son ordre, ses groupes, ses sous-menus et ses libellés. Une page peut être présente dans plusieurs menus. Une entrée peut cibler une page ou une adresse HTTPS autorisée. |
| Réordonner et choisir la visibilité | Offrir un contrôle clavier pour déplacer l’entrée et changer de parent. Après enregistrement et rechargement, retrouver le même ordre entre frères et les choix bureau/tablette/mobile. Changer un menu ne déplace aucune page. |
| Deux opérateurs ouvrent la même révision | La première sauvegarde réussit. La seconde conserve la saisie et permet de relire la dernière révision, puis de réexaminer les impacts avant de soumettre. |
| Accès lecture ou inter-site | La lecture autorisée expose le brouillon du seul site courant. Une écriture en lecture seule et une cible étrangère sont rejetées côté serveur. |
| Site actif et historique | Comparer l’état du moteur avant/après et les révisions locales. Seule une sauvegarde explicite et valide ajoute une révision centrale. |

## Intégration au parcours Studio

La fiche Site donne le contexte de site et du brouillon. La maquette situe les vues Pages et Menus dans l’atelier. Le lot 02 fournit ces vues ciblées et leurs contrats. FEAT-003-04 porte l’entrée générale de l’atelier et l’éditeur structuré, FEAT-003-05 le canvas. Prévoir une entrée directe autorisée aux vues de ce lot pour sa recette isolée. En l’absence de brouillon, présenter l’état vide et utiliser le parcours de création du socle lorsqu’il est disponible. FEAT-004 porte l’aperçu et FEAT-005 l’application au site.

## Références

[Carte de cadrage](https://app.notion.com/p/41d49e23bbdb81e397a7e9419df59f8c) · [Lot parent](../FEAT-003/SPEC.md) · [Contrat des données](ARCHITECTURE.md) · [Permissions](SECURITY.md) · [Plan](TASKLIST.md) · [Maquettes](VISUAL-REVIEW.md)
