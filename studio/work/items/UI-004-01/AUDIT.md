# T01 — Audit de la composition et de l’éditeur installé

20 novembre 2026 · auteur /root, contributions lecture seule /root/t01_frontend et /root/t01_inventaire. Périmètre : code, services installés, navigateur, modèle et références ; aucun correctif produit réalisé.

## Couverture et niveau de preuve

| Sous-parcours / frontière | État d’examen | Preuve et limite |
|---|---|---|
| Accès opérateur/site, CSRF, droits gestion/lecture | Examiné et tests ciblés rejoués | test_builder_batch/edit_web/canvas ; pas de modification des droits du site réel |
| Modèle, révisions, UUID, copies/références et validation | Examiné et tests ciblés rejoués | Schémas 1–4, 1 Mio, 2 000 nœuds, profondeur 12 ; aucune migration nouvelle |
| Sélection/rendu moteur | Vérifié sur installé | Accueil R18, iframe réelle, UUID de texte sélectionné ; formats mesurés 1200/820/390 |
| Édition locale, texte long et undo | Vérifié sur installé | Formulaire local, confirmation puis undo ; empreinte R18 inchangée |
| Insertion/transfert, dimensions, sections | Examiné code et tests existants | Commandes présentes, pas de recette complète de chaque geste sur données métier |
| Sauvegarde/idempotence/conflit | Contrats existants rejoués sur SQLite isolé | 16 réussites, 1 test concurrence ignoré faute de select_for_update ; aucune sauvegarde sur Tennis AI |
| Catalogue/médias/version/portée | Examiné code et interface | Cinq types standards + article ; image désactivée car aucun média disponible |
| Reprise durable et autosave | Examiné code | Absents de l’interface actuelle ; pas de test d’une capacité inexistante |
| Navigation/import/comparaison/Wagtail avancé | Consommateurs examinés | Contrats/retours identifiés dans inventaire ; connecteur Figma réel à qualifier dans FEAT-006 |
| Configuration/build/routes/assets livrés | Examiné et comparaison image | 20 fichiers représentatifs identiques workspace/image ; build propre futur à T21 |
| Performance/lecteur d’écran/tactile matériel | À vérifier dans T18/UI-002 | Aucune conformité ou mesure de performance déclarée ici |
| Publication/restauration/production | Hors périmètre de réalisation T01 | FEAT-005 et T20 conservent leurs preuves et mandats |

Sources principales : [navigateur](evidence/audit-browser.json), [tests](evidence/tests-cibles-sqlite.log), [inventaire image](evidence/inventaire-image.json), [page de référence](evidence/page-reference.json). Code et artefacts sont identifiés par le manifeste du lot.

## Capacités et consommateurs à réemployer

| Capacité | Fichier / service observé | Consommateurs | Traitement |
|---|---|---|---|
| Brouillons immuables et tête attendue | composition/services.py, models.py, validation.py | navigation, édition, imports et preview | Réutiliser ; T02 doit garder compatibilité/version |
| Commandes structure/placement | editor.py::_apply/_canvas_change, placement.py | V1, builder_batch et editorial | Conserver/extrait partagé, pas suppression par nom |
| Sauvegarde transactionnelle et reçus | builder_batch.py::save_batch, BuilderSave | builder_views.save et UI du batch | Réutiliser droits, clé/empreinte, mapping ; T03/T08 ajoutent autosave |
| Catalogue interne | catalogue.py::bibliotheque/reference et appearance_contract | éditeurs, catalogue_views, moteur de validation/import | Réutiliser versions/portée/médias ; T10 qualifie extensions |
| Gestes pointeur déjà présents en V1 | static/ui/canvas.js::preview (resize:89–106, translation libre/transfert:108–126), capture/cancel/lostpointercapture:166–213 ; canvas_parent.html:18 émet les poignées | Ancien canvas cv-stage et formulaire cv-gesture (POST au lâcher) | Examiner/extrait des calculs, capture et annulation réutilisables avant suppression ; ne pas conserver l’ancien renderer/transport ni annoncer leur intégration au nouveau pont |
| Sélection/mesures | builder.js, builder-frame.js, builder_views.document | coque actuelle ; nouveau canvas à raccorder | Extraire contrat d’identité/port/CSP, remplacer ancienne coque |
| Rendu enregistré | composition/preview.py, preview_views et engine/reference/preview.py | FEAT-004, canvas et comparaison Figma | Réutiliser ; ne pas présenter projection locale comme rendu confirmé |
| Import et comparaison | depots/imports/provenance/comparison_views | remises, reprise builder, comparaison | Adapter consommateurs vers nouveau parcours, source réelle FEAT-006 |
| Édition Wagtail avancée | editorial.py/editorial_views et ArticleForm | page Articles et retours au builder | Conserver ; extraire formulaire partagé avant retrait V1 |

L’[inventaire T21](INVENTAIRE-T21.md) détaille tous les candidats d’écran, routes, scripts, styles, templates, flags, build, tests et guides avec leurs consommateurs. Aucun package React/TypeScript/drag dédié exclusif n’est installé : le build frontend actuel est Tailwind seul. Ne pas transformer cette absence en preuve de simplicité du futur parcours.

