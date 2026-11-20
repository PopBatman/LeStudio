# T01 — Référence produit et premier parcours

Version 1 · 20 novembre 2026. Direction d’interaction adoptée dans la [vision Notion](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539). La pièce jointe fluide reste la référence de gestes ; sa grille/délai ne sont pas des décisions du modèle final.

## Page de comparaison et scénario J1

| Repère | Valeur observée |
|---|---|
| Site | Tennis AI · 59177d82-095d-4e5b-b095-7b73c220de4b |
| Révision de base de l’audit | R18 · 04fd242a-17a9-464f-8a09-ad18d58be4d4 · schéma 4 |
| Page principale | Accueil · cbf41f07-a35b-4043-81df-98e91c8118a5 |
| Sections | f268f311-3712-4998-921c-2fe5f54675ca et e5b50d4d-bf3d-47f5-8180-bfb1a16fc78f |
| Texte sélectionné et édité localement puis annulé | 884f1547-70f2-4abb-b075-8a3a30cf4020 |
| Autre page pour les dépôts vides | A propos · 145b6d32-3a68-456a-a76b-db47fd1bf07b ; aucune section |
| Composition réellement présente | 2 conteneurs, 2 boutons, 1 texte ; ni titre ni image |
| Média | Aucun disponible pour ce site dans la bibliothèque observée |
| Conservation | Empreinte et UUID de R18 identiques avant/après inspection ; session temporaire supprimée |

Le [support de comparaison](evidence/comparaison-reference.html) présente **le même contenu R18** à gauche (capture de l’éditeur local installé) et à droite (copie de son rendu Wagtail dans une coque cible illustrative). Ce support est une référence d’audit, pas un nouvel éditeur. Les commandes de largeur/texte long ne font aucune requête à Studio.

### Préparation contrôlée du pilote T03

Au lancement T03, relire la tête et retrouver ces pages par UUID. Si elles ont changé, consigner la nouvelle base et adapter la recette sans écraser les changements. Préparer un brouillon sur Accueil, conserver ses composants existants, ajouter un titre et une image de démonstration dans les deux sections. Le catalogue livré fournit la définition heading et image ; la commande technique catalogue.attribuer_media peut attribuer l’asset de démonstration « Étude de formes » au site. Les droits de cet asset sont documentés dans catalogue.py. Cette préparation reste à réaliser en T03 ; aucun média n’est créé ici.

Périmètre minimum T03 : déplacer l’image horizontalement et entre sections, redimensionner la boîte du titre (retour à la ligne, pas taille typographique implicite), modifier son texte, annuler/rétablir un geste complet, autosauvegarder avec acquittement, rouvrir et comparer le rendu Wagtail de la nouvelle révision. Historique et autosave minimaux sont inclus dès T03, avant leur consolidation T08. Aucun effet sur le site actif.

## Contrat UX des gestes

| Geste | État provisoire / commit | Refus, annulation et accès équivalent |
|---|---|---|
| Insérer depuis bibliothèque gauche | Cible et voisins prévisualisés ; au lâcher, occurrence avec UUID nouveau et défauts utiles | Parent/version/média incompatibles expliqués ; Échap/capture perdue ne commitent rien ; bibliothèque puis destination au clavier |
| Déplacer dans une section | Translation X/Y réelle selon modèle, guides et voisins ; un commit de geste | Bornes/superposition explicites ; commande clavier de placement équivalente |
| Transférer entre sections/conteneurs | UUID/contenu/références conservés, conversion du repère et contraintes du parent cible | Descendance/dépôt interdit : source inchangée ; annoncer la destination au clavier |
| Réordonner une section | Poignée, indicateur avant/après et défilement ; enfants conservés | Échap ou cible disparue annule ; alternative clavier accessible |
| Redimensionner | Poignées et alignements contextuels, boîte bornée, ratio image et reflow définis | Texte jamais masqué silencieusement ; valeurs accessibles au clavier ; boîte et police distinguées |
| Éditer sur place | Double-clic, DOM de saisie/caret conservés ; validation et sortie explicites | Sélection de texte ne déclenche aucun drag ; changement de sélection/menu ne perd pas la saisie |
| Régler | Clic droit et bouton Options ; menu court, approfondissement à la demande | Entrée/Espace ouvrent, Échap ferme et rend le focus ; tactile sans dépendre du clic droit |
| Annuler/rétablir | Un geste complet, cible et voisins inclus ; geste provisoire absent de l’historique | Annuler après autosave crée une nouvelle intention, pas suppression d’une révision |
| Sauvegarder | Modifié → en cours → confirmé pour le lot exact ; intentions plus récentes encore modifiées | Clé/requête stables si résultat inconnu ; base périmée : conflit sans écrasement ; révocation : arrêt |
| Formats / navigation | Héritage/surcharge affichés ; structure partagée distincte ; page/sélection/base suivies | Retour héritage explicite, geste/saisie traités avant changement de page ou format |

## États et scénarios de référence

| Cas | Données / largeur | Observation à prouver dans le lot propriétaire |
|---|---|---|
| R1 — Page existante | Accueil R18 et base relue en T03 ; 1200/820/390 et 980 px | Identités, transformation et rendu de même révision, stabilité scroll/resize/police/image |
| R2 — Page/section vide | A propos actuelle, puis conteneur vide de recette | Dépôt depuis bibliothèque, cible clavier et création sans commandes intermédiaires obligatoires |
| R3 — Contenu long | Texte de 115 caractères essayé localement ; titre de deux puis cinq lignes | Reflow, voisins, focus, absence de masquage et dimensions persistées |
| R4 — Dense / imbriqué | Données fictives, cinq types existants, volume à définir dès T03 avec T18 | Limites et fluidité mesurées sur appareil identifié, pas de budget supposé acquis |
| R5 — Erreur / reprise | Requête rejetée/perdue, autre tête, permission retirée, moteur indisponible | État confirmé/non-confirmé identifiable ; reprise conforme à T08/T09 |
| R6 — Trois origines | Vierge/template et Figma réellement qualifié dans FEAT-006 | Même modèle/éditeur ; T19 puis tests sur artefact nettoyé T21 |

Le navigateur de cet audit a réellement vérifié la sélection, le texte long local/undo et les formats mesurés. Le tactile matériel, lecteur d’écran, budgets, gestes futurs et reprise durable ne sont pas déclarés validés. [W3C Pointer Events](https://www.w3.org/TR/pointerevents3/) et [W3C APG Menu Button](https://www.w3.org/WAI/ARIA/apg/patterns/menu-button/), consultés le 20 novembre 2026, guident les contrats d’interruption et de focus ; ils ne remplacent pas leur recette.
