# Contrat proposé entre Studio et le moteur

## Composants et persistance

Conserver le registre FEAT-002 comme source du site attendu. Placer le code moteur sous un répertoire distinct proposé `studio/engine/`, avec ses réglages Django, sa distribution verrouillée, son image et ses migrations Wagtail. Démarrer deux projets Compose de démonstration depuis la même image identifiée par son digest. Chacun reçoit sa base PostgreSQL dédiée, son rôle, son volume de médias, ses réglages et son identité de service. Les éditeurs et leurs sessions appartiennent à la base du site. Le navigateur de l’opérateur et le compte PostgreSQL de Studio n’administrent pas ces instances.

Créer côté central une relation optionnelle vers `registre.Site`. Une liaison confirmée porte un site unique, un UUID d’instance unique, une référence de profil administré, les versions observées et l’heure de la dernière confirmation. Conserver séparément le résultat de la dernière tentative (horodatage UTC, identifiant de tentative, état, code de diagnostic). L’état courant présenté distingue la dernière confirmation de la dernière tentative. L’absence de ligne est l’état initial. La migration centrale est additive et ne lie aucun site existant.

## Lectures API v1 proposées

Protocole HTTPS interne authentifié par mTLS, sous une origine fixe du profil. Toutes les réponses JSON réussies portent `site_id` et `instance_id` (UUID). Le client compare chaque paire aux deux identités préprovisionnées. Les versions de contrat et d’image sont distinctes de la version Wagtail. Ces routes sont à construire dans le projet moteur.

| Route GET | Réponse attendue |
|---|---|
| `/internal/identity` | HTTP 200, JSON avec la paire d’UUID et `contract_major: 1`. Sert à sélectionner le parseur initial. |
| `/internal/version` | HTTP 200, JSON avec la paire, `contract_major: 1`, `contract_minor: 0`, `engine_version` et `wagtail_version` (versions textuelles), `image_digest` (SHA-256 qualifié). |
| `/internal/health` | HTTP 200 pour `status: "ready"` après lecture de la base du site et de sa page de référence. HTTP 503 et `status: "unavailable"` si indisponible. Ce signal porte uniquement sur l’instance contrôlée. |
| `/internal/render` | HTTP 200, `text/html; charset=utf-8`, en-têtes `X-Studio-Site` et `X-Studio-Instance`. Résoudre la page Wagtail locale de référence et rendre son contenu publié avec un marqueur de fixture propre au site. La preuve compare les en-têtes et le marqueur visible attendu fourni par le profil de démonstration. |

Contrat initial 1.0. Accepter les champs additionnels d’une version mineure de v1 lorsque tous les champs obligatoires et leurs valeurs restent compatibles. Une rupture de sémantique requiert une nouvelle majeure. Pendant le premier lot, accepter seulement les versions et digests moteur qualifiés dans le manifeste local. Une nouvelle livraison moteur passe les tests du contrat avant ajout au manifeste. Traiter mauvaise majeure, schéma mal formé ou version non qualifiée comme incompatibles. Contrôler le type de contenu et borner les réponses (proposition : 16 Kio JSON, 64 Kio HTML). Le rendu technique utilise une fixture sans données personnelles. Aucun HTML distant n’est injecté dans l’interface de Studio.

## Raccordement et reprise

Entrée proposée : commande locale avec acteur, UUID de site et alias de profil. Le profil résout l’origine HTTPS, l’instance attendue, les références des certificats et le marqueur de démonstration. Le paramètre « acteur » est réservé au terminal d’un administrateur de confiance agissant pour l’opérateur désigné. Un futur point d’entrée web devra prendre l’acteur dans la session. Réutiliser les sélecteurs et le niveau gestion de FEAT-002 pour le site, y compris si le client est archivé.

1. Valider mandat et profil. Dans une transaction courte, réserver la tentative avec un identifiant et une échéance. Une tentative active provoque un conflit explicite. Une tentative expirée peut être reprise avec un nouvel identifiant.
2. Hors transaction, vérifier les quatre lectures dans le budget global proposé de 10 secondes (connexion max. 2 secondes, lectures bornées par le temps restant). Aucun rejeu automatique dans ce parcours manuel. Vérifier le certificat, les deux UUID, les versions, la santé et le rendu avant confirmation.
3. Dans une nouvelle transaction, verrouiller le site et la tentative, relire le mandat et le profil, vérifier l’identifiant de tentative et l’unicité des deux côtés. Confirmer en une écriture atomique avec la dernière observation. Un second succès identique actualise la date. Une autre instance pour une fiche déjà liée ou une instance revendiquée par un autre site entraîne un conflit. Le remplacement explicite est reporté.
4. En cas d’échec, terminer uniquement la tentative encore courante et conserver la dernière association confirmée. Prévoir des codes distincts pour erreur réseau ou TLS, authentification, contrat incompatible, identité incorrecte, indisponibilité, rendu inattendu et conflit. Une tentative sans liaison antérieure laisse le site sans association. Un processus interrompu laisse une tentative expirante, jamais une confirmation implicite.

## Exploitation à qualifier

Dans le laboratoire, n’exposer que les entrées de démonstration nécessaires sur la boucle locale. Prévoir un réseau de service dédié vers les seules API et un réseau de données privé par instance. Sauvegarder base et médias de chaque site avec le même point de cohérence, conserver la configuration et les références d’identité séparément. Tester la restauration isolée avec les marqueurs du bon site avant toute décision d’exploitation.

Relever CPU, mémoire, espace des bases et médias, temps de démarrage et de vérification pour une puis deux instances. Observer le comportement de B pendant l’arrêt de A. Consigner les mesures sur le matériel utilisé avant d’estimer une capacité de production. Le dimensionnement, les objectifs de reprise et l’exploitation de production demandent des mesures dédiées. [Sécurité](SECURITY.md) · [Plan et scénarios](TASKLIST.md)

**Origine du digest.** L’administrateur démarre le conteneur depuis l’image référencée par digest et fournit ce digest dans la configuration de lancement. La qualification compare la valeur déclarée via l’API au digest observé par le runtime local sur chacune des deux instances. Le champ retourné par le processus distant est une déclaration de version, sans propriété d’attestation matérielle.

**Rendu et portée UI.** Utiliser une route de diagnostic qui sert le rendu d’une page de référence via un type de page et un gabarit déjà fournis ou préparés par Wagtail. Contrôler le type de page et la révision de contenu attendus dans la fixture. Toute création d’un écran produit ou d’un nouveau gabarit frontend spécifique demandera de reprendre le jalon UI du Workflow avant le code concerné.
