# T02 — Options de contrat à éprouver

Version 1 · proposition technique de /root ; aucune réalisation ni approbation humaine nouvelle.

## Représentation et compatibilité de départ

L’existant accepte les schémas 1–4 ; version 4 ajoute placement base/tablet/mobile. Layout : stack/grid, columns 1–12, gap 0–128 px. Placement flow : span, largeur optionnelle en pourcentage et hauteur optionnelle en px ; free : x/width en pourcentage du parent, y/height en px et z. Ces unités sont locales au parent, jamais des coordonnées de la fenêtre. L’héritage tablet/mobile part directement de base ; les seuils existants sont 768 et 1024 px. Les largeurs 1200/820/390 sont des références de recette et non des seuils.

La proposition conserve arbre, tableaux, définition épinglée, props typées, apparence et références. Pas de duplication du parent dans un deuxième index persistant ni de géométrie DOM enregistrée en parallèle. Toute nouvelle sémantique exige une version explicite ; le moteur annonce/refuse cette version avant de prétendre rendre.

## Comparer avant de figer le schéma

| Mode | Usage et position réelle | Taille, voisins et limites proposées |
|---|---|---|
| Flux | Ordre dans le parent, largeur et alignement contrôlés ; pas seulement monter/descendre | Hauteur texte intrinsèque ; gap du parent ; voisins repoussés par le flux. Une translation libre X/Y ne doit pas être annoncée si seul l’ordre change |
| Grille responsive | Colonnes configurées par le parent, départ de colonne explicite si nécessaire + span et ordre de lecture | Auto-placement des autres enfants selon ordre ; aucun dense qui change la lecture ; collision gérée dans le groupe. La boîte texte grandit avec son contenu |
| Libre borné, conditionnel | Groupe/parent local avec bornes et règles de superposition explicites | Le libre legacy reste lisible. Nouveau libre seulement si une référence le justifie, calques explicites, hauteur du groupe suffisante, repli par format et ordre de lecture conservé |

Candidat d’extension minimal si la grille est retenue : départ de colonne et alignement de l’occurrence (start/center/end/stretch), hauteur auto ou minimale pour les textes/conteneurs ; pas de pixel absolu global ni de placement CSS arbitraire. Définir noms, types, valeurs et bornes exacts dans DISPOSITION.md après comparaison ; ce tableau n’est pas une API acceptée. Conserver columns 1–12 comme borne technique actuelle est une option, jamais la preuve d’une grille universelle à 12.

Espacement : réutiliser gap validé du parent ; padding ou alignement nouveaux seulement s’ils sont requis par les compositions, sous forme de champs bornés. Une section occupe la largeur disponible et se réordonne ; sa position horizontale libre n’est pas proposée.

## Contenu variable et redimensionnement

Redimensionner un titre change sa boîte et le retour à la ligne ; le niveau de titre et la taille typographique restent des réglages distincts. En flux/grille, hauteur auto/minimale, texte intégral et voisins recalculés. Une réduction de hauteur qui masquerait le texte est refusée ou convertie explicitement en minimum ; ne pas conserver un height fixe avec débordement accidentel comme réponse produit.

Pour une image, choisir explicitement entre ratio intrinsèque avec hauteur automatique et boîte bornée avec ajustement contain/cover si cette capacité est livrée. Défaut proposé : ratio intrinsèque, aucune coupe silencieuse. Remplacement de média : même occurrence, nouveau ref_id autorisé, largeur préservée ; recalcul après chargement, voisins ajustés dans la même intention. Un média absent reste signalé, sans URL distante arbitraire.

En libre, un contenu qui dépasse ne doit ni être masqué ni chevaucher un voisin implicitement : agrandir le groupe et les voisins dans un geste atomique si une solution déterministe existe, sinon refuser la confirmation en proposant le retour au flux. Cette alternative doit être éprouvée ; elle ne devient pas un moteur de résolution générique.

## Dépôt et conversion de repère

Un dépôt valide fournit parent UUID, ancre before (UUID frère ou null), format et intention de position/taille. Le modèle résout l’emplacement ; les mesures DOM ne sont pas des droits. Pour une boîte libre, x = 100 × (gauche cible − gauche de la zone de contenu du parent) / largeur de cette zone ; largeur exprimée dans le même repère, y en px locaux. Définir l’arrondi et vérifier les bornes après arrondi. Recalculer après scroll, chargement image/police ou resize ; annuler une confirmation si la génération de mesures ou la cible est périmée.

