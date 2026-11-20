# Sources et observation du dépôt

La carte [ARCH-002-01](https://app.notion.com/p/41d49e23bbdb81839d40cef2848e3a3a) complète les lots [ARCH-002](../ARCH-002/REPORT.md), [FEAT-002](../FEAT-002/SPEC.md) et [UI-001](../UI-001/SPEC.md). Elle précède l’atelier FEAT-003.

La [fiche](../../../templates/registre/site.html) contient les informations métier. La [vue](../../../registre/views.py) conserve les contrôles par site et par client. Le [modèle](../../../raccordement/models.py) porte au plus une liaison par site. Le [service de lecture](../../../raccordement/services.py) sépare le dernier succès de la dernière tentative et tient compte des expirations. Le [transport](../../../raccordement/transport.py) définit les résultats compatibles. La commande de lecture existante utilise déjà ce service.

Observation locale du 19 novembre 2026 par « raccordement etat » uniquement : tennis-ai, confirmation à 10 h 55 min 36 s (Europe/Paris), Wagtail 7.4.4, moteur 1.0.0, contrat 1.0 ; UUID d’instance et alias confirmés présents. L’heure correspond à la dernière confirmation, pas à une sonde du jour. Les fixtures visuelles sont fictives et indépendantes de ces valeurs. L’affichage dans Django sera vérifié au développement.
