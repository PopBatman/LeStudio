# Habilitations et protection du brouillon

| Acteur ou donnée | Règle à appliquer sur chaque entrée du service |
|---|---|
| Opérateur actif, mandat Site en lecture | Tête et révisions du site seulement. Écriture refusée. |
| Opérateur actif, mandat Site en gestion | Création, révision et lecture sur ce site. La gestion d’un site ne confère aucun pouvoir sur le catalogue global ou sur Wagtail. |
| Mandat Client seul, autre site, UUID inconnu | Même réponse de ressource introuvable pour un site ou une révision ciblée. Dans un document destiné à un site accessible, une référence imbriquée étrangère reçoit le même diagnostic de champ invalide qu’une référence absente. |
| Compte anonyme, inactif, hors groupe ou révoqué | Appliquer la frontière FEAT-001/002 à la lecture et au commit. Aucun compte client/graphiste pour ce service. |
| Provenance et contenu | Auteur, site, parent et numéro déterminés côté serveur. Ressources privées et références éditoriales validées par portée de confiance. Un UUID fourni dans le JSON n’est pas une preuve d’appartenance. |

Les données Studio peuvent être privées. Accepter les seules propriétés typées prévues dans le [document V1](COMPOSITION.md). Exclure les scripts, plugins et secrets de liaison, les URLs internes et les chemins de fichiers. Les journaux techniques limitent les informations au type d’opération, résultat et identifiants autorisés ; ne pas journaliser le document, un lien Figma privé ou des commentaires tiers. Les diagnostics de validation gardent seulement le nom du champ et le motif. Couvrir rejet d’une référence inter-site, droits retirés entre lecture et sauvegarde, défaillance de validation et absence d’appel à une instance distante.

Les exemples et preuves utilisent des données fictives. Les révisions sont immuables dans le parcours normal. Conservation, effacement et sauvegardes doivent s’inscrire dans la procédure existante du registre avant traitement de données personnelles ; l’immutabilité de l’édition ne constitue pas une politique de conservation illimitée.
