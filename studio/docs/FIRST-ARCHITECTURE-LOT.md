# Premier lot : ARCH-001 — fondation technique de Studio

Le [registre du lot](../work/items/ARCH-001/task.json) indique son état, et le [rapport](../work/items/ARCH-001/REPORT.md) décrit les vérifications réelles.

## Résultat visé

Ce lot prépare les fondations du Studio central dans le dossier produit `studio/` avec les éléments suivants : structure Django, PostgreSQL local, configuration, exécution Docker et vérifications reproductibles.

| Inclus dans la proposition de lot | Traitement |
|---|---|
| Existant | Identifier le code, les configurations et les conventions à préserver |
| Stack | Choisir des versions compatibles, sourcer puis verrouiller |
| Architecture | Définir les responsabilités et une arborescence minimale |
| Exécution | Démarrage local du Studio et de PostgreSQL dans Docker |
| Configuration | Variables documentées, validation des valeurs nécessaires et exemple sans secrets |
| Persistance | Migrations et vérifications exécutées sur PostgreSQL |
| Qualité | Contrôles locaux et fichier CI minimal |
| Documentation | Démarrage, arrêt, maintenance locale et limites réellement observées |

Les écrans métier, le catalogue fonctionnel, les connecteurs fournisseurs et les modules clients sont traités dans leurs lots. Le choix d’un écran ou de Contact ne découle pas d’ARCH-001.

## UI et maquette

Le lot est préparé avec **UI non requise**, car il porte sur une base technique sans écran utilisateur vendu comme résultat. La maquette et les captures de design sont non applicables pour ce périmètre.

Si une interface de connexion, un tableau de bord, une galerie de composants ou un éditeur entre dans le lot, mettre à jour le périmètre, la tasklist et le statut UI avant le frontend concerné. Les paliers de conception et de vérification deviennent alors applicables.

## Documents du lot

| Document | Usage |
|---|---|
| [SPEC.md](../work/items/ARCH-001/SPEC.md) | Périmètre et critères d’acceptation |
| [RESEARCH.md](../work/items/ARCH-001/RESEARCH.md) | Sources et compatibilité de la stack |
| [ARCHITECTURE.md](../work/items/ARCH-001/ARCHITECTURE.md) | Proposition de responsabilités et points de conception |
| [SECURITY.md](../work/items/ARCH-001/SECURITY.md) | Contrôles de configuration, secrets, journaux et ressources |
| [TASKLIST.md](../work/items/ARCH-001/TASKLIST.md) | Ordre de réalisation proposé |
| [REVIEW.md](../work/items/ARCH-001/REVIEW.md) | Revue du lot |
| [EVIDENCE.md](../work/items/ARCH-001/EVIDENCE.md) | Registre des preuves |
| [REPORT.md](../work/items/ARCH-001/REPORT.md) | Résultats et écarts de l’exécution |

## Démarrage local

Suivre le [guide de démarrage du Studio](../README.md).
