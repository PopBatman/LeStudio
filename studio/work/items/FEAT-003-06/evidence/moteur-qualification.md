# Qualification du moteur et de la passerelle

Le 19 novembre 2026, deux sites fictifs ont démarré chacun un moteur PostgreSQL/Wagtail 7.4.4, une administration humaine et une passerelle nginx exigeant un certificat client propre au site. Le Studio de recette a effectué les lectures depuis ses réseaux de gestion. Les deux moteurs ont servi la page native 4 avec le même jeton publié initial `2`.

| Exercice exécuté | Résultat observé |
| --- | --- |
| Connexion humaine à chaque administration, création et publication par soumission du formulaire Article avec session et CSRF | Redirection Wagtail vers l’explorateur. Les deux articles sont lisibles sur leur instance respective. |
| Nouvelle révision de travail par soumission du formulaire éditeur | Le jeton retourné pour A reste `2`. |
| Compte témoin ayant accès à l’administration et aucun droit sur la branche | Wagtail refuse la lecture du formulaire et la publication. Un test vérifie le titre préservé après POST avec CSRF valide. |
| Requêtes TLS de Studio avec les identités de site et d’instance inversées séparément, puis le certificat de l’autre site | Chaque tentative donne le diagnostic éditorial indisponible. |
| Page de diagnostic, identifiant absent, restriction de connexion sur l’ancêtre, racine étrangère imbriquée et dépublication | Même refus `inaccessible`. Retirer la restriction ou la racine de recette rend le jeton publié à nouveau lisible. Le test moteur couvre aussi deux sites partageant la même racine. |
| Moteur B suspendu pendant une lecture à travers sa passerelle TLS | Expiration après 10,01 secondes, résultat indisponible. Moteur repris après la mesure. |
| Ancienne image ARCH-002 réelle sur troisième base, avec son certificat et ses quatre routes | Diagnostic confirmé, aucune capacité éditoriale annoncée. |
| Montée de version depuis une autre base initialisée par cette ancienne image vers l’image qualifiée | Migration appliquée, jeton de la page de diagnostic conservé, aucune migration manquante. La nouvelle administration répond sur la boucle locale, rend le corps public de l’article et le connecteur confirme la publication par TLS. |
| Tests automatisés moteur sur PostgreSQL | 5 réussites, dont publication native, refus d’édition et de publication et filtration du jeton. |
| Tests transport, mandat et raccordement ciblés côté Studio sur SQLite | 14 tests découverts, 13 réussites, 1 test concurrent réservé à PostgreSQL. |

Le test de transport initial échouait faute de fonction de lecture. Le premier contrôle du modèle constatait l’absence d’ArticlePage. Le client valide le type, les deux identités, la page et la chaîne décimale de révision. Les tests de contrat rejouent les entrées invalides, le délai et la limite de 16 Kio.

L’image initiale de l’exercice à deux sites porte le digest `sha256:e4f802c7c758a12694c0be9a363764b3038e61d8dc3f1f13edfc0068c7cb6768`. L’image finale, incluant le gabarit public utilisé par l’aperçu et le filtre de type exact, porte le digest `sha256:1369717cc26dbc26288ebf30a50c01c21e9fb6077a7ad1fd7d3837f503623c71`. L’image historique essayée porte le digest `sha256:0850616d25a5d9e7fdb98ffbcd57d91735ea622efc317c375e3648bd7ceec80a`.

[Configuration de l’instance et de l’administration locale](../../../../engine/lab/README.md)
