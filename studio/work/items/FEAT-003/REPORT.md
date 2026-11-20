# Bilan du cadrage parent

Le point d’entrée proposé est la fiche Site existante, avec un accès à l’atelier selon le mandat. La section Wagtail livrée dans ARCH-002-01 reste alimentée par son service de lecture. Le brouillon, sa révision et les éventuelles versions appliquées possèdent leurs propres sources. Cette distinction permet de préparer un nouveau site même avant son premier raccordement.

La [spécification](SPEC.md) décrit les comportements et la [tasklist](TASKLIST.md) répartit les réalisations entre les huit cartes du Kanban. Les [contrats](ARCHITECTURE.md) et les [règles d’accès](SECURITY.md) lient ces cartes à un même modèle de brouillon. La [recherche](RESEARCH.md) indique pour chacune les interfaces existantes et ce qui reste à vérifier. Le premier sous-lot à prendre est FEAT-003-01. Il préparera le stockage local et ses contrôles de concurrence. Le premier parcours opérateur complet dépend ensuite des sous-lots 02 à 04.

Le mandat couvre le cadrage et les maquettes de la fiche, examinables dans le [compte rendu visuel](VISUAL-REVIEW.md). Les révisions d’atelier, actions de création, portail et import font partie du produit à réaliser. Les huit cartes enfants gardent leur état et leurs propres exigences de développement et de recette. Les accords de conception humaine, tests métier et preuves d’application seront consignés lorsqu’ils auront lieu.

Contributions du cadrage : /root pour les sources, la spécification, le plan, le registre et le rapprochement Notion ; /root/feat3_arch pour les contrats et les permissions ; /root/feat3_design pour les maquettes et leur examen ; /root/feat3_review pour la [revue indépendante](REVIEW.md).

## Premier incrément de réalisation

Le développement suit l’ordre du Kanban. Le [rapport du socle de composition](../FEAT-003-01/REPORT.md) documente le stockage local et la recette du premier sous-lot. Les pages et menus (02) et la bibliothèque (03) peuvent ensuite être cadrés sur ce contrat. La création ou la reprise depuis la fiche Site relève du sous-lot 04.

## Livraison de l’atelier et de ses huit sous-lots

Le registre local et les rapports des sous-lots 01 à 07 attestent le socle de brouillons, la navigation, le catalogue, l’éditeur structuré, le canvas responsive, les références éditoriales Wagtail et les remises du portail graphiste. Le lot 08 ajoute le troisième point de départ de l’atelier. Une sélection Figma revue par le gestionnaire produit une composition versionnée V4, accessible ensuite dans les mêmes interfaces. [Rapport 08](../FEAT-003-08/REPORT.md)

**FEAT-003 est DONE pour le Studio local.** La qualification du fournisseur du sous-lot 08 a été simulée à la demande de l’utilisateur. La suite complète sur PostgreSQL, la recette navigateur, les deux voies de création et d’ajout et la revue indépendante sont référencées dans les [preuves du dernier incrément](../FEAT-003-08/EVIDENCE.md). Le Visual Builder V2 reste suivi dans UI-003.
