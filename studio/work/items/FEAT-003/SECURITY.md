# Droits et données de l’atelier

## Matrice de contrôle proposée

| Acteur | Portée, opération et contrôle |
|---|---|
| Opérateur actif avec mandat Site en lecture | Consulte la fiche, l’historique de raccordement projeté pour son rôle et le brouillon de son site. Le GET de la fiche ou de l’atelier ne crée aucune révision. |
| Opérateur actif avec mandat Site en gestion | Peut créer et enregistrer le brouillon, choisir un modèle, traiter les propositions et gérer les invitations de ce site. Recontrôler le mandat à l’écriture. Les identifiants de liaison et l’alias confirmé suivent la règle de gestion d’ARCH-002-01. |
| Opérateur avec mandat Client seul ou mandat sur un autre Site | Requête directe traitée comme une fiche inconnue. Aucune visibilité des révisions, médias, soumissions ou composants d’un site voisin. |
| Compte retiré du groupe, révoqué ou visiteur | Appliquer les refus et la connexion FEAT-001/002. Sur une fiche accessible en lecture seule, une écriture est refusée même si une requête est construite à la main. |
| Équipe technique habilitée | Développe et révise les composants globaux. Distinguer le mandat Site du pouvoir de promouvoir une définition pour tous les sites. La permission de promotion et son attribution restent à spécifier au 03. |
| Graphiste invité | Dépose via un portail dédié à l’invitation, sans compte. Le site est résolu par le serveur à partir de l’invitation. Accès limité au lien et aux commentaires/versions autorisés de cette invitation. |
| Client | Aucune surface d’administration Studio ou Wagtail. Les comptes Wagtail des opérateurs restent gérés par l’instance concernée. |

Conserver le filtrage serveur FEAT-002 pour chaque lecture, commande, liste, téléchargement ou traitement différé. Le site du formulaire ou de l’URL n’est jamais une preuve de mandat. Un accès retiré entre lecture et sauvegarde interrompt la transaction. Les médias, versions de templates privés, objets Wagtail et résultats Figma s’autorisent avec leur propre portée. La recherche de composants ne retourne que les composants déjà globaux et ceux du site accessible.

## Risques, contrôles et recettes à programmer

| Surface | Contrôle proposé | Vérification dans le sous-lot |
|---|---|---|
| Brouillon et concurrence | Validation du schéma, profondeur/volume bornés, contrainte d’unicité de tête, comparaison de révision et transaction. Protection CSRF des commandes de session. | Deux opérations simultanées, formulaire périmé, structure cyclique, erreur en milieu d’écriture et réexécution. Vérifier l’intégrité de deux bases de référence ou de deux sites logiques selon le composant testé. |
| Texte, styles et rendu | Échappement des textes. Paramètres structurés et valeurs autorisées, y compris liens et médias. Les variantes libres acceptent des paramètres de disposition typés. Aucune entrée de code, script, feuille de style ou plugin exécutable depuis l’éditeur. | Valeurs invalides et ressources extérieures au périmètre refusées ; champs fautifs signalés, précédente révision intacte. Prévenir les débordements sans masquer leur origine dans le canvas. |
| Versions et promotion | Épingler les versions utilisées. Vérifier licence et droits graphiques, retirer identifiants, contenu et actifs privés avant promotion. | Mise à jour d’un composant global et suppression de l’accès au composant privé d’un autre site. |
| Invitation temporaire et dépôt | Jeton aléatoire stocké par empreinte, expiration/révocation, contrôle de chaque soumission ; éviter la conservation du jeton dans journaux, historique d’audit ou référent sortant. Distinguer le portail sans compte des sessions administratives. Quotas, pagination, tailles de commentaire et limites d’envoi à préciser au 07. | Liens expirés/révoqués ou rejoués après révocation, manipulation d’un ID, abus et erreurs de saisie. Vérifier qu’un dépôt valide avec une seule vue produit une notification interne au site désigné. |
| Métadonnées et API Figma | Le dépôt du lien ne déclenche pas de lecture fournisseur. Pour l’analyse 08, extraire un identifiant depuis un format Figma permis et appeler un endpoint fournisseur fixé par l’intégration. Limiter permissions, taille, ressources et durée des lectures. Protéger les secrets côté serveur. Une autorisation manquante produit un diagnostic minimal. | Vérifier chemins d’échec sur fichier factice autorisé ou privé, droits révoqués, limitation fournisseur et analyse interrompue ; comparer les autorisations avant de conserver ou appliquer le résultat. |
| Propriété et durée de vie | Pour liens, commentaires, médias et métadonnées, identifier provenance, portée et droit d’usage. Décider au 07 de la durée de vie de l’invitation, de la conservation des soumissions, de l’effacement et de la gestion des sauvegardes avant traitement de données réelles. | Fixtures fictives pour maquettes, tests et captures. Exercer retrait d’accès et effacement sur une soumission, préserver seulement les références d’audit autorisées. |
| Données de raccordement | Réutiliser inspect_link et connection_panel sur le site autorisé. Ne copier ni certificats, alias techniques dans les brouillons, origine interne, corps de diagnostic ou clé d’API. Aucun probe ni opération de publication à l’ouverture ou à l’enregistrement. | Espionner les points d’écriture et le transport ; vérifier que le contexte du lecteur et les erreurs excluent les données de gestion. |

Les observations du prototype attestent un comportement d’interface sur données fictives. Les contrôles backend, l’analyse Figma sur une ressource autorisée et les conditions opérationnelles de conservation seront qualifiés pendant les lots correspondants. Voir les [contrats d’architecture](ARCHITECTURE.md) et les [droits de la fiche Site livrée](../ARCH-002-01/SECURITY.md).
