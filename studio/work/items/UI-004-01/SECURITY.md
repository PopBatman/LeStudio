# T01 — Risques de l’audit

| Risque concret | Contrôle | Preuve / limite |
|---|---|---|
| Modifier Tennis AI pendant une inspection | Aucun POST de sauvegarde, publication ou modification de données ; lecture et gestes locaux non confirmés seulement | Numéro et empreinte de révision avant/après comparés ; reçus temporaires d’aperçu distincts |
| Accéder au mauvais site ou élargir les droits | Choisir un opérateur déjà autorisé ; services normaux acteur/site | Identifiants minimaux de contexte ; pas de nouveau compte/rôle |
| Fuite de cookie/secret | Session temporaire en mémoire du script, non imprimée ; suppression à la fin | Captures hors cookies, logs filtrés ; aucun .env lu |
| Tests sur base active | Test runner SQLite mémoire ou base isolée déclarée ; pas de migration sur données métier | Commandes/environnement et résultat consignés |
| Exécution d’une ressource externe | Prototype adopté copié, inspection locale avec réseau extérieur bloqué | Simulation séparée de l’application installée |
| Inventaire interprété comme suppression autorisée | Candidats justifiés par consommateurs ; migrations/services partagés préservés | T21 garde retrait et requalification après T19 |
| Faux succès ou preuve périmée | Relier AC, sources, image et observations ; conserver échecs/corrections | Contrôles et revue sur artefacts finaux, limites explicites |

