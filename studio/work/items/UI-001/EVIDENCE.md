# Preuves de UI-001

Les observations datent du 18 novembre 2026. Le [registre technique](task.json) conserve les dates UTC, les empreintes des artefacts et celles des sources associées.

| Preuve | Observation |
|---|---|
| [Maquette](evidence/maquette.html) | Référence illustrative préparée avant le développement des templates. |
| [Tests initiaux](evidence/red.json) | RED historique. Trois assertions échouaient avec les nouvelles routes absentes. Le contrôle Django courant les remplace. |
| [Exécution Django et HTTP](evidence/django.json) | Contrôles système et migrations, sept tests, dépendances et vérification des réponses servies par Compose. |
| [Parcours Chromium](evidence/browser.json) et [script exécuté](evidence/parcours.cjs) | Navigation au clavier, états du formulaire, texte long, filtre, largeur effective et analyse axe-core aux deux formats. |
| [Desktop](evidence/desktop.png) et [page entière](evidence/desktop-complet.png) | Chromium à 1440 × 960. |
| [Mobile](evidence/mobile.png) et [page entière](evidence/mobile-complet.png) | Chromium à 390 × 844. |
| [Avis indépendant](REVIEW.md) | Correction du débordement, nouvelle observation sur le serveur local et avis favorable. |

Pour reproduire le parcours, démarrer la galerie sur le port 8000. Exécuter `node evidence/parcours.cjs` depuis le dossier du lot avec Playwright et axe-core accessibles à Node. `CHROMIUM_PATH` permet de choisir un exécutable Chromium et `UI_OUTPUT` un répertoire de sortie existant. Par défaut le script crée un répertoire temporaire. Le contrôle exécuté utilisait Playwright 1.64.0-alpha-1790635538000 et axe-core 4.14.1, avec la version de Chromium indiquée dans le résultat.
