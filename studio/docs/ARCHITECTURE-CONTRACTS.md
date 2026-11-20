# Contrats d’architecture : features, connecteurs et UX/UI

Version du Workflow : 1.0 • Date : 18 novembre 2026.

**Ces conventions organisent le développement dans le Workflow AI.** Elles s’appliquent au périmètre mandaté. Les noms de domaines, chemins et exemples sont illustratifs ; ils ne sélectionnent pas un premier module et ne figent pas tous les choix du produit.

## 1. Trois contrats et une responsabilité commune

| Élément | Ce qu’il porte |
|---|---|
| Feature | Résultat utilisateur, règles métier, permissions, données et critères d’acceptation |
| Connecteur | Traduction d’une capacité applicative vers un système extérieur, avec ses garanties et erreurs |
| Composant UX/UI | Présentation, interactions, variantes et états d’un parcours |

Une **feature** est une évolution livrée. Une **application Django** regroupe le code d’une responsabilité cohérente. Un **module activable** est une capacité sélectionnable pour un site, avec configuration, compatibilité et cycle de vie. Ces notions ne se correspondent pas systématiquement une à une.

Le backend compétent applique les décisions métier. Le connecteur adapte les échanges. Le composant présente les données et déclenche les interactions prévues. Les tâches internes utilisent les mêmes contrats que le web.

## 2. Contrat de feature

### Fiche préalable

Avant d’implémenter un comportement, préciser le besoin, les acteurs, le périmètre, les données, les permissions, les invariants, les états, les erreurs et les scénarios d’acceptation. Identifier les effets externes et les changements de schéma.

| Question | Exemple de réponse à obtenir |
|---|---|
| Qui agit ? | Acteur et contexte du site explicitement identifiés |
| Quelle ressource change ? | Propriétaire des données et périmètre accessible |
| Quelles conditions ? | Préconditions, état initial et permissions |
| Quel résultat ? | État obtenu et effets attendus |
| Quel échec ? | Refus, conflit, résultat incertain ou reprise |
| Quelle preuve ? | Scénario observable, test ou vérification adaptée |

Une règle ne dépend pas exclusivement du formulaire HTTP : un appel interne, une commande ou une tâche doit respecter le même invariant.

### Structure Django

| Emplacement indicatif | Responsabilité |
|---|---|
| `apps/<domaine>/models.py` | Données, relations, contraintes structurelles et comportements propres aux objets |
| `services.py` | Cas d’usage, autorisations, transitions, transactions et orchestration |
| `permissions.py` | Règles d’accès réutilisables |
| `selectors.py`, si utile | Lectures complexes ou partagées, limitées au contexte autorisé |
| `forms.py` ou schémas d’entrée | Adaptation et validation des données reçues |
| `views.py` | Traduction HTTP, appel du service, réponse ou rendu |
| `templates/` | Écrans et fragments du domaine |
| `migrations/` | Évolution des structures et données |
| `tests/` | Comportements, permissions et intégration |

Créer ces éléments selon les responsabilités réelles. Une petite feature n’exige pas plusieurs couches abstraites. Un domaine modifiant les données d’un autre passe par son contrat public, plutôt que par des écritures dispersées.

### Validation et contexte

Le navigateur aide à prévenir les erreurs ; les entrées sont validées à leur arrivée ; les services vérifient les règles et permissions ; la base protège les contraintes structurelles pertinentes. Les lectures et écritures reçoivent un acteur et un contexte de ressource explicites.

Le comportement concurrent est défini : rejet d’une révision périmée, verrouillage approprié ou autre stratégie justifiée. Les signaux implicites ne doivent pas rendre les effets distants essentiels difficiles à identifier et à reprendre.

Pour une feature de Studio, le central possède ses opérations et données. Une capacité métier d’un site est portée par le moteur propriétaire des données correspondantes. Lorsqu’une feature traverse cette frontière, décrire commandes, réponses, authentification, compatibilité et résultat incertain. Le serveur physique commun ne détermine pas cette propriété logique.

