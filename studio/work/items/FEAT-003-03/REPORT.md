# Rapport de cadrage du 19 novembre 2026

Le sous-lot fournit le contrat des composants et de l’apparence des brouillons, consommé ensuite par l’éditeur structuré et le canvas. La dépendance du Kanban est FEAT-003-01, déjà livré. FEAT-003-02 fournit le scénario de non-régression des pages et menus. Les critères du lot distinguent l’ajout d’une définition dans la bibliothèque, la sélection d’une version par un site et la future application d’un brouillon au moteur.

Le cadrage s’appuie sur la [spécification](SPEC.md), le [contrat technique](ARCHITECTURE.md), la [recette proposée](TASKLIST.md), les [règles d’autorisation](SECURITY.md) et la [maquette examinable](VISUAL-REVIEW.md). Les tests d’intégration Django, de migration et de concurrence appartiennent au mandat de développement.

Les travaux ont été répartis entre /root (spécification, vérifications documentaires et Notion), /root/lib_contract (contrat et exemple), /root/lib_design (maquettes et examen navigateur) et /root/lib_review (revue indépendante du cadrage). [Revue](REVIEW.md) · [Preuves](EVIDENCE.md)

## Réalisation du 19 novembre 2026

La fiche Site ouvre les vues Bibliothèque et Apparence. Cinq types globaux sont livrés. La bibliothèque expose leurs variantes, la portée et la version épinglée. L’opérateur peut régler les valeurs du site et d’une occurrence existante, réinitialiser les surcharges, adopter une autre version, remplacer ou retirer une occurrence. Les références indisponibles donnent un diagnostic. La vue permet également d’instruire la promotion d’une définition locale par deux opérateurs distincts.

Le registre et ses migrations ont été réalisés par /root/catalog_registry, le contrat V3 et les sauvegardes par /root/catalog_v3, les vues et formulaires par /root/catalog_ui. La revue indépendante de /root/catalog_review a porté sur les droits, les versions, la conservation des contenus et les formulaires rendus. Une anomalie du formulaire de changement de version détectée dans Chromium a été corrigée et couverte par un test de régression avant la qualification finale.

Le paquet Docker a passé **104 tests sur PostgreSQL**. Sur SQLite, 98 tests réussissent et six tests réservés à PostgreSQL sont ignorés. La recette Chromium a couvert le passage de V2 à V3, l’isolation de deux sites, le conflit d’édition, la version d’un bouton, la promotion avec revue et la correction d’un média révoqué. La configuration du poste a conservé ses brouillons et son raccordement après migration. [Preuves](EVIDENCE.md) · [Guide opérateur](../../../docs/BROUILLONS.md)

Le catalogue partagé contient les cinq versions standards sur une installation vierge. Les composants sur mesure se livrent par une commande technique pour un rendu présent dans le code. La première ressource attribuable est l’illustration de démonstration livrée avec Studio. L’éditeur général de nouvelles occurrences appartient au lot 04.
