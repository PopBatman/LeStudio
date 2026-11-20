# Autorisations et erreurs

| Contexte | Contrôle à vérifier dans Studio |
|---|---|
| Opérateur actif avec lecture | Réutiliser les lectures de composition filtrées par SiteGrant et appartenance au groupe. Une demande de modification en lecture seule reçoit 403. |
| Site inconnu, accès absent ou révoqué | Pour un opérateur authentifié, même réponse 404 sur lecture, calcul d’impact et écriture. La connexion reste requise pour les vues web. |
| Opérateur avec gestion | Vérifier le droit courant dans la transaction d’enregistrement. L’UUID du site dans la route délimite les pages, menus et révisions. Refuser la référence à un autre site sans le nommer. |
| Formulaire et chemins | POST avec protection CSRF. Échapper titres, libellés et erreurs. Valider le document entier, les UUID, slugs, cycles, limites et toutes les destinations avant écriture. |
| Entrée externe | Autoriser uniquement une URL HTTPS absolue selon le contrat. Aucun chargement ni contrôle réseau depuis le serveur pendant la validation. L’analyse d’impact couvre les références de pages du document. |
| Effacement et conflit | Contrôler à nouveau la révision et les impacts sous verrou, même pour un appel direct au service. Une décision périmée doit être réexaminée. Aucun changement partiel. |

Préparer en TDD deux sites et deux opérateurs, un accès retiré entre examen et confirmation, une révision périmée, un UUID externe valide syntaxiquement, un protocole interdit et du texte contenant du balisage. Observer refus, absence de fuite et absence de nouvelle révision sur échec. Les exemples de cadrage utilisent des données fictives.
