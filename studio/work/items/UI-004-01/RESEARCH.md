# T01 — Sources, alternatives et limites

Sources relues le 20 novembre 2026 : carte T01, règle de relecture, UI-004, vision, roadmap, T21, FEAT-003-01/03 et FEAT-004. [Instantané](evidence/sources-notion.json). La carte T01 est postérieure au premier instantané du parent : elle exige désormais les consommateurs et l’inventaire pour T21, intégrés ici. Le plan courant reste 21 tâches et 14 sous-lots UI-004.

Sources locales : contrats projet, code et tests de composition/catalogue/preview, frontend et templates, moteur de référence, configuration/build et documentation active. [Audit](AUDIT.md), [inventaire](INVENTAIRE-T21.md) et [manifeste](evidence/manifest-sources.json) séparent constat et proposition. Les anciens rapports fournissent des points de reprise ; leurs chiffres de tests ne deviennent pas les tests présents.

Le navigateur de Studio local et les métadonnées Tennis AI fixent une base R18 réelle, sans titre/image/média disponible. L’hypothèse initiale d’une page déjà prête pour le pilote n’est pas confirmée ; une préparation explicite est requise en T03. La page et sa révision ont conservé leur empreinte durant l’audit.

Les alternatives frontend sont comparées dans [la décision](DECISION-FRONTEND.md). La voie JS native est retenue dans le périmètre technique de cet audit. Le choix du modèle et du rendu de travail n’est pas fabriqué : T02/T03 doivent le spécifier et le démontrer. Construire un renderer supplémentaire divergent augmenterait le risque de faux aperçu ; réemployer les règles et la sécurité du moteur est une contrainte.

Sources primaires consultées le 20 novembre 2026 : [React — intégration dans l’existant](https://react.dev/learn/add-react-to-an-existing-project), [W3C Pointer Events](https://www.w3.org/TR/pointerevents3/), [W3C APG — Menu Button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/). Elles documentent l’adoption progressive, la capture/interruption et le focus/menu ; elles ne démontrent pas les performances ou l’accessibilité du produit.

Les budgets/appareils, la concurrence PostgreSQL, le lecteur d’écran, le matériel tactile et Figma réel restent à qualifier dans leurs lots ; aucun de ces points n’est présenté comme une capacité livrée par T01.
