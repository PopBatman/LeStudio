# LeStudio · langage visuel de l’atelier

## Composition et identité

Le site, la page et la révision occupent la barre de l’atelier, avec les commandes de sauvegarde et d’aperçu. L’opérateur choisit un élément à gauche, observe la page au centre et règle la sélection dans l’inspecteur. Le site fictif Atlas du Sud emploie des titres Georgia, un paysage vert et une encre olive à l’intérieur de sa page. Les commandes de la coque emploient DM Sans. Ce découpage doit encore être reconnaissable sur une capture recadrée.

Les fondations de production sont définies dans [gallery.css](../../../frontend/gallery.css) et dans le [contrat des composants](../../../docs/COMPOSANTS-UI.md). Le tableau fixe les rôles proposés pour la V2. Les couleurs et tailles du prototype restent soumises à l’examen artistique.

| Rôle | Fondation Studio | Emploi dans l’atelier |
| --- | --- | --- |
| Texte principal et surfaces sombres | Encre `#262724` | Libellés, titres de panneaux, commandes prioritaires. Vérifier séparément le contraste des commandes sur fond sombre. |
| Surface principale et papier | Fond `#f8f7f3`, papier `#f6f3eb` | Coque et regroupements. Un espace autour de la page fait apparaître sa limite effective. |
| Séparateurs et information secondaire | Ligne `#d8d6cb`, sable `#ddd8c9`, texte secondaire `#62645c` | Séparer bibliothèque, page et inspecteur. Garder lisibles la version d’un composant, la portée du média et l’origine de la valeur responsive. |
| Marque et action | Vermillon `#ef603b`, texte accent `#a2311a` | Réserver le vermillon à un accent ponctuel. Utiliser une teinte de texte contrastée pour les petits libellés et proposer un état en mots pour toute alerte. |
| Typographie de la coque | DM Sans locale, puis Arial ou police système. Monospace système disponible pour les identifiants. | Libellés courts en graisse moyenne, titres de panneau plus affirmés. Réserver les capitales courtes aux repères. Les titres et paragraphes du canvas suivent la typographie du site. |
| Focus et sélection | Focus de la galerie de 3 px en `#893219` sur surface claire | Le prototype propose un contour de focus bleu pour les commandes. Examiner sa visibilité dans la coque et sur le contenu d’Atlas du Sud. Le focus décrit la commande pilotée au clavier. Le contour de sélection et le nom du calque décrivent le bloc en cours. Les deux doivent rester distincts quand le focus entre dans l’inspecteur. |

Sur le fond Studio `#f8f7f3`, le calcul de luminance relative sRGB donne un contraste de 14,01:1 pour l’encre, 6,55:1 pour le texte accent et 5,60:1 pour le texte secondaire. Le vermillon donne 3,06:1 sur ce fond et 2,96:1 sur papier ; réserver les petits libellés à l’encre ou au texte accent. Ces mesures portent sur les paires de couleurs des fondations. Tester séparément le style effectivement rendu, les états sélectionnés et les contours superposés aux images.

## Densité et gestes à examiner

Utiliser une trame proposée de 4, 8, 12, 16 et 24 px. Rapprocher le libellé de son champ, séparer deux groupes de propriétés et dégager le pourtour de la page. La taille du contenu dans le canvas dépend de la largeur simulée. Une page longue garde une voie de retour aux commandes et le texte d’un calque long reste identifiable.

| Repère | Forme et comportement attendus |
| --- | --- |
| Icônes | Un pictogramme correspond à une intention stable. Les commandes rares et tout message de résolution gardent un libellé visible. Une commande compacte a un nom accessible et un focus visible. |
| Poignée et dépôt | Placer la poignée près du bloc concerné. Le guide indique la destination et la position avant/après. Une destination refusée donne le motif. Le libellé de la commande de déplacement reste compréhensible sans geste de glissement. |
| Sélection et édition | Contour sur le bloc et nom dans les calques et l’inspecteur. L’édition de texte conserve le titre visible sur la page. Les commandes de retour depuis l’aperçu restaurent le contexte d’édition. |
| Révisions et erreurs | Afficher en mots l’état de la saisie et la révision de l’aperçu. Pour une péremption, montrer les deux révisions. Pour une erreur, donner une action de reprise. Pour un conflit, permettre d’examiner la version courante en conservant la saisie. |
| Formats | Bureau avec trois régions. Sur tablette, évaluer la place réellement disponible pour la page. Sur mobile, rendre les panneaux accessibles par commande nommée et restituer le focus à la fermeture. Le sélecteur de largeur de la page et la largeur physique de l’appareil sont deux contrôles distincts. |

La [matrice des interactions](INTERACTIONS.md) précise les alternatives clavier. La [fiche de revue](VISUAL-REVIEW.md) recueille l’avis humain sur la densité, la lisibilité et les gestes. Les preuves de fidélité du moteur et du glisser-déposer de production seront apportées par les sous-lots 02 et 03.
