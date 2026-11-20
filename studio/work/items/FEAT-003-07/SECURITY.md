# Accès, protection et cycle de vie

## Autorisations par action

| Action | Autorité relue côté serveur |
|---|---|
| Créer, révoquer et remplacer un lien | Compte actif, groupe Opérateurs Studio et mandat de gestion sur le Site sélectionné. Identifier le site autorisé à chaque commande, même si l’opérateur possède également un mandat Client. La révocation est idempotente. |
| Consulter l’activité, les versions et les détails | Mandat Site en lecture ou gestion au moment de la requête. Restreindre la requête de liste, les compteurs, pages suivantes et détails à ce même périmètre. Un droit Client seul ou un autre site ne révèle aucun résultat de la fiche demandée. |
| Déposer et ouvrir le reçu | Capacité de portail valide pour l’invitation, soumise à expiration et révocation. La page publique présente le formulaire ou le reçu de son dépôt, avec une désignation minimale du projet si nécessaire. Elle ne présente ni annuaire, ni listes de sites, ni liens vers les autres soumissions ou applications privées. |
| Utiliser une source au lot 08 | Même contrôle de site sur l’objet et mandat de gestion pour prendre une décision d’analyse. L’accès à la ressource Figma est accordé séparément dans le prochain lot. Un graphiste invité ne reçoit aucun compte ou droit de rédaction Studio/Wagtail. |

L’archivage administratif du Client et les droits de ses Sites gardent la sémantique du registre existant. Un mandat retiré ferme l’accès de la personne à la liste et au détail. Pour fermer également un lien de partage déjà émis au nom du site, un gestionnaire le révoque explicitement. [Procédure du registre](../../../docs/REGISTRE.md)

## Secret et surface publique

Proposition de transport à qualifier en navigateur et dans les journaux du déploiement.

- Tirer au moins 32 octets aléatoires via la bibliothèque cryptographique de la plateforme, transmettre une représentation opaque et n’enregistrer que son empreinte unique. Le lien s’affiche une seule fois au gestionnaire. Une perte conduit à révoquer puis réémettre. La copie et la transmission au graphiste sont des gestes du gestionnaire via son canal autorisé.
- Une adresse d’invitation à fragment, illustrée par `/depot/#<secret>`, charge un chemin commun. Un script local minimal efface le fragment de l’entrée courante de l’historique puis transmet le secret par POST de même origine sur HTTPS, avec la protection CSRF Django. Aucun jeton dans le chemin ni la chaîne de requête. Une saisie manuelle du code sur le même formulaire permet un échange sans JavaScript. L’UI opérateur rend le code sélectionnable lors de l’émission initiale.
- Après échange, émettre une capacité de portail opaque dans un cookie distinct, HttpOnly, Secure en exploitation, SameSite strict et limité au chemin du portail. Stocker son empreinte côté serveur et borner sa validité à la première échéance entre l’invitation et sa propre durée courte. Chaque soumission recontrôle l’invitation courante. Les routes publiques ignorent toute session d’administration et les routes privées ignorent la capacité du portail. Un GET, y compris une prélecture de messagerie, ne crée aucun dépôt et ne consomme pas l’invitation.
- Empêcher la mise en cache des réponses sensibles, supprimer le référent sortant et servir localement styles et scripts indispensables. Configurer les journaux applicatifs, HTTP et de supervision pour exclure corps, cookies, fragments, liens Figma, commentaires et réponses d’émission. Vérifier avec des marqueurs fictifs dans la recette, y compris les erreurs. Limiter les traces aux événements nécessaires, date, référence interne non secrète et résultat borné.
- Servir la même réponse générique pour une invitation inconnue, expirée ou révoquée. Préserver les messages de champ précis pour la personne déjà autorisée. La page publique doit rester utilisable à 320 px, au clavier, sur erreur et après expiration en cours de saisie.

## Entrées et limites proposées pour la première qualification

