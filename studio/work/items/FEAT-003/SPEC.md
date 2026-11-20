# FEAT-003 — Atelier du site

## Premier parcours proposé

Depuis « Mes sites », l’opérateur ouvre la fiche du site courant. La nouvelle entrée « Atelier du site » montre si un brouillon existe et, le cas échéant, sa révision et son dernier enregistrement. La fiche conserve les informations du registre et le panneau « Moteur Wagtail » de ARCH-002-01. Un site peut être préparé avant son raccordement. Une confirmation technique n’atteste ni la disponibilité actuelle ni la version de composition appliquée.

| Situation | Ce que voit et peut faire l’opérateur |
|---|---|
| Gestion, aucun brouillon | Action de création. Choisir un template personnalisable ou une page vierge. L’entrée Figma indique sa disponibilité réelle ; choix opérable lorsqu’une proposition autorisée peut être examinée. |
| Gestion, brouillon existant | Reprendre le brouillon du site. Enregistrer modifie sa révision locale. Une erreur garde la saisie ; un conflit donne le choix de relire et de rapprocher les changements. |
| Lecture | Consulter la révision disponible ou l’état vide. Les opérations d’écriture sont contrôlées côté serveur. |
| Accès direct à un autre site | Appliquer les refus FEAT-002, y compris pour un identifiant de composant, ressource ou brouillon imbriqué. |
| Raccordement vide, expiré ou en échec | Garder la dernière confirmation connue et la tentative séparées. Le statut du brouillon dépend de son propre historique. |
| Composition active/précédente sans source confirmée | Indiquer l’indisponibilité du renseignement. La version Wagtail et le digest d’image sont des informations techniques sur le moteur. |

## Comportements et critères transversaux

1. Créer un brouillon dans un site A, le modifier, recharger et le retrouver sous la même identité. Ouvrir un site B et vérifier l’isolation. Départ template, vierge et import accepté produisent un document de même schéma. Le premier incrément livre le socle 01 ; l’entrée opérable sur la fiche dépend aussi de 04.
2. Deux opérateurs ouvrant la même révision peuvent relire le dernier succès. Une sauvegarde devenue obsolète reçoit un conflit et conserve la saisie. Une structure invalide est rejetée intégralement. L’enregistrement se limite au brouillon local.
3. Une page possède une identité stable et une position dans la hiérarchie. Les menus ordonnés sont indépendants, avec sous-menus, destinations internes ou externes et visibilité selon la largeur. Renommer, déplacer ou supprimer une page signale les destinations affectées.
4. Les composants versionnés sont globaux ou propres au site. La révision référence une version et des paramètres validés. L’apparence porte couleurs, typographies, espacements, médias et variantes. Les composants sur mesure sont livrés par l’équipe ; la promotion vers le catalogue global demande revue et retrait des données propriétaires.
5. Éditeur structuré et canvas lisent et écrivent le même document. Sélection, déplacement, ordre, taille et propriétés disposent d’une alternative clavier. Tester grille, flux, conteneur et superposition avec adaptations distinctes bureau/tablette/mobile, débordement signalé et valeur de repli explicite.
6. Titres, textes courts, images, boutons et liens sont éditables en brouillon dans Studio. Les contenus avancés restent sous la responsabilité éditoriale de Wagtail. Une référence distante périmée, inconnue ou inaccessible doit être identifiable ; l’opérateur ne reçoit jamais de promesse de synchronisation que le connecteur ne peut pas tenir.
7. Le graphiste dispose d’une invitation temporaire et révocable, limitée à un site, pour déposer un lien Figma, un commentaire et de nouvelles versions. Une seule déclinaison suffit. L’opérateur autorisé retrouve chaque soumission datée et son signalement dans Studio.
8. L’import présente provenance, frames, styles, composants et correspondances disponibles. L’opérateur accepte ou rejette avant insertion. Les éléments non reconnus et les déclinaisons manquantes restent visibles pour traitement manuel. Couvrir fichier privé inaccessible, permission retirée et limitation de requêtes.
9. La fiche réutilise le contrat de lecture central et ses droits. GET de fiche ou d’atelier sans sonde ni écriture ; toute mutation explicite reste locale. Les liens navigateur proviennent d’une destination autorisée et configurée. L’adresse d’administration locale de tennis-ai relève de l’exploitation du poste.
10. Les parcours sont vérifiés avec jeux de données fictifs, droits lecture/gestion, bureau et petit écran, focus visible, contrôles clavier et retour d’erreur. La qualification du canvas et du portail s’effectue dans leurs propres sous-lots.

## Frontières de livraison

FEAT-004 porte l’aperçu et FEAT-005 l’application, l’historique opérationnel et la restauration. Les opérations de FEAT-003 ne les déclenchent pas. L’accès Studio et Wagtail est réservé à l’équipe habilitée. Le portail de dépôt constitue une entrée distincte pour les graphistes. Les maquettes de la fiche demandées ici sont des propositions examinables avant le développement. [Architecture](ARCHITECTURE.md) · [Permissions](SECURITY.md) · [Maquettes](VISUAL-REVIEW.md) · [Plan par sous-lot](TASKLIST.md)

## Contrats des éléments de la fiche

| Élément | Données et comportement |
|---|---|
| Entrée Atelier | Nom du site, capacité de lecture/gestion et métadonnées minimales de la tête du brouillon (identité, révision, date si connue). GET reste consultatif. L’action de création ou de reprise est nommée selon l’état et le rôle. |
| Carte du raccordement | Réutiliser le contexte connection produit par la vue existante, sa divulgation native et sa projection par rôle. Une absence d’information apparaît comme telle. |
| Choix du point de départ | Trois options identifiables au clavier. Le modèle et la page vierge sont proposés au premier parcours d’édition. Figma reste informatif jusqu’à la disponibilité d’une proposition autorisée. Annuler revient à la fiche sans persistance implicite. |
| Enregistrement | Libellé explicite, révision de base et état en attente pendant soumission. Réussite : confirmer la nouvelle révision. Erreur de saisie : identifier le champ et conserver les valeurs. Conflit : conserver les modifications locales et proposer de relire la version centrale. |
| Consultation | Sections nommées, historique lisible au clavier et à petite largeur, libellés de statut indépendants de la couleur. Aucun lien d’administration généré depuis le profil moteur. |
