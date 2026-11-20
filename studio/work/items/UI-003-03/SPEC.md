# UI-003-03 · Bibliothèque, drag-and-drop et édition directe

Depuis la fiche Site, un opérateur disposant du mandat de gestion ouvre le canvas de la dernière révision et compose sa page dans l’atelier. La bibliothèque se trouve à gauche, le bloc et son guide de dépôt au centre, les réglages avancés dans l’inspecteur. Le mandat de lecture conserve le parcours de consultation de UI-003-02.

## Parcours et critères observables
| Tâche | Comportement à livrer et à vérifier |
| --- | --- |
| Trouver un composant | Rechercher par nom et filtrer par catégorie. Chaque résultat présente vignette locale, libellé, portée globale ou site, version et disponibilité. Distinguer catalogue vide et recherche sans résultat. Seules les versions internes admises pour ce site sont insérables. Une version historique déjà présente reste identifiable. |
| Construire une page vierge | Donner accès depuis l’atelier à une section de destination, puis à l’insertion du premier bloc. Une section vide et un conteneur vide doivent chacun accepter un premier enfant autorisé. |
| Insérer ou déplacer | Au pointeur ou au toucher, choisir la destination avec un guide « avant », « après » ou « dans ». Au clavier, choisir le composant, le parent et la position par leur nom et valider ; Échap annule. Un dépôt invalide explique le motif et laisse la page intacte. Un parent ne peut être déplacé dans ses descendants. |
| Modifier le contenu en contexte | Activer le titre ou texte sélectionné, saisir dans la page et confirmer ou annuler. Pour l’image, choisir un média autorisé et modifier son alternative ; pour le bouton, modifier libellé et destination HTTPS admise. Garder les variantes, styles et réglages de disposition dans l’inspecteur. Préserver les limites de longueur du schéma et la saisie refusée. |
| Dupliquer et supprimer | La duplication d’un conteneur crée un nouvel UUID par occurrence dans son sous-arbre. Préserver les références autorisées et les versions ; expliquer tout refus concernant une référence épinglée. Indiquer les descendants touchés avant suppression. Rendre le focus au voisin ou au parent survivant. |
| Annuler et rétablir | Un geste confirmé constitue un pas dans l’historique local. Annuler une suppression restitue l’ordre et les identités ; rétablir un duplicata reprend les mêmes nouvelles identités. Un nouveau geste après annulation ouvre une nouvelle branche et efface le rétablissement précédent. |
| Adapter au format | Le flux ou la grille respecte les colonnes et le parent. En placement libre, montrer les bornes et le chevauchement avant confirmation, avec solution au clavier. Un chevauchement volontaire demande une intention explicite ; un dépassement interdit est refusé. Modifier le mobile conserve la valeur de base et la tablette. Effacer une surcharge restaure la valeur héritée. |
| Enregistrer et rouvrir | Les gestes forment une seule sauvegarde de brouillon depuis Rn. Le succès identifie Rn+1. Une réouverture retrouve la même composition et un aperçu réel est préparé sur Rn+1. Si le moteur échoue après la sauvegarde, conserver Rn+1 et proposer de réessayer son rendu. Un aller-retour sans changement ne crée aucune révision. |
| Deux opérateurs ou réponse perdue | Deux opérateurs partant de Rn ne peuvent écraser leurs changements. Exposer le conflit, préserver les gestes locaux et permettre d’examiner la tête avant reprise explicite. Réessayer une sauvegarde dont la réponse s’est perdue doit retrouver son résultat sans créer une deuxième révision. |

La surface d’édition indique si elle montre des changements locaux. L’aperçu Wagtail de référence garde son numéro de révision jusqu’à l’enregistrement et à la préparation du nouveau reçu. Confirmer une modification est distinct d’appliquer une composition à un site actif.

## Limites
Les contenus éditoriaux avancés restent régis par les droits Wagtail. UI-003-04 traitera la comparaison au fichier Figma ; un brouillon Figma déjà confirmé peut utiliser les mêmes gestes que les autres origines. UI-003-05 porte la bascule des anciennes vues. Le cadrage conserve ces vues et les anciens brouillons comme témoins de parité.
