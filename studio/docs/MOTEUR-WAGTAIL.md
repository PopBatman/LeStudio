# Raccorder un moteur Wagtail au Studio local

Le registre peut contenir une fiche Site sans domaine et sans moteur. Le raccordement se fait depuis un terminal d’administration de confiance. Choisir l’identifiant d’un opérateur actif ayant un mandat de gestion sur le site. Un opérateur ayant seulement la lecture peut consulter la dernière observation enregistrée.

## Préparer l’instance et le profil

Démarrer une instance du moteur commun avec ses propres identifiants PostgreSQL, base, médias, clé Django, UUID d’instance et UUID de site Studio. Utiliser le digest de l’image qualifiée, le marqueur de référence du site et un frontal HTTPS qui exige un certificat client de lecture propre à cette instance. Réserver l’accès au port applicatif du moteur au frontal privé. Le [laboratoire local](../engine/lab/README.md) fournit un exemple pour deux sites indépendants.

Côté Studio, monter le fichier des profils et les certificats en lecture seule dans le conteneur web. Définir la variable d’environnement du service `STUDIO_ENGINE_PROFILES` avec le chemin absolu du fichier JSON monté. Relier le service au réseau de gestion autorisé. Une surcharge Compose locale peut fournir ces montages et ce réseau. Les profils, les clés et les certificats d’exploitation sont provisionnés séparément du dépôt. Le fichier est un objet indexé par alias. Chaque entrée contient les champs suivants.

| Champs du profil | Valeur attendue |
|---|---|
| `site_id`, `instance_id` | UUID connus hors bande du site du registre et de l’instance. |
| `origin` | Origine HTTPS du frontal, avec le port si nécessaire. Son nom doit correspondre au certificat serveur. |
| `ca`, `cert`, `key` | Chemins absolus dans le conteneur Studio vers la confiance serveur, le certificat client et sa clé de service. |
| `engine_version`, `image_digest` | Version du moteur autorisée et digest obtenu au lancement de l’image, sous la forme `sha256:` suivie de 64 caractères hexadécimaux minuscules. |
| `marker` | Texte de référence attendu dans le paragraphe de la page Wagtail publiée. |

## Vérifier et consulter

Depuis `studio/`, remplacer les arguments en majuscules par les valeurs du site.

```bash
docker compose exec -T web python manage.py raccordement verifier OPERATEUR UUID_SITE ALIAS
docker compose exec -T web python manage.py raccordement etat OPERATEUR UUID_SITE
```

La vérification effectue quatre GET, contrôle les deux UUID, les versions, la disponibilité et le rendu, puis enregistre la confirmation dans Studio. La lecture de l’état utilise uniquement la base centrale. Dans le JSON, `confirmed.at` date le dernier succès ; `status` et `attempt` décrivent le dernier contrôle. Une vérification infructueuse renvoie un code de sortie d’échec et préserve la confirmation antérieure. Reprendre la commande après correction du profil ou de la disponibilité. Une tentative déjà active expire avant reprise.

Pour une rotation, autoriser temporairement le nouveau certificat en plus de l’ancien, mettre à jour le profil, vérifier la liaison puis retirer l’ancien certificat. Une copie restaurée et démarrée en parallèle nécessite une identité et des justificatifs propres. [Politique de sécurité](../work/items/ARCH-002/SECURITY.md)

## Activer la lecture de la publication d’un article

Le moteur équipé de FEAT-003-06 fournit le type de page **Article**. Lors du déploiement de cette image, appliquer ses migrations Django. Dans l’administration Wagtail, identifier le **site Wagtail** dont la racine contient les articles autorisés. Configurer `EDITORIAL_WAGTAIL_SITE_ID` avec la clé numérique de cet enregistrement Site. L’UUID de la fiche Studio, le numéro de la page racine et le numéro d’un article ont chacun un autre usage.

Le frontal privé du moteur doit accepter la lecture éditoriale versionnée avec le même certificat client que le diagnostic. Consigner le digest de la nouvelle image qualifiée dans le profil de cette instance et relancer la vérification de raccordement. Un moteur configuré pour cette lecture annonce `editorial.published.v1`. Les moteurs antérieurs continuent d’assurer le diagnostic ARCH-002. Sur une fiche nouvellement créée, le raccordement confirmé et cette capacité sont nécessaires pour vérifier un article.

