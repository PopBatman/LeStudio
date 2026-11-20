# Qualification du moteur commun

Depuis `studio/`, construire l’image et lancer le laboratoire sur un poste avec Docker Compose, Python 3, OpenSSL et suffisamment de ressources pour huit conteneurs locaux.

```sh
docker build -t studio-arch002-engine:qa engine/
python3 -B engine/lab/qualify.py --output /tmp/arch002-qualification.json
```

La commande construit le Studio jetable puis démarre les deux moteurs au même digest OCI. Chaque site a sa base PostgreSQL, son rôle applicatif, son volume média, sa clé Django et son frontal mTLS. Le projet central fournit deux réseaux de gestion privés. Seuls les frontaux et le client central sont membres de ces réseaux. Les ports restent internes. Le certificat de lecture et son autorité sont propres à chaque site.

Les profils, paramètres et certificats de qualification sont produits dans un répertoire temporaire privé. Les autorités privées restent hors des conteneurs. La commande crée ses propres projets Compose à noms aléatoires et supprime leurs volumes à la fin du parcours. Aucun compte, site ou secret du Studio courant n’est utilisé.

Le rapport JSON contient les versions et digests, les refus de raccordement, les observations d’isolement, le résultat de rotation, la récupération d’une base et de son média depuis des copies de qualification, le coût de démarrage et un échantillon de consommation. Les temps de lancement incluent les migrations sur base neuve. Les mesures locales dépendent du poste et de son cache. Le test de restauration arrête le moteur A le temps de prendre les copies cohérentes. La restauration est contrôlée dans une base distincte et un répertoire temporaire sans serveur web exposé.

## Activer les articles et leur administration locale

Construire une image contenant la migration `reference.0002_articlepage`. Sur une instance de recette, appliquer les migrations et relever les sites Wagtail avec `python manage.py shell -c "from wagtail.models import Site; print(list(Site.objects.values('id', 'hostname', 'root_page_id')))"`. Affecter à `EDITORIAL_WAGTAIL_SITE_ID` l’identifiant **du Site Wagtail** vérifié dans cette liste. Laisser cette variable vide conserve le diagnostic initial. Redémarrer le service moteur avec l’image qualifiée et sa passerelle mise à jour.

Pour une administration de développement accessible depuis ce poste, fournir un port libre dans `ENGINE_ADMIN_PORT` du fichier d’environnement de l’instance. Les exemples ci-dessous utilisent l’instance fictive `atelier-a` et un fichier d’environnement préparé par le laboratoire. Depuis `studio/`, exécuter sur cette instance uniquement

```sh
docker compose -p atelier-a --env-file /chemin/atelier-a.env -f engine/lab/instance.yaml -f engine/lab/admin.yaml up -d admin-local
docker compose -p atelier-a --env-file /chemin/atelier-a.env -f engine/lab/instance.yaml -f engine/lab/admin.yaml exec admin-local python manage.py createsuperuser
```

Un administrateur existant peut créer le compte éditeur dans Wagtail et lui attribuer les permissions sur la branche concernée. Avec `ENGINE_ADMIN_PORT=18571`, l’interface se trouve à `http://127.0.0.1:18571/admin/`. Dans le profil administré de cette instance, le champ facultatif `admin_url` reçoit cette adresse complète. En hébergement, employer l’URL HTTPS de l’administration déployée. Le navigateur utilise sa session Wagtail et la passerelle interne conserve son authentification par certificat client.

Dans Studio, rejouer la vérification du raccordement avec le profil mis à jour pour enregistrer la capacité `editorial.published.v1`. Dans Wagtail, créer une page **Article** sous la racine du site, enregistrer et publier selon les droits attribués. Le nombre visible dans le chemin d’édition Wagtail `/admin/pages/4/edit/` est l’identifiant de page à vérifier dans l’atelier Studio. Le moteur retourne seulement les identités attendues et l’identifiant de la révision publiée. Un brouillon enregistré seul garde la révision précédente visible dans Studio.

## Autoriser le rendu privé d’une composition Studio

Utiliser une image moteur contenant les gabarits de FEAT-004 et la passerelle de ce dossier. Dans l’environnement de l’instance, définir `ENGINE_PREVIEW_ENABLED=1`. Pour les articles, renseigner aussi la racine Wagtail comme indiqué ci-dessus.

Le dossier TLS de la **passerelle du site** contient la liste des sujets de certificats clients autorisés à préparer un aperçu. Relever le sujet RFC 2253 du certificat du profil Studio avec `openssl x509 -in /chemin/client.crt -noout -subject -nameopt RFC2253`. Pour le sujet fictif `CN=a-first`, la ligne du fichier `preview-operators.map` est la suivante.

```nginx
"CN=a-first" 1;
```

La passerelle exige à la fois une chaîne valide selon son autorité de lecture et une correspondance du sujet autorisé. Utiliser des sujets distincts pour les lecteurs du diagnostic et les opérateurs d’aperçu, y compris pour la rotation. Si le fichier est absent, le diagnostic continue de fonctionner et le POST d’aperçu est refusé. Appliquer la configuration à l’instance concernée, recharger la passerelle puis revérifier son raccordement dans Studio. L’effet attendu est la capacité `preview.v1` et un rendu lisible par le seul opérateur autorisé sur le site.
