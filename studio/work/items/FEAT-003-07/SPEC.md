# Portail graphiste de dépôt Figma

Un gestionnaire de site confie un lien d’invitation temporaire à un graphiste. Celui-ci peut remettre la première version de sa maquette puis en déposer d’autres. L’équipe retrouve les versions dans la fiche du site, même si celui-ci n’a encore ni brouillon ni instance Wagtail. Le dépôt enregistre une référence de conception. L’analyse et la proposition de correspondance appartiennent à FEAT-003-08. [Carte du lot](https://app.notion.com/p/41d49e23bbdb8121912bd62c7f557c09) · [Direction produit](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539)

## Parcours et droits

| Personne | Entrée | Résultat observable |
|---|---|---|
| Opérateur habilité en gestion sur A | Mes sites → fiche A → Dépôts Figma | Crée une invitation et voit son échéance. Le lien complet est révélé à la création pour transmission manuelle. Il peut révoquer une invitation et en créer une nouvelle en cas de perte. |
| Graphiste muni du lien | Portail dédié, sans compte | Voit le formulaire de remise. Un lien de maquette et un commentaire facultatif suffisent. Une seule déclinaison est acceptée, y compris sur un fichier privé. Obtient un reçu avec numéro de version et date. |
| Opérateur habilité en lecture ou gestion sur A | Dépôts de la fiche A | Voit le signalement interne et l’historique paginé du site. Peut identifier invitation, numéro et date d’une version et consulter son commentaire. Le mandat de lecture donne accès aux dépôts, la gestion permet également de créer ou révoquer une invitation. |
| Personne sans mandat sur A | Fiche, historique ou signalement | Aucune donnée de A accessible. Le lien invité ouvre uniquement le dépôt qu’il autorise. Les droits externes ne se transforment jamais en session opérateur. |

Le graphiste peut soumettre une deuxième version du même fichier ou d’un autre fichier avec la même invitation active. Une nouvelle remise intentionnelle donne une nouvelle version, même si le lien est identique. Une répétition technique du même envoi rend le premier reçu. Le signalement est visible dans Studio aux opérateurs qui disposent encore de l’accès au site. Sur la fiche Site, avant l’ouverture de l’historique, afficher « Dernier dépôt Figma » avec version et date de la dernière remise encore conservée. Le signal est dérivé du dépôt validé, reste visible après lecture et s’actualise dès la remise suivante. Quand il ne reste aucun dépôt consultable, la fiche revient à son état vide. Les commentaires sont du texte brut. Aucune image de couverture, identité Figma ou liste de clients n’est nécessaire au reçu.

## Règles du dépôt

- Le serveur détermine le site depuis l’invitation à chaque remise. Au moment de l’écriture, il contrôle sa validité, son expiration, sa révocation et le site destinataire. Le registre conserve les habilitations du site après archivage administratif du client. Une invitation existante reste soumise à sa propre échéance et à sa révocation explicite. Un accusé de réception signifie que le dépôt est enregistré.
- Un lien désigne un fichier de design Figma, éventuellement une sélection dans celui-ci. La validation est locale. Une erreur de syntaxe conserve la saisie et indique le champ à corriger. Un lien privé bien formé peut être reçu même si l’équipe devra demander l’accès pour l’analyser plus tard.
- Une invitation expirée, révoquée ou inconnue aboutit au même écran public d’indisponibilité. Une limite de fréquence atteinte indique quand réessayer. Une révocation intervenue pendant la saisie s’applique à la confirmation.
- Les versions sont numérotées dans l’ordre des dépôts pour chaque invitation. Le numéro décrit une remise au Studio. FEAT-003-08 devra dater sa propre lecture du fichier Figma, dont le contenu peut évoluer après le dépôt.
- Le lot concerne la remise et son suivi. L’ouverture d’un compte externe, l’envoi de courriels, le téléversement de fichiers, les appels à Figma et la création d’un brouillon de composition relèvent d’autres décisions. Aucune action de ce parcours ne publie le site.

## Recette à réaliser après développement

| Critère Notion | Essai et résultat attendus |
|---|---|
| Dépôt limité au site, sans compte | Sur A et B, créer deux invitations. Déposer pour A depuis un navigateur sans session. Vérifier un reçu, un dépôt sur A, les comptes et le nombre de révisions Studio/Wagtail inchangés. |
| Refus et confidentialité | Comparer les états publics à échéance exacte, après révocation et avec un lien inconnu. Une saisie déjà ouverte ne peut plus être confirmée. Aucun autre site, client, lien privé ou opérateur dans la réponse. |
| Plusieurs versions et accès par site | Déposer deux versions sur A, dont une reprenant le même fichier. Vérifier l’ordre, la provenance, les commentaires, la pagination et le rejet d’accès croisé. Rejouer le même envoi puis deux envois distincts concurrents sur PostgreSQL. |
| Une seule déclinaison | Déposer une seule URL avec ou sans sélection Figma, commentaire vide. Obtenir le reçu sans champ desktop/mobile obligatoire. Ni appel fournisseur, ni génération de composant. |
| Information opérateur | Deux opérateurs de A retrouvent le signalement correspondant au dépôt. B et un opérateur dont le mandat a été retiré ne peuvent le lire. Un échec d’écriture annule dépôt et signalement. Vérifier les journaux avec données synthétiques. |

Pour les parcours de refus, d’édition et de remise, tester clavier seul, focus et annonces, petit écran et actualisation du reçu. Les contrôles de cadrage portent sur la maquette. Les essais serveur, PostgreSQL, collecte de journaux et isolation sur deux sites seront exécutés sur la future application. [Plan](TASKLIST.md) · [Architecture](ARCHITECTURE.md) · [Protection des données](SECURITY.md)
