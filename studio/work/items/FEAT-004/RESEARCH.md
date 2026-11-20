# Existant examiné le 20 novembre 2026

| Source | Conséquence pour FEAT-004 |
|---|---|
| ARCH-002 et engine/cmengine/urls.py | Les quatre diagnostics acceptent GET. Le rendu technique sert la live_revision d’une ReferencePage sur la paire site/instance. Cette réponse sert de témoin de raccordement. |
| engine/reference/editorial.py et raccordement/transport.py | La capacité editorial.published.v1 identifie un ArticlePage public dans l’arbre du site propriétaire. Son résultat fournit le numéro publié. Le rendu doit reconfirmer la visibilité et la révision lorsqu’il utilise l’article. |
| composition/models.py, validation.py et appearance_contract.py | CompositionRevision est immuable et chaînée. Les versions 1 à 4 sont lisibles par le validateur existant. Catalogue, portée du site et versions exactes contraignent le moteur. SiteMedia.active peut changer après la préparation. |
| composition/placement.py | Les formats base, tablet et mobile combinent règles de conteneur et placement par bloc. La fidélité se vérifie sur une même révision et avec les valeurs effectives de chaque format. |
| Wagtail 7.4, PreviewableMixin.serve_preview et Revision.as_object | Le premier point d’extension restitue un objet en contexte de prévisualisation. Le second reconstitue un objet de révision. La composition Studio demande en plus un adaptateur moteur, des gabarits de composants et un contrôle de portée. |
| Carte FEAT-004 et vision du 19 novembre | Le builder consommera le rendu. Le catalogue exécutable est interne. La preuve attendue au développement est une capture du moteur associée aux versions effectivement utilisées. |

[Documentation Wagtail sur les modèles et la prévisualisation](https://docs.wagtail.org/en/v7.4/reference/models.html) · [Direction produit Visual Builder V2](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539) · [Feuille de route](https://app.notion.com/p/41c49e23bbdb810d9b63c90efd1aeff6).
