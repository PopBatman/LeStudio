# ARCH-002-01 — Visualiser le raccordement Wagtail dans la fiche Site

Depuis « Mes sites », l’opérateur ouvre une fiche autorisée. Après les informations du site, la section « Moteur Wagtail » présente la dernière observation enregistrée. L’opérateur doit pouvoir répondre à deux questions distinctes : quand la liaison a-t-elle été confirmée et que s’est-il passé à la dernière tentative ? Une confirmation datée ne renseigne pas sur la disponibilité actuelle du site.

## Données présentées

Le résumé reste visible sans déplier les détails. Le badge décrit la dernière tentative. Une ligne distincte conserve la dernière confirmation réussie, même si une tentative ultérieure échoue ou est en cours. Présenter l’heure locale avec fuseau explicite (Europe/Paris pour la fiche française) et une valeur machine ISO 8601. Une tentative achevée porte sa date de fin, une tentative encore ouverte sa date de début. Une tentative expirée sans fin enregistrée conserve son heure de début. Une information historique manquante se lit « Non renseigné » ou « Aucune confirmation enregistrée ».

| Résultat central | Présentation attendue |
|---|---|
| unlinked, sans tentative | Non raccordé. Aucune vérification enregistrée. |
| connected avec confirmation | Raccordement confirmé. Afficher l’horodatage du succès et celui de la dernière tentative. |
| checking | Vérification en cours. Conserver le succès antérieur s’il existe. |
| attempt_expired | Dernière vérification expirée. |
| incompatible | Dernière vérification en échec, version incompatible. |
| identity, identity_mismatch, association_conflict | Dernière vérification en échec, identité ou association non conforme. |
| Autre diagnostic d’échec connu | Dernière vérification en échec. Motif compréhensible issu du dictionnaire local. |
| Valeur inconnue ou succès sans confirmation datée | Résultat indéterminé. Conserver les seules informations attestées. |

Le nom de la fiche vient du registre. Les détails présentent les versions disponibles de Wagtail, du moteur et du contrat (majeure.mineure). Pour le gestionnaire, ajouter les UUID du site et de l’instance confirmée, l’alias confirmé et le diagnostic assaini. Afficher « Aucune confirmation enregistrée » en l’absence de succès. Les détails utilisent une divulgation native activable au clavier. Les responsables peuvent conserver l’action FEAT-002 « Modifier le site » sur la fiche.

## Critères de recette du produit à développer

1. Une fiche sans ligne SiteConnection affiche le vide, y compris si son domaine est absent.
2. Sur une fiche confirmée, comparer les valeurs affichées avec la lecture autorisée de la même liaison. Vérifier tennis-ai sur le poste et une autre liaison fictive en tests pour détecter les constantes.
3. Après échec, expiration ou nouvelle tentative, le succès antérieur reste daté et distinct du résultat le plus récent. Sans succès antérieur, aucune instance confirmée n’est annoncée.
4. Version et identités proviennent des champs existants. Tester une ancienne ligne dont les versions sont partielles et un diagnostic inconnu.
5. Le domaine FEAT-002 est du texte. Aucun lien d’administration, d’API interne ou de site public n’est proposé sur la seule base d’un alias ou d’un domaine. Une future destination navigateur devra être explicitement configurée, validée et autorisée.
6. Tester les données autorisées dans le contexte, le HTML et les erreurs. Aucun secret, chemin local, journal brut ni détail trans-site.
7. Vérifier lecture, gestion, absence de mandat, mandat client seul, révocation et accès direct à une autre fiche. Voir la matrice de sécurité.
8. Un GET ou HEAD de fiche ne déclenche ni sonde réseau, ni lecture de profil, ni écriture de liaison. Plusieurs consultations rendent la même observation tant que les données ou l’expiration ne changent pas.
9. Bureau et mobile, ouverture et fermeture des détails au clavier, focus visible, libellés textuels et absence de débordement. Qualifier la future page Django avec captures fictives et revue indépendante.

Sources : [carte Notion](https://app.notion.com/p/41d49e23bbdb81839d40cef2848e3a3a), [plan](TASKLIST.md), [contrat technique](ARCHITECTURE.md), [permissions](SECURITY.md), [examen des maquettes](VISUAL-REVIEW.md).
