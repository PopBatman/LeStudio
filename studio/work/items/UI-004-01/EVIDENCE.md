# T01 — Index des preuves

| Artefact | Observation | Limite |
|---|---|---|
| [Sources Notion](evidence/sources-notion.json) | Carte, règle, parent/vision/roadmap/T21 et socles relus au lancement | Références documentaires, pas autorisation technique nouvelle |
| [Page R18](evidence/page-reference.json) | UUID/contenus de référence, sections, thème et empreinte | Métadonnées et contenu minimal de la page de démonstration |
| [Navigateur réel](evidence/audit-browser.json) et [script](evidence/audit-browser.cjs) | Contexte, commandes, navigateur, étapes, largeurs mesurées, empreinte avant/après et suppression de session | Aucun POST de sauvegarde ni test du futur éditeur |
| [Capture Wagtail](evidence/installe-wagtail-1440.png), [édition locale](evidence/installe-edition-1440.png), [mobile](evidence/installe-edition-390.png), [texte long](evidence/installe-texte-long-local.png) | Rendu réellement ouvert et différence entre canvas et projection | Une capture seule ne vaut pas conformité accessible |
| [Formats 1200](evidence/installe-wagtail-format-1200.png), [820](evidence/installe-wagtail-format-820.png), [390](evidence/installe-wagtail-format-390.png) | Largeurs de l’iframe mesurées dans le navigateur | Pas de validation de tous les cas responsive |
| [Rendu capturé](evidence/rendu-wagtail-r18.html) | Copie exacte du document Wagtail après retrait du script de pont pour lecture locale | Ne constitue pas un nouveau reçu moteur |
| [Tests ciblés](evidence/tests-cibles-sqlite.log) et [métadonnées](evidence/tests-cibles-sqlite.json) | 16 succès et 1 cas PostgreSQL ignoré sur SQLite mémoire | Concurrence PostgreSQL non rejouée |
| [Inventaire livré](INVENTAIRE-T21.md) et [comparaison image](evidence/inventaire-image.json) | Consommateurs et 20 sources identiques entre workspace et image | Pas un inventaire de tous fichiers internes de l’image |
| [Comparaison autonome](evidence/comparaison-reference.html), [test de référence](evidence/check-reference.json) | Même contenu de page ; largeur/texte long/onglets et clavier du rapport | Cible simulée, aucune fonction d’édition produit livrée |
| [Bureau du rapport](evidence/comparaison-bureau.png), [mobile du rapport](evidence/comparaison-mobile.png), [pilote](evidence/reference-pilote.png) | Support de référence ouvert réellement | Images illustratives, distinctes des captures produit |
| [Sources empreintées](evidence/manifest-sources.json) | Identifie les sources de l’audit et de la suite ciblée, comparaison workspace/image | Ne certifie pas un approbateur |
| [Revue indépendante](REVIEW.md) | AC1–AC4, inventaire, décision et transmission examinés | Pas une validation humaine du nouvel éditeur |

Le premier essai de collecte cherchait un titre absent de R18 et s’est arrêté sur un timeout : [résultat historique](evidence/audit-browser-premier-essai.json), conservé inactif au registre, pas compté comme réussite. La collecte finale sélectionne le texte réellement présent, indique les préconditions titre/image et passe ses assertions.

Les scripts d’audit/référence portent des assertions adaptées ; aucune logique métier produit n’est modifiée. Pas de RED/GREEN artificiel ni de nouvelle installation de dépendance. L’adaptateur de contrôles du sous-lot appelle les fonctions Workflow AI existantes avec la seule extension locale du format d’identifiant.

Auteur : /root ; contributions : /root/t01_inventaire et /root/t01_frontend ; reviewer final distinct identifié dans REVIEW.md. Les preuves du parent et des anciens builders restent historiques et ne sont pas annoncées rejouées.
