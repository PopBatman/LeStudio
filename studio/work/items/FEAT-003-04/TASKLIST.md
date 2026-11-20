# Plan de développement

1. Partir des tests d’accès à la fiche Site. Spécifier en TDD le contexte sans brouillon, la reprise de la tête existante et la lecture seule, y compris sur un site non raccordé.
2. Livrer un modèle de départ local versionné et la page vierge. Tester la création unique, l’origine, le renouvellement des identités, la validation V3 et la conservation des révisions V1/V2. Vérifier l’état indisponible de Figma et le refus d’un appel forcé.
3. Couvrir par des tests de service la création de sections et de blocs imbriqués, l’édition des propriétés, le déplacement, le changement d’ordre et la suppression confirmée. Qualifier les limites, les références de site, la conservation des réglages et des menus.
4. Brancher les formulaires de la fiche, de l’arborescence et de l’inspecteur sur ces services. Tester CSRF, habilitation retirée, champ invalide, double soumission et conflit avec un autre panneau.
5. Rejouer les cinq scénarios de la carte sur Django avec PostgreSQL. Réouvrir le brouillon, comparer deux sites et l’historique. Vérifier l’absence d’écriture moteur.
6. Éprouver bureau et téléphone, clavier seul, placement du focus, annonces d’erreur et lecteur d’écran. Conserver captures et écarts observés. Faire relire la réalisation et rapprocher le Kanban. UI-002 suit la qualification transversale d’accessibilité et de direction artistique.
