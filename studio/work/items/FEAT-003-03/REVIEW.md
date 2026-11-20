# Revue indépendante du cadrage

Le 19 novembre 2026, l’exécutant `/root/lib_review` a comparé les cinq critères de la carte aux contraintes du parent FEAT-003 et aux points d’entrée du socle livré. [Carte Notion](https://app.notion.com/p/41d49e23bbdb81d69beec505505929a3) · [Architecture du parent](../FEAT-003/ARCHITECTURE.md)

## Points vérifiés dans l’existant

- La validation V1/V2 accepte uniquement la couleur d’accent et l’espacement dans le thème. Elle traite directement le conteneur, le titre et le texte. Pour les autres feuilles, elle recourt à des résolveurs locaux recevant l’identité du site. [Validateur](../../../composition/validation.py)
- Les opérations de navigation préparent aujourd’hui un candidat V2. Le service de sauvegarde et la revalidation après copie contiennent des branches spécifiques à V2. Le développement devra éprouver une modification de menu sur un brouillon enrichi et sa relecture historique. [Opérations de navigation](../../../composition/navigation.py) · [Services](../../../composition/services.py)
- Une feuille de contenu inchangée peut être recopiée lors d’une opération de navigation. Le diagnostic d’aptitude à l’application devra contrôler séparément la disponibilité de ses références, y compris après un retrait de droits sur un média.

## Examen du contrat et du jeu fictif

Les cinq critères Notion disposent chacun d’un cas de recette dans la spécification. Le contrat précise l’identité privée par site, les versions immuables, l’adoption explicite par occurrence et le diagnostic d’un composant ou d’un média indisponible. Il prévoit la conservation des menus lors du premier passage en V3, la relecture des anciens formats, puis la modification d’un menu sur une tête V3. Le bouton initial utilise une destination HTTPS externe. La promotion enregistre la décision et la version globale dans une même transaction après examen du candidat épinglé. [Spécification](SPEC.md) · [Contrat](ARCHITECTURE.md) · [Droits et recette négative](SECURITY.md)

J’ai relu le JSON et résolu ses quatre occurrences sur les deux sites. Le bouton des deux sites utilise respectivement les versions 1 et 2. L’espacement d’occurrence de 8 prime sur le réglage de définition de 12 puis sur le thème de 16. Les deux clés locales « signature » se résolvent vers leur propre site. Chaque menu cible la page du site auquel il appartient. [Fixture examinée](evidence/catalogue.json)

## Examen de la maquette

Dans Chromium 156 à 360 × 740, j’ai activé le lien de saut au clavier, modifié la couleur, enregistré une révision simulée et consulté le diagnostic de version manquante et le mode lecture seule. J’ai aussi soumis un encart local à la revue simulée. La confirmation attendait les deux contrôles, puis la copie « Encart partagé » apparaissait sous le filtre Global. L’encart d’origine conservait sa version locale. La police système et le libellé du diagnostic sont cohérents avec le contrat après correction. L’autorisation serveur, l’examen effectif des droits et les transactions feront l’objet des tests de développement. [Maquette](evidence/maquettes.html) · [Limites et parcours](VISUAL-REVIEW.md)

**Avis favorable au passage en READY pour le cadrage.** La compatibilité effective des données, l’isolation en base et la revue technique de promotion restent des critères de réalisation à vérifier sur l’application.

## Revue indépendante de réalisation

Le 19 novembre 2026, l’exécutant distinct `/root/catalog_review` a relu les points d’entrée du catalogue, les permissions de promotion, les contraintes des versions, la validation V3, les copies avec références privées et les formulaires Django. Les rôles de proposition et de décision sont contrôlés dans le service transactionnel. Les sites conservent leurs épingles après publication d’une version globale. La migration du catalogue et le média livré sont inclus dans le paquet Docker.

Sur une base SQLite isolée migrée, j’ai créé deux sites ayant chacun une définition privée sous la même clé. Après passage de V1 à V3 sur le premier site, j’ai vérifié qu’un enregistrement identique gardait la révision courante. J’ai attribué puis révoqué un média, modifié un menu et constaté que la référence conservée déclenchait toujours le diagnostic. La correction explicite du thème a supprimé ce diagnostic. J’ai relu le menu, la révision historique et le brouillon du second site et vérifié leur intégrité.

Les vérifications ciblées du catalogue, de l’apparence, des vues et de la navigation passent sur SQLite. Deux corrections d’interface issues de la revue ont été relues : la présentation des diagnostics résout désormais directement chaque occurrence par son identifiant, et le choix d’un composant image accepte la présence de propriétés historiques de forme différente sur le bloc à remplacer. Le formulaire permet également de retirer un réglage lié à une définition devenue indisponible. [Tests et preuves](EVIDENCE.md) · [Parcours navigateur de réalisation](evidence/application-navigateur.json)

**Avis de réalisation favorable pour le Studio central local.** L’éditeur général de nouvelles occurrences, le rendu d’une page entière et l’application au moteur ont leurs lots dédiés. La décision de promotion s’appuie sur un examen humain du justificatif enregistré.

### Contrôle final du formulaire d’occurrence

La recette navigateur a relevé une collision entre le nom de contexte du bloc sélectionné et la variable réservée du moteur de templates Django. La vue fournit désormais `occurrence`. Les formulaires de sélection et de confirmation transmettent son UUID. J’ai rejoué les quatre tests web sur une base SQLite isolée après correction. Le test de régression vérifie l’identifiant dans le HTML des deux formulaires et la version effectivement enregistrée. Le [relevé Chromium](evidence/application-navigateur.json) confirme l’adoption explicite du bouton v2 puis la relecture de la variante sur téléphone. Avis favorable confirmé.
