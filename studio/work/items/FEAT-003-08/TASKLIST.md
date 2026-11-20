# Ordre de réalisation

1. Écrire des tests rouges autour du contrat 07 → 08 sur deux sites fictifs. Couvrir la remise conservée après révocation d’invitation, la remise effacée, le gestionnaire rétrogradé et le profil Figma absent. Figer les historiques et le catalogue avant essai.
2. Introduire le profil de lecture et l’adaptateur isolé. Vérifier les réponses contrôlées de l’API, le ciblage d’un nœud, la version épinglée, les champs manquants, la taille, le délai et la reprise après quota. Qualifier en lecture un fichier de recette autorisé et documenter le périmètre effectivement accessible.
3. Normaliser les frames et construire les propositions à partir des définitions actives du catalogue. Éprouver les choix ambigus, les tokens compatibles ou indisponibles, les images et références privées, une seule vue, l’exclusion d’un bloc et des variantes manquantes. Exercer les bornes du document canonique avant la confirmation.
4. Persister les tentatives et les décisions de revue avec leur portée et leur version. Tester reprise après interruption, réponse tardive, changement d’accès, effacement, nouvelle analyse, changement de tête ou de définition. Qualifier les transactions concurrentes sur PostgreSQL et la purge/restauration des observations associées à une remise.
5. Brancher les vues privées depuis le détail du dépôt et le point de départ Figma de l’atelier. Rejouer sélection, comparaison, acceptation, correction, rejet, récapitulatif et confirmation au clavier et à 320 px. Préserver les décisions encore valables en cas d’erreur ; expliciter celles qui demandent une nouvelle revue.
6. Produire une révision par le service de composition, avec la traçabilité des UUID finaux. Tester première création et ajout de pages ; réouvrir pour éditer chaque résultat. Comparer les historiques de deux sites, leurs menus, thèmes, états publiés et définitions du catalogue. Vérifier l’idempotence y compris après perte de réponse.
7. Recetter le paquet Studio et ses migrations sur base neuve et existante. Fournir preuves expurgées fournisseur, tests, captures et revue indépendante. Consigner la procédure de profil, le diagnostic, les décisions résiduelles et le résultat observé dans Notion. FEAT-004 qualifiera le rendu Wagtail de la révision ; UI-003 qualifiera l’éditeur visuel.

Chaque palier s’appuie sur les [critères produit](SPEC.md), le [contrat du connecteur](CONNECTOR-SPEC.md) et les limites du [dossier sécurité](SECURITY.md).

## Exécution

Les paliers 1 à 7 sont livrés en local. Pour le palier 2, l’utilisateur a expressément choisi une recette simulée. Le connecteur a été exercé sur une API HTTPS isolée et sur des réponses contrôlées. Pour un futur passage à un compte Figma réel, qualifier séparément un fichier de test autorisé et ses permissions. [Résultats](EVIDENCE.md)
