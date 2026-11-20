# Rapprochement de Notion et du dépôt

La [carte 03](https://app.notion.com/p/41d49e23bbdb81d69beec505505929a3) rattache le lot au socle 01 et requiert une UI. Le [plan parent](../FEAT-003/TASKLIST.md) permet de cadrer 03 dès la livraison du socle. Les pages et les menus de 02 sont également livrés et constituent un cas de compatibilité à protéger.

| Existant examiné | Conséquence de conception |
|---|---|
| [Validateur](../../../composition/validation.py) | Les schémas 1 et 2 admettent déjà des références de définition avec portée, clé et version. Titre, texte et conteneur ont des règles propres. Le thème accepte accent et espacement. Les feuilles personnalisées s’appuient sur des résolveurs de définitions et de ressources. |
| [Services du brouillon](../../../composition/services.py) et [navigation spécialisée](../../../composition/navigation.py) | Une commande de navigation prépare aujourd’hui un candidat V2. L’introduction de V3 doit conserver la version et les réglages d’une tête V3 lors d’un changement de page ou de menu. Vérifier également le bilan de modification des chemins et le remappage à la copie. |
| [Contrat du socle](../FEAT-003-01/COMPOSITION.md) et [preuves du lot 02](../FEAT-003-02/EVIDENCE.md) | Réutiliser l’identité des occurrences et les révisions locales, le droit de lecture/gestion par site et les limites du document. Les feuilles personnalisées inchangées d’une révision passée disposent déjà d’un traitement particulier dans les commandes de navigation. |
| [Contrat Studio](../../../docs/ARCHITECTURE-CONTRACTS.md) et [raccordement](../ARCH-002/ARCHITECTURE.md) | Les primitives de l’interface opérateur et les définitions destinées aux sites remplissent des fonctions distinctes. Le catalogue, le diagnostic et la revue relèvent du Studio central. Une version du moteur observée au raccordement ne prouve pas qu’une composition y est appliquée. |

Les données des maquettes et de la fixture sont fictives. Cette étude porte sur la version du projet disponible le 19 novembre 2026.
