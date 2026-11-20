# Inventaire préparatoire au retrait V1/V2 — T01 vers T21

20 novembre 2026 · exécution réelle `/root/t01_inventaire` · lecture seule du produit.

Cet inventaire contribue à AC1 de T01 et à la préparation de [UI-004-14 / T21](https://app.notion.com/p/41e49e23bbdb81189b25e4404b1afa47). Il classe les fichiers, consommateurs et points de livraison observés ; il ne constate aucune suppression. T21 se clôture après T19, puis T20 utilise l’artefact nettoyé et requalifié. [Contrat parent](../UI-004/ARCHITECTURE.md).

## Méthode et couverture

Examen des routes et vues, imports directs et dynamiques, inclusions de templates, chargements JS/CSS, styles partagés, configuration, dépendances, contexte Docker, tests et guides actifs. Recherches `rg -n` ciblées dans `composition/`, `depots/`, `registre/`, `central/`, `templates/`, `static/ui/`, `tests/`, `docs/` et fichiers de build connus ; les fichiers secrets sont exclus.

Les chemins ci-dessous sont relatifs à `studio/`. Les lignes sont celles observées lors de cet audit ; le manifeste du lot identifie les versions. « Supprimer » désigne un candidat au retrait après remplacement et qualification du parcours. Un nom historique ne prouve pas qu’un fichier est exclusif.

| Frontière | Couverture de cet inventaire | Limite |
|---|---|---|
| Écrans Structure/Canvas V1 et coque/édition V2 | Examiné par code, templates, routes et chargements | Aucun geste navigateur exécuté par cet agent |
| Composition, sauvegarde, catalogue, droits et Wagtail | Consommateurs partagés identifiés | Les tests métier ne sont pas rejoués par cet agent |
| Import/comparaison Figma et édition avancée | Imports et liens vers les builders examinés | Pas de qualification d’une source Figma réelle ici |
| Build et dépendances | Sources Docker, Tailwind, requirements, CI examinées | Absence future d’anciens fichiers à prouver sur le build T21 |
| Image installée | 20 fichiers représentatifs comparés au workspace | Échantillon, pas inventaire intégral de l’image |
| Anciennes routes/configurations | Dispatch et modes examinés dans le dépôt | Configurations externes d’exploitation à rapprocher par T21 sans exposer de secret |

## Inventaire et consommateurs

| Classe / groupe | Fichiers ou éléments | Consommateurs observés et traitement |
|---|---|---|
| Supprimer après remplacement — V1 serveur | `composition/editor_views.py`, `canvas_views.py`, `canvas_forms.py` | `editor_navigation.py:25` importe dynamiquement `editor_views.editor`. Ce dernier importe `CanvasForm` et `surface` aux lignes 14–16. Chemin propre aux écrans Structure/Canvas. |
| Supprimer après remplacement — V1 templates | `templates/composition/editor.html`, `editor_inspector.html`, `editor_definition.html`, `editor_article.html`, `editor_observation.html`, `canvas_surface.html`, `canvas_parent.html` | `editor_views.py:165` rend `editor.html`, qui inclut le canvas et l’inspecteur aux lignes 49 et 54. Les wrappers `editor_article.html` et `editor_observation.html` incluent les templates partagés `editorial_*` : retirer les wrappers, préserver leurs cibles utiles. |
| Supprimer après remplacement — V1 frontend | `static/ui/editor.js`, `canvas.js`, `canvas.css` | Chargements dans `templates/composition/editor.html:2,56`. `canvas.js` porte déjà resize (`preview:89–106`), translation libre/transfert (`108–126`), capture/cancel/lostpointercapture (`166–213`), avec poignées dans `canvas_parent.html:18`. Examiner et extraire les mécanismes utiles avant retrait : leur dépendance à `cv-stage` et au formulaire POST `cv-gesture` ne convient pas telle quelle au nouveau pont/historique. Retirer ensuite fichiers, chargements et ressources exclusives ; aucune ancienne surface dormante. |
| Remplacer — V2 coque/projection | `templates/composition/builder.html`, `builder_edit.html` ; `static/ui/builder.css`, `builder-edit.css`, `builder-edit.js` | `builder_views.py:94` rend la coque ; `builder.html:12` inclut `builder_edit.html`, qui charge modèle et logique JS aux lignes 23–24. La projection `.be-node` est l’ancienne implémentation à retirer. Le nouvel éditeur remplace les fonctions utiles, sans garder un ancien écran dormant. |
| Conserver/extrait partagé — modèle de gestes | `static/ui/builder-edit-model.js` | Consommé par `builder-edit.js`, chargé par `builder_edit.html:23`. Commandes, UUID, replay/undo et invariants utiles au nouveau parcours. Extraire ou remplacer les parties activement réutilisées ; supprimer ce qui ne sert que la projection V2. Un fichier conservé exige un usage actuel démontré. |
| Conserver/extrait partagé — pont Wagtail | `static/ui/builder.js`, `builder-frame.js`, portions de `builder-drop.js` et de `composition/builder_views.py` | `builder_views.py:160–162` lit le module frame par chemin de fichier pour l’instrumentation contrôlée. `builder.html:62–63` charge drop/coque. Préserver les garanties du pont sélection/mesure ; remplacer navigation et interactions exclusives. Un déplacement de module exige mise à jour du chargement, de la CSP et des tests. |
| Conserver/extrait partagé — lecture des calques | `composition/builder_views.py::layers_for` à la ligne 38 | Import direct par **`depots/comparison_views.py:16`**. Supprimer globalement `builder_views.py` casserait la comparaison Figma. Extraire le sélecteur ou adapter le consommateur avant retrait du handler. |
| Conserver/extrait partagé — formulaire article | `composition/editor_forms.py::ArticleForm` | **`composition/editorial_views.py:14,77`** l’utilise encore. Le reste de `editor_forms.py` (`ACTIONS`, `LayoutForm`, `editor_form`, `command`, `secure_url`) est consommé par `editor_views.py`. Extraire `ArticleForm` avant retrait du module exclusif V1. |
| Conserver — métier de composition | `composition/editor.py`, `builder_batch.py`, `services.py`, `validation.py`, `placement.py`, `appearance_contract.py`, `catalogue.py`, `structure.py`, `canvas_format.py` | `builder_batch.py:11` importe `_FIELDS/_apply/_block_location/_canvas_change/_member` de `editor.py` ; `editorial.py:16` partage des helpers. `builder_views.py:25,27–30` consomme format, création, structure et services. Ces contrats ne sont pas du code mort d’écran. |
| Conserver — modèles/migrations | `CompositionRevision`, `PreviewTicket`, `BuilderSave` ; migrations composition dont `0006_builder_save.py` | `BuilderSave` est lu/créé par `builder_batch.py:160,189` pour l’idempotence et lu par `builder_views.py:57`. Migration nécessaire à installation/mise à niveau. Le nom `BuilderSave` ne justifie aucune suppression de données ou migration. |
| Conserver et adapter les liens — édition avancée | `editorial_views.py`, `editorial.py`, `editorial.html`, `editorial_article.html`, `editorial_observation.html` | Contrat Wagtail avancé indépendant. `editorial_views.py:45,69,89` construit le retour vers `registre:site-builder`. Préserver la capacité et diriger vers le seul nouvel éditeur. |
| Conserver et adapter — comparaison/import | `depots/comparison*.py`, `provenance.py`, `imports.py` ; `templates/composition/figma_compare.html` ; `static/ui/figma-compare.js/.css` ; templates `depots/import_*` | Liens de `comparison_views.py:181–202,290–291` vers `site-builder/builder-view` avec `edit=1`. `import_review.html:11–12` expose aussi ces destinations. Adapter liens et sélection ; ne pas supprimer la comparaison avec la coque V2. |
| Remplacer — sélecteurs/fallback de transition | `composition/editor_navigation.py`, réglage dans `central/settings.py`, Compose, processeur de contexte, branches templates | `STUDIO_EDITOR_MODE` défini en `settings.py:18–20`, injecté en `compose.yaml:23`, processeur enregistré en `settings.py:71`. `navigation_context:16–19` fournit `editor_coexistence/studio_editor_route` ; `legacy:22–26` importe V1 sauf en mode compatibility. Le mode **builder masque les entrées, mais garde V1 accessible par le dispatch des anciennes URLs**. |
| Adapter ou retirer — routes V1 | `registre/urls.py:42–43` : `site-canvas`, `site-editor` | Peuvent devenir redirections explicites testées. Ne doivent plus charger ancien handler/rendu. Les vieux POST ne doivent pas rejouer implicitement une commande ; `compatibility()` répond actuellement 409 via `editor_resume.html`. Réévaluer ce contrat sans garder le flag de réactivation V1. |
| Remplacer — routes de coque V2 | `registre/urls.py:37–40` : `site-builder`, `builder-save`, `builder-view`, `builder-document` | Les noms d’URL peuvent éventuellement devenir ceux du nouveau parcours. Le retrait porte sur l’implémentation, pas le nom seul. Conserver/extrait des endpoints partagés et adapter tous les consommateurs. Les routes Figma `:35–36` ont encore un usage actif. |
| Adapter — retours d’aperçu | `composition/preview_views.py:35–40` | `destination()` interprète `origine=editor/canvas` et `STUDIO_EDITOR_MODE` pour choisir V1 ou builder. Retirer la branche de réactivation V1, garder les retours utiles depuis les signets. |
| Nettoyer partiellement — styles communs | `static/ui/registre.css:66–86`, sélecteurs `ed-*` | **Pas de suppression globale du bloc** : usages actifs hors V1 dans `depots/import_node.html:8,12` (`ed-pages/ed-form`), `import_review.html:16,25` (`ed-choices/ed-form`), `composition/preview_prepare.html:10,15` et `preview_view.html:29` (`ed-pages`), `editorial_article.html:4` (`ed-values`). Retirer uniquement les règles sans consommateur ou renommer les styles partagés avec leurs usages. |
| Conserver — fondations et ressources partagées | `gallery.css`, `workspace.css`, `registre.css` hors règles exclusives, DM Sans et sa licence | Chargements communs `workspace/base.html:7–8`, autres espaces actifs. Aucun fichier séparé d’icônes/police/image exclusivement V1/V2 identifié dans les sources examinées ; pictogrammes builder surtout en glyphes/caractères. |

### Points qui empêchent une suppression par nom

1. `editor_forms.py` contient un formulaire encore utilisé par l’édition avancée.
2. `builder_views.py` contient un sélecteur importé par la comparaison Figma.
3. `registre.css` contient des classes `ed-*` encore partagées par import, aperçu et édition avancée.
4. `editor.py`, `builder_batch.py`, `BuilderSave` et les migrations portent des contrats de persistance actifs.
5. `editor_navigation.legacy` effectue un import différé : analyser uniquement les imports en tête de fichier manquerait la réactivation V1.

## Configuration, dépendances et artefact

| Point | Constat | Traitement T21 |
|---|---|---|
| Ressources HTTP | `central/urls.py:38` autorise `editor.js`, `canvas.js/.css`, `builder.js/.css`, `builder-edit.js/.css`, `builder-drop.js`, `builder-edit-model.js` | Nettoyer les fichiers exclusifs et l’autorisation de livraison ; vérifier leurs URLs directement après build |
| Contexte Docker | `.dockerignore:45–58` inclut explicitement les anciens assets, dont `builder-frame.js` | Actualiser la liste ; conserver seulement les entrées utilisées par le nouvel éditeur |
| Image | Dockerfile copie `composition/`, `templates/`, `static/ui/`, `tests/` selon le contexte filtré | Build propre obligatoire, inspecter image et fichiers servis. Image précédente réservée au retour opérationnel, pas copiée dans la nouvelle |
| Tailwind | `frontend/gallery.css:2` scanne `../templates` | Recompiler après retrait des templates pour retirer les utilitaires sans usage |
| npm/lockfile | `frontend/package.json` et lockfile : Tailwind/CLI ; pas de React, TypeScript ou package de gestes dédié | Aucune dépendance npm exclusive supprimable identifiée. Ne pas retirer Tailwind ; rendre le lockfile cohérent avec tout changement futur |
| Python | Requirements Studio et moteur : Django/Cotton/PostgreSQL/Pillow/Wagtail et dépendances partagées | Aucun package exclusivement builder identifié ; ne pas supprimer une dépendance sur une recherche de nom |
| CI | `.gitlab-ci.yml` : job global Django/PostgreSQL, aucune étape propre à un builder | Adapter les suites attendues ; pas de job exclusif à retirer actuellement |
| Variable de transition | `STUDIO_EDITOR_MODE` dans settings et Compose ; aucune occurrence dans `local.env.example` | Retirer ou remplacer les branches permettant de réactiver V1/V2 et rapprocher la configuration d’exploitation effective sans exposer les secrets |
| Commandes/permissions | Pas de commande Django ou permission dédiée exclusive identifiée ; les droits sont ceux du site | Conserver les contrôles opérateur/site ; rechercher de nouveau les consommateurs quand le nouveau code sera stabilisé |
| Historique | Anciens dossiers V1/V2 et preuves dans `work/items/` | Conserver comme preuves passées, sans charger leurs prototypes dans le produit ni copier les anciens éditeurs dans un dossier dormant |

### Échantillon du conteneur installé

[Comparaison enregistrée](evidence/inventaire-image.json) : commandes exactes, répertoire de travail, date UTC, version Python, sorties/code retour et SHA-256 pour chaque entrée.

Les **20 fichiers représentatifs sont présents dans le conteneur web et identiques au workspace** : handlers/formulaires/navigation V1, handlers/batch V2, JS/CSS V1/V2 et trois templates principaux. L’observation confirme que les implémentations existent dans l’installation courante, pas seulement dans des rapports. Elle ne constitue pas une recette des gestes ou un inventaire intégral de l’image.

## Tests à conserver, déplacer ou adapter

| Groupe | Traitement attendu |
|---|---|
| `test_editor_web.py`, `test_canvas_web.py`, `test_editorial_web.py` | Retirer/adapter les attentes d’anciens écrans vers le nouveau parcours ; conserver droits, conflits et références utiles. `test_editorial_web.py:89` patche encore `composition.editor_views.editorial_admin_url`. |
| `test_editor_transition.py` | Remplacer coexistence/builder/compatibility et retour V1 par anciennes URLs vers seul éditeur, absence de réactivation et reprise des signets |
| `test_builder_canvas.py`, `test_builder_edit_web.py`, `test_builder_parity.py` | Adapter coque/projection ; conserver pont isolé, droits, manifeste et sauvegarde lorsque leur contrat reste actif |
| `test_builder_batch.py` | Conserver atomicité, idempotence, copies/références et concurrence ; adapter seulement les changements contractuels |
| `test_editor_services.py`, `test_editor_concurrency.py`, `test_canvas_domain.py` | Conserver invariants métier/placement partagés ; retirer uniquement attentes exclusives d’écran |
| `test_editorial_builder_web.py`, `test_figma_compare_web.py`, `test_figma_imports.py`, `test_figma_provenance.py`, tests éditoriaux/services/transport/moteur | Consommateurs encore nécessaires ; vérifier après liens adaptés et extraction des helpers |

Les noms de fichiers ne suffisent pas à décider quels tests sont devenus sans objet. T21 doit maintenir les garanties des contrats encore utilisés et rejouer les scénarios critiques sur la révision après nettoyage.

## Guides actifs et historique

- `docs/BROUILLONS.md:64–84` : procédures Structure/Canvas et anciens contrats ; `:101–103` : accès directs V1 et sauvegarde manuelle V2.
- `docs/MOTEUR-WAGTAIL.md:42,50–75` : retours d’aperçu, sélection/composition dans le canvas et comparaison.
- `README.md` ne comporte pas de procédure builder autonome ; préserver le démarrage et l’exploitation générale.
- Dossiers `work/items/FEAT-003-04/`, `FEAT-003-05/`, `UI-003/` et `UI-003-01/` à `UI-003-05/` : contrats, maquettes, rapports et preuves historiques conservés. Leur présence ne permet pas de relancer l’ancienne application depuis le nouvel artefact.

## Faisabilité, ordre de traitement et limites

Le retrait est réalisable après remplacement des parcours et qualification T19. Il est prématuré dans T01 : le nouveau contrat de disposition et le rendu de travail ne sont pas encore implémentés. Une suppression immédiate détruirait des parcours utiles et certains contrats partagés.

Ordre partiel recommandé :

1. Extraire les helpers, formulaires et styles activement partagés ; fournir des consommateurs et tests explicites.
2. Raccorder édition avancée, import/comparaison, aperçu et navigation au seul nouvel éditeur.
3. Définir les anciennes URLs et vieux POST ; supprimer sélecteurs, flags, imports/fallbacks de réactivation.
4. Retirer physiquement handlers, vues/templates, projection JS/CSS et ressources exclusives au fil de leur remplacement qualifié.
5. Nettoyer contexte Docker, livraison HTTP, manifests/lockfiles si concernés, tests et guides actifs.
6. Construire proprement, prouver installation et mise à niveau, ouvrir anciens documents et contrôler les ressources effectivement servies.
7. Rejouer vierge/template/Figma, ancien brouillon, gestes/sauvegarde, aperçu, publication/restauration et faire relire le diff **après** nettoyage.

Une recherche textuelle seule ne prouve ni absence de chargement dynamique, ni absence d’ancien bundle dans une image. Tout élément conservé exige un usage partagé ou une obligation de migration démontrée. Le retour opérationnel s’appuie sur une version/image antérieure compatible et les sauvegardes utiles ; aucune copie dormante V1/V2 dans le code courant.

Ce rapport n’autorise et n’atteste aucune correction. Les lignes et consommateurs doivent être revalidés sur la révision candidate de T21. Aucun test applicatif, build propre, migration, déploiement ou contrôle d’une configuration secrète n’a été exécuté par cet agent.
