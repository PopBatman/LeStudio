# Revue indépendante du cadrage

Exécutant `/root/u304_review`, 20 novembre 2026. La [carte UI-003-04](https://app.notion.com/p/41d49e23bbdb81218933e4095ea7ebe8) demande une comparaison traçable et la reprise de la composition canonique par le même atelier.

## Vérifications sur le socle

- À la confirmation initiale, le service traduit les identifiants de la projection en UUID enregistrés. Lors d’un ajout dans un brouillon existant, le reçu de l’analyse référence la révision de résultat. L’origine de la première révision du site ne suffit donc pas pour retrouver toutes les pages importées. [Confirmation](../../../depots/imports.py) · [Projection des frames](../../../composition/figma_mapping.py)
- Plusieurs frames d’un même groupe peuvent désigner une seule page. L’entrée d’une frame désigne la page et son entrée suffixée `@container` le bloc conteneur. Le rattachement d’une section ou d’une occurrence exige la révision et la page de cet import. Un nouveau bloc ou une copie reçoit son propre UUID. [Correspondances](../../../composition/figma_mapping.py) · [Duplication](../../../composition/builder_batch.py)
- La consultation courante d’une analyse peut relire le fournisseur. Le profil devenu indisponible ou une version modifiée peuvent invalider les détails. L’effacement manuel et la purge à 90 jours retirent la version fournisseur et la table des correspondances. Une ancienne composition garde son document canonique. [Service d’analyse](../../../depots/imports.py) · [Effacement des remises](../../../depots/services.py)
- Le reçu Wagtail est lié au site, à la révision, à la page, à l’opérateur et à sa session. Sa vérification contrôle l’expiration et l’empreinte du rendu. L’approbation d’un écart exige une décision métier distincte et un format identifié. L’audit d’une décision doit rester compréhensible après expiration du reçu. [Vérification du reçu](../../../composition/preview_views.py)

## Examen du dossier et contre-vérification

La [spécification](SPEC.md) et le [contrat technique](ARCHITECTURE.md) couvrent les cinq critères de sortie de la carte. La tâche du composant inconnu a une identité locale. Le gestionnaire atteste le rattachement du PNG à une version et une frame. L’identité de comparaison réunit notamment les empreintes du PNG et du résultat Wagtail, la largeur et le format, le site, la page et la révision. La [sécurité](SECURITY.md) et la [recette prévue](TASKLIST.md) couvrent la portée de chaque mandat, l’effacement du PNG et des notes, le conflit d’écriture et la réouverture d’un import ancien dont les correspondances ont disparu.

Une première lecture de la maquette faisait apparaître l’approbation du bureau en consultant un format mobile dépourvu de frame. L’auteur a corrigé cette portée et ajouté une bascule sur petit écran. Dans Chromium, j’ai rejoué au clavier le parcours à 360 × 800. L’approbation motivée en bureau affiche « Écart approuvé » pour R8. Passer en mobile affiche « Comparaison indisponible » et retire la commande de décision. La correction du titre en bureau affiche R9 avec « À examiner ». L’historique conserve R8. La largeur du document est restée de 360 pixels. Le navigateur n’a enregistré aucune exception JavaScript ni requête HTTP(S) durant cet essai. [Maquette examinée](evidence/maquette.html) · [Revue visuelle](VISUAL-REVIEW.md)

**Avis favorable au passage du cadrage en READY.** Le fonctionnement avec stockage privé du PNG, rendu Wagtail réel, sources purgées et opérateurs concurrents sera vérifié pendant le développement. Les [tests du socle](evidence/socle-postgresql.log) exercent les fonctions déjà livrées.

## Revue de réalisation

L’auteur de la provenance a relu indépendamment le [service de référence et de décision](evidence/revue-service.md). La revue a fait ajouter la révision attendue au contrôle transactionnel du remplacement de PNG. L’auteur du service a vérifié les [routes de comparaison et le retour au canvas](evidence/revue-integration.md). La contre-recette couvre la concurrence, le changement de tête et la purge pendant une vérification du rendu.
