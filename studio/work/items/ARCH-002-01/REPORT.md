# Consultation du raccordement dans la fiche Site

## Cadrage initial

La fiche Site peut afficher une observation historique dès sa prochaine évolution. Elle dispose déjà du contexte opérateur et le service central sait lire la liaison. L’instance, l’alias et les versions décrivent le dernier succès. Les date et issue de tentative peuvent être plus récentes. Le relevé de tennis-ai figure dans la [recherche](RESEARCH.md).

Le changement proposé est une section de la page existante, avec résumé puis détails repliables. Le domaine reste textuel et les destinations d’administration et publiques attendent une source navigateur autorisée. Les maquettes emploient un exemple fictif pour faire varier l’état et le niveau d’accès. Voir la [spécification](SPEC.md), le [plan de réalisation](TASKLIST.md), les [maquettes](VISUAL-REVIEW.md) et la [revue de cadrage](REVIEW.md).

Le premier mandat couvrait le cadrage et la conception. Le raccordement et la fiche Django existants restent les sources de référence pour la future recette. La validation produit, l’intégration, les contrôles de sécurité côté serveur et les captures de la future page exécutée sont prévus au développement. Le lot parent ARCH-002 reste terminé.

Contributions de /root pour le contrat, /root/a201_design pour la conception et l’examen navigateur, /root/a201_registry pour la vérification documentaire et /root/a201_review pour la relecture indépendante.

## Réalisation et recette du 19 novembre 2026

La page existante Mes sites → fiche Site présente désormais « Moteur Wagtail » sous la fiche métier. Elle lit la même observation centrale que la commande etat, contrôle le mandat Site et projette les seules valeurs autorisées. Le gestionnaire peut déplier les identifiants et le diagnostic. La normalisation du snapshot conserve les champs canoniques de l’association dans les anciennes données de versions partielles ou mal formées. L’ouverture de la fiche ne déclenche aucune vérification distante.

| Critères | Observation |
|---|---|
| AC1 à AC4 | Tests d’intégration sur le vide, la confirmation, le premier échec, l’expiration et la tentative en cours, les deux dates, les entrées anciennes et le résultat inconnu. Concordance de la fiche réelle tennis-ai avec PostgreSQL pour les deux dates et les informations du moteur. |
| AC5 à AC8 | Domaine textuel, absence d’URL de gestion, filtrage lecteur/gestionnaire dans le contexte et dans le HTML, refus d’accès direct ou après révocation. Plusieurs consultations GET/HEAD sans écriture de connexion, chargement de profil ou sonde. |
| AC9 | Parcours réel par formulaire de connexion et lien « Mes sites », clavier, 320, 390 et 1440 pixels. Quatre captures de fiches fictives. Revue de réalisation indépendante favorable. |

52 tests réussis sur PostgreSQL, 50 réussis et deux tests de concurrence réservés à PostgreSQL ignorés sur SQLite. Le service web local a été reconstruit avec son complément Compose tennis-ai. Le contrôle de santé répond ok, aucune migration n’est requise. La lecture sur le poste a confirmé Wagtail 7.4.4 et le dernier succès de tennis-ai à 10 h 55 (Paris).

Contributions : /root pour la vue, la projection, le snapshot, PostgreSQL et l’intégration locale ; /root/impl_tests pour les tests des accès et états ; /root/impl_visual pour le gabarit, les styles et la recette navigateur ; /root/impl_review pour la revue indépendante. [Pièces de réalisation](EVIDENCE.md)
