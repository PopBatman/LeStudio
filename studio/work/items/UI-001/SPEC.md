# UI-001 — Fondations de l’interface Studio
L’opérateur et le développeur consultent une galerie locale de composants sur /ui/. Ils parcourent le sommaire, examinent les fondations et essaient les contrôles avec des données fictives. [Carte de cadrage](https://app.notion.com/p/41c49e23bbdb813aa05cdf184fdfd4fb).

| Élément | Contrat attendu |
|---|---|
| Navigation, liens | Libellé et destination locale, lien actif identifiable, saut au contenu. Ancres utilisables au clavier. |
| Boutons | Texte, type et variantes primaire, secondaire et indisponible. Un bouton déclenche une action, un lien mène à une destination. |
| Champ | Identifiant unique, label visible, valeur, aide et erreur reliées au contrôle. Succès et refus démontrables sans persistance. |
| Alertes et badges | Texte explicite et variante sémantique. La couleur complète le message. |
| Tableau et état vide | En-têtes, données de démonstration, libellé long et alternative en l’absence de résultats. |
| Fondations | Typographie, palette, contrastes et largeurs documentés. Les styles communs et les exemples métier sont séparés. |

Critères de fin : composants réutilisés dans la galerie, références de conception antérieures au code, rendu vérifié sur Chromium desktop et mobile, parcours clavier et focus, captures reliées aux sources, tests de la route locale, revue indépendante. Les exemples restent en mémoire dans la page. L’accès opérateur et les sites clients appartiennent aux lots suivants.
