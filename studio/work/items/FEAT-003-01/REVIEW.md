# Revue indépendante du cadrage

Le 19 novembre 2026, le réviseur indépendant `/root/draft_review` a confronté les cinq critères de la [carte du sous-lot](https://app.notion.com/p/41d49e23bbdb81a5aeddfea5f1ef8d56) aux [choix du parent](../FEAT-003/ARCHITECTURE.md), aux [services de registre](../../../registre/services.py) et à la [gestion réelle des habilitations](../../../registre/management/commands/registre_access.py).

| Critères | Constat documentaire |
|---|---|
| AC1 et AC5 | La plus grande révision du site forme sa tête logique. Le contrat conserve l’origine, le numéro, le parent et le document historique. Une lecture par site et UUID de révision fournit une entrée stable aux futurs éditeurs et à l’aperçu. La composition appliquée est inconnue tant que le moteur n’en atteste aucune. |
| AC2 | La provenance est extérieure au document validé. Les trois origines et les deux consommateurs sont exercés avec des entrées contrôlées dans la recette prévue. Les futures intégrations Figma et Wagtail gardent leurs frontières. |
| AC3 | Le mandat Site est contrôlé à chaque opération. Les révisions et les références imbriquées sont résolues dans le périmètre du site. Une ressource inaccessible ne révèle pas son propriétaire. La recette couvre compte révoqué, lecteur et accès entre deux sites. |
| AC4 | Le verrou du site existe avant la première révision et sérialise les créations à vide. La comparaison de la base et l’insertion relèvent d’une transaction unique. La recette propose des connexions PostgreSQL distinctes, un échec intermédiaire et une reprise après réponse perdue. |

Un contrôle indépendant de l’[exemple V1](evidence/composition-v1.json) a vérifié les champs racine, deux pages dont une racine, le lien de parenté, une section, deux blocs globaux épinglés, leur ordre, les cinq UUID distincts, les propriétés de texte et les dispositions de base et mobile. Le document représente 843 octets en JSON compact UTF-8. Ce contrôle porte sur cette fixture précise.

Les contrôles de concurrence, la validation de toutes les mutations, la migration sur base existante et les effets de l’implémentation sont des tests futurs du [plan](TASKLIST.md). Le mandat actuel ne fournit aucune nouvelle surface UI.

Les précisions demandées en revue ont été intégrées. L’accès direct à une révision hors site reçoit le refus de ressource introuvable ; le document d’un site autorisé contenant une référence étrangère reçoit le même diagnostic de champ que pour une référence absente. Un éditeur ancien peut identifier une révision de schéma inconnu et obtenir le diagnostic de compatibilité avant modification. **Avis favorable au passage en READY pour le cadrage.**

## Revue indépendante de réalisation

Le 19 novembre 2026, le réviseur /root/composition_review a examiné le modèle, sa migration, les quatre services internes, le validateur V1 et les tests. Les lectures de tête et d’historique suivent le mandat du site. Lors d’une création depuis une source autorisée, les identifiants d’occurrence sont renouvelés et les références internes remappées. La sauvegarde conserve les révisions antérieures. Un schéma futur produit une réponse de compatibilité avec métadonnées seules.

Deux points ont été relevés en revue et corrigés. Le JSON brut est borné avant décodage et la taille compacte contrôlée avant la résolution des ressources. Une inspection du SQL PostgreSQL a également montré que la première requête de contrôle de l’adhésion verrouillait le groupe commun à tous les opérateurs. La requête corrigée cible la ligne d’adhésion ; un test sur deux sites et deux gestionnaires distincts couvre leur capacité à écrire indépendamment. Les courses de création et de sauvegarde sur le même site conservent une seule tête gagnante.

Le réviseur a rejoué les 23 tests ciblés dans un conteneur hors réseau sur SQLite (20 réussites, trois cas réservés à PostgreSQL), inspecté la migration de la base fictive préexistante et le résultat de relecture d’un document de 1 048 576 octets. La suite finale d’intégration sur PostgreSQL comporte 75 tests réussis. La qualification des trois origines utilise des adaptateurs locaux de test ; les interfaces éditoriales et fournisseurs relèvent de leurs sous-lots.

**Avis favorable sur AC1 à AC5 pour la réalisation du socle FEAT-003-01.**
