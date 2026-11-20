# Frontières et choix techniques UI-004

Cadrage v1 · 20 novembre 2026. [Contrats Studio](../../../docs/ARCHITECTURE-CONTRACTS.md). Aucun code ni dépendance modifié ici.

## Réemploi et interfaces

| Propriétaire | Contrat actuel | Adaptation à cadrer |
|---|---|---|
| Registre / accès | Acteur/site explicites, `services._writing_site`, droits de gestion sous verrou | Autosave et reprise gardent ces droits ; aucun accès admin client/graphiste |
| Composition | `CompositionRevision`, schémas 1–4, tête verrouillée et historique | T02 éprouve avant extension ; migration explicite, anciennes révisions intactes |
| Commandes | `editor._apply/_canvas_change`, `builder_batch.save_batch` ; key/base/page/commands/selection, validation, atomicité et mapping UUID | Geste/voisins atomiques ; T08 avance base/mapping sans reload ; limites 128 commandes, 1 Mio, 2 000 nœuds |
| Catalogue | `catalogue.bibliotheque`, portée/version, propriétés et médias contrôlés | T10 qualifie cinq types avant ajouts, templates et copies |
| Aperçu | `preview.render_preview`, `engine/reference/preview.py`, manifeste et reçu | Conserver identité de la révision rendue pendant une nouvelle saisie |
| Pont | `builder_views.document`, builder/frame/drop JS ; iframe opaque, CSP, nonce, MessageChannel, rectangles UUID | T03 qualifie événements/rendu de travail ; aucune ouverture aux scripts/messages arbitraires |
| Import | `depots/imports.py`, correspondances et provenance ; recette historique simulée | FEAT-006 qualifie source réelle et modèle T02 sans écraser les corrections |
| Moteur | Instance Wagtail : contenus avancés/rendu ; raccordement mTLS | Aucune écriture SQL directe/SSH ; application explicite dans FEAT-005 |

## Organisation frontend : recommandation à conclure en T01

Le projet possède déjà modèle de commandes JS et pont isolé ; `frontend/package.json` ne compile que Tailwind. React/TypeScript ne sont pas installés dans ce projet. Un framework ne résout pas seul l’écart de rendu.

| Option | Coût et intérêt | Position de cadrage |
|---|---|---|
| JS modulaire sur Django actuel | Réemploie modèle/pont/services/tests ; clarifier états et éviter les reconstructions DOM qui perdent le focus | Recommandation initiale pour éprouver J1 sans migration globale |
| Îlot React/TypeScript pour l’éditeur | Garde backend/renderer ; ajoute compilation, dépendances et migration des états/événements | Option si T01 établit un gain justifiant ce coût ; parité/pont/coexistence à tester |
| Réécriture frontend générale | Toucherait registre, accès et autres écrans | Hors périmètre, aucun besoin constaté ne la justifie |

