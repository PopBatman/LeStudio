# Bilan du cadrage

Le dossier fixe le contrat minimal du socle. Un site peut commencer sans brouillon ni liaison ; une opération explicite du gestionnaire crée la première révision. Les lectures suivantes et les sauvegardes sont bornées par le mandat Site. Une concurrence se résout par comparaison de révision et transaction. Le résultat demeure dans la base centrale. Les cinq critères Notion sont traduits en scénarios mesurables dans la [spécification](SPEC.md) et le [plan de réalisation](TASKLIST.md).

Le [document V1](COMPOSITION.md) définit une structure commune aux éditeurs, illustrée par une [composition fictive](evidence/composition-v1.json). Les tailles maximales proposées seront vérifiées sur PostgreSQL pendant le développement. Les parcours de départ externes servent ici de contrats de données ; leurs interfaces se construiront dans les sous-lots dédiés. Il n’y a aucune nouvelle maquette de ce lot backend. Les [maquettes de la fiche du parent](../FEAT-003/VISUAL-REVIEW.md) restent la référence pour l’intégration future.

La [revue indépendante](REVIEW.md) examine le cadrage. Les tests métier, migrations, courses concurrentes et contrôles de non-écriture moteur restent des livrables de la réalisation. Contributions de /root pour les contrats métier, la persistance, les permissions, la recette et le rapprochement Notion ; /root/draft_schema pour COMPOSITION.md et la fixture ; /root/draft_review pour la revue.

## Réalisation du socle

Le Studio central dispose de quatre services : lire la tête, lire une révision identifiée, créer le brouillon et enregistrer une nouvelle révision. Le modèle CompositionRevision protège la fiche Site, conserve une lignée ordonnée et impose l’unicité du numéro dans le site. Le document et la provenance initiale sont validés côté serveur. L’autorisation en lecture est appliquée dans la requête de révision. Les écritures utilisent une transaction et verrouillent notamment le compte, l’adhésion, le site et le mandat. Le lecteur obtient uniquement les métadonnées d’une révision de schéma incompatible.

Les définitions intégrées sont le conteneur, le titre et le texte. Des résolveurs locaux autorisés peuvent décrire de nouvelles définitions et références, ou fournir une composition initiale pour un template ou une proposition Figma acceptée. Les tests utilisent des fournisseurs fictifs dans ces deux parcours. Les occurrences copiées ont de nouveaux UUID et les liens de parenté sont remappés ensemble. Le [guide de service](../../../docs/BROUILLONS.md) précise les points d’entrée pour les futurs éditeurs.

| Critères | Résultat local |
|---|---|
| AC1 et AC5 | Migration additive sur une base de recette contenant déjà une fiche et un raccordement. Aucune révision créée par migration. Deux révisions relues, origine conservée, corps historique de schéma inconnu masqué. |
| AC2 | Même service et même document pour les origines vierge, modèle et Figma autorisé. Une origine externe exige un fournisseur de confiance ; la commande refuse un corps externe substitué par l’appelant. |
| AC3 | Accès restreint par site, mandats lecture et gestion, compte révoqué, identifiants étrangers et références média contrôlés dans les tests de service. |
| AC4 | Courses PostgreSQL à deux connexions, sur première création et sur modification d’une même base : un seul succès par course. Une erreur intermédiaire déclenche le rollback. Validation du schéma, des identités et des bornes. |

Une lecture et une création d’un document compact de 1 Mio ont été chronométrées sur base PostgreSQL isolée. Les temps décrivent un essai local et dépendent de la machine. Les [preuves](EVIDENCE.md) séparent migration, tests et mesure. Le parent FEAT-003 poursuit son découpage ; les écrans de création et de reprise appartiennent au sous-lot 04.

Contributions de /root/composition_validator pour le document V1 et ses essais, /root/composition_service pour les services et le stockage, /root/composition_tests pour les scénarios de droits et de concurrence, /root/composition_review pour la revue indépendante et /root pour l’intégration, la qualification PostgreSQL et le rapprochement Notion.

Résultat final : 75 tests réussis sur PostgreSQL. Sur SQLite, 70 tests réussis et cinq tests réservés à PostgreSQL. Les deux opérateurs de sites distincts peuvent enregistrer indépendamment. La revue a également conduit à borner le JSON brut à 4 Mio avant décodage, en plus de la limite de 1 Mio compacte avant résolution. Sur le poste Studio, la migration est appliquée et le service web répond au contrôle de santé. La fiche et la liaison existantes ont été conservées, avec zéro brouillon créé implicitement.
