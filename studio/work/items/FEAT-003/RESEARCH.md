# Existant, sources et décisions à préciser

La [carte parente](https://app.notion.com/p/41c49e23bbdb8170b68adf9f4a546fe4) porte la vision fonctionnelle. Les huit cartes sont des unités de réalisation futures. Le registre sélectionne déjà les sites accessibles, et la [vue de fiche](../../../registre/views.py), sa [projection par rôle](../../../registre/raccordement.py) et son [gabarit](../../../templates/registre/site.html) présentent le résultat du [service central](../../../raccordement/services.py). Le [rapport ARCH-002-01](../ARCH-002-01/REPORT.md) documente les tests d’accès et les captures réelles.

Observation locale du 19 novembre 2026, via la commande existante « raccordement etat » : tennis-ai a une confirmation le 19 novembre à 10 h 55 heure de Paris, Wagtail 7.4.4 et contrat 1.0. La lecture consulte l’enregistrement central. Aucune nouvelle sonde n’est nécessaire pour concevoir la fiche. Aucun modèle existant ne fournit de révision de composition active ou de brouillon d’atelier. Les exemples des maquettes seront fictifs.

## Sources et arbitrages par sous-lot

| Carte | Interface réutilisée | Point à trancher ou qualifier dans le sous-lot |
|---|---|---|
| [01 · Socle](https://app.notion.com/p/41d49e23bbdb81a5aeddfea5f1ef8d56) | Identité Site et mandat, transactions Django/PostgreSQL | Fixer la taille maximale du document et vérifier une migration de schéma avec deux anciennes révisions. |
| [02 · Navigation](https://app.notion.com/p/41d49e23bbdb81e397a7e9419df59f8c) | Identités stables du socle 01 | Fixer les règles de slug et de profondeur ; préciser le message et le choix opérateur pour chaque lien affecté. |
| [03 · Composants](https://app.notion.com/p/41d49e23bbdb81d69beec505505929a3) | Socle 01 et conventions UI-001 pour l’interface opérateur | Proposer comme premier catalogue conteneur, titre, texte, image et bouton. Valider leurs paramètres et le responsable de promotion. |
| [04 · Éditeur structuré](https://app.notion.com/p/41d49e23bbdb8168b7f3e3ad6dca78ba) | Fiche, composants UI, composition, pages et bibliothèque | Confirmer l’ergonomie de reprise/conflit et la sélection du premier template. |
| [05 · Canvas](https://app.notion.com/p/41d49e23bbdb81e386a3ef5f4bf26492) | Commandes et schéma communs avec 04 | Mesurer la réactivité sur une page représentative et fixer seuils, zoom, règles de débordement et repli mobile. |
| [06 · Contenus](https://app.notion.com/p/41d49e23bbdb813fb814de85024ce68d) | Identité moteur ARCH-002 ; brouillon local de 01 et éditeur 04 | Qualifier les droits médias et la provenance d’une référence/révision Wagtail. L’API actuelle ne lit ni révision éditoriale arbitraire ni média privé. |
| [07 · Portail](https://app.notion.com/p/41d49e23bbdb8121912bd62c7f557c09) | Portée Site de FEAT-002, séparation opérateur de FEAT-001 | Fixer durée d’invitation, conservation et effacement convenus, limites de dépôt et procédure de révocation avant données de tiers. |
| [08 · Import](https://app.notion.com/p/41d49e23bbdb81c0b724f655557db7d9) | Soumissions 07, versions de composants 03 et document modifiable 04 | Qualifier sur un fichier autorisé les métadonnées disponibles, les quotas et le consentement avant copie des ressources. |

L’API Figma documente une lecture par clé de fichier, avec version et sélection possible de nœuds. La capacité effective dépend du droit de lecture, du type de compte et des quotas. Une soumission de lien et une autorisation d’API sont deux événements distincts. Cette recherche n’a lu aucun fichier Figma de client. [Lecture des fichiers](https://developers.figma.com/docs/rest-api/file-endpoints/) · [Authentification](https://developers.figma.com/docs/rest-api/authentication/) · [Limites](https://developers.figma.com/docs/rest-api/rate-limits/)
