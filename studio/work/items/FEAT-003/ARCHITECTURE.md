# Contrats de l’atelier

## Point d’entrée dans la fiche Site

La vue site_detail filtre déjà la fiche par sites(request.user), relit la liaison par inspect_link et transmet au gabarit la projection connection_panel filtrée par can_manage. Le panneau « Moteur Wagtail » conserve la dernière confirmation et la dernière tentative avec leurs dates distinctes. Une version Wagtail, un profil et un UUID d’instance décrivent le dernier succès. Ils ne permettent de déduire ni une version de composition appliquée, ni une URL de navigateur. Le panneau Atelier proposé consulte les métadonnées du brouillon du même Site. Aucune consultation ne crée de brouillon ni ne déclenche de sonde. Proposition à éprouver dans le premier incrément : une fiche sans liaison confirmée permet le travail local ; une liaison en échec conserve le brouillon.

Sources : [vue existante](../../../registre/views.py), [projection de la liaison](../../../registre/raccordement.py), [fiche exécutée](../../../templates/registre/site.html), [service central](../../../raccordement/services.py), [contrat Studio](../../../docs/ARCHITECTURE-CONTRACTS.md).

## Modèle proposé pour FEAT-003-01

Une tête de brouillon par Site pointe sur une révision de composition du Studio central. Une révision conserve son identifiant, son site, sa révision parente, sa version de schéma, sa date, son auteur et le document validé. L’origine du premier document (vierge, modèle et sa version, sélection d’une analyse Figma) reste une information de provenance. Les trois parcours produisent le même document. Une migration additive doit laisser une fiche ancienne sans tête de brouillon.

| Partie du document | Identité et invariants à valider à chaque écriture |
|---|---|
| Pages | Identifiants internes stables, parent éventuel, ordre entre pairs, titre et segment de chemin. Racine valide, parents du même site, unicité des chemins et absence de cycle. |
| Menus | Identités propres au menu et à ses entrées. Arbres ordonnés indépendants des pages, cible interne par ID ou externe autorisée, visibilité par format. Un retrait de page signale les entrées affectées. |
| Sections, conteneurs et éléments | Identifiants stables, ordre des enfants, type et version du composant, propriétés typées. Références de composants globales ou du site. Les déplacements conservent l’identité. |
| Présentation | Palette, polices, espacements et logo propres au site. Variantes des composants, règles de flux (grille/flex) et placements libres bornés avec coordonnées, dimensions et ordre de superposition. Les surcharges tablette/mobile héritent des valeurs de base et sont modifiables séparément. |
| Contenu | Valeurs simples appartenant au brouillon Studio. Pour un contenu avancé, référence portée par le site et l’instance, type, identifiant éditorial, révision source si connue. Une référence de média exige une ressource autorisée pour le site. |

La lecture restitue le document et sa révision. Une écriture contient le site résolu côté serveur, la révision de base et les modifications. Les deux éditeurs soumettent au même service de validation. Dans une transaction, recontrôler le droit de gestion, comparer la tête à la révision de base, vérifier toutes les références puis enregistrer révision et tête ensemble. La création initiale est également conditionnelle. Deux onglets partant de la même révision obtiennent un seul nouvel enregistrement ; le second conserve sa saisie et reçoit un conflit permettant de recharger et de reprendre. Une répétition de la même demande doit permettre de retrouver le résultat ou de signaler la révision avancée sans doubler ses effets. Un schéma plus récent ou un composant incompatible exige une mise à niveau explicite avant réenregistrement.

La version de brouillon courante et ses révisions antérieures sont centrales. La version **active appliquée** et la **précédente appliquée** ne pourront être affichées comme telles qu’avec une attestation d’application du moteur. En leur absence, les afficher comme inconnues ou indisponibles. FEAT-004 consommera une révision explicite pour l’aperçu. FEAT-005 portera validation distante, confirmation d’application, historique de publication et restauration. Les quatre lectures ARCH-002 n’offrent pas ces opérations.

## Contrats et points à qualifier dans les sous-lots

| Sous-lot | Contrat proposé et vérification de passage |
|---|---|
| 01 · Socle | Choisir le stockage concret des révisions, la taille maximale du document et les règles de compatibilité après mesure. Relire une même révision sur les deux surfaces. Tester écriture concurrente, reprise et refus inter-site sur PostgreSQL. |
| 02 · Pages et menus | Une commande décrit le déplacement, le renommage ou la suppression par ID stable. Déterminer la normalisation des chemins et la politique pour les entrées invalides. Montrer la liste des liens affectés avant résolution manuelle. |
| 03 · Bibliothèque | Un bloc épingle un type, une origine, une version et des propriétés validées. Premier catalogue proposé : conteneur, titre, texte court, image, bouton. Une promotion crée une version globale revue et expurgée des ressources du client. Vérifier que les anciens sites conservent leur version. |
| 04 · Éditeur structuré | Les formulaires et commandes d’ordre lisent et modifient le modèle 01. Un modèle de départ est copié avec des IDs locaux. La voie Figma exige une proposition validée du 08. Tester annulation, erreurs de champ et rechargement. |
| 05 · Canvas | La sélection vise les mêmes IDs que l’arborescence. Déplacement, redimensionnement et inspecteur traduisent un geste ou une commande clavier en modification du même document. Qualifier aux trois largeurs l’isolation des surcharges, les débordements, le volume d’éléments et le temps de réponse. |
| 06 · Contenus | Studio porte titre, texte court, image autorisée et bouton au stade de brouillon. Wagtail garde les articles, leurs droits et leurs révisions éditoriales. L’API ARCH-002 ne lit pas la révision d’un article. Qualifier le contrat de lecture séparé avant toute comparaison effective. En cas de révision source indisponible ou divergente, marquer la référence à vérifier et préserver la saisie. |
| 07 · Dépôt | Invitation temporaire → soumissions versionnées d’un lien Figma avec commentaire facultatif → notification interne au bon opérateur. Une seule déclinaison suffit. Chaque dépôt reste associé à une invitation et à son site même après révocation. Qualifier durée de conservation et effacement. |
| 08 · Analyse | Analyse explicite en lecture d’une soumission autorisée. Conserver source/version accessibles, correspondances de composants, incertitudes, vues absentes et problèmes de droits. L’opérateur accepte ou rejette des éléments, puis valide une révision de brouillon via le service 01. Rejouer la même validation ne duplique pas la composition. Vérifier les permissions et volumes réels du fournisseur sur une ressource de test autorisée. |

Les décisions d’implémentation de chaque tranche seront vérifiées dans sa propre mission. Un accès au connecteur de conception dans un outil de travail ne constitue pas un droit accessible au futur serveur Studio.
