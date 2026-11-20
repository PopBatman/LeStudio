# Plan de développement FEAT-003-02

1. Figer en tests rouges la relecture des révisions V1 et leur première modification en V2. Inclure duplication de brouillon, historique et refus d’une version inconnue.
2. Tester puis étendre les validateurs et les opérations de pages et de menus. Couvrir cycles, collisions, ordre, profondeur, identités, limites et cibles absentes.
3. Tester puis développer le calcul d’impact sur tout le sous-arbre et tous les menus. Tester confirmation, résolution explicite, annulation et brouillon concurrent. Couvrir le retrait d’une entrée portant des enfants et vérifier la conservation du thème, des blocs et des sections des pages conservées.
4. Raccorder les vues spécialisées Pages et Menus aux services de composition. Tester une entrée directe autorisée, un brouillon absent et le retour à la fiche. L’entrée générale de la fiche relève de FEAT-003-04. Vérifier permissions depuis chaque entrée, CSRF, lecture seule et refus inter-site en requêtes directes.
5. Reproduire les parcours des maquettes au clavier, sur téléphone et sur bureau. Vérifier persistance après rechargement et reprise après conflit.
6. Exécuter la suite Studio sur base isolée et qualifier l’absence d’écriture dans le site actif, l’historique et l’isolation. Faire relire le diff et rattacher les preuves de réalisation à la carte.

Le mandat actuel couvre le cadrage et les maquettes. Ces étapes de réalisation restent à exécuter lors du lancement du développement.
