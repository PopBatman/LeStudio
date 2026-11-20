# Import intelligent et correspondance Figma

Depuis le détail d’une remise Figma, un gestionnaire peut examiner ce que le fichier contient, choisir les éléments utiles et les convertir en pages modifiables dans l’atelier. La décision porte sur une remise, une version observée du fichier et un site précis. Le numéro de remise de Studio et la version Figma observée sont affichés séparément. La composition active reste sous la responsabilité des lots de rendu et de publication. [Carte Notion](https://app.notion.com/p/41d49e23bbdb81c0b724f655557db7d9) · [Direction Visual Builder V2](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539)

## Du dépôt au brouillon

1. **Ouvrir la remise.** Le gestionnaire du site choisit **Analyser la maquette**. La fiche indique les prérequis si le profil de lecture manque. Un lecteur garde la consultation prévue par le portail 07. Les opérations d’analyse, de revue et de confirmation exigent la gestion du site. Le graphiste continue de disposer de son seul portail de remise.
2. **Sélectionner les frames.** Présenter les pages de design et les frames disponibles dans la portée autorisée. Une page Figma organise des frames et ne devient pas automatiquement une page du site. Proposer un titre de page de destination et demander quels écrans représentent des formats de la même page. Une seule vue suffit. L’opérateur voit les formats absents et les propriétés qui suivront l’héritage Studio.
3. **Comparer et décider.** Pour chaque ligne, montrer le nœud source, le composant et la version du catalogue, la portée globale ou privée, les propriétés ou tokens proposés, la raison et les écarts connus. Le gestionnaire accepte, corrige en choisissant une définition compatible ou écarte. Aucune correspondance, même forte, ne vaut approbation. Le récapitulatif distingue sélection, exclusions et éléments à concevoir. Une ligne sans cible doit être écartée ou résolue avant inclusion.
4. **Confirmer la destination.** Sans brouillon, choisir la page d’accueil parmi les pages sélectionnées. Avec un brouillon, présenter l’ajout des nouvelles pages, leurs parents et chemins ; laisser choisir d’autres slugs si nécessaire. Une modification du brouillon, du fichier, des droits ou du catalogue impose une nouvelle vérification. Aucun écran de comparaison ne déclenche de sauvegarde de la composition à son ouverture.
5. **Retrouver le résultat.** Une confirmation réussie donne la révision Studio, les pages créées et un accès à l’atelier existant. Une répétition de la même confirmation redonne le même résultat. L’historique permet de relier chaque page et occurrence issue de l’import à la décision de revue dans les limites de conservation. L’ouverture dans le futur builder V2 utilisera ces mêmes documents canoniques.

## Règles de correspondance proposées

La V1 privilégie des règles explicables. Une clé de composant fournisseur reliée à une définition interne autorisée peut fournir une suggestion forte. Une compatibilité de structure, de propriétés ou de nom fournit une suggestion à examiner. Deux candidats compatibles exigent un choix. Une correspondance de nom seule ne suffit jamais à choisir automatiquement une portée privée, une destination de bouton ou un média. Aucun service d’IA externe n’est requis pour cette première version.

| Observation sur la frame | Proposition et décision attendue |
|---|---|
| Texte « Nos ateliers » | Titre ou texte court selon la structure observée. Montrer le contenu et demander le niveau si le titre est retenu. |
| Instance de bouton avec libellé | Choisir une définition livrée et sa variante. Demander au gestionnaire une destination HTTPS valide lorsqu’elle manque. |
| Couleur, police ou espacement | Conserver la valeur observée et son origine. Proposer seulement un token autorisé par le manifeste. Une police inconnue ou une unité incompatible demande adaptation ou exclusion explicite. En ajout à un brouillon, les décisions s’appliquent aux nouveaux blocs. |
| Remplissage image ou instance sans équivalent | Signaler la ressource et son droit de réutilisation à vérifier. Pour retenir une image, choisir un média déjà attribué au site et renseigner l’alternative. Un composant inconnu est classé « à implémenter en interne ». |
| Frame mobile seule | L’opérateur choisit le rôle de la frame et confirme la base utilisable dans Studio. Les valeurs observées et les formats non fournis restent distingués. La V1 ne déduit aucune géométrie des écrans manquants. |

## Critères de recette du développement

| Critère Notion | Observation attendue |
|---|---|
| 1. Fichier autorisé | Sur un fichier de recette et une remise du site A, enregistrer l’heure, la version réellement lue, les frames retenues et les métadonnées accessibles. Sélectionner un nœud ciblé et vérifier la portée de la réponse. |
| 2. Source inaccessible | Tester profil absent, permission retirée, remise effacée, site B, nœud absent et quota. L’opérateur reçoit un état actionnable sans identité étrangère ; ni persistance de contenu nouvellement refusé ni modification de la composition. |
| 3. Propositions révisables | Sur un titre, une couleur et deux définitions ambiguës, accepter, corriger, écarter et rouvrir la revue. La confirmation reprend uniquement les décisions achevées. Le lecteur et le graphiste ne peuvent agir. |
| 4. Écarts et formats | Avec une seule frame et un élément inconnu, constater les formats absents, garder un titre accepté et exclure l’inconnu. Aucun composant exécutable ou plugin ajouté au catalogue. |
| 5. Brouillon canonique | Tester première création et ajout sur site existant. Réouvrir et modifier une occurrence dans l’atelier. Comparer anciennes révisions, menu, thème, références privées, compteurs de pages et état du moteur. Deux confirmations simultanées, un retour après perte de réponse et un changement de tête n’entraînent aucune duplication. |

La fonction de lecture Figma devra être qualifiée avec un fichier fictif autorisé. L’usage d’une maquette en mémoire couvre l’interaction de revue. [Connecteur](CONNECTOR-SPEC.md) · [Architecture et données](ARCHITECTURE.md) · [Plan de réalisation](TASKLIST.md)
