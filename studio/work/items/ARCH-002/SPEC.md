# ARCH-002 — Raccordement manuel d’une instance Wagtail

Un opérateur habilité doit pouvoir vérifier que la fiche du site A désigne bien son instance Wagtail A, constater sa disponibilité et reconnaître son contenu dans un rendu technique local. Les décisions fonctionnelles du 18 novembre sont la référence. Les choix de réalisation ci-dessous constituent la proposition de cadrage du 19 novembre. [Carte Notion](https://app.notion.com/p/41c49e23bbdb81cd9f76d83b6f00758e)

**Parcours proposé.** Le gestionnaire sélectionne une fiche existante et une origine proposée par l’administrateur. Depuis le terminal local de confiance, il lance une vérification sous une identité opérateur explicitement désignée et contrôlée. Studio vérifie les droits, interroge l’instance et enregistre localement le résultat. L’opérateur peut relancer le même contrôle. L’exploitation prépare séparément les instances de démonstration et leurs identités. Aucun nouvel écran produit n’est prévu.

| Critère | Preuve à produire lors du développement |
|---|---|
| AC1 — Site indépendant | Créer un site sans domaine ni profil. La fiche reste valide, sans liaison ni trafic moteur. Les sites existants conservent leurs UUID après migration. |
| AC2 — Autorité | Tester opérateur sans mandat, lecteur et gestionnaire du site. Seul le gestionnaire peut lancer le raccordement. Connaître l’UUID ou gérer un site voisin ne suffit pas. |
| AC3 — Identité | Deux instances A et B portent des UUID distincts. Accepter A pour sa fiche. Refuser B à la place de A, y compris si elle utilise la même image et renvoie un état sain. |
| AC4 — Contrat et versions | Vérifier les champs, types, taille et politique de compatibilité. Refuser version inconnue, champ requis absent ou réponse incohérente sur plusieurs lectures. |
| AC5 — Disponibilité | Distinguer état technique dégradé, délai dépassé, accès refusé et identité incorrecte. Un résultat ancien garde sa date. L’état administratif du client et l’état public du site restent indépendants. |
| AC6 — Atomicité | Répéter le contrôle, essayer une autre instance déjà liée, révoquer un mandat pendant le contrôle et lancer deux tentatives concurrentes. Aucune tentative obsolète ne remplace une association confirmée. |
| AC7 — Isolation | Exécuter deux instances d’une même image avec rôles, bases, médias, réglages et éditeurs séparés. Vérifier le cloisonnement des lectures et l’arrêt d’une seule instance. |
| AC8 — Premier rendu | Pour chaque site, lire via Wagtail sa page technique publiée localement et reconnaître son marqueur propre. Une identité correcte accompagnée du contenu de l’autre site échoue au contrôle. |
| AC9 — Effets et preuves | Constater uniquement des lectures API côté moteur, des diagnostics expurgés, des migrations propres à chaque service et des versions reproductibles. Archiver résultats positifs et négatifs des deux instances. |

Les brouillons de configuration relèvent de FEAT-003, les aperçus de FEAT-004 et l’application, l’historique et la restauration contrôlée de FEAT-005. La fiche de raccordement conserve des observations. Elle n’active aucun module et ne publie aucune configuration.