### Modules activables

Le module expose identité, compatibilité moteur, dépendances, permissions, schéma de configuration, points d’interface et devenir des données. Un manifeste YAML ou une définition Python contrôlée peut porter ces informations ; il reste déclaratif.

Distinguer livraison de code, préparation du schéma, activation, configuration, désactivation et retrait. Une désactivation ne supprime pas implicitement les données. Un champ de configuration n’installe pas un paquet et ne devient pas du code arbitraire.

## 3. Contrat de connecteur

### Capacité et fournisseur

Commencer par une opération précise : envoyer un message, lire des disponibilités, transmettre une facture ou suivre une opération. Le nom du fournisseur ne suffit pas à définir le périmètre.

| Élément | Rôle |
|---|---|
| Service métier | Décider pourquoi agir, sur quelles données et avec quelles permissions |
| Contrat de capacité | Définir les entrées, résultats, erreurs et garanties attendus |
| Adaptateur | Traduire ce contrat vers le fournisseur |
| SDK éventuel | Détail interne de l’adaptateur |
| Connexion configurée | Compte, portée site/client, paramètres et références de secrets |

Un contrat substituable peut utiliser une interface typée telle qu’un `Protocol`. Les données restent validées à l’exécution. Les types et exceptions du fournisseur sont normalisés à la frontière.

Les capacités communes répondent à des usages identifiés. Les fonctionnalités propres à un fournisseur restent explicites ; on ne prétend pas que tous les fournisseurs offrent les mêmes garanties.

### Structure du connecteur

| Partie | Contenu |
|---|---|
| Contrat | Types, opérations, résultats et erreurs |
| Configuration | Schéma versionné, paramètres, scopes et références de secrets |
| Client fournisseur, si utile | Transport, authentification, limites et réponses brutes |
| Adaptateur | Traduction vers le contrat applicatif |
| Événements entrants | Vérification, déduplication et transmission au cas d’usage |
| Métadonnées | Capacités supportées, compatibilité et limites |
| Vérifications | Tests de contrat, simulations et qualification réelle ciblée |

Le code est livré par une version contrôlée. La sélection dans Studio associe une configuration à du code disponible. Implémentation, configuration d’un compte et qualification du compte réel sont suivies séparément.

### Droits et configuration

Les identités et secrets sont limités aux comptes, sites et opérations nécessaires. Les réglages affichables contiennent des références ; les valeurs secrètes n’apparaissent pas dans les erreurs, journaux, prompts ou exports documentaires.

Les destinations sont connues ou validées. Un paramètre ne doit pas permettre de détourner librement une requête vers une ressource interne. Délais, pagination, taille et volume sont bornés. Les journaux relient opération, tentative et référence distante en minimisant les données sensibles.

Une vérification de connexion privilégie un contrôle sans effet métier, quand il existe. Elle décrit ce qu’elle prouve. Un envoi ou une création de test est une action distincte, identifiée et comprise dans le mandat applicable.

### Résultats, erreurs et reprises

| Situation | Comportement attendu |
|---|---|
| Demande acceptée | Enregistrer la référence et l’état observé ; distinguer acceptation et résultat final |
| Authentification/configuration invalide | Diagnostic exploitable sans fuite de secret |
| Capacité absente | Refus explicite, avec indication du prérequis manquant |
| Erreur définitive | Échec expliqué, sans répétition automatique |
| Erreur temporaire ou limitation | Reprise bornée lorsque l’opération et le contrat le permettent |
| Délai dépassé après l’envoi | Résultat potentiellement incertain ; rechercher l’état distant ou utiliser l’idempotence supportée |
| Réponse inattendue | Erreur normalisée et diagnostic corrélé |

Une clé d’idempotence ne crée pas une garantie chez un fournisseur qui ne la supporte pas. La reprise inclut délais, limites, concurrence, abandon et intervention humaine utile.

