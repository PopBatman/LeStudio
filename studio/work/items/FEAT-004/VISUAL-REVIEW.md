# Revue visuelle du cadrage

Depuis la fiche Site, l’opérateur choisit **Préparer R12** pour examiner l’accueil de l’Imprimerie des Saules. La maquette emploie des données fictives et la police DM Sans du Studio. Le cadre vert regroupe les commandes de l’opérateur. Le papier ivoire représente la page du site. [Ouvrir la maquette interactive](evidence/maquettes.html)

| Situation | Interaction et résultat attendus |
|---|---|
| Préparation | La révision enregistrée figure sur le bouton. Le message de progression annonce la vérification. L’opérateur peut annuler ou retourner à la fiche. Un scénario distinct explique le sort du formulaire modifié. |
| Lecture de R12 | La page, le site, la révision, l’instance, les composants, le contenu éditorial et les médias accompagnent le rendu. L’opérateur choisit le format de lecture en conservant la révision. [Bureau](evidence/apercu-bureau.png) · [Tablette](evidence/apercu-tablette.png) · [Mobile](evidence/apercu-mobile.png) |
| Comparaison | Le sélecteur alterne entre R12 et R11. Le titre du brouillon change. L’article public référencé conserve sa révision 35 dans les deux vues. La référence active est affichée comme inconnue. |
| Nouvelle sauvegarde | Un avertissement indique R13 et conserve l’identification de l’ancien aperçu. **Préparer R13** ouvre la nouvelle révision. [État périmé sur mobile](evidence/revision-perimee-mobile.png) |
| Échec et sortie | Après coupure, le cadre disparaît et **Réessayer** relance la préparation. Après dix minutes, l’aperçu expiré demande une nouvelle préparation. Un refus masque le nom du site et propose **Retour à Mes sites**. Une version introuvable ou un moteur incompatible permet de revenir à la fiche du site autorisé. [Connexion perdue](evidence/connexion-perdue-mobile.png) |

Chromium a parcouru la maquette aux largeurs de 1 280, 768 et 320 px. Le lien de saut et la préparation ont été activés au clavier. La comparaison a affiché R11 avec la révision éditoriale correspondante. Les sept états alternatifs ont tenu sans débordement horizontal. **Préparer R13** et le retour à la fiche ont abouti à chaque taille. Le navigateur a relevé zéro erreur JavaScript et zéro requête HTTP. [Compte rendu des essais](evidence/examen-maquettes.json)

Pour la recette du produit, refaire ces parcours contre deux sites de test raccordés, capturer le véritable rendu moteur et son reçu, vérifier son isolement, sa durée effective, les annonces au lecteur d’écran et le retour au point d’origine dans l’atelier. Les captures jointes documentent uniquement la proposition d’interface. L’appréciation visuelle par l’opérateur reste ouverte.

## Recette de réalisation

Chromium a ouvert la fiche Site, préparé R3 au clavier et lu l’article de l’instance Wagtail A. Les cinq UUID de blocs, l’image décodée et la police embarquée ont été vérifiés sur le même reçu dans les trois formats. Les captures ci-dessous proviennent du moteur. La comparaison a ouvert R2, une seconde session a obtenu un refus et une interruption de connexion a masqué la page. Après rétablissement, la préparation a réussi. [Bureau](evidence/wagtail-bureau.png) · [Tablette](evidence/wagtail-tablette.png) · [Mobile](evidence/wagtail-mobile.png) · [Parcours dans Studio](evidence/studio-mobile.png) · [Relevé navigateur](evidence/navigateur.json)
