# TDD et tests de comportement

Le TDD est utilisé pour les invariants, permissions, transitions, transformations et erreurs testables. Les travaux purement documentaires ou cosmétiques ont des contrôles adaptés.

| Étape | Preuve attendue |
|---|---|
| RED | Un scénario issu de l’exigence échoue pour la raison attendue |
| GREEN | L’implémentation satisfait ce scénario et les vérifications affectées |
| REFACTOR | Une amélioration utile conserve les comportements vérifiés |
| Intégration | Les composants fonctionnent ensemble dans le contexte pertinent |

Un échec d’import ou de configuration ne prouve pas un RED métier. Les assertions portent sur des résultats observables ; elles ne recopient pas l’implémentation.

Conserver le résultat RED et sa révision. Lorsque le GREEN courant le remplace, marquer la preuve RED `active: false` dans `task.json` et consigner ce remplacement ; ne pas changer son résultat observé en réussite. Les anciennes révisions suivent la même règle. Une preuve active en échec ou non exécutée empêche de satisfaire le contrôle qui exige ce type, même si une autre preuve est passée. Un test de refus qui confirme correctement le comportement attendu est un test réussi, pas un échec à archiver.

## Scénarios prioritaires

- Action permise et action refusée selon acteur, ressource et contexte.
- Entrée invalide, état incompatible, doublon et modification concurrente.
- Erreur de connecteur, délai dépassé et résultat distant incertain.
- Migration et conservation des données lorsque le lot les modifie.
- Intégration des formulaires et réponses serveur.

Distinguer simulations, essais locaux et qualification distante. Conserver les preuves dans [EVIDENCE.md](../templates/EVIDENCE.md) et appliquer [TESTING-POLICY.md](../governance/TESTING-POLICY.md).

Ne pas élargir les tests sans risque concret restant. Après une modification, relancer les vérifications touchées.