Le champ facultatif `admin_url` du profil désigne l’entrée de l’administration accessible **depuis le navigateur de l’opérateur**. Utiliser l’adresse effective de ce site. Un port local sur `127.0.0.1` suppose que le navigateur a accès au service sur sa propre machine. La session humaine et les permissions de publication se gèrent dans Wagtail. [Parcours opérateur](BROUILLONS.md#modifier-une-page-qui-référence-un-article-wagtail)

## Examiner une révision du site

Dans **Mes sites**, ouvrir la fiche puis **Aperçu du site**. Choisir la révision enregistrée et sa page, puis **Préparer l’aperçu**. Depuis l’atelier ou le canvas, le lien d’aperçu ouvre la révision indiquée dans un autre onglet et préserve la saisie en cours. Pour examiner cette saisie, enregistrer d’abord les modifications.

Le sélecteur Bureau, Tablette ou Mobile conserve la révision. **Provenance du rendu** indique l’instance Wagtail et les références effectivement utilisées. **Comparer les révisions** permet de revoir la même page dans la révision précédente. Le message « Version active inconnue » indique que Studio ne dispose pas encore d’une preuve d’application de la composition. Une nouvelle sauvegarde est signalée séparément.

Le reçu personnel expire dix minutes après le début de la préparation. Fermer l’aperçu ou se déconnecter révoque son accès. Une perte de connexion, un changement de raccordement ou le retrait d’une ressource peuvent suspendre la consultation. Après correction, utiliser **Repréparer**. Pour un moteur qui retourne un diagnostic de compatibilité, vérifier le digest du profil, la capacité `preview.v1` et l’autorisation du certificat sur la passerelle. [Activation par instance](../engine/lab/README.md#autoriser-le-rendu-privé-dune-composition-studio)

Les blocs sont rendus par les gabarits internes. Les liens de la page rendue sont neutralisés pour cette lecture privée. Le sélecteur **Pages** de Studio permet de naviguer entre les pages de la révision. Les articles doivent être publics sur la racine Wagtail configurée et toujours à la révision épinglée. Les inclusions éditoriales ou médias hors du périmètre pris en charge sont signalés lors de la préparation.

### Sélectionner un bloc dans le canvas Wagtail

Dans **Mes sites**, ouvrir la fiche du site puis **Canvas Wagtail**. Choisir une révision enregistrée et une page, puis **Afficher le rendu**. Le site utilise le même raccordement et les mêmes droits d’aperçu privé que pour FEAT-004.

Cliquer sur un bloc dans la page ou activer son bouton dans **Navigation → Calques** au clavier. L’**Inspecteur** indique le composant et l’identifiant de cette occurrence. Deux titres utilisant la même définition restent sélectionnables séparément. Le sélecteur **Vue** permet de comparer les largeurs. **Aperçu de référence** ouvre le document Wagtail du même reçu.

**Actualiser le rendu** redemande la révision affichée. Si une sauvegarde plus récente existe, **Ouvrir la dernière sauvegarde** permet de la consulter. Lorsque le moteur est indisponible, **Lire la structure** donne accès aux calques du brouillon pour lequel l’opérateur dispose toujours du droit de lecture. Le gestionnaire peut composer la dernière révision avec les commandes ci-dessous.

### Composer dans le canvas

Avec le mandat de gestion, ouvrir **Canvas Wagtail**, choisir la dernière révision et la page, puis **Afficher le rendu**. Double-cliquer sur un texte pour le modifier. Pour ajouter un composant au rendu, ouvrir **Insérer dans la page rendue**, choisir sa version et faire glisser **Placer dans la page** jusqu’à la destination. On peut aussi activer ce bouton puis toucher la destination.

**Modifier la page** ouvre la vue de travail. La bibliothèque permet de rechercher un composant ou de filtrer par catégorie. Au clavier, choisir le composant, sélectionner la destination puis activer **Placer ici**. Dans une page vierge, **Ajouter une section** crée le premier emplacement. Les calques permettent de retrouver une occurrence, et l’inspecteur de déplacer, dupliquer ou supprimer le bloc. **Annuler** et **Rétablir** parcourent les gestes de l’onglet. Confirmer la saisie dans la page avant d’enregistrer.

**Enregistrer** crée une révision de brouillon pour l’ensemble des gestes et prépare son rendu Wagtail privé. Si le rendu échoue, relever le numéro de révision confirmé puis relancer son affichage. En cas de réponse perdue, utiliser **Réessayer la sauvegarde** dans le même onglet. En cas de conflit, **Examiner la dernière sauvegarde** ouvre la version concurrente pendant que la liste des gestes locaux reste disponible. La publication du site reste une opération distincte.

### Comparer une page importée à sa frame Figma

Avec un mandat de gestion, ouvrir **Canvas Wagtail**, sélectionner la page importée puis **Comparer à la référence Figma**. Depuis une remise confirmée, le lien de la page ouvre aussi ce canvas. Le site peut contenir à la fois des pages sur modèle et des pages Figma. La comparaison est proposée sur les pages dont l’import est attesté.

1. Choisir **Bureau**, **Tablette** ou **Mobile**. Dans **Provenance et export PNG**, vérifier la remise, la version du fichier et la frame. Joindre son export PNG statique (6 Mio maximum), examiner l’image et cocher l’attestation avant de confirmer. Un export haute densité garde les proportions de la frame. Une seule frame suffit.
2. Cliquer sur **Préparer le rendu Wagtail** si nécessaire. Sur ordinateur, l’export et le rendu apparaissent côte à côte. Sur mobile, utiliser **Référence** et **Rendu Wagtail**. Un format sans frame permet d’inspecter le site et indique que la référence manque.
3. Dans **Écarts de la page**, choisir la page entière ou une occurrence, puis **Examiner cet élément**. Sélectionner **À corriger**, **Accepter cet écart** ou **Aucun écart constaté**. Expliquer l’écart, vérifier le format et la révision, cocher la confirmation et **Consigner la décision**.
4. **Modifier dans l’atelier** ouvre l’éditeur habituel sur l’occurrence choisie. Après enregistrement, ouvrir de nouveau la comparaison. Une nouvelle révision ou un export remplacé demande un nouvel examen. **Historique des décisions** conserve le motif, l’auteur et la preuve examinée pendant la durée autorisée de la remise.

Après expiration d’un reçu, relancer la préparation du rendu. Si la remise a été effacée, sa référence privée et ses décisions sont retirées et la page du brouillon reste disponible. Le lecteur du site conserve son parcours de consultation du canvas. Une décision visuelle ne publie pas le site.
