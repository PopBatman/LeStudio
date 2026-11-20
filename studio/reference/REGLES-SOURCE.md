> Référence source conservée. Les clarifications de session et conventions actuelles se trouvent dans [les décisions du projet](../project/DECISIONS.md). Le choix actuel est un seul serveur avec des services dockerisés ; les anciennes questions de topologie ne bloquent pas le travail sur Studio.

# Registre documentaire des règles Studio

Version 0.1 — 18 novembre 2026. **Cadrage documentaire uniquement ; développement Studio suspendu.**

Ce registre conserve les **47 identifiants et formulations du fichier utilisateur**, avec leur ligne source. Il classe les éléments et propose des moyens de vérification, sans valider à la place de l’utilisateur une architecture, un premier lot ou une exception.

La source reste `Texte collé(8).txt`. Les numéros de ligne incluent les lignes vides et commencent à 1. Les graphies originales sont conservées. Le JSON conserve également la ligne complète et ses espaces terminaux.

## Légende : quatre dimensions séparées

| Dimension | Sens dans ce dossier |
|---|---|
| Expression / décision | Exigence exprimée, choix conditionnel, portée à clarifier ou proposition source. Ces libellés décrivent la source et le besoin de clarification. |
| Mise en œuvre | **Non audité dans ce dossier** pour chaque règle. Aucun verdict global « non implémenté » n’est prononcé. |
| Preuve de vérification | **Non établie** pour chaque règle. Ce registre ne produit aucune preuve de test, de configuration distante ou d’application effective. |
| Moyen de contrôle | Toujours **PROPOSÉ** ; il décrit comment une preuve pourrait être établie après définition du contrat concerné. |

| Statut de décision | Interprétation |
|---|---|
| exigence exprimée | Formulation affirmative ou interdiction présente dans la source. Ce statut rapporte l’expression utilisateur et ne certifie ni la réalisation ni la qualification. |
| choix conditionnel | Adoption soumise à une option, une évaluation ou un besoin explicitement mentionné dans la source. |
| portée à clarifier | Une orientation est exprimée, mais son périmètre ou sa relation à une autre formulation demande un arbitrage. |
| proposition source | Formulation conservée au conditionnel dans le document utilisateur, sans promotion en décision validée. |

**Le fichier `registres/regles.json` est un registre documentaire, pas un moteur d’autorisation, une machine à états ni un dispositif de blocage technique.** Une entrée n’accorde aucun droit à un agent et ne déclenche aucune installation.

## Note de lecture technique

