# Développer un connecteur

Ce parcours complète [FEATURE-WORKFLOW.md](FEATURE-WORKFLOW.md). Lire les [contrats d’architecture](../../studio/docs/ARCHITECTURE-CONTRACTS.md).

## Contrat avant implémentation

| Domaine | Travail |
|---|---|
| Capacité | Définir l’opération utile, ses entrées, résultats et limites |
| Fournisseur | Lire sa documentation primaire et identifier version, authentification, quotas et garanties |
| Portée | Associer compte, site/client et opérations autorisées |
| Configuration | Valider paramètres et destinations ; conserver des références de secrets |
| Erreurs | Définir refus, erreur temporaire, limitation et résultat incertain |
| Reprise | Définir idempotence réellement supportée, doublons et réconciliation |
| Événements | Authentification, rattachement, ordre, déduplication et prise en charge durable |
| Exploitation | Diagnostic, journal minimal, métriques utiles et révocation |

Le métier décide pourquoi agir. L’adaptateur traduit l’échange. Le SDK reste un détail interne. Une opération spécifique au fournisseur peut rester explicite.

## Construction et qualification

1. Écrire [CONNECTOR-SPEC.md](../templates/CONNECTOR-SPEC.md) et les scénarios.
2. Préparer la tasklist et les écrans de réglage/diagnostic concernés.
3. Tester le contrat et les cas d’erreur avec des réponses maîtrisées.
4. Implémenter l’adaptateur, ses limites et sa sélection contrôlée.
5. Qualifier les hypothèses utiles dans un environnement fournisseur autorisé.
6. Intégrer les résultats à la feature et à l’interface.
7. Réaliser la revue et conserver les limites.

Un test de connexion privilégie une opération sans effet métier lorsque le fournisseur le permet. Un envoi réel de test est une action distincte. Une lecture réussie ne démontre pas tous les droits d’écriture.

Distinguer **implémenté**, **configuré** et **qualifié**. Une simulation réussie ne prouve pas une connexion réelle. L’activation choisit du code déjà livré ; elle n’installe pas librement des dépendances en production.

