# Rapprochement du 19 novembre 2026

| Source examinée | Incidence sur le lot |
|---|---|
| [Carte Notion 04](https://app.notion.com/p/41d49e23bbdb8168b7f3e3ad6dca78ba) et [découpage parent](../FEAT-003/TASKLIST.md) | Les trois dépendances déclarées, 01, 02 et 03, sont DONE dans le Kanban. 08 est une intégration future. Le type UI de la carte impose maquettes et essais d’accessibilité. Le dossier local conserve l’identifiant FEAT et le marqueur UI du workflow. |
| [Fiche Site](../../../templates/registre/site.html) et [routes livrées](../../../registre/urls.py) | La fiche mène à Pages, Menus, Bibliothèque et Apparence. Ajouter l’entrée générale Atelier et la reprise du brouillon en gardant ces accès spécialisés. |
| [Socle de composition](../../../composition/services.py) | La création distingue déjà blank, template et figma. Les deux dernières origines exigent un résolveur de confiance. L’acceptation du nom d’une origine dans le service ne rend pas son parcours disponible à l’écran. |
| [Navigation](../../../composition/navigation.py) et [contrat V3](../FEAT-003-03/ARCHITECTURE.md) | Réutiliser les pages, les menus, les UUID et les versions de composant épinglées. Le modèle de sections/blocs existe déjà. L’ajout et le déplacement généraux de ces occurrences manquent dans le parcours opérateur actuel. |
| [Apparence](../../../composition/appearance.py) et [formulaires de bibliothèque](../../../composition/catalogue_forms.py) | L’édition, le retrait, la validation typée des propriétés et les diagnostics d’occurrences existent pour les définitions du site. Réutiliser ces règles dans l’inspecteur. |
| [Primitives Cotton](../../../templates/cotton) et [contrats Studio](../../../docs/ARCHITECTURE-CONTRACTS.md) | Réutiliser bouton, champ, lien, badge, alerte et état vide lorsque leur contrat convient. Prévoir les essais réels clavier, lecteur d’écran et petits écrans. |
| [Contrat du raccordement](../ARCH-002/ARCHITECTURE.md) | L’identité du brouillon appartient à Studio. Le parcours fonctionne sur une fiche non raccordée, conserve l’état de connexion existant et ne contacte pas Wagtail pour sauvegarder. |
