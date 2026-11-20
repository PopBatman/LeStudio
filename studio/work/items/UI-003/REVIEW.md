# Revue indépendante du cadrage parent

Revue documentaire du 20 novembre 2026 par `/root/u3_review`. Pièces examinées : carte mère Notion, spécification, sources, architecture, sécurité, plan des cinq sous-lots, HTML illustratif et trois captures du dossier de cadrage.

| Exigence examinée | Constat |
| --- | --- |
| Trois parcours, un atelier | Les entrées vierge, modèle et remise Figma confirmée convergent sur le même brouillon ; les maquettes montrent un site fictif, sa bibliothèque, une sélection et l’inspecteur. |
| Fidélité et sélection | Le code actuel porte des UUID de blocs et sert l’aperçu sous CSP sandbox. UI-003-02 prévoit de qualifier séparément la correspondance entre ces UUID et les cibles rendues, ainsi que la péremption. La capture tablette illustre la différence entre révision demandée et affichée. |
| Sécurité, historique, accessibilité | Les critères couvrent un mandat révoqué, deux sites distincts, deux modifications concurrentes, les références manquantes, trois largeurs, le clavier et le lecteur d’écran. Les essais applicatifs et la preuve de parité sont attribués aux lots qui réaliseront ces comportements. |
| Reprise et retrait | La recette Figma antérieure est identifiée comme simulée. La matrice composant/version et le dossier de compatibilité Figma ont des responsables par sous-lot. La V1 reste accessible pendant la qualification et la décision de bascule est explicitement humaine. |

Deux ajustements ont été vérifiés dans les documents. SPEC.md accepte une source Figma à une seule largeur et préserve les autres largeurs disponibles. TASKLIST.md précise le contenu de la matrice des composants et du dossier de compatibilité Figma.

Avis favorable pour le cadrage parent. Le prototype haute fidélité et son approbation UX/DA humaine relèvent de UI-003-01. Les captures illustrent une proposition de conception. La comparaison du rendu applicatif avec Wagtail, les essais d’accessibilité et la recette de bascule restent à exécuter dans leurs sous-lots.

[Carte de référence](https://app.notion.com/p/41d49e23bbdb81dd983eff8b4010cf39)
