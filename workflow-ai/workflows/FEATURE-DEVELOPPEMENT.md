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

## Passage de la spécification au code

Le développement piloté par la spécification (SDD) prend pour référence la version identifiée de la spécification et les décisions applicables. Relier chaque tranche de la tasklist aux critères d’acceptation concernés avant de développer.

Pour les tranches qui justifient le TDD, transmettre au Test Engineer externe le mandat applicable, la spécification versionnée, la tasklist et la révision de départ. Il remet les tests de référence, leur correspondance avec les critères et la [preuve RED](FEATURE-TDD.md) sur le commit de tests. Codex reprend cette base pour implémenter le comportement et produire les preuves GREEN, puis vérifie les effets d’un refactor éventuel. Appliquer la [politique de tests](../governance/TESTING-POLICY.md) pour toute modification des tests de référence et pour la CI.

Claude Code est l’outil prévu pour le Test Engineer externe après installation autorisée. Si cet exécutant manque, déclarer le mode dégradé et ce qui reste ouvert. Codex peut produire des tests dans le mandat applicable, en indiquant leur provenance. Un passage externe exigé par le lot reste ouvert jusqu’à son exécution.

## Exécution

1. Traiter une tranche cohérente de la tasklist.
2. Appliquer le [cycle TDD](FEATURE-TDD.md) selon la [politique de tests](../governance/TESTING-POLICY.md#choisir-une-vérification-utile).
3. Implémenter les cas d’usage et leurs points d’entrée.
4. Vérifier l’intégration et les effets sur les données.
5. Corriger les défauts dans le même mandat et mettre à jour les preuves affectées.
6. Transmettre le diff et les preuves de la révision finale à la [revue](FEATURE-REVIEW.md).

Appliquer les [règles de délégation](../governance/AGENT-PERMISSIONS.md#délégation) aux travaux confiés à un autre exécutant.

Ne pas engager un changement de périmètre, un coût ou un effet externe non autorisé pour finir plus vite. Préparer le résultat concret puis exposer seulement la décision manquante.

