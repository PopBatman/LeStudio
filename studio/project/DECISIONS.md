# Décisions, propositions et corrections

Date de consolidation : 18 novembre 2026.

Les références SRC ci-dessous repèrent les messages de cette conversation ou le fichier fourni. Elles ne sont pas des signatures. Les décisions exprimées par l’utilisateur, les conventions intégrées au Workflow et les choix produit restant à préciser conservent des statuts distincts.

## Sources

| Référence | Origine |
|---|---|
| SRC-01 | Fichier utilisateur « Texte collé(8).txt » : 47 énoncés numérotés et catalogue |
| SRC-02 | Clarification utilisateur : « on prend un seul serveurs et tout est dockerisé » |
| SRC-03 | Priorité utilisateur : « Ici on se concentre sur la création de notre outil Studio » |
| SRC-04 | Demande de cadrage : développer les features, connecteurs et composants UX/UI |
| SRC-05 | Demande actuelle : écrire les processus, mettre à jour Notion et livrer le Workflow AI installable |
| SRC-06 | Historique : recherche avant modules inconnus, tasklist avant code, maquettes frontend et discussion TDD |
| SRC-07 | Correction utilisateur : développement commencé avant le cadrage du projet, des règles et de l’architecture |
| SRC-08 | Demande du 18 novembre 2026 de séparer les règles IA du projet Django/Wagtail |

## Choix et exigences exprimés

| ID | Énoncé actuel | Origine | Effet |
|---|---|---|---|
| DEC-001 | La création du Studio central est prioritaire | SRC-03 | Les lots sont orientés vers l’outil Studio |
| DEC-002 | Base d’hébergement : un serveur, services dockerisés | SRC-02 | Les anciennes variantes par site/client ne bloquent plus le cadrage produit |
| DEC-003 | Python/Django, PostgreSQL et moteur Wagtail constituent la direction de la stack | SRC-01 | Qualifier les versions compatibles avant installation ; préciser la portée de chaque composant |
| DEC-004 | Le moteur des sites est commun et versionné | SRC-01 et historique | Documenter compatibilité et personnalisation |
| DEC-005 | Wagtail porte les responsabilités éditoriales et ne devient pas le gestionnaire d’infrastructure | SRC-01, W000 | Séparer édition, métier et opérations de Studio |
| DEC-006 | Le générateur ne doit pas installer librement des composants en production | SRC-01, C002 | Livraison contrôlée, permissions et pipeline adaptés |
| DEC-007 | Le Workflow doit intégrer les trois contrats de développement | SRC-04–05 | Procédures distinctes et cycle commun |
| DEC-008 | La prochaine étape produit est la fondation d’architecture | SRC-05 | ARCH-001 est préparé dans le paquet, sans prétendre l’exécuter ici |
| DEC-009 | La méthode comprend recherche, tasklist, maquette applicable, tests et revue | SRC-06 | Choisir des vérifications proportionnées et tracer les limites |
| DEC-010 | Séparer la gouvernance IA du produit Django/Wagtail | SRC-08 | Les règles et outils vivent dans `workflow-ai/`. Les sources, décisions et lots du produit vivent dans le dossier frère `studio/`. |

« Exprimé » n’indique pas qu’une exigence est déjà implémentée ou vérifiée. Les versions, paramètres et contrôles concrets restent à qualifier dans le lot concerné.

## Conventions intégrées au Workflow

Ces conventions sont la référence de développement de cette version du Workflow. Elles ne constituent pas une approbation des choix détaillés de tous les futurs modules.

| ID | Convention | Justification | Traitement |
|---|---|---|---|
| CONV-001 | Applications Django par responsabilité, services applicatifs explicites | Conserver les règles pour tous les points d’entrée | Préciser le découpage dans ARCH-001 puis chaque feature |
| CONV-002 | Connecteurs derrière des contrats de capacité | Limiter la dépendance aux fournisseurs et expliciter les erreurs | Appliquer aux intégrations retenues |
| CONV-003 | Fondations UI, primitives partagées, composants métier locaux | Réutiliser sans confondre présentation et décisions métier | Détailler au premier lot frontend |
| CONV-004 | Contextes acteur/site/client explicites | Éviter les accès implicites trop larges | Définir la matrice d’autorisation du périmètre |
| CONV-005 | Configuration désirée distincte du résultat appliqué | Représenter les opérations et échecs réels | Définir lors du premier parcours de configuration |
| CONV-006 | Intention persistée pour les effets externes devant survivre à un arrêt | Préserver le travail à effectuer et maîtriser la reprise | Retenir lorsque le besoin le justifie |

Les chemins et découpages illustratifs des contrats seront adaptés au dépôt cible. Le nombre de dépôts et la séparation des processus seront choisis sur la base de l’existant et des besoins, sans rouvrir toute la discussion d’hébergement.

## Choix produit encore à préciser

| ID | Proposition | Justification | Traitement |
|---|---|---|---|
| PROP-001 | Opérateur Studio comme premier utilisateur | Concentrer le premier parcours | Périmètre produit proposé ; accès clients à spécifier |
| PROP-002 | Espaces sites, atelier, modules, connexions, contenus/aperçu et suivi | Organiser le travail de l’opérateur | Structure de navigation à confronter aux parcours avant les écrans |
| PROP-003 | Séparation logique du Studio central, du moteur et des adaptateurs | Rendre les responsabilités explicites | Traduction en dossiers, packages ou processus à arrêter dans les lots concernés |

## Corrections de l’historique

| Sujet | État corrigé |
|---|---|
| Premier lot « site vitrine + Contact » | Choix antérieur de l’assistant, non adopté comme premier lot de Studio |
| Ancien SESSION-SCOPE | Ne prouvait pas la validation du périmètre inventé par l’assistant |
| SQLite du prototype | Écart par rapport à PostgreSQL exprimé dans la source ; aucune exception locale créée rétroactivement |
| Serveur par site / par client | Formulations historiques remplacées dans la direction de travail par SRC-02 |
| Tests anciens réussis | Preuves de comportements du prototype, pas approbation du besoin ni de l’architecture actuelle |
| Capacités agentiques | Rôles, instructions, intégrations configurées et mécanismes réellement exécutés restent distincts |

## Prochaines décisions de lot

Qualifier les versions compatibles, le découpage minimal du dépôt cible, les entrées d’exécution, la configuration locale et les contrôles CI. Tout résultat est daté et relié à la révision examinée.

Un nouveau choix est enregistré avec sa source, son périmètre, sa justification et les conséquences. Il ne remplace pas silencieusement une décision existante.

