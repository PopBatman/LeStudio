# Droits et intégrité pendant la coexistence et le retrait

| Cas | Vérification exigée avant décision |
| --- | --- |
| Session et mandat | Sur deux sites fictifs, exercer gestion, lecture seule, absence de mandat et révocation en cours de session. Vérifier page, calques, formulaires, historique, rendu, média privé et référence Figma par leurs entrées normales. Une redirection vers V2 refait le contrôle de portée. |
| Écriture V1 en vol | Ouvrir un formulaire puis changer de mode. Pendant la coexistence, valider CSRF, droits et révision de base via le service courant. Après retrait, refuser explicitement la soumission et proposer de relire la tête. Aucun corps de POST ne doit être rejoué vers la nouvelle route. |
| Écriture V2 ou réponse interrompue | Conserver le sens de la clé de sauvegarde, l’ordre des commandes et le contrôle de tête. Vérifier la reprise après coupure et la révocation avant écriture. Un changement d’interface ne transforme pas des gestes locaux en sauvegarde. |
| Aperçu et contenus Wagtail | Vérifier session, site et durée du reçu privé. Tester panne, moteur incompatible, article retiré, référence d’un autre site et capacité d’édition de l’article épinglé. Comparer les contenus publics avant/après sur les deux sites. |
| Source Figma | L’ancien lien de remise ou un favori ne confère aucun droit de gestion. Tester source purgée, page canonique encore visible, PNG retiré et historique privé indisponible. |
| Retour en arrière | Restaurer uniquement le routage ou l’image Studio qualifiée. Vérifier aussitôt les restrictions après révocation et la présence des révisions enregistrées depuis la bascule. Empreintes et compteurs servent de témoins ; aucun secret ni contenu client dans les preuves. |