| Paramètre | Valeur de départ et contrôle |
|---|---|
| Invitation | 7 jours par défaut à compter de l’émission, échéance serveur exacte. L’échange d’un secret et l’envoi de versions ne prolongent pas l’échéance. |
| URL Figma | 2 048 caractères maximum. Lire avec un parseur d’URL. Exiger HTTPS, hôte exact `figma.com` ou `www.figma.com`, chemin de conception `/design/<clé>/…` ou ancien chemin `/file/<clé>/…`. Refuser identifiants dans l’autorité, port non standard et caractères de contrôle. Construire depuis les champs validés une référence canonique au fichier et, s’il est fourni et valide, au nœud. Écarter paramètres de partage/suivi, fragment et nom libre du fichier lors de la conservation. Signaler un format ou un sélecteur de nœud incompatible et laisser corriger la saisie. |
| Commentaire et médias | Commentaire texte brut facultatif de 2 000 caractères maximum. Aucune pièce jointe ou archive. Afficher le texte échappé. La présence d’une seule déclinaison responsive permet de déposer. |
| Dépôts | Proposer 20 nouvelles versions par invitation et 5 nouvelles soumissions sur 10 minutes par invitation. Une reprise idempotente déjà autorisée restitue son reçu sans consommer un second quota. À saturation, expliquer le délai ou inviter à contacter le gestionnaire. |
| Échange initial | Limiter les tentatives d’échange en amont du traitement coûteux, avec pour essai 10 par 10 minutes et par provenance réseau pseudonymisée. Compteur partagé entre processus, durée de vie bornée, tenue compte de l’origine fiable réellement disponible dans le déploiement. Tester les effets de bureaux utilisant une adresse commune. |
| Consultation | Pages de 20 soumissions, tri et curseur documentés dans l’architecture. Le changement de page relit les droits. Aucun nombre de résultats calculé avant filtrage par site. |

Le dépôt valide la forme d’une référence. Un fichier privé, renommé ou inaccessible peut avoir une adresse de forme valide. Le reçu atteste la remise du lien et la date. La lecture de Figma, les droits fournisseur et les alertes de correspondance relèvent du lot 08. Les seuils ci-dessus sont des hypothèses de dimensionnement à mesurer sur données fictives.

## Conservation et effacement

Proposer 90 jours à compter de chaque **dépôt** pour conserver lien et commentaire. L’expiration de l’invitation ferme les nouvelles remises. Elle n’altère pas la date de purge de chaque version. Dans la même intervention d’effacement, retirer le lien et le commentaire des dépôts et des projections éventuelles, neutraliser l’accès du lot 08, puis garder uniquement les références minimales justifiées pour l’audit ou les versions déjà produites. Un reçu après effacement ne doit pas redonner accès au contenu. Une purge répétée aboutit au même état. Conserver l’ordre historique sans réutiliser de numéro de version. Purger les secrets dérivés et capacités expirées dès la fin de leur utilité. Le graphiste dispose dans le portail de la notice et du contact vérifié chargé des demandes.

Le responsable du traitement fixe le délai applicable, la notice, le canal de contact, les personnes habilitées et le traitement des copies restaurées avant collecte réelle. Documenter la rotation des sauvegardes et rejouer les effacements avant remise en service d’une restauration. Vérifier sur deux sites fictifs la disparition des contenus effacés dans la fiche, le signalement et la lecture par 08, ainsi que la conservation des dépôts voisins. [Procédure déjà prévue par FEAT-002](../FEAT-002/PROTECTION-DONNEES.md)

## Mise en service à qualifier

L’image Studio actuelle limite les hôtes à la boucle locale et Compose publie le service sur le poste. La recette locale doit couvrir l’invitation de bout en bout sur une origine de test avant de promettre un accès Internet au graphiste. Pour la mise en service externe, définir une origine de portail HTTPS configurée explicitement, ses hôtes admis, ses cookies, la protection des journaux et la liste de routes publiques. Générer les liens à partir de cette origine configurée. Une éventuelle exposition doit préserver la confidentialité de la console et des moteurs avec les contrôles de déploiement appropriés. Cette qualification est distincte du prototypage sur données fictives. [Paramètres actuels](../../../central/settings.py) · [Exposition locale](../../../compose.yaml)
