# Données personnelles des clients et contacts

**Statut au 18 novembre 2026.** Procédure proposée pour le référentiel privé de Studio. Le responsable du traitement doit désigner les personnes habilitées, renseigner les critères ci-dessous et faire un exercice sur données fictives avant d’y inscrire des personnes réelles. La [carte FEAT-002](https://app.notion.com/p/41c49e23bbdb81ed98b0c5d404d27dbf) fixe cette condition de mise en service.

## Collecte et visibilité

| Usage | Données utiles | Accès proposé |
|---|---|---|
| Identifier un client et rattacher ses sites | Type, nom d’affichage, identifiants internes et dates. Un nom commercial ou un domaine peut identifier une personne physique. | Opérateur explicitement habilité pour l’opération. La présence d’un site dans une liste autorisée ne donne aucun accès automatique à l’annuaire du client. |
| Joindre la bonne personne | Nom d’affichage, un rôle principal et au moins un moyen de contact. Recueillir les deux coordonnées seulement si leur usage est justifié. | Personnel chargé de cette relation, dans le périmètre client autorisé. Un contact référencé ne reçoit aucun compte. |
| Répondre à l’exercice d’un droit | Référence interne, date, nature de la demande, périmètre, décision motivée et suites. | Référent désigné et exécutant habilité pour le dossier. Notion, tickets de développement et captures reçoivent exclusivement des exemples fictifs. |

Avant la collecte, documenter la finalité, sa base juridique, les destinataires et l’information à fournir, y compris lorsqu’un client transmet les coordonnées d’un tiers. Les champs administratifs facultatifs nécessitent une finalité identifiée. Les champs libres et les journaux doivent exclure les coordonnées superflues et les secrets. [RGPD, articles 5, 6, 13, 14 et 25](https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra)

## Traiter une demande individuelle

1. **Recevoir.** Publier un canal joignable par un particulier ou un contact externe sans compte Studio. Le référent inscrit la date de réception et l’échéance dans un registre restreint. Il accuse réception, identifie le droit demandé et transmet la demande au responsable du traitement si Studio agit comme sous-traitant pour ce périmètre.
2. **Établir l’identité.** Utiliser des éléments déjà connus et proportionnés au risque, par exemple une confirmation par un canal individuel préalablement vérifié. Une boîte fonctionnelle partagée peut être insuffisante. En cas de doute raisonnable, demander uniquement le complément nécessaire. Vérifier le mandat si un tiers agit pour la personne. Limiter l’accès au justificatif éventuellement reçu et l’éliminer dès qu’il cesse d’être nécessaire. [CNIL, répondre à une demande d’accès](https://www.cnil.fr/fr/professionnels-comment-repondre-une-demande-de-droit-dacces)
3. **Délimiter.** Rechercher les occurrences pertinentes dans les fiches actives et archivées et les copies identifiées. Vérifier les homonymes et les rattachements séparément. Un même nom ou courriel saisi chez deux clients ne suffit pas à attribuer les deux fiches à une personne. Faire intervenir le référent habilité lorsqu’une recherche dépasse le périmètre de l’opérateur.
4. **Agir et contrôler.** Pour un accès, préparer les informations requises et une copie intelligible des données de la personne. Protéger les droits des tiers et vérifier le destinataire. Pour une rectification, corriger chaque occurrence confirmée et contrôler le résultat. Pour un effacement, examiner le motif et les exceptions applicables, par exemple une obligation de conservation ou la défense d’un droit en justice. Retirer les données éligibles des usages actifs par une intervention habilitée et vérifiée. Si la dernière coordonnée doit disparaître, traiter la fiche contact entière plutôt que d’y inscrire une valeur fictive. Préserver les sites et les autres contacts. Pour les seules données dont la conservation est justifiée, consigner le motif, les accès restreints et l’échéance de réexamen. L’archivage administratif d’un client laisse ses données présentes. [RGPD, articles 15 à 19](https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra)
5. **Informer et clore.** Répondre dans les meilleurs délais et au plus tard un mois après réception. Lorsque la complexité ou le nombre de demandes le justifie, informer la personne dans ce premier mois des motifs et de la prolongation, de deux mois au maximum. Motiver tout refus et indiquer les voies de réclamation auprès de la CNIL et de recours juridictionnel. En cas de rectification ou d’effacement, aviser les destinataires selon l’article 19 et documenter toute exception. Transmettre la réponse par canal sécurisé, retirer les fichiers de travail, puis inscrire le résultat et la date de clôture. [RGPD, articles 12 et 19](https://eur-lex.europa.eu/eli/reg/2016/679/oj/fra)

## Conservation et restauration

| Support | Déclencheur de revue | Traitement à organiser |
|---|---|---|
| Client et contact | Fin de relation, interlocuteur remplacé, demande individuelle, archivage ou revue périodique | Vérifier la nécessité de chaque donnée. Retirer les données devenues inutiles. Pour toute conservation intermédiaire, limiter données, accès et durée au motif documenté. |
| Journaux et registre des demandes | Fin de la période justifiée par la sécurité ou la preuve du traitement d’une demande | Tracer le minimum utile. Restreindre les accès et planifier la purge. Exclure corps des formulaires, coordonnées recherchées et copies de justificatifs des journaux applicatifs et des URL journalisées. |
| Extrait remis à la personne | Remise ou expiration du moyen de téléchargement | Limiter l’extrait au demandeur vérifié, protéger le transfert et supprimer la copie de travail. Aucun export collectif n’est prévu par le parcours. |
| Sauvegardes | Fin du cycle de rotation ou restauration | Documenter protection, accès et échéance de rotation. Si des copies isolées contiennent une donnée effacée, en maîtriser les accès et la date de disparition. Rejouer les effacements et rectifications intervenus depuis la sauvegarde avant la remise en service. Garder au strict nécessaire les références permettant cette réconciliation. |

Le responsable du traitement fixe et justifie la périodicité de revue, les durées ou critères par finalité, le cycle des sauvegardes et le sort des archives. L’état « archivé » de Studio masque une fiche de la liste courante. Il ne règle ni la date de purge ni les habilitations d’un archivage intermédiaire. [CNIL, durées de conservation](https://www.cnil.fr/fr/passer-laction/les-durees-de-conservation-des-donnees)

## Vérification avant première donnée réelle

Le propriétaire du Studio identifie l’organisme responsable du traitement, le référent, son relais, l’exécutant technique et le canal de réception. Il documente les finalités, les bases juridiques, la notice, les échéances, le mécanisme d’intervention habilitée et le contrôle des restaurations. Ces décisions d’exploitation restent ouvertes au cadrage.

Sur des fiches fictives, rejouer une demande d’accès comportant un homonyme, puis une rectification ou un effacement visant un contact d’un client archivé. Contrôler le contenu remis, les enregistrements restants, les droits sur les autres clients, la traçabilité minimale et le résultat après restauration d’essai. Conserver la date du test et le résultat dans le dossier d’exploitation à accès limité.
