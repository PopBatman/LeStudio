# ARCH-002 — Raccordement du moteur commun

## Cadrage du 19 novembre 2026

Le lot dispose d’un [contrat de raccordement manuel](ARCHITECTURE.md), de [neuf critères observables](SPEC.md), d’une [politique de confiance et de rotation](SECURITY.md) et d’un [plan de réalisation](TASKLIST.md). L’[inventaire](RESEARCH.md) rattache la proposition aux versions, aux services et aux habilitations du dépôt.

Le mandat initial portait sur la conception et la documentation. L’équipe propose le TLS mutuel, des UUID de site et d’instance vérifiés hors bande et quatre lectures sous une origine administrée. Le premier essai de réalisation devra confronter deux instances indépendantes de la même image à une fiche valide, une identité croisée, une rupture de compatibilité et une indisponibilité.

La révision du contrat est identifiée par la commande de fingerprint du Workflow et reportée sur la [carte Notion](https://app.notion.com/p/41c49e23bbdb81cd9f76d83b6f00758e). Le contrôle de planification porte sur les documents. La mission de développement suivante a qualifié ces points sur le poste local.

## Réalisation

Le moteur 1.0.0 utilise Wagtail 7.4.4, Django 5.2.19 et PostgreSQL 17.12. Son image Linux amd64 embarque les dépendances Python verrouillées. Une instance initialise sa propre page de référence Wagtail, rattachée à son site et à son UUID d’instance. La lecture du rendu utilise la révision publiée. Le Studio central ajoute une migration, une commande et un client HTTPS. Le [guide opérateur](../../../docs/MOTEUR-WAGTAIL.md) décrit la configuration et la consultation des résultats.

| Critères | Résultat local |
|---|---|
| AC1, AC2 | Passage depuis une base FEAT-002 contenant un site sans domaine. Aucune liaison créée par migration. La commande contrôle le mandat de site avant l’appel réseau et avant la confirmation. |
| AC3, AC4 | Contrôles des deux UUID, de la version du contrat, de la version du moteur et du digest qualifié. Le laboratoire enregistre les confirmations distinctes et les refus avec diagnostic. |
| AC5, AC6 | Historique limité à la dernière confirmation et à la dernière tentative. Tests de perte de mandat, reprise, unicité, concurrence et préservation d’une confirmation après un échec. |
| AC7, AC8 | Deux projets de site depuis une image commune, avec PostgreSQL, rôles, médias, éditeurs et sessions séparés. Le contenu Wagtail attendu est lu au travers de chaque frontal mTLS. |
| AC9 | Le connecteur utilise quatre GET. Qualification du renouvellement de certificat, de la panne de base et de la reprise, avec une copie de restauration jetable. Les mesures de ressources sont celles d’une démonstration locale. |

Le laboratoire indépendant utilise des sites fictifs et ses propres projets Compose. La migration centrale a également été appliquée sur l’installation Studio habituelle avec son volume existant. Les opérations de configuration et de publication éditoriale appartiennent aux lots suivants. Le correctif Wagtail et l’image sont qualifiés pour cet environnement et cette architecture. Les [preuves](EVIDENCE.md) distinguent tests centraux, tests moteur et qualification réelle.

Contributions de `/root/link_impl` pour l’association, `/root/engine_impl` pour le moteur, `/root/lab_impl` pour l’environnement des deux sites et `/root` pour le transport, les profils et l’intégration centrale. La [revue de réalisation](REVIEW.md) complète l’examen du cadrage.
