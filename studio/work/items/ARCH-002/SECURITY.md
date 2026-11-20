# Sécurité du raccordement en lecture seule

**Proposition technique du 19 novembre 2026.** La [carte ARCH-002](https://app.notion.com/p/41c49e23bbdb81cd9f76d83b6f00758e) fixe la séparation des instances et la lecture seule. Les contrôles ci-dessous sont à réaliser et à vérifier lors du développement.

## Qui peut agir

Le service Studio reçoit un acteur et l’UUID du site. Il retrouve la fiche dans la portée de lecture de cet acteur avant de restituer un état. Déclencher un contrôle distant ou enregistrer une association requiert le mandat de gestion sur **ce site**. La commande de maintenance est réservée à l’administrateur local de confiance agissant pour l’opérateur identifié. Si elle accepte un nom d’opérateur, l’accès au terminal constitue la frontière de confiance. Réévaluer le mandat lors de la validation finale. Pour l’acteur sans accès au site, la réponse reste indifférenciée entre site absent et site inaccessible. [Services du registre](../../../registre/services.py) · [Matrice des habilitations](../FEAT-002/SECURITY.md)

## Confiance initiale et destination

1. Hors du canal à vérifier, l’administrateur provisionne un profil attribué à un site. Il enregistre son UUID Studio, l’UUID stable attendu de l’instance, l’origine HTTPS exacte (hôte et port), la confiance serveur et la référence du certificat client de lecture. Il configure côté moteur les mêmes identités attendues et le droit de lecture de cette identité cliente. Une réponse de découverte ne peut pas fixer ces valeurs de référence.
2. L’opérateur sélectionne le profil autorisé ou indique l’origine correspondante. Le connecteur compose lui-même les chemins du contrat. Refuser une origine différente, les identifiants dans l’URL, les redirections et les réglages de proxy hérités. Autoriser au niveau réseau uniquement les destinations de gestion provisionnées, y compris après résolution de nom. Appliquer une durée totale et une taille de réponse bornées.
3. Pour chaque lecture, TLS mutuel vérifie le nom et la chaîne du serveur ainsi que l’identité cliente autorisée spécifiquement par l’instance. L’autorité et la correspondance du certificat client sont provisionnées indépendamment de la saisie opérateur. Si un frontal termine TLS, seul ce frontal peut joindre l’interface interne du moteur. Il doit imposer l’autorisation sur les routes de diagnostic et transmettre l’identité vérifiée via un canal privé maîtrisé.
4. Comparer les UUID reçus au couple attendu, puis contrôler contrat, version et santé. Valider une association dans une transaction courte avec unicité du site et de l’instance et contrôle de la révision locale. Une tentative échouée conserve le diagnostic daté et l’éventuelle dernière association vérifiée. Un échec interdit de présenter la tentative comme une confirmation de disponibilité.

Le domaine éditorial facultatif reste distinct de l’origine interne. L’API et le justificatif de lecture donnent accès aux seules lectures prévues. Les réponses du moteur sont traitées comme des données bornées et validées. Le rendu de démonstration est vérifié sur une fixture technique identifiée et ne doit pas être injecté comme HTML de confiance dans Studio.

## Secrets, séparation et rotation

La base centrale conserve une référence opaque de profil. Les clés de service sont provisionnées hors bande sous forme de fichiers d’exécution à accès restreint, en lecture seule pour le processus concerné. La clé privée de l’autorité reste hors des conteneurs. Les accès humains au coffre-fort et aux hôtes restent externes à Studio. Le connecteur opère exclusivement en HTTPS.

Chaque instance possède ses identifiants PostgreSQL limités à sa base, ses volumes de médias, ses réglages, sa clé Django et ses comptes éditeurs. Studio atteint uniquement la façade interne autorisée. Une exposition locale du rendu technique, si nécessaire, est liée à la boucle locale. Les sauvegardes et restaurations doivent conserver le rattachement au site. Une copie démarrée en parallèle reçoit une identité et des justificatifs distincts avant exposition.

Pour une rotation, provisionner le nouveau certificat, autoriser brièvement les deux identités sur la seule instance cible, basculer le profil, revérifier le couple attendu, puis retirer l’ancienne autorisation. En cas de compromission, retirer immédiatement l’autorisation touchée et reprendre la vérification avec des justificatifs renouvelés.

## Diagnostics et vérifications attendues

Conserver une catégorie stable, l’horodatage, l’acteur, le site et une référence de tentative. Distinguer droit insuffisant, authentification du service refusée, communication indisponible, identité incorrecte, contrat incompatible et état dégradé. Limiter la visibilité aux acteurs habilités. Exclure certificats, clés, corps de réponse et contenu éditorial des traces et de Notion.

| Situation sur deux instances fictives A et B | Observation attendue |
|---|---|
| Mandat de lecture seul ou mandat sur le site frère | Aucun appel réseau pour raccorder le site. |
| Certificat expiré, non reconnu, ou justificatif de A présenté à B | Refus de lecture, diagnostic limité, aucun nouveau lien. |
| Profil valide mais UUID de site ou d’instance différent | Refus d’identité, association précédente préservée. |
| Changement d’origine, redirection, réponse excessive ou délai dépassé | Arrêt borné et absence d’association partielle. |
| Deux vérifications concurrentes ou perte du mandat avant validation | Une tentative périmée ne peut écraser la dernière association confirmée. |
| Données, média, compte éditeur et marqueur de rendu propres à A | Vérifier séparément la séparation des bases, volumes, comptes et rendus avec B. |
| Remplacement puis retrait du certificat de lecture | Nouveau certificat accepté pour la même instance, ancien certificat refusé, autres sites inchangés. |
