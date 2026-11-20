# Risques et contrôles UI-004

Cadrage documentaire du 20 novembre 2026. Écritures présentes : dossier UI-004 et synthèse Notion. Les vérifications de réalisation ci-dessous restent à exécuter dans les sous-lots.

| Surface | Risque | Contrôle / responsable | Preuve attendue |
|---|---|---|---|
| Droits/site | Autosave ou réessai sur site retiré, lecture inter-sites | Services acteur/site sous verrou, CSRF conservés ; T03/T09 | Gestion/lecture, site A/B, révocation/session expirée, ancienne clé |
| Pont | Message forgé ou mesure d’une ancienne page | Iframe opaque/CSP/module fixe, contexte/nonce/port ; T03 | Source/contexte inconnus refusés, scroll/resize, expiration |
| Texte/médias/styles | Injection ou référence privée détournée | Propriétés typées, texte échappé, médias du site, renderer contrôlé ; T02/T06/T10 | Collage riche selon contrat, liens invalides, média retiré/inter-site |
| Geste | Capture perdue ou saisie/drag corrompt le document | Travail provisoire séparé, annulation et validation complète ; T02/T04–T07 | Échap, pointercancel/capture perdue, multi-pointeur, descendance, texte long |
| Sauvegarde | Acquittement tardif trompeur, doublon après réponse perdue | Base/clé/empreinte et acquittement du lot exact ; T03/T08/T09 | Réponses inversées, même clé/clé altérée, atomicité et concurrence PostgreSQL |
| Reprise | Perte après fermeture ou contenu local conservé après révocation | T09 définit stockage minimal, acteur/site, rétention/purge ; rien ajouté ici | Fermer/rouvrir, déconnexion, autre acteur, révocation/expiration |
| Rendu | Projection locale annoncée certifiée ; mesures absentes | Distinguer travail/révision Wagtail ; suspendre geste spatial sans repères fiables ; T03 | Moteur indisponible, média/police tardifs, rendu périmé |
| Migration | Nouveau schéma casse ancien document/repli | Versionnement explicite, historique et compatibilité ; T02/T19/T21 | Lecture 1–4, nouvelle sauvegarde, retour compatible et décision humaine |
| Retrait V1/V2 | Ancien éditeur réactivable par URL/flag ou bundle encore livré ; service partagé supprimé par erreur | Inventaire consommateurs dès T01, suppression physique T21 après T19, usages conservés démontrés, build et tests APRÈS nettoyage | Sources et fichiers servis/image sans anciens builders, installation/mise à niveau et tous parcours critiques requalifiés avant T20 |
| Performance | Fluidité du prototype annoncée acquise | Appareil/scénario/candidat/budgets dès T03 ; T18/UI-002 | Traces simple/dense et résultats humains distincts |

Aucun secret, cookie, clé privée ou donnée client supplémentaire dans les preuves. Contenus de démonstration autorisés pour la recette. Le code des composants est livré par l’équipe ; une maquette ne peut installer du code. Application et production restent distinctes dans FEAT-005/ARCH-003. Limites observées : [RESEARCH.md](RESEARCH.md).

