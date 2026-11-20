# Rapport de cadrage du 19 novembre 2026

Le dossier traduit les cinq critères de la carte en parcours et en tests de développement. La partie nouvelle porte sur la navigation indépendante dans un brouillon et sur la gestion des impacts d’un changement de chemin ou d’une suppression. Le socle de stockage et les droits par site proviennent de FEAT-003-01 et FEAT-002.

L’exécution du cadrage a été répartie entre /root (parcours, sécurité et plan), /root/nav_contract (contrat V2 et fixture), /root/nav_design (maquettes et vérification navigateur) et /root/nav_review (revue indépendante). Les résultats sont référencés dans [les preuves](EVIDENCE.md) et [la revue](REVIEW.md). La recette de l’application et les tests de migration/concurrence sont planifiés pour le développement. Le mandat actuel porte sur le cadrage.

## Réalisation sur le Studio local

Le mandat de développement du 19 novembre 2026 couvre la réalisation de FEAT-003-02. La fiche Site donne accès à Pages et Menus. Le droit de gestion permet de créer le brouillon vierge, les pages, les menus et leurs entrées. La lecture simple présente le même document et sa révision. Les changements de chemin et les retraits montrent un bilan avant confirmation. Une sauvegarde réussie crée une révision centrale. La lecture et la navigation sont également disponibles pour les sites sans raccordement Wagtail.

Les exécutants /root/nav_impl_domain, /root/nav_impl_services et /root/nav_impl_web ont pris en charge respectivement la validation, les opérations transactionnelles et le parcours Django. Le réviseur /root/navigation_release_review a examiné ces changements et rejoué des scénarios sur une base isolée. Les révisions V1 et les anciens composants personnalisés sont conservés. L’envoi d’un document complet garde les contrôles du service commun. Le format V2 utilise la colonne JSON existante.

La suite du paquet Docker compte 88 tests réussis sous PostgreSQL. Sous SQLite, 83 réussissent et cinq contrôles propres à PostgreSQL sont ignorés. Le parcours Chromium sur PostgreSQL couvre les impacts multi-menus, la sauvegarde, le reciblage, le rechargement, la lecture seule sur mobile et la résolution d’un conflit. [Résultats et captures](EVIDENCE.md) · [Guide opérateur](../../../docs/BROUILLONS.md)
