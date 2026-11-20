# Droits, ressources et diagnostics

| Opération | Autorisation et résultat attendu |
|---|---|
| Lire le catalogue ou un diagnostic | Exiger une session opérateur et une habilitation de lecture au site. Filtrer d’abord les définitions et ressources accessibles. Un identifiant privé d’un autre site et une référence inconnue donnent le même retour. |
| Modifier un brouillon | Exiger le droit de gestion, un POST protégé par CSRF et la révision de base. Recontrôler l’habilitation et la tête sous verrou. En conflit, garder la saisie et présenter la révision courante. Une révocation avant confirmation empêche l’écriture. |
| Ajouter une version technique | Autoriser une référence à un type de rendu livré et examiné par l’équipe. Valider clés, types, taille, variantes, limites et références au serveur. Les libellés et textes sont échappés au rendu. Les polices viennent des familles livrées, les styles de tokens admis. |
| Proposer une promotion | Identifier la version locale exacte, l’auteur et le motif. Consigner dans Studio une référence de preuve de réutilisation adaptée à la création et aux ressources, sans publier les pièces privées ni l’identité du client dans le catalogue partagé. |
| Accepter ou refuser | Réserver la décision à un réviseur distinct, habilité à publier au catalogue. Vérifier les droits et la copie expurgée, la version examinée et le résultat des contrôles techniques. Changer la proposition invalide la revue précédente. Répéter l’acceptation ne crée pas deux versions. |
| Retrait ou droits échus | Écarter la ressource des nouvelles sélections. Sur un ancien brouillon, identifier l’emplacement et signaler le problème sans afficher d’élément privé. L’historique du site reste lisible par un opérateur habilité. |

Tests négatifs à programmer sur deux sites fictifs : référence privée malgré un UUID valide, acteur lecture seule, approbation par l’auteur, droits absents, référence modifiée entre revue et validation, deuxième écriture concurrente, paramètre de style ou balisage libre. Pour chaque refus, vérifier l’absence de changement au catalogue global et aux révisions des autres sites. Le parcours de bibliothèque réalise ses lectures dans Studio, sans connexion au moteur pour charger des ressources.
