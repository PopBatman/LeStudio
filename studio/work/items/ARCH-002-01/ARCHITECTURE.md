# Contrat de présentation

Le point d’entrée reste la vue site_detail du registre. Elle sélectionne déjà la fiche via sites(request.user) et calcule le droit de gestion avec can_manage. Après ce contrôle, utiliser inspect_link(request.user, site.pk), le service de lecture qu’utilise la commande « raccordement etat ». Traiter une perte d’accès entre les deux lectures avec le même 404 qu’une fiche inaccessible. Le gabarit reçoit uniquement la projection autorisée du résultat. Cette évolution appartient à la fiche Site existante et aux composants UI-001.

| Source centrale | Usage |
|---|---|
| Site.name, Site.id, Site.domain | Identité de la fiche, UUID dans les détails de gestion, domaine textuel selon FEAT-002 |
| status et attempt.started_at / finished_at | Résultat et date de la tentative. Le service calcule déjà l’expiration d’une tentative ouverte. |
| confirmed.at, confirmed.instance_id, confirmed.profile | Dernier succès, UUID et alias confirmés. Le profil d’une tentative échouée n’est pas conservé comme tel. |
| confirmed.wagtail_version, engine_version, contract_major, contract_minor | Versions observées à la confirmation, affichées individuellement si disponibles. |
| image_digest, attempt.id, actor | Données inutiles au parcours. Omettre du contexte spécifique au panneau. |
| API de gestion, URL publique et URL d’administration | L’origine privée existe dans les profils d’exploitation. Le snapshot ne conserve aucune de ces URL navigateur validées. |

La future vue doit construire une liste explicite des champs présentables. Les valeurs inconnues se traduisent en libellé neutre, les valeurs manquantes restent distinguées d’une erreur réseau. Une version ou un identifiant ne doit jamais être reconstruit à partir du nom du site. Les erreurs du moteur proviennent de la dernière tentative enregistrée. L’ouverture de la fiche et des détails se limite à des lectures centrales, sans lire les fichiers montés.

Les données de ARCH-002 suffisent. Aucun nouveau champ, migration ou endpoint n’est nécessaire. Le navigateur ne contacte pas Wagtail. Tester les effets de bord avec espion sur les appels au connecteur et contrôle de la base avant/après ; conserver les contrôles HTTP et de cache de FEAT-002. Plans de vérification dans la [tasklist](TASKLIST.md).
