# T02 — Risques, permissions et erreurs

Version 1 · risque STANDARD, aucune donnée réelle modifiée par le cadrage.

| Risque | Contrat et preuve prévue |
|---|---|
| Écriture ou lecture d’un autre site | Contexte acteur/site et habilitation dans le service, vérifiés avant reçu/rejeu ; tests deux sites et révocation |
| Geste partiellement appliqué | Copie par groupe puis validation finale ; transaction de lot et aucune révision/reçu sur échec |
| Écrasement concurrent | Révision de base contrôlée sous verrou de site ; course PostgreSQL et reçu idempotent |
| Contenu caché / voisin perdu | Hauteur et reflow explicites ; pas de conversion/migration silencieuse ; aller-retour et texte long |
| Import ou configuration exécutables | Champs typés/bornés et catalogue interne versionné ; aucun CSS/HTML/JS libre ni URL média arbitraire |
| Surcharge ou structure cyclique | Budgets taille/nœuds/profondeur/commandes ; groupes et opérations dans budget global ; refus avant traitement coûteux |
| Pont de rendu détourné ou périmé | Réemploi nonce/MessageChannel/CSP et contexte frame/page/version ; mesures périmées invalidées ; extensions qualifiées en T03 |
| Ressource retirée | Références média/contenu résolues dans le site ; diagnostic distinct de la conservation d’un historique ; pas de réautorisation par migration |
| Version moteur divergente | Version supportée vérifiée, refus explicite ; ne jamais certifier l’état de travail comme aperçu enregistré |

Les preuves utilisent des données fictives ou les métadonnées minimales de T01 ; pas de secret, cookie, token, export complet client ni consultation de .env. Studio ne modifie pas directement les bases des moteurs, n’emploie pas SSH et ne publie pas par l’autosave.

Pas de migration de base nécessaire présumée pour un changement JSON ; examiner les besoins réels avant de générer une migration Django. Pour les brouillons, conserver les révisions anciennes et créer une nouvelle révision de conversion explicite. Repli sur version/image compatible selon schéma réellement écrit.

Le cadrage est documentaire. Les tests de sécurité ci-dessus sont planifiés ; ils n’ont pas été rejoués pendant cette mission.