Vers flux/grille : convertir vers ordre, départ/span et alignement disponibles, sans conserver des coordonnées inactives trompeuses. Vers libre : matérialiser la boîte complète du parent cible. Parent et ordre sont partagés ; calculer/revalider tous les formats, ne pas rebaser seulement celui qui est visible. Si une conversion n’est pas représentable, refuser le dépôt et garder la source ; aucune conversion silencieuse destructrice. Un changement local de mode doit respecter les règles d’héritage, et leur remise à zéro doit être testée.

## Unité atomique du geste

Candidat de protocole versionné : un groupe identifié contient les opérations bornées de structure, placement, propriétés et voisins d’une seule intention. Le lot de sauvegarde conserve key/base/page et contient des groupes ordonnés. Le schéma exact du transport est décidé avec la compatibilité des consommateurs existants ; ne pas modifier sous le même contrat une liste historique de commandes.

Traitement : contrôler acteur/site/base et structure d’enveloppe → copier l’état précédent → appliquer les opérations du groupe sans publier d’intermédiaire → valider document, permissions/références et collisions de l’ensemble affecté dans tous les formats → accepter une entrée d’historique. Répéter pour chaque groupe ; sauvegarder une seule révision/reçu pour le lot complet, ou rien. Tous les enfants affectés par parent_layout et les descendants transférés sont inclus dans la validation, pas seulement le bloc sélectionné.

Exemple conceptuel : A et B voisins se déplacent ensemble ; A vers la place actuelle de B, B vers une place libre. L’état intermédiaire A/B en collision n’est jamais validé comme un geste ; l’état final sans collision doit passer. Un deuxième groupe indépendamment invalide annule le lot entier. Une superposition voulue exige une intention et un ordre de calques explicites dans chaque format concerné.

Insertion/duplication : conserver le mapping local/canonique existant ; remapper aussi commandes en attente, sélection et historique avant une nouvelle soumission. Rejouer exactement key/payload sur résultat inconnu ; clé réutilisée avec autre contenu refusée. Une permission révoquée est vérifiée avant tout reçu retourné. La concurrence sur base périmée refuse l’écrasement.

## Prévisualisation, annulation et focus

États : repos → geste provisoire → destination valide ou refus expliqué → confirmation locale → modifié → sauvegarde en cours → acquittement de la seule version envoyée. Le rendu de travail et l’aperçu certifié d’une révision restent identifiables. Aucune requête persistante pour chaque mouvement du pointeur.

Escape, pointercancel, capture perdue ou cible retirée annulent la session provisoire et restaurent document, voisins, sélection et focus. Le geste provisoire n’entre pas dans l’historique. Une saisie texte est traitée avant une navigation/page/format ; le clic ou la sélection de texte ne commence pas un drag. Les alternatives clavier aux dépôt/taille/options produisent la même intention.

Undo/redo porte sur la cible et tous les effets induits ; après sauvegarde, undo crée un nouvel état à sauvegarder. Prévoir continuité après acquittement sans recharge, mais sa mise en œuvre UI appartient à T03/T08.

## Lecture et migration

Lire les versions 1–4 sans réécrire leurs révisions. Pour une extension version 5 : copie normalisée déterministe, UUID/ordre/props/définitions/références inchangés sauf champs explicitement migrés ; conserver les hauteurs fixes legacy et leur sens dans l’ancienne version. Convertir une hauteur fixe en minimum requiert un rapport visible et une nouvelle révision, car cela peut modifier le rendu.

Pas de migration automatique des données réelles pendant T02. Tester les fixtures 1–4, un export minimal de R18 et un schéma futur rejeté. Une définition indisponible reste consultable selon le contrat de conservation existant ; elle ne devient ni insérable ni publiable. Si une transformation n’est pas sans perte, garder le document ancien lisible, expliquer la limite et exiger une conversion explicite. Repli : lecteur/image précédente compatible pour l’ancienne version, jamais rétroconversion silencieuse d’une version 5 déjà écrite.

Les trois origines vierge/template/Figma accepté consomment ce même document. Adapter les producteurs sans nouvelle occurrence lors d’une migration ; les instanciations de template ont de nouveaux UUID. Les références Figma non représentables restent des écarts/propositions, pas du HTML/CSS exécutable.

