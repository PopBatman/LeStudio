# Développement

## Préparation

Lire le mandat, la spécification, les décisions, la tasklist et les instructions du dépôt. Vérifier les fichiers existants et les capacités réellement disponibles. Consigner les inconnues avant de les transformer en comportement.

## Conventions

| Type | Responsabilité |
|---|---|
| Feature | Cas d’usage, règles métier, permissions et données |
| Connecteur | Traduction vers une capacité externe, erreurs et garanties |
| UI | Présentation, états et interactions à partir de données préparées |

Appliquer [ARCHITECTURE-CONTRACTS.md](../../studio/docs/ARCHITECTURE-CONTRACTS.md). Préserver les frontières entre Studio, moteur et Workspace. Une configuration n’exécute pas de code arbitraire.

## Exécution

1. Traiter une tranche cohérente de la tasklist.
2. Appliquer le TDD quand il apporte une preuve de comportement.
3. Implémenter les cas d’usage et leurs points d’entrée.
4. Vérifier l’intégration et les effets sur les données.
5. Corriger les défauts dans le même mandat et mettre à jour les preuves affectées.
6. Préparer le diff et les éléments nécessaires à la revue.

Déléguer les travaux indépendants avec le [contrat de délégation](../templates/DELEGATION.md). Utiliser les capacités de sous-agents du runtime si elles existent ; une succession de rôles dans la même exécution n’est pas une revue indépendante.

Ne pas engager un changement de périmètre, un coût ou un effet externe non autorisé pour finir plus vite. Préparer le résultat concret puis exposer seulement la décision manquante.

