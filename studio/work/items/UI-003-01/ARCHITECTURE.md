# Contrat de présentation et de données
Le prototype est un document HTML autonome. Les boutons manipulent des données fictives dans le navigateur. L’interface cible se compose de la fiche d’entrée, d’une barre d’atelier, d’un explorateur, de la page sélectionnée, de l’inspecteur et d’une vue d’aperçu.

| Donnée | Rôle dans la cible | Invariant à préserver |
| --- | --- | --- |
| Site et mandat opérateur | Déterminer le portefeuille et la capacité de modification | Toutes les références sont résolues dans le site autorisé |
| Page et occurrence | Cible du canvas, du calque et de l’inspecteur | Une sélection utilise l’identité canonique de l’occurrence, y compris si deux blocs portent le même libellé |
| Origine | Vierge, modèle versionné ou correspondance Figma confirmée | Les commandes agissent sur le même modèle de brouillon |
| Tête lue, saisie locale, révision enregistrée | Distinguer modification locale et sauvegarde | Une écriture concurrente rend la base obsolète. Préserver la saisie et proposer une reprise explicite |
| Révision de l’aperçu, état et page | Expliquer quelle version a été rendue | Un résultat périmé ou indisponible est identifié avant toute action qui dépend du rendu |
| Format, panneau, sélection, focus | Représenter l’état de travail de l’opérateur | Le changement de largeur du viewport ne modifie pas à lui seul le document |

Les transitions à spécifier pour l’intégration sont ouverture, sélection, édition, annulation, sauvegarde acceptée ou conflictuelle, préparation d’aperçu et retour. L’aperçu simulé sert à examiner ces transitions. UI-003-02 devra obtenir le document privé du moteur et qualifier la correspondance de sélection dans son iframe isolée. UI-003-03 appliquera les commandes au service compétent et vérifiera leurs effets après relecture. Le contrat [INTERACTIONS.md](INTERACTIONS.md) précise les commandes selon le mode d’entrée.
