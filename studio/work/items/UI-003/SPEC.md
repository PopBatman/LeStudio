# UI-003 — Visual Builder V2
Cadrage parent du 20 novembre 2026. L’opérateur ouvre une fiche Site et compose une page dans un seul atelier. Il voit le site tel que le moteur rend la révision choisie, sélectionne un bloc dans la page et le modifie au même endroit. La barre supérieure identifie le site, la page, la largeur et l’état du brouillon. Le panneau gauche réunit Pages, Calques, Composants et Médias. L’inspecteur à droite détaille la sélection.

## Trois entrées dans le même atelier
| Entrée | Premier geste | Résultat à la réouverture |
| --- | --- | --- |
| Page vierge | Insérer un titre via la bibliothèque dans une section autorisée | La page et son titre sont retrouvés dans la révision enregistrée |
| Modèle | Ouvrir Présentation d’activité v1, sélectionner un bloc, modifier son texte | Le brouillon conserve les identifiants des autres blocs et l’origine du modèle |
| Figma | Ouvrir le brouillon après confirmation des correspondances FEAT-003-08 | Mêmes calques, inspecteur et opérations. L’opérateur retrouve la provenance, les écarts acceptés, les composants inconnus et les déclinaisons manquantes |

Depuis les trois entrées, l’opérateur peut changer de page, sélectionner un bloc dans les calques, modifier son contenu, enregistrer, comparer le rendu et revenir à la fiche Site. Le graphiste invité reste limité au dépôt de sa proposition. Les contenus avancés administrés dans Wagtail conservent leur parcours et leurs droits.

## Contrat d’usage et recette transverse
| Capacité | Résultat observable | Lot de preuve |
| --- | --- | --- |
| Rendu | Page, site, instance et révision affichés correspondent au rendu privé FEAT-004. Si N+1 existe pendant la lecture de N, N reste identifié. Indisponibilité, incompatibilité, expiration et repli en lecture sont visibles. | 02 |
| Sélection | Le même UUID est sélectionné dans le canvas, les calques et l’inspecteur, y compris après un déplacement. Une réponse de rendu retardée ne déplace pas la sélection vers une autre page. | 02–03 |
| Composition | Recherche, insertion, duplication, déplacement, suppression et annulation ont une commande clavier. Un guide montre la destination et explique un refus. Titres, textes, boutons et images se modifient dans le contexte du bloc. | 03 |
| Versions | Une sauvegarde sur la révision de départ produit un successeur. Deux sessions concurrentes voient un conflit explicite. Une demande rejetée conserve la saisie et propose de relire la dernière révision. Undo/redo respecte les contraintes du document et ne réécrit pas l’historique. | 03 |
| Responsive | Bureau, tablette et mobile montrent la largeur inspectée, les valeurs héritées et les surcharges. Une surcharge mobile ne modifie pas la valeur bureau. Un débordement ou chevauchement est localisable au clavier. | 01–03 |
| Catalogue et médias | L’insertion vérifie identifiant, version, portée globale/site, propriétés typées, enfants et compatibilité du rendu. Une référence absente ou d’un autre site est signalée. Une version ultérieure du catalogue laisse les instances existantes identifiables. | 02–04 |
| Figma | Comparer la référence disponible au rendu du même brouillon. Une seule largeur source suffit. Conserver les largeurs disponibles et signaler les déclinaisons manquantes. L’opérateur tranche les écarts ; un composant inconnu est proposé à l’équipe pour développement interne. | 04 |
| Continuité | Les brouillons historiques v1 à v4 s’ouvrent avec leurs références. La recette couvre site A/site B, révocation, page longue, navigation clavier, lecteur d’écran et trois largeurs. La bascule V1 attend parité, approbation humaine et retour arrière vérifié. | 05 |

## Limites et décisions réservées
La publication, l’application à Wagtail et la restauration du site actif relèvent de FEAT-005. Le cadrage exclut marketplace, plugins installables et conversion de HTML/JS externe en composant. La qualification Figma de FEAT-003-08 utilise un fournisseur simulé à la demande de l’utilisateur. Un brouillon canonique déjà validé suffit pour la recette de reprise dans l’atelier.

UI-003-01 fera arbitrer la densité, le comportement des panneaux sur petit écran, le rythme de sauvegarde et la perception des états d’annulation. UI-003-02 qualifiera le pont de sélection sécurisé et la fidélité par famille de composants. UI-003-05 recueillera la décision humaine de bascule. Les cinq cartes conservent leurs mandats et leurs preuves propres.
