# T01 — Décision technique d’organisation frontend

20 novembre 2026 · décision de conception de l’auteur d’audit /root, étayée par /root/t01_frontend. Mandat : comparer les options et arrêter une organisation pour préparer les sous-lots. Ce document n’invente pas d’approbation humaine ni de dépendance déjà installée.

**Retenir JavaScript natif organisé par responsabilités, servi par Django, pour J1 et les gestes UI-004.** Réutiliser le modèle conceptuel de commandes et le pont Wagtail isolé ; remplacer les anciennes interfaces au lieu de les conserver dormantes. Ne pas introduire React/TypeScript dans ce premier incrément.

## Raisons et alternatives

| Option | Coût concret / bénéfice | Décision |
|---|---|---|
| JS modulaire natif | Modèle, pont, services et tests existent ; extraire ce qui dépend des cartes, séparer geste/rendu/historique/persistance, préserver DOM/focus | Retenue ; changements limités à l’éditeur et contrats qui le nécessitent |
| Îlot React/TypeScript | Ajout compilation JS, dépendances/lockfile, livraison bundles, migration des états et événements, pont impératif iframe et tests associés ; ne résout pas seul le rendu partagé | Non retenue pour J1, bénéfice supplémentaire non démontré ici |
| Réécriture frontend générale | Toucherait registre, accès, catalogue et autres écrans sans résoudre directement le contrat du geste | Hors besoin |

Cinq scripts actuels séparent déjà modèle, projection, coque, frame et dépôt (1 375 lignes observées). Le package frontend compile seulement Tailwind. Le problème prioritaire est le rendu local de cartes distinct du rendu moteur, la granularité des gestes et leur sauvegarde ; le choix d’un framework ne supprime aucune de ces obligations.

## Périmètre et coût de migration retenus

Conserver Django/templates et design system des autres espaces. Réemployer côté backend validation, UUID, droits, catalogue, révisions et reçu idempotent. Extraire les parties du modèle de gestes qui restent utilisées ; éliminer leur dépendance aux sélecteurs .be-* de l’ancienne projection. Réutiliser identité/nonce/MessageChannel/CSP et adapter chargements, URLs et tests si les modules sont déplacés. Examiner aussi les mécanismes pointeur V1 de canvas.js (resize, translation libre, capture/annulation) : ils existent déjà mais dépendent de cv-stage et d’un formulaire HTTP. Extraire ce qui reste utile puis supprimer l’ancien écran et son transport ; ne pas réinventer ces acquis ni les déclarer compatibles avec le pont sans qualification.

Coûts réels : état de geste provisoire, groupement cible/voisins, conservation de saisie/focus, raccordement d’un rendu immédiat fidèle, cycle d’acquittement sans reload et continuité undo. Ces travaux restent à T02–T09 ; aucune estimation de jours ni engagement de performance n’est inventé.

## Frontière Wagtail et contrats à fixer

Le moteur garde rendu et contenus avancés. T02 définit flux/grille/libre borné, parent/enfant, formats/ordre et geste atomique. Le pont actuel permet sélection/mesures/dépôt mais ne mute pas le document de travail. T03 qualifie une extension bornée sur rendu moteur ou une projection partageant effectivement ses règles ; contexte de travail, générations de mesures et reçu enregistré sont distincts.

Le choix de l’organisation frontend est arrêté par cet audit ; le choix précis du protocole de rendu et de disposition appartient aux sous-lots propriétaires. Réexaminer le framework seulement si T03 démontre un problème de synchronisation, focus ou testabilité que cette séparation ne permet pas de maîtriser, en chiffrant alors le coût de migration.

[React — intégration dans un projet existant](https://react.dev/learn/add-react-to-an-existing-project), consulté le 20 novembre 2026 : une adoption partielle est possible. Ce fait documenté rend l’option réversible ; il n’apporte pas à lui seul une raison de l’adopter.