shadcn-django est un port non officiel de shadcn/ui ; ses composants copiés dans le projet utilisent Django Cotton. L’évaluation concerne les composants et leur articulation avec la bibliothèque maison, sans présumer de leur adoption ni opposer deux moteurs exclusifs. Source primaire consultée le 18 novembre 2026 : [dépôt shadcn-django](https://github.com/SarthakJariwala/shadcn-django). Cette note est distincte des formulations utilisateur et ne vaut pas décision d’architecture.

## Repérage

| Groupe | Nombre | Lignes sources |
|---|---|
| LT — Technologies | 14 | 8–21 |
| A — Architecture | 13 | 27–39 |
| D — Responsabilités Django | 8 | 96–103 |
| W — Responsabilités Wagtail | 9 | 109–117 |
| C — Cadrage | 3 | 123–125 |

Les doublons ou rapprochements sont signalés par leurs identifiants, jamais supprimés silencieusement. Les catalogues de modules, de connecteurs et la fiche d’exemple ne sont pas convertis en règles numérotées dans ce fichier.

## LT — Technologies

### LT001

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **8** |
| Formulation exacte | Python : Langage principal |
| Catégorie | Choix technologique |
| Portée | Langage principal du code applicatif de Studio et du moteur client ; le mot principal ne rend pas les autres langages interdits. |
| Origine de la portée | déduite — proposition à discuter |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Revue des composants applicatifs et de leurs langages, en documentant les usages de JavaScript et des outils de build sans les assimiler à un changement de langage principal. |
| Questions à examiner | 1. Quels composants doivent obligatoirement être écrits en Python ? |
| Règles liées | `LT002`, `LT009`, `LT014` |

### LT002

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **9** |
| Formulation exacte | Django : Backend du Studio et des sites |
| Catégorie | Choix technologique |
| Portée | Backend du Studio central et des sites clients. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Vérifier dans les décisions et les dépendances que ces deux backends reposent sur Django ; contrôler leurs responsabilités respectives. |
| Questions à examiner | 1. Quelle frontière entre code commun du moteur et code propre au Studio central ? |
| Règles liées | `A002`, `C000`, `D001`, `D008` |

### LT003

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **10** |
| Formulation exacte | Wagtail : CMS et constructeur de pages |
| Catégorie | Choix technologique |
| Portée | CMS et composition de pages ; périmètre principal des instances clientes décrit par C001. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner les modèles de pages, blocs et permissions éditoriales ; vérifier que les fonctions d’infrastructure restent hors du rôle Wagtail. |
| Questions à examiner | 1. Le Studio central utilisera-t-il Wagtail pour un besoin éditorial précis, ou aucunement ? |
| Règles liées | `A003`, `W000`, `W008`, `C001` |

### LT004

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **11** |
| Formulation exacte | PostgreSQL : Stockages des données |
| Catégorie | Choix technologique |
| Portée | Stockage applicatif en PostgreSQL. La source ne mentionne pas d’exception locale ou de test et distingue par ailleurs le stockage de fichiers. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Comparer les configurations des environnements au choix PostgreSQL ; prévoir des tests exécutés sur cette base avant d’établir une preuve de conformité. |
| Questions à examiner | 1. Quels environnements sont concernés ? Toute exception de développement doit-elle être interdite ou explicitement autorisée ? 2. Quelle frontière entre données applicatives et fichiers placés dans un stockage compatible S3 ? |
| Règles liées | `A006` |

### LT005

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **12** |
| Formulation exacte | Tailwind CSS : Design system |
| Catégorie | Choix technologique UI |
| Portée | Styles et système de conception des interfaces ; application au Studio et au moteur proposée à partir des deux tableaux de stack. |
| Origine de la portée | déduite — proposition à discuter |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner le build CSS et les règles de tokens, variantes et composants ; vérifier que les interfaces utilisent les conventions définies. |
| Questions à examiner | 1. Quels tokens, variantes, états et critères d’accessibilité constituent le design system ? |
| Règles liées | `A004`, `LT006`, `LT007` |

### LT006

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **13** |
| Formulation exacte | Shacdn-django : Composants UI |
| Catégorie | Bibliothèque UI candidate |
| Portée | Composants UI sélectionnés ; niveau d’obligation à rapprocher de A005, qui prévoit une évaluation. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **choix conditionnel** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner les composants shadcn-django envisagés, leur code copié utilisant Django Cotton et leur articulation avec la bibliothèque maison ; consigner les composants retenus, adaptés et exclus avant intégration. |
| Questions à examiner | 1. Quels composants shadcn-django souhaitons-nous évaluer avant une éventuelle intégration ? 2. Comment les composants copiés utilisant Cotton s’articuleraient-ils avec la bibliothèque maison et quelles fonctionnalités recouvriraient-ils ? |
| Règles liées | `A005`, `LT007` |

### LT007

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **14** |
| Formulation exacte | Django Cotton : Composants UI |
| Catégorie | Choix technologique UI |
| Portée | Composants de templates du Studio et du moteur ; le rattachement de « à évaluer » dans A005 doit être clarifié. |
| Origine de la portée | déduite — proposition à discuter |
| Statut de décision | **portée à clarifier** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Cartographier les composants réutilisables et leur responsable ; vérifier leur composition et leurs interfaces sur un exemple approuvé. |
| Questions à examiner | 1. A005 impose-t-il une évaluation de Cotton aussi, ou uniquement de shadcn-django ? 2. Quelles responsabilités sont attribuées à Cotton et aux composants sélectionnés ? |
| Règles liées | `A005`, `LT006` |

### LT008

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **15** |
| Formulation exacte | HTMX : Interactions serveurs |
| Catégorie | Choix d’interaction UI |
| Portée | Interactions avec le serveur ; le tableau du Studio retient HTMX et celui du Site Engine dit « si nécessaire ». |
| Origine de la portée | explicite dans la source |
| Statut de décision | **portée à clarifier** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les parcours qui nécessitent HTMX et contrôler la validation et les permissions côté serveur pour chacun. |
| Questions à examiner | 1. HTMX est-il une convention obligatoire dans le Studio et une option par fonctionnalité côté site ? 2. Quels parcours doivent également fonctionner sans interaction HTMX ? |
| Règles liées | `LT002`, `LT009`, `D002` |

### LT009

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **16** |
| Formulation exacte | Alpine.js : Interactions locales |
| Catégorie | Choix d’interaction UI |
| Portée | Interactions locales ; Alpine est présent dans le tableau du Studio et conditionnel dans celui du Site Engine. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **portée à clarifier** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Recenser les comportements locaux et vérifier qu’ils ne portent pas seuls une validation métier ou une autorisation. |
| Questions à examiner | 1. Quelles interactions locales nécessitent Alpine ? 2. Quel socle JavaScript est commun et quelles dépendances sont activées selon le site ? |
| Règles liées | `LT008`, `D005`, `D006` |

### LT010

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **17** |
| Formulation exacte | n8n : Automatisation et intégration |
| Catégorie | Automatisation optionnelle |
| Portée | Automatisation et intégration, avec caractère optionnel explicite dans A013. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **choix conditionnel** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Pour chaque besoin, documenter si n8n est utilisé, les données reçues, les droits, la reprise après erreur et la responsabilité des règles métier. |
| Questions à examiner | 1. n8n sera-t-il partagé, isolé par client ou absent par défaut ? 2. Quels traitements restent impérativement dans le backend ? |
| Règles liées | `A013`, `D005`, `D008` |

### LT011

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **18** |
| Formulation exacte | Gitlab CI/CD : Tests et déploiements |
| Catégorie | Outil de livraison |
| Portée | Tests et déploiements par GitLab CI/CD. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Vérifier le graphe des jobs, les critères de blocage, les identités et les protections du dépôt avec une pipeline d’essai. |
| Questions à examiner | 1. Quels contrôles sont bloquants ? 2. Quels environnements et quelles actions exigent une validation humaine ? 3. Le tableau d’outils envisagés doit-il retenir mypy ou Pyright ? |
| Règles liées | `A010`, `A011`, `A012`, `C002` |

### LT012

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **19** |
| Formulation exacte | Docker : Packaging et déploiement |
| Catégorie | Packaging et exécution |
| Portée | Packaging et déploiement des applications dans Docker. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner les fichiers de construction, l’identité de l’image livrée et les paramètres d’exécution ; qualifier l’image sur l’environnement prévu. |
| Questions à examiner | 1. Quelles images, quels processus et quels volumes composent une instance ? |
| Règles liées | `A011`, `LT011` |

### LT013

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **20** |
| Formulation exacte | Scaleway : Infrastructure cloud  |
| Catégorie | Fournisseur d’infrastructure |
| Portée | Infrastructure cloud Scaleway ; services précis à choisir. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Faire correspondre l’inventaire d’infrastructure à la cible documentée ; qualifier accès, réseau, sauvegardes et exploitation sur les services retenus. |
| Questions à examiner | 1. Quels services Scaleway, quelles régions et quelles tailles correspondent à la V1 ? 2. Quelles dépendances peuvent rester chez d’autres fournisseurs spécialisés ? |
| Règles liées | `A007`, `A008` |

### LT014

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **21** |
| Formulation exacte | GSAP : Animations premium |
| Catégorie | Animation optionnelle |
| Portée | Animations premium ; le tableau Site Engine prévoit CSS ou GSAP selon le projet. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **choix conditionnel** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Justifier l’usage de GSAP pour les animations retenues ; prévoir des critères de performance, de lisibilité et de réduction des animations. |
| Questions à examiner | 1. Dans quels cas GSAP apporte-t-il une capacité nécessaire ? 2. Quels budgets d’animation et de performance seront retenus ? |
| Règles liées | `LT009`, `A004` |

## A — Architecture

### A001

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **27** |
| Formulation exacte | Architecture : Single Codebase, Multi-Instance |
| Catégorie | Principe d’architecture |
| Portée | Code commun et instances multiples. La définition de la codebase, de l’instance et des variantes est encore à préciser. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Comparer les instances à un moteur versionné commun ; examiner la stratégie d’extensions et rechercher les divergences de code propres à un client. |
| Questions à examiner | 1. Single Codebase vise-t-il uniquement le moteur client ? 2. Les modules sont-ils inclus dans une image commune ou dans des variantes gouvernées ? 3. Comment le Studio central et le moteur sont-ils versionnés et répartis dans les dépôts ? |
| Règles liées | `A008`, `A009`, `A011`, `C000` |

### A002

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **28** |
| Formulation exacte | Backend : Django |
| Catégorie | Choix technologique |
| Portée | Backend en Django ; LT002 précise Studio et sites. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Contrôler la cohérence des composants backend et de leurs dépendances avec LT002, sans dupliquer une décision divergente. |
| Questions à examiner | 1. Quelles responsabilités Django sont communes au moteur et lesquelles appartiennent seulement au Studio ? |
| Règles liées | `LT002`, `D001`, `D008` |

### A003

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **29** |
| Formulation exacte | CMS : Wagtail |
| Catégorie | Choix technologique |
| Portée | CMS Wagtail ; la localisation principalement distante reste une proposition de cadrage C001. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Vérifier les responsabilités CMS et leur affectation aux applications ; contrôler la séparation imposée par W000. |
| Questions à examiner | 1. Quelle place précise pour Wagtail dans la topologie retenue ? |
| Règles liées | `LT003`, `W000`, `C001` |

### A004

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **30** |
| Formulation exacte | Design : Tailwind + composants réutilisables |
| Catégorie | Principe UI |
| Portée | Tailwind et composants réutilisables pour les interfaces ; conventions communes proposées aux deux applications. |
| Origine de la portée | déduite — proposition à discuter |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Recenser les composants partagés, leurs variantes, leurs états et leurs usages ; vérifier leur conformité aux conventions UI définies. |
| Questions à examiner | 1. Quels éléments doivent rester identiques entre Studio et thèmes clients ? 2. Comment un thème client peut-il varier sans modifier le moteur commun ? |
| Règles liées | `LT005`, `LT006`, `LT007`, `A005` |

### A005

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **31** |
| Formulation exacte | Composants UI : Django Cotton, shacdn-django à évaluer |
| Catégorie | Sélection de composants UI |
| Portée | Django Cotton et shacdn-django ; l’expression « à évaluer » maintient une sélection ouverte. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **choix conditionnel** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Comparer les composants et les approches de composition envisagés ; examiner l’usage de Cotton par les composants shadcn-django candidats et documenter la sélection sans déduire leur adoption de leur présence au catalogue. |
| Questions à examiner | 1. L’évaluation porte-t-elle sur le socle Cotton, sur les composants shadcn-django copiés qui l’utilisent, ou sur l’ensemble de cette approche ? 2. Quels composants sont adoptés, adaptés, développés en interne ou exclus ? |
| Règles liées | `LT006`, `LT007`, `A004` |

### A006

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **32** |
| Formulation exacte | Base de données : PostgreSQL |
| Catégorie | Choix de base de données |
| Portée | PostgreSQL pour les bases ; aucune exception d’environnement n’est formulée. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Contrôler les configurations et exécuter les vérifications pertinentes sur PostgreSQL ; documenter les éventuels écarts sans les considérer autorisés. |
| Questions à examiner | 1. Le choix s’applique-t-il également au développement et aux tests ? 2. Comment sont isolés bases, rôles et sauvegardes par instance ? |
| Règles liées | `LT004`, `A008` |

### A007

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **33** |
| Formulation exacte | Infrastructure : Scaleway |
| Catégorie | Fournisseur d’infrastructure |
| Portée | Infrastructure Scaleway, en cohérence avec LT013 et les tableaux des deux applications. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Comparer l’architecture déployable et l’inventaire d’exploitation à la décision d’hébergement, puis qualifier les services sélectionnés. |
| Questions à examiner | 1. Quelles fonctions sont hébergées chez Scaleway et lesquelles utilisent un prestataire externe ? |
| Règles liées | `LT013`, `A008` |

### A008

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **34** |
| Formulation exacte | Isolation : Un serveur par client |
| Catégorie | Contrainte d’isolation |
| Portée | La source dit un serveur par client ; la conversation antérieure disait un serveur distinct par site. L’unité d’isolation doit être fixée. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **portée à clarifier** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Après arbitrage, contrôler la correspondance Client/Site/Instance/Serveur et tester les frontières d’accès aux données, secrets et opérations. |
| Questions à examiner | 1. Un client peut-il avoir plusieurs sites ? 2. Ces sites partagent-ils un serveur ou chacun possède-t-il son serveur ? 3. Qu’appelle-t-on serveur dans l’offre cible : instance virtuelle, machine dédiée ou autre unité explicitement choisie ? |
| Règles liées | `A001`, `A006`, `A007`, `D007` |

### A009

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **35** |
| Formulation exacte | Versionning : GitLab |
| Catégorie | Gestion des versions |
| Portée | Versionnement via GitLab ; objets versionnés et organisation des dépôts à préciser. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner les dépôts, références de versions et protections ; vérifier la traçabilité entre sources, artefacts et instances. |
| Questions à examiner | 1. Quels dépôts hébergent Workspace, Studio, moteur et modules ? 2. Comment versionner configurations, schémas et compatibilités ? |
| Règles liées | `A001`, `LT011`, `A010`, `A011` |

### A010

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **36** |
| Formulation exacte | CI/CD : Gitlab CI/CD |
| Catégorie | Chaîne de livraison |
| Portée | CI/CD GitLab, en cohérence avec LT011. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Qualifier le graphe des jobs, les droits des runners et les conditions de promotion ; faire échouer un contrôle attendu pour vérifier son effet bloquant. |
| Questions à examiner | 1. Quelles règles de branche, de validation et de cible sont applicables à la V1 ? |
| Règles liées | `LT011`, `A009`, `A011`, `A012` |

### A011

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **37** |
| Formulation exacte | Déploiement : Images Docker versionnées |
| Catégorie | Artefact de déploiement |
| Portée | Déploiements par images Docker versionnées. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Relier chaque déploiement à l’image construite et contrôlée ; proposer une identité immuable de l’artefact et vérifier qu’elle reste la même pendant sa promotion. |
| Questions à examiner | 1. Comment désigner une version : tag, digest, manifeste de release ? 2. Quand une demande de module nécessite-t-elle une nouvelle image ? |
| Règles liées | `LT012`, `A001`, `A010`, `C002` |

### A012

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **38** |
| Formulation exacte | Mises à jour : Progressives et controlées |
| Catégorie | Politique de mise à jour |
| Portée | Mises à jour progressives et contrôlées ; population pilote, rythme et critères non définis. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **portée à clarifier** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les étapes de promotion, les critères de santé et métier, les conditions d’arrêt et de reprise ; qualifier ce parcours sur une instance de test. |
| Questions à examiner | 1. Quelle instance est pilote et qui autorise la suite ? 2. Que faire après un échec de migration ou une vérification de santé défaillante ? 3. Quels changements permettent un retour arrière et lesquels demandent une procédure spécifique ? |
| Règles liées | `A010`, `A011`, `D007` |

### A013

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **39** |
| Formulation exacte | Automatisation métier : n8n en option  |
| Catégorie | Automatisation optionnelle |
| Portée | n8n en option pour l’automatisation métier. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **choix conditionnel** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Documenter le besoin et le contrat de chaque workflow n8n retenu ; vérifier ses droits, ses erreurs et sa coexistence avec les règles backend. |
| Questions à examiner | 1. Quel critère déclenche l’adoption de n8n ? 2. Comment gérer versions, accès et isolation des workflows ? |
| Règles liées | `LT010`, `D005`, `D008` |

## D — Responsabilités Django

### D001

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **96** |
| Formulation exacte | Authentification |
| Catégorie | Responsabilité applicative |
| Portée | Authentification attribuée à Django par la rubrique « Règles Django ». |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir acteurs et parcours d’authentification, puis prévoir tests de connexion, session, récupération et accès refusé adaptés aux besoins. |
| Questions à examiner | 1. Quels comptes existent dans le Studio, dans le CMS et sur les sites ? 2. Quelles identités sont distinctes ou fédérées ? |
| Règles liées | `D006`, `W007` |

### D002

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **97** |
| Formulation exacte | Formulaires métier |
| Catégorie | Responsabilité applicative |
| Portée | Formulaires métier attribués à Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Écrire les contraintes des champs, les règles de soumission et les erreurs attendues avant les tests et l’implémentation de chaque formulaire. |
| Questions à examiner | 1. Quels formulaires appartiennent à la V1 ? 2. Quelles règles de validation, de conservation et de suivi s’appliquent à chacun ? |
| Règles liées | `D005`, `D006`, `LT008` |

### D003

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **98** |
| Formulation exacte | Connexions API |
| Catégorie | Responsabilité d’intégration |
| Portée | Connexions API attribuées à Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Pour chaque connecteur retenu, vérifier le contrat, les droits, les délais, l’idempotence et la reprise après erreurs à l’aide d’essais adaptés. |
| Questions à examiner | 1. Quelles API sont entrantes ou sortantes ? 2. Quels connecteurs sont réellement nécessaires au premier lot ? |
| Règles liées | `D007`, `A013` |

### D004

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **99** |
| Formulation exacte | Modules métier |
| Catégorie | Responsabilité modulaire |
| Portée | Modules métier attribués à Django ; leur contrat commun n’est pas encore défini par ce libellé. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir un contrat de module puis examiner ses dépendances, versions, configuration, permissions, migrations et états de vie. |
| Questions à examiner | 1. Quelle différence entre module livré, installé, activé, désactivé et retiré ? 2. Comment gérer les dépendances et les données d’un module désactivé ? |
| Règles liées | `A001`, `A011`, `C002` |

### D005

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **100** |
| Formulation exacte | La logique métier |
| Catégorie | Responsabilité métier |
| Portée | Logique métier attribuée à Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Décrire les invariants métier par fonctionnalité et vérifier qu’ils restent contrôlés par le backend pour les différents points d’entrée. |
| Questions à examiner | 1. Quelles règles sont configurables et dans quelles limites ? 2. Quelle logique reste dans Django lorsqu’un workflow externe est utilisé ? |
| Règles liées | `D002`, `D004`, `D006`, `A013` |

### D006

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **101** |
| Formulation exacte | Les autorisations |
| Catégorie | Responsabilité de contrôle d’accès |
| Portée | Autorisations applicatives attribuées à Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Établir la matrice acteurs/actions/ressources et prévoir des vérifications de refus, y compris sur les appels directs aux services et API concernés. |
| Questions à examiner | 1. Quels rôles peuvent créer un site, activer un module, publier un contenu ou déclencher un déploiement ? 2. Comment limiter les identités techniques par instance et par opération ? |
| Règles liées | `D001`, `D007`, `W007`, `C002` |

### D007

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **102** |
| Formulation exacte | Les communications entre Studio et les serveurs clients |
| Catégorie | Communication de contrôle |
| Portée | Échanges entre Studio et serveurs clients, attribués à Django ; le tableau du Studio précise une API de contrôle authentifiée. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Documenter les commandes et réponses autorisées, l’authentification, les droits, l’audit et le comportement en cas de perte de réponse ; qualifier les scénarios d’erreur. |
| Questions à examiner | 1. Quel sens de connexion est retenu ? 2. Quelle identité et quels droits pour chaque instance ? 3. Comment distinguer une commande reçue, exécutée et confirmée sans la rejouer abusivement ? |
| Règles liées | `A008`, `A012`, `D003`, `D006` |

### D008

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **103** |
| Formulation exacte | Les traitements applicatifs. |
| Catégorie | Responsabilité de traitement |
| Portée | Traitements applicatifs attribués à Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Inventorier les traitements et définir leur exécution, leurs limites de ressources, leur suivi et leur reprise ; vérifier ces contrats sur le lot retenu. |
| Questions à examiner | 1. Quels traitements sont synchrones, différés ou périodiques ? 2. Quelles erreurs sont reprises, abandonnées ou soumises à arbitrage ? |
| Règles liées | `D005`, `LT010`, `A013` |

## W — Responsabilités Wagtail

### W000

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **109** |
| Formulation exacte | Wagtail ne doit pas devenir notre moteur de gestion d'infrastructure. |
| Catégorie | Interdiction de responsabilité |
| Portée | Wagtail ne doit pas devenir le moteur de gestion d’infrastructure. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Examiner la répartition des responsabilités et les actions accessibles depuis Wagtail ; vérifier que le pilotage d’infrastructure est porté par le composant prévu et ses droits dédiés. |
| Questions à examiner | 1. Quelle interface précise relie les besoins éditoriaux aux actions de gestion du Studio sans donner à Wagtail ce rôle ? |
| Règles liées | `C000`, `C001`, `D007` |

### W001

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **110** |
| Formulation exacte | Pages éditoriales |
| Catégorie | Responsabilité éditoriale |
| Portée | Pages éditoriales attribuées à Wagtail. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir types de pages et règles de publication ; prévoir des vérifications de création, édition, prévisualisation et accès selon les rôles retenus. |
| Questions à examiner | 1. Quels types de pages et quels parcours éditoriaux dans la V1 ? |
| Règles liées | `LT003`, `W005`, `W008` |

### W002

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **111** |
| Formulation exacte | Gestion des images |
| Catégorie | Responsabilité média |
| Portée | Gestion des images attribuée à Wagtail. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir formats, droits, tailles et transformations autorisés ; vérifier téléversement, accès, rendu et suppression selon le contrat retenu. |
| Questions à examiner | 1. Quel stockage d’images et quelles règles d’accès ? 2. Quelle politique s’applique aux fichiers non fiables et aux images inutilisées ? |
| Règles liées | `W003`, `W005` |

### W003

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **112** |
| Formulation exacte | Gestion des contenus |
| Catégorie | Responsabilité de contenu |
| Portée | Gestion des contenus attribuée à Wagtail ; le périmètre recoupe W006. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les objets de contenu, leur cycle de vie et leurs droits ; relier chaque objet aux vérifications éditoriales pertinentes. |
| Questions à examiner | 1. W003 et W006 doivent-ils rester deux règles distinctes ? 2. Quels contenus relèvent de Wagtail plutôt que de données métier Django ? |
| Règles liées | `W006`, `D005` |

### W004

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **113** |
| Formulation exacte | Composition des pages |
| Catégorie | Responsabilité de composition |
| Portée | Composition des pages attribuée à Wagtail. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les blocs et assemblages permis ; vérifier les contraintes de composition, les valeurs invalides et les variations de thème prévues. |
| Questions à examiner | 1. Quels blocs sont disponibles et quelles contraintes régissent leur assemblage ? |
| Règles liées | `W008`, `A004`, `LT007` |

### W005

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **114** |
| Formulation exacte | Administration éditoriale |
| Catégorie | Responsabilité d’administration |
| Portée | Administration éditoriale attribuée à Wagtail. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir le périmètre de l’administration éditoriale et les permissions ; examiner les parcours des éditeurs et les actions refusées. |
| Questions à examiner | 1. Qui édite et qui publie ? 2. Quelles actions restent réservées à l’administration du Studio ? |
| Règles liées | `W000`, `W007`, `D006` |

### W006

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **115** |
| Formulation exacte | Les contenus |
| Catégorie | Responsabilité de contenu |
| Portée | Les contenus sont attribués à Wagtail ; le libellé ne précise pas une responsabilité distincte de W003. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Faire correspondre ce libellé à un périmètre explicite ou documenter son lien avec W003, en conservant la traçabilité de l’identifiant. |
| Questions à examiner | 1. S’agit-il d’un doublon de W003 ou d’une distinction entre stockage des contenus et leur gestion ? |
| Règles liées | `W003`, `W001` |

### W007

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **116** |
| Formulation exacte | Les utilisateurs du CMS |
| Catégorie | Responsabilité d’identité éditoriale |
| Portée | Utilisateurs du CMS attribués à Wagtail, en articulation avec l’authentification et les autorisations Django. |
| Origine de la portée | explicite par la rubrique de la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les rôles CMS et leur relation aux comptes Django/Studio ; vérifier les permissions éditoriales et la séparation des accès aux instances. |
| Questions à examiner | 1. Un utilisateur du Studio est-il automatiquement un utilisateur CMS ? 2. Comment déléguer, retirer et auditer les accès d’un client à son CMS ? |
| Règles liées | `D001`, `D006`, `W005`, `A008` |

### W008

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **117** |
| Formulation exacte | Assemblage de page avec StreamField |
| Catégorie | Mécanisme de composition éditoriale |
| Portée | Assemblage des pages avec StreamField. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir les blocs, schémas et règles de validation ; examiner leur rendu et les conséquences d’une évolution de schéma sur les contenus existants. |
| Questions à examiner | 1. Quelles compatibilités et migrations pour les blocs modifiés ou supprimés ? 2. Comment versionner les composants utilisés par un contenu déjà publié ? |
| Règles liées | `W004`, `A001`, `A012` |

## C — Cadrage

### C000

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **123** |
| Formulation exacte | Notre Studio central serait une application en Django indépendante. |
| Catégorie | Proposition de découpage |
| Portée | Studio central envisagé comme une application Django indépendante ; le conditionnel est conservé. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **proposition source** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Après arbitrage, comparer le découpage retenu aux responsabilités et cycles de vie attendus ; préciser l’indépendance applicative, de déploiement et de données. |
| Questions à examiner | 1. Indépendante de quels composants et à quels niveaux ? 2. Quels objets et quelles actions appartiennent à la V1 du Studio central ? |
| Règles liées | `LT002`, `A001`, `D007`, `W000` |

### C001

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **124** |
| Formulation exacte | Wagtail serait principalement installé sur les serveurs distants |
| Catégorie | Proposition de répartition |
| Portée | Wagtail envisagé principalement sur les serveurs distants ; « serait » et « principalement » n’excluent pas toute exception. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **proposition source** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Après clarification, cartographier les installations Wagtail et contrôler leur rôle éditorial ainsi que leur relation au Studio. |
| Questions à examiner | 1. Existe-t-il un besoin Wagtail dans le Studio central ? 2. Que désigne précisément « principalement » dans l’architecture cible ? |
| Règles liées | `LT003`, `A003`, `W000`, `A008` |

### C002

| Champ | Valeur |
|---|---|
| Source | `Texte collé(8).txt`, ligne **125** |
| Formulation exacte | Ne pas laisser le générateur installer automatiquement des composants en production |
| Catégorie | Interdiction de mutation de production |
| Portée | Le générateur ne doit pas installer automatiquement des composants en production ; le terme générateur et les opérations visées doivent être précisés. |
| Origine de la portée | explicite dans la source |
| Statut de décision | **exigence exprimée** |
| Mise en œuvre | non audité dans ce dossier |
| Preuve de vérification | non établie |
| Moyen de contrôle **PROPOSÉ** | Définir le point de passage autorisé pour les changements de code et vérifier les droits effectifs des générateurs, agents et pipelines ; prévoir un essai montrant qu’une installation directe non autorisée est refusée. |
| Questions à examiner | 1. Le générateur désigne-t-il l’agent de développement, un constructeur UI ou une fonction du Studio ? 2. Quelles validations autorisent une livraison CI/CD ? 3. Comment distinguer installation de code, migrations, activation d’un module déjà livré et modification de configuration ? |
| Règles liées | `D004`, `D006`, `A010`, `A011` |

## Portée des contrôles de ce livrable

La vérification effectuée pour ce document porte uniquement sur l’exhaustivité du registre : 47 IDs uniques, association fidèle aux lignes et formulations source, cohérence des références entre IDs et présence des champs requis. Elle ne vérifie ni le code du prototype, ni les protections du Workspace, ni GitLab, Notion ou Scaleway.

Les exigences fermes W000 et C002 restent des interdictions exprimées. Leurs contrôles effectifs sont à concevoir puis à vérifier ; le présent classement ne les active pas. C000 et C001 restent des propositions source au conditionnel. Les options n8n, GSAP et la sélection de composants UI ne deviennent pas obligatoires par leur présence dans la liste de technologies.
