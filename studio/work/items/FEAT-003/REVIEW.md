# Avis indépendant sur le cadrage de FEAT-003

Le 19 novembre 2026, le réviseur /root/feat3_review a examiné la [carte parente](https://app.notion.com/p/41c49e23bbdb8170b68adf9f4a546fe4), les huit [cartes sources](RESEARCH.md), les [contrats](ARCHITECTURE.md), les [droits](SECURITY.md), la [spécification](SPEC.md), le [plan](TASKLIST.md) et la [maquette](evidence/maquettes.html). Les auteurs du contrat et du prototype sont distincts du réviseur.

| Contrôle | Observation |
|---|---|
| Traçabilité | Les huit dépendances de carte et leurs critères sont couverts par sous-lot. Le socle 01 précède les pages et les composants, le portail 07 peut avancer à part. La formulation du 04 a été précisée pour indiquer que le choix Figma dépend de la livraison du 08. |
| Réemploi de la fiche | La vue existante filtre par mandat et utilise inspect_link puis connection_panel. Une lecture centrale indépendante de tennis-ai retrouve la confirmation du 19 novembre à 10 h 55 (Paris), Wagtail 7.4.4 et une dernière tentative achevée. La proposition distingue ces observations, le brouillon local et les versions appliquées inconnues. |
| Contrats et frontières | Une révision canonique par sauvegarde, des identités stables, une écriture atomique avec contrôle de révision et des références portées par site servent les deux éditeurs. L’avancement du brouillon ne dépend pas d’une sonde moteur. Le travail éditorial avancé, l’accès au portail, l’approbation des propositions Figma et la publication disposent de frontières distinctes. |
| Examen indépendant au navigateur | Sur Chromium, aux largeurs de 320 et 1 440 px, le gestionnaire peut ouvrir au clavier la création depuis une fiche dont la dernière tentative a échoué. Le choix vierge puis l’enregistrement simulé de « Atelier de revue » donnent la révision 1. La voie Figma est annoncée indisponible. La variante lecture donne accès à la consultation ; la variante sans mandat affiche « Fiche introuvable ». Aucun débordement horizontal détecté sur les deux fiches en lecture. |

**Avis favorable au cadrage parent.** Le prototype a été examiné avec des données fictives. Le développement des huit tranches, les tests de persistance et de permissions, la qualification réelle de l’accès Figma et la validation artistique humaine restent des travaux distincts. Les critères de recette de chaque tranche sont portés au [plan](TASKLIST.md).

## Revue indépendante de la réalisation de l’atelier

Le 20 novembre 2026, `/root/import_acceptance` a rapproché les critères transversaux de la spécification avec les rapports de livraison des lots 01 à 07 et la recette du lot 08. Le socle de révisions, les pages et menus, le catalogue, l’éditeur structuré, le canvas responsive, les références éditoriales et le portail de dépôt disposent chacun d’une recette de leur parcours. Le dernier sous-lot rattache les frames explicitement acceptées aux pages et occurrences du même document de composition. Les observations HTTPS simulées et les vérifications de création, d’ajout et d’édition sont conservées dans [la revue du lot 08](../FEAT-003-08/REVIEW.md).

**Avis favorable à la clôture de la réalisation locale avec la recette Figma simulée demandée par l’utilisateur.** Le passage à un fichier Figma réel requiert le profil de son site et la qualification du fournisseur avec ce fichier. Le futur éditeur unifié relève de UI-003.
