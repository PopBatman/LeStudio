# FEAT-002 — Clients et sites

Le mandat du 18 novembre 2026 porte sur la préparation du lot dans le Studio central. Le [cadrage métier du Kanban](https://app.notion.com/p/41c49e23bbdb81ed98b0c5d404d27dbf) est traduit en dix [critères d’acceptation](SPEC.md). L’[inventaire](RESEARCH.md) précise ce que fournissent FEAT-001 et UI-001.

| Livrable de cadrage | Résultat |
|---|---|
| [Modèle et migrations](ARCHITECTURE.md) | Champs requis et facultatifs, normalisation, homonymes, rattachements, contraintes PostgreSQL, transactions et passage depuis FEAT-001. |
| [Habilitations](SECURITY.md) | Le groupe opérateur ouvre Studio. Deux mandats distincts limitent la consultation et la gestion des clients et des sites. La capacité de créer un client est attribuée explicitement. |
| [Données personnelles](PROTECTION-DONNEES.md) | Proposition de procédure pour recevoir et traiter une demande, gérer les copies et suivre les échéances. Le responsable, le canal, les durées ou critères de conservation et l’exercice sur données fictives sont à finaliser avant utilisation réelle. |
| [Plan de réalisation](TASKLIST.md) | Ordre des travaux, dépendances, responsabilités prévues et contrôles à produire. |
| [Maquettes](evidence/maquettes.html) | Parcours de liste, fiche et formulaire avec variantes de droits, erreurs et archive. L’[examen du support](evidence/examen-maquettes.json) conserve le périmètre visuel et les résultats sur deux formats. |
| [Relecture](REVIEW.md) | Relecture indépendante de la concordance du dossier de conception avec les règles du Kanban. |

Le groupe de travail a réuni `/root` pour le cadrage et la concordance documentaire, `/root/cadrage_droits` pour l’inventaire des habilitations, `/root/cadrage_donnees` pour la procédure sur les données personnelles et `/root/cadrage_maquettes` pour le support visuel. La [révision du dossier](task.json) distingue les références illustratives des futures preuves de fonctionnement.

Le cadrage ci-dessus a précédé le mandat de développement. Les résultats de la réalisation sont détaillés ci-dessous.

## Réalisation locale

L’espace privé propose les entrées **Clients** et **Mes sites**. L’opérateur peut créer, consulter et modifier les fiches autorisées, renseigner des contacts et archiver ou réactiver un client. Les mandats de lecture et de gestion sont indépendants pour chaque client et chaque site. La [commande d’attribution](../../../docs/REGISTRE.md) gère aussi le droit de créer le premier client.

| Critères | Qualification |
|---|---|
| AC1–AC4 | Modèles et contraintes, normalisation, coordonnées obligatoires, homonymes, plusieurs sites et archivage administratif. Le parcours Chromium crée un client, corrige un contact invalide, crée un site sans domaine, archive puis réactive le client. |
| AC5–AC7 | Tests des mandats, absence de données du client chez le gestionnaire d’un seul site, refus de changer le rattachement, absence d’écriture partielle et éditions concurrentes dans deux connexions PostgreSQL. |
| AC8 | Migration additive exercée sur une base PostgreSQL au niveau FEAT-001 avec utilisateur, groupe et session préexistants. Vérification du registre vide et de l’absence de droits métier ajoutés. Second passage des migrations et contrôle du schéma. |
| AC9 | Captures Chromium du parcours réel en 1440 × 960 et 390 × 844, contrôle clavier, recherche vide, messages de validation et revérification avec un libellé long. |
| AC10 | Exercice technique sur deux contacts fictifs homonymes. Contrôle de la copie ciblée, effacement dans un client archivé et réapplication sur une base restaurée depuis une sauvegarde PostgreSQL. Les sites et le contact de l’autre client restent présents. |

Les fonctions d’exploitation impliquant des personnes réelles requièrent toujours un responsable, un canal de réception, une politique de conservation et une validation organisationnelle. Les essais et les captures portent sur des données fictives. Voir la [procédure](PROTECTION-DONNEES.md) et les [preuves de développement](EVIDENCE.md).

Les agents `/root/registre_backend`, `/root/registre_web` et `/root/registre_admin` ont réalisé le métier, l’interface et la commande de maintenance. `/root` a intégré et vérifié la pile Docker. `/root/registre_revue` a assuré la revue indépendante.
