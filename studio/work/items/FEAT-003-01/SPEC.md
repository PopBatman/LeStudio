# FEAT-003-01 — Socle de composition et brouillons

L’opérateur habilité doit pouvoir préparer une composition dans Studio, la retrouver après rechargement et conserver une version cohérente lorsqu’un collègue travaille sur le même site. Ce premier sous-lot livre ultérieurement le service Django de persistance consommé par les éditeurs. Il ne modifie pas la fiche Site. Les [maquettes du parent](../FEAT-003/VISUAL-REVIEW.md) illustrent l’usage prévu au sous-lot 04.

## Règles fonctionnelles

- Un site existant commence sans brouillon. Un accès en lecture renvoie cet état ou la tête courante. Seule une création explicite par un gestionnaire produit une première révision.
- Chaque révision identifie le site, le document de composition et son auteur au moment de l’écriture. Un enregistrement valide ajoute une révision reliée à sa précédente. Une relecture ciblée conserve les identités de pages, sections et composants, ainsi que les valeurs responsive.
- Le parcours vierge, le template et la proposition Figma acceptée alimentent la même structure. L’origine est une métadonnée de confiance établie par le service appelant. En 01, qualifier les trois origines avec des entrées de test contrôlées. La sélection de modèles, l’analyse Figma et les éditeurs interactifs arrivent dans leurs propres lots.
- Le lecteur du site peut consulter la tête ou une révision accessible. Le gestionnaire du site peut également créer et enregistrer. Les mandats Client et Site sont distincts. La révocation d’accès s’applique à la prochaine opération.
- Le brouillon peut exister avant le raccordement du moteur. L’heure du dernier succès, la tentative, la version Wagtail et le diagnostic appartiennent à ARCH-002/ARCH-002-01. La composition active et la précédente appliquée restent inconnues en l’absence d’une attestation d’application ; deux révisions locales successives ne l’établissent pas.
- La préparation est locale au Studio central. Aperçu de la révision sélectionnée, application, retour arrière et édition de contenu Wagtail relèvent d’autres lots. Aucun nouveau point d’entrée HTTP ou écran dans cette tranche.

## Acceptation du développement

| Critère de la carte | Preuve attendue |
|---|---|
| AC1 · Créer, relire, enregistrer | Site sans moteur et site raccordé. Après création puis modification, relire avec une nouvelle connexion à la base. La tête et son parent correspondent aux deux contenus. Fiche du site, voisin, liaison et version appliquée demeurent intacts. |
| AC2 · Trois origines et deux consommateurs | Injecter trois documents valides via les adaptateurs fictifs et le même service. Pour chaque révision, deux consommateurs indépendants retrouvent le même contenu, dans le même ordre, avec les mêmes identifiants. |
| AC3 · Portée du site | Lecture et gestion réussissent selon le mandat. Tester lecteur en écriture, mandat Client seul, révocation, lecture directe d’une révision B via A et référence étrangère dans un bloc de A. Réponse sans information sur B. |
| AC4 · Validation et concurrence | Tester le document invalide, les valeurs limites, deux créations simultanées et deux sauvegardes d’une même tête. Un seul succès dans chaque course. Une erreur intermédiaire laisse le compte de révisions et la tête inchangés. |
| AC5 · Identités, versions et frontière Wagtail | Comparer identifiants stables après déplacement ou renommage, provenance initiale conservée, schéma ancien/inconnu traité explicitement. Espionner le connecteur, le chargement de profil et les écritures vers le moteur : aucun appel pour lire ou enregistrer un brouillon. |

[Contrat de composition](COMPOSITION.md) · [Persistance et services](ARCHITECTURE.md) · [Habilitations](SECURITY.md) · [Plan de réalisation](TASKLIST.md)
