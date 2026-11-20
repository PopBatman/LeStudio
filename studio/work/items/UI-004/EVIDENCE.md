# Preuves du cadrage

Périmètre : préparation documentaire, sans modification applicative, de données métier ou de configuration d’exploitation.

| Artefact | Ce qu’il démontre | Limite |
|---|---|---|
| [Sources Notion](evidence/sources-notion.json) | Cartes/références réellement lues et exigences rapprochées | Instantané, pas preuve d’exécution ni autorisation |
| [Sources actualisées](evidence/sources-notion-actualisees.json) | Relecture après ajout de T21 pendant la session ; versions courantes parent/vision/roadmap/T19/T20/T21 | Remplace les versions des mêmes pages du premier instantané, qui reste historique |
| [Prototype adopté](evidence/prototype-adopte.html) | Copie exacte de la pièce jointe de la vision | Simulation, auteur initial non attesté |
| [Inspection de référence](evidence/inspection-reference.json) | Ouverture Chromium 1440/390 sans réseau, métadonnées et SHA du prototype | Pas de test des gestes, Wagtail ou sauvegarde réelle |
| [Bureau](evidence/reference-simulee-1440.png) / [petit écran](evidence/reference-simulee-390.png) | Rendu du prototype effectivement ouvert, images examinées | Références simulées ; pas des captures du nouvel éditeur |
| [État local](evidence/etat-local.json) | Métadonnées Docker/Tennis AI observées par commandes en lecture seule | Pas une qualification de raccordement ou de rendu |
| [Manifeste](evidence/manifest.json) | Empreintes du contrat et des sources examinées, en l’absence de Git | Ne certifie pas un approbateur |
| [Revue](REVIEW.md) | Relecture du cadrage par un agent distinct | Pas une recette applicative |
| [Contrôles](evidence/controles.log) | Check planning et fingerprint exécutés sur le dossier | Le CLI ne teste pas le produit ni les permissions réelles |

Délégation réelle : auteur/coordonateur `/root` ; lecture de code `/root/audit_existant` ; revue indépendante identifiée dans REVIEW.md. Les empreintes actives du registre portent sur le cadrage, sans réutiliser les preuves anciennes comme tests du nouvel éditeur.

Tests applicatifs, concurrence, raccordement actuel, mesures de performance, lecteur d’écran, publication et bascule : non exécutés ici, à prouver dans les sous-lots indiqués par la tasklist.
