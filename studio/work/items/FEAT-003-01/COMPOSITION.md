# Document de composition v1

Ce contrat est proposé pour l’implémentation du socle. Les futurs éditeurs lisent le même instantané JSON ordonné. Une page vierge, une copie de template et une proposition Figma acceptée passent par le même validateur. La provenance du départ, le site autorisé, la révision de base, l’auteur et les horodatages appartiennent à l’enveloppe serveur. La donnée fournie à l’éditeur ne contient aucun secret de raccordement.

## Forme à enregistrer

L’[exemple fictif](evidence/composition-v1.json) est une révision de document possible, prête à servir de fixture. Les clés sont obligatoires sauf mention contraire. Un objet de propriétés accepte uniquement les clés documentées pour son type. Les tableaux portent l’ordre, y compris après relecture. L’ordre des clés d’un objet JSON est indifférent.

| Niveau | Champs et règles v1 |
|---|---|
| Racine | `schema_version` entier égal à 1, `pages` liste, `menus` liste vide dans 01, `theme` objet de réglages du site. La forme des entrées de menus et leurs opérations relèvent de 02. |
| Page | `id` UUID, `parent_id` UUID de page ou null, `slug` segment, `title` texte non vide (120 caractères), `sections` liste ordonnée. Une racine unique avec un slug vide. Autres slugs ASCII minuscules alphanumériques séparés par des tirets, de 1 à 80 caractères et uniques entre enfants du même parent. Un parent peut apparaître plus loin dans le document. Tout parent doit exister et conduire à la racine sans cycle. L’ordre relatif dans pages donne l’ordre entre frères. |
| Section | `id` UUID, `layout` objet, `blocks` liste ordonnée. Une section peut être vide. |
| Bloc | `id` UUID, `definition` référence épinglée, `props` objet de valeurs typées, `children` liste ordonnée. Seul un conteneur accepte des enfants. Chaque occurrence garde son UUID en cas de déplacement ou de renommage. |
| Définition | `scope` vaut global ou site, `key` est une clé du registre, `version` un entier strictement positif. La clé est résolue sous la portée du site destinataire à chaque écriture. Une définition globale est déclarée explicitement partageable. |
| Thème | Objet éventuellement vide ; pour 01, seules `accent` et `gap` sont prévues. Couleur hexadécimale #RRGGBB et espacement entier de 0 à 128 pixels CSS. Polices, logos, variantes et gestion de catalogue relèvent de 03. |
| Disposition | `base` obligatoire ; `tablet` et `mobile` facultatives. Base et surcharges acceptent `display` (stack ou grid), `columns` (entier de 1 à 12), `gap` (entier de 0 à 128). Defaults de base : stack, une colonne, espacement du thème ou zéro. Chaque surcharge hérite directement de base ; la modification d’une surcharge laisse l’autre intacte. La colonne est unique en mode stack après résolution. Les gestes canvas, coordonnées libres et superpositions relèvent de 05. |

Le noyau v1 reconnaît les définitions globales version 1 `container` (props : layout), `heading` (props : text et level entier de 1 à 6) et `text` (props : text). Le texte est du texte brut de 1 à 4 000 caractères. Le registre de référence peut être déclaré dans le code du socle ; identité, version et périmètre suffisent à 01. Les fonctionnalités de bibliothèque de 03 seront libres d’introduire de nouvelles définitions par leurs validateurs versionnés.

## Références et isolation

Pour autoriser ultérieurement des propriétés média et contenu sans créer de second CMS, la valeur d’un champ déclaré « référence » prend la forme décrite ci-dessous. Ce champ n’est accepté que par une définition qui le déclare et si une source locale de confiance peut l’autoriser pour le site. Le socle teste le contrat avec un résolveur et des ressources fictives pour deux sites. Tant qu’une ressource réelle n’a pas de source de résolution fiable, son ajout est refusé. Un site sans moteur peut créer et enregistrer du texte, des pages et des dispositions locales.

| Référence typée | Résolution |
|---|---|
| Média | `kind=media`, `ref_id` UUID opaque d’une référence centrale de média autorisée pour le Site. La résolution vérifie appartenance ou partage explicite et droit de réutilisation. |
| Contenu Wagtail avancé | `kind=wagtail_content`, `ref_id` UUID opaque d’une référence centrale scoped au Site. Ce descripteur côté serveur conserve l’instance, le type, l’identifiant éditorial et la révision source connue, éventuellement inconnue. La persistance du brouillon ne consulte pas le moteur. |

Un identifiant présent dans le JSON ne prouve aucun droit. Toute référence indisponible ou rattachée à un autre site donne le même diagnostic de validation borné, sans nom ni métadonnée de la ressource. Une version jadis valide dont la référence a disparu reste identifiable dans son instantané historique sous le contrôle des droits de lecture ; une nouvelle sauvegarde exige de résoudre ou corriger les références. Les sous-lots 03 et 06 devront livrer les résolveurs, formats et droits opérationnels de leurs ressources.

## Bornes et évolution

- Document limité à 1 048 576 octets JSON compact UTF-8, sans échappement des caractères Unicode ordinaires. Vérifier les limites d’entrée avant désérialisation sur tout futur endpoint et appliquer aussi la limite au service commun. Initialement 100 pages, 2 000 occurrences cumulées de sections et blocs, douze niveaux de blocs par section, douze niveaux de pages racine comprise. Ces seuils de départ sont à mesurer sur PostgreSQL dans la recette ; ils ne constituent pas des performances déjà qualifiées.
- UUID sous forme canonique ; aucune collision entre identifiants déclarés dans le document. Les références à une page sont résolues dans ce document. Un template copié ou un import accepté reçoit de nouveaux UUID d’occurrences et ses références internes sont remappées ensemble. Lors d’une modification ordinaire, les occurrences conservées gardent leurs identifiants. Des IDs d’occurrence identiques dans deux documents ne donnent aucun droit sur l’autre site : toute recherche de révision ou de ressource est bornée par le Site.
- Initialisation vierge : une page racine, aucune section, menus vides, thème vide. Le type et la version d’une définition sont indépendants de la version du schéma et du numéro de révision du brouillon. Types JSON exacts ; une valeur booléenne ne satisfait pas un entier. Refuser les valeurs numériques non finies, les champs inconnus et les clés dupliquées d’un JSON brut.
- Une version de schéma future reçoit une erreur de compatibilité. Une version historique reste intacte ; une conversion supportée produit un document candidat et une nouvelle révision après validation et comparaison de la base. Une révision incompatible ne peut pas être réenregistrée en perdant des champs. Aucune page Wagtail, entrée de menu ou version active n’est déduite du document enregistré.
- Recette de compatibilité : lire et recharger la fixture, modifier un titre et réordonner deux éléments en conservant leurs IDs, puis comparer l’ancienne révision octet pour octet après sérialisation canonique. Muter séparément parent/ID, portée de référence, version de schéma, propriété inconnue, type, cardinalité et profondeur. Vérifier le refus et l’absence de nouvelle tête ou révision partielle.
