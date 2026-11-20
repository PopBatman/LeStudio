# Stack de Studio — portée et qualification

Date : 18 novembre 2026.

Les versions du Studio central pour le développement local sont verrouillées dans le [Dockerfile](../Dockerfile), la [composition Docker](../compose.yaml) et les [dépendances Python](../requirements.txt).

| Élément | Statut dans la direction du projet | Portée |
|---|---|---|
| Python | Choix exprimé | Langage principal |
| Django | Choix exprimé | Backend Studio et moteur |
| PostgreSQL | Choix exprimé, sans exception locale établie | Persistance applicative et vérifications pertinentes |
| Wagtail | Choix exprimé pour le CMS | Moteur éditorial ; pas de rôle de gestion d’infrastructure |
| Django Templates | Direction exprimée | Rendu serveur des interfaces |
| Tailwind CSS | Choix exprimé | Styles et design system |
| Django Cotton | Direction de composants | Réutilisation de templates ; qualification avec la stack retenue |
| shadcn-django | À évaluer et sélectionner | Composants s’appuyant sur Cotton, à examiner selon le besoin |
| HTMX | Selon interactions requises | Requêtes serveur et fragments |
| Alpine.js | Selon interactions locales requises | États temporaires de présentation |
| GSAP | Selon le projet | Animations justifiées |
| n8n | Option explicite | Orchestration ou intégration, sans déplacer les invariants métier |
| GitLab / GitLab CI/CD | Choix exprimé | Code, contrôles et livraison |
| Docker | Choix exprimé | Services conteneurisés |
| Scaleway | Direction d’hébergement exprimée | Qualification distante dans un lot d’exploitation |
| Monitoring | Besoin exprimé | Outil et périmètre à choisir ; Cockpit ou équivalent cité dans la source |

## Fondation locale ARCH-001

| Besoin immédiat | Traitement proposé |
|---|---|
| Démarrer Studio | Application Django centrale minimale |
| Vérifier les données | PostgreSQL local et migrations réelles |
| Reproduire l’environnement | Construction Docker et configuration locale documentées |
| Protéger la configuration | Variables nécessaires explicitement validées, exemple sans secrets |
| Contrôler les changements | Validation de structure, contrôles Django et tests pertinents dans une CI minimale |
| Préparer les extensions | Frontières feature/connecteur/UI documentées ; aucune génération de centaines d’applications |

La compatibilité de Wagtail est examinée avec l’écosystème cible, sans imposer son installation dans le processus central s’il n’y porte aucun besoin éditorial. La création du moteur est un périmètre explicite, pas un ajout implicite de contenu métier.

## Versions du Studio central

Python 3.12.16, Django 5.2.19 LTS, Psycopg 3.3.9 et PostgreSQL 17.12. La matrice de Wagtail 7.4 permet au futur moteur éditorial de partager la série Python/Django retenue. La [recherche du lot](../work/items/ARCH-001/RESEARCH.md) conserve les sources et les limites de cette qualification. Le [rapport local](../work/items/ARCH-001/REPORT.md) relie les résultats à la révision examinée.