## Constats et ordre de résolution

| ID / priorité | Attendu → observé | Impact, preuve / confiance | Faisabilité, action minimale et propriétaire |
|---|---|---|---|
| T01-F01 · structurante | Éditer dans le rendu → cartes locales, canvas Wagtail masqué en édition | Confirmation navigateur et CSS builder-edit.css:2, renderPage:246 ; confirmé | Après modèle T02 : T03 qualifie rendu de travail et pont, sans changer le framework pour résoudre ce seul problème |
| T01-F02 · structurante | Geste libre avec voisins atomique → drop selon Y, une commande par historique, validation après chaque commande | builder-edit.js:146, model.commit:77, batch:136 ; déduit du code | T02 définit unité de geste/validation : une séquence avec collision transitoire ne doit pas simuler une atomie non disponible ; T04 généralise |
| T01-F03 · essentielle | Autosave/undo fiables → bouton Enregistrer, postPreview recharge, historique mémoire | builder-edit.js:577–609 et modèle replay ; confirmé code/interface | T03 minimum puis T08/T09 ; ordonner requêtes/acquittements/UUID et ne pas perdre les gestes plus récents |
| T01-F04 · interaction | Dans la V2 installée, resize et texte sur place → champs numériques/formulaire local et inspecteur permanent ; la V1 possède déjà des poignées et du drag libre sur sa propre surface | Captures installé et entryForm/settings ; confirmé | T05/T06 après T02 : réutiliser règles/commandes et examiner les calculs de canvas.js V1 avant extraction ; les adapter au pont/rendu/historique cible, conserver focus/caret et accès clavier/tactile |
| T01-F05 · donnée de recette | Pilote titre/image → aucun titre, image ou média attribué en R18 | Page JSON et bibliothèque réelle ; confirmé | Préparer en T03 un brouillon sur la même page et média de démonstration autorisé ; ne pas prétendre que la donnée existe déjà |
| T01-F06 · retrait | Seul nouvel éditeur livré → V1 encore chargé par URL en mode builder, ressources V1/V2 dans image | editor_navigation.legacy, settings/urls et inventaire image ; confirmé code/image, activation URL à vérifier par recette T21 | Inventorier maintenant, extraire partagés, remplacer puis supprimer T21 après T19 ; pas de suppression dans cet audit |
| T01-F07 · reprise | Réouverture retrouve non-confirmé → requête/gestes en mémoire seulement | Pas de journal durable observé, beforeunload/retry ; déduit du code | Arbitrage borné de stockage/rétention T09 ; pas de promesse universelle hors ligne |
| T01-F08 · formats | Surcharges compréhensibles/lecture cohérente → modèle déjà présent mais rendu de travail séparé | placement.py et formats réels mesurés ; code + navigateur | T02/T07 qualifient texte long/voisins/ordre et héritage ; les captures seules ne valident pas tout le responsive |

Ces constats regroupent les causes ; les actions sont rattachées aux cartes existantes sans nouveau backlog concurrent. Aucune fuite de données ou corruption n’a été démontrée par cet audit. Ce périmètre ne constitue pas un audit de sécurité exhaustif.

## Conséquences, incertitudes et repli

- T02 peut réemployer le schéma 4 seulement si ses cas d’usage passent. Une nouvelle propriété ou commande impose validation Studio et moteur, compatibilité/import, tests et migration explicite.
- Le rendu de travail doit rester local et réactif tout en correspondant aux règles Wagtail ; T03 devra éprouver une voie précise. La sélection/pointeur ne doit pas dépendre du serveur. Les contenus/code arbitraires restent interdits.
- Le groupement de voisins n’est pas garanti par la seule transaction de save_batch : le validateur actuel examine chaque commande. Décider avant implémentation ; un changement doit prouver rollback, collisions et undo.
- Les extractions partagées précèdent le retrait. layers_for, ArticleForm et plusieurs classes ed-* ont des consommateurs hors anciens écrans. Supprimer leurs fichiers d’un bloc casserait Figma, articles ou aperçus.
- Le retour opérationnel après T21 utilise une image/version précédente compatible avec les données et les sauvegardes nécessaires ; pas d’ancien éditeur dormant dans le code courant.
- La concurrence PostgreSQL n’a pas été requalifiée ici. Le cas ciblé SQLite est explicitement ignoré, non compté comme réussi ; T03/T09 devront l’exercer sur PostgreSQL.

## Résultat de l’audit

AC1 : matrice et inventaire avec consommateurs. AC2 : [contrat de référence](REFERENCE-PRODUIT.md). AC3 : [décision frontend](DECISION-FRONTEND.md). AC4 : pages, UUID, données absentes et scénarios explicités. [Comparaison visuelle](evidence/comparaison-reference.html) : même Accueil R18 ; capture installée versus coque illustrative autour d’une copie exacte du rendu Wagtail, avec variante de texte long simulée.
