# Confidentialité et isolation du canvas

## Accès au rendu

Réutiliser les contrôles FEAT-004 de session, site, révision, page, raccordement authentifié et dépendances. L’accès de consultation suffit à sélectionner un bloc dans la page. La préparation existante peut créer un reçu temporaire privé, limité actuellement à dix minutes et douze reçus par opérateur. Ni l’ouverture, ni le changement de format ou de sélection, ni une nouvelle préparation ne doivent changer le brouillon, les contenus Wagtail, la version active ou les droits. Conserver les lectures de révocation et d’échéance à la livraison, pendant l’affichage et au retour dans l’onglet, sans mettre le HTML privé ni les références de session en cache persistant.

## Frontière du document de mesure

La restitution de référence conserve intégralement la politique de FEAT-004. La représentation instrumentée proposée pour le canvas doit être qualifiée séparément. Elle nécessite une autorisation de script précisément limitée à son module immuable par empreinte cryptographique CSP. Conserver une iframe et une politique serveur sandboxées, d’origine opaque, sans accès même origine, navigation de premier niveau, fenêtres, formulaires ou stockage applicatif. Seuls styles et actifs locaux déjà vérifiés sont acceptés ; bloquer les connexions sortantes du document, ainsi que ses sous-cadres. Le module ne contient aucun contenu du site, secret, URL fournisseur ou code importé. Il n’évalue aucun texte comme programme. La vérification du HTML issu du moteur intervient avant instrumentation. L’aperçu normal, le moteur et les contenus Figma ne reçoivent pas cette capacité. Faire examiner les en-têtes effectifs et la fidélité par un exécutant indépendant avant toute intégration.

La coque accepte uniquement le canal de sa propre iframe et la génération active. Une origine opaque ne suffit pas à authentifier un message. Lier l’initialisation à la fenêtre attendue et à une valeur de liaison à usage unique ; remettre au module un canal dédié, sans transmettre cookie, URL de reçu ou secret d’accès. Limiter les échanges aux événements de disponibilité, choix d’UUID et mesure, avec tailles et fréquence bornées, valeurs finies et identités autorisées. La navigation, le remplacement de document, la perte du mandat, l’expiration ou l’échec de vérification ferment le canal, effacent les mesures et ignorent les réponses tardives. Une mesure reçue ne déclenche pas d’écriture ni de requête vers une URL qu’elle fournirait.

## Preuves obligatoires à la réalisation

| Situation | Résultat à observer |
| --- | --- |
| Deux sites, deux sessions, deux blocs partageant un libellé | La sélection revient à l’occurrence de la page admise. Les reçus, ressources et pages du second contexte sont inaccessibles au premier. |
| Révocation, déconnexion, expiration pendant affichage ou réponse tardive | Le contenu privé et le contour disparaissent. Un message oriente vers une nouvelle préparation seulement si le site reste autorisé. |
| Profil moteur, définition, média ou article modifié | La vérification refuse le reçu antérieur ; état et commande de reprise explicites, aucun contenu substitué silencieusement. |
| Module indisponible ou mesures ambiguës | État de sélection spatiale indisponible, calques accessibles sur lecture autorisée, possibilité d’aperçu FEAT-004 valide. |
| Contrôles navigateur | Observer en-têtes, requêtes réseau, isolation de la coque, cycle du canal et disparition des contenus en fin de droit. Exercer clavier, focus, largeurs, défilement et zoom. |
| Absence de publication | Comparer avant/après tête et nombre des révisions Studio, pointeurs de publication et réponse publique Wagtail sur données fictives. Distinguer le reçu technique attendu des écritures éditoriales. |

Les captures de qualification utilisent des sites fictifs et des libellés minimaux. Exclure des pièces partagées les cookies, identifiants de connexion, certificats et URL privées de reçus.
