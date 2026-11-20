# Existant examiné le 19 novembre 2026

| Source | Conséquence pour le lot |
|---|---|
| [Kanban, carte du sous-lot](https://app.notion.com/p/41d49e23bbdb81e397a7e9419df59f8c) | UI requise et cinq critères de recette. La dépendance déclarée est le socle FEAT-003-01, livré. |
| [Parcours parent](../FEAT-003/SPEC.md) et [maquette parent](../FEAT-003/evidence/maquettes.html) | Partir de la fiche existante et du contexte du brouillon. Le site peut être préparé avant raccordement. |
| [Services centraux](../../../composition/services.py) et [validation](../../../composition/validation.py) | Les lectures et écritures sont déjà bornées au site. Le document V1 connaît les pages et refuse les menus non vides. La lecture des versions et la duplication des occurrences devront évoluer ensemble. |
| [Preuves du socle](../FEAT-003-01/EVIDENCE.md) | Réutiliser son historique immuable et ses vérifications PostgreSQL. Les tests V1 existants serviront à détecter des régressions. |
| [Contrats Studio](../../../docs/ARCHITECTURE-CONTRACTS.md) et [raccordement](../ARCH-002/ARCHITECTURE.md) | La composition appartient au Studio central. Réutiliser la projection de raccordement existante. Aucune sonde ni administration Wagtail dans le parcours de navigation. |

Les seuils de menus, l’utilisation exclusive de HTTPS pour les destinations externes et la résolution explicite des entrées touchées sont des choix de conception proposés pour ce lot. Ils sont détaillés dans le contrat technique. La disponibilité réelle d’une destination externe reste hors mesure.
