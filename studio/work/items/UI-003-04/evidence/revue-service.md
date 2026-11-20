# Revue indépendante du service de comparaison

L’exécutant `/root/u304_source`, auteur de la résolution de provenance, a relu le service de référence et de décision de `/root/u304_service`, sa migration et son raccordement aux vues HTTP.

La revue a relevé que l’écran proposait le dépôt du PNG sur la tête du brouillon tandis que le service de rattachement ne contrôlait pas la révision affichée. Une nouvelle sauvegarde entre l’ouverture et la confirmation risquait de remplacer le témoin depuis une vue devenue historique. L’auteur a ajouté la révision attendue au contrat d’écriture et la contrôle sous verrou. La lecture de l’historique diffère également les octets PNG et le document complet des révisions.

La contre-recette a utilisé des imports et des acteurs fictifs en base isolée. Elle a exercé trois scénarios complémentaires aux six tests du service. Le rendu du moteur de ces tests est simulé. La preuve de navigateur indépendante utilise ses propres instances.

- Après confirmation d’un écart sur R1 puis création de R2, répéter la décision ou tenter de remplacer la référence depuis R1 signale un conflit. L’image antérieure, l’unique décision passée et la tête R2 ont été relues en base.
- La décision sur la page et celle sur un bloc disposent de leurs propres antécédents. Présenter la décision de page comme antécédent du bloc, ou changer le format mobile en bureau, a été refusé. Les deux décisions valides restent en base.
- Effacer la remise pendant le calcul simulé du rendu a supprimé le témoin et empêché la décision. Le service recontrôle l’éligibilité dans sa transaction finale.

La série du service vérifie la normalisation du PNG, les refus de taille et de format, l’isolement entre sites, la perte du mandat, la rétention, les clés de rejeu et la concurrence de deux gestionnaires. Neuf tests sont passés sur PostgreSQL. Sur SQLite, huit tests sont passés et la course nécessitant les verrous PostgreSQL a été ignorée. La contre-recette et la revue n’ont laissé aucun défaut bloquant dans le service examiné.
