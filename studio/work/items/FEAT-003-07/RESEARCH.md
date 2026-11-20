# État du dépôt avant le portail

La carte 07 demande un dépôt sans compte, plusieurs versions pour une même invitation et un signalement interne. La décision Visual Builder V2 rattache chaque dépôt à une provenance utilisable par le lot 08. Le lot 08 devra obtenir ses propres autorisations Figma, proposer des correspondances avec la bibliothèque et faire accepter la traduction par l’opérateur. Un dépôt peut porter sur une seule maquette. [Carte de cadrage](https://app.notion.com/p/41d49e23bbdb8121912bd62c7f557c09) · [Contrat du lot 08](https://app.notion.com/p/41d49e23bbdb81c0b724f655557db7d9) · [Décision produit](https://app.notion.com/p/41d49e23bbdb81e8b4afd6205adc8539)

| Surface examinée | Élément réutilisable ou travail à prévoir |
|---|---|
| FEAT-001 et FEAT-002, dépendances du Kanban | Le groupe Opérateurs Studio, le compte actif et les mandats explicites gouvernent la console. Le registre distingue un mandat Client d’un mandat Site. L’archivage d’un client conserve l’accès aux sites déjà attribués. Ajouter les commandes d’invitation à la fiche Site avec ces mêmes contrôles et une entrée publique dédiée. [Accès](../../../workspace/access.py) · [Services du registre](../../../registre/services.py) · [Guide](../../../docs/REGISTRE.md) |
| Transactions d’autorisation | La commande de gestion des mandats et les mutations de composition verrouillent d’abord l’utilisateur. La composition relit appartenance au groupe, site et mandat dans la transaction. Réutiliser cette discipline pour créer/révoquer, sans écrire de révision de composition. [Mandats](../../../registre/management/commands/registre_access.py) · [Brouillon](../../../composition/services.py) |
| Routage et exploitation | Django possède déjà le middleware CSRF et les sessions de la console. Le projet monte les écrans privés et des ressources locales. L’hôte et le port par défaut sont limités à la boucle locale. Définir le parcours public et son origine de diffusion avant utilisation par un graphiste externe. [Routes](../../../central/urls.py) · [Configuration](../../../central/settings.py) · [Compose](../../../compose.yaml) |
| Dépôts et signaux | L’inventaire des applications installées et de leurs modèles ne présente aucun registre de dépôts, aucune boîte de notifications graphiste et aucun fournisseur de droits Figma. Une liste de soumissions triées, rattachée à la fiche Site et à son habilitation, fournit le premier signal de dépôt. [Applications](../../../central/settings.py) · [Modèles du registre](../../../registre/models.py) |
| Passage au 08 | Le socle de composition accepte déjà une origine nommée Figma sous la forme d’une référence et d’une version opaques, résolues par un fournisseur local. L’éditeur refuse actuellement un démarrage Figma direct. Le 07 fournit les coordonnées d’une soumission. Le 08 produira la proposition acceptée qui permettra de créer le brouillon. [Création de révision](../../../composition/services.py) · [Éditeur](../../../composition/editor.py) · [Contrat parent](../FEAT-003/ARCHITECTURE.md) |

## Vérification de l’existant

Le 19 novembre 2026, les suites existantes du registre, des accès et de la composition ont été exécutées dans une base SQLite de test en mémoire. Django a découvert 29 tests, dont 26 réussis et 3 réservés à un moteur avec verrouillage de lignes. Elles exercent notamment le maintien des mandats Site après archivage du Client, la rétrogradation des droits, la copie d’une source Figma déjà acceptée par un résolveur de test et le refus de la création Figma dans l’éditeur. Les essais spécifiques des nouveaux jetons, du portail et des transactions PostgreSQL sont planifiés dans la [tasklist](TASKLIST.md).

Commande exécutée depuis le dossier Studio.

```sh
docker compose exec -T web python manage.py test tests.test_registre_grants tests.test_registre_web tests.test_composition_services tests.test_editor_web --settings=central.test_settings
```

L’échange du lien avec un destinataire externe et la politique d’effacement demandent une qualification d’exploitation. La maquette peut être examinée sur des données fictives en attendant cette qualification. [Protection des données du registre](../FEAT-002/PROTECTION-DONNEES.md)
