# Habilitations proposées pour le Studio privé

Toute consultation ou modification métier requiert le compte actif et le groupe « Opérateurs Studio » de FEAT-001. Un second contrôle porte sur l’action et l’objet. Le type de client, un rôle de contact, le statut staff et le statut superutilisateur Django ne valent pas habilitation sur le portefeuille.

| Capacité explicite | Droits proposés |
|---|---|
| Opérateur seul | Ouvrir l’espace de travail. Les recherches et listes du registre retournent uniquement les objets autorisés, y compris zéro résultat. |
| Créer un client | Capacité distincte attribuée nominativement, notamment au propriétaire. Créer une fiche donne à son auteur un mandat de gestion sur cette nouvelle fiche, dans la même transaction. |
| Lecture client | Consulter les renseignements du client et ses contacts. Sur la fiche, afficher seulement les sites sur lesquels le même acteur a un mandat. |
| Gestion client | Inclut la lecture. Modifier le client, créer ou modifier ses contacts, archiver ou réactiver le client et créer un site sur un client actif. À la création du site, attribuer explicitement un mandat de gestion au créateur. |
| Lecture site | Consulter ce site à partir de Mes sites. Si le client n’est pas lisible, l’interface omet son identité, ses liens et ses contacts. |
| Gestion site | Inclut la lecture. Modifier les champs de ce site. Le droit ne s’étend ni au client ni aux autres sites, même en présence d’un domaine ou d’un serveur commun. |

**Attribution et retrait.** Proposition pour le premier lot : le propriétaire désigne les opérateurs et leurs capacités. Un administrateur de confiance les attribue par une commande de maintenance locale explicite, en ciblant le compte, l’action et l’UUID de la ressource pour les mandats objet. Le droit de créer un client se donne séparément. Une opération répétée conserve la même habilitation. Une opération sur une cible inconnue échoue sans changement. Les opérateurs existants démarrent avec zéro mandat métier. Le propriétaire peut ainsi ouvrir le premier client sans distribuer un accès universel. La délégation autonome des droits par un gestionnaire de fiche et une interface graphique d’administration sont reportées.

**Contrôles à chaque requête.** Appliquer d’abord la portée autorisée, puis rechercher, compter, trier et paginer. Donner le même résultat pour un objet inexistant ou invisible (404). Pour un objet visible, signaler l’action interdite par 403. Une requête anonyme ou expirée suit FEAT-001. Protéger les écritures contre les demandes sans jeton CSRF. Les liens parent/enfant doivent correspondre aux clés enregistrées, y compris après une navigation directe. Refuser une substitution du parent à la création ou en édition. Le domaine ne sert pas de clé d’accès.

**Archive et concurrence.** La gestion du client permet l’archivage administratif. L’écran explique l’effet et demande confirmation. Le service préserve tous les mandats et tous les sites. L’opérateur habilité à un site peut toujours le retrouver et le gérer pendant l’archivage du client. Revérifier le droit, l’état et la version au moment de l’écriture. En cas de conflit, retourner une explication et proposer de recharger la fiche. Une erreur de validation rend le formulaire et ses valeurs utiles sans exposer de données d’un autre périmètre.

**Données et traces.** Limiter messages, journaux et preuves au strict nécessaire. Les requêtes de recherche susceptibles de contenir des coordonnées sont exclues des journaux d’URL. Un contrôle des habilitations et une procédure d’intervention autorisée précèdent l’utilisation de données personnelles réelles. [Procédure dédiée](PROTECTION-DONNEES.md)

**Vérifications prévues.** Croiser deux clients, deux sites frères, un opérateur sans mandat, un lecteur de site et un gestionnaire client. Vérifier accès directs, services, erreurs, compteurs, recherches, propositions de doublons, sélection du parent, archivage et révocation en cours de session. Vérifier aussi que les privilèges Django seuls n’ajoutent aucun résultat et que les fiches conservent leurs rattachements après un refus.
