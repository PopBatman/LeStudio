# Revue indépendante du cadrage

Le 19 novembre 2026, le réviseur `/root/a201_review` a rapproché la [carte Notion](https://app.notion.com/p/41d49e23bbdb81839d40cef2848e3a3a), les modèles et services des lots ARCH-002 et FEAT-002, la [spécification](SPEC.md), le [contrat technique](ARCHITECTURE.md), les [habilitations](SECURITY.md), le [plan de recette](TASKLIST.md) et la [maquette](evidence/maquettes.html).

| Critères | Constat au cadrage |
|---|---|
| AC1 à AC4 | L’état vide, la dernière tentative et le dernier succès sont distincts. La spécification couvre l’expiration sans fin enregistrée, la confirmation partielle et le diagnostic inconnu. Les champs prévus existent dans la fiche et le résultat de `inspect_link`. |
| AC5 à AC8 | Le domaine reste du texte. Les profils privés n’entrent pas dans la lecture. La projection par rôle, le filtrage côté serveur et le refus d’un site hors mandat sont spécifiés. La recette prévoit le contrôle des écritures et des appels au moteur. |
| AC9 | Le réviseur a ouvert la maquette dans Chromium aux largeurs de 320, 390 et 1 440 pixels. Dans le scénario d’échec après confirmation, les deux dates restent lisibles. « Aller au contenu » puis Tab et Entrée permettent d’ouvrir les détails. Les identifiants de l’instance et du profil sont absents du panneau lecteur. Avec le mandat fictif retiré, le panneau disparaît au profit de « Fiche introuvable ». La largeur du document est restée dans la fenêtre et le navigateur n’a émis aucune requête HTTP pendant l’exercice. |

**Avis favorable au cadrage.** L’examen porte sur le contrat proposé et le prototype fictif. La preuve des habilitations Django, des lectures centrales sans effet de bord et de la concordance avec la fiche réelle de tennis-ai relève de la recette de l’implémentation.

## Revue indépendante de la réalisation

Le 19 novembre 2026, le réviseur `/root/impl_review` a examiné le point d’entrée de la fiche, la projection par rôle, le service de lecture central, le gabarit, le CSS et les tests Django.

| Critères | Vérification de la réalisation |
|---|---|
| AC1 à AC4 | Le réviseur a comparé la réponse HTTP 200 de la vue Django pour tennis-ai et le résultat de la lecture centrale, dans une transaction PostgreSQL en lecture seule. La version, l’instance, le profil et les deux horodatages concordent. La suite ciblée couvre aussi la fiche vide, l’échec postérieur, la tentative en cours, l’expiration et les anciennes valeurs partielles. |
| AC5 à AC8 | Le code limite les valeurs présentées par rôle dès la composition du contexte. Le registre conserve son contrôle du site et du client. La fiche présente le domaine en texte et préserve le 404 hors mandat. Le réviseur a relancé les neuf tests de la fiche dans un conteneur privé de réseau avec SQLite en mémoire. Tous ont réussi, y compris le contrôle des requêtes de lecture et de l’absence d’appels au profil et au moteur. |
| AC9 | Le [rapport du parcours navigateur](evidence/produit-navigateur.json) couvre les trois largeurs, l’ouverture et la fermeture des détails au clavier et les parcours de lecture, gestion et refus. Le réviseur a également examiné le [rendu de bureau](evidence/produit-bureau-confirme.png) et le [rendu mobile après échec](evidence/produit-mobile-echec.png). Les deux dates et les détails sont lisibles sur chacun. |

Un point soulevé pendant la revue a été corrigé. Le service de lecture extrait désormais les champs de version connus avant d’ajouter l’identité et la date issues des colonnes persistées. Ainsi, un ancien JSON partiel ou mal formé préserve les données de confirmation faisant autorité.

**Avis favorable à la clôture technique du lot.** La recette porte sur la consultation historique et les habilitations de la fiche.
