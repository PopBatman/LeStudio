# Persistance et interface du socle

## Stockage retenu pour la réalisation proposée

Dans la base PostgreSQL du Studio, une révision de composition immuable porte un UUID, une FK Site, un numéro croissant propre au site, un parent facultatif, une date serveur, l’auteur et un instantané JSON de schéma versionné. Identifiant de la révision et version du schéma répondent à deux questions différentes. La première révision porte la provenance (vierge, modèle/version ou proposition Figma acceptée). Les suivantes héritent de cette origine par la lignée. L’auteur provient de la session de service, avec conservation de l’historique si le compte est désactivé ; définir la FK nullable SET_NULL à la suppression du compte.

Pour matérialiser la tête du parent FEAT-003 sans pointeur à synchroniser, retenir la révision de plus grand numéro du site. Contrainte unique (site, numéro) et index correspondant ; aucune tête s’il n’existe pas de ligne. Le numéro est positif. Révision 1 sans parent, toute autre révision liée à la précédente du même site. La FK Site protégée évite une destruction implicite de l’historique ; traiter la politique de purge explicitement dans les opérations de conservation. Aucun miroir de composition dans la base Wagtail. Une migration additive crée le stockage vide, y compris pour les sites déjà raccordés.

## Contrat de service interne proposé

| Opération | Préconditions et résultat |
|---|---|
| lire_brouillon(acteur, site) | Mandat Site lecture/gestion. Retourne absence ou enveloppe de la tête. Aucun enregistrement à la lecture. |
| lire_revision(acteur, site, revision_id) | Même filtre, clé composite de recherche site + UUID. Retourne cette révision, y compris si une autre est devenue la tête. Contrat destiné aussi à FEAT-004. |
| creer_brouillon(acteur, site, origine, document) | Mandat gestion, tête absente, provenance autorisée. Résultat avec UUID de révision, numéro 1, parent nul, horodatage, schéma, provenance et document relisibles. Une création répétée reçoit un conflit et peut relire la tête. |
| enregistrer_brouillon(acteur, site, revision_de_base, document) | Gestion, UUID de base obligatoire correspondant à la tête de ce site. Même enveloppe, nouveau numéro et UUID, parent égal à la base. La provenance initiale est conservée. |

Pour un document historique dont le schéma est inconnu du lecteur, retourner les métadonnées de la révision autorisée et un diagnostic de compatibilité. L’éditeur ne reçoit pas le corps brut et ne peut pas sauvegarder en perdant des champs. L’instantané reste conservé pour une future conversion explicite.

Les noms de fonctions sont indicatifs. Les commandes reçoivent le site et l’acteur séparément du document. Les futurs adaptateurs des éditeurs structurés et visuels appellent ces mêmes règles. Pour les origines externes, employer une référence stable vérifiée par le fournisseur autorisé ; en son absence, refuser la création depuis cette origine. Les tests de contrat peuvent substituer un fournisseur fictif. N’accepter ni création d’une proposition Figma ni accès au fichier fournisseur dans ce service.

## Transaction et reprise

1. Borner la taille de l’entrée et valider sa forme. Dans une transaction PostgreSQL, contrôler les habilitations actuelles en verrouillant dans un ordre partagé avec les services de gestion le compte, l’adhésion au groupe, le site puis le mandat Site. Pour l’adhésion, couvrir la ligne d’association qui peut être retirée. Conserver une durée de transaction courte, sans appel distant.
2. Verrouiller le site même lorsqu’aucun brouillon n’existe encore. Relire la dernière révision pour ce site après le verrou, comparer à la base fournie ou à l’absence attendue. Contrôler la propriété effective des références locales, avec cohérence transactionnelle pour les références mutables.
3. Insérer l’instantané et ses métadonnées ensemble. En cas de panne, tout est annulé. Deux créations concurrentes ou deux modifications de la même base ne peuvent produire deux révisions gagnantes. Après une réponse perdue, réessayer avec la même précondition retourne un conflit si la première écriture a abouti ; la lecture de la tête permet la réconciliation, en conservant la saisie de l’appelant.
4. Distinguer absence de brouillon lors d’une lecture autorisée, site/révision introuvable ou hors mandat, écriture interdite sur site lisible, base obsolète, document invalide et schéma incompatible. Pour une base étrangère ou périmée, communiquer uniquement la tête du site déjà autorisé. Retourner un chemin de champ local et un motif borné dans les erreurs de validation. Aucune fusion silencieuse.

Les tests concurrents utilisent des connexions distinctes sur PostgreSQL et vérifient l’état après commit. SQLite en mémoire peut couvrir la validation pure et le contrat séquentiel. La migration est à éprouver depuis une base Studio contenant des fiches et des liaisons existantes.
