# Bilan du cadrage

Le gestionnaire part d’une remise du portail, sélectionne les frames d’une version Figma accessible et examine les correspondances avec la bibliothèque autorisée du site. Le cadrage propose des règles explicables et une décision par élément. Les composants inconnus et les formats absents restent visibles dans le bilan. Les dépendances FEAT-003-03, 04 et 07 sont DONE. [Spécification](SPEC.md) · [Carte Notion](https://app.notion.com/p/41d49e23bbdb81c0b724f655557db7d9)

Deux destinations sont prévues. La première création utilise l’origine Figma du modèle de composition. Pour une tête existante, le choix proposé est un ajout explicite de pages qui conserve les pages, menus et styles existants. Un changement de source ou de brouillon impose de revoir la comparaison. L’opérateur reste responsable des choix et retrouve la révision dans l’atelier. [Architecture](ARCHITECTURE.md) · [Revue visuelle](VISUAL-REVIEW.md)

Le profil de lecture géré par site, les seuils d’analyse et la sélection des types de composants sont des choix de conception proposés pour la V1. Une connexion REST de recette devra être qualifiée avec les permissions effectives d’un fichier dédié. Le cadrage a utilisé les documents de l’API, les services existants en conteneur isolé et une maquette sur des données fictives. [Contrat du connecteur](CONNECTOR-SPEC.md) · [Preuves](EVIDENCE.md)

Le responsable du lot a établi le rapprochement Notion, la spécification, la recherche fournisseur, les essais de composition et le plan. Les exécutants import_arch et import_mock ont produit les contrats de données et de sécurité ainsi que la maquette. L’exécutant indépendant import_review a examiné les critères et le prototype. [Revue indépendante](REVIEW.md) · [Plan de développement](TASKLIST.md)

**Conclusion du cadrage — READY.** Le prochain mandat peut porter sur le développement du connecteur et de la revue des correspondances.

## Livraison du 20 novembre 2026

Le gestionnaire peut analyser une remise depuis son détail, regrouper les formats, corriger les correspondances de composants et de tokens, examiner les exclusions, puis confirmer la création ou l’ajout de pages dans le brouillon habituel. L’atelier, le canvas et l’aperçu lisent la même composition. Une confirmation répétée restitue la révision locale déjà créée. [Guide opérateur et configuration](../../../docs/REGISTRE.md#importer-une-remise-dans-le-brouillon)

La réalisation a été répartie entre `import_provider` (connecteur), `import_domain` (persistance, transaction et purge), `import_ui` (parcours et navigateur) et le responsable du lot (projection, intégration et déploiement local). `import_acceptance` a revu le résultat séparément. La revue a fait corriger l’application d’un espacement explicitement écarté ou corrigé dans la disposition du conteneur.

**DONE sur Studio local avec recette Figma simulée**, conformément au mandat. La qualification a utilisé une API HTTPS fictive. Les pages importées étaient éditables, les anciennes révisions et les éléments publiés ont été préservés. Aucun profil fournisseur réel n’a été activé sur Tennis AI. [Preuves et limites](EVIDENCE.md)
