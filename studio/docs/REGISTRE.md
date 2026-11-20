# Accès au registre Clients et sites

Le propriétaire désigne les opérateurs et les fiches qu’ils peuvent gérer. Depuis `studio/`, l’administrateur local crée si nécessaire le compte avec `docker compose exec web python manage.py create_operator IDENTIFIANT`. Un compte actif du groupe « Opérateurs Studio » peut ouvrir son espace de travail. Ses listes métier dépendent des mandats attribués.

## Créer le premier client

Remplacer `IDENTIFIANT` par l’identifiant du compte, puis exécuter la commande suivante.

```bash
docker compose exec web python manage.py registre_access grant IDENTIFIANT create-client
```

Se connecter à [l’espace de travail](http://127.0.0.1:8000/) et ouvrir **Clients**. Choisir **Créer un client**, renseigner son nom et son type. L’auteur reçoit la gestion de cette fiche. Il peut y ajouter des contacts et y créer un site avec un simple nom. La création du site attribue également à son auteur un mandat de gestion sur ce site.

## Attribuer une fiche à un autre opérateur

Utiliser l’UUID de la fiche, visible dans l’adresse de sa page de détail. Remplacer les valeurs en majuscules. Le niveau `read` permet la consultation et `manage` permet aussi la modification. Réexécuter la commande avec le niveau souhaité pour modifier un mandat existant.

```bash
docker compose exec web python manage.py registre_access grant IDENTIFIANT client UUID_CLIENT --level read
docker compose exec web python manage.py registre_access grant IDENTIFIANT site UUID_SITE --level manage
```

La lecture d’un client inclut ses contacts. Les mandats de chaque site sont attribués séparément. Un opérateur limité au site le retrouve dans **Mes sites**. Archiver le client masque sa fiche dans la liste des clients actifs et conserve les habilitations sur ses sites.

## Retirer une habilitation

```bash
docker compose exec web python manage.py registre_access revoke IDENTIFIANT site UUID_SITE
docker compose exec web python manage.py registre_access revoke IDENTIFIANT client UUID_CLIENT
docker compose exec web python manage.py registre_access revoke IDENTIFIANT create-client
```

Le retrait cible l’objet ou la capacité indiquée. Il est possible de retirer un mandat résiduel à un compte désactivé ou sorti du groupe opérateur. Les mêmes commandes peuvent être répétées.

Utiliser des données fictives pour la qualification. Les conditions de passage aux données personnelles réelles et la procédure d’exercice des droits figurent dans le [dossier de protection des données](../work/items/FEAT-002/PROTECTION-DONNEES.md).


## Recevoir une maquette Figma

Dans **Mes sites → fiche Site → Consulter les dépôts Figma**, un gestionnaire peut créer une invitation valable sept jours. Copier le lien avant de quitter l’écran et le transmettre au graphiste par le canal convenu. Le code est aussi disponible pour une saisie manuelle. Si le lien a été perdu, révoquer l’invitation puis en créer une nouvelle.

Le graphiste ouvre le lien, colle l’adresse HTTPS de son fichier de design Figma et, s’il le souhaite, ajoute un commentaire. Une seule maquette suffit. **Transmettre la version** ouvre un reçu daté. **Déposer une autre version** crée une nouvelle remise sous la même invitation. Le numéro du reçu suit les remises dans Studio. Les autorisations de lecture du fichier se gèrent dans Figma.

Sur la fiche Site, **Dernier dépôt Figma** indique la version et la date. Ouvrir l’historique pour consulter une remise. Les gestionnaires peuvent révoquer le lien ou effacer une remise depuis son détail. La révocation ferme aussitôt le formulaire et les reçus de l’invitation. Les versions conservées restent accessibles aux opérateurs habilités du site.

### Adresse de partage et conservation

Sur le poste, l’adresse de partage utilise la boucle locale et le port Studio. Un navigateur sur un autre ordinateur a besoin d’un portail HTTPS joignable. Lors d’une ouverture externe autorisée, renseigner dans la configuration Compose `STUDIO_PORTAL_ORIGIN` avec l’origine complète, et `STUDIO_PORTAL_CONTACT` avec le canal vérifié pour l’effacement. Le frontal conserve le champ Host du portail et expose uniquement `/depot/`, les deux fichiers `/assets/depot-public.css`, `/assets/depot-public.js` et la police `/assets/fonts/dm-sans-latin.woff2`. Le serveur applique également cette séparation sur l’hôte public. Au frontal, journaliser seulement les informations opérationnelles nécessaires. Exclure corps, cookies, référents et paramètres de requête. Le décompte des échanges utilise l’adresse du pair direct. Avec un frontal commun, mesurer le quota partagé avant l’ouverture aux équipes.

Les réglages livrés permettent 20 remises par invitation, dont cinq par fenêtre de dix minutes. Une tentative d’échange du lien est limitée à dix essais sur dix minutes pour la même provenance. La session du portail dure au maximum une heure et se rouvre avec l’invitation encore valide.

Après 90 jours, la remise cesse d’être consultable. Le service Compose `purge-depots` exécute le nettoyage au démarrage et toutes les heures. Après restauration d’une sauvegarde en environnement isolé, rejouer les effacements intervenus depuis la sauvegarde, puis la purge des échéances avant de rouvrir le service. Pour rejouer une décision individuelle, l’opérateur doit disposer du mandat de gestion du site. Les identifiants ci-dessous sont ceux du dossier d’effacement.

```sh
docker compose exec -T web python manage.py purge_depots --operateur OPERATEUR --site UUID_SITE --soumission UUID_REMISE
docker compose exec -T web python manage.py purge_depots
```

Avant collecte réelle, qualifier l’origine de partage, les durées, la notice, les destinataires et la rotation des sauvegardes selon la [procédure de protection des données](../work/items/FEAT-002/PROTECTION-DONNEES.md). Le lot FEAT-003-08 traitera l’analyse autorisée et la proposition de correspondance.

## Importer une remise dans le brouillon

Depuis la fiche Site, ouvrir **Consulter les dépôts Figma**, choisir une remise et utiliser **Analyser la maquette** avec un mandat de gestion. L’atelier donne aussi accès aux remises. Le numéro de remise appartient à Studio. La version affichée après l’analyse identifie le fichier lu chez le fournisseur.

1. Choisir une à huit frames et examiner les correspondances. Chaque ligne indique sa source, ses candidats dans le catalogue du site et les écarts à traiter. Accepter une définition, corriger les propriétés ou écarter la ligne. Vérifier notamment le média autorisé, le texte alternatif, la destination des boutons et les couleurs.
2. Dans **Choisir les pages et formats**, regrouper les frames qui représentent la même page, choisir leur format et une frame de base par groupe. Une vue mobile seule suffit. Le récapitulatif indique les formats absents. Choisir l’accueil d’un nouveau brouillon ou le parent et le segment des pages ajoutées.
3. Ouvrir **Examiner le résultat**, puis **Confirmer l’intégration au brouillon**. Le reçu donne la révision enregistrée et un lien vers la page dans l’atelier. Une confirmation répétée retrouve la même révision. Un changement de version, de catalogue ou de tête du brouillon demande une nouvelle comparaison.

**Configuration par site.** Le service web lit le fichier JSON désigné par la variable `STUDIO_FIGMA_PROFILES`. Monter ce fichier et le fichier du jeton en lecture seule dans le conteneur web. Chaque entrée a pour clé l’UUID de la fiche Site. Exemple fictif de contenu du profil :

```json
{
  "00000000-0000-4000-8000-000000000001": {
    "generation": "1",
    "files": ["FichierDeRecette"],
    "token_file": "/run/studio-figma/lecture",
    "components": {}
  }
}
```

Le jeton de lecture est géré sur le serveur. Chaque clé dans `files` doit être autorisée pour ce site. Les entrées facultatives de `components` associent une clé de composant Figma au triplet Studio `scope`, `key`, `version`. Une rotation ou un changement de périmètre demande une nouvelle revue. La recette du 20 novembre a utilisé un serveur HTTPS simulé et des données fictives. Le poste local peut recevoir des remises sans profil Figma. L’analyse de véritables fichiers demande de configurer et de qualifier leur accès. [Recette de l’import](../work/items/FEAT-003-08/EVIDENCE.md)
