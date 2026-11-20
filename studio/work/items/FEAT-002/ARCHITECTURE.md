# Modèle du registre et évolution du dépôt

Cette conception technique est proposée pour le Studio central. PostgreSQL est la source de vérité. Le premier incrément réutilise les comptes et le contrôle d’entrée de FEAT-001. Il peut être développé sur données fictives indépendamment du raccordement Wagtail.

## Modèle et contraintes proposés

| Entité | Champs et règles |
|---|---|
| Client | UUID, `client_type` parmi COMPANY, ASSOCIATION, INDIVIDUAL, `display_name` requis (160), dates automatiques `created_at`, `updated_at`, `archived_at` nullable. L’archive est déterminée par cette dernière date. |
| Contact | UUID, FK client obligatoire et protégée, `display_name` (160) et `role` (100) requis, `email` (254), `phone` (32), dates automatiques. Au moins un canal renseigné. Un rôle par fiche, plusieurs contacts du même rôle autorisés. |
| Site du Studio | UUID, FK client obligatoire et protégée, `name` requis (160), type facultatif (80), description facultative (1 000), domaine facultatif (253 en notation ASCII), dates automatiques. L’UUID du site constitue sa clé de contexte logique dès sa création. |
| Mandats client et site | Deux tables avec FK vers le compte Django, FK obligatoire vers l’objet cible et niveau lecture ou gestion. Unicité du couple compte/objet. Les services de la feature appliquent le niveau et la portée. Voir la [matrice](SECURITY.md). |

Longueurs exprimées en caractères, proposées pour le lot. Trimmer les textes avant validation, conserver la casse des noms et refuser les champs requis vides ou composés de blancs. Uniformiser l’absence d’un champ texte facultatif en chaîne vide. Utiliser des clés étrangères, des colonnes requises et des contraintes CHECK pour les types, les niveaux, les libellés obligatoires non blancs et la présence d’au moins une coordonnée non blanche. Les choix du formulaire complètent les contraintes en base.

- **Courriel.** Supprimer les blancs périphériques, valider le format, mettre en minuscules la partie domaine et préserver la partie locale. Aucune vérification par envoi. Si deux canaux sont saisis, valider les deux.
- **Téléphone.** Accepter les chiffres avec séparateurs usuels (espaces, tirets, points, parenthèses) et un éventuel « + » initial. Retirer les séparateurs, exiger de 6 à 15 chiffres et conserver le zéro national ou le préfixe saisi. Le format est une proposition de saisie, sans déduction du pays.
- **Domaine.** Accepter un nom d’hôte sans schéma, chemin, port ni identifiants. Normaliser la casse et le point final, convertir les libellés internationalisés en notation ASCII avant contrôle (63 caractères par libellé, 253 au total). Aucun appel DNS. Le premier lot n’atteste pas la propriété du domaine.
- **Doublons.** Les UUID font foi. Proposer un avertissement non bloquant pour un nom de client similaire ou, dans le même client, un nom de site ou de contact déjà utilisé (égalité après trim et comparaison insensible à la casse). Afficher uniquement les fiches déjà consultables. Ni nom, ni rôle, ni coordonnée, ni domaine ne constitue une clé métier globale. Aucun rapprochement ni transfert automatique.
- **Modifications concurrentes.** Transmettre la version lue (par exemple `updated_at`). Comparer et écrire atomiquement, signaler un conflit si une autre modification est intervenue. Créer la fiche et le premier mandat dans une même transaction. Sérialiser la création d’un enfant avec l’archivage du client. Une seconde demande d’archiver une fiche déjà archivée garde son état et sa date.

## Points d’entrée prévus

L’application de registre portera les modèles, requêtes filtrées, formulaires et services. Les vues Django transmettront acteur et cible au service. L’écran Clients conduira à la fiche, aux contacts et aux actions d’archive. L’entrée Mes sites sera directement accessible au titulaire d’un mandat site. Les formulaires de création d’enfant prendront leur parent depuis le contexte autorisé. En édition, le rattachement sera immuable. Les lectures utiliseront GET et les changements POST avec CSRF, suivis d’une redirection en cas de succès. L’UI réutilisera le gabarit privé et les composants de UI-001.

Le futur rattachement au moteur pourra référencer l’UUID du site. Le contexte logique est établi par l’identité et le filtrage des données. La création d’une fiche ne provisionne aucun environnement physique. Les opérations techniques et l’activation des modules restent extérieures à cette transaction.

## Plan de migration à exécuter pendant la réalisation

1. Enregistrer la nouvelle application et embarquer son paquet et ses migrations dans le contexte de construction Docker. Déclarer la dépendance vers le modèle utilisateur configuré.
2. Créer des tables vides, les contraintes et les index de rattachement/recherche justifiés par les requêtes. Conserver les clés de clients et sites sur les relations protégées. Aucun import des exemples UI-001 ni aucune promotion des comptes de FEAT-001.
3. Sur une base PostgreSQL jetable au niveau FEAT-001, conserver un compte et une session fictifs, appliquer la migration, vérifier les clés, contraintes, mandats vides, connexion et santé. Tester aussi sur base neuve et au second passage.
4. Qualifier la récupération sur une copie jetable. Dès que le registre contient des données, un retour applicatif doit préserver les tables et les fiches. Évaluer une correction en avant ou une restauration contrôlée avant tout retrait de schéma.

Les migrations, l’attribution de droits et le développement appartiennent à la future réalisation. [Contrats d’architecture](../../../docs/ARCHITECTURE-CONTRACTS.md)
