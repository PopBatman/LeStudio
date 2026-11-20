# Capacités du Workflow AI

Ce tableau décrit le paquet livré. Le [rapport de livraison v1.0.0](../evidence/DELIVERY-REPORT.md) conserve les vérifications effectuées sur la version d’origine. La version 1.1 installe les outils et le projet dans deux dossiers frères. Un fichier de configuration ou une instruction ne prouve pas qu’un service externe fonctionne.

| Capacité | Livré | Limite et raccordement |
|---|---|---|
| Processus feature/connecteur/UI | Contrats, étapes, modèles et critères de sortie | À appliquer au besoin réel de chaque lot |
| Installation | Script sans dépendance, simulation, contrôle des conflits, conservation des instructions existantes | L’installation crée les dossiers `workflow-ai/` et `studio/` sous la racine choisie |
| Dossiers de travail | CLI `new`, `status`, `check`, `fingerprint` | Pas de planificateur autonome ni de gestion multi-exécuteurs |
| Autorisations | Mandat documenté, actions et chemins déclarés ; contrôles de présence/cohérence | Pas d’identité d’approbateur signée, de sandbox ou de contrôle de toutes les commandes du système |
| Transitions | Vérifications locales retournant un code d’échec lorsque leurs prérequis manquent | Aucun moteur de transitions serveur ; un agent peut modifier les fichiers s’il en a les droits |
| Sous-agents | Rôles, contrat de délégation, périmètres et revue indépendante | Le runtime doit réellement exposer la délégation ; aucun agent n’est créé par un fichier Markdown |
| Maquettes | Brief, états, décisions et preuve avant les changements UI | Génération dépendante de l’outil d’image/design disponible ; aucune clé ni image fictive de preuve livrée |
| Screenshots | Matrice de captures, contexte et procédure de qualification | Navigateur à raccorder ; aucune capture de Studio prétendue dans cette livraison |
| Notion | Projection documentaire Python, allowlist, révisions et registre de reprise ; publication de session via connexion interactive | Le jeton REST local reste à configurer ; ses écritures réelles restent à qualifier séparément |
| GitLab | Fragment CI local pour vérifier les outils du workflow et guide de raccordement | Runner, branche protégée, droits, secrets et politique de fusion à configurer sur le dépôt choisi |
| Mémoire | Sources, décisions, rapports, preuves et règles versionnés | Pas de base vectorielle, de recherche sémantique autonome ou de synchronisation bidirectionnelle |
| Produit Studio | Lot ARCH-001 préparé | Aucun produit, module catalogue, serveur ou déploiement installé par le workflow |

## Ce qu’une vérification prouve

Un fichier de preuve ayant le SHA256 attendu prouve que ses octets concordent avec le registre. Une empreinte de contrat et des empreintes d’entrées concordantes permettent de détecter certains changements postérieurs. Elles ne prouvent pas que le contenu est honnête, que le test est pertinent ou qu’un humain a approuvé le lot.

Les contrôles portent sur les fichiers déclarés, pas sur l’exhaustivité des dépendances du comportement testé. Les preuves actives doivent rester conformes au contrat et aux sources courantes ; l’historique inactif ne satisfait aucun contrôle. Un échec actif ne peut pas être neutralisé par un autre résultat réussi.

Une revue déclarée indépendante doit correspondre à une exécution distincte observable. Le CLI vérifie la déclaration et les preuves fournies ; il n’authentifie pas les personnes ou agents. Les protections GitLab et les permissions d’outils apportent une autre couche, à configurer sans donner aux agents le pouvoir de contourner leur propre contrôle.

## Hors périmètre

Lancement durable de jobs agentiques, moteur d’autorisation central, transitions transactionnelles, authentification forte des approbateurs, bus d’événements, coffre de secrets, service de déploiement et qualification de tous les connecteurs. Ce sont des chantiers à spécifier, pas des fonctionnalités obtenues en installant ce dossier.
