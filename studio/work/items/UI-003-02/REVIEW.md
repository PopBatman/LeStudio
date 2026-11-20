# Revue indépendante du cadrage · 20 novembre 2026

Exécutant : `/root/u302review`. La [carte UI-003-02](https://app.notion.com/p/41d49e23bbdb818e8587c6e772f22913) demande de comparer la page effectivement rendue par Wagtail à celle du canvas pour une même révision, de sélectionner une occurrence stable et de conserver les droits et l’état publié.

## Examen du socle effectivement livré

Les empreintes SHA-256 des quatre relevés FEAT-004 ci-dessous et des trois captures du moteur sur ordinateur, tablette et mobile concordent avec le registre task.json de FEAT-004.

| Pièce examinée | Ce qu’elle établit pour le cadrage |
| --- | --- |
| [Relevé navigateur](../FEAT-004/evidence/navigateur.json) | Les cinq UUID sont identiques et dans le même ordre aux largeurs de cadre 1200, 820 et 320 px. Image et police étaient chargées. Le pointage dans une composition imbriquée nécessite un essai propre à UI-003-02. |
| [Relevé mTLS](../FEAT-004/evidence/rendu-mtls.json) | Deux instances de laboratoire, retrait d’un média, restriction d’article et reprise après coupure disposent d’observations existantes. Une nouvelle sélection doit réutiliser le contrôle des dépendances et du mandat du reçu. |
| [Échéance et tête de révision](../FEAT-004/evidence/peremption.json) | Le reçu de R3 s’est distingué de la tête R4 ; le reçu expiré renvoyait 410. Une navigation de page et un changement de tête pendant un chargement doivent faire l’objet d’une recette V2. |
| [Comparaison avant/après](../FEAT-004/evidence/non-publication.json) | Les objets avant/après des deux moteurs et de Studio sont identiques. Répéter la comparaison pour les nouveaux gestes d’ouverture, de sélection, de changement de largeur et d’actualisation. |

Le contrôle des identités, de l’ordre et de l’unicité est réalisé dans [preview.py](../../../composition/preview.py). Le contrôle à la délivrance, l’échéance, l’empreinte de rendu et la réponse isolée sont examinables dans [preview_views.py](../../../composition/preview_views.py). Ce rapprochement s’appuie sur les sources et preuves existantes.

Les 13 tests existants des modules `tests.test_preview_bridge`, `tests.test_preview_cleanup`, `tests.test_preview_web` et `tests.test_preview_transport` ont été rejoués le 20 novembre dans le conteneur web Studio local avec `central.test_settings` (SQLite en mémoire). Tous passent. Ce contrôle qualifie le socle de l’aperçu dans l’image installée.

## Contrôle indépendant de la maquette

Dans Chromium, à 320 px, j’ai ouvert Itinéraires puis sélectionné sa deuxième occurrence au clavier depuis les calques. Le calque et le bloc ont porté la même sélection et l’inspecteur a indiqué leur UUID. La simulation de péremption a retiré l’UUID sélectionné ; le repli après indisponibilité a affiché la structure en masquant la page rendue. La largeur du document était de 320 px et aucune requête HTTP(S) n’a été émise pendant ce parcours. L’exercice a porté sur les données fictives de [la maquette](evidence/maquette.html).

## Avis de cadrage

La spécification, la tasklist, les contrats d’architecture et de sécurité et la revue visuelle couvrent les cinq critères Notion. La recette proposée associe le clic sur un enfant et le choix du calque parent à leurs UUID distincts ; le jeu de données à deux sites vérifie les droits de chaque contexte. Le document FEAT-004 sert de témoin pour comparer la page instrumentée, à même largeur et ressources chargées. Les cas de page absente de la nouvelle tête, de réponse tardive et de retrait du mandat ont une condition de sortie explicite.

**Avis favorable au cadrage.** Le nouveau canal de sélection dans une iframe opaque, la géométrie des contours et la parité du rendu instrumenté demandent encore un essai sur le moteur réel et une revue indépendante pendant la réalisation. Le repli de lecture conserve un contrôle d’autorisation propre. Les essais au lecteur d’écran et les captures appariées du nouveau canvas relèvent de cette recette applicative.

## Revue de réalisation
/root/u302_real_review a examiné le code livré, les en-têtes d’isolation et la parité visuelle des trois formats. Le correctif d’échéance du document ouvert directement a été vérifié. [Avis indépendant](evidence/revue-realisation.md).

/root/canvas_qual a qualifié deux moteurs Wagtail isolés et comparé les surfaces au même reçu ainsi que les états publics avant/après. [Rapport de recette](evidence/avis-recette-wagtail.md).
