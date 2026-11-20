# FEAT-004 — Rapport de cadrage du 20 novembre 2026

Le lot définit comment ouvrir et comparer un aperçu privé de la composition enregistrée d’un site. La page doit provenir du moteur Wagtail raccordé. Un reçu identifie la révision Studio, l’instance, la page, les composants et les ressources effectivement rendus. Une préparation expirée, une restriction éditoriale et une révision Studio plus récente ont chacune un comportement distinct.

Le [contrat de feature](SPEC.md) fixe huit scénarios de recette. Le [contrat technique](ARCHITECTURE.md) précise les échanges et le futur point de consommation de UI-003. La [sécurité](SECURITY.md) décrit les contrôles à répéter sur chaque lecture, y compris les médias. La [tasklist](TASKLIST.md) ordonne la qualification à deux instances et les preuves d’absence de publication.

L’architecture a été examinée par /root/preview_arch, la proposition d’interface par /root/preview_mock et la revue indépendante par /root/preview_review. Les [pièces de cadrage](EVIDENCE.md) permettent de rejouer les contrôles documentaires et de parcourir la maquette.

Le palier READY porte sur les prérequis documentaires. La construction et la qualification du rendu de bout en bout restent à réaliser. Le sous-lot Figma FEAT-003-08 reste READY et le parent FEAT-003 IMPLEMENTING. La priorité d’exécution du Kanban est conservée.

## Livraison locale et activation sur Tennis AI

Depuis **Mes sites → fiche Site → Aperçu du site**, choisir la page et préparer la révision enregistrée. La comparaison indique les différences de composition. Le reçu précise l’échéance et la provenance du rendu. Les liens entre pages passent par le sélecteur de la coque Studio. Le contrat de rendu et ses UUID de blocs sont disponibles pour UI-003. [Guide opérateur](../../../docs/MOTEUR-WAGTAIL.md#examiner-une-révision-du-site)

Les 190 tests Studio sur PostgreSQL et les neuf tests Wagtail sur PostgreSQL passent. La recette a exercé deux instances isolées, les refus et les trois formats au navigateur. Les accès au HTML et aux médias ont cessé après perte des conditions requises. L’état des contenus publiés et les réponses HTTP publiques ont été comparés avant et après. La revue indépendante de réalisation conclut en faveur de la livraison locale. [Preuves](EVIDENCE.md) · [Revue](REVIEW.md)

L’activation supplémentaire demandée pour Tennis AI a mis à jour le digest de son profil administré après sauvegarde locale privée de la configuration et de la base moteur. Les deux pages de sa révision Studio R16 ont été rendues sur son instance Wagtail. Les 16 révisions centrales, les pointeurs de publication, la réponse publique et l’accès à la connexion de l’administration ont été vérifiés. La lecture éditoriale de nouveaux articles reste soumise à la configuration indépendante de leur racine. Le lot est DONE sur le poste local.