T01 rend une décision motivée avant code. La recommandation de l’auteur n’est pas une approbation utilisateur. Une intégration React peut être limitée à une partie de l’application : [documentation primaire](https://react.dev/learn/add-react-to-an-existing-project), consultée le 20 novembre 2026.

## Rendu de travail : décision T02/T03

Actuellement `builder-edit.js::renderPage` reconstruit des cartes `.be-node` et le CSS masque le canvas Wagtail en édition. Après sauvegarde manuelle, `postPreview` recharge le rendu. Le pont Wagtail mesure/sélectionne ; il ne transmet pas de document de travail mutable.

Comparer une couche d’édition sur le rendu moteur avec transformations locales connues, et une projection qui partage réellement les règles de présentation du moteur. Toute extension de protocole reste bornée, authentifiée, isolée et sans publication. Sélection et mouvements ne doivent pas attendre le réseau. Aucune voie n’est déclarée acquise ici.

Condition de choix : à page/révision/largeur identiques, boîtes, contenu, retour à la ligne, styles et imbrication concordent après geste/réouverture. Mesures recalculées ou invalidées après scroll, resize, police/image chargée, changement de page/révision. Un écart interdit de présenter le travail comme aperçu confirmé et doit être traité pour J1.

## Modèle de disposition : décision T02

`placement.py` possède flux/libre borné, X/largeur en %, Y/hauteur en px, span, z et héritage base/tablet/mobile. Le moteur accepte au plus le schéma 4. La grille 12 colonnes et le pas 16 px du prototype sont des détails de simulation.

T02 éprouve flux, grille et groupes libres bornés sur les pages retenues en T01 : déplacement horizontal réel, parent/enfant, ordre de lecture, taille intrinsèque, texte long, ratio, voisins, superposition et héritage. Taille de boîte et typographie sont distinctes ; toute propriété nouvelle est décrite, validée et rendue jusqu’au moteur et aux imports.

Un geste provisoire ne modifie pas le confirmé. Son commit regroupe composant et voisins en une intention annulable. Définir regroupement atomique et mapping UUID si plusieurs commandes sont nécessaires. Un transfert de parent conserve identité/références et recalcule explicitement ses coordonnées/contraintes locales.

## Sauvegarde, historique et HTTP

Réutiliser POST JSON, CSRF et `save_batch`. Même requête logique = même clé ; modification ultérieure = nouvelle clé. Une sauvegarde en vol par contexte est la proposition initiale ; les gestes plus récents restent en attente. L’acquittement lie révision, numéro, sélection et mapping ; il ne marque jamais une intention ultérieure enregistrée.

Le point d’entrée actuel accepte HEAD (204 si autorisé) et POST JSON : 400 corps illisible, 415 type de contenu incorrect, 413 taille excessive, 422 validation, 409 conflit de base ou clé réutilisée avec un autre contenu, 403 gestion/CSRF refusée et 404 ressource masquée. T03 conserve et qualifie ces réponses pour les nouveaux usages. Le point d’entrée existant est JSON ; aucun remplacement HTMX imposé. Une redirection HTML de session ou une réponse inattendue ne valent pas acquittement : préserver les intentions, réauthentifier et relire selon les droits.

T08 définit l’undo à travers les autosauvegardes : les révisions ne sont pas supprimées ; annuler un geste déjà confirmé crée une nouvelle intention valide. T09 définit conservation, portée acteur/site et purge de la reprise après fermeture. La mémoire JS actuelle ne prouve pas de reprise durable. Revérifier les droits avant reprise/réessai.

## Compatibilité, retrait obligatoire et repli

Le code actuel garde les anciens écrans V1/V2 et leurs routes ; les rapports historiques restent consultables. La décision Notion actualisée impose désormais **T19 → T21 → T20** : recette/compatibilité, suppression physique puis requalification, production de l’artefact nettoyé. T21/UI-004-14 est obligatoire pour clôturer le parent ; T19 ne dépend pas de T21.

Dès T01, inventorier fichiers, routes/handlers, consommateurs et chargements dynamiques ; classer supprimer/remplacer/conserver avec usage démontré. T21 retire les vues, templates, composants, JS/CSS/icônes/assets exclusifs, flags/préférences/fallbacks, imports différés, endpoints/commandes/settings/variables/permissions/registrations/adaptateurs sans consommateur, packages exclusifs et étapes CI/build ; actualiser lockfiles, manifestes, fixtures/tests et guides. Retirer les modules remplacés au fil du travail si le parcours reste qualifié ; la clôture T21 attend T19.

Conserver ou extraire clairement les services de composition, révisions, catalogue, droits, sauvegarde et Wagtail réellement partagés ; conserver les migrations utiles à une installation ou mise à niveau. Le nom V1/V2 seul ne justifie aucune suppression. Ne pas garder de copie dormante des éditeurs dans le code courant. Les rapports et preuves passées demeurent ; aucun historique Git n’est créé ou supposé dans cet espace.

Après nettoyage : construire proprement assets/image, inspecter aussi les fichiers effectivement servis et prouver l’absence des anciennes implémentations/ressources. Une ancienne URL peut rediriger vers le nouvel éditeur selon un contrat testé ; elle ne doit charger ni ancien handler ni ancien rendu. Une recherche textuelle seule ne démontre pas l’absence de chargement dynamique ou de ressource dans l’image.

La révision nettoyée doit passer installation propre, mise à niveau supportée, reprise des schémas 1–4 et des références/templates/imports/médias, puis les parcours vierge/template/Figma, gestes, sauvegarde, aperçu, publication et restauration. Relier tests, captures et revue du diff à ce nouveau candidat. T20 utilise cet artefact, pas celui antérieur au nettoyage.

Le retour opérationnel s’appuie sur une version/image précédente identifiable et des sauvegardes compatibles avec les données. Une évolution de schéma T02 doit éprouver ce repli ; elle ne justifie pas de conserver deux éditeurs désactivés dans la version courante. Tout consommateur ou nettoyage restant maintient T21, la clôture UI-004 et la production pilote ouverts.
