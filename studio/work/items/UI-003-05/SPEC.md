# Qualifier le passage de l’atelier V1 au Visual Builder

Depuis la fiche Site, un gestionnaire doit pouvoir reprendre un ancien brouillon, accomplir les tâches qu’il utilisait dans Structure et Canvas et retrouver le résultat sur le moteur Wagtail raccordé. Un lecteur conserve ses parcours autorisés. Le site actif garde sa composition publiée pendant les essais. [Carte Notion](https://www.notion.so/41d49e23bbdb811e9acbd8b4162d3954) · [Vision du Visual Builder](../UI-003/SPEC.md)

## Périmètre et conditions de passage

| Décision | Preuve à présenter | Si la preuve manque |
| --- | --- | --- |
| Corriger la parité | Pour chaque tâche de la [matrice](MATRICE-PARITE.md), partir d’une entrée utilisateur réelle, nommer le rôle, l’action et son résultat persistant. Montrer le chemin V2 ou la surface métier conservée. Un service accessible uniquement par appel interne ne suffit pas. | Conserver l’entrée V1. Corriger les écarts de la tâche ou faire consigner une décision produit explicite si un usage doit évoluer. |
| Qualifier les brouillons | Ouvrir puis corriger des données des schémas 1 à 4. Comparer tête, parents, identités, définitions, références, menus, thème et dispositions. Vérifier qu’une simple lecture ou un changement d’interface ne crée aucune révision. | Arrêter la bascule pour tout écart de données inexpliqué. [Contrat de compatibilité](ARCHITECTURE.md) |
| Accepter l’UX du produit | Présenter les trois origines sur bureau, tablette et mobile, avec captures de l’application et même rendu privé Wagtail. Consigner les observations clavier et lecteur d’écran et l’avis graphique humain sur la version examinée. | La coexistence continue. UI-003-01 a validé le prototype Atlas du Sud. L’avis attendu ici porte sur le produit livré. |
| Basculer les entrées | Identifier la version qualifiée, les sites concernés, les références au test de retour, la décision humaine et ses réserves éventuelles. Vérifier les liens directs et indirects, les droits et les formulaires déjà ouverts. | Garder la configuration précédente. Une réserve concernant l’accès, les données ou une tâche essentielle maintient la V1 disponible. |
| Retirer les anciennes vues | Après fonctionnement en mode V2, examiner les régressions signalées, l’usage restant des anciennes URL et l’exercice de retour sur une tête créée par V2. Obtenir la décision explicite portant sur le retrait, avec les références des preuves. | Prolonger la coexistence ou rouvrir la V1. Le plan de retour reste utilisable après le retrait. |

## Recette UX et accessibilité à mener sur le produit

| Origine | Tâche de bout en bout | Éléments observables |
| --- | --- | --- |
| Page vierge | Depuis un site sans révision, choisir le départ vierge, créer la première section, insérer et déplacer au clavier un titre, annuler/rétablir, enregistrer, rouvrir. | Emplacement de dépôt annoncé, focus récupérable, une révision pour les gestes confirmés, même UUID dans les calques et le rendu. Le lecteur peut ensuite consulter la révision. |
| Modèle | Reprendre le modèle, déplacer ou supprimer une section, changer une propriété sur mobile, revenir à l’héritage, corriger une référence éditoriale autorisée, comparer le rendu. | Effets sur les descendants annoncés. Le bureau et la tablette conservent leurs valeurs. Le choix ou remplacement de l’article respecte racine, mandat et version Wagtail. |
| Remise Figma | Reprendre une création initiale puis un ajout de pages à un site existant. Comparer la frame déclarée avec le rendu, corriger une occurrence et relire la décision sur la nouvelle révision. | Versions de source et du brouillon identifiées, écart à réexaminer, accès à l’édition si la source privée a expiré, format manquant explicite. Le fournisseur de recette est simulé. |

Pour chaque origine, conserver les observations sur les trois tailles, avec taille de fenêtre et largeur du rendu distinguées. Comparer avant/après à page, contenu et zoom identifiés. Couvrir textes longs, cible répétée ou imbriquée, zoom, affichage étroit et moteurs indisponibles. Vérifier ordre de tabulation, activation, fermeture des panneaux, nom/rôle/état, annonces d’erreur et de réussite, focus après retrait d’un bloc et alternative complète au glisser-déposer. Consigner navigateur, lecteur d’écran, versions, gestes et annonces effectivement observées.

Le dossier de décision recensera hiérarchie visuelle, densité, finition, lisibilité, compréhension des commandes et fluidité perçue. Utiliser les verdicts de UI-002 « accepté », « accepté sous réserve » ou « refusé », avec auteur humain, date, version, parcours et tailles examinés, écarts, responsables et contre-recette. Demander séparément l’autorisation de passer aux entrées V2 puis de retirer les vues V1. La [carte UI-002](https://www.notion.so/41d49e23bbdb81799166e11836c31bff) est DRAFT lors du cadrage. Ses preuves et son avis doivent être rapprochés pour la bascule ; la préparation du présent lot peut avancer.
