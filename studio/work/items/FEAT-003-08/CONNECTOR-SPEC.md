# Contrat de lecture du fichier de design

**Opération proposée.** Recevoir un acteur Studio, un UUID de site et une remise du portail. Résoudre localement la remise et un profil de lecture administré pour le site. Le profil contient une référence de secret et les clés des fichiers ou branches explicitement autorisés pour ce site. Déléguer au connecteur uniquement la lecture de ce périmètre. La clé du lien remis par le graphiste ou l’accès personnel de l’agent dans Figma ne constituent pas cette autorisation. [Contrat de remise](../FEAT-003-07/ARCHITECTURE.md)

## Appels et résultat

Utiliser l’API REST v1 sur l’origine fixe HTTPS de l’API Figma. Pour la recette initiale, proposer un jeton de lecture géré côté serveur et le scope `file_content:read`. La rotation/remise en cause du profil intervient indépendamment du raccordement Wagtail. Une intégration OAuth pourra remplacer le mode de fourniture du jeton si l’exploitation le retient. [Authentification Figma](https://developers.figma.com/docs/rest-api/authentication/)

Lire le fichier par `GET /v1/files/{key}` avec une profondeur limitée pour obtenir la version et l’inventaire nécessaire. Pour un lien ciblé, limiter les résultats conservés au nœud autorisé et à ses descendants sélectionnés. Lire les sous-arbres sélectionnés en groupes bornés via `GET /v1/files/{key}/nodes`, avec `ids` et la version exacte de l’inventaire. Convertir le sélecteur canonique de remise au format d’identifiant de l’API. Un nœud demandé peut être absent ou nul malgré un succès HTTP. Écarter les nœuds annexes hors sélection. [Endpoints des fichiers et des nœuds](https://developers.figma.com/docs/rest-api/file-endpoints/)

Retourner un résultat typé contenant version, date de lecture, frames et nœuds retenus, relations parent/enfant, styles observés, valeurs visibles, références de composants/variantes et diagnostics. Conserver seulement les éléments nécessaires à la revue. Les variables nommées peuvent rester non résolues. Le service Variables local requiert un accès spécifique et un périmètre supplémentaire ; la V1 se fonde sur les valeurs accessibles dans le fichier. Les médias restent des références à rapprocher des médias autorisés du site. Aucune URL d’asset ou de miniature fournie par le document n’est suivie dans cette version. [Disponibilité des variables](https://developers.figma.com/docs/rest-api/variables-endpoints/)

## Bornes proposées pour la qualification

Budget par analyse explicite à éprouver sur fixtures : un inventaire, au plus quatre groupes de lecture de nœuds, huit frames sélectionnées, 2 000 nœuds normalisés, 8 Mio de réponses décodées cumulées et 30 secondes au total. Vérifier schéma et types au fil de la lecture, profondeur et taille avant conservation. Un budget atteint donne une analyse incomplète et propose de réduire la sélection. Une analyse tronquée ne devient pas silencieusement applicable. Les paramètres `depth` et `ids` limitent la lecture. L’arbre s’explore par sélection ; il n’existe pas de promesse de pagination universelle des couches.

| Situation | Résultat et reprise |
|---|---|
| Profil ou scope absent ; fichier absent ou interdit | Diagnostic minimal. Fermer l’accès aux résultats devenus inéligibles et demander une vérification de configuration ou de partage à l’équipe habilitée. |
| Délai, indisponibilité, réponse incomplète ou non reconnue | Échec borné avec identifiant de tentative local ; possibilité de relancer explicitement. Pas de mutation du brouillon. |
| Limite fournisseur | Respecter le délai indiqué par `Retry-After`. À défaut de valeur exploitable, appliquer un délai local borné. Présenter la reprise différée et mutualiser les appels d’une même analyse. Les quotas varient selon le siège, le plan et l’endpoint. [Limites de l’API](https://developers.figma.com/docs/rest-api/rate-limits/) |
| Profil ou source modifié, nouvelle version Figma | Marquer la comparaison à reprendre. Confirmer une version et un choix renouvelés avant création de révision. |
| Retour répété, résultat local incertain | Relire la tentative et son résultat durable par clé de demande. Réessayer une lecture n’autorise jamais à dupliquer une décision d’application. |

La validation finale effectue une lecture fraîche bornée de l’accès et de la dernière version, hors transaction de composition. À son retour, recontrôler en transaction la remise, le mandat, le profil, le catalogue et la tête locale. L’API de lecture constate une version à un instant donné ; une modification Figma ultérieure ne modifie pas le document Studio enregistré. Aucun webhook, écriture fournisseur ou traitement au simple dépôt. Journaux avec identifiants internes, durée, compteurs et classe de résultat. Vérifier le comportement sur simulateur puis sur un fichier dédié à la recette avant de déclarer le connecteur opérationnel.
