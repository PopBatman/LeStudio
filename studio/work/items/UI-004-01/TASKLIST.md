# T01 — Ordre d’exécution

Écrite avant scripts et références de comparaison du lot. Le mandat couvre l’audit, ses supports, contrôles, revue et publication documentaire.

| ID | Résultat | Dépend de | Zone / exécutant réel | Vérification |
|---|---|---|---|---|
| A1 | Relecture Notion, règles et périmètre rapprochés | — | Dossier T01, /root | Carte/parent/vision/roadmap/T21 et socles ; changement utile signalé |
| A2 | Inventaire capacités et graphe des consommateurs V1/V2 | A1 | Sources en lecture seule, /root/t01_inventaire ; /root/t01_frontend | Fichiers/fonctions/consommateurs localisables ; classer partagé/remplacer/supprimer sans supprimer |
| A3 | Révision/page et état installé identifiés, tests ciblés isolés | A1 | /root, preuves T01 | Hashes locaux/image, métadonnées sans secrets, tests sans modification du brouillon |
| A4 | Référence de gestes et comparaison installé/cible sur même contenu | A2/A3 | /root, référence HTML et navigateur | Desktop/mobile, sélection, contenu long, scénarios et portée T03 ; simulation clairement marquée |
| A5 | Décision frontend et transmission T02/T03/T21 | A2/A4 | /root | Choix motivé, coût/limites, données/rendu partagé et critères de passage |
| A6 | Revue indépendante, correction des écarts et contrôle des preuves | A3/A4/A5 | Reviewer distinct à identifier | AC1–AC4, contrats, preuves, empreintes et liens cohérents |
| A7 | Rapport court, carte et jalon parent à jour | A6 | /root | Résultat utilisable, limites et prochaine unité, sans lancement T02 implicite |

Aucune modification de comportement métier n’étant demandée, pas de cycle RED/GREEN artificiel. Les scripts de collecte/validation reçoivent leurs propres assertions utiles ; les tests existants sont rejoués uniquement sur les frontières de l’audit. Les preuves de l’ancien builder restent historiques.


## État de sortie

A1–A6 exécutées : audit, inventaire, navigateur/tests, référence, décision et revue terminés. Le rapport technique et le registre portent les résultats ; la publication A7 est consignée dans evidence/publication-notion.json dès son exécution, sans lancer T02. Le produit et la révision Tennis AI ne sont pas modifiés.
