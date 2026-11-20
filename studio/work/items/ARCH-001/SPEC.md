# ARCH-001 — Fondation technique du Studio central

Le lot porte sur le Studio central local. Le suivi courant figure dans [le registre du lot](task.json) et les résultats dans [le rapport](REPORT.md).

| Champ | Valeur |
|---|---|
| Type | Architecture |
| Objectif | Préparer et installer la base technique minimale de Studio dans le dépôt cible |
| Priorité | Première étape produit indiquée par l’utilisateur, après installation du Workflow |
| Interface utilisateur | Non requise dans le périmètre décrit |
| Environnement | Poste Linux local, dossier `studio/` |
| Mandat d’implémentation | Instruction de lancement du 18 novembre 2026, consignée dans `task.json` |
| Responsable d’exécution | Codex, exécution principale `/root` |

## 1. Résultat attendu

Un développeur peut démarrer le Studio central Django avec PostgreSQL dans un environnement Docker local, exécuter les migrations et les vérifications documentées, puis poursuivre le développement selon les contrats feature/connecteur/UX-UI.

La structure reste minimale. Les emplacements des responsabilités sont explicites ; les modules futurs ne sont pas tous générés.

## 2. Périmètre

| Inclus | Résultat |
|---|---|
| Audit de l’existant | Fichiers et conventions utiles identifiés, écarts recensés, conservation du travail existant |
| Qualification de la stack | Versions compatibles sourcées puis verrouillées |
| Structure applicative | Entrée Django centrale, paramètres, routage technique et responsabilités documentées |
| PostgreSQL | Base locale, migrations et contrôles pertinents |
| Docker local | Construction et démarrage reproductibles, services et volumes identifiés |
| Configuration | Variables attendues validées, exemple sans valeurs secrètes |
| Signal technique | Réponse minimale permettant de vérifier le démarrage, sans écran produit |
| Qualité et CI | Contrôles locaux et fichier GitLab CI minimal cohérents |
| Documentation | Démarrage, arrêt, configuration, reprise locale et preuves |

Les limites suivantes restent explicites : aucune fonction métier de client, aucun Contact présélectionné, aucune intégration fournisseur réelle, aucun déploiement distant, aucune publication de registre, aucun push et aucun changement de protection GitLab. L’accès autonome des clients et les écrans de Studio seront spécifiés dans leurs lots.

Le moteur Wagtail reste une responsabilité du produit. Ce lot précise son interface et sa compatibilité ; son installation dans le processus central n’est pas supposée nécessaire. Tout démarrage d’un moteur séparé ajouté au lot doit être explicite dans sa tasklist et ses critères.

## 3. Critères d’acceptation

| ID | Critère | Preuve attendue lors de la réalisation |
|---|---|---|
| AC-01 | L’existant est recensé avant modification et les fichiers hors périmètre sont préservés | Inventaire ciblé, différences et justification des changements |
| AC-02 | Les versions retenues sont compatibles et verrouillées | Références primaires datées, fichiers de dépendances et résultat d’installation |
| AC-03 | Studio central utilise Django et sa base de vérification est PostgreSQL | Configuration résolue sans secret affiché, contrôles de connexion et tests sur PostgreSQL |
| AC-04 | L’image applicative se construit et les services locaux démarrent selon la documentation | Commandes exactes, codes retour, identités d’artefacts et états observés |
| AC-05 | Les migrations s’appliquent sur une base de test neuve et un second passage reste cohérent | Résultats des deux opérations sur un volume jetable identifié |
| AC-06 | Un signal technique répond sans exposer secret, configuration détaillée ou données métier | Vérification HTTP et inspection du contenu |
| AC-07 | Les paramètres indispensables sont validés et une configuration invalide produit une erreur exploitable | Scénario de configuration correcte et scénario de refus |
| AC-08 | Aucun secret réel ni compte administrateur à mot de passe fixe n’entre dans le code ou les exemples | Revue des fichiers et contrôle adapté |
| AC-09 | Les contrôles de qualité pertinents sont reproductibles localement et décrits dans la CI | Résultats locaux ; exécution distante signalée séparément si non réalisée |
| AC-10 | Les frontières feature/connecteur/UI sont lisibles sans modules métier artificiels | Revue de la structure et des responsabilités |
| AC-11 | La documentation permet à un autre opérateur de démarrer le périmètre et connaître ses limites | Relecture et reproduction locale lorsque l’environnement le permet |
| AC-12 | Le rapport relie les preuves à la révision et distingue contrôles exécutés, non applicables et ouverts | Rapport et preuves exacts, revue indépendante selon les moyens disponibles |

Le signal technique n’est pas une promesse de disponibilité de modules métier. Un pipeline décrit mais non exécuté sur GitLab reste une configuration à qualifier.

## 4. Données et sécurité

Utiliser uniquement des données locales de test. Les noms de variables peuvent être documentés ; leurs valeurs secrètes restent dans le mécanisme local autorisé. Les commandes de diagnostic ne doivent pas imprimer l’environnement complet.

Les volumes et ressources de test sont identifiables et distincts des données existantes. Aucun nettoyage destructif de données existantes n’est implicite dans le mandat. Les bases de vérification sont réellement PostgreSQL ; l’absence du service ne se contourne pas en remplaçant silencieusement la base par SQLite.

## 5. UX/UI

**Non applicable pour ce périmètre technique.** Aucun écran métier, design final ou éditeur n’est annoncé. Un endpoint technique peut être vérifié par HTTP sans maquette.

Si une interface est ajoutée, modifier le périmètre et le statut UI, décrire les états et produire les maquettes avant son implémentation. Les screenshots de vérification seront ensuite capturés sur une version réellement exécutée.

## 6. Dépendances avant implémentation

Les chemins autorisés et le mandat figurent dans [task.json](task.json). Les choix locaux sont documentés dans [ARCHITECTURE.md](ARCHITECTURE.md) et [SECURITY.md](SECURITY.md).
