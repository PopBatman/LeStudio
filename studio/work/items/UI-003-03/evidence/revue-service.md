# Revue indépendante du service de sauvegarde et de la migration

Le service de lot construit la composition à partir de la révision courante du site. La migration 0006 ajoute la table des reçus de sauvegarde et sa contrainte d’unicité. La revue couvre le parcours HTTP de l’opérateur, le service, les validateurs de composition, les modèles et les essais PostgreSQL. Le cas de concurrence examiné est celui de deux opérateurs modifiant le même site.

## Portée et atomicité

Le service ouvre une transaction, vérifie le mandat de gestion et verrouille le site avant de rechercher le reçu ou de lire la tête. Tous les gestes utilisent la page du lot et les mêmes identifiants locaux. Un changement de parent passe par la résolution du parent dans cette page. Un sous-arbre déplacé est détaché avant la résolution, ce qui exclut sa descendance des destinations possibles. La duplication exige une identité locale par occurrence, vérifie les références de chaque copie avec le contrat du site et crée les UUID canoniques côté serveur. Une nouvelle association éditoriale doit toujours passer par la confirmation Wagtail.

La validation de chaque geste précède l’écriture. Le dernier geste invalide annule la transaction entière. La révision et le reçu sont écrits dans cette même transaction. L’absence de différence conserve le numéro initial. Les relations et la contrainte de la migration correspondent à celles du modèle Django. Cette migration ajoute une table vide et n’exécute aucune transformation de révision.

## Rejeu et conflit

La contrainte porte sur le site, l’opérateur et la clé. Le reçu mémorise l’empreinte du contenu normalisé, la révision obtenue, la sélection et les correspondances d’identités. Un rejeu exact retrouve la première réponse, y compris si une révision plus récente existe. Un autre contenu avec cette clé est refusé. Une autre demande basée sur une ancienne tête obtient un conflit. Les essais de concurrence utilisent deux connexions PostgreSQL et une barrière de départ. Ils contrôlent le nombre total de révisions et le résultat de chaque requête.

Un essai Chromium supplémentaire a interrompu le premier POST côté navigateur, coupé puis rétabli le réseau. Le deuxième POST contenait les mêmes octets. Une réponse de validation simulée a rendu les gestes modifiables et l’annulation a restauré la page. Cet essai contrôle le client. Les essais transactionnels contrôlent séparément l’écriture et le rejeu réels.

## Résultat de la relecture

La revue a identifié un cas dans le contrôle de superposition. Après le placement volontaire de deux blocs sur des plans distincts, une modification ultérieure pouvait ramener le second sur le plan du premier. Le service ne regardait que les paires nouvellement superposées. Le contrôle doit également préserver l’ordre explicite d’une paire existante lors du passage à deux plans identiques, tout en permettant la lecture des anciens brouillons.

Le correctif compare les anciens et nouveaux plans de chaque paire. Le test serveur part d’une superposition sauvegardée et tente d’égaliser les deux plans, avec et sans case de confirmation. Les deux demandes sont refusées. La contre-vérification du modèle local confirme que le refus laisse les positions et l’historique intacts. La série ciblée après correction compte 21 réussites sur PostgreSQL et 20 réussites sur SQLite, où le test de concurrence exigeant des verrous de lignes est ignoré.

La revue est terminée. Le défaut constaté est corrigé et couvert sur le serveur et dans la vue de travail.
