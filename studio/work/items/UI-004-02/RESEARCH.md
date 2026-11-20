# T02 — Sources et état réel rapprochés

20 novembre 2026 · lecture de cadrage, sans tests applicatifs ni interrogation de la tête courante. Pas de dépôt Git exploitable dans LeStudio ou studio ; identification par manifeste SHA-256.

## Notion relu avant cadrage

Les pages complètes relues figurent dans [sources-notion.json](evidence/sources-notion.json) : carte T02, parent UI-004, T01, règle de relecture « 03 — Workflow, tasklist et preuves », guide de prise de lot, vision produit, roadmap, socle FEAT-003-01, catalogue FEAT-003-03, aperçu FEAT-004 et futur parcours T03. Leurs dates d’édition ne valent pas approbation. La carte T02 initiale est DRAFT, type Architecture, UI requise non ; T01 est DONE, parent PLANNED.

Décisions humaines reprises : manipulation directe/prototype adoptés et retrait physique V1/V2 imposé dans le plan courant du 20 novembre. Choix frontend : décision technique de l’auteur T01, JS natif sur Django. Aucun choix de grille, schéma ou protocole de rendu immédiat n’est présenté comme accepté par l’utilisateur.

## Matrice de l’existant

| Source locale | Constat observé en lecture | Conséquence T02 |
|---|---|---|
| composition/validation.py, placement.py | Schémas 1–4 ; flow/free et stack/grid ; unités locales, champs et limites stricts | Comparer avant extension, préserver lecteurs et bornes |
| composition/editor.py | block_place peut appliquer parent/before et placement | Garder le transfert atomique et tester les repères |
| composition/builder_batch.py | Transaction/idempotence/base existent ; document et collisions validés après chaque commande | Nouveau groupe de geste final cible/voisins, distinct du lot |
| static/ui/builder-edit-model.js | block_place n’applique pas parent/before comme le serveur | Test de parité explicite avant réemploi/extraction |
| engine/reference/preview.py | Rendu schémas 1–4, min-height calculée depuis les enfants free ; hauteur fixe des boîtes | Contrat contenu long et nouveaux champs à propager au renderer |
| composition/figma_mapping.py | Produit du schéma 4, identités source/occurrence ; ne traduit pas toute position/dimension | Adapter au contrat final sans prétendre qualifier Figma réel |
| composition/canvas_format.py et renderer | Seuils 768/1024 ; formats de démonstration 390/820/1200 | Tester aussi largeur 980 et voisinage des seuils |
| Catalogue et services | Définitions versionnées, médias par site, historique/conflits/droits | Migration sans propagation de catalogue ni contournement |
| T01 / REFERENCE-PRODUIT.md et page-reference.json | Audit R18 sans titre/image ni média disponible | Préparation contrôlée en T03, aucune donnée créée ici |

La collision existante compare les frères libres ; le mélange flux/libre n’est pas couvert par cette détection. La largeur flow en grille est relative à l’aire de grille, contrairement à la largeur free relative au parent contenant. Ces écarts interdisent de recopier naïvement une boîte entre modes/parents.

## Vérifications prévues et limites actuelles

Prolonger tests/test_composition_validation.py, test_composition_services.py, test_builder_batch.py, test_builder_parity.py, test_builder_canvas.py, test_preview_bridge.py, test_figma_mapping.py, test_figma_imports.py et test_figma_provenance.py ; moteur engine/reference/test_preview.py. Les tests déjà réussis dans T01/FEAT-004 ne sont pas déclarés rejoués.

La mission ne modifie que le dossier T02 et sa restitution Notion. Aucun rendu navigateur nouveau nécessaire pour les documents de cadrage ; la preuve de rendu appartient à la réalisation planifiée. Aucun connecteur Figma réel appelé.

## Délégation réelle

/root/t02_existant : lecture seule indépendante des modèles, commandes, renderer et producteurs ; aucun fichier autorisé à l’écriture ; rapport reçu, limites intégrées. /root/t02_revue : revue indépendante favorable du cadrage, sans réserve de fond ; compte rendu dans REVIEW.md et evidence/revue-cadrage.md.

Comparaison de fraîcheur : les 213 sources du manifeste T01 sont identiques au workspace courant. Cette comparaison est enregistrée dans evidence/comparaison-sources-t01.json ; elle ne réinterroge ni l’image Docker ni la tête du brouillon.

## Limite des outils Workflow AI

Le CLI partagé ne reconnaît que des identifiants sans suffixe et lie Architecture au préfixe ARCH. T02 possède déjà l’identité Notion UI-004-02 et le type Architecture ; ne pas renommer la carte ni la transformer en composant pour contourner cette limite. Le contrôle complémentaire local evidence/check-planning.py adapte uniquement l’identité/type de ce lot dans un module chargé en mémoire, vérifie les documents et refuse les opérations hors cadrage. Le workflow partagé reste inchangé. Le PASS complémentaire n’est ni une validation des gestes ni un mandat d’implémenter.

