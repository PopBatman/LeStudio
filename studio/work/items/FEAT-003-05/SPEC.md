# FEAT-003-05 — Composer une page sur le canvas

Depuis **Mes sites → fiche Site → Atelier du site**, l’opérateur ouvre une page et passe de **Structure** à **Canvas**. Les deux vues présentent les mêmes occurrences, la même page et la même révision du brouillon. Un site sans brouillon reprend le parcours de création de FEAT-003-04. Un site sans raccordement peut utiliser le canvas. [Carte Notion](https://app.notion.com/p/41d49e23bbdb81e386a3ef5f4bf26492) · [Contrat parent](../FEAT-003/SPEC.md)

## Parcours opérateur

1. Choisir le format **Bureau**, **Tablette** ou **Mobile**. Un libellé annonce le format actif et la provenance de la valeur sélectionnée. Le format de la page simulée et la largeur de l’écran de l’opérateur peuvent différer.
2. Choisir une section ou un conteneur, puis insérer une version de composant autorisée. Sélectionner un bloc sur la surface ou dans la structure. L’inspecteur identifie page, parent, position et format. Un bloc masqué par un autre reste sélectionnable dans la liste.
3. En flux, glisser vers une destination valide avec repère avant/après ou fin de liste. Une pile organise les enfants en colonne et une grille les répartit en colonnes. Redimensionner depuis une poignée, ou renseigner les dimensions dans l’inspecteur. Le déplacement de structure change l’ordre de lecture pour tous les formats.
4. Pour une superposition, choisir le placement libre dans le parent et régler la position, les dimensions et le niveau de superposition. Le niveau agit dans le parent et le format sélectionnés. Le passage au libre conserve l’identité, les propriétés et la place de lecture du bloc.
5. Sur téléphone ou au clavier, sélectionner une destination et une position dans un formulaire, ou régler les valeurs numériques. Les deux modes offrent ces opérations. **Échap** annule le geste en cours. L’interface indique la cible avant confirmation et restitue le focus sur l’élément encore présent.
6. Ajuster une valeur sur tablette ou mobile puis retirer uniquement cette surcharge pour retrouver la valeur héritée. Les deux formats héritent directement de la base. Modifier la base peut affecter les formats qui en héritent. Montrer tout format devenu invalide avant l’enregistrement.
7. L’enregistrement d’une commande effective ajoute une seule révision. Les mouvements intermédiaires du pointeur, le changement de format, la sélection et l’annulation sont locaux. Sur conflit, garder la proposition, relire la révision courante, puis demander une confirmation explicite après comparaison. S’il manque la cible, permettre de sélectionner un élément encore présent.

La consultation expose les dispositions enregistrées et les diagnostics. Le mandat de gestion autorise l’écriture. Le rendu est une surface de composition alimentée par les composants locaux. L’aperçu éditorial relève de FEAT-004, la publication de FEAT-005, l’import Figma de FEAT-003-08 et la qualification humaine transverse de UI-002.

## Critères de recette du produit

| Attendu Notion | Essai reproductible à réaliser sur Django |
|---|---|
| Déplacement persistant | Sur un site fictif, insérer deux textes homonymes et un conteneur. Déplacer le second texte dans le conteneur, changer l’ordre, enregistrer et rouvrir une session. Vérifier l’UUID, le parent, l’ordre et l’ancienne révision. |
| Parité entre vues | Sélectionner une occurrence dans Canvas, changer son texte dans Structure, puis déplacer et redimensionner dans Canvas. Rouvrir Structure, comparer la sélection et le document relu au serveur. Vérifier aussi Pages, Menus et Apparence. |
| Grilles, libre et surcharges | Régler une grille bureau, superposer deux blocs, changer la largeur sur tablette et le niveau sur mobile. Recharger les trois formats, remettre une valeur en héritage, vérifier les valeurs effectives et l’ordre de lecture. Tester un changement de parent avec une géométrie devenue invalide. |
| Parcours sans glisser | Au clavier seul, insérer, sélectionner, changer de parent, réordonner, redimensionner, ajuster le niveau et retirer une surcharge. Refaire au tactile par sélections et boutons. Vérifier focus, message de statut et accès au bloc recouvert avec un lecteur d’écran. |
| Isolation, responsive et erreurs | Sur deux sites et en lecture seule, essayer une mutation interdite, une valeur hors borne, un texte trop long et deux écritures concurrentes. Comparer les têtes. Observer les formats et les limites sous charge, et vérifier l’absence d’appel ou d’écriture au moteur. |

Les montants numériques, la compatibilité de lecture/écriture et le traitement des changements de mode sont précisés dans le [contrat technique](ARCHITECTURE.md). Les essais sur le prototype et ceux à rejouer sur l’application figurent dans la [revue visuelle](VISUAL-REVIEW.md).

## États de l’interface

| Situation | Comportement observable |
|---|---|
| Page vide | Afficher le nom de la page et une commande pour créer la première section. Garder le sélecteur de pages et le retour vers Structure accessibles. |
| Déplacement ou redimensionnement en cours | Afficher le bloc choisi, le parent de destination, un repère de dépôt et les dimensions courantes dans les unités du format simulé. Conserver la position initiale jusqu’à confirmation. Annuler ou perdre le pointeur restaure l’état précédent. |
| Proposition valide en cours de sauvegarde | Indiquer le traitement et prévenir un double envoi. Après succès, annoncer le format, le résultat et la révision. Un geste sans changement garde le numéro de révision. |
| Débordement ou superposition | Signaler un texte qui sort du cadre avec un accès au bloc et au format concernés. Permettre d’agrandir le bloc ou de repasser en flux. Un chevauchement voulu garde les deux blocs sélectionnables ; l’ordre clavier reste celui du document. Une géométrie hors bornes bloque la sauvegarde. |
| Erreur de champ ou concurrente | Conserver les valeurs proposées, associer le message à la commande et placer le focus sur le résumé ou le champ. En cas de concurrence, proposer relecture et comparaison avant nouvel envoi. |
| Consultation ou format inconnu | En lecture, présenter la page et ses réglages avec accès aux sélections. Une révision de schéma inconnu affiche son numéro et l’incompatibilité. |
