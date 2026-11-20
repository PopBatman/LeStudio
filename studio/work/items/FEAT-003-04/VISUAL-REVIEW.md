# Parcours de la fiche Site à l’éditeur structuré

La [maquette interactive](evidence/maquettes.html) s’ouvre sur la fiche fictive « Maison des dunes ». Les scénarios en pied de page permettent de reprendre un brouillon existant, de passer en lecture seule ou de simuler une écriture concurrente. Le prototype conserve les changements en mémoire pendant les allers-retours entre la fiche et l’atelier.

| Parcours | Comportement à examiner |
|---|---|
| Créer le premier brouillon | Choisir le modèle « Présentation d’activité » v1, qui fournit un accueil, une section, un titre et un texte. Le départ vierge donne un accueil à remplir. L’entrée Figma indique son indisponibilité. [Création sur téléphone](evidence/creation-mobile.png) |
| Composer une page vide | Ajouter une section puis un titre ou un texte. Sélectionner le bloc, modifier le texte et enregistrer. La révision affichée et l’annonce de succès rendent la sauvegarde perceptible. |
| Retrouver une occurrence et son ordre | Sélectionner un bloc dans la liste indentée. L’inspecteur place le focus sur la sélection. Monter ou descendre le bloc au clavier ; avec deux sections, choisir une destination pour y déplacer le bloc. « Revenir à la structure » replace le focus sur le titre de l’arborescence. [Éditeur sur bureau](evidence/editeur-bureau.png) |
| Corriger un champ | Enregistrer un texte vide. Le champ conserve la saisie et reçoit le focus, avec une erreur liée au contrôle. Annuler restaure la dernière valeur. [Erreur sur téléphone](evidence/erreur-mobile.png) |
| Reprendre après un conflit | Choisir le scénario de conflit puis modifier un texte. Comparer la révision courante et la proposition conservée, puis confirmer à nouveau. [Comparaison sur bureau](evidence/conflit-bureau.png) |
| Consulter | En lecture seule, consulter les éléments et leurs valeurs. Un site inaccessible affiche un refus générique. |

Chromium a parcouru le modèle, le départ vierge, l’insertion, le changement d’ordre, l’édition, la reprise depuis la fiche et les états de refus, d’erreur et de conflit à 1440, 390 et 320 pixels de large. Les essais ont vérifié le lien de saut, l’activation de commandes par Entrée, le premier champ en erreur et la largeur du document. [Relevé navigateur](evidence/examen-maquettes.json)

La maquette illustre une seule page et deux types de blocs. Le développement couvrira le sélecteur de pages, les conteneurs imbriqués, le catalogue accessible du site, les propriétés typées, le retrait confirmé et la disposition des sections. La fiche réelle conservera ses entrées Pages, Menus, Bibliothèque et Apparence. Vérifier sur Django la création atomique, la reprise après recharge du navigateur, les habilitations réelles et les annonces avec un lecteur d’écran. UI-002 suit la validation transversale d’accessibilité et de direction artistique.