### Transaction et effet extérieur

L’action d’un fournisseur n’appartient pas à la transaction PostgreSQL. Django permet de différer un callback avec `on_commit()` ; son échec après commit n’annule pas la transaction. Ce callback ne constitue pas, à lui seul, une file durable. Voir la [documentation Django sur les transactions](https://docs.djangoproject.com/en/5.2/topics/db/transactions/).

Si une intention doit survivre à un arrêt, l’enregistrer dans la même transaction que les données métier, puis la faire traiter séparément. Ce mécanisme d’outbox transactionnelle conserve l’intention ; il ne garantit pas universellement une exécution exactement une fois. Spécifier la prise en charge concurrente, les tentatives, les doublons et la réconciliation. Le besoin détermine l’outil d’exécution ; aucune file particulière n’est imposée par ce contrat.

### Webhooks

Authentifier selon le mécanisme réel du fournisseur, vérifier le rattachement au compte et au site, valider les données et limiter leur taille. Prévoir rejeux, doublons et événements reçus hors ordre. Un événement authentifié n’obtient pas de privilèges supplémentaires.

Pour un traitement différé, accuser réception après une prise en charge durable, puis appliquer les règles par le service compétent. Stripe documente par exemple les livraisons en double ; cette garantie doit être étudiée pour chaque fournisseur : [webhooks Stripe](https://docs.stripe.com/webhooks).

### Place de n8n

n8n peut organiser des échanges lorsqu’il apporte une valeur identifiée. Les invariants, permissions et états métier de référence restent contrôlés par les services. Un workflow externe respecte les mêmes droits qu’un autre point d’entrée.

## 4. Contrat UX/UI

### Concevoir le parcours et les niveaux de composants

L’UX précise l’ordre des actions, les informations utiles, les erreurs et la récupération. L’UI réalise ce parcours avec des éléments de présentation.

| Niveau | Exemples | Propriété |
|---|---|---|
| Fondations | Couleurs, typographies, espacements, contrastes et mouvements | Design system |
| Primitives | Bouton, champ, lien, badge, icône | Bibliothèque commune |
| Composés | Dialogue, groupe de champs, pagination, tableau | Bibliothèque commune lorsque l’usage est générique |
| Métier | Carte de site, état de module, résumé d’opération | Domaine concerné |
| Écrans | Atelier, catalogue, connexions, activité | Feature et parcours |

Studio et les sites peuvent partager des mécanismes et des primitives tout en conservant thèmes et compositions adaptés à leurs usages.

### Fiche de composant

Décrire usage, propriétés et types attendus, valeurs par défaut, variantes autorisées, emplacements de contenu, états, événements, clavier, focus et adaptation aux petits écrans. Ajouter textes longs, contenu absent et réduction des animations lorsque pertinents.

Cotton fournit des attributs et slots pour composer les templates : [composants Cotton](https://django-cotton.com/docs/components). Les composants métier restent proches de la feature ; les primitives partagées ne connaissent pas ses décisions.

| Technologie | Responsabilité |
|---|---|
| Django | Données, permissions, validation et réponses |
| Templates / Cotton | Composition et rendu |
| Tailwind | Styles, tokens et variantes |
| HTMX | Interactions serveur et remplacement de fragments définis |
| Alpine | État local temporaire |
| Wagtail | Données éditoriales, composition et liaison au rendu |

shadcn-django s’appuie sur Cotton. Les composants retenus sont revus puis maintenus avec leurs dépendances et obligations applicables : [dépôt du projet](https://github.com/SarthakJariwala/shadcn-django).

### Rendu, thèmes et fragments

Les composants reçoivent des données préparées. Ils ne réalisent pas d’écriture métier ou d’appel fournisseur caché pendant un rendu. Les permissions serveur restent effectives même si l’interface masque ou désactive une action.

Les réglages de thème utilisent des variantes connues, tokens ou variables CSS contrôlées et des valeurs validées. Ils n’autorisent pas l’injection libre de HTML, JavaScript ou CSS. Le contenu riche suit une politique de rendu définie.

Tailwind détecte les classes dans les sources ; conserver des noms complets plutôt que les fabriquer par fragments au runtime : [détection des classes](https://tailwindcss.com/docs/detecting-classes-in-source-files).

Le contrat HTMX précise cible du fragment, données, statut HTTP, erreurs, session expirée, double soumission et focus. Si une erreur de validation utilise le statut 422, prévoir explicitement le remplacement du fragment correspondant. Les protections CSRF et permissions du serveur restent appliquées. Voir la [documentation HTMX](https://htmx.org/docs/).

### Wagtail et composants

Un bloc Wagtail définit des données éditoriales. Son template les relie aux composants de présentation. Les blocs peuvent disposer de templates dédiés : [StreamField](https://docs.wagtail.org/en/stable-7.4.x/topics/streamfield.html).

Le changement d’un bloc ou de ses variantes doit considérer les contenus déjà enregistrés. La composition éditoriale ne devient pas un gestionnaire d’infrastructure ou un client fournisseur dissimulé.

### Vérification

Une galerie interne présente les variantes et états utiles. Vérifier le rendu réel, les petits écrans, les erreurs, le clavier et le focus. Pour un dialogue modal, examiner ouverture, navigation interne, fermeture et retour de focus conformément au parcours : [guide APG du W3C](https://www.w3.org/WAI/ARIA/apg/patterns/dialog-modal/).

Les captures complètent les tests ; elles ne démontrent pas seules l’accessibilité ou le fonctionnement. Les retouches visuelles simples reçoivent une vérification proportionnée.

## 5. Cycle commun et preuves

| Palier | Feature | Connecteur | UX/UI |
|---|---|---|---|
| Recherche | Besoin et domaine | Documentation et garanties | Parcours, références, accessibilité |
| Spécification | Règles, données, droits, erreurs | Contrat, configuration et résultats | Entrées, états, variantes, interactions |
| Tasklist | Tranche de comportement | Adaptateur, tests, qualification | Réutilisation et intégration |
| Maquette applicable | Parcours visible | Réglages et diagnostics | États et variantes |
| Tests pertinents | Invariants, permissions, concurrence | Réponses, erreurs, doublons | Interactions significatives |
| Implémentation | Services et points d’entrée | Adaptateur contrôlé | Rendu et comportements |
| Intégration / revue | Parcours complet et preuves | Qualification ciblée et limites | Navigateur, clavier, captures |

Le TDD porte sur des comportements observables, permissions et risques testables. La tasklist précède le code ; la maquette précède le frontend concerné ; les captures de vérification suivent l’implémentation. Les sous-agents peuvent travailler en parallèle après définition de leurs interfaces et de leurs périmètres.

La disponibilité no-code résulte d’un code compatible, de prérequis satisfaits et d’une configuration valide. Chaque contrat expose les informations nécessaires au Studio. Une demande inédite suit une étude et un développement avant de devenir une capacité disponible.

## 6. Critères de fin

| Livrable | Prêt dans son périmètre lorsque… |
|---|---|
| Feature | Critères métier, droits, données, migrations et parcours sont vérifiés |
| Connecteur | Contrat et erreurs testés ; hypothèses fournisseur qualifiées ou explicitement ouvertes |
| Composant | Contrat, états, interactions, rendu et accessibilité examinés selon le besoin |
| Module activé | Code compatible, prérequis et configuration effectivement disponibles |
| Opération | Résultat observé distinct de la demande ou de la seule acceptation |

Les liens techniques ont été consultés lors du cadrage du 18 novembre 2026. Ils justifient les mécanismes cités ; les versions du produit sont qualifiées à l’ouverture du lot. Aucun exemple ne vaut sélection d’un module ou autorisation de déploiement.

