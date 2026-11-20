# FEAT-002 — Clients et sites

**Résultat attendu.** Depuis son espace privé, un opérateur retrouve les clients et sites qui lui sont confiés. Il peut créer ou tenir à jour les fiches dans la limite de ses habilitations. La création enregistre une fiche locale. [Décisions métier validées dans le Kanban](https://app.notion.com/p/41c49e23bbdb81ed98b0c5d404d27dbf).

## Règles adoptées avec l’utilisateur

Un client est une entreprise, une association ou un particulier. Son type sert à décrire la fiche. Chaque client peut détenir plusieurs sites et avoir plusieurs contacts. Chaque contact et chaque site appartiennent à un seul client. Un site possède son propre contexte logique indépendamment du serveur qui pourrait l’héberger. Son domaine est facultatif et peut être complété plus tard.

Un contact possède un nom, un seul rôle principal en texte libre et au moins une coordonnée parmi courriel et téléphone. Plusieurs contacts peuvent avoir le même rôle. Référencer un contact ne crée aucun compte. Un collaborateur de l’équipe Studio utilise un compte opérateur avec des habilitations ciblées.

L’archivage d’un client retire sa fiche des listes courantes. Les sites, leur disponibilité, leur contexte et leurs habilitations sont conservés. La réactivation rend la même fiche à nouveau visible parmi les actifs. Le parcours ordinaire comporte la création, la consultation, la modification et l’archivage administratif. Les demandes d’effacement suivent une procédure distincte. Les données réelles sont réservées à l’exploitation après préparation de cette procédure.

## Proposition de parcours

- **Clients.** Ouvrir la liste des clients accessibles, rechercher par nom, filtrer par type et basculer entre actifs et archivés. Créer un client, consulter sa fiche, corriger ses renseignements et administrer ses contacts selon la matrice de droits. La fiche affiche uniquement les sites pour lesquels l’opérateur possède un droit.
- **Sites.** Depuis un client actif autorisé, créer une fiche en indiquant seulement le nom. Depuis « Mes sites », retrouver ses sites habilités, y compris quand le client est archivé. Un opérateur limité à un site consulte sa fiche sans accéder à l’annuaire des contacts ni aux sites voisins.
- **Modification et archivage.** Afficher les erreurs près des champs et conserver les valeurs valides. Demander confirmation pour archiver ou réactiver. Proposition pour une fiche archivée : consultation et réactivation possibles, modifications de la fiche client, des contacts et créations d’enfants suspendues. Les sites existants restent modifiables selon leurs propres droits.
- **Données minimales.** Le premier formulaire client demande type et nom d’affichage. Les coordonnées individuelles se saisissent sur les contacts. Les champs administratifs (adresse, SIRET, RNA, etc.) restent facultatifs dans le cadrage métier et leur collecte attend une finalité établie. Une fiche Site peut recevoir un type, une description ou un domaine.

Les fiches techniques, la facturation, les comptes clients, le CMS, les modules, le DNS, l’hébergement et le déploiement relèvent de travaux ultérieurs. Le modèle futur distinguera le serveur et la fiche technique propre au site. Les secrets restent dans le coffre externe et les opérations SSH sont réalisées manuellement hors Studio.

## Critères d’acceptation pour la réalisation

| ID | Scénario vérifiable |
|---|---|
| AC1 | Créer et retrouver un client de chacun des trois types. Les noms identiques sont acceptés. Un nom vide ou un type inconnu est refusé. |
| AC2 | Enregistrer deux sites du même client, dont un sans domaine. Modifier le domaine de l’un sans toucher à l’autre. La fiche créée ne déclenche aucune opération technique. |
| AC3 | Créer deux contacts de même rôle chez un client. Accepter courriel seul, téléphone seul ou les deux. Refuser un canal invalide ou le retrait de la dernière coordonnée. Aucun compte opérateur n’est créé. |
| AC4 | Archiver puis réactiver un client. Vérifier listes, recherche et restrictions de la fiche archivée, conservation des UUID, des contacts et de l’accès direct aux sites autorisés. |
| AC5 | Un opérateur habilité au seul site A ne retrouve ni le site frère B ni les contacts de leur client. Un gestionnaire limité à A peut modifier A, annuler et revenir à A sans révéler le client. Un gestionnaire client ne voit aucun site sans habilitation correspondante. Contrôler aussi recherches, sélecteurs, compteurs et suggestions. |
| AC6 | Refuser une écriture avec un mandat de lecture, un parent incohérent, une tentative de réaffectation ou un droit révoqué. Appliquer les mêmes contrôles sur URL directe, formulaire et service. Une session expirée renvoie à la connexion. |
| AC7 | Une erreur d’écriture annule la création de l’objet et du mandat initial ensemble. Deux éditions simultanées signalent le conflit sans écraser la première. Une validation échouée conserve la version enregistrée. |
| AC8 | Migrer une base au niveau FEAT-001 puis relancer les migrations. Comptes, sessions et groupes existants sont préservés. Le registre est vide et aucun droit métier n’est automatiquement attribué. |
| AC9 | En navigateur, parcourir au clavier les listes, fiches, formulaires, confirmations et retours. Examiner listes vides, absence de résultat, erreur de contact, noms longs et petit écran avec des données fictives. |
| AC10 | Avant utilisation réelle, attribuer les responsabilités, fixer les critères de conservation et exercer une demande fictive de droits jusqu’à la réponse et au suivi des copies. Vérifier les journaux et les traces. |

La [conception technique](ARCHITECTURE.md), la [matrice des droits](SECURITY.md), la [procédure données personnelles](PROTECTION-DONNEES.md), le [plan](TASKLIST.md) et les [maquettes](VISUAL-REVIEW.md) constituent le dossier de préparation. Les choix d’implémentation proposés se distinguent des décisions métier déjà adoptées.
