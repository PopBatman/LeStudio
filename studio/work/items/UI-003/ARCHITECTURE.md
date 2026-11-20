# Architecture du Visual Builder V2

## Responsabilités et existant vérifié

| Frontière | Réemploi et travail à prévoir |
|---|---|
| Studio central | La fiche Site et le portefeuille déterminent le contexte de l’opérateur. La coque V2 réunit pages, calques, composants, médias, canvas et inspecteur. Les onglets, le focus, la sélection, le format et les gestes en cours relèvent de l’interface. |
| Composition | `composition/services.py` lit le brouillon et ses révisions par site. Une sauvegarde acceptée crée un descendant de la tête sous verrou. `editor.py`, `navigation.py`, `appearance_contract.py` et `placement.py` possèdent les opérations et validations. Les schémas 1 à 4 sont reconnus par le validateur. Tester chaque ancien schéma en lecture et lors de sa première modification. |
| Bibliothèque | `catalogue.py` expose les définitions globales et du site, avec portée, clé, version et état, ainsi que les médias autorisés. Les règles d’insertion et de conservation des références historiques doivent s’appliquer aux commandes de la V2. Le moteur dispose de renderers explicitement développés. Un élément non pris en charge porte un diagnostic. |
| Remises Figma | `depots/imports.py::confirm` rattache une décision confirmée à une révision Studio et conserve la correspondance des occurrences. L’éditeur ouvre cette composition, y compris les nouvelles pages ajoutées à un brouillon, par leurs identifiants canoniques. Un ancien reçu peut désigner une révision historique. Proposer alors de reprendre la tête et vérifier que la page y existe. |
| Rendu Wagtail | `composition/preview.py` assemble les données autorisées, sollicite l’instance raccordée et vérifie le manifeste. `engine/reference/preview.py` et ses gabarits produisent le HTML des composants installés. Les droits de publication et d’administration du moteur sont distincts du mandat d’édition Studio. |

## Édition et révisions

Les entrées vierge et template reprennent `creer_atelier`, l’entrée Figma une remise déjà confirmée. Les trois convergent sur les mêmes services et le même document. La provenance est une information de traçabilité. Un changement ultérieur dans Figma ne synchronise pas le brouillon.

Une intention cible le site courant, l’UUID de la révision de base, la page et l’occurrence. Un déplacement désigne le parent de destination et, si besoin, le voisin avant lequel insérer. Les gestes au pointeur et les commandes clavier doivent produire la même intention. L’inspecteur explicite les valeurs héritées et les surcharges par format. Dupliquer exige de nouveaux UUID pour l’occurrence et sa descendance. Les références aux définitions et ressources doivent rester valides dans la portée du site.

Le parcours proposé distingue le travail local en cours de la révision enregistrée. Annuler/rétablir agit sur les gestes avant sauvegarde, y compris une suppression. La V1 enregistre les commandes structurelles individuellement. UI-003-03 devra donc qualifier leur regroupement ou une sauvegarde validée atomiquement avec le comportement de confirmation existant. Si la tête a avancé, conserver la saisie le temps d’examiner le conflit et de reprendre sur la tête relue. Une réponse incertaine implique de relire la tête avant toute répétition. La restauration d’un état appliqué au site relève de FEAT-005.

## Sélection dans le rendu

L’aperçu FEAT-004 porte site, instance, page, UUID et numéro de révision, ressources et liste ordonnée des blocs. Le gabarit `preview_blocks.html` émet `data-studio-block-id` pour chaque occurrence. Studio vérifie leur identité, ordre et unicité. Il sert le document dans une iframe à origine opaque avec une CSP restrictive. L’aperçu actuel ne fournit ni rectangles de sélection ni pont d’événements vers l’éditeur.

UI-003-02 doit qualifier un mécanisme d’association entre cible affichée et UUID. La sortie attendue lie page, site, instance, révision, empreinte du rendu et format de visualisation à la cible. À chaque défilement, changement de largeur, nouvelle révision ou expiration, recalculer ou invalider les repères. La coque porte les contrôles d’édition et les libellés accessibles. Les calques permettent une sélection au clavier par UUID. Toute mesure manquante, périmée ou ambiguë désactive l’action spatiale concernée. L’identification d’un bloc par sa seule position dans le DOM serait instable. Le pont et sa stratégie de mesure restent une décision de conception de UI-003-02, à vérifier dans un vrai navigateur avant intégration.

Pendant la saisie, indiquer la dernière révision effectivement rendue et les modifications en cours. Après sauvegarde, préparer un reçu pour la nouvelle révision. Écarter une réponse tardive concernant une autre page ou une ancienne révision. Si le moteur est indisponible, limiter le repli à la lecture de la composition avec un état explicite. Les valeurs de base, les surcharges tablette/mobile, l’imbrication, les blocs répétés, le zoom et le défilement entrent dans la comparaison de rendu.

## Évolution et retrait

Le cadrage ne requiert aucune migration de données. Avant bascule, confronter les écrans V1 et V2 aux mêmes brouillons et révisions, en particulier les contenus éditoriaux Wagtail liés et les versions de composants anciennes. Prévoir un accès V1 réversible durant la qualification. UI-003-05 documentera la parité, le résultat du retour V1 et la décision humaine avant masquage, puis les conditions d’un retrait ultérieur. Les révisions et les services métiers demeurent nécessaires après le retrait des vues.

Sources projet : [contrats Studio](../../../docs/ARCHITECTURE-CONTRACTS.md), [brouillons](../../../docs/BROUILLONS.md), [livraison de l’aperçu](../FEAT-004/REPORT.md), [recette Figma simulée](../FEAT-003-08/REPORT.md), [vision produit](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539).
