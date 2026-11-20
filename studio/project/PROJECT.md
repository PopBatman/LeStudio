# Studio — fiche projet

Version du document : 1.0 • Date : 18 novembre 2026.

## Produit

**Studio est l’outil de travail qui permet de préparer, composer, configurer et maintenir les sites de clients à partir d’un moteur commun et de capacités réutilisables.**

Le développement du Studio central est la priorité exprimée par l’utilisateur. Le moteur de sites et le Workflow AI l’accompagnent ; l’ancien prototype « site vitrine + contact » ne définit pas le premier périmètre du produit.

| Élément | Rôle |
|---|---|
| Studio | Composition, configuration, suivi et opérations autorisées sur les sites |
| Moteur Django/Wagtail | Exécution des sites, contenus, rendu et modules métier |
| Workflow AI | Processus et outils pour étudier, développer et vérifier Studio et le moteur |
| Notion | Consultation, recherche, décisions et références documentaires |

## Orientations exprimées

| Orientation | Statut et portée |
|---|---|
| Clients : commerçants et petites industries | Cible exprimée ; les domaines précis sont étudiés par besoin |
| Moteur commun versionné | Principe exprimé ; personnalisation par contenus, configuration et extensions maîtrisées |
| Un seul serveur, services dockerisés | Dernière clarification utilisateur ; les détails de topologie sont secondaires |
| Priorité à la sécurité | À traduire en permissions, validation, séparation des données, maîtrise des dépendances et preuves |
| Recherche, tasklist, maquettes et TDD adapté | Paliers demandés pour un développement structuré |
| Contrats feature / connecteur / UX-UI | Cadre à utiliser dans les processus et à préciser pour chaque réalisation |

Les anciennes formulations « un serveur par site » ou « par client » restent des éléments historiques. Elles ne doivent pas réapparaître comme un arbitrage bloquant pour démarrer le travail produit.

## Utilisateur principal proposé

L’opérateur du Studio, initialement le développeur qui réalise et maintient les sites. Le libre-service des clients et ses permissions seront définis selon les parcours retenus ; leur disponibilité n’est pas présumée.

## Espaces fonctionnels proposés

| Espace | Résultat recherché |
|---|---|
| Mes sites | Retrouver une réalisation, la rattacher à un client et connaître son état |
| Atelier du site | Définir identité, structure, navigation et apparence parmi les possibilités disponibles |
| Modules | Examiner les capacités, leurs prérequis et leurs réglages |
| Connexions | Configurer les services nécessaires et comprendre leur état |
| Contenus et aperçu | Éditer les contenus et examiner un rendu identifiable |
| Publication et activité | Examiner les changements, suivre les opérations et retrouver leur résultat |

Ces espaces constituent une proposition produit. Ils ne sont pas tous inclus dans ARCH-001.

## Parcours directeur proposé

Créer un site client, définir sa structure et son apparence, configurer les capacités disponibles, enregistrer un brouillon puis consulter un aperçu sur le moteur. La publication et le suivi prolongent ce parcours selon le lot retenu.

| Objet | Signification |
|---|---|
| Client | Entité à laquelle rattacher les sites et les accès |
| Site | Réalisation identifiable, avec contenus et configuration |
| Module | Capacité livrée et éventuellement activable |
| Connexion | Configuration d’un compte ou système externe pour une portée définie |
| Configuration | Ensemble de paramètres validés, avec version identifiable |
| Opération | Demande suivie jusqu’à un résultat observé |

Ce vocabulaire ne constitue pas encore un schéma de données intégral. Les modèles sont introduits lorsqu’un cas d’usage les justifie.

## Premier lot d’architecture

Le [rapport ARCH-001](../work/items/ARCH-001/REPORT.md) décrit la fondation locale du Studio central, les versions vérifiées et les résultats. Le [guide de démarrage](../README.md) permet de lancer Django et PostgreSQL.

Aucun module métier n’est sélectionné par ce lot. Le catalogue reste une réserve de possibilités à étudier. Son existence ne constitue pas une promesse de disponibilité.

## Références

- [Décisions et propositions](DECISIONS.md)
- [Stack et portée](STACK.md)
- [Contrats d’architecture](../docs/ARCHITECTURE-CONTRACTS.md)
- [Premier lot d’architecture](../docs/FIRST-ARCHITECTURE-LOT.md)

