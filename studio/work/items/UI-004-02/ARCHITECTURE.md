# T02 — Architecture du périmètre préparé

Version 1 · cadrage ; les chemins ci-dessous sont les zones de réalisation futures, pas un mandat d’écriture actuel.

| Propriétaire | Réemploi constaté | Travail prévu |
|---|---|---|
| Modèle central | composition/validation.py, placement.py, appearance_contract.py, models.py, services.py | Schéma/compatibilité, règles finales parent/format/boîte ; sauvegarde et droits existants |
| Commandes | composition/editor.py, builder_batch.py | Groupe atomique cible/voisins, contrôle final par geste et transaction de lot |
| État local | static/ui/builder-edit-model.js ; gestes canvas.js historiques | Isoler modèle utile sans dépendance DOM V1/V2, parité parent/before/placement ; aucune ancienne interface conservée comme cible |
| Rendu moteur | engine/reference/preview.py, assets/preview.css et templates/reference/preview_blocks.html | Même sémantique par version, texte/ratio/voisins, diagnostics version incompatible |
| Producteurs | composition/editor.py, assets/presentation-activite-v1.json, figma_mapping.py | Aucun producteur laissé en version 4 si le contrat requiert la version 5 ; conserver imports déjà enregistrés |
| Pont / aperçu | composition/preview.py, static/ui/builder-frame.js et pont de prévisualisation existant | T02 fixe identité/repère/génération ; protocole de mutation et surface qualifiés en T03 |
| Documentation | docs/DISPOSITION.md prévu ; docs/BROUILLONS.md et docs/COMPOSANTS-UI.md | Une référence durable et liens de contrats ; pas de copie concurrente par origine |

## Interfaces

Voir [contrat proposé](CONTRAT-PROPOSE.md). Transport versionné, entrées bornées, acteur/site/base explicites. Réutiliser le reçu idempotent et le mapping UUID. Erreurs : document/commande/format invalide, cible incompatible, collision, ressource/composant indisponible, clé réutilisée, base périmée, moteur incompatible ou indisponible. Conserver leurs codes existants quand applicables ; nouveaux codes et statuts HTTP documentés avec les tests du transport au lancement.

Un batch atomique existant n’est pas un groupe de geste : la validation intermédiaire dans _command est l’écart principal. La parité JS/serveur doit inclure block_place avec parent/before, que le modèle local actuel ne traite pas comme le serveur. Ne pas déplacer une validation uniquement dans le navigateur.

## Réalisation bornée

T02 livre contrats, extension minimale nécessaire et démonstrateur/tests de modèle + rendu. Son lancement éventuel doit autoriser explicitement ces zones ; task.json n’autorise actuellement que work/items/UI-004-02/. Aucun nouvel écran d’édition, bundle React/TypeScript, import Figma réel, endpoint d’application ou retrait physique V1/V2 pendant ce cadrage.

Architecture frontend retenue par T01 : JavaScript natif organisé par responsabilités, servi par Django. Ce choix est technique, sans nouvelle validation humaine inventée. Extraire et qualifier les mécanismes utiles ; conserver l’inventaire T21.

## Options et décision attendue

Réutiliser version 4 si les essais représentent toute l’intention ; sinon étendre par version 5. Comparer flux/grille pour déplacement X et contenu variable, libre borné conditionnel pour superposition. Rejeter le tri vertical comme réponse intégrale à AC1 ; ne pas figer une grille universelle depuis la maquette.

Le rendu immédiat de T03 doit partager effectivement les règles du moteur. Le présent cadrage ne promet pas qu’une projection de cartes et l’aperçu sont équivalents. Les manifests/identités/version et génération de mesures doivent permettre de détecter un état périmé.

## Vérification prévue

Tests de schéma/placement/commandes, parité JS/serveur, concurrence et reçu sur PostgreSQL, fixtures historiques, adaptateurs vierge/template/Figma simulé au niveau annoncé. Renderer Wagtail réel sur compositions fictives et largeurs de référence. T03 reprend la vraie page et la chaîne complète sans publication ; T19/T21 couvrent la bascule et le retrait.

