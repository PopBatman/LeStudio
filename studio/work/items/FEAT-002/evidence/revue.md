# Relecture du cadrage

Le 18 novembre 2026, l’agent indépendant `/root/revue_cadrage002` a comparé la carte Notion, les propositions de droits, les règles d’archive, la spécification et les parcours illustrés.

**Écart corrigé.** Le premier formulaire de modification du site présentait le client et renvoyait à sa fiche. Il convenait à l’opérateur disposant aussi d’un mandat client, mais exposait ce client au gestionnaire habilité au seul site. La variante dédiée conserve l’opérateur sur Mes sites, la fiche du site, son formulaire et sa confirmation. L’annulation et le succès respectent cette portée. Le critère AC5 couvre aussi ce parcours.

Le réviseur a examiné ces quatre vues et leurs liens après correction. **Avis favorable au cadrage documentaire.** La revue d’une future implémentation et l’exercice effectif des droits sur données fictives restent dans le plan de réalisation. [Maquette relue](maquettes.html) · [Contrôle visuel du support](examen-maquettes.json)

## Revue de la réalisation

L’agent indépendant `/root/registre_revue` a examiné le code, les mandats, la concurrence, le comportement HTTP et les captures du parcours réel. Deux constats ont conduit à valider les critères de recherche avant l’interrogation PostgreSQL et à rejeter les caractères NUL dans les services avant l’écriture. Le réviseur a contre-vérifié les corrections, dont la conservation de la version de la fiche après refus.

Il a examiné quatre écrans sur trois largeurs (320, 390 et 1440 px), avec un mandat limité au seul site et un libellé de 160 caractères. Aucun nom de client confidentiel n’apparaissait dans ces rendus. Il a également relu le résultat du test concurrent PostgreSQL et les deux captures Chromium du parcours. **Verdict favorable** dans le périmètre local sur données fictives.
