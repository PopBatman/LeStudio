# Contrat de migration d’interface et de réversibilité

## Compatibilité des données

Les deux générations d’interface lisent les mêmes révisions immuables de composition. Le numéro du schéma de document est indépendant de la génération de l’éditeur. La stratégie proposée change le point d’entrée dans Studio. Chaque écriture intentionnelle conserve le service métier, le contrôle de tête et les conversions déjà prévues par la commande. Le lot ne prévoit aucun traitement de réécriture en masse. [Validation](../../../composition/validation.py) · [Sauvegarde des révisions](../../../composition/services.py) · [Commandes groupées](../../../composition/builder_batch.py)

| Témoin à préparer sur sites fictifs | Points à comparer après lecture, modification et retour V1 |
| --- | --- |
| Schéma 1, structure simple et définition épinglée | Document d’origine relisible à l’identique. Sur une écriture, inventorier l’unique différence attendue et toute évolution de schéma nécessaire. Une annulation intégrale conserve la tête. |
| Schéma 2, arborescence de pages et menus | Identités et parentés des pages, chemins, cibles et ordre des menus restent cohérents, y compris après navigation entre les deux interfaces. |
| Schéma 3, apparence, catalogue privé et article Wagtail | Vérifier les versions de définition, tokens, variantes et références du site, dont une version retirée déjà utilisée. Confirmer de nouveau une liaison éditoriale uniquement pour une action qui le requiert. |
| Schéma 4, conteneurs et placements | Rejouer flux, grille, position libre, bornes, superposition explicite et surcharge mobile. Vérifier l’héritage après retour en V1. |
| Imports Figma initiaux et ajoutés | Suivre UUID de page et d’occurrences, filiation de la révision, décision visuelle sur ancienne tête, associations de source encore autorisées. Une purge de remise conserve le document canonique. |
| Schéma inconnu ou dépendance indisponible | Afficher le diagnostic et les consultations autorisées. Refuser une écriture incompatible et vérifier l’historique. |

Archiver pour chaque témoin le site, les UUID, le numéro, le parent et l’empreinte de chaque révision, les références de composants/médias/articles, l’état publié et sa réponse HTTP. Vérifier aussi un brouillon créé par V2 **après** bascule. Soumettre deux écritures partant de la même tête depuis les deux interfaces, puis rejouer une sauvegarde de lot dont la réponse s’est perdue. Les résultats attendus sont une seule suite cohérente de révisions, un conflit explicite au besoin et des pages publiques identiques. FEAT-005 pourra prendre la révision par son identifiant existant.

## Séquence d’exploitation proposée

1. **Coexistence.** Garder les routes et services actuels. Établir la cartographie des liens et des commandes, y compris la fiche Site, le catalogue Article, les retours d’aperçu, le reçu d’import et les favoris. Examiner le code partagé avec le Visual Builder avant de décider quels fichiers pourront être retirés. Préparer un réglage de navigation réversible dans la configuration Studio et conserver l’image compatible qui sert encore les deux interfaces.
2. **Essai sur banc isolé.** À données égales, servir le CTA V2, enregistrer une modification en V2 puis rétablir l’entrée V1 par configuration. Ouvrir la nouvelle tête en V1, comparer son contenu et son rendu, puis revenir à la V2. Mesurer les commandes effectivement utilisées, le délai de récupération et les versions d’image/configuration. Le test doit aussi partir de la version candidate au retrait et réinstaller l’image de coexistence sur la même base.
3. **Bascule autorisée.** Après parité démontrée et avis humain sur le produit, appliquer le réglage sur la cible approuvée. La fiche Site et les retours métier privilégient V2. Masquer les anciennes commandes dans la navigation courante. Garder pendant l’observation un accès opérateur de repli aux vues V1 et documenter son emplacement. Tester une session déjà ouverte, son avertissement de sortie et une seconde session en lecture.
4. **Retrait autorisé.** Après examen de l’observation, retirer l’implémentation des anciennes vues et leurs assets exclusifs. Les anciennes URL GET connues peuvent rester des points de compatibilité vers la page V2 autorisée. Préserver le site, la page, la révision et l’occurrence uniquement si elles sont valides ; expliciter les options de format ou cibles devenues indisponibles. Un ancien POST doit être refusé avec une consigne pour relire la tête et reprendre dans le nouvel atelier. Ne jamais transférer automatiquement l’écriture. Les services encore appelés par l’éditorial, les calques et le canvas restent testés.
5. **Incident.** Si une tâche essentielle disparaît, si un droit s’élargit, si un brouillon ne se rouvre plus ou si une différence de données reste inexpliquée, interrompre la bascule. Consigner version, parcours, rôle et révision. Revenir à la configuration précédente, ou à l’image de coexistence testée si les vues ont été retirées. Maintenir les restrictions d’accès et préserver la tête courante. En cas d’atteinte à l’intégrité, suspendre les écritures concernées et qualifier l’incident avant reprise. Rejouer santé, droits, lecture, sauvegarde contrôlée sur témoin et empreintes publiques. Aucun retour de navigation ne doit restaurer une base, changer le moteur Wagtail ou republier le site.

La durée d’observation et le périmètre d’exposition seront consignés dans la décision opérationnelle. La proposition de configuration et les commandes de déploiement devront être vérifiées sur l’artefact à livrer. [Routes](../../../registre/urls.py) · [Matrice de parité](MATRICE-PARITE.md)

## Configuration réalisée et reprise en exploitation

Le service Compose `web` lit `STUDIO_EDITOR_MODE` à son démarrage. La valeur par défaut `coexistence` présente les deux entrées sur la fiche Site. La valeur `builder` dirige l’action principale et les retours métier vers V2. Les signets directs `/sites/<uuid>/atelier/` et `/sites/<uuid>/atelier/canvas/` permettent alors le repli opérateur. La valeur `compatibility` fait reprendre ces signets en V2 et répond 409 à un formulaire V1 autorisé resté ouvert. Les coordonnées de reprise sont validées sur le site et la révision accessibles.

Sur le poste local, conserver les mêmes fichiers Compose et le même nom de projet lors de chaque recréation. Après une bascule autorisée, remplacer `coexistence` par `builder` dans la commande ci-dessous. Pour revenir aux entrées V1, utiliser la valeur affichée. Exécuter depuis `studio/` avec l’image de coexistence qualifiée déjà installée.

```bash
STUDIO_EDITOR_MODE=coexistence docker compose -p lestudio-local \
  -f compose.yaml -f "$HOME/.config/lestudio/tennis-ai/studio-compose.yaml" \
  up -d --wait --no-deps --no-build web
```

Après un retrait physique, réaffecter d’abord le tag de l’image complète conservée au service web. Sur cette installation, `docker tag lestudio-local-web:coexistence-ui00305 lestudio-local-web:latest` rétablit cette image. Recréer le service avec la commande ci-dessus. Vérifier `/health/`, la destination de **Reprendre le brouillon**, la réouverture du dernier numéro de révision et les mandats de gestion et lecture. Le test sur copie PostgreSQL a conservé la base entre les quatre installations et comparé les empreintes de chaque document parent. [Journal des images, des délais et des révisions](evidence/retour-image.json)
