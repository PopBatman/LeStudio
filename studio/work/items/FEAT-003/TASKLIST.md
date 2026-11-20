# Plan de livraison de l’Atelier du site

Le parent porte les contrats communs et la revue des maquettes. Les huit cartes existantes gardent une recette et un mandat propres. Premier parcours visé : depuis « Mes sites », un gestionnaire ouvre la fiche, crée un brouillon local depuis une page vierge ou un template, enregistre puis reprend la même révision. Les données du moteur restent consultables à côté de l’entrée Atelier.

| Sous-lot et dépendances | Incrément et condition de sortie vérifiable |
|---|---|
| 01 · Socle, après FEAT-002, ARCH-002 et ARCH-002-01 | Identité du site, révisions et validation commune. Deux écritures concurrentes sur la même base donnent un seul succès ; relecture après redémarrage, isolation entre sites et aucune écriture moteur. |
| 02 · Pages et menus, après 01 | Arbre de pages et menus distincts. Recharger un menu imbriqué ordonné et une page hors menu ; repérer liens affectés par changement de slug ou suppression. |
| 03 · Composants et apparence, après 01 | Registre global et par site, versions épinglées, tokens et variantes. Après promotion revue, les autres sites restent sur leur version choisie. |
| 04 · Éditeur structuré, après 01, 02, 03 | Intégrer l’entrée de la fiche et le formulaire de brouillon ; template et vierge convergent. Reprendre le brouillon, tester erreurs, accès direct, écran étroit et clavier. L’entrée Figma indique son indisponibilité jusqu’à la livraison de 08. |
| 05 · Canvas responsive, après 04 et 03 | Déplacer, redimensionner, superposer et ordonner avec gestes et clavier. Recharger dans les deux éditeurs et comparer exactement le document et ses variantes. |
| 06 · Contenus simples et Wagtail, après 01, 04 et ARCH-002 | Éditer titre, image ou lien localement. Préserver la référence éditoriale Wagtail et signaler une révision divergente ou invérifiable. Tester les frontières entre propriétaires de contenus. |
| 07 · Portail graphiste, après FEAT-001 et FEAT-002 | Branche indépendante du canvas. Dépôts Figma successifs par invitation limitée à un site, une seule vue responsive suffisante ; tester expiration, révocation, notification interne et confidentialité. |
| 08 · Import Figma, après 07, 03 et 04 | Lire un fichier réellement autorisé, produire une proposition traçable, montrer manques et correspondances. Seuls les éléments acceptés rejoignent le brouillon ; tester perte de droits et reprise sans duplication. |

## Ordre des travaux

1. Cadrage parent : relire les cartes et la fiche livrée, définir données, droits, interface et protocole de recette.
2. Concevoir puis examiner sur navigateur les maquettes de la fiche Site (bureau/mobile, gestion/lecture, brouillon absent/existant, raccordement confirmé/absent ou tentative en échec). Conserver les captures fictives et la revue séparément des futures preuves produit.
3. Sur mandat de sous-lot, commencer par le socle 01. 02 et 03 deviennent parallélisables après son contrat stabilisé ; 07 peut être préparé indépendamment. Dans chaque carte, préciser le schéma et les limites, écrire les tests de règles et d’accès avant le code, vérifier persistance, puis recette et revue.
4. Après 04, qualifier le premier parcours local complet. Après 05, 06 et 08, qualifier les interactions croisées, le jeu de données à deux sites et la non-modification de la version active. UI-002 suit la validation humaine d’accessibilité et de direction artistique ; ARCH-003 suit les environnements distants.

## Résultat au 20 novembre 2026

Les huit sous-lots sont livrés en local. Le contrôle final de 08 utilise le fournisseur simulé demandé. Une qualification Figma réelle reste à effectuer pour l’usage d’un compte et de fichiers autorisés. [Rapport de réalisation](REPORT.md)
