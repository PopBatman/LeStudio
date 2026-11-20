# T01 — Architecture de l’audit

Lire les services, commandes, validation, catalogue, pont isolé, moteurs et leurs consommateurs sans modifier l’application. Les conclusions s’appuient sur les sources locales empreintées et la version réellement exécutée.

L’audit reprend le backend de composition comme propriétaire des données et droits ; le frontend porte gestes/focus/états provisoires ; le moteur raccordé produit l’aperçu de révision. Les ressources de comparaison sont des fichiers de travail isolés. Les lectures opérateur utilisent une session temporaire limitée à un compte déjà habilité au site ; sa valeur n’apparaît dans aucune preuve et elle est supprimée après inspection.

Les options et la décision finale d’organisation frontend sont consignées dans DECISION-FRONTEND.md. Le modèle flux/grille/libre, la migration et le protocole de rendu de travail appartiennent aux contrats T02/T03. L’inventaire T21 distingue l’implémentation d’écran exclusive des services réellement partagés ; aucun retrait par nom de fichier.

Le CLI Workflow AI fourni ne reconnaît que les identifiants parents. Le contrôle local de ce sous-lot utilise un adaptateur documenté qui élargit uniquement la validation d’identifiant dans le processus de vérification, puis appelle les mêmes fonctions de contrôle/empreinte. Le workflow partagé n’est pas modifié.

