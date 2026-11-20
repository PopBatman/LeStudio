# Accès, intégrité et reprise

| Frontière | Contrôle de réalisation |
|---|---|
| Fiche, atelier, lecture de révision | Réutiliser la session opérateur et le mandat de lecture sur le site. Pour un site inaccessible, une révision étrangère ou une occurrence étrangère, masquer les métadonnées de la cible. |
| Création et modification | POST avec CSRF, mandat de gestion vérifié dans le service transactionnel, site de la route et acteur de la session. La création exige une tête absente. Une modification exige le même UUID de tête au moment d’écrire. Une erreur conserve l’historique. |
| Modèle et Figma | Autoriser uniquement des coordonnées de modèle reconnues par le fournisseur local. Copier et revalider les références. Le formulaire ne fournit ni document de confiance, ni artefact Figma arbitraire, ni chemin de gabarit. Aucune requête externe pendant la création locale. |
| Structure et contenu | Valider le parent, la position et le type de destination. Rejeter cycles, nœud inconnu, doublon, limites dépassées, valeur de style libre et média non autorisé. Conserver thème et menus hors de l’opération. Échapper les textes et restituer les erreurs avec des identifiants du site accessible. |
| Retrait et concurrence | Afficher la portée du retrait, revoir la confirmation si la tête a changé. Une référence devenue inaccessible reste diagnostiquée. Un mouvement ne doit pas la rendre utilisable sur une autre page ou un autre site en contournant le validateur. |
| Effets | Aucune écriture au moteur, aucun appel à l’administration Wagtail. Les preuves utilisent des sites fictifs, des ressources attribuées et des opérateurs de test. |

Essais négatifs prévus : mandat retiré entre formulaire et confirmation, double création, révision obsolète face à une modification dans Apparence, UUID inter-site, média révoqué entre sélection et sauvegarde, déplacement dans sa descendance, dépassement des limites d’imbrication et soumission Figma forcée. Pour chaque échec, vérifier la tête, l’absence de révision partielle et le contenu du message.
