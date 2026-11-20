# Cadrage du 20 novembre 2026
Le prochain incrément de l’atelier permet au gestionnaire de composer à partir de la bibliothèque du site, de modifier les propriétés courantes dans la page et de sauvegarder une suite de gestes en une révision. Le canvas livré en UI-003-02 fournit le rendu de référence et la sélection par occurrence.

Le [contrat opérateur](SPEC.md) couvre l’insertion, le déplacement, la duplication, la suppression, les quatre types de contenu éditables et la reprise après conflit. Le [contrat technique](ARCHITECTURE.md) précise le passage du rendu identifié à la surface de travail, le retour à un aperçu vérifié et le rejeu d’une sauvegarde. Les [contrôles d’accès](SECURITY.md) s’appliquent au site, aux références et à chaque écriture.

La [maquette](evidence/maquette.html) et la [revue visuelle](VISUAL-REVIEW.md) permettent d’examiner les gestes prévus. Le [plan de réalisation](TASKLIST.md) définit la recette à mener sur deux sites. Les résultats disponibles à ce stade concernent le socle livré et la maquette de cadrage.

## Réalisation dans Studio local

Depuis la fiche Site, le gestionnaire choisit la page de la dernière révision et ouvre **Canvas Wagtail**. Le double-clic sur une occurrence éditable et le dépôt depuis **Insérer dans la page rendue** ouvrent la vue de travail à l’emplacement choisi. Une autre entrée, **Modifier la page**, donne accès à la bibliothèque, aux calques et à l’inspecteur. Les commandes clavier et tactiles opèrent sur les mêmes identifiants. Les étapes pour l’opérateur figurent dans le [guide du canvas](../../../docs/MOTEUR-WAGTAIL.md#composer-dans-le-canvas).

Les modifications restent en mémoire jusqu’à **Enregistrer**. La transaction vérifie le mandat et la révision sous verrou. Le reçu associe l’opérateur, le site et la clé de sauvegarde au résultat et aux UUID définitifs. Le rendu privé est ensuite préparé sur la révision confirmée. Les six gestes du [parcours sur modèle](evidence/realisation-modele.json) ont créé une seule révision malgré la perte de la réponse. La [recette de concurrence](evidence/realisation-conflit.json) conserve le brouillon du premier opérateur et les gestes locaux du second. La [panne de passerelle](evidence/realisation-indisponibilite.json) a permis de vérifier la réouverture après rétablissement du moteur.

La qualification emploie deux sites fictifs raccordés à de vrais moteurs Wagtail. La [page vierge](evidence/realisation-page-vide.json) a été composée au clavier et au tactile émulé. Le [parcours Figma](evidence/realisation-figma.json) utilise une remise confirmée depuis le fournisseur simulé. Les réponses des deux pages publiques gardent leurs [empreintes avant et après](evidence/pages-publiees.json).

Sur l’image livrée, PostgreSQL valide 225 tests. SQLite en valide 210, et les 15 cas réservés à PostgreSQL sont ignorés. Le contrôle des migrations et les vérifications HTTP passent sur le [poste local](evidence/realisation-poste-local.json). Les 16 révisions et leur empreinte sont identiques avant et après installation.
